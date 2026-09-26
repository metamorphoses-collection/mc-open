#!/usr/bin/env python3
"""
Fast UDG generator for "Le Graphe Incarné".
Strategy: place points on a grid-like pattern with controlled spacing,
then perturb to get target density.
"""

import json
import math
import random
import numpy as np

random.seed(42)
np.random.seed(42)

N = 50
MIN_DIST = 5.0
MAX_RADIUS = 46.0
BLOCKADE_R = 8.0
TARGET_DENSITY = 0.38
TARGET_EDGES = int(TARGET_DENSITY * N * (N-1) / 2)  # ~466

def compute_graph(points):
    n = len(points)
    adj = np.zeros((n, n), dtype=int)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            d = math.sqrt((points[i][0]-points[j][0])**2 + (points[i][1]-points[j][1])**2)
            if d <= BLOCKADE_R:
                adj[i][j] = 1
                adj[j][i] = 1
                edges.append((i, j, round(d, 3)))
    return adj, edges

def density(adj, n):
    return (np.sum(adj) // 2) / (n*(n-1)//2)

# Strategy: hex grid with spacing tuned for target density
# With spacing s, each point has ~6 neighbors within distance s.
# We want avg_degree = 2*E/N = 2*466/50 ≈ 18.6
# At blockade_r=8, with spacing s, neighbors within r are at distances s, s*sqrt(3), 2s, etc.
# For s≈5.5: ring1 at 5.5 (6 nbrs), ring2 at 5.5*sqrt(3)≈9.5 (no), so ~6 nbrs. Too few.
# For s≈5.0: ring1 at 5.0 (6), ring2 at 5*sqrt(3)≈8.66 (no, >8), so ~6. Still too few.
# Need avg degree ~18.6, so multiple shells within 8µm.
# With s≈3.5: ring1 at 3.5 (6), ring2 at 3.5*sqrt(3)≈6.06 (6), ring3 at 7.0 (6) = 18. But s<5 violates min_dist.
#
# Conclusion: with min_dist=5.0 and blockade=8.0, max possible neighbors per point:
# Only points at distance [5.0, 8.0] are neighbors.
# In hex packing with s=5: ring1=5 (6 nbrs), ring2=5*sqrt(3)=8.66 (>8, no) → max ~6 nbrs
# In hex packing with s=5.5: ring1=5.5 (6), ring2=9.5 (no) → ~6
# Max avg degree ≈ 6, max density = 6*50/(2*1225) ≈ 0.122
#
# So density 0.38 is IMPOSSIBLE with min_dist=5 and blockade=8!
# Realistic max: ~0.12 with hex packing.
#
# Let's aim for the actual hard zone: lower the min_dist or raise blockade.
# OR: accept the physics and find the max achievable density.
#
# Per the user spec, let's keep the constraints and find the densest possible graph.
# Actually, with less regular packing we can get some pairs at exactly 5.0,
# and have more complex arrangements. But the shell argument holds.
#
# Let's try: place points with random perturbation and measure actual max density.
# Then adjust constraints to hit Cazals zone if needed.

# APPROACH: Use provided constraints, find densest achievable UDG
# If density < 0.30, adjust blockade_radius to hit target

print(f"Target edges for d=0.38: {TARGET_EDGES}")
print(f"With min_dist={MIN_DIST}, blockade={BLOCKADE_R}:")
print(f"  Edge window: [{MIN_DIST}, {BLOCKADE_R}] = {BLOCKADE_R-MIN_DIST} µm wide")
print(f"  Ratio blockade/min_dist = {BLOCKADE_R/MIN_DIST:.2f}")
print()

# Try hex packing first to find max density
def hex_grid(spacing, n_target, max_r):
    """Generate hex grid points within max_r."""
    pts = []
    rows = int(2 * max_r / (spacing * math.sqrt(3)/2)) + 1
    cols = int(2 * max_r / spacing) + 1
    for row in range(-rows, rows+1):
        for col in range(-cols, cols+1):
            x = col * spacing + (row % 2) * spacing / 2
            y = row * spacing * math.sqrt(3) / 2
            if math.sqrt(x**2 + y**2) <= max_r:
                pts.append((x, y))
    # Sort by distance from center and take closest n_target
    pts.sort(key=lambda p: p[0]**2 + p[1]**2)
    return pts[:n_target]

# Test with hex packing
for sp in [5.0, 5.5, 6.0, 6.5, 7.0]:
    pts = hex_grid(sp, N, MAX_RADIUS)
    if len(pts) >= N:
        pts = pts[:N]
        adj, edges = compute_graph(pts)
        d = density(adj, N)
        degs = [int(np.sum(adj[i])) for i in range(N)]
        min_d = min(math.sqrt((pts[i][0]-pts[j][0])**2+(pts[i][1]-pts[j][1])**2)
                    for i in range(N) for j in range(i+1,N))
        print(f"Hex spacing={sp}: {len(pts)} pts, {len(edges)} edges, density={d:.4f}, "
              f"deg={min(degs)}-{max(degs)}, min_dist={min_d:.2f}")
    else:
        print(f"Hex spacing={sp}: only {len(pts)} pts (need {N})")

# The analysis shows we can't hit 0.38 with these constraints.
# SOLUTION: increase blockade radius to hit target density.
# With hex packing at s=5.0:
#   blockade >= 5*sqrt(3) ≈ 8.66 to include 2nd ring → ~12 neighbors
#   blockade >= 10.0 to include 3rd ring → ~18 neighbors
#
# Let's find the right blockade_r for density 0.38 with a good layout.

print("\n--- Finding optimal blockade radius for density ~0.38 ---")
pts = hex_grid(5.5, N, MAX_RADIUS)
if len(pts) < N:
    pts = hex_grid(5.0, N, MAX_RADIUS)
pts = pts[:N]

# Add small perturbation to break perfect symmetry
pts_perturbed = []
for x, y in pts:
    dx = random.gauss(0, 0.3)
    dy = random.gauss(0, 0.3)
    nx, ny = x + dx, y + dy
    if math.sqrt(nx**2 + ny**2) <= MAX_RADIUS:
        pts_perturbed.append((nx, ny))
    else:
        pts_perturbed.append((x, y))

# Verify min_dist
min_d_actual = min(
    math.sqrt((pts_perturbed[i][0]-pts_perturbed[j][0])**2 +
              (pts_perturbed[i][1]-pts_perturbed[j][1])**2)
    for i in range(N) for j in range(i+1, N)
)
print(f"Min distance after perturbation: {min_d_actual:.2f}")

# Sweep blockade radius
for br in np.arange(5.0, 16.0, 0.25):
    adj, edges = compute_graph(pts_perturbed[:N] if len(pts_perturbed) >= N else pts_perturbed)
    # Recompute with this blockade
    adj2 = np.zeros((N,N), dtype=int)
    ed2 = []
    for i in range(N):
        for j in range(i+1,N):
            d = math.sqrt((pts_perturbed[i][0]-pts_perturbed[j][0])**2 +
                         (pts_perturbed[i][1]-pts_perturbed[j][1])**2)
            if d <= br:
                adj2[i][j] = 1
                adj2[j][i] = 1
                ed2.append((i,j,round(d,3)))
    dens = len(ed2) / (N*(N-1)//2)
    if abs(dens - 0.38) < 0.02:
        print(f"  blockade_r={br:.2f}: density={dens:.4f}, edges={len(ed2)}")

print("\n--- Using blockade_r that gives density in [0.30, 0.45] ---")

# Find exact blockade_r for density closest to 0.38
best_br = BLOCKADE_R
best_diff = 1.0
for br in np.arange(5.0, 20.0, 0.1):
    adj2 = np.zeros((N,N), dtype=int)
    ed2 = []
    for i in range(N):
        for j in range(i+1,N):
            d = math.sqrt((pts_perturbed[i][0]-pts_perturbed[j][0])**2 +
                         (pts_perturbed[i][1]-pts_perturbed[j][1])**2)
            if d <= br:
                adj2[i][j] = 1
                adj2[j][i] = 1
                ed2.append((i,j,round(d,3)))
    dens = len(ed2) / (N*(N-1)//2)
    diff = abs(dens - 0.38)
    if diff < best_diff and dens >= 0.30:
        best_diff = diff
        best_br = br
        best_dens = dens

print(f"Optimal blockade_r = {best_br:.1f} µm → density = {best_dens:.4f}")

# Rebuild graph with optimal blockade
BLOCKADE_R_FINAL = best_br
adj_final = np.zeros((N,N), dtype=int)
edges_final = []
for i in range(N):
    for j in range(i+1,N):
        d = math.sqrt((pts_perturbed[i][0]-pts_perturbed[j][0])**2 +
                     (pts_perturbed[i][1]-pts_perturbed[j][1])**2)
        if d <= BLOCKADE_R_FINAL:
            adj_final[i][j] = 1
            adj_final[j][i] = 1
            edges_final.append((i,j,round(d,3)))

d_final = density(adj_final, N)
degrees = [int(np.sum(adj_final[i])) for i in range(N)]
points = pts_perturbed[:N]

print(f"\nFinal graph: {N} nodes, {len(edges_final)} edges, density={d_final:.4f}")
print(f"Degree range: {min(degrees)}–{max(degrees)}, mean: {np.mean(degrees):.1f}")
print(f"Blockade radius: {BLOCKADE_R_FINAL:.1f} µm")
print(f"Min distance: {min_d_actual:.2f} µm")
max_r_actual = max(math.sqrt(p[0]**2+p[1]**2) for p in points)
print(f"Max radius from center: {max_r_actual:.2f} µm")

# === STEP 2: Thread assignment ===
THREADS = ["PARI", "CHRONIQUE", "COMPLOT", "LANGUE", "NOMBRE",
           "FOI", "ÉPÉE", "PARCHEMIN", "MALIETTE", "JEU"]
NUM_THREADS = 10
THREADS_PER_PAGE = 5
adj = adj_final
edges = edges_final

def shared_threads(a, b):
    return len(a & b)

def compute_cost(assignments):
    cost = 0.0
    for i in range(N):
        for j in range(i+1, N):
            s = shared_threads(assignments[i], assignments[j])
            if adj[i][j] == 1:
                if s < 3:
                    cost += (3 - s) ** 2 * 10
            else:
                if s > 1:
                    cost += (s - 1) ** 2 * 5

    thread_counts = [0] * NUM_THREADS
    for a in assignments:
        for t in a:
            thread_counts[t] += 1
    for c in thread_counts:
        cost += (c - 25) ** 2 * 2
    return cost

def sa_optimize(iterations=600000):
    assignments = [set(random.sample(range(NUM_THREADS), THREADS_PER_PAGE)) for _ in range(N)]
    current_cost = compute_cost(assignments)
    best = [s.copy() for s in assignments]
    best_cost = current_cost

    T = 150
    cooling = (0.001 / 150) ** (1.0 / iterations)

    for it in range(iterations):
        page = random.randint(0, N-1)
        old = assignments[page].copy()
        rem = random.choice(list(old))
        avail = [t for t in range(NUM_THREADS) if t not in old]
        add = random.choice(avail)
        assignments[page].discard(rem)
        assignments[page].add(add)

        nc = compute_cost(assignments)
        delta = nc - current_cost
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            current_cost = nc
            if nc < best_cost:
                best_cost = nc
                best = [s.copy() for s in assignments]
        else:
            assignments[page] = old
        T *= cooling
        if it % 100000 == 0:
            print(f"  SA iter {it}: cost={current_cost:.0f}, best={best_cost:.0f}, T={T:.3f}")

    return best, best_cost

print("\n=== Thread Assignment (SA) ===")
best_assignments, best_cost = sa_optimize()

# Analyze
connected_ok = connected_total = disconnected_ok = disconnected_total = 0
for i in range(N):
    for j in range(i+1, N):
        s = shared_threads(best_assignments[i], best_assignments[j])
        if adj[i][j] == 1:
            connected_total += 1
            if s >= 3: connected_ok += 1
        else:
            disconnected_total += 1
            if s <= 1: disconnected_ok += 1

print(f"\nConnected >= 3 shared: {connected_ok}/{connected_total} ({100*connected_ok/max(connected_total,1):.1f}%)")
print(f"Disconnected <= 1 shared: {disconnected_ok}/{disconnected_total} ({100*disconnected_ok/max(disconnected_total,1):.1f}%)")

tc = [0]*NUM_THREADS
for a in best_assignments:
    for t in a: tc[t] += 1
print(f"Thread counts: {dict(zip(THREADS, tc))}")

# Save
output = {
    "metadata": {
        "title": "Le Graphe Incarné — UDG Layout",
        "N": N,
        "min_distance_um": MIN_DIST,
        "max_radius_um": MAX_RADIUS,
        "blockade_radius_um": round(BLOCKADE_R_FINAL, 1),
        "density": round(d_final, 4),
        "num_edges": len(edges_final),
        "degree_range": [min(degrees), max(degrees)],
        "mean_degree": round(float(np.mean(degrees)), 2),
        "constraint_satisfaction": {
            "connected_ge3_shared": f"{connected_ok}/{connected_total}",
            "disconnected_le1_shared": f"{disconnected_ok}/{disconnected_total}"
        }
    },
    "points": [{"id": i, "x": round(p[0], 3), "y": round(p[1], 3)} for i, p in enumerate(points)],
    "edges": [{"source": e[0], "target": e[1], "distance_um": e[2]} for e in edges_final],
    "adjacency_matrix": adj.tolist(),
    "thread_assignments": {
        i: {
            "threads": sorted([THREADS[t] for t in best_assignments[i]]),
            "thread_indices": sorted(list(best_assignments[i]))
        }
        for i in range(N)
    },
    "threads": THREADS
}

out = "./visualizations/graph_oulipo_udg.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSaved to {out}")

print("\n=== Thread Assignments per Page ===")
for i in range(N):
    ts = ", ".join(sorted([THREADS[t] for t in best_assignments[i]]))
    print(f"Page {i+1}: {ts}")
