# 4×4 King Graph — 2D flat showcase

**Proper name (main text figures)**: *4×4 king graph — 2D N=16 d=0.35 α=4*

**Role in the paper**: the **2D engineered-register showcase**. Not a constraint text; it is a pure graph-family demonstration that anchors the §7 register-geometry staircase on the flat-2D endpoint. Runs on Pasqal FRESNEL_CAN1 2D hardware today. **First (and so far only) Rydberg MIS result in the paper at ratio = 1.000 both noiseless AND noisy** on the same register.

---

## Graph definition

The **king graph on a 4×4 chessboard**: 16 vertices at grid positions (i, j) for i, j ∈ {0, 1, 2, 3}. Two vertices are connected iff `max(|Δi|, |Δj|) ≤ 1` and `(Δi, Δj) ≠ (0, 0)` — the chess king's move set.

## Unit-disk realization

Placed on a unit grid with spacing **s = 5.6 µm** and blockade radius **R_b = 8.0 µm**:

- **Edges (king's diagonal)**: distance s√2 = **7.92 µm < R_b ✓** — all king's moves blockade
- **Non-edges (king's leap, 2 steps)**: distance 2s = **11.2 µm > R_b ✓** — king's-leap non-moves do not blockade
- **Minimum inter-atom distance**: 5.6 µm > FRESNEL_CAN1 floor (5.0 µm) ✓

**Exact 2D unit-disk graph at R_b = 8.0 µm.** No embedding loss, no fidelity gap, no SA optimization needed. The graph IS the register.

## Invariants

- **N**: 16
- **E**: 42
- **Density**: 0.350
- **Classical MIS α**: **4** (four non-attacking kings, e.g. the four corners (0,0), (0,3), (3,0), (3,3))
- **Degree distribution**: corners have 3 neighbours, edge pieces have 5, interior pieces have 8
- **Not bipartite**: contains K_3 (triangles at 3-way corners)
- **Not planar**: contains K_5 (e.g. at the interior 3×3 block)
- **Exact 2D UDG**: yes, proven by the spacing argument above

## How it was built

Generated programmatically by `3_MIS/quantum/core/build_2d_2L_3d_showcase.py`. No constraint text associated — the showcase is pure geometry. The related Italian constraint text *Il quadrato dei re* (`il_quadrato_dei_re.md`, 16 short chapters, period allusion to Damiano's *Libro da imparare giuocare a scacchi*, Rome 1512) was written on this graph but is classified as a showcase artifact, not a main-text engineered entry.

## Graph file

- **Definition + coordinates**: `3_MIS/oulipo/graphs/showcase_2d_2L_3d.json` key `2D_4x4x1_king`
- **Pipeline-inverse result** (against the chapter text Il quadrato dei re): F1 = 0.538 at k=8 (moderate — the text is very short and the designed graph is recovered only partially from prose, but this is not the point of the showcase)

## Quantum status (2026-04-11)

### Phase 1 3D EMU_MPS noisy sweep (from `20260411_noisy_3d_small_set`)

Noiseless + noisy Constantin-calibrated EMU_MPS on the exact 4×4 register (z=0 flat, treated as 3D with one layer):

| mode | shots | valid% | best IS | ratio | ⟨w⟩ |
|---|---|---|---|---|---|
| **noiseless** | 500 | **100.0%** | **4** | **1.000** | 3.99 |
| **noisy** (5 × 200, Constantin Apr-10) | 1000 | **86.8%** | **4** | **1.000** | 3.69 |

**Both noiseless and noisy reach the classical MIS optimum of 4 (all four corners).** The 86.8% noisy validity is dominated by SPAM errors (1.5% false-pos, 9% false-neg) applied to atoms that are individually correct. **No ratio degradation under noise.**

### Planned FRESNEL_CAN1 QPU run

QPU submission: 1 run, 500 shots. Expected ratio ≥ 0.9 based on the EMU numbers above. This is the **single cleanest "runs on real 2D hardware today"** result the paper can show, and the register photo from FRESNEL will be the first physical-atoms panel in §Hardware.

## Why this graph and this graph only as the 2D showcase

1. **Smallest N at which ratio = 1.000 both noiseless and noisy is non-trivial**: N < 10 is too trivial to convince anyone; N > 20 gets into optimization-variance territory. N = 16 is the sweet spot.
2. **Exact 2D UDG means zero embedding loss** — the register perfectly realizes the target graph, so the result tests the quantum pipeline, not the SA embedder.
3. **FRESNEL-ready**: min atom distance 5.6 µm > 5.0 µm floor, max radial distance 8.4 µm < 46 µm FRESNEL limit. Drop-in submission.
4. **Period-matched to Damiano 1512**: the first printed chess treatise in Europe is contemporaneous with Giambullari 1544 and Pacioli 1509. The showcase sits naturally next to the natural texts in the paper's Florentine-humanist frame.
5. **Literary companion exists** (*Il quadrato dei re*, 16 short chapters) should a reviewer want narrative context — but the main-text argument is purely the graph.

## Companion graphs in the showcase family

- **5×5 king graph** (N=25, d=0.24, α=9) — same family, larger. Used in §7 Figure gallery Option A/C top row.
- **5×5×2 king graph** (N=50, d=0.26, α=9) — the 2L extension. Used as the **2L engineered cell** of the 6-cell EMU table.
