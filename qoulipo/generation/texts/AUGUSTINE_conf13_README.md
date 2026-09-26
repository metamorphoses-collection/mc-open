# Augustine — *Confessiones Liber XIII*

**Proper name (main text)**: *Augustine, Confessions Book XIII (LA) N=22 k=8*

**Role in the paper**: **dense natural-text anchor**, the 2D/2L/3D ladder's densest endpoint (d=0.411). Also the first target in the 6-cell EMU table — Augustine 2D N=14 prefix is the **natural-text 2D cell** of the 6-cell 2D / 2L / 3D × natural / engineered grid.

---

## Source text

- **Author**: Aurelius Augustinus (354–430 AD)
- **Work**: *Confessiones*, specifically Book XIII (the final book, on Genesis 1 and the seven days of creation)
- **Language**: Classical / Late-antique Latin
- **Edition used**: public-domain Latin edition, chapter-by-chapter split
- **Chapter count**: 22 (Book XIII is divided into 22 chapters in the standard division)

## How the graph was built

Per `3_MIS/classical/core/build_topic_graph.py`, with paragraph-to-chapter mapping:

1. Text split into 22 chapter files `3_MIS/classical/reference_texts/latin_texts/augustine_conf13_chapters/chapter_01.txt..chapter_22.txt`
2. Each chapter embedded with `intfloat/multilingual-e5-large` (earlier runs) or `intfloat/multilingual-e5-large-instruct` (for this paper's figures)
3. k-NN graph with k=8, cosine-similarity threshold 0.78
4. Output: `3_MIS/classical/graphs/augustine/graph_Augustine_Conf13.json`

## Invariants

- **N**: 22
- **E**: 95
- **Density**: 0.411 — **the densest natural text in the corpus**
- **Node labels**: `p0, p1, p2, ..., p21` (alphabetical-sort order; the graph file stores them in that order)
- **Classical MIS (ILP)**: 6
- **Backbone ratio MIS/N**: 0.273
- **Rigidity ρ** (fraction of MIS-essential nodes): 0.333 (intermediate — architectonic but with fungibility)

## Pipeline-inverse recovery

Using e5-large-instruct with the canonical graph-ID mapping (see `natural_recovery.py`):

| k | recall | precision | F1 |
|---|---|---|---|
| 8 | 0.547 | 0.546 | 0.546 |
| 16 | higher recall, lower precision | | |

**Best F1 = 0.546**. Moderate recovery — the graph's density combined with a small N makes k=8 a reasonable sampling, but the 22-chapter granularity means the thematic signal per chapter is strong enough to be recoverable without being perfect.

See `3_MIS/oulipo/natural_recovery_results.json` for the full F1 sweep.

## Quantum status (2026-04-11)

- **3D SA embedding**: `3_MIS/quantum/embeddings/augustine_13_coords_3d_best.json` — gradient-MDS variant with combined fidelity **0.895** (recall 0.895, precision 0.897).
- **3D recall=1.0 embedding** (`augustine_13_coords_3d_recall1.json`) exists but at the cost of non-edge precision 0.66 — all target edges blockade but 34% of non-edges also blockade.
- **Noisy EMU_MPS 3D runs** (N=14 prefix, 5×200 shots Constantin noise): 100% noiseless valid, 85.3% noisy valid, best IS 3 (matches classical MIS for N=14 subgraph), ratio 1.0. **From 20260410_3d_noisy_constantin**.
- **2D SA embedding at N=14**: being built in `augustine_13_coords_2d_N14.json` as part of the 6-cell 2D/2L/3D comparison table (the **2D natural** cell).

## Why this book and this book only

1. **Canonical**: the *Confessions* are the most recognized Latin text in the natural-language-processing + humanities overlap, and using them makes the paper's claims broadly intelligible.
2. **Dense**: at d=0.411 it sits at the upper end of natural-text density and is the hardest natural-text case for a UDG embedding. This is where the 2D cap bites hardest and where the 2D→2L→3D staircase shows the largest lift.
3. **Small enough for clean quantum runs**: at N=22 the full graph is tractable in 3D EMU_MPS; at N=14 prefix it fits comfortably in noisy EMU_MPS with Constantin calibration.
4. **The 3D SA converges**: augustine_13_coords_3d_best at 0.895 combined fidelity is our best natural-text 3D gradient embedding.

## Not to be confused with

- **augustine_conf13full** (N=38) — a separate graph covering Books 7–13 of the Confessions, different node count, different density, used as a secondary natural-text entry in the pipeline-inverse database.
