#!/usr/bin/env python3
"""
Generate a Unit Disk Graph (UDG) for "Le Graphe Incarné" OuLiPo experiment.
- N=50 atoms on 2D plane
- Min distance between any two points >= 5.0 µm
- All points within 46.0 µm radius from center
- Blockade radius = 8.0 µm (edges for pairs within this distance)
- Target density d ≈ 0.30–0.45 (Cazals hard zone)
Then solve thread assignment via simulated annealing.
"""

import json
import math
import random
import numpy as np

random.seed(2026)
np.random.seed(2026)

# === STEP 1: Generate UDG layout ===

N = 50
MIN_DIST = 5.0       # µm
MAX_RADIUS = 46.0    # µm from center
BLOCKADE_R = 8.0     # µm — edge threshold
TARGET_DENSITY = 0.38

def compute_adjacency(points, blockade_r):
    n = len(points)
    adj = np.zeros((n, n), dtype=int)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= blockade_r:
                adj[i][j] = 1
                adj[j][i] = 1
                edges.append((i, j, round(dist, 3)))
    return adj, edges

def density(adj, n):
    num_edges = np.sum(adj) // 2
    max_edges = n * (n - 1) // 2
    return num_edges / max_edges

# Strategy: place points in a smaller circle to get density right.
# With min_dist=5 and blockade=8, a point connects to neighbors within 8µm.
# In a hexagonal packing with spacing ~6µm, each point has ~6 neighbors.
# We need avg degree ~0.38*49 ≈ 18.6. That's quite high.
# Actually density 0.38 means 0.38 * 1225 ≈ 466 edges, avg degree ~18.6.
# With blockade 8µm and min_dist 5µm, we need points packed fairly tight.
# Effective placement radius: about 20-25 µm should work.

def generate_layout(seed, placement_radius):
    """Generate a UDG layout with given placement radius."""
    rng = random.Random(seed)
    points = []
    attempts = 0
    while len(points) < N and attempts < 500000:
        r = placement_radius * math.sqrt(rng.random())
        theta = rng.uniform(0, 2 * math.pi)
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        if math.sqrt(x**2 + y**2) > MAX_RADIUS:
            attempts += 1
            continue

        too_close = False
        for px, py in points:
            if math.sqrt((x - px)**2 + (y - py)**2) < MIN_DIST:
                too_close = True
                break

        if not too_close:
            points.append((x, y))
        attempts += 1

    return points

print("Searching for UDG with target density ~0.38...")
best_points = None
best_density_diff = float('inf')
best_adj = None
best_edges = None
best_d = 0

# Sweep over placement radii and seeds
for pr_idx, placement_r in enumerate(np.arange(15.0, 30.0, 0.5)):
    for seed in range(2026, 2126):
        pts = generate_layout(seed, placement_r)
        if len(pts) < N:
            continue
        adj_t, edges_t = compute_adjacency(pts, BLOCKADE_R)
        d = density(adj_t, N)
        diff = abs(d - TARGET_DENSITY)

        if diff < best_density_diff:
            best_density_diff = diff
            best_points = pts
            best_adj = adj_t
            best_edges = edges_t
            best_d = d
            if diff < 0.005:
                print(f"  R={placement_r:.1f}, seed={seed}: density={d:.4f}, edges={len(edges_t)} *** CLOSE ***")

        if best_density_diff < 0.005:
            break
    if best_density_diff < 0.005:
        break

if best_density_diff >= 0.005:
    # Print best found
    print(f"  Best so far: density={best_d:.4f} (diff={best_density_diff:.4f})")

print(f"\nBest density: {best_d:.4f}")
print(f"Number of edges: {len(best_edges)}")
print(f"Number of nodes: {len(best_points)}")

points = best_points
adj = best_adj
edges = best_edges

degrees = [int(np.sum(adj[i])) for i in range(N)]
print(f"Degree range: {min(degrees)}–{max(degrees)}, mean: {np.mean(degrees):.1f}")

# Verify all points within MAX_RADIUS and min_dist satisfied
max_r_actual = max(math.sqrt(p[0]**2 + p[1]**2) for p in points)
min_d_actual = min(
    math.sqrt((points[i][0]-points[j][0])**2 + (points[i][1]-points[j][1])**2)
    for i in range(N) for j in range(i+1, N)
)
print(f"Max distance from center: {max_r_actual:.2f} µm (limit: {MAX_RADIUS})")
print(f"Min inter-point distance: {min_d_actual:.2f} µm (limit: {MIN_DIST})")

# === STEP 2: Thread assignment via Simulated Annealing ===

THREADS = ["PARI", "CHRONIQUE", "COMPLOT", "LANGUE", "NOMBRE",
           "FOI", "ÉPÉE", "PARCHEMIN", "MALIETTE", "JEU"]
