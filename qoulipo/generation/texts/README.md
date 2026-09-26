# QOuLiPo engineered texts — provenance and graph invariants

This directory is the QOuLiPo corpus: natural-language texts written
under explicit graph-theoretic constraints so that a computed
similarity graph has a designed structure (independent set size,
density, bipartition, unit-disk realizability, etc.). The quantum
pipeline uses these texts to test how well a neutral-atom MIS solver
can recover constrained combinatorial structure from real prose.

Every text below is accompanied by its **designed graph** (JSON in
`../graphs/`), its **key invariants**, and a one-paragraph summary of
**how it was generated and what it means**. Results of running the
classical NLP+MIS pipeline against each text are in
`pipeline_inverse_db.json`.

---

## Showcase corpus (verified hardware-ready, 2D / 2L / 3D)

### `il_quadrato_dei_re.md` — 2D flat UDG showcase
- **Language**: Italian
- **Graph**: 4×4 king graph. 16 vertices at unit grid positions,
  edges = king's moves (|Δx| ≤ 1, |Δy| ≤ 1, ≠ (0,0)).
- **Invariants**: N=16, E=42, density=0.350, MIS=4, 3-regular to
  5-regular to 8-regular by vertex (corner/edge/interior), not
  bipartite, not planar, **exact 2D unit-disk graph** at spacing
  s=5.6 µm and blockade R_b=8.0 µm (diagonal s√2=7.92<R_b, king's
  2-step 2s=11.2>R_b).
- **Graph files**: `../graphs/showcase_2d_2L_3d.json` key
  `2D_4x4x1_king`.
- **How generated**: hand-written 16 short chapters (~300 words each),
  one per king square. Each chapter explicitly names its 3-5-8 king
  neighbours and avoids naming non-neighbours. Period allusion: Pedro
  Damiano's *Libro da imparare giuocare a scacchi* (Rome 1512), the
  first printed chess treatise, contemporaneous with Giambullari 1544
  and Pacioli 1509.
- **Meaning**: the most favourable case for a Rydberg MIS solver —
  the graph is exactly embeddable in 2D FRESNEL hardware today. Used
  as the paper's 2D pitch showcase.
- **Pasqal status (2026-04-11)**: noiseless + noisy 3D EMU_MPS =
  ratio 1.000 (both), noisy valid 86.8%. First-ever noisy MIS on an
  exact 2D-UDG engineered text.

### `le_otto_dimore.md` — 2L bi-layer UDG showcase
- **Language**: Italian
- **Graph**: Q_3, the 3-cube. 8 vertices labeled by 3-bit strings,
  12 edges (Hamming distance 1).
- **Invariants**: N=8, E=12, density=0.429, MIS=4 (either parity
  class), 3-regular, bipartite, **NOT 2D-UDG** (simple proof:
  placing 000 with 3 neighbours at 120° forces 011 inside R_b),
  **EXACT 2L unit-ball graph** in a slab of height 7.0 µm with
  square side 7.0 µm.
- **Graph file**: `../graphs/graph_q3_bilayer_showcase.json`.
- **How generated**: 8 short chapters (~250 words each), one per
  vertex. Thematic axes: v₀ = basso/alto, v₁ = terra/cielo, v₂ =
  solitudine/incontro. Period allusion: Ficino, *De triplici vita*
  (Florence 1489).
- **Meaning**: the cleanest possible demonstration that bi-layer
  neutral-atom registers unlock a graph class strictly larger than
  flat 2D. The "non-2D-UDG but 2L-UDG" proof is the shortest version
  of the paper's bi-layer pitch, per Henriet 2026-04-11 roadmap memo.
- **Pasqal status (2026-04-11)**: noiseless + noisy 3D EMU_MPS (with
  the atoms at z ∈ {0, 7.0} µm) = ratio 0.75 (both), noisy valid
  93.8%. First-ever noisy Rydberg MIS on a provably-non-2D-UDG graph.

### `sonetti_dal_tesseratto.md` — literary artefact (no clean quantum embedding)
- **Language**: Italian
- **Graph**: Q_4, the 4-cube tesseract. 16 vertices labeled by 4-bit
  strings, 32 Hamming-1 edges.
- **Invariants**: N=16, E=32, density=0.267, MIS=8 (either parity
  class), 4-regular, bipartite, **NOT 2D-UDG**, **NOT exactly
  realisable as a 3D unit-ball graph** (Q_4 needs 4 orthogonal axes).
