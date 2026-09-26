#!/usr/bin/env python3
"""
Helper for the corpus cleanup. For a given graph file, compute
  canonical_N, canonical_E, canonical_density, canonical_MIS,
  canonical_rho, canonical_optima
where rho = fraction of nodes appearing in every enumerated optimum,
optima = number of distinct optimal-size MIS found (capped at OPT_CAP).

If enumeration would exceed OPT_CAP or TIME_CAP_S seconds, returns rho/optima as None
and stamps `canonical_rho_note: "cap_reached"`.

Usage:
  from _compute_canonical import canonical_metrics
  m = canonical_metrics(graph_file_path, opt_cap=500, time_cap_s=120)
"""
import json
import math
import time
from itertools import combinations
from pathlib import Path


def load_graph(path):
    """Return (nodes:list[str], edges_idx:list[(int,int)]) or None if not a usable graph."""
    d = json.loads(Path(path).read_text())
    inner = d.get("graph") if isinstance(d.get("graph"), dict) else d
    raw_nodes = inner.get("nodes")
    raw_edges = inner.get("edges")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        return None
    if not isinstance(raw_edges, list):
        return None
    if isinstance(raw_nodes[0], dict):
        nodes = [str(n.get("id", i)) for i, n in enumerate(raw_nodes)]
    else:
        nodes = [str(n) for n in raw_nodes]
    name_to_idx = {n: i for i, n in enumerate(nodes)}
    edges_idx = []
    for e in raw_edges:
        if isinstance(e, dict):
            a, b = str(e.get("source")), str(e.get("target"))
        elif isinstance(e, (list, tuple)):
            a, b = str(e[0]), str(e[1])
        else:
            continue
        if a in name_to_idx and b in name_to_idx:
            edges_idx.append((name_to_idx[a], name_to_idx[b]))
    return nodes, edges_idx


def solve_mis(N, edges_idx):
    from pulp import (LpProblem, LpMaximize, LpVariable, LpBinary,
                      PULP_CBC_CMD, value as lpvalue)
    prob = LpProblem("mis", LpMaximize)
    x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(N)]
    prob += sum(x)
    for a, b in edges_idx:
        prob += x[a] + x[b] <= 1
    prob.solve(PULP_CBC_CMD(msg=0))
    return [i for i in range(N) if lpvalue(x[i]) > 0.5]


def enumerate_optima(N, edges_idx, alpha, opt_cap=500, time_cap_s=120):
    """Enumerate up to opt_cap distinct MIS of size alpha. Return list of frozensets."""
    from pulp import (LpProblem, LpMaximize, LpVariable, LpBinary,
                      PULP_CBC_CMD, lpSum, value as lpvalue)
    found = []
    seen = set()
    t0 = time.time()
    while len(found) < opt_cap and (time.time() - t0) < time_cap_s:
        prob = LpProblem(f"mis_enum_{len(found)}", LpMaximize)
        x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(N)]
        prob += lpSum(x)
        for a, b in edges_idx:
            prob += x[a] + x[b] <= 1
        # Force MIS size = alpha
        prob += lpSum(x) == alpha
        # Exclude all previously-found solutions
        for k, sol in enumerate(found):
            # at least one variable in sol must be 0  =>  sum_{i in sol} x_i <= alpha-1
            prob += lpSum(x[i] for i in sol) <= alpha - 1
        prob.solve(PULP_CBC_CMD(msg=0, timeLimit=max(1, time_cap_s - (time.time()-t0))))
        sol = frozenset(i for i in range(N) if lpvalue(x[i]) and lpvalue(x[i]) > 0.5)
        if not sol or sol in seen or len(sol) != alpha:
            break
        seen.add(sol)
        found.append(sol)
    return found


def canonical_metrics(graph_path, opt_cap=500, time_cap_s=120):
    g = load_graph(graph_path)
    if g is None:
        return None
    nodes, edges_idx = g
    N = len(nodes)
    E = len(edges_idx)
    d = 2 * E / (N * (N - 1)) if N > 1 else 0.0
    mis = solve_mis(N, edges_idx)
    alpha = len(mis)
    optima = enumerate_optima(N, edges_idx, alpha, opt_cap=opt_cap, time_cap_s=time_cap_s)
    n_opt = len(optima)
    cap_reached = n_opt >= opt_cap
    if optima:
        intersection = set(optima[0])
        for s in optima[1:]:
            intersection &= set(s)
        rho = len(intersection) / alpha if alpha else 0.0
    else:
        rho = None
    return {
        "canonical_N": N,
        "canonical_E": E,
        "canonical_density": round(d, 4),
        "canonical_MIS": alpha,
        "canonical_rho": round(rho, 4) if rho is not None else None,
        "canonical_optima": n_opt,
        "canonical_optima_cap_reached": cap_reached,
    }


if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    print(json.dumps(canonical_metrics(p), indent=2))