NUM_THREADS = len(THREADS)
THREADS_PER_PAGE = 5
TARGET_SHARED_CONNECTED = 3
TARGET_SHARED_DISCONNECTED = 1

def shared_threads(a, b):
    return len(a & b)

def compute_cost(assignments, adj, n):
    cost = 0.0
    for i in range(n):
        for j in range(i+1, n):
            s = shared_threads(assignments[i], assignments[j])
            if adj[i][j] == 1:
                if s < TARGET_SHARED_CONNECTED:
                    cost += (TARGET_SHARED_CONNECTED - s) ** 2 * 10
            else:
                if s > TARGET_SHARED_DISCONNECTED:
                    cost += (s - TARGET_SHARED_DISCONNECTED) ** 2 * 5

    thread_counts = [0] * NUM_THREADS
    for a in assignments:
        for t in a:
            thread_counts[t] += 1
    target_count = n * THREADS_PER_PAGE / NUM_THREADS
    for c in thread_counts:
        cost += (c - target_count) ** 2 * 2

    return cost

def sa_optimize(adj, n, iterations=800000, T_start=200, T_end=0.001):
    assignments = []
    for _ in range(n):
        chosen = random.sample(range(NUM_THREADS), THREADS_PER_PAGE)
        assignments.append(set(chosen))

    current_cost = compute_cost(assignments, adj, n)
    best_assignments = [s.copy() for s in assignments]
    best_cost = current_cost

    cooling = (T_end / T_start) ** (1.0 / iterations)
    T = T_start

    for it in range(iterations):
        page = random.randint(0, n-1)
        old_set = assignments[page].copy()

        remove_t = random.choice(list(old_set))
        available = [t for t in range(NUM_THREADS) if t not in old_set]
        add_t = random.choice(available)

        assignments[page].remove(remove_t)
        assignments[page].add(add_t)

        new_cost = compute_cost(assignments, adj, n)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            current_cost = new_cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_assignments = [s.copy() for s in assignments]
        else:
            assignments[page] = old_set

        T *= cooling

        if it % 100000 == 0:
            print(f"  SA iter {it}: cost={current_cost:.1f}, best={best_cost:.1f}, T={T:.4f}")

    return best_assignments, best_cost

print("\n=== Thread Assignment (Simulated Annealing) ===")
best_assignments, best_cost = sa_optimize(adj, N)

print(f"\nFinal cost: {best_cost:.1f}")

connected_ok = 0
connected_total = 0
disconnected_ok = 0
disconnected_total = 0

for i in range(N):
    for j in range(i+1, N):
        s = shared_threads(best_assignments[i], best_assignments[j])
        if adj[i][j] == 1:
            connected_total += 1
            if s >= TARGET_SHARED_CONNECTED:
                connected_ok += 1
        else:
            disconnected_total += 1
            if s <= TARGET_SHARED_DISCONNECTED:
                disconnected_ok += 1

print(f"Connected pairs with >= 3 shared: {connected_ok}/{connected_total} ({100*connected_ok/max(connected_total,1):.1f}%)")
print(f"Disconnected pairs with <= 1 shared: {disconnected_ok}/{disconnected_total} ({100*disconnected_ok/max(disconnected_total,1):.1f}%)")

thread_counts = [0] * NUM_THREADS
for a in best_assignments:
    for t in a:
        thread_counts[t] += 1
print(f"Thread counts: {dict(zip(THREADS, thread_counts))}")

# === Save results ===
output = {
    "metadata": {
        "title": "Le Graphe Incarné — UDG Layout",
        "N": N,
        "min_distance_um": MIN_DIST,
        "max_radius_um": MAX_RADIUS,
        "blockade_radius_um": BLOCKADE_R,
        "density": round(best_d, 4),
        "num_edges": len(edges),
        "degree_range": [min(degrees), max(degrees)],
        "mean_degree": round(np.mean(degrees), 2),
        "constraint_satisfaction": {
            "connected_ge3_shared": f"{connected_ok}/{connected_total}",
            "disconnected_le1_shared": f"{disconnected_ok}/{disconnected_total}"
        }
    },
    "points": [{"id": i, "x": round(p[0], 3), "y": round(p[1], 3)} for i, p in enumerate(points)],
    "edges": [{"source": e[0], "target": e[1], "distance_um": e[2]} for e in edges],
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

output_path = "./visualizations/graph_oulipo_udg.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nSaved to {output_path}")

print("\n=== Thread Assignments per Page ===")
for i in range(N):
    threads_str = ", ".join(sorted([THREADS[t] for t in best_assignments[i]]))
    print(f"Page {i+1}: {threads_str}")
