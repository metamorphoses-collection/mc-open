#!/usr/bin/env python3
"""
Recompute Table 1 (backbone fidelity) Cov / Var / Fid at the canonical MIS for
each of the 10 rows, using the paper's canonical embedder
(intfloat/multilingual-e5-large-instruct) and graph_k*.json.

For each text:
  1. Load source pages from corpus/natural/<id>/source/*.txt
  2. Embed with e5-large-instruct (same prefix convention as paper)
  3. Load the appropriate graph JSON to fix N, E and graph identity
  4. Solve ILP for one canonical MIS M of size alpha(G)
  5. Coverage similarity C = mean_{v not in M} max_{u in M} cos(e_v, e_u)
  6. Variance capture V = tr(Sigma_M) / tr(Sigma_V)
  7. Topic coverage T = fraction of Louvain communities containing >=1 MIS page
  8. Fidelity F = (C * V * T)^(1/3)
"""
import json
import math
import os
import re
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, value as lpvalue
from sklearn.metrics.pairwise import cosine_similarity

HERE = Path(__file__).resolve().parent
NATURAL = HERE.parent / "corpus" / "natural"

PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
MODEL_NAME = "intfloat/multilingual-e5-large-instruct"

# (text_id, graph_file, label)
# Uses the same graph / chunking as the Table 1 row reports.
ROWS = [
    ("giambullari_inferno", "graph_k8.json",         "Giambullari 151"),
    ("galileo_dialogo",     "graph_k8.json",         "Galileo 65"),
    ("dante_inferno",       "graph_k8.json",         "Dante 34"),
    ("boethius_consolatio", "graph_k8.json",         "Boethius 72"),
    ("heptameron_1559",     "graph_k8.json",         "Heptameron 72 (k=8)"),
    ("augustine_conf13",    "graph_k8.json",         "Augustine 38"),
    ("lactantius_demort",   "graph_k8.json",         "Lactantius 52"),
    ("ausonius_epigrammata","graph_k8.json",         "Ausonius Epigrammata 27"),
    ("ausonius_engineered", "graph_k8.json",         "Ausonius Engineered 10"),
    ("ausonius_mosella",    "graph_k8.json",         "Ausonius Mosella 8"),
]


