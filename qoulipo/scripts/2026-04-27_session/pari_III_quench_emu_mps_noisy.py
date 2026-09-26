#!/usr/bin/env python3
"""Pari de Nithard III (N=100) quench, EMU_MPS WITH FRESNEL noise model, T=4µs.

§6.2 second-leg-of-fork submission. Same protocol as the noiseless run
but with the canonical Pasqal Cloud FRESNEL_CAN1 default noise model
(SPAM 0.025/0.10, T2*=4.5µs, T1=100µs, state_prep_error=0).

Result (decoded after ~4h cloud-emulator wall time):
  status DONE, has_result=False, errors=None
  total_shots=0, no bitstrings returned
  → silent resource-exhaustion failure mode = bond-dimension/Krylov ceiling
  → instantiates the §6.2 fork second-leg DNF
"""
import os
import json, math, time
from pathlib import Path

CORPUS = Path("corpus/qoulipo/pari_de_nithard_III")
OUT = Path(__file__).parent / "pari_III_emu_mps_noisy"
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
T_QUENCH_NS = 4000
SHOTS = 200

# Canonical FRESNEL_CAN1 noise (Pasqal Cloud API default,
# source: quantum/fresnel_noise_params_api.json retrieved 2026-04-09).
NOISE_PARAMS = {
    "p_false_pos": 0.025,
    "p_false_neg": 0.10,
    "relaxation_rate": 0.01,
    "dephasing_rate": 0.22222222222222222,
    "state_prep_error": 0.0,
}


def main():
    g = json.loads((CORPUS / "graph_knn.json").read_text())
    nodes = g["nodes"]; positions = g["positions"]
    N = len(nodes)
    print(f"Pari III: N={N}, SA fidelity={g.get('fidelity'):.3f}")

    from pulser import Register, Pulse, Sequence
    from pulser.devices import VirtualDevice
    from pulser.waveforms import InterpolatedWaveform, ConstantWaveform
    from pulser.channels import Rydberg
    from pulser.noise_model import NoiseModel
    from pulser.backend.config import EmulationConfig
    from pasqal_cloud import SDK

    ch = Rydberg.Global(max_abs_detuning=2*math.pi*50, max_amp=2*math.pi*20,
                        clock_period=1, min_duration=16, max_duration=100_000_000)
    dev = VirtualDevice(name="FresnelLike2D", dimensions=2, rydberg_level=70,
                        max_atom_num=120, max_radial_distance=120, min_atom_distance=2.0,
                        supports_slm_mask=False, channel_objects=(ch,))
    qubits = {f"q{i}": (float(positions[n][0]), float(positions[n][1]))
              for i, n in enumerate(nodes)}
    reg = Register(qubits)

    seq = Sequence(reg, dev)
    seq.declare_channel("ising", "rydberg_global")
    seq.add(Pulse(InterpolatedWaveform(T_PREP_NS, [1e-9, OMEGA, OMEGA]),
                  InterpolatedWaveform(T_PREP_NS, [DELTA_NEG, DELTA_NEG, DELTA_NEG]), 0), "ising")
    seq.add(Pulse(ConstantWaveform(T_QUENCH_NS, OMEGA),
                  ConstantWaveform(T_QUENCH_NS, DELTA_POS), 0), "ising")

    noise = NoiseModel(runs=100, **NOISE_PARAMS)
    cfg = EmulationConfig(noise_model=noise)
    cfg_str = cfg.to_abstract_repr()

    sdk = SDK(project_id=PROJECT_ID, username=USER, password=PWD)
    print("Submitting noisy EMU_MPS at T=4µs...")
    try:
        b = sdk.create_batch(serialized_sequence=seq.to_abstract_repr(),
                             jobs=[{"runs": SHOTS}], emulator="EMU_MPS",
                             backend_configuration=cfg_str)
        info = {"batch_id": str(b.id), "T_ns": T_QUENCH_NS, "shots": SHOTS,
                "noise": NOISE_PARAMS, "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        print(f"  -> batch {b.id}")
    except Exception as e:
        info = {"error": str(e)[:500]}
        print(f"  ERROR: {e}")

    (OUT / "batch.json").write_text(json.dumps(info, indent=2))
    print(f"\nSaved {OUT}/batch.json")


if __name__ == "__main__":
    main()
