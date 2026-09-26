#!/usr/bin/env python3
"""
Combinatorial thread-assignment design for Nithard's Wager 100 v3.

Target: N=100 page text whose kNN graph at k=16 hits the Cazals hard zone
(d >= 0.30) under the multilingual-e5-large-instruct embedder.

Recipe (from successful Nithard's Wager 50 EN):
  - 10 thematic threads
  - Exactly 5 threads activated per page
  - 3 narrative voices (Nithard, Pascal, the Porteur de Maliettes)
  - ~370 words per page, keyword-saturated prose
  - Thread overlap >= 3 is the "strong pair" edge criterion

Design strategy: bimodal overlap distribution with a planted cluster structure.
We want:
  - Most page pairs to share 2-3 threads (below threshold, no edge)
  - A significant minority to share 4-5 threads (above threshold, edge)
so the kNN graph has the right density.

Random 5-subset assignment gives (hypergeometric) probabilities:
  share 0: 0.4%   share 3: 39.7%
  share 1: 9.9%   share 4: 9.9%
  share 2: 39.7%  share 5: 0.4%

If we treat share>=3 as a potential edge, that's about 50% of pairs.
At k=16 on N=100, each page has ~16 neighbours, so edge count ~800 undirected,
d ~0.16 (matches k/N). Not dense enough.

To get d >= 0.30 we plant a cluster structure:
  - 5 'cluster themes' of 20 pages each
  - Within a cluster, pages share 4-5 threads (near-complete subgraph)
  - Across clusters, pages share 1-2 threads (no edges)
This gives each cluster ~C(20,2) = 190 edges, total ~950, d ~0.19.
Still not quite, but at k=16 all cluster-mates get included (19 per page)
plus some cross-cluster hubs, pushing d above 0.30.

A cleaner approach: use a combinatorial block design. Specifically,
a resolvable 2-(10,5,4) design or equivalently two disjoint perfect
matchings of the complement graph on 10 threads. This gives exactly
126 distinct 5-subsets of 10. We pick 100 with a clustered structure
to create the density we want.

Output:
  - thread_matrix.json: 100 rows x 5 thread indices
  - predicted_density.json: theoretical graph stats
"""

import json
import random
from itertools import combinations
from pathlib import Path

# 10 thematic threads with specific keyword pools
THREADS = {
    0: {"name": "CHRONICLE",
        "keywords": ["chronicle", "chronicler", "chronicled", "chronicling", "record", "annals"]},
    1: {"name": "FAITH",
        "keywords": ["faith", "faithful", "belief", "believed", "creed", "devotion", "prayer"]},
    2: {"name": "TONGUE",
        "keywords": ["tongue", "language", "vernacular", "Latin", "Romance", "dialect", "speech"]},
    3: {"name": "WAGER",
        "keywords": ["wager", "stake", "bet", "gamble", "risk", "pari", "wagered"]},
    4: {"name": "MALIETTE",
        "keywords": ["maliette", "valise", "case", "folio", "satchel", "portfolio"]},
    5: {"name": "NUMBER",
        "keywords": ["number", "numbered", "count", "counting", "enumeration", "calculation", "arithmetic"]},
    6: {"name": "PARCHMENT",
        "keywords": ["parchment", "vellum", "manuscript", "codex", "palimpsest", "copyist"]},
    7: {"name": "SWORD",
        "keywords": ["sword", "blade", "battle", "Fontenoy", "war", "soldier", "steel"]},
    8: {"name": "CIPHER",
        "keywords": ["cipher", "code", "encrypted", "decoded", "secret", "concealed", "hidden"]},
    9: {"name": "DREAM",
        "keywords": ["dream", "dreamt", "vision", "oneiric", "reverie", "apparition", "dreaming"]},
}

VOICES = ["NITHARD", "PASCAL", "PROFESSOR"]

N_PAGES = 100
THREADS_PER_PAGE = 5
N_THREADS = len(THREADS)


def assign_clustered_threads(n_pages=100, n_clusters=5, cluster_size=20, seed=42):
    """
    Clustered assignment: split 100 pages into 5 clusters of 20 pages.
    Each cluster has a 'core' of 3 threads that all its pages share, plus
    2 rotating threads from the remaining 7 drawn randomly per page.
    This guarantees high within-cluster thread overlap (>=3) and low
    cross-cluster overlap.
    """
    rng = random.Random(seed)

    # Assign cluster cores: 5 clusters, each gets 3 unique-ish threads
    # We use overlapping cores so the 10 threads are all used across clusters
    # Cluster 0: {0,1,2}   Cluster 1: {3,4,5}
    # Cluster 2: {6,7,8}   Cluster 3: {9,0,3}
    # Cluster 4: {6,1,4}
    cluster_cores = [
        [0, 1, 2],   # CHRONICLE, FAITH, TONGUE
        [3, 4, 5],   # WAGER, MALIETTE, NUMBER
        [6, 7, 8],   # PARCHMENT, SWORD, CIPHER
        [9, 0, 3],   # DREAM, CHRONICLE, WAGER
        [6, 1, 4],   # PARCHMENT, FAITH, MALIETTE
    ]
    assert len(cluster_cores) == n_clusters

    assignments = []
    for page_idx in range(n_pages):
        cluster_id = page_idx // cluster_size
        if cluster_id >= n_clusters:
            cluster_id = cluster_id % n_clusters
        core = cluster_cores[cluster_id]
        # Pick 2 more threads from the 7 not in core
        rest_pool = [t for t in range(N_THREADS) if t not in core]
        rotating = rng.sample(rest_pool, THREADS_PER_PAGE - len(core))
        threads = sorted(core + rotating)
        voice = VOICES[page_idx % 3]
        assignments.append({
            "page": page_idx + 1,
            "cluster": cluster_id,
            "threads": threads,
            "thread_names": [THREADS[t]["name"] for t in threads],
            "voice": voice,
        })
    return assignments


