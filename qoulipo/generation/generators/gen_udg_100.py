#!/usr/bin/env python3
"""
Generate UDG with N=100 nodes satisfying FRESNEL_CAN1 QPU constraints.
  - min_atom_distance >= 5.0 µm
  - max_radial_distance <= 46.0 µm from center
  - blockade radius R_b = 8.0 µm
Strategy: hex grid at spacing ~5.2 µm, select 100 closest to center,
perturb with sigma=0.2 µm, verify constraints, compute graph + MIS.
"""

import json, math, random
import numpy as np

# ---------- constants ----------
N = 100
MIN_DIST = 5.0       # µm
MAX_RADIUS = 46.0    # µm
BLOCKADE_R = 8.0     # µm
SEED = 31415

random.seed(SEED)
np.random.seed(SEED)

# ---------- hex grid generation ----------
def hex_grid(spacing, max_r):
    """Generate hex-grid points within max_r of origin."""
    pts = []
    row_height = spacing * math.sqrt(3) / 2
    rows = int(max_r / row_height) + 2
    cols = int(max_r / spacing) + 2
    for row in range(-rows, rows + 1):
        for col in range(-cols, cols + 1):
            x = col * spacing + (row % 2) * spacing / 2
            y = row * row_height
            if math.sqrt(x * x + y * y) <= max_r:
                pts.append((x, y))
    pts.sort(key=lambda p: p[0]**2 + p[1]**2)
    return pts

# Find a spacing that yields >= 100 points inside MAX_RADIUS
# With spacing=5.0, hex packing in a circle of radius R gives ~(2*pi*R^2)/(sqrt(3)*s^2) points
# For R=46, s=5: ~ 2*pi*2116 / (1.732*25) ~ 13300/43.3 ~ 307 points => plenty
# But we want to keep points well inside to leave margin. Use a smaller placement_radius.

# Try spacings and find one that gives a good graph
for spacing in [5.0, 5.1, 5.2, 5.3, 5.4, 5.5]:
    pts = hex_grid(spacing, MAX_RADIUS)
    print(f"Hex spacing={spacing}: {len(pts)} points available within {MAX_RADIUS} µm")

# Use spacing=5.2 for a good balance
SPACING = 5.2
all_pts = hex_grid(SPACING, MAX_RADIUS)
print(f"\nUsing spacing={SPACING}, {len(all_pts)} candidates, selecting {N} closest to center")

# Select N closest to center
pts = all_pts[:N]
max_r_before = max(math.sqrt(p[0]**2 + p[1]**2) for p in pts)
print(f"Placement radius before perturbation: {max_r_before:.2f} µm")

# ---------- perturbation ----------
SIGMA = 0.2
MAX_TRIES = 100

def perturb_points(pts, sigma, min_dist, max_r):
    """Add Gaussian perturbation while respecting constraints."""
    result = list(pts)
    for i in range(len(result)):
        for _ in range(MAX_TRIES):
            dx = random.gauss(0, sigma)
            dy = random.gauss(0, sigma)
            nx, ny = result[i][0] + dx, result[i][1] + dy
            # Check radius
            if math.sqrt(nx**2 + ny**2) > max_r:
                continue
            # Check min distance to all previously placed points
            ok = True
            for j in range(len(result)):
                if j == i:
                    continue
                d = math.sqrt((nx - result[j][0])**2 + (ny - result[j][1])**2)
                if d < min_dist:
                    ok = False
                    break
            if ok:
                result[i] = (nx, ny)
                break
    return result

pts_final = perturb_points(pts, SIGMA, MIN_DIST, MAX_RADIUS)

# ---------- verify constraints ----------
min_pair_dist = float('inf')
for i in range(N):
    for j in range(i + 1, N):
        d = math.sqrt((pts_final[i][0] - pts_final[j][0])**2 +
                      (pts_final[i][1] - pts_final[j][1])**2)
        if d < min_pair_dist:
            min_pair_dist = d

