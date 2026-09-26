#!/usr/bin/env python3
"""Castello dei 49 destini — FRESNEL_CAN1 QPU submission.

Submitted 2026-04-27 with 250 shots remaining on the QPU budget.
King-7×7 (Chebyshev-1 only) approximation of the canonical extended-king
text: FRESNEL_CAN1's amplitude floor (Ω ≥ π/10) caps R_b ≤ 12 µm at
a = 5 µm spacing, so the canonical Chebyshev-≤2 graph (which would
require R_b > 14.14 µm) is unreachable on this hardware. The submitted
register realises the king-only subset:
  - N=49, E=156 (vs canonical E=396), d=0.13
  - king-7×7 MIS = 16 (checkerboard), vs canonical MIS = 9

Status as of session close (2026-04-27 evening): batch still PENDING in
FRESNEL queue. Result expected next session.

Batch ID: 2d401cff-8314-4bb0-a685-7f8e47e80942
"""
import argparse, json, math, os, time
from itertools import combinations
from pathlib import Path

os.environ.setdefault("PASQAL_LOG_LEVEL", "ERROR")
OUT_DIR = Path(__file__).parent / "castello_49_fresnel"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_ID = "9311685e-cc0c-43b2-8db6-6e11d352878a"
USER = os.environ["PASQAL_USER"]   # your Pasqal cloud login
PWD = "zomfeg-0hoDby-ruhzij"

C6 = 865723
A_UM = 5.0
R_B_UM = 8.0
OMEGA = C6 / R_B_UM ** 6   # ≈ 3.30 rad/µs
DELTA_NEG = -3 * OMEGA
DELTA_POS = +3 * OMEGA
T_NS = 4000
SHOTS_DEFAULT = 250


def build_grid_7x7():
    nodes, coords = [], {}
    for r in range(7):
        for c in range(7):
            nid = f"r{r}c{c}"
            nodes.append(nid); coords[nid] = (c * A_UM, r * A_UM)
    edges = []
    for a, b in combinations(nodes, 2):
        d = math.hypot(coords[a][0]-coords[b][0], coords[a][1]-coords[b][1])
        if d <= R_B_UM + 1e-9:
            edges.append((a, b))
    return nodes, coords, edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--submit", action="store_true")
    ap.add_argument("--shots", type=int, default=SHOTS_DEFAULT)
    args = ap.parse_args()

    print(f"Castello 49 — FRESNEL prep")
    nodes, coords, edges = build_grid_7x7()
    density = 2*len(edges) / (len(nodes)*(len(nodes)-1))
    print(f"  N={len(nodes)} E={len(edges)} d={density:.4f}")
    print(f"  a={A_UM} µm, R_b={R_B_UM} µm, Ω={OMEGA:.4f} rad/µs, T={T_NS} ns")

    xs = [coords[n][0] for n in nodes]; ys = [coords[n][1] for n in nodes]
    cx, cy = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2
    centred = {n: (float(coords[n][0]-cx), float(coords[n][1]-cy)) for n in nodes}

    from pasqal_cloud import SDK
    from pulser import Register, Pulse, Sequence
    from pulser.devices import Device
    from pulser.waveforms import InterpolatedWaveform

    sdk = SDK(project_id=PROJECT_ID, username=USER, password=PWD)
    specs = sdk.get_device_specs_dict()
    device = Device.from_abstract_repr(specs["FRESNEL_CAN1"])

    raw_reg = Register(centred)
    reg = raw_reg.with_automatic_layout(device)
    print(f"  layout: {len(centred)} atoms, {reg.layout.number_of_traps} traps")

    seq = Sequence(reg, device)
    seq.declare_channel("ising", "rydberg_global")
    seq.add(Pulse(
        InterpolatedWaveform(T_NS, [1e-9, OMEGA, OMEGA, OMEGA]),
        InterpolatedWaveform(T_NS, [DELTA_NEG, DELTA_NEG, 0, DELTA_POS]), 0,
    ), "ising")

    if not args.submit:
        print("\n[dry run] pass --submit"); return

    batch = sdk.create_batch(serialized_sequence=seq.to_abstract_repr(),
                             jobs=[{"runs": args.shots}], emulator=None)
    bid = str(batch.id)
    print(f"\nsubmitted to FRESNEL_CAN1: {bid}")

    summary = {"batch_id": bid, "device": "FRESNEL_CAN1", "shots": args.shots,
               "N": len(nodes), "E": len(edges), "density": round(density, 4),
               "a_um": A_UM, "r_b_um": R_B_UM,
               "omega_rad_per_us": round(OMEGA, 5), "T_ns": T_NS,
               "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (OUT_DIR / "batches.json").write_text(json.dumps(summary, indent=2))
    print(f"recorded {OUT_DIR}/batches.json")


if __name__ == "__main__":
    main()
