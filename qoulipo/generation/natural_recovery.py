#!/usr/bin/env python3
"""
Thread c: natural-text k-NN recovery F1.

For each natural-text graph in our database, load the original book's
per-chapter (or per-page) text from disk, re-embed with e5-large-instruct,
rebuild the k-NN graph at k=8/16/24, and compare against the stored
graph.

High recall means the stored graph is reproducible with the project's
standard embedder — a sanity check for the classical pipeline.
"""

import json
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline_inverse_v2 import metrics, build_knn, embed_pages, MODEL_NAME

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "oulipo" / "natural_recovery_results.json"


# Natural text sources: (display, graph_file, text_source)
NATURAL_SOURCES = [
    {
        "display": "augustine_conf13 (LA) N=22 k=8",
        "graph": "3_MIS/classical/graphs/augustine/graph_Augustine_Conf13.json",
        "text_dir": "3_MIS/classical/reference_texts/latin_texts/augustine_conf13_chapters",
        "text_pattern": "chapter_*.txt",
        "first_n_files": 22,  # Book 13 only = chapters 1..22 of the 38-file dir
    },
    {
        "display": "augustine_conf13full (LA) N=38 k=8",
        "graph": "3_MIS/classical/graphs/augustine_conf13/graph_augustine_conf13_k8.json",
        "text_dir": "3_MIS/classical/reference_texts/latin_texts/augustine_conf13_chapters",
        "text_pattern": "chapter_*.txt",
    },
    {
        "display": "augustine_conf13full (LA) N=38 k=16",
        "graph": "3_MIS/classical/graphs/augustine_conf13/graph_augustine_conf13_k16.json",
        "text_dir": "3_MIS/classical/reference_texts/latin_texts/augustine_conf13_chapters",
        "text_pattern": "chapter_*.txt",
    },
    {
        "display": "lactantius_demort (LA) N=52 k=8",
        "graph": "3_MIS/classical/graphs/lactantius/graph_lactantius_demort_k8.json",
        "text_dir": "3_MIS/classical/reference_texts/latin_texts/lactantius_demort_chapters",
        "text_pattern": "chapter_*.txt",
    },
    {
        "display": "lactantius_demort (LA) N=52 k=16",
        "graph": "3_MIS/classical/graphs/lactantius/graph_Lactantius_DeMort_k16.json",
        "text_dir": "3_MIS/classical/reference_texts/latin_texts/lactantius_demort_chapters",
        "text_pattern": "chapter_*.txt",
    },
    {
        "display": "giambullari_65 (IT) N=65 k=8",
        "graph": "3_MIS/classical/graphs/giambullari/graph_giambullari_65.json",
        # Uses the full topic_graph.json since nodes carry text
        "from_topic_graph": "3_MIS/classical/graphs/giambullari/topic_graph.json",
    },
    {
        "display": "giambullari_155 (IT) N=155 k=8",
        "from_topic_graph": "3_MIS/classical/graphs/giambullari/topic_graph.json",
        "use_full_topic_graph": True,
    },
]


def load_chapter_texts(source):
    """
    Return (node_ids, texts) for a natural text.
    Three modes:
      - text_dir + text_pattern: read chapter_NN.txt files
      - from_topic_graph: use the topic_graph.json node 'text_full' field
    """
    if "text_dir" in source:
        text_dir = BASE.parent / source["text_dir"]
        files = sorted(text_dir.glob(source["text_pattern"]))
        first_n = source.get("first_n_files")
        if first_n is not None:
            files = files[:first_n]
        # Use the graph file's node order as the canonical order so that
        # stored edges resolve correctly. Then pair each graph node with
        # the corresponding chapter text by position: graph node 0 ↔
        # alphabetical position 0 among text files, etc.
        graph_file = source.get("graph")
        if graph_file:
            g = json.loads((BASE.parent / graph_file).read_text())
            raw = g.get("nodes", [])
            graph_ids = [n["id"] if isinstance(n, dict) else n for n in raw]
            # Augustine uses "p0","p1","p10",..."p21" (alphabetical order).
            # Lactantius uses "chapter_01",..."chapter_52" (also alphabetical).
            # In BOTH cases, the alphabetical order matches the file sort
            # order one-to-one as long as the number of files equals the
            # number of nodes. Verify and pair.
            if len(graph_ids) != len(files):
                raise RuntimeError(f"nodes ({len(graph_ids)}) != files ({len(files)})")
            node_ids = graph_ids  # use the GRAPH's IDs as canonical
            # Reorder files to match graph_ids order. For "pN" scheme,
            # the graph sort puts p0,p1,p10,p11,...,p2,p20,p21,p3,... so
            # we need to map each "pN" to chapter_{N+1:02d}.
            # For "chapter_NN" scheme we can just use file stems 1:1.
            if graph_ids[0].startswith("p") and graph_ids[0][1:].isdigit():
                # Map "pN" to files[N] by numeric index into sorted files
                file_by_idx = {i: f for i, f in enumerate(files)}
                paired = []
                for gid in graph_ids:
                    num = int(gid[1:])
                    paired.append(file_by_idx[num])
                files = paired
            else:
                # chapter_NN scheme: files already sorted alphabetically
                # to match graph_ids
                pass
        else:
            node_ids = [f.stem for f in files]
        texts = [f.read_text(encoding="utf-8", errors="ignore").strip()
                 for f in files]
        return node_ids, texts
    elif "from_topic_graph" in source:
        tg = json.loads((BASE.parent / source["from_topic_graph"]).read_text())
        node_ids = []
        texts = []
        for n in tg["nodes"]:
            nid = n["id"] if isinstance(n, dict) else n
            txt = (n.get("text_full") or n.get("text") or n.get("preview") or "") if isinstance(n, dict) else ""
            if txt and len(txt) > 30:
                node_ids.append(nid)
                texts.append(txt)
        return node_ids, texts
    else:
        return [], []


