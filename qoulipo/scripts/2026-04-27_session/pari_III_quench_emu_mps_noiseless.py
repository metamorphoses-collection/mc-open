#!/usr/bin/env python3
"""Pari de Nithard III (N=100) quench, EMU_MPS NOISELESS, T = 1, 2, 4 µs.

§6.2 first-leg-of-fork submission. Pasqal Cloud's noiseless MPS backend
on the same protocol the FRESNEL QPU runs.

Result (decoded after completion, 200 shots each):
  T=1µs: valid 0.5%  best IS 4/26  ratio 0.154  mean HW 13.6
  T=2µs: valid 1.0%  best IS 6/26  ratio 0.231  mean HW 13.3
  T=4µs: valid 0%    best IS 0/26  ratio 0.000  mean HW 14.4
"""
import os
import json, math, time
from pathlib import Path

CORPUS = Path("corpus/qoulipo/pari_de_nithard_III")
OUT = Path(__file__).parent / "pari_III_emu_mps_noiseless"
OUT.mkdir(parents=True, exist_ok=True)

PROJECT_ID = "9311685e-cc0c-43b2-8db6-6e11d352878a"
USER = os.environ["PASQAL_USER"]   # your Pasqal cloud login
PWD = "zomfeg-0hoDby-ruhzij"

R_B = 8.0
C6 = 865723
OMEGA = C6 / R_B ** 6
DELTA_NEG = -3 * OMEGA
DELTA_POS = +3 * OMEGA
T_PREP_NS = 500
T_QUENCH_NS_LIST = [1000, 2000, 4000]
SHOTS = 200


def main():
    g = json.loads((CORPUS / "graph_knn.json").read_text())
    nodes = g["nodes"]; positions = g["positions"]
    N = len(nodes)
    print(f"Pari III: N={N}, SA fidelity={g.get('fidelity'):.3f}")

    from pulser import Register, Pulse, Sequence
    from pulser.devices import VirtualDevice
    from pulser.waveforms import InterpolatedWaveform, ConstantWaveform
    from pulser.channels import Rydberg
    from pasqal_cloud import SDK

    ch = Rydberg.Global(max_abs_detuning=2*math.pi*50, max_amp=2*math.pi*20,
                        clock_period=1, min_duration=16, max_duration=100_000_000)
    dev = VirtualDevice(name="FresnelLike2D", dimensions=2, rydberg_level=70,
                        max_atom_num=120, max_radial_distance=120, min_atom_distance=2.0,
                        supports_slm_mask=False, channel_objects=(ch,))
    qubits = {f"q{i}": (float(positions[n][0]), float(positions[n][1]))
              for i, n in enumerate(nodes)}
    reg = Register(qubits)
    sdk = SDK(project_id=PROJECT_ID, username=USER, password=PWD)
    print("Submitting noiseless EMU_MPS, T=1, 2, 4 µs...")
    batches = {}
    for T_ns in T_QUENCH_NS_LIST:
        seq = Sequence(reg, dev)
        seq.declare_channel("ising", "rydberg_global")
        seq.add(Pulse(InterpolatedWaveform(T_PREP_NS, [1e-9, OMEGA, OMEGA]),
                      InterpolatedWaveform(T_PREP_NS, [DELTA_NEG, DELTA_NEG, DELTA_NEG]), 0), "ising")
        seq.add(Pulse(ConstantWaveform(T_ns, OMEGA),
                      ConstantWaveform(T_ns, DELTA_POS), 0), "ising")
        try:
            b = sdk.create_batch(serialized_sequence=seq.to_abstract_repr(),
                                 jobs=[{"runs": SHOTS}], emulator="EMU_MPS")
            batches[f"quench_t{T_ns}ns"] = {"batch_id": str(b.id), "T_ns": T_ns,
                                            "shots": SHOTS}
            print(f"  T={T_ns}ns: {b.id}")
        except Exception as e:
            batches[f"quench_t{T_ns}ns"] = {"error": str(e)[:300], "T_ns": T_ns}
            print(f"  T={T_ns}ns: ERROR {e}")
        time.sleep(1)
    summary = {"campaign": "Pari III noiseless EMU_MPS quench",
               "N": N, "E": len(g["edges"]), "fidelity": g.get("fidelity"),
               "backend": "EMU_MPS", "noise": None,
               "T_ns_list": T_QUENCH_NS_LIST, "shots": SHOTS, "batches": batches,
               "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (OUT / "batches.json").write_text(json.dumps(summary, indent=2))
    print(f"\nSaved {OUT}/batches.json")


if __name__ == "__main__":
    main()
