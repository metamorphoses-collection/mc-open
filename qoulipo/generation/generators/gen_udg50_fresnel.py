#!/usr/bin/env python3
"""
Generate UDG 50 designed for FRESNEL R_b=8.0µm physics.
The old UDG 50 was designed at R_b=14.8µm — wrong blockade for the hardware.
This version creates positions where the UDG at R_b=8.0µm IS the intended graph.

Then submits to EMU_MPS for validation.
"""
import os
import json, math, random, time
import numpy as np
import networkx as nx
from pathlib import Path
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, value

random.seed(2026)
np.random.seed(2026)

BASE = Path(__file__).resolve().parent
N = 50
MIN_DIST = 5.0
MAX_RADIUS = 46.0
BLOCKADE_UM = 8.0  # FRESNEL actual R_b

# === STEP 1: Generate hex grid positions ===
def hex_grid(spacing, max_r):
    pts = []
    rows = int(2 * max_r / (spacing * math.sqrt(3)/2)) + 2
    cols = int(2 * max_r / spacing) + 2
    for row in range(-rows, rows+1):
        for col in range(-cols, cols+1):
            x = col * spacing + (row % 2) * spacing / 2
            y = row * spacing * math.sqrt(3) / 2
            if math.hypot(x, y) <= max_r:
                pts.append((x, y))
    pts.sort(key=lambda p: math.hypot(*p))
    return pts

# Try different spacings to maximize density at R_b=8.0
print("=== Sweep spacing to maximize density at R_b=8.0µm ===")
best_spacing = 5.5
best_density = 0
best_edges = 0

for sp_100 in range(500, 800, 5):  # spacing from 5.0 to 8.0 in 0.05 steps
    sp = sp_100 / 100.0
    pts = hex_grid(sp, MAX_RADIUS)
    if len(pts) < N:
        continue
    pts = pts[:N]

    # Check min dist
    min_d = min(math.hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1])
                for i in range(N) for j in range(i+1, N))
    if min_d < MIN_DIST:
        continue

    # Count edges at R_b=8.0
    edges = 0
    for i in range(N):
        for j in range(i+1, N):
            if math.hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1]) <= BLOCKADE_UM:
                edges += 1
    d = edges / (N*(N-1)//2)

    if edges > best_edges:
        best_edges = edges
        best_density = d
        best_spacing = sp
        print(f"  spacing={sp:.2f}: edges={edges}, d={d:.4f}, min_dist={min_d:.2f}")

print(f"\nBest: spacing={best_spacing:.2f}, edges={best_edges}, d={best_density:.4f}")

# === STEP 2: Generate final positions with best spacing + perturbation ===
pts = hex_grid(best_spacing, MAX_RADIUS)[:N]

# Perturb to break symmetry
def perturb(pts, sigma=0.15, min_d=MIN_DIST, max_r=MAX_RADIUS):
    new_pts = list(pts)
    for i in range(len(new_pts)):
        for attempt in range(100):
            dx = random.gauss(0, sigma)
            dy = random.gauss(0, sigma)
            nx_, ny_ = new_pts[i][0] + dx, new_pts[i][1] + dy
            if math.hypot(nx_, ny_) > max_r:
                continue
            ok = True
            for j in range(len(new_pts)):
                if j == i: continue
                if math.hypot(nx_ - new_pts[j][0], ny_ - new_pts[j][1]) < min_d:
                    ok = False
                    break
            if ok:
                new_pts[i] = (round(nx_, 3), round(ny_, 3))
                break
    return new_pts

pts = perturb(pts)

# === STEP 3: Build UDG at R_b=8.0µm ===
G = nx.Graph()
G.add_nodes_from(range(N))
edges_list = []
for i in range(N):
    for j in range(i+1, N):
        d = math.hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1])
        if d <= BLOCKADE_UM:
            G.add_edge(i, j)
            edges_list.append({"source": i, "target": j, "distance_um": round(d, 3)})

E = G.number_of_edges()
density = nx.density(G)
degrees = [G.degree(n) for n in G.nodes]
min_dist = min(math.hypot(pts[i][0]-pts[j][0], pts[i][1]-pts[j][1])
               for i in range(N) for j in range(i+1, N))
max_r = max(math.hypot(*p) for p in pts)

# MIS via ILP
prob = LpProblem("MIS", LpMaximize)
x = {n: LpVariable(f"x_{n}", cat=LpBinary) for n in G.nodes}
prob += sum(x.values())
for u, v in G.edges():
    prob += x[u] + x[v] <= 1
prob.solve(PULP_CBC_CMD(msg=0))
mis_size = sum(1 for n in G.nodes if value(x[n]) > 0.5)

# Adjacency matrix
adj = np.zeros((N, N), dtype=int)
for u, v in G.edges():
    adj[u][v] = 1
    adj[v][u] = 1

print(f"\n=== UDG 50 @ R_b={BLOCKADE_UM}µm ===")
print(f"N={N}, E={E}, density={density:.4f}")
print(f"Degrees: min={min(degrees)}, max={max(degrees)}, mean={np.mean(degrees):.1f}")
print(f"MIS={mis_size} (MIS/N={mis_size/N:.3f})")
print(f"Min dist: {min_dist:.3f}µm, Max radius: {max_r:.2f}µm")
print(f"FRESNEL: min_dist={'OK' if min_dist >= 5.0 else 'FAIL'}, "
      f"max_r={'OK' if max_r <= 46.0 else 'FAIL'}")

