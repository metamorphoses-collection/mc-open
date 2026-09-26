# *Le Kaléidoscope* — 17-triptych constraint with ρ = 0

**Proper name (main text)**: *Le Kaléidoscope (EN) N=51 k=2*

**Role in the paper**: **ρ=0 showcase**. The **only text in the whole corpus to reach F1 = 1.000** in pipeline-inverse recovery. Anchors the paper's rigidity argument: Kaléidoscope has the maximum-possible backbone fungibility (no essential pages) and the NLP pipeline recovers the designed graph perfectly at the matched adaptive k.

---

## Text

- **Author**: (engineered by the project)
- **Language**: English
- **Homage**: Bernard Maréchal (ZaZiPo founder, Christophe's former professor)
- **Page count**: 51
- **Word count**: ~18,600
- **File**: `3_MIS/oulipo/texts/kaleidoscope.md`
- **Epigraph**: *"every reading is valid"*

## Constraint (ρ = 0 by design)

**17 triptychs**. Each triptych is a group of 3 pages sharing an **identical thread set**, making them mutually interchangeable in any Maximum Independent Set solution. Every triptych contributes exactly 1 page to any optimal MIS; the pipeline has 3^17 = 129,140,163 valid backbones. **Rigidity ρ = 0.000** by construction: no single page is essential, because any page can be swapped for either of its two twins.

Each triptych presents the same thematic material through three narrative lenses:

- **Version A** — the **WITNESS** (first person, sensory, immediate)
- **Version B** — the **ANALYST** (third person, critical, distant)
- **Version C** — the **DREAMER** (second person, speculative, counterfactual)

## Thread vocabulary (15 threads, 5 per page)

| # | Thread | Domain |
|---|---|---|
| 0 | WAGER | Probability, risk, decision under uncertainty |
| 1 | CHRONICLE | Historical record, witnessed events |
| 2 | CONSPIRACY | Fabrication, forgery, hidden agendas |
| 3 | TONGUE | Language, translation, birth of vernacular |
| 4 | NUMBER | Mathematics, combinatorics, counting |
| 5 | FAITH | Belief, doubt, silence of God |
| 6 | SWORD | War, conflict, fratricidal violence |
| 7 | PARCHMENT | Manuscripts, textual transmission |
| 8 | MALIETTE | The teacher, ZaZiPo, the gift of reading |
| 9 | GAME | OuLiPo, ludic constraint, rules that free |
| 10 | MIRROR | Reflection, doubling, self-reference |
| 11 | INK | Writing, inscription, the physical act of text |
| 12 | SHADOW | Hidden meaning, the unsaid |
| 13 | FIRE | Destruction, purification, passion |
| 14 | STONE | Permanence, architecture, foundation |

## Graph invariants

- **N**: 51
- **Designed edges at thread-overlap ≥ 4**: ~51 (exactly 17×3 = the intra-triptych triangle edges)
- **Density**: **0.040** — **very sparse** (one of the sparsest in the corpus)
- **Classical MIS**: 17 — exactly one page from each triptych
- **MIS count**: 3^17 ≈ 129 million
- **Rigidity ρ**: **0.000** (essential pages: 0)
- **Graph family**: 17 disjoint triangles (K_3 cliques), zero inter-triangle edges at threshold ≥ 4

## Pipeline-inverse recovery

Using e5-large-instruct with k-NN at various k values:

| k | recall | precision | F1 |
|---|---|---|---|
| **2*** (adaptive) | **1.000** | **1.000** | **1.000** |
| 8 | 1.000 | 0.309 | 0.472 |
| 16 | 1.000 | 0.309 | 0.472 |
| 24 | 1.000 | 0.309 | 0.472 |

**Best F1 = 1.000** at k=2. **The only text in the entire corpus to hit perfect recovery**. At k=2 (matched to the triangle-per-triptych average degree of 2), the pipeline recovers *exactly* the 51 designed edges — 17 triangles × 3 edges each — and nothing else.

**This is the paper's strongest single-text pipeline-inverse result.** It proves that when a constrained text has a clean hidden graph structure, e5-large-instruct can recover it perfectly at the matched k.

## Quantum status (2026-04-11)

Not currently submitted to any EMU / QPU target. At N=51 and density 0.040, the graph is very sparse and the classical MIS = 17 is trivially large — the quantum demonstration would not be informative because the problem is too easy. **Kaléidoscope's role is purely pipeline-recovery and rigidity**, not quantum advantage.

## Why this book and this book only

1. **The cleanest pipeline-inverse result in the paper** (F1=1.000). No other text reaches perfect recovery.
2. **Minimum rigidity (ρ=0)** gives the literary extreme of "everything is fungible" — the hermeneutic opposite of a tight architectonic text like Dante's *Commedia*.
3. **Adaptive-k methodology anchor**: Kaléidoscope shows why the paper's "k matched to average designed degree" rule matters. At k=8 the F1 is 0.472 (half-and-half); at k=2 the F1 jumps to 1.000. No other text makes the k-sensitivity argument this cleanly.
4. **Homage to Bernard Maréchal** ties the paper to Christophe's personal teaching lineage (ZaZiPo, Lille) — a small but real humanities-network credit.
