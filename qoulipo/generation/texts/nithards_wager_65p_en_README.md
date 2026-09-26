# *Nithard's Wager — Hard-Zone Edition (65 pages)*

**Proper name (main text)**: *Nithard's Wager Hard-Zone (EN) N=65 k=9*

**Role in the paper**: **the Cazals hard-zone headline**. At F1 = 0.764 via plain e5-large-instruct (no fine-tuning), it is the single strongest engineered-text result in the paper and anchors the §QOuLiPo and §density-law arguments. Sits at the Cazals-Nguyen hardness landscape's hard zone (N ≈ 65, d ≈ 0.133) — where classical MIS ILP becomes slow and where quantum advantage is plausible.

---

## Text

- **Author**: (engineered by the project)
- **Language**: English
- **Page count**: 65
- **Word count**: ~21,400
- **File**: `3_MIS/oulipo/texts/nithards_wager_65p_en.md`
- **Narrative**: three voices interweave — **Nithard** the Carolingian chronicler, **Pascal** the mathematician, and the **Professor** (the *Porteur de Maliettes*). Each page activates exactly 5 of 10 thematic threads, following a combinatorial design that places the text in the hard zone of the Cazals landscape.

## Historical hook

**Nithard** (~795–844) was the grandson of Charlemagne, cousin and biographer of Charles the Bald. His *Historiae* is one of the four principal sources for the **Oaths of Strasbourg** (February 842) — the oldest surviving document in Old French and Old High German, sworn by Louis the German and Charles the Bald against their brother Lothair. The wager of the title is the historiographer's wager: whether the written chronicle can be trusted against the living memory of participants.

The **Pascal** voice is Blaise Pascal, the mathematician of the wager (the famous *Pensées* argument). The **Professor** is a teacher-figure who connects the chronicle to the mathematics.

## Constraint (hard-zone by design)

**10 thematic threads** (WAGER, CHRONICLE, CONSPIRACY, TONGUE, NUMBER, FAITH, SWORD, PARCHMENT, MALIETTE, GAME) and **5 threads per page**. This gives average designed degree ≈ 9, landing the designed graph's density at exactly **0.133** — the center of the Cazals hard zone.

The threshold is **thread-overlap ≥ 4**: two pages are connected iff they share at least 4 of their 5 threads.

## Graph invariants

- **N**: 65
- **Designed edges**: ~283 (at overlap ≥ 4)
- **Density**: **0.133** — Cazals hard-zone center
- **Average designed degree**: ~9 (hence the **k*=9** adaptive match)
- **Classical MIS**: TBD (ILP tractable, slow)
- **Graph family**: dense thematic-cluster structure, small number of clique communities

## Pipeline-inverse recovery

Using e5-large-instruct:

| k | recall | precision | F1 |
|---|---|---|---|
| 8 | 0.764 | - | **0.764** |
| **9*** (adaptive) | — | — | **~0.75–0.77** (approximately) |
| 16 | 0.598 | — | — |
| 24 | 0.453 | — | — |

**Best F1 = 0.764** at k=8. **The highest engineered-text recovery in the non-fine-tuned embedder regime.** This demonstrates that when a 65-page constrained text is written with 10 threads × 5 threads-per-page in the hard zone, e5-large-instruct recovers about 3/4 of the designed edges directly — **without fine-tuning**.

## Why this book and this book only

1. **The engineered-text F1 ceiling without fine-tuning** (0.764). Above it only Kaléidoscope (1.000 at k=2 on a much simpler designed graph). Nithard's Wager is the ceiling for **non-trivial** engineered texts.
2. **Cazals hard-zone anchor**: at (N=65, d=0.133) it is the closest point in the corpus to the "quantum advantage appears here" region of the Cazals MIS hardness landscape.
3. **Density-law anchor**: d ≈ k/N is satisfied exactly here (9/65 ≈ 0.138). This is a textbook example of the density law that the paper uses to explain why natural texts at human length are classically trivial.
4. **Historical depth**: Nithard 842 + Pascal 1662 + the Porteur de Maliettes — three centuries meet in one text, which matches the paper's interdisciplinary aesthetic.
5. **Linguistic purity**: English, one clean language throughout, no translation noise.

## Not to be confused with

- **oulipo_65_hardzone (FR)** — French version of the same constraint, F1 = 0.747
- **oulipo_65_hardzone_en_v2** — a later English rewrite, F1 = 0.727
- **nithards_wager_100p_en** — N=100 extension, F1 = 0.493 (the F1 ceiling drops at larger N)
- **nithards_wager_100_v3_en** — N=100 v3 with a different thread assignment; in appendix only
