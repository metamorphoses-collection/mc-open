#!/usr/bin/env python3
"""Enumerate all optimal MIS solutions on Giambullari canonical N=151 graph.

Used to verify the '24 optima' claim in Table 1 of the paper.
"""
import json, time
from pathlib import Path
import pulp

GRAPH = Path("corpus/natural/giambullari_inferno/graph_k8.json")
CAP = 100  # generous cap; expected ~24


def load_graph():
    g = json.loads(GRAPH.read_text())
    nodes = g.get("nodes", [])
    if nodes and isinstance(nodes[0], dict):
        nodes = [n.get("id") or n.get("name") for n in nodes]
    edges = []
    for e in g.get("edges", []):
        if isinstance(e, dict):
            edges.append((e["source"], e["target"]))
        else:
            edges.append((e[0], e[1]))
    return nodes, edges


def solve_mis(nodes, edges, blocks):
    """Solve MIS with optional 'block' constraints (each blocked set must be missing >=1)."""
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    prob = pulp.LpProblem("mis", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(n)]
    prob += pulp.lpSum(x)
    for a, b in edges:
        if a in idx and b in idx:
            prob += x[idx[a]] + x[idx[b]] <= 1
    for blk in blocks:
        # at least one of the blocked vertices must be 0 (i.e. sum < |blk|)
        idxs = [idx[v] for v in blk if v in idx]
        prob += pulp.lpSum([x[i] for i in idxs]) <= len(idxs) - 1
    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=120)
    prob.solve(solver)
    if prob.status != 1:
        return None, None
    sel = frozenset(nodes[i] for i in range(n) if x[i].value() and x[i].value() > 0.5)
    return sel, len(sel)


def main():
    nodes, edges = load_graph()
    print(f"Graph: N={len(nodes)}, E={len(edges)}")

    # First MIS
    t0 = time.time()
    s, alpha = solve_mis(nodes, edges, [])
    print(f"MIS size = {alpha}  (solved in {time.time()-t0:.1f}s)")
    print(f"  first optimum has {len(s)} nodes")

    # Enumerate
    blocks = [s]
    optima = [s]
    while len(optima) < CAP:
        s_next, sz = solve_mis(nodes, edges, blocks)
        if s_next is None:
            print(f"  solver failed at iter {len(optima)+1}")
            break
        if sz < alpha:
            print(f"  enumeration complete after {len(optima)} optima (next solve returned size {sz} < {alpha})")
            break
        if s_next in optima:
            print(f"  WARN: duplicate optimum at iter {len(optima)+1}, breaking")
            break
        optima.append(s_next)
        blocks.append(s_next)
        if len(optima) % 5 == 0:
            print(f"  {len(optima)} optima found... ({time.time()-t0:.1f}s)")

    if len(optima) >= CAP:
        print(f"  CAP HIT at {CAP}")

    # Persistent core
    core = set(optima[0])
    for o in optima[1:]:
        core &= set(o)
    rho = len(core) / alpha if alpha else 0
    print()
    print(f"=== RESULT ===")
    print(f"  N = {len(nodes)}")
    print(f"  MIS = {alpha}")
    print(f"  # optimal MIS solutions enumerated: {len(optima)}")
    print(f"  persistent core size: {len(core)}")
    print(f"  rho = {len(core)}/{alpha} = {rho:.3f}")
    print(f"  total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