- **Graph file**: `../graphs/graph_sonetti_tesseratto.json`.
- **How generated**: 16 Italian Petrarchan sonnets (endecasillabo,
  ABBA ABBA CDC DCD). Each vertex labeled by its 4-bit feature
  tuple: v₀ terra/cielo, v₁ diurno/notturno, v₂ solitudine/incontro,
  v₃ memoria/profezia. The 8 even-parity sonnets form one MIS.
- **Meaning**: **literary artefact only**. There is no exact
  unit-ball 3D register for Q_4 — we verified this empirically (best
  SA combined fidelity ≈ 0.875) and it is consistent with Q_4's
  4-dimensional nature. The book is useful as a constrained-writing
  exercise and as an example of the literary-combinatorial tradition
  (Queneau-Calvino lineage), but **not** as a quantum-hardware target.
  Do not submit to Pasqal as-is.

### `la_vita_nel_cubo.md` — literary artefact (no clean quantum embedding)
- **Language**: Italian
- **Graph**: truncated-cube polyhedron + 6 thematic long-range edges.
  24 vertices, 42 edges.
- **Invariants**: N=24, E=42, density=0.152. The 36 polyhedral edges
  form a 3-regular planar Archimedean solid; the 6 long-range
  "thematic" edges break planarity by design.
- **Graph files**: `../graphs/graph_vita_nel_cubo.json` +
  `../graphs/coords_vita_nel_cubo_truncated.json`.
- **How generated**: 24 prose chapters (~300 words each), one per
  truncated-cube vertex, each naming its 3 polyhedral neighbours and
  (if applicable) its 1 long-range partner. The 6 long-range motifs
  are: water drop (v00↔v23), mirror shards (v01↔v22), unopened
  letter (v02↔v21), incense (v05↔v18), pomegranate (v07↔v16),
  two-clocks (v11↔v12). Narrative frame: the 6-months-post-mortem
  inventory of the Florentine humanist Giacomo di Tommaso's palazzo
  by his students, each room containing a copy of Pacioli's *De
  Divina Proportione* (1509) open on a different page.
- **Meaning**: **literary artefact only**. The 6 long-range edges
  violate the unit-ball property in every dimension we tried. The
  book is in the Perec *La Vie mode d'emploi* tradition of
  room-graph constrained writing and is the longest QOuLiPo prose
  piece to date (7300 words), but **not** a quantum-hardware target.

---

## 50-page corpus (designed-graph thread assignments)

These were all written earlier in the project. Each text has
`#### PAGE n` (or `## Page n`) delimited pages with explicit
`Threads: X, Y, Z, ...` annotations; the designed graph is built by
thread-overlap (≥4 threads shared → edge). See
`finetune_embedder.py` for the contrastive-fine-tune recipe.

| text | lang | N | density | best recovery F1 | MIS family |
|---|---|---|---|---|---|
| `kaleidoscope.md` | EN | 51 | 0.040 | **1.000** (k=2) | K_3-triptychs, ρ=0 |
| `livre_irremplacable.md` | FR | 50 | 0.234 | 0.627 (k=11) | dense clusters |
| `livre_irremplacable_v2.md` | FR | 50 | 0.234 | 0.675 (k=11) | v2 rewrite |
| `livre_fractal.md` | EN | 50 | 0.082 | 0.282 (k=4) | fractal hierarchy |
| `piege_du_lecteur.md` | FR | 50 | 0.025 | 0.396 (k=2) | trap-the-reader |
| **`proces_de_nithard.md`** | FR | 50 | 0.030 | **0.732** with fine-tuned | bipartite (prosecution/defense) |
| `partition_du_texte.md` | FR | 50 | 0.086 | 0.643 (k=4) | partitioned |
| `carte_du_texte.md` | FR | 50 | — | — (parser TBD) | 5×10 planar grid |
| `oulipo_nithard_pascal_v1_original.md` | EN | 50 | 0.084 | 0.259 | early draft |
| `incarnate_graph_50_en.md` | EN | 50 | 0.167 | 0.646 | incarnate UDG |
| `incarnate_graph_50p_en.md` | EN | 50 | 0.167 | 0.641 | variant |
| `oulipo_udg_50pages.md` | FR | 50 | 0.167 | 0.629 | UDG 50 FR |
| `oulipo_udg_50pages_en.md` | EN | 50 | 0.167 | 0.646 | UDG 50 EN |