def predict_graph_density(assignments, tau=3):
    """
    Compute theoretical graph properties under the assumption that two pages
    form an edge iff they share >= tau threads.  This is the design-time
    upper bound; the actual graph under an embedder will be weaker because
    stylistic baseline softens the gap.
    """
    N = len(assignments)
    thread_sets = [set(a["threads"]) for a in assignments]
    overlap_counts = [0] * 6  # shared 0..5 threads
    edge_pairs = []
    for i in range(N):
        for j in range(i + 1, N):
            ov = len(thread_sets[i] & thread_sets[j])
            overlap_counts[ov] += 1
            if ov >= tau:
                edge_pairs.append((i, j, ov))
    E_potential = len(edge_pairs)
    max_E = N * (N - 1) // 2
    d_potential = E_potential / max_E

    # Degree distribution
    from collections import Counter
    deg = Counter()
    for i, j, ov in edge_pairs:
        deg[i] += 1
        deg[j] += 1
    degrees = [deg.get(i, 0) for i in range(N)]

    return {
        "N": N,
        "overlap_counts_by_shared_threads": overlap_counts,
        "overlap_fraction": [c / max_E for c in overlap_counts],
        "tau_edge_threshold": tau,
        "E_potential_at_tau": E_potential,
        "d_potential_at_tau": d_potential,
        "mean_degree": sum(degrees) / N,
        "min_degree": min(degrees),
        "max_degree": max(degrees),
    }


def simulate_knn_density(assignments, k_values=(8, 16, 25), penalty_per_missing=0.015):
    """
    Approximate kNN density assuming page similarity is dominated by thread
    overlap. For each page, rank neighbours by overlap count (break ties at
    random), pick top-k, and count how many unique edges result after
    symmetrisation.
    """
    import random
    rng = random.Random(123)
    N = len(assignments)
    thread_sets = [set(a["threads"]) for a in assignments]

    sims = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            ov = len(thread_sets[i] & thread_sets[j])
            # Baseline similarity 0.85 + overlap bonus, + small jitter
            s = 0.85 + 0.02 * ov + rng.uniform(-0.005, 0.005)
            sims[i][j] = s
            sims[j][i] = s

    results = {}
    for k in k_values:
        edges = set()
        for i in range(N):
            top_idx = sorted(range(N), key=lambda j: sims[i][j], reverse=True)
            top_idx = [j for j in top_idx if j != i][:k]
            for j in top_idx:
                a, b = min(i, j), max(i, j)
                edges.add((a, b))
        E = len(edges)
        d = E / (N * (N - 1) / 2)
        results[f"k={k}"] = {"edges": E, "density": round(d, 4)}
    return results


def main():
    assignments = assign_clustered_threads(n_pages=N_PAGES, n_clusters=5, cluster_size=20)
    stats = predict_graph_density(assignments, tau=3)
    knn_stats = simulate_knn_density(assignments, k_values=(8, 16, 25))

    out_dir = Path(__file__).parent
    out_dir.joinpath("thread_matrix.json").write_text(json.dumps({
        "threads": THREADS,
        "voices": VOICES,
        "n_pages": N_PAGES,
        "threads_per_page": THREADS_PER_PAGE,
        "assignments": assignments,
    }, indent=2))

    out_dir.joinpath("predicted_density.json").write_text(json.dumps({
        "overlap_stats": stats,
        "knn_stats_simulated": knn_stats,
        "notes": [
            "Overlap stats are the pure combinatorial design (not the embedder).",
            "kNN sim assumes similarity = 0.85 + 0.02*overlap + small jitter.",
            "Target: d >= 0.30 at k=16 for hard-zone eligibility.",
        ],
    }, indent=2))

    print("\n=== Thread assignment design ===")
    print(f"N pages: {N_PAGES}, threads/page: {THREADS_PER_PAGE}, total threads: {N_THREADS}")
    print(f"\nOverlap distribution (number of page pairs sharing N threads):")
    for i, c in enumerate(stats["overlap_counts_by_shared_threads"]):
        pct = 100 * c / (N_PAGES * (N_PAGES - 1) / 2)
        print(f"  share {i}: {c:5} pairs ({pct:5.1f}%)")
    print(f"\nPotential density at tau=3: {stats['d_potential_at_tau']:.3f}")
    print(f"Mean degree at tau=3: {stats['mean_degree']:.1f}")
    print(f"\nSimulated kNN density (similarity = 0.85 + 0.02*overlap):")
    for k, v in knn_stats.items():
        marker = " ** HARD ZONE" if v["density"] >= 0.30 else ""
        print(f"  {k}: d = {v['density']:.4f}, E = {v['edges']}{marker}")


if __name__ == "__main__":
    main()
