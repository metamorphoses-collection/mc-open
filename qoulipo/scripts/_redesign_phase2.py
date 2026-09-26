#!/usr/bin/env python3
"""Phase 2 redesigns: 3 design-coupled rebuilds.

  jumeaux_en + jumeaux_fr  — shared designed graph (declared edge list)
  irreplaceable_book       — double-domination graph constructed procedurally
  partition_du_texte (k=4) — re-induce sparser subgraph (or accept k=8, update paper)
"""
import json
import math
import random
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compute_canonical import canonical_metrics

QOULIPO = Path(__file__).resolve().parent / "qoulipo"


def write_metadata_for(folder, canonical_graph, paper_row, mode, extra=None):
    base = QOULIPO / folder
    existing = json.loads((base / "metadata.json").read_text()) if (base / "metadata.json").exists() else {}
    print(f"  computing metrics for {canonical_graph}...")
    m = canonical_metrics(base / canonical_graph, opt_cap=500, time_cap_s=180)
    out = {
        "text_id": existing.get("text_id", folder),
        "title": existing.get("title", folder),
        "lang": existing.get("lang", existing.get("language", "EN")),
        "canonical_N": m["canonical_N"],
        "canonical_graph_file": canonical_graph,
        "canonical_E": m["canonical_E"],
        "canonical_density": m["canonical_density"],
        "canonical_MIS": m["canonical_MIS"],
        "canonical_rho": m["canonical_rho"],
        "canonical_optima": m["canonical_optima"],
        "canonical_optima_cap_reached": m["canonical_optima_cap_reached"],
        "paper_table_row": paper_row,
        "graph_mode": mode,
    }
    for k in ("subtitle", "author", "title_en", "description", "type",
              "designed_property", "register_target", "project", "paper",
              "graph_note", "source_pages", "graph_pages"):
        if k in existing:
            out[k] = existing[k]
    if extra:
        out.update(extra)
    (base / "metadata.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ {folder}: N={m['canonical_N']} E={m['canonical_E']} d={m['canonical_density']} "
          f"MIS={m['canonical_MIS']} ρ={m['canonical_rho']} #opt={m['canonical_optima']}"
          f"{' (cap)' if m['canonical_optima_cap_reached'] else ''}")
    return m


def redesign_jumeaux():
    """Both EN and FR folders deposit the same edge list (graph_target_shared.json).
    Target: paper Table 5 row N=30, d=0.085, MIS=15, ρ=0.304, #opt=68.
    Construction: random 3-regular-ish graph on 30 vertices, ~38 edges → d≈0.087.
    Iterate seeds until MIS ≈ 15."""
    print("\n[jumeaux_en + jumeaux_fr] building shared designed graph (target: N=30, d≈0.085, MIS=15)")
    target_E = 38  # 2*38/(30*29)=0.087
    best = None
    for seed in range(1, 200):
        random.seed(seed)
        nodes = [f"page_{i + 1:02d}" for i in range(30)]
        # Sample target_E random pairs without repetition
        all_pairs = list(combinations(range(30), 2))
        random.shuffle(all_pairs)
        edge_set = set()
        for i, j in all_pairs:
            if len(edge_set) >= target_E:
                break
            edge_set.add((i, j))
        # Try this graph
        from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, value as lpv
        prob = LpProblem("mis", LpMaximize)
        x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(30)]
        prob += sum(x)
        for a, b in edge_set:
            prob += x[a] + x[b] <= 1
        prob.solve(PULP_CBC_CMD(msg=0))
        mis = int(sum(lpv(xi) > 0.5 for xi in x))
        if mis == 15:
            best = (seed, edge_set)
            break
        if best is None or abs(mis - 15) < abs(best[2] if len(best) > 2 else 99):
            best = (seed, edge_set, mis)
    seed, edges_set = best[0], best[1]
    edges = [{"source": f"page_{a + 1:02d}", "target": f"page_{b + 1:02d}"} for a, b in edges_set]
    nodes = [f"page_{i + 1:02d}" for i in range(30)]
    graph = {
        "N": 30, "E": len(edges),
        "density": round(2 * len(edges) / (30 * 29), 4),
        "geometry": "Designed sparse graph shared across EN and FR variants (cross-lingual isomorphism by construction)",
        "source": f"Generated from random seed {seed} targeting N=30, d≈0.085, MIS=15. "
                  "Same edge list deposited in both jumeaux_en/ and jumeaux_fr/ folders.",
        "design_seed": seed,
        "nodes": nodes,
        "edges": edges,
    }
    for folder in ("jumeaux_en", "jumeaux_fr"):
        base = QOULIPO / folder
        (base / "graph_target_shared.json").write_text(json.dumps(graph, indent=2) + "\n")
        write_metadata_for(folder, "graph_target_shared.json",
                           "Les Jumeaux du Graphe", "designed_shared_isomorphic",
                           extra={"designed_property": "Shared designed graph across EN+FR (isomorphic by construction; same edge list)",
                                  "register_target": "2D embedding requires SA",
                                  "twin_of": "jumeaux_fr" if folder == "jumeaux_en" else "jumeaux_en",
                                  "type": "qoulipo_engineered",
                                  "project": "QOuLiPo",
                                  "paper": "Jurczak 2026, arXiv"})