**Proc̀es de Nithard note**: standard e5-instruct gives F1=0.093
(failure mode — bipartite constraint too subtle for semantic
similarity alone). Our fine-tuned `e5-large-oulipo` model, trained
contrastively on thread-overlap pairs across the engineered corpus,
lifts this to **F1=0.732** at thread-overlap threshold ≥ 3. This is
documented in `proces_repair_results.json`.

---

## 65-page hard-zone corpus (Cazals hard-zone MIS targets)

These texts are designed to sit in the Cazals-Nguyen hard-zone of MIS
difficulty: N ≈ 65, density ≈ 0.13, where the classical ILP MIS
solver becomes slow and where quantum advantage is plausible. Each
page activates 5 of 10 thematic threads; the overlap-≥4 rule gives
the designed adjacency.

| text | lang | N | density | best recovery F1 |
|---|---|---|---|---|
| **`oulipo_65_hardzone_en.md`** | EN | 65 | 0.133 | **0.771** (k=9) |
| **`nithards_wager_65p_en.md`** | EN | 65 | 0.133 | **0.764** (k=9) |
| `oulipo_65_hardzone.md` | FR | 65 | 0.133 | 0.747 (k=9) |
| `oulipo_udg65_text.md` | EN | 65 | 0.202 | 0.746 (k=13) |
| `oulipo_65_hardzone_en_v2.md` | EN | 65 | 0.133 | 0.727 (k=9) |
| `oulipo_nithard_pascal.md` | EN | 65 | 0.088 | 0.254 (k=6) |

**These are the paper's headline engineered targets**: the pipeline
recovers ~75% of the designed edges at the matched k, without
fine-tuning, on a fully natural-language text in the Cazals hard
zone. This is the strongest single argument that constrained
writing really does embed combinatorial structure into semantic
space in a way that modern sentence-transformer embedders can see.

---

## 100-page corpus

| text | lang | N | density | best recovery F1 |
|---|---|---|---|---|
| `oulipo_100_hardzone.md` | FR | 100 | 0.188 | 0.547 |
| `nithards_wager_100p_en.md` | EN | 100 | 0.099 | 0.493 |
| `oulipo_v2_100pages.md` | EN | 100 | 0.080 | (no edges at thr≥4) |
| `oulipo_v2_100pages_revised.md` | EN | 100 | 0.080 | 0.340 |
| `oulipo_v2b_100pages_fr_revised.md` | FR | 100 | 0.080 | 0.411 (EN-inherited) |

At N=100 the pipeline recovery F1 drops noticeably compared to N=65
(~0.5 vs ~0.75). Open question for future work: is this a bottleneck
of the 1024-dim E5 embedder, or an artifact of the thread-per-page
density at N=100?

---

## Smaller / misc

| text | lang | N | density | best F1 |
|---|---|---|---|---|
| `jumeaux_en.md` | EN | 30 | 0.085 | 0.487 (k=2) |
| `jumeaux_fr.md` | FR | 30 | 0.085 | 0.487 (EN-inherited) |

---

## Methodology notes

**Embedder**: all recovery results reported in this README are from
`intfloat/multilingual-e5-large-instruct`
(feedback_always_e5_instruct.md). The fine-tuned
`e5-large-oulipo` (contrastively trained on thread-overlap pairs
from this corpus) is used only for Procès de Nithard and similar
bipartite-constraint texts, where it gives a ~8× lift over plain
instruct.

**Adaptive k**: for each text we compute k* = round(2·|E|/N) (the
average designed degree) and report best F1 across k ∈
{8, 16, 24, k*}. For very sparse designed graphs (d<0.05) the
canonical k=8/16/24 values are too large; k=2 or k=3 gives the
right recovery regime.

**Designed adjacency rule**: two pages share an edge iff their
thread sets overlap by ≥ 4 elements. This threshold was set by
`finetune_embedder.py` during the contrastive training phase and is
used consistently across the corpus.

**Graph recovery metric**: F1 score between the recovered k-NN
graph and the designed adjacency, computed on the upper triangle of
the |N|×|N| pair matrix.

---

## Database

The full recovery results are in
`pipeline_inverse_db.json` (top-level JSON with `engineered` and
`natural` sections). The Procès de Nithard repair run is in
`proces_repair_results.json`. The natural-text k-NN reproducibility
results are in `natural_recovery_results.json`.