max_r_actual = max(math.sqrt(p[0]**2 + p[1]**2) for p in pts_final)
print(f"\nConstraint check:")
print(f"  Min pair distance: {min_pair_dist:.3f} µm (need >= {MIN_DIST})")
print(f"  Max radial distance: {max_r_actual:.3f} µm (need <= {MAX_RADIUS})")
assert min_pair_dist >= MIN_DIST, f"Min distance violated: {min_pair_dist:.4f}"
assert max_r_actual <= MAX_RADIUS, f"Max radius violated: {max_r_actual:.4f}"
print("  ALL CONSTRAINTS SATISFIED")

# ---------- compute graph ----------
adj = np.zeros((N, N), dtype=int)
edges = []
for i in range(N):
    for j in range(i + 1, N):
        d = math.sqrt((pts_final[i][0] - pts_final[j][0])**2 +
                      (pts_final[i][1] - pts_final[j][1])**2)
        if d <= BLOCKADE_R:
            adj[i][j] = 1
            adj[j][i] = 1
            edges.append((i, j, round(d, 3)))

num_edges = len(edges)
density = num_edges / (N * (N - 1) // 2)
degrees = [int(np.sum(adj[i])) for i in range(N)]
print(f"\nGraph properties:")
print(f"  N = {N}")
print(f"  Edges = {num_edges}")
print(f"  Density = {density:.4f}")
print(f"  Degree: min={min(degrees)}, max={max(degrees)}, mean={np.mean(degrees):.2f}")

# ---------- MIS via ILP ----------
print("\nComputing MIS via ILP...")
try:
    import pulp
    prob = pulp.LpProblem("MIS", pulp.LpMaximize)
    x = [pulp.LpVariable(f"x{i}", cat="Binary") for i in range(N)]
    prob += pulp.lpSum(x)
    for i in range(N):
        for j in range(i + 1, N):
            if adj[i][j] == 1:
                prob += x[i] + x[j] <= 1
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    mis_size = int(pulp.value(prob.objective))
    mis_nodes = [i for i in range(N) if pulp.value(x[i]) > 0.5]
    print(f"  MIS size = {mis_size}")
    print(f"  MIS density = {mis_size / N:.4f}")
except ImportError:
    print("  pulp not available, skipping MIS")
    mis_size = None
    mis_nodes = []

# ---------- save JSON ----------
BASE = "./visualizations"

output = {
    "N": N,
    "blockade_um": BLOCKADE_R,
    "density": round(density, 4),
    "num_edges": num_edges,
    "placement_radius": round(max_r_actual, 2),
    "seed": SEED,
    "degrees": {
        "min": min(degrees),
        "max": max(degrees),
        "mean": round(float(np.mean(degrees)), 2)
    },
    "points": [{"id": i, "x": round(p[0], 3), "y": round(p[1], 3)} for i, p in enumerate(pts_final)],
    "edges": [{"source": e[0], "target": e[1], "distance_um": e[2]} for e in edges],
    "adj": adj.tolist(),
    "mis_size": mis_size,
    "mis_nodes": mis_nodes
}

out_path = f"{BASE}/graph_udg_100.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nSaved to {out_path}")

# ---------- update generation log ----------
log_path = f"{BASE}/udg_generation_log.txt"
with open(log_path, 'a', encoding='utf-8') as f:
    f.write(f"\n{'='*50}\n")
    f.write(f"Generating UDG N={N}, FRESNEL_CAN1 constraints\n")
    f.write(f"Date: 2026-04-08\n")
    f.write(f"Seed: {SEED}\n")
    f.write(f"Spacing: {SPACING} µm (hex grid)\n")
    f.write(f"Perturbation sigma: {SIGMA} µm\n")
    f.write(f"Min pair distance: {min_pair_dist:.3f} µm (constraint >= {MIN_DIST})\n")
    f.write(f"Max radial distance: {max_r_actual:.3f} µm (constraint <= {MAX_RADIUS})\n")
    f.write(f"Blockade radius: {BLOCKADE_R} µm\n")
    f.write(f"Edges: {num_edges}\n")
    f.write(f"Density: {density:.4f}\n")
    f.write(f"Degrees: min={min(degrees)}, max={max(degrees)}, mean={np.mean(degrees):.2f}\n")
    if mis_size is not None:
        f.write(f"MIS size: {mis_size} (density {mis_size/N:.4f})\n")
    f.write(f"Output: graph_udg_100.json\n")
    f.write(f"{'='*50}\n")
print("Updated udg_generation_log.txt")

print("\nDone!")