def construct_irreplaceable_book(target_N=50, target_alpha=17, target_E_lo=275, target_E_hi=300, max_attempts=2000):
    """Procedural construction of a graph with:
      - N = target_N
      - MIS = target_alpha (unique)
      - rho = 1.0 (unique optimum)
      - d ≈ 0.234 (E in [275, 300])
      - double domination: every non-MIS vertex has ≥2 MIS neighbours
    Uses pulp ILP for verification."""
    from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, lpSum, value as lpv

    n_mis = target_alpha
    n_off = target_N - n_mis  # 33

    for attempt in range(max_attempts):
        random.seed(attempt)
        edges = set()
        # 1. Each non-MIS vertex connects to k_i MIS vertices, k_i ≥ 2.
        #    Use k_i = 3 for richer double-domination.
        for v_off in range(n_mis, target_N):
            ms = random.sample(range(n_mis), 3)
            for m in ms:
                a, b = sorted((v_off, m))
                edges.add((a, b))
        # 2. Add random edges among non-MIS to fill density.
        target_E = random.randint(target_E_lo, target_E_hi)
        off_pool = list(combinations(range(n_mis, target_N), 2))
        random.shuffle(off_pool)
        for a, b in off_pool:
            if len(edges) >= target_E:
                break
            edges.add((a, b))
        # 3. Verify properties via ILP
        prob = LpProblem("mis", LpMaximize)
        x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(target_N)]
        prob += lpSum(x)
        for a, b in edges:
            prob += x[a] + x[b] <= 1
        prob.solve(PULP_CBC_CMD(msg=0))
        alpha = int(sum(lpv(xi) > 0.5 for xi in x))
        if alpha != target_alpha:
            continue
        sel = frozenset(i for i in range(target_N) if lpv(x[i]) > 0.5)
        # 4. Check uniqueness: forbid this solution and re-solve, must give alpha-1
        prob2 = LpProblem("mis2", LpMaximize)
        y = [LpVariable(f"y{i}", cat=LpBinary) for i in range(target_N)]
        prob2 += lpSum(y)
        for a, b in edges:
            prob2 += y[a] + y[b] <= 1
        prob2 += lpSum(y[i] for i in sel) <= alpha - 1
        prob2.solve(PULP_CBC_CMD(msg=0))
        alpha2 = int(sum(lpv(yi) > 0.5 for yi in y))
        if alpha2 < alpha:
            # Unique optimum — verify double-dom
            adj = {i: set() for i in range(target_N)}
            for a, b in edges:
                adj[a].add(b); adj[b].add(a)
            non_mis = [i for i in range(target_N) if i not in sel]
            ok = all(len(adj[v] & sel) >= 2 for v in non_mis)
            if ok:
                return list(edges), sel, attempt
    return None


def redesign_irreplaceable_book():
    print("\n[irreplaceable_book] procedural construction (target: N=50, MIS=17 unique, ρ=1.0, d≈0.234)")
    base = QOULIPO / "irreplaceable_book"
    result = construct_irreplaceable_book()
    if result is None:
        print("  FAILED: no graph found")
        return
    edges_idx, mis_set, attempt = result
    nodes = [f"p{i + 1:03d}" for i in range(50)]
    edges = [{"source": nodes[a], "target": nodes[b]} for a, b in edges_idx]
    mis_pages = [nodes[i] for i in sorted(mis_set)]
    graph = {
        "N": 50, "E": len(edges),
        "density": round(2 * len(edges) / (50 * 49), 4),
        "geometry": ("Designed double-domination graph: 17 MIS pages (no edges among them); "
                     "each non-MIS page has ≥2 MIS neighbours; uniqueness verified by ILP."),
        "source": f"Procedural construction (attempt {attempt}, ILP-verified MIS=17 unique, double-dom).",
        "design_attempt_seed": attempt,
        "designed_MIS_pages": mis_pages,
        "nodes": nodes, "edges": edges,
    }
    (base / "graph_target.json").write_text(json.dumps(graph, indent=2) + "\n")
    write_metadata_for("irreplaceable_book", "graph_target.json",
                       "The Irreplaceable Book", "designed_double_domination",
                       extra={"designed_property": "Double-domination: every non-MIS page has ≥2 MIS neighbours; unique MIS, ρ=1.0",
                              "register_target": "2D embedding requires SA",
                              "type": "qoulipo_engineered",
                              "project": "QOuLiPo",
                              "paper": "Jurczak 2026, arXiv"})


def redesign_partition_du_texte_k4():
    """Try inducing the graph at k=4 to match paper d≈0.087.
    Since we don't have embeddings stored, fall back to: take graph_k8 induced on
    canonical 50, then prune to keep only the k=4 nearest by some sensible
    proxy. Without saved embeddings this isn't fully reproducible, so the cleanest
    move is to just accept k=8 and flag drift."""
    print("\n[partition_du_texte] graph_k8 induced subgraph keeps d=0.177 (paper d=0.087 was at k=4).")
    print("  Action: keep induced k=8 subgraph as canonical; flag Table 5 drift.")
    base = QOULIPO / "partition_du_texte"
    meta = json.loads((base / "metadata.json").read_text())
    meta["paper_table5_drift_note"] = (
        "Paper Table 5 row claims d=0.087, MIS=20, ρ=0.481, #opt=14 — those numbers are "
        "consistent with a k=4 NLP graph. The deposited graph_k8.json is k=8. The induced "
        "subgraph on canonical 50 pages is N=50, d=0.177, MIS=13, ρ=0.154, #opt=103. "
        "Either: (a) recompute embeddings + build k=4 graph (regenerates instance), "
        "or (b) update Table 5 to k=8 numerics. Currently flagged for paper update."
    )
    (base / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print("  ✓ drift note added")


def main():
    print("Phase 2 redesigns — 3 design-coupled rebuilds\n")
    redesign_jumeaux()
    redesign_irreplaceable_book()
    redesign_partition_du_texte_k4()


if __name__ == "__main__":
    main()
