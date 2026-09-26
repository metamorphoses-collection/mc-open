#!/usr/bin/env python3
"""Embed the v2 Friar pages, build k-NN graphs at k in {3,5,8}, and
check recovery of the designed dodecahedron adjacency.

Uses intfloat/multilingual-e5-large-instruct (the paper's canonical embedder),
cosine threshold 0.78, symmetrised k-NN (union).

Writes:
  graph_k3.json, graph_k5.json, graph_k8.json  (canonical k-NN graphs)
  recovery_report.json                          (per-k TP/FP/FN + MIS stats)
  recovery_report.txt                           (human-readable summary)
"""
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).resolve().parent
FRIAR = HERE.parent                    # corpus/qoulipo/friars_notebook/
SOURCE = FRIAR / "source"
DESIGNED = FRIAR / "graph_designed.json"

MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
INSTRUCT_PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
SIM_THRESHOLD = 0.78
KS = [3, 5, 8]


def load_pages():
    pages = []
    for i in range(1, 21):
        f = SOURCE / f"page_{i:03d}.txt"
        raw = f.read_text(encoding="utf-8").strip()
        # Strip trailing "[v2 motifs: ...]" metadata line so the embedding
        # sees only the prose.
        lines = raw.splitlines()
        if lines and lines[-1].startswith("[v2 motifs:"):
            lines = lines[:-1]
            # also drop trailing blank
            while lines and not lines[-1].strip():
                lines.pop()
        text = "\n".join(lines)
        pages.append((f"page_{i:03d}", text))
    return pages


def build_kNN(sim, k, names, threshold):
    """Symmetric k-NN (union): edge (i,j) if j in top-k of i OR i in top-k of j,
    AND cos >= threshold."""
    N = len(names)
    # rank neighbours per node (exclude self)
    neigh = []
    for i in range(N):
        order = np.argsort(-sim[i])
        order = [j for j in order if j != i][:k]
        neigh.append(set(order))
    edges = set()
    for i in range(N):
        for j in neigh[i]:
            if sim[i, j] < threshold:
                continue
            a, b = (i, j) if i < j else (j, i)
            edges.add((a, b))
    # symmetrise by union (already covered — we add both directions)
    return sorted(edges)


def mis_ilp(N, edges):
    """Return (mis_size, list_of_all_max_independent_sets).
    Uses brute-force 2^N for N<=22."""
    adj = [[False]*N for _ in range(N)]
    for a, b in edges:
        adj[a][b] = True
        adj[b][a] = True
    best = 0
    all_max = []
    # enumerate in increasing popcount for a bit of pruning
    for mask in range(1 << N):
        if bin(mask).count("1") < best:
            continue
        # check independence
        ok = True
        bits = [i for i in range(N) if mask >> i & 1]
        for i, j in combinations(bits, 2):
            if adj[i][j]:
                ok = False
                break
        if not ok:
            continue
        size = len(bits)
        if size > best:
            best = size
            all_max = [tuple(bits)]
        elif size == best:
            all_max.append(tuple(bits))
    return best, all_max


def compute_rho(all_max):
    if not all_max:
        return 0.0, 0
    common = set(all_max[0])
    for s in all_max[1:]:
        common &= set(s)
    size = len(all_max[0])
    return len(common) / size if size else 0.0, len(common)


def main():
    print(f"[{time.strftime('%H:%M:%S')}] loading pages from {SOURCE}", flush=True)
    pages = load_pages()
    names = [n for n, _ in pages]
    texts = [INSTRUCT_PREFIX + t for _, t in pages]
    print(f"  {len(pages)} pages, avg chars={np.mean([len(t) for _,t in pages]):.0f}", flush=True)

    print(f"[{time.strftime('%H:%M:%S')}] loading model {MODEL_NAME}", flush=True)
    model = SentenceTransformer(MODEL_NAME)
    print(f"[{time.strftime('%H:%M:%S')}] embedding...", flush=True)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False,
                       batch_size=8)
    print(f"  embeddings shape={emb.shape}", flush=True)

    print(f"[{time.strftime('%H:%M:%S')}] computing cosine", flush=True)
    sim = cosine_similarity(emb)
    np.fill_diagonal(sim, -1.0)  # exclude self

    # designed reference
    designed = json.loads(DESIGNED.read_text())
    desigedges = {tuple(sorted((int(e["source"][5:])-1, int(e["target"][5:])-1)))
                  for e in designed["edges"]}

    report = {"model": MODEL_NAME, "threshold": SIM_THRESHOLD, "N": 20,
              "designed_edges": len(desigedges), "k_results": {}}

    for k in KS:
        edges = build_kNN(sim, k, names, SIM_THRESHOLD)
        edge_set = set(edges)
        tp = len(edge_set & desigedges)
        fp = len(edge_set - desigedges)
        fn = len(desigedges - edge_set)
        density = 2 * len(edges) / (20*19)
        mis_size, all_max = mis_ilp(20, edges)
        rho, intersect_size = compute_rho(all_max)

        out = {
            "k": k, "num_edges": len(edges), "density": round(density, 4),
            "TP": tp, "FP": fp, "FN": fn,
            "precision": tp / (tp+fp) if tp+fp else 0.0,
            "recall": tp / (tp+fn) if tp+fn else 0.0,
            "MIS_size": mis_size,
            "n_MIS_optima": len(all_max),
            "rho": round(rho, 4),
            "intersect_size": intersect_size,
        }
        report["k_results"][str(k)] = out

        # write graph_kN.json in paper format
        graph_json = {
            "text_id": "friars_notebook",
            "version": "v2",
            "k": k,
            "threshold": SIM_THRESHOLD,
            "embedder": MODEL_NAME,
            "N": 20,
            "E": len(edges),
            "density": round(density, 4),
            "nodes": names,
            "edges": [{"source": names[a], "target": names[b]} for a, b in edges],
        }
        (FRIAR / f"graph_k{k}.json").write_text(json.dumps(graph_json, indent=2))
        print(f"  k={k}: E={len(edges)}, d={density:.3f}, "
              f"TP={tp}/{len(desigedges)}, FP={fp}, "
              f"MIS={mis_size}, #opt={len(all_max)}, rho={rho:.3f}", flush=True)

    (HERE / "recovery_report.json").write_text(json.dumps(report, indent=2))

    # human summary
    lines = [
        "Friar's Notebook v2 — embedding recovery report",
        f"  embedder: {MODEL_NAME}",
        f"  threshold: {SIM_THRESHOLD}",
        f"  designed (dodecahedron) edges: {len(desigedges)}",
        f"  target: MIS=8, ρ=0, density=0.158",
        "",
        f"{'k':>3}  {'E':>4}  {'d':>6}  {'TP':>3}  {'FP':>3}  {'FN':>3}  "
        f"{'prec':>5}  {'rec':>5}  {'MIS':>3}  {'#opt':>5}  {'ρ':>5}",
    ]
    for k in KS:
        r = report["k_results"][str(k)]
        lines.append(
            f"{k:>3}  {r['num_edges']:>4}  {r['density']:>6.3f}  "
            f"{r['TP']:>3}  {r['FP']:>3}  {r['FN']:>3}  "
            f"{r['precision']:>5.3f}  {r['recall']:>5.3f}  "
            f"{r['MIS_size']:>3}  {r['n_MIS_optima']:>5}  {r['rho']:>5.3f}"
        )
    (HERE / "recovery_report.txt").write_text("\n".join(lines) + "\n")
    print()
    print("\n".join(lines))


if __name__ == "__main__":
    main()
