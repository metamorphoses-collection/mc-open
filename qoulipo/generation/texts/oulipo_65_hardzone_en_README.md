# README — Le Pari de Nithard — 65-Page Hard-Zone Edition (English)

**File**: `oulipo_65_hardzone_en.md`
**Display name**: *oulipo_65_hardzone_en (EN) N=65 k=9*
**Role**: appendix — alternate to main-text nithards_wager_65p_en

---

## At a glance

- **Language**: EN
- **Constraint family**: 65p EN hard-zone
- **Word count**: 28056
- **N (pages)**: 65
- **Designed edges**: 277
- **Density**: 0.1332
- **Adaptive k\***: 9
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.771

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/oulipo_65_hardzone_en.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `oulipo_65_hardzone_en.md`
- **Master index**: `3_MIS/oulipo/texts/README.md`

## Provenance

Engineered text in the QOuLiPo corpus, written by the project under a
graph-theoretic constraint. Threads and designed adjacency parsed per
the finetune_embedder.py recipe (thread-overlap ≥ 4 → designed edge).

Per the project convention, all engineered texts use the instruct
variant of multilingual-e5-large for pipeline-inverse recovery,
unless the designed graph has bipartite or sparse structure that
requires the contrastively fine-tuned `e5-large-oulipo` model (see
`feedback_always_e5_instruct.md` and the Procès de Nithard case).

## Role in the paper

appendix — alternate to main-text nithards_wager_65p_en

See `3_MIS/oulipo/texts/README.md` for the full corpus index, and
(where applicable) the hand-written per-book README files for the
main-text entries.
