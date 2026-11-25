"""Print the die-link register counts reported in the paper."""
import json
from functools import lru_cache
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
DIE = ROOT / "data" / "die"


def exact_independence_number(G):
    """Exact independence number for a small sparse graph."""
    adj = {n: frozenset(G.neighbors(n)) for n in G.nodes}

    @lru_cache(maxsize=None)
    def rec(remaining):
        if not remaining:
            return 0
        # include all current isolates
        isolates = tuple(v for v in remaining if not (adj[v] & remaining))
        if isolates:
            return len(isolates) + rec(frozenset(remaining) - frozenset(isolates))
        v = min(remaining, key=lambda u: len(adj[u] & remaining))
        rest = remaining - {v}
        return max(rec(rest), 1 + rec(rest - adj[v]))

    return rec(frozenset(G.nodes))


def report(path):
    R = json.loads(path.read_text())
    adj = R["adj"]
    n = R["n"]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from((i, j) for i in range(n) for j in range(i + 1, n) if adj[i][j])
    edges = R["edges"]
    iso = sum(1 for _, d in G.degree() if d == 0)
    mis = exact_independence_number(G)
    print(f"{path.name}: {n} sites, {edges} edges, {iso} isolated site(s), independence number {mis}")
    return n, edges, mis


if __name__ == "__main__":
    report(DIE / "unique_55.json")
    report(DIE / "as_run_56.json")
