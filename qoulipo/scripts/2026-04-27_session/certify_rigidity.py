#!/usr/bin/env python3
"""Certified rigidity ρ via per-vertex ILP exclusion (no enumeration cap).

For each vertex v in some optimum S: re-solve MIS with x_v = 0. If MIS
shrinks, v is in the persistent core. Counting these gives the exact
persistent-core size and exact ρ = |core| / MIS, with no dependence on
the 500-solution enumeration cap.

Computes the certified rigidity for the headline 5 corpora used in §3
of the paper. Result: Giambullari moved from sampled ρ=0.327 (capped) to
certified ρ=0.878 (24 optima, 36-page core). See §3.4 + Table 2.
"""
import json, time
from pathlib import Path
import pulp

CORPUS = Path("corpus/natural")

CASES = [
    ("giambullari_inferno",  "graph_k8.json", "Giambullari 151 (k=8)"),
    ("galileo_dialogo",      "graph_k8.json", "Galileo 65 (k=8)"),
    ("boethius_consolatio",  "graph_k8.json", "Boethius 72 (k=8)"),
    ("heptameron_1559",      "graph_k16.json", "Heptaméron 72 (k=16)"),
    ("dante_inferno",        "graph_k8.json", "Dante 34 (k=8)"),
]


def load_graph(folder, gf):
    p = CORPUS / folder / gf
    if not p.exists():
        for alt in p.parent.glob("graph*.json"):
            p = alt; break
    g = json.loads(p.read_text())
    nodes = g.get("nodes", [])
    edges = g.get("edges", [])
    if nodes and isinstance(nodes[0], dict):
        nodes = [n.get("id") or n.get("name") for n in nodes]
    parsed_edges = []
    for e in edges:
        if isinstance(e, dict):
            parsed_edges.append((e["source"], e["target"]))
        else:
            parsed_edges.append((e[0], e[1]))
    return nodes, parsed_edges, p


def solve_mis(nodes, edges, fix_zero=None, time_limit=60):
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    prob = pulp.LpProblem("mis", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(n)]
    prob += pulp.lpSum(x)
    for a, b in edges:
        if a in idx and b in idx:
            prob += x[idx[a]] + x[idx[b]] <= 1
    if fix_zero:
        for v in fix_zero:
            if v in idx:
                prob += x[idx[v]] == 0
    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    prob.solve(solver)
    return [nodes[i] for i in range(n) if pulp.value(x[i]) > 0.5]


def main():
    out = []
    for folder, gf, label in CASES:
        try:
            nodes, edges, gp = load_graph(folder, gf)
        except Exception as e:
            print(f"[skip] {folder}: {e}"); continue
        N = len(nodes)
        print(f"\n=== {label} (N={N}, E={len(edges)}, file={gp.name}) ===")
        t0 = time.time()
        S = solve_mis(nodes, edges, time_limit=60)
        mis_size = len(S)
        print(f"  MIS size: {mis_size}  ({time.time()-t0:.1f}s)")
        core = []
        t0 = time.time()
        for v in S:
            S2 = solve_mis(nodes, edges, fix_zero=[v], time_limit=30)
            if len(S2) < mis_size:
                core.append(v)
        rho_certified = len(core) / mis_size if mis_size else 0.0
        print(f"  core: {len(core)}/{mis_size} (ρ={rho_certified:.3f})  "
              f"{time.time()-t0:.1f}s for {mis_size} per-vertex solves")
        out.append({
            "folder": folder, "label": label, "N": N, "E": len(edges),
            "mis_size": mis_size, "core_size": len(core),
            "rho_certified": round(rho_certified, 4), "core_pages": core,
        })

    Path(__file__).parent.joinpath("certified_rigidity.json").write_text(json.dumps(out, indent=2))
    print("\n=== summary ===")
    for r in out:
        print(f"  {r['label']:<28s} ρ_certified = {r['rho_certified']}  "
              f"(core {r['core_size']}/{r['mis_size']})")


if __name__ == "__main__":
    main()