# === STEP 4: Save graph ===
output = {
    "N": N,
    "blockade_um": BLOCKADE_UM,
    "density": round(density, 4),
    "num_edges": E,
    "placement_radius": round(max_r, 2),
    "seed": 2026,
    "hex_spacing": best_spacing,
    "degrees": {
        "min": min(degrees),
        "max": max(degrees),
        "mean": round(float(np.mean(degrees)), 2)
    },
    "mis_size": mis_size,
    "points": [{"id": i, "x": round(pts[i][0], 3), "y": round(pts[i][1], 3)} for i in range(N)],
    "edges": edges_list,
    "adj": adj.tolist()
}

out_path = BASE / "graph_udg50_fresnel.json"
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {out_path}")

# === STEP 5: Submit to EMU_MPS ===
print("\n=== Submitting to EMU_MPS ===")

try:
    from pasqal_cloud import SDK
    from pulser import Register, Pulse, Sequence
    from pulser.devices import DigitalAnalogDevice
    from pulser.waveforms import InterpolatedWaveform

    PASQAL_PROJECT_ID = "9311685e-cc0c-43b2-8db6-6e11d352878a"

    # FRESNEL physics
    C6_FRESNEL = 865723
    OMEGA = C6_FRESNEL / (BLOCKADE_UM ** 6)  # 3.303 rad/µs
    DELTA_0 = -3 * OMEGA
    DELTA_F = +3 * OMEGA
    T_NS = 4000

    sdk = SDK(
        project_id=PASQAL_PROJECT_ID,
        username=os.environ['PASQAL_USER'],
        password='zomfeg-0hoDby-ruhzij',
    )

    # Build register with native positions (fidelity = 1.0 by definition)
    qubits = {f"q{i}": (pts[i][0], pts[i][1]) for i in range(N)}
    reg = Register(qubits)

    # Use DigitalAnalogDevice for EMU (more permissive than FRESNEL device)
    seq = Sequence(reg, DigitalAnalogDevice)
    seq.declare_channel("ising", "rydberg_global")

    sweep = Pulse(
        InterpolatedWaveform(T_NS, [1e-9, OMEGA, 1e-9]),
        InterpolatedWaveform(T_NS, [DELTA_0, 0, DELTA_F]),
        0,
    )
    seq.add(sweep, "ising")

    serialized = seq.to_abstract_repr()

    # Submit to EMU_MPS
    batch = sdk.create_batch(
        serialized_sequence=serialized,
        jobs=[{"runs": 1000}],
        emulator="EMU_MPS",
    )
    print(f"EMU batch submitted: {batch.id}")

    # Save batch info
    emu_info = {
        "udg50_fresnel": {
            "batch_id": str(batch.id),
            "N": N,
            "E": E,
            "density": round(density, 4),
            "mis_size": mis_size,
            "blockade_um": BLOCKADE_UM,
            "omega": round(OMEGA, 4),
            "fidelity": 1.0,
            "desc": "UDG 50 redesigned for FRESNEL R_b=8.0µm (native positions)",
            "graph_file": "graph_udg50_fresnel.json"
        }
    }
    with open(BASE / "emu_udg50_fresnel_batch.json", 'w') as f:
        json.dump(emu_info, f, indent=2)
    print(f"Batch metadata saved to emu_udg50_fresnel_batch.json")

    # Wait for result
    print("Waiting for EMU result...")
    for attempt in range(60):
        time.sleep(10)
        b = sdk.get_batch(batch.id)
        status = str(b.status)
        if 'DONE' in status:
            print(f"  Status: {status} (after {(attempt+1)*10}s)")
            break
        elif 'ERROR' in status or 'CANCEL' in status:
            print(f"  Status: {status}")
            break
        if attempt % 6 == 0:
            print(f"  Status: {status} ({(attempt+1)*10}s)")
    else:
        print("  Timeout after 600s — check later")
        import sys; sys.exit(0)

    # Analyze results
    total = valid = best = 0
    unique_is = set()
    is_sizes = []

    for job in b.ordered_jobs:
        if not hasattr(job, 'result') or job.result is None:
            continue
        counts = job.result
        if isinstance(counts, dict):
            for bs, count in counts.items():
                total += count
                bits = [int(c) for c in str(bs)]
                selected = [i for i in range(min(len(bits), N)) if bits[i] == 1]

                is_valid = True
                for a in range(len(selected)):
                    for b_ in range(a+1, len(selected)):
                        if G.has_edge(selected[a], selected[b_]):
                            is_valid = False
                            break
                    if not is_valid:
                        break

                if is_valid and len(selected) > 0:
                    valid += count
                    is_sizes.extend([len(selected)] * count)
                    if len(selected) > best:
                        best = len(selected)
                    unique_is.add(tuple(sorted(selected)))

    pct = 100 * valid / total if total else 0
    ratio = best / mis_size if mis_size else 0

    print(f"\n=== EMU RESULTS ===")
    print(f"Valid IS: {valid}/{total} = {pct:.1f}%")
    print(f"Best IS: {best} (MIS={mis_size}), ratio={ratio:.3f}")
    print(f"Unique valid IS: {len(unique_is)}")
    if is_sizes:
        print(f"Mean IS: {np.mean(is_sizes):.2f}, Median: {int(np.median(is_sizes))}")

    # Save results
    results = {
        "udg50_fresnel": {
            "N": N, "E": E, "density": round(density, 4),
            "mis_size": mis_size, "blockade_um": BLOCKADE_UM,
            "fidelity": 1.0,
            "total_shots": total,
            "valid_is_count": valid,
            "valid_is_pct": round(pct, 1),
            "best_is_size": best,
            "ratio": round(ratio, 3),
            "unique_valid_is": len(unique_is),
            "mean_is_size": round(float(np.mean(is_sizes)), 2) if is_sizes else 0,
            "batch_id": str(batch.id),
        }
    }
    with open(BASE / "emu_udg50_fresnel_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to emu_udg50_fresnel_results.json")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback; traceback.print_exc()