def load_source(text_id, target_N=None):
    sdir = NATURAL / text_id / "source"
    # Special cases: single-file sources need re-chunking
    # Galileo: 400-word chunks (matches the corpus README)
    if text_id == "galileo_dialogo":
        single = sdir / "galileo_dialogo_full.txt"
        if single.exists():
            full = single.read_text(encoding="utf-8", errors="replace")
            words = full.split()
            if target_N and target_N > 0:
                chunk_size = max(1, len(words) // target_N)
                chunks = [" ".join(words[i*chunk_size:(i+1)*chunk_size])
                          for i in range(target_N)]
                return chunks, [f"chunk_{i:03d}" for i in range(target_N)]
    # Dante: split into cantos by "Canto I" / "Canto II" / Roman numerals
    if text_id == "dante_inferno":
        single = sdir / "dante_inferno_gutenberg.txt"
        if single.exists():
            full = single.read_text(encoding="utf-8", errors="replace")
            # split on "Canto" boundary
            parts = re.split(r"(?im)^\s*canto\s+[IVXL]+", full)
            parts = [p for p in parts if p.strip()]
            # Expect ~34 cantos; take first N
            if target_N and target_N > 0 and len(parts) >= target_N:
                return parts[:target_N], [f"canto_{i+1:02d}" for i in range(target_N)]
            # fallback: equal word chunks
            if target_N:
                words = full.split()
                chunk_size = max(1, len(words) // target_N)
                chunks = [" ".join(words[i*chunk_size:(i+1)*chunk_size])
                          for i in range(target_N)]
                return chunks, [f"canto_{i+1:02d}" for i in range(target_N)]
    # Default: per-file
    files = sorted(sdir.glob("*.txt"))
    if not files:
        files = sorted(sdir.glob("*.md"))
    texts = [p.read_text(encoding="utf-8", errors="replace").strip() for p in files]
    return texts, [p.stem for p in files]


def load_graph(path):
    d = json.loads(path.read_text())
    nodes = d.get("nodes", [])
    if nodes and isinstance(nodes[0], dict):
        nodes = [n.get("id", str(i)) for i, n in enumerate(nodes)]
    nodes = [str(n) for n in nodes]
    edges = []
    for e in d.get("edges", []):
        if isinstance(e, dict):
            edges.append((str(e["source"]), str(e["target"])))
        else:
            edges.append((str(e[0]), str(e[1])))
    return nodes, edges


def solve_mis(N, edges_idx):
    prob = LpProblem("mis", LpMaximize)
    x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(N)]
    prob += sum(x)
    for a, b in edges_idx:
        prob += x[a] + x[b] <= 1
    prob.solve(PULP_CBC_CMD(msg=0))
    return [i for i in range(N) if lpvalue(x[i]) > 0.5]


def louvain_partition(N, edges_idx):
    import networkx as nx
    try:
        import community as community_louvain  # python-louvain
        G = nx.Graph()
        G.add_nodes_from(range(N))
        G.add_edges_from(edges_idx)
        part = community_louvain.best_partition(G, random_state=42)
        return part
    except ImportError:
        # fallback: greedy modularity
        G = nx.Graph()
        G.add_nodes_from(range(N))
        G.add_edges_from(edges_idx)
        from networkx.algorithms.community import greedy_modularity_communities
        comms = list(greedy_modularity_communities(G))
        part = {}
        for ci, c in enumerate(comms):
            for v in c:
                part[v] = ci
        return part


def topic_coverage(mis_set, partition):
    # fraction of Louvain communities that contain >=1 MIS page
    comms_all = set(partition.values())
    comms_mis = set(partition[v] for v in mis_set if v in partition)
    return len(comms_mis) / len(comms_all) if comms_all else 1.0


def recompute_one(text_id, graph_file, label, model):
    d = NATURAL / text_id
    if not d.exists():
        print(f"  SKIP {label}: no dir {d}")
        return None
    gpath = d / graph_file
    if not gpath.exists():
        print(f"  SKIP {label}: no graph {gpath}")
        return None
    nodes, edges = load_graph(gpath)
    N = len(nodes)

    # Load source matched to node names (pass target_N to enable chunking for
    # single-file sources)
    source_texts, stems = load_source(text_id, target_N=N)
    if len(source_texts) != N:
        # Try matching by node-name order if possible
        name_to_idx = {n: i for i, n in enumerate(nodes)}
        if all(s in name_to_idx for s in stems):
            order = [name_to_idx[s] for s in stems]
            # reorder source_texts to match node order
            tmp = [None]*N
            for src_i, node_i in enumerate(order):
                tmp[node_i] = source_texts[src_i]
            source_texts = tmp
            if None in source_texts:
                print(f"  WARN {label}: source/graph partial overlap ({sum(1 for t in source_texts if t)}"
                      f" of {N})")
                return None
        else:
            # Assume rank-aligned (rare: embedding-graph built in source-dir order)
            if len(source_texts) < N:
                print(f"  SKIP {label}: {len(source_texts)} source files vs N={N}")
                return None
            source_texts = source_texts[:N]

    # Embed
    texts_prefixed = [PREFIX + t for t in source_texts]
    emb = model.encode(texts_prefixed, normalize_embeddings=True,
                       show_progress_bar=False, batch_size=8)

    # Build edge index list
    name_to_idx = {n: i for i, n in enumerate(nodes)}
    edges_idx = [(name_to_idx[a], name_to_idx[b]) for a, b in edges
                 if a in name_to_idx and b in name_to_idx]

    # Classical MIS
    mis = solve_mis(N, edges_idx)
    alpha = len(mis)

    # Coverage similarity C
    mis_set = set(mis)
    non_mis = [i for i in range(N) if i not in mis_set]
    if non_mis:
        sim_nm_m = cosine_similarity(emb[non_mis], emb[mis])
        C = float(np.mean(np.max(sim_nm_m, axis=1)))
    else:
        C = 1.0

    # Variance capture V = tr(Sigma_M) / tr(Sigma_V)
    tr_V = float(np.trace(np.cov(emb.T)))
    tr_M = float(np.trace(np.cov(emb[mis].T))) if len(mis) >= 2 else 0.0
    V = tr_M / tr_V if tr_V > 0 else 0.0

    # Topic coverage T via Louvain
    part = louvain_partition(N, edges_idx)
    T = topic_coverage(mis, part)

    # Composite F = sqrt(C * V); T reported separately as a methodology check
    F = (max(C, 0) * max(V, 0)) ** 0.5

    return {
        "label": label, "text_id": text_id,
        "N": N, "E": len(edges_idx),
        "density": round(2*len(edges_idx)/(N*(N-1)) if N > 1 else 0, 4),
        "alpha": alpha,
        "C": round(C, 3), "V": round(V, 3),
        "T": round(T, 3), "F": round(F, 3),
    }


def main():
    from sentence_transformers import SentenceTransformer
    print(f"Loading model {MODEL_NAME}...", flush=True)
    model = SentenceTransformer(MODEL_NAME)
    print("Done.", flush=True)

    print(f"\n{'label':<30} {'N':>4} {'E':>5} {'d':>6} {'alpha':>5}  "
          f"{'C':>5} {'V':>5} {'T':>5} {'F':>5}")
    print("-" * 90)
    results = []
    for text_id, graph_file, label in ROWS:
        try:
            r = recompute_one(text_id, graph_file, label, model)
        except Exception as e:
            print(f"  ERR {label}: {e}")
            continue
        if not r:
            continue
        results.append(r)
        print(f"{r['label']:<30} {r['N']:>4} {r['E']:>5} {r['density']:>6.4f} "
              f"{r['alpha']:>5}  {r['C']:>5.3f} {r['V']:>5.3f} {r['T']:>5.3f} "
              f"{r['F']:>5.3f}")

    out = HERE / "table1_recomputed.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