def load_stored_edges(graph_file, node_ids=None):
    g = json.loads((BASE.parent / graph_file).read_text())
    nodes = g.get("nodes", [])
    edges = g.get("edges", g.get("links", []))
    # Reconcile node ids: graph file nodes might be dicts or strings
    if isinstance(nodes[0], dict):
        graph_ids = [n["id"] for n in nodes]
    else:
        graph_ids = list(nodes)
    if node_ids is None:
        node_ids = graph_ids
    idx = {n: i for i, n in enumerate(node_ids)}
    stored = set()
    for e in edges:
        if isinstance(e, dict):
            u, v = e["source"], e["target"]
        else:
            u, v = e[0], e[1]
        if u in idx and v in idx:
            ii, jj = idx[u], idx[v]
            stored.add((min(ii, jj), max(ii, jj)))
    return stored, node_ids


def main():
    results = {}
    for src in NATURAL_SOURCES:
        display = src["display"]
        print(f"\n=== {display} ===")
        try:
            node_ids, texts = load_chapter_texts(src)
            N = len(node_ids)
            if N < 4:
                print(f"  SKIP: only {N} texts loaded")
                continue
            if "graph" in src:
                stored, node_ids = load_stored_edges(src["graph"], node_ids)
            else:
                # use topic_graph edges
                stored, node_ids = load_stored_edges(
                    src.get("from_topic_graph") or src["graph"], node_ids)

            # If using full topic_graph with 155 pages, reload edges against
            # the full node list
            if src.get("use_full_topic_graph"):
                tg = json.loads((BASE.parent / src["from_topic_graph"]).read_text())
                idx = {n["id"]: i for i, n in enumerate(tg["nodes"])}
                stored = set()
                for e in tg.get("edges", []):
                    u = e["source"] if isinstance(e, dict) else e[0]
                    v = e["target"] if isinstance(e, dict) else e[1]
                    if u in idx and v in idx:
                        ii, jj = idx[u], idx[v]
                        stored.add((min(ii, jj), max(ii, jj)))
                node_ids = [n["id"] for n in tg["nodes"]]
                texts = [(n.get("text_full") or n.get("text") or n.get("preview") or "") for n in tg["nodes"]]
                N = len(node_ids)

            density = len(stored) / (N * (N - 1) // 2) if N > 1 else 0
            avg_deg = 2 * len(stored) / N if N > 0 else 0
            k_star = max(2, round(avg_deg))
            print(f"  N={N}  stored_edges={len(stored)}  density={density:.3f}  "
                  f"avg_deg={avg_deg:.1f}  k*={k_star}")

            # Embed
            embeddings = embed_pages(texts)

            k_results = {}
            for k in sorted(set([8, 16, 24, k_star])):
                recovered = build_knn(embeddings, k=k)
                m = metrics(recovered, stored, N)
                k_results[f"k={k}"] = m
                tag = " *" if k == k_star else "  "
                print(f"    k={k:2d}{tag}: recall={m['recall']:.3f} "
                      f"prec={m['precision']:.3f} f1={m['f1']:.3f}")

            results[display] = {
                "display": display,
                "N": N,
                "density": round(density, 4),
                "stored_edges": len(stored),
                "avg_degree": round(avg_deg, 2),
                "k_star": k_star,
                "k_results": k_results,
                "best_f1": max(r["f1"] for r in k_results.values()),
            }
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    OUT.write_text(json.dumps(results, indent=2))
    print("\n\n========== SUMMARY ==========")
    print(f"{'display':<52} {'d':>6} {'best_F1':>9}")
    for name, r in results.items():
        print(f"{name:<52} {r['density']:>6.3f} {r['best_f1']:>9.3f}")
    if results:
        mean_f1 = np.mean([r["best_f1"] for r in results.values()])
        print(f"\nMean natural-text F1 recovery: {mean_f1:.3f}")
    print(f"\nSaved → {OUT}")


if __name__ == "__main__":
    main()
