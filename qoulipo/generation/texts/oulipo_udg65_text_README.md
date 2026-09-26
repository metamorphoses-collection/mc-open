# *The UDG 65 Text* — largest hard-zone UDG engineered text

**Proper name (main text)**: *UDG 65 text (EN) N=65 k=13*

**Role in the paper**: **the largest native-UDG engineered text**. The only book in the main corpus explicitly designed so that its designed k-NN graph is *by construction* a 2D unit-disk graph — meaning it can be submitted to FRESNEL directly on flat 2D hardware, without any embedding loss. F1 = 0.746 via plain e5-large-instruct, the second-highest engineered-text F1 in the 65-page family after Hardzone Nithard's Wager.

---

## Text

- **Author**: (engineered by the project)
- **Language**: English
- **Page count**: 65
- **Word count**: ~20,200
- **File**: `3_MIS/oulipo/texts/oulipo_udg65_text.md`

## Constraint (unit-disk graph by design)

The text is written so its thread-overlap graph (threshold ≥ 4) is, provably, a **2D unit-disk graph**. Each page corresponds to a point in a 2D thematic space; two pages share enough threads (edge in the similarity graph) iff their thematic points are close enough (within R_b in the designed 2D embedding).

This is the strongest possible constraint family for quantum applications: **the designed graph is the register**. There is no embedding loss, no fidelity gap between the target and what the Rydberg array enforces — by construction. All the classical MIS ILP solutions are valid quantum MIS solutions on a 2D register.

## Thread design

- **Thread vocabulary**: tightly coupled to a 2D UDG layout
- **Threads per page**: 5
- **Overlap threshold**: ≥ 4 (per the finetune_embedder.py recipe)

## Graph invariants

- **N**: 65
- **Designed edges at threshold ≥ 4**: 420
- **Density**: **0.202** — dense (denser than Nithard's Wager 0.133)
- **Average designed degree**: ~13 (adaptive **k*=13**)
- **Graph family**: native 2D unit-disk graph, spatially structured
- **By construction**: realizable as a 2D UDG on a physical register, no embedding SA needed

## Pipeline-inverse recovery

Using e5-large-instruct:

| k | recall | precision | F1 |
|---|---|---|---|
| 8 | 0.636 | 0.790 | 0.704 |
| **13*** (adaptive) | ~0.75 | ~0.74 | **0.746** |
| 16 | 0.898 | 0.604 | **0.722** |
| 24 | 0.971 | 0.443 | 0.609 |

**Best F1 = 0.746** at k=13. Second-highest in the 65-page family after Nithard's Wager Hard-Zone EN (0.764). The precision is **0.79 at k=8** — the highest precision in the engineered corpus outside Kaléidoscope — because the UDG structure naturally matches small-k neighbourhoods.

## Quantum status (2026-04-11)

**Candidate for a FRESNEL 2D QPU run** (planned but not yet submitted). Because the designed graph is a native 2D UDG, the QPU submission is trivial: the atom positions are given by the designed 2D coordinates, no SA embedding needed. **This is the most direct engineered-text-to-QPU path in the corpus.**

Submission would use:
- blockade radius R_b = 8.0 µm
- minimum inter-atom distance ≥ 5.0 µm (FRESNEL_CAN1 floor)
- standard adiabatic pulse (4 µs, Ω = C6/R_b^6)
- 500 shots
- Expected classical MIS comparison against ILP on the same graph

## Why this book and this book only

1. **Only native 2D UDG engineered text in the main corpus**. Every other engineered book (Kaléidoscope, Hardzone Nithard, Procès, Livre irremplaçable) has a designed graph that is *not* guaranteed 2D-UDG and requires SA embedding with fidelity loss. UDG 65 text is the only case where designed graph = register graph.
2. **Direct 2D FRESNEL candidate** — ready for the QPU pitch without the usual embedding-fidelity caveat.
3. **High-precision recovery** (prec = 0.79 at k=8) — the UDG structure's spatial correlations match k-NN neighbourhoods directly, giving the cleanest engineered-text recovery profile.
4. **65-page family companion** to Nithard's Wager: N=65, same page count, different constraint family — the two 65-page books together span "hard-zone dense" (Nithard's Wager) and "hard-zone UDG" (UDG 65).
5. **QPU pitch clarity**: when a reviewer asks "what would you run on a 2D Rydberg machine right now", the answer is UDG 65 text, not a natural text (which needs a lossy SA embedding) and not an engineered non-UDG text (Kaléidoscope, Procès).

## Not to be confused with

- **oulipo_udg_50pages.md** (FR) / **oulipo_udg_50pages_en.md** (EN) — smaller 50-page UDG texts, F1 ≈ 0.63–0.65. In appendix only.
- **oulipo_udg100_text.md** — 100-page UDG extension (threads missing in current parser, needs preprocessing). In appendix only.
