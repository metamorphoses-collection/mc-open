# Pacioli Dodecahedron — 3D engineered register showcase

**Proper name (main text figures)**: *Pacioli dodecahedron — 3D N=20 d=0.16 α=8*

**Role in the paper**: the **3D engineered-register showcase**. The regular dodecahedron is the Platonic solid Luca Pacioli devoted a section of his *De Divina Proportione* (Venezia 1509) to, illustrated by Leonardo da Vinci. It is the paper's period-anchored, literary-humanist-rooted 3D unit-ball graph — exact, small enough for EMU_MPS, and empirically NOT 2L-realizable (SA combined fidelity saturates at ~0.77 on bi-layer search).

---

## Graph definition

The **1-skeleton of the regular dodecahedron**: 20 vertices at the corners of the Platonic solid, 30 edges (5 per pentagonal face × 12 faces / 2), **3-regular**, non-planar, non-bipartite (contains 5-cycles).

## Unit-ball realization

Using the standard canonical coordinates (8 cube vertices `(±1, ±1, ±1)` plus 12 rectangle vertices `(0, ±φ, ±φ⁻¹)` and cyclic permutations, where φ = (1+√5)/2 is the golden ratio):

- **Scale factor**: 5.0 µm → edge length **2·5/φ = 6.18 µm < R_b ✓**
- **Next-shortest pair distance**: **2·5 = 10.0 µm > R_b ✓** (the non-edges, at ratio φ to the edges)
- **Minimum inter-atom distance**: 6.18 µm > Pasqal floor (2.0 µm) ✓

**Exact 3D unit-ball graph at R_b = 8.0 µm.** All 30 edges blockade, all 160 non-edges do not. Zero embedding loss.

## Invariants

- **N**: 20
- **E**: 30
- **Density**: 0.158
- **Classical MIS α**: **8** (one of several equivalent max independent sets)
- **3-regular**: every vertex has exactly 3 neighbours
- **Not bipartite**: contains pentagonal 5-cycles (odd cycles)
- **Planar**: yes, as the 1-skeleton of a convex polytope (Euler characteristic holds)
- **Exact 3D UDG**: yes, via golden-ratio spacing
- **2L realizability**: **NO**. Best 2L SA combined fidelity saturates at 0.767 (from `graph_pacioli_dodecahedron.json` verification run). The dodecahedron requires full 3D coordinates.

## How it was built

Generated programmatically by `3_MIS/quantum/core/build_dodecahedron.py`:

1. Standard dodecahedron coordinates (cube + rectangle generators, golden-ratio proportioned)
2. Edges taken as the 30 shortest pairwise distances (verified 3-regular)
3. UDG verification at R_b = 8.0 µm, scale = 5.0 µm
4. 2L SA feasibility check: 6 restarts × 400k iterations of the sa_embed_2d_2L_3d 2L embedder, best combined fidelity = 0.767

## Graph file

- **Definition, coordinates, verification, 2L SA test**: `3_MIS/oulipo/graphs/graph_pacioli_dodecahedron.json`

## Quantum status (2026-04-11)

**Submitted in the 6-cell new EMU run** (`20260411_6cell_new`), as the **3D engineered cell**:

- 1 noiseless batch + 5 noisy batches (Constantin Apr-10 calibration)
- Total 1200 shots on EMU_MPS, free compute
- **Results pending** at time of this README (submission is in-flight)

Expected based on the exact 3D UDG + 3-regular + small N: noiseless valid ~100%, noisy valid ≥ 85%, best IS very close to classical MIS (α = 8).

## Why this graph and this graph only as the 3D showcase

1. **Pacioli 1509 + Leonardo 1509 are exactly the period the paper's natural corpus lives in** (Giambullari 1544, Damiano 1512). The dodecahedron is the literary-humanist 3D object; no other Platonic solid has Leonardo's drawings of the same specificity.
2. **Exact 3D UDG by construction** (golden-ratio spacing), so there is zero embedding loss. Unlike Sonetti dal Tesseratto (Q_4) or La vita nel cubo (truncated cube + long-range), which I tried earlier and discarded because they are NOT exactly unit-ball-realizable, the dodecahedron is clean.
3. **Not 2L-realizable** (empirical SA ceiling 0.77). **This is the paper's only engineered 3D graph that genuinely needs the third dimension** — unlike the 5×5×2 king graph, which can also be flattened to 2L but benefits from the bi-layer structure. The dodecahedron cannot be flattened without fidelity loss.
4. **3-regular and N = 20** is the cleanest structural pair for a 3D showcase: low enough density that it fits comfortably in Constantin's noise model budget, high enough connectivity that the MIS = 8 out of 20 vertices is non-trivial (ratio 0.4 for the classical optimum).
5. **Completes the engineered-register trio**: king 4×4 (2D), 5×5×2 king (2L), Pacioli dodecahedron (3D). Three graphs, three register tiers, three Italian Renaissance period anchors (Damiano chess treatise 1512, Italian military garrison layout lineage, Pacioli *De Divina Proportione* 1509).

## Companion graphs in the showcase family

- **King 4×4**: the 2D endpoint (flat)
- **King 5×5×2**: the 2L endpoint (bi-layer)
- **Pacioli dodecahedron**: the 3D endpoint (full)

The three showcase registers span the 2D / 2L / 3D staircase with matched "small-N, exact-unit-ball, high-ratio" properties.

## Not to be confused with

- **Sonetti dal Tesseratto** (Q_4, literary artifact only, NOT 3D-UDG realizable — the 4-cube requires 4 orthogonal axes)
- **La vita nel cubo** (truncated cube + 6 thematic long-range edges, literary artifact only, NOT unit-ball-realizable because the 6 long-range edges span more than R_b)
- Both of these are in S3 Appendix as literary-artifact-only entries; only the Pacioli dodecahedron is the paper's quantum 3D showcase.
