#!/usr/bin/env python3
"""
UDG generator v2 for "Le Graphe Incarné" — fixes min_dist, increases SA quality.
"""
import json, math, random
import numpy as np

random.seed(42)
np.random.seed(42)

N = 50
MIN_DIST = 5.0
MAX_RADIUS = 46.0

# From analysis: need blockade ~15µm with hex-packed points to get density ~0.38
# Use hex grid at spacing 5.5 (ensures min_dist >= 5.0 even with small perturbation)

def hex_grid(spacing, n_target, max_r):
    pts = []
    rows = int(2 * max_r / (spacing * math.sqrt(3)/2)) + 1
    cols = int(2 * max_r / spacing) + 1
    for row in range(-rows, rows+1):
        for col in range(-cols, cols+1):
            x = col * spacing + (row % 2) * spacing / 2
            y = row * spacing * math.sqrt(3) / 2
            if math.sqrt(x**2 + y**2) <= max_r:
                pts.append((x, y))
    pts.sort(key=lambda p: p[0]**2 + p[1]**2)
    return pts[:n_target]

# Generate base layout
pts = hex_grid(5.5, N, MAX_RADIUS)
assert len(pts) >= N, f"Only {len(pts)} points generated"
pts = pts[:N]

# Small perturbation preserving min_dist
def perturb(pts, sigma=0.2, min_d=5.0, max_r=46.0):
    new_pts = list(pts)
    for i in range(len(new_pts)):
        for attempt in range(50):
            dx = random.gauss(0, sigma)
            dy = random.gauss(0, sigma)
            nx, ny = new_pts[i][0] + dx, new_pts[i][1] + dy
            if math.sqrt(nx**2 + ny**2) > max_r:
                continue
            ok = True
            for j in range(len(new_pts)):
                if j == i: continue
                if math.sqrt((nx-new_pts[j][0])**2 + (ny-new_pts[j][1])**2) < min_d:
                    ok = False
                    break
            if ok:
                new_pts[i] = (nx, ny)
                break
    return new_pts

pts = perturb(pts)

# Verify constraints
min_d_actual = min(
    math.sqrt((pts[i][0]-pts[j][0])**2 + (pts[i][1]-pts[j][1])**2)
    for i in range(N) for j in range(i+1, N)
)
max_r_actual = max(math.sqrt(p[0]**2+p[1]**2) for p in pts)
print(f"Min distance: {min_d_actual:.3f} µm (>= {MIN_DIST})")
print(f"Max radius: {max_r_actual:.2f} µm (<= {MAX_RADIUS})")
assert min_d_actual >= MIN_DIST - 0.001, f"Min dist violation: {min_d_actual}"

# Find blockade_r for density ~0.38
all_dists = []
for i in range(N):
    for j in range(i+1, N):
        d = math.sqrt((pts[i][0]-pts[j][0])**2 + (pts[i][1]-pts[j][1])**2)
        all_dists.append((d, i, j))
all_dists.sort()

