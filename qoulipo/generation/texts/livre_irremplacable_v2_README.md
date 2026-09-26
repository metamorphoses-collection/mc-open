# *Le Livre irremplaçable — v2* (dense-cluster constraint)

**Proper name (main text)**: *Le Livre irremplaçable v2 (FR) N=50 k=11*

**Role in the paper**: **highest designed density in the main corpus** (0.234). Second-highest engineered F1 at its matched adaptive k (0.675 at k=11). Anchors the §dense-cluster argument and serves as the density-ladder upper endpoint for the pipeline-inverse experiment.

---

## Text

- **Author**: (engineered by the project)
- **Language**: French
- **Page count**: 50
- **Word count**: ~17,800
- **File**: `3_MIS/oulipo/texts/livre_irremplacable_v2.md`
- **Version**: v2 (revision of the earlier `livre_irremplacable.md`, with tighter thematic structure)
- **Homage**: Bernard Maréchal (ZaZiPo lineage)

## Constraint (dense thematic-cluster)

The text's constraint is the **opposite extreme of Procès de Nithard's bipartite**: instead of forcing edges to span an A/B partition, Le Livre irremplaçable forces edges into **dense thematic clusters**. Pages within a cluster share many threads (leading to thread-overlap ≥ 4 edges), pages in different clusters share very few.

**Thread vocabulary**: ~12 threads, 5 per page.

**Thread-overlap rule**: threshold ≥ 4 for a designed edge, same as the rest of the 50-page corpus.

The effect is a graph with several dense "islands" connected by sparse inter-island edges — classically the kind of structure where community-detection algorithms work well and where MIS has a small number of tight solutions.

## Graph invariants (v2)

- **N**: 50
- **Designed edges at threshold ≥ 4**: 287
- **Density**: **0.234** — **highest in the main engineered corpus**
- **Average designed degree**: ~11.5 (adaptive **k*=11**)
- **Graph family**: dense thematic-cluster (several 8–12-page cliques with occasional bridging edges)

## Pipeline-inverse recovery

Using e5-large-instruct at canonical k values plus adaptive k*:

| k | recall | precision | F1 |
|---|---|---|---|
| 8 | 0.606 | 0.680 | 0.641 |
| **11*** (adaptive) | 0.7–0.75 | 0.6–0.65 | **0.675** |
| 16 | 0.840 | 0.504 | 0.630 |
| 24 | 0.951 | 0.395 | 0.558 |

**Best F1 = 0.675** at k=11 (matched adaptive). This is the **highest F1 in the dense-cluster family** and second only to Kaléidoscope's 1.000 and the 65-page hardzone books in the engineered corpus.

**Key observation**: v2 outperforms v1 by 0.048 F1 (0.675 vs 0.627). The v2 rewrite tightened the thematic clustering and made the designed structure more semantically coherent, which the pipeline recovers better. This is the only A/B-test pair in the paper showing that *rewriting for tighter constraint* improves *pipeline recoverability*.

## Quantum status (2026-04-11)

Not currently submitted to any EMU / QPU target. At N=50 and density 0.234, the graph is medium-density and the classical MIS solver handles it in milliseconds. The quantum argument on this text is not about raw advantage but about the **constrained-writing methodology**: if a writer can produce a dense-cluster text recoverable at F1 = 0.675, the pipeline is reliable for denser test cases too.

## Why this book and this book only

1. **Highest main-text engineered density** (0.234). Every other main-text engineered book is sparser. Without it the paper would be missing the upper endpoint of the density ladder.
2. **A/B comparison with v1** is unique in the engineered corpus. The +0.048 F1 lift from v1 to v2 is the cleanest demonstration that rewriting matters.
3. **French language balance**: together with Procès de Nithard, Le Livre irremplaçable v2 is the French half of the main-text engineered corpus.
4. **Dense-cluster graph family**: different from the bipartite (Procès), the hard-zone (Nithard's Wager), the triangle-triptych (Kaléidoscope), and the UDG-structured (UDG 65 text) families. Covers the fifth constraint family.

## Not to be confused with

- **livre_irremplacable.md** (v1) — the original version, F1 = 0.627. In appendix only.
- **livre_irremplacable_v2.validation.json** — thread-assignment validation file, not a separate text.
- **livre_fractal.md** — a different book in the fractal-hierarchy family; unrelated.
