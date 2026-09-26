#!/usr/bin/env python3
"""Embedder edge-recall + MIS-recovery for all engineered QOuLiPo texts.

Computes, for each of the 22 engineered QOuLiPo folders, the recall and
F1 of the embedder-derived k-NN graph relative to the deposited canonical
graph, plus the size of the MIS recovered from the embedder graph relative
to the canonical MIS.

This is the "aggregate recovery" computation cited in §4.5 of the paper.

v2: handles dict-adjacency graph format and node-id ↔ filename mapping
(p001 ↔ page_001 normalisation).

Output: /tmp/qoulipo_embedder_recall.json (also pushed back to dev_scripts).
"""
import json, re, time
from pathlib import Path
import numpy as np

ROOT = Path("corpus/qoulipo")
MODEL = "intfloat/multilingual-e5-large-instruct"
PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
DEFAULT_K = 8
SKIP = {"pascal_menil_bilayer"}


def parse_graph(g):
    """Return (nodes, edges_set) from any of three formats."""
    if isinstance(g, dict) and "nodes" in g and "edges" in g:
        nodes = g["nodes"]
        if nodes and isinstance(nodes[0], dict):
            nodes = [n.get("id") or n.get("name") for n in nodes]
        edges = []
        for e in g["edges"]:
            if isinstance(e, dict):
                edges.append((e["source"], e["target"]))
            else:
                edges.append((e[0], e[1]))
        return list(nodes), set(tuple(sorted(map(str, e))) for e in edges)
    # Dict-adjacency: {"p1": [neighbours], ...}
    if isinstance(g, dict):
        nodes = list(g.keys())
        edges = set()
        for n, nbrs in g.items():
            if not isinstance(nbrs, list):
                continue
            for m in nbrs:
                edges.add(tuple(sorted(map(str, (n, m)))))
        return nodes, edges
    return None, None


def normalize_node_id(nid):
    """Normalize 'p001', 'p1', 'page_001' → '1' for cross-format matching."""
    s = str(nid)
    m = re.match(r"^(?:page_|p)0*(\d+)$", s)
    return m.group(1) if m else s


def load_source_pages(folder):
    src_dir = folder / "source"
    if not src_dir.exists():
        return None
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(src_dir.glob("*.txt"))}


def solve_mis(n, edges_idx, time_limit=10):
    try:
        import pulp
    except Exception:
        return None
    prob = pulp.LpProblem("mis", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(n)]
    prob += pulp.lpSum(x)
    for a, b in edges_idx:
        prob += x[a] + x[b] <= 1
    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    prob.solve(solver)
    return [i for i in range(n) if pulp.value(x[i]) > 0.5]


def main():
    print(f"Loading {MODEL}...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL)
    print("Loaded.\n")

    results = []
    folders = [d for d in sorted(ROOT.iterdir()) if d.is_dir() and not d.name.startswith("_")]
    folders = [f for f in folders if f.name not in SKIP]

    for folder in folders:
        meta_p = folder / "metadata.json"
        if not meta_p.exists():
            continue
        meta = json.loads(meta_p.read_text())
        if meta.get("source_contract") in ("component", "register_showcase"):
            print(f"[skip] {folder.name}: {meta.get('source_contract')}")
            continue

        N_meta = meta.get("canonical_N")
        canonical_MIS = meta.get("canonical_MIS")
        designed_k = int(meta.get("designed_k") or meta.get("k") or DEFAULT_K)
        gf = meta.get("canonical_graph_file")
        try:
            g_raw = json.loads((folder / gf).read_text())
        except Exception as e:
            print(f"[graph-err] {folder.name}: {e}")
            continue
        canon_nodes, canon_edges = parse_graph(g_raw)
        if canon_nodes is None:
            continue
        pages = load_source_pages(folder)
        if not pages:
            continue

        # Smart node-id ↔ filename matching
        norm_to_canon = {normalize_node_id(n): n for n in canon_nodes}
        norm_to_page = {normalize_node_id(p): p for p in pages.keys()}
        common = sorted(set(norm_to_canon.keys()) & set(norm_to_page.keys()),
                        key=lambda s: int(s) if s.isdigit() else 1e9)
        if len(common) < len(canon_nodes) // 2:
            print(f"[align-fail] {folder.name}: {len(common)}/{len(canon_nodes)}")
            continue
        kept = [(norm_to_canon[k], pages[norm_to_page[k]]) for k in common]
        canon_ids, texts = zip(*kept)

        # Embed
        t0 = time.time()
        emb = model.encode([PREFIX + t for t in texts], normalize_embeddings=True,
                           show_progress_bar=False, batch_size=8)
        sim = emb @ emb.T
        n = len(canon_ids)
        recovered = set()
        for i in range(n):
            order = np.argsort(-sim[i])
            cnt = 0
            for j in order:
                if j == i: continue
                recovered.add(tuple(sorted((canon_ids[i], canon_ids[j]))))
                cnt += 1
                if cnt >= designed_k: break

        canon_named = set(tuple(sorted(map(str, e))) for e in canon_edges)
        kept_set = set(canon_ids)
        canon_named = set(e for e in canon_named if e[0] in kept_set and e[1] in kept_set)

        if canon_named:
            tp = len(recovered & canon_named)
            recall = tp / len(canon_named)
            precision = tp / max(len(recovered), 1)
            f1 = 2 * recall * precision / max(recall + precision, 1e-9)
        else:
            recall = precision = f1 = float("nan")

        id_to_idx = {nid: i for i, nid in enumerate(canon_ids)}
        edges_idx = [(id_to_idx[a], id_to_idx[b]) for a, b in recovered
                     if a in id_to_idx and b in id_to_idx]
        rmis = solve_mis(n, edges_idx, time_limit=10)
        mis_recovery = (len(rmis) / canonical_MIS) if (rmis and canonical_MIS) else float("nan")

        dt = time.time() - t0
        results.append({
            "folder": folder.name, "N": n, "k": designed_k,
            "canonical_MIS": canonical_MIS, "canonical_E": len(canon_named),
            "recovered_E": len(recovered),
            "edge_recall": recall, "edge_precision": precision, "edge_f1": f1,
            "recovered_MIS": len(rmis) if rmis else None,
            "mis_recovery_ratio": mis_recovery, "elapsed_s": round(dt, 1),
        })
        print(f"{folder.name:40s} N={n:>3d} k={designed_k:>2d} "
              f"recall={recall:.3f} F1={f1:.3f} MIS_rec={mis_recovery:.3f} ({dt:.1f}s)")

    if results:
        rs = [r["edge_recall"] for r in results if not np.isnan(r["edge_recall"])]
        f1s = [r["edge_f1"] for r in results if not np.isnan(r["edge_f1"])]
        mrs = [r["mis_recovery_ratio"] for r in results if not np.isnan(r["mis_recovery_ratio"])]
        print(f"\n=== AGGREGATE OVER {len(results)} TEXTS ===")
        print(f"edge recall: mean={np.mean(rs):.3f} median={np.median(rs):.3f} range [{min(rs):.3f}, {max(rs):.3f}]")
        print(f"edge F1:     mean={np.mean(f1s):.3f} median={np.median(f1s):.3f}")
        print(f"MIS recovery: mean={np.mean(mrs):.3f} median={np.median(mrs):.3f}")

    out = Path(__file__).parent / "qoulipo_embedder_recall.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