target_edges = int(0.38 * N*(N-1)//2)
print(f"Target edges: {target_edges}")

# Blockade_r = distance of the target_edges-th closest pair
if target_edges <= len(all_dists):
    BLOCKADE_R = all_dists[target_edges-1][0] + 0.01
else:
    BLOCKADE_R = all_dists[-1][0] + 0.01

# Build graph
adj = np.zeros((N,N), dtype=int)
edges = []
for d, i, j in all_dists:
    if d <= BLOCKADE_R:
        adj[i][j] = 1
        adj[j][i] = 1
        edges.append((i, j, round(d, 3)))

d_final = len(edges) / (N*(N-1)//2)
degrees = [int(np.sum(adj[i])) for i in range(N)]
print(f"\nBlockade radius: {BLOCKADE_R:.3f} µm")
print(f"Edges: {len(edges)}, Density: {d_final:.4f}")
print(f"Degree range: {min(degrees)}–{max(degrees)}, mean: {np.mean(degrees):.1f}")

# === STEP 2: Thread assignment via SA ===
THREADS = ["PARI", "CHRONIQUE", "COMPLOT", "LANGUE", "NOMBRE",
           "FOI", "ÉPÉE", "PARCHEMIN", "MALIETTE", "JEU"]

def compute_cost(asgn):
    cost = 0.0
    for i in range(N):
        for j in range(i+1, N):
            s = len(asgn[i] & asgn[j])
            if adj[i][j]:
                if s < 3: cost += (3-s)**2 * 15
            else:
                if s > 1: cost += (s-1)**2 * 8
    # Balance
    tc = [0]*10
    for a in asgn:
        for t in a: tc[t] += 1
    for c in tc:
        cost += (c-25)**2 * 3
    return cost

print("\n=== SA Thread Assignment ===")
asgn = [set(random.sample(range(10), 5)) for _ in range(N)]
cur_cost = compute_cost(asgn)
best_asgn = [s.copy() for s in asgn]
best_cost = cur_cost
T = 200.0
iters = 1000000
cool = (0.0005/200)**(1.0/iters)

for it in range(iters):
    p = random.randint(0, N-1)
    old = asgn[p].copy()
    rem = random.choice(list(old))
    avail = [t for t in range(10) if t not in old]
    add = random.choice(avail)
    asgn[p].discard(rem)
    asgn[p].add(add)
    nc = compute_cost(asgn)
    delta = nc - cur_cost
    if delta < 0 or random.random() < math.exp(-delta/max(T,1e-10)):
        cur_cost = nc
        if nc < best_cost:
            best_cost = nc
            best_asgn = [s.copy() for s in asgn]
    else:
        asgn[p] = old
    T *= cool
    if it % 200000 == 0:
        print(f"  iter {it}: cost={cur_cost:.0f}, best={best_cost:.0f}, T={T:.3f}")

# Report
c_ok = c_tot = d_ok = d_tot = 0
for i in range(N):
    for j in range(i+1, N):
        s = len(best_asgn[i] & best_asgn[j])
        if adj[i][j]:
            c_tot += 1
            if s >= 3: c_ok += 1
        else:
            d_tot += 1
            if s <= 1: d_ok += 1

print(f"\nConnected >= 3 shared: {c_ok}/{c_tot} ({100*c_ok/c_tot:.1f}%)")
print(f"Disconnected <= 1 shared: {d_ok}/{d_tot} ({100*d_ok/d_tot:.1f}%)")

tc = [0]*10
for a in best_asgn:
    for t in a: tc[t] += 1
print(f"Thread counts: {dict(zip(THREADS, tc))}")

# Save
output = {
    "metadata": {
        "title": "Le Graphe Incarné — UDG Layout",
        "experiment": "OuLiPo UDG: first literary text isomorphic to a neutral-atom register",
        "N": N,
        "min_distance_um": MIN_DIST,
        "max_radius_um": MAX_RADIUS,
        "blockade_radius_um": round(BLOCKADE_R, 3),
        "density": round(d_final, 4),
        "num_edges": len(edges),
        "degree_range": [min(degrees), max(degrees)],
        "mean_degree": round(float(np.mean(degrees)), 2),
        "hex_spacing_um": 5.5,
        "constraint_satisfaction": {
            "connected_ge3_shared": f"{c_ok}/{c_tot}",
            "disconnected_le1_shared": f"{d_ok}/{d_tot}"
        }
    },
    "points": [{"id": i, "x": round(p[0],3), "y": round(p[1],3)} for i, p in enumerate(pts)],
    "edges": [{"source": e[0], "target": e[1], "distance_um": e[2]} for e in edges],
    "adjacency_matrix": adj.tolist(),
    "thread_assignments": {
        str(i): {
            "threads": sorted([THREADS[t] for t in best_asgn[i]]),
            "thread_indices": sorted(list(best_asgn[i]))
        }
        for i in range(N)
    },
    "threads": THREADS
}

out_path = "./visualizations/graph_oulipo_udg.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSaved: {out_path}")

print("\n=== Assignments ===")
for i in range(N):
    ts = ", ".join(sorted([THREADS[t] for t in best_asgn[i]]))
    print(f"Page {i+1}: {ts}")
