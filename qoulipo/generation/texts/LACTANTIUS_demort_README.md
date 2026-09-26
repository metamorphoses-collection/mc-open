# Lactantius — *De mortibus persecutorum*

**Proper name (main text)**: *Lactantius, De mortibus persecutorum (LA) N=52 k=8*

**Role in the paper**: **medium-density natural-text anchor**, the middle of the 2D→2L→3D ladder (d=0.232). Holds the **2L natural cell** of the 6-cell EMU table (Lactantius 2L N=24 prefix) and the **3D natural cell** (Lactantius 3D N=18 prefix). Most importantly, the site of the paper's **noise-assisted ratio improvement** phenomenon — the noisy 3D EMU run at N=18 improves over the noiseless run (ratio 0.667 → 0.889, +0.222).

---

## Source text

- **Author**: Lucius Caecilius Firmianus Lactantius (~250–325 AD)
- **Work**: *De mortibus persecutorum* ("On the Deaths of the Persecutors"), a Christian Latin prose polemic chronicling the fates of Roman emperors who persecuted the early Church
- **Language**: Late-antique Classical Latin
- **Structure**: 52 chapters (varying in length from ~100 to ~600 words)
- **Edition used**: public-domain Latin edition, chapter-by-chapter split

## How the graph was built

Via `build_topic_graph.py`:

1. Text split into 52 chapter files `3_MIS/classical/reference_texts/latin_texts/lactantius_demort_chapters/chapter_01.txt..chapter_52.txt`
2. Each chapter embedded with `intfloat/multilingual-e5-large-instruct` (current paper standard)
3. k-NN graph at **k=8** → `graph_lactantius_demort_k8.json` (main-text variant)
4. k-NN graph at **k=16** → `graph_Lactantius_DeMort_k16.json` (appendix variant)

## Invariants (k=8 version — main text)

- **N**: 52
- **E**: 308
- **Density**: 0.232 — **medium density, the middle of the natural-text ladder**
- **Node labels**: `chapter_01, chapter_02, ..., chapter_52` (one-to-one with source filenames)
- **Classical MIS (ILP)**: 20 (for the full N=52 graph)
- **Rigidity ρ**: 0.556 (intermediate — partial architectonic)

## Pipeline-inverse recovery

Using e5-large-instruct and canonical `chapter_NN` IDs:

| k | recall | precision | F1 |
|---|---|---|---|
| 8 | 0.789 | 0.810 | **0.799** |
| 16 | 0.981 | 0.530 | 0.688 |

**Best F1 = 0.799** at k=8 — **the second-highest natural-text recovery in the whole database**, behind only `augustine_conf13full` (0.885) and ahead of Giambullari (0.247–0.528). Precision 0.81 is excellent: e5-instruct introduces very few spurious edges.

## Quantum status (2026-04-11)

### Phase 1 3D noisy sweep (Lactantius N=18 prefix, from `20260411_noisy_3d_small_set`)

- **Noiseless EMU_MPS**: 100% valid, best IS = 6, ratio = **0.667**, ⟨w⟩ = 5.82
- **Noisy EMU_MPS** (5 × 200 shots Constantin Apr-10): 88.9% valid, best IS = **8**, ratio = **0.889**, ⟨w⟩ = 5.40
- **Delta**: **+0.222 ratio noise-assisted**. The noisy run finds a larger independent set than the noiseless run.
- **Interpretation**: thermal noise in the adiabatic sweep explores the solution landscape more widely than the noiseless adiabat, sampling valid independent sets of higher cardinality.

### Phase 2b 2L SA embedding (to be submitted)

- **2L coords**: `lactantius_coords_2L_N24.json` (under construction)
- Target: N=24 prefix, 2L register (z ∈ {0, 6.4 µm})
- Classification: **2L-natural cell of the 6-cell table**
- Expected: intermediate fidelity between the 2D cap and the full 3D ceiling

## Why this book and this book only

1. **Latin + public-domain**: anyone can reproduce the results from the public Latin text.
2. **Medium density**: d=0.232 sits between the dense Augustine endpoint (0.411) and the sparse Giambullari endpoint (0.104), so the ladder's middle-density measurement happens on a single consistent text.
3. **Bipartite structure** (persecution cycle / deliverance cycle) gives clean thematic clusters that k-NN with e5-instruct recovers at F1 = 0.80, making it the most interpretable "MIS as literary-structural tool" case in the paper.
4. **Best noise-assisted improvement**: the +0.222 ratio lift at N=18 is the paper's strongest quantum-signal data point on a natural text.
5. **Tractable at every register tier**: N=52 fits in classical MIS ILP, N=24 fits in 2L noisy EMU_MPS, N=18 fits in 3D noisy EMU_MPS — the same text at three register classes, three different N, is the perfect ladder anchor.

## Not to be confused with

- **lactantius_demort k=16** (same N=52, d=0.447) — the denser variant at k=16. Used in §7 for the 2D→2L→3D ladder v3 comparison; in the appendix for the F1 recovery sweep.
