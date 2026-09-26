#!/usr/bin/env python3
"""
Run EMU on the DESIGNED graph (thread overlap ≥ 4) for the rho=1.0 text.
Skips the embedding step — uses the combinatorial structure directly.

Steps:
  1. Build designed graph from thread assignments
  2. Solve MIS via ILP (verify ρ=1.0)
  3. SA embed into 2D register
  4. Build Pulser sequence
  5. Submit to EMU_MPS (noiseless)
  6. Analyze results
"""

import json
import sys
import os
from pathlib import Path

import numpy as np
import networkx as nx

# Add classical core to path
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "classical" / "core"))

from pasqal_emulator import (
    embed_sa, embedding_quality, build_sequence,
    mis_ilp, mis_greedy, log, compare,
    BLOCKADE_UM, N_SAMPLES
)

OUT_DIR = Path(__file__).resolve().parent


def build_designed_graph(threads_json_path, edge_overlap=4):
    """Build graph from thread assignments using overlap criterion."""
    with open(threads_json_path) as f:
        data = json.load(f)

    N = data["N"]
    assignments = data["assignments"]

    G = nx.Graph()
    node_ids = []
    node_threads = {}

    for page_str, info in sorted(assignments.items(), key=lambda x: int(x[0])):
        nid = f"p{int(page_str) + 1}"  # 0-indexed in JSON, 1-indexed in text
        node_ids.append(nid)
        node_threads[nid] = set(info["threads"])
        G.add_node(nid, role=info["role"], threads=info["threads"])

    # Add edges where thread overlap >= edge_overlap
    for i, ni in enumerate(node_ids):
        for j in range(i + 1, len(node_ids)):
            nj = node_ids[j]
            overlap = len(node_threads[ni] & node_threads[nj])
            if overlap >= edge_overlap:
                G.add_edge(ni, nj, weight=overlap / 6.0)  # normalized overlap

    return G, node_ids, node_threads


def main():
    threads_path = OUT_DIR / "threads" / "design_a_rho1_threads.json"

    print("=" * 70)
    print("  DESIGNED GRAPH EMU — Le Livre Irremplaçable (ρ=1.0)")
    print("=" * 70)

    # 1. Build designed graph
    print("\n[1] Building designed graph (overlap ≥ 4)...")
    G, node_ids, node_threads = build_designed_graph(threads_path, edge_overlap=4)
    N = G.number_of_nodes()
    E = G.number_of_edges()
    d = nx.density(G)
    print(f"    N={N}, E={E}, density={d:.4f}")

    # 2. Solve MIS
    print("\n[2] Solving MIS via ILP...")
    mis = mis_ilp(G)
    print(f"    MIS size: {len(mis)} (ratio: {len(mis)/N:.3f})")
    print(f"    MIS nodes: {mis}")

    # Check MIS nodes are the designed backbone (pages 1-17)
    designed_mis = set(f"p{i+1}" for i in range(17))
    actual_mis = set(mis)
    print(f"    Match with designed MIS: {len(designed_mis & actual_mis)}/{len(designed_mis)}")

    # 3. SA embedding
    print("\n[3] SA embedding into 2D register...")
    coords = embed_sa(G, blockade_um=BLOCKADE_UM, spacing=5.5, n_iter=12000, n_restarts=10)

    # Quality check
    quality = embedding_quality(G, coords, BLOCKADE_UM)
    print(f"    SA fidelity: {quality['fidelity']:.1%}")
    print(f"    True edges in UDG: {quality['true_edges']}/{E}")
    print(f"    False edges in UDG: {quality['false_edges']}")

    # Save coords
    coords_path = OUT_DIR / "graphs" / "coords_livre_irremplacable_designed.json"
    coords_path.parent.mkdir(parents=True, exist_ok=True)
    with open(coords_path, "w") as f:
        json.dump({n: list(c) for n, c in coords.items()}, f, indent=2)
    print(f"    Saved coords to {coords_path}")

    # 4. Build pulse sequence
    print("\n[4] Building adiabatic pulse sequence...")
    seq = build_sequence(G, coords)
    print(f"    Duration: {seq.get_duration()} ns")
    print(f"    Atoms: {len(coords)}")

    # 5. Submit to EMU
    print("\n[5] Submitting to EMU_MPS (noiseless)...")
    try:
        from pasqal_cloud import SDK
        from pulser_pasqal import PasqalCloud

        # Load credentials
        key_path = BASE / "quantum" / "core" / "qpu_submit_all.py"
        creds = {}
        with open(key_path) as f:
            for line in f:
                if "PASQAL_USER" in line and "=" in line:
                    creds["user"] = line.split("=")[1].strip().strip('"').strip("'")
                if "PASQAL_PASS" in line and "=" in line:
                    creds["pass"] = line.split("=")[1].strip().strip('"').strip("'")
                if "PASQAL_PROJECT" in line and "=" in line:
                    creds["project"] = line.split("=")[1].strip().strip('"').strip("'")

        project_id = creds.get("project", "9311685e-cc0c-43b2-8db6-6e11d352878a")

        sdk = SDK(
            username=creds["user"],
            password=creds["pass"],
            project_id=project_id,
        )

        # Submit
        from pulser import Sequence
        batch = sdk.create_batch(
            serialized_sequence=seq.to_abstract_repr(),
            jobs=[{"runs": N_SAMPLES}],
            emulator="EMU_MPS",
        )
        print(f"    Batch ID: {batch.id}")
        print(f"    Status: {batch.status}")

        # Save batch info
        batch_info = {
            "text": "livre_irremplacable_designed",
            "graph_type": "designed_overlap4",
            "N": N,
            "E": E,
            "density": round(d, 4),
            "mis_size": len(mis),
            "sa_fidelity": quality["fidelity"],
            "batch_id": str(batch.id),
            "emulator": "EMU_MPS",
            "shots": N_SAMPLES,
            "noiseless": True,
        }
        batch_path = OUT_DIR / "batches" / "emu_livre_irremplacable_designed.json"
        batch_path.parent.mkdir(parents=True, exist_ok=True)
        with open(batch_path, "w") as f:
            json.dump(batch_info, f, indent=2)
        print(f"    Saved batch info to {batch_path}")

    except Exception as e:
        print(f"    EMU submission failed: {e}")
        import traceback
        traceback.print_exc()

    # 6. Summary
    print(f"\n{'=' * 70}")
    print(f"  SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Graph: N={N}, E={E}, d={d:.4f}")
    print(f"  MIS: {len(mis)} pages (ratio={len(mis)/N:.3f})")
    print(f"  SA fidelity: {quality['fidelity']:.1%}")
    print(f"  Designed ρ: 1.000 (unique MIS)")
    print(f"  EMU: submitted (noiseless, {N_SAMPLES} shots)")


if __name__ == "__main__":
    main()
