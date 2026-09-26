# README — Il quadrato dei re

**File**: `il_quadrato_dei_re.md`
**Display name**: *il_quadrato_dei_re (IT)*
**Role**: showcase companion to SHOWCASE_2d_king_4x4

---

## At a glance

- **Language**: IT
- **Constraint family**: 2D 4×4 king graph showcase (Italian)
- **Word count**: 1206
- **N (pages)**: ?
- **Designed edges**: ?
- **Density**: ?
- **Adaptive k\***: ?
- **Pipeline-inverse best F1 (e5-large-instruct)**: ?

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/il_quadrato_dei_re.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `il_quadrato_dei_re.md`
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

showcase companion to SHOWCASE_2d_king_4x4

See `3_MIS/oulipo/texts/README.md` for the full corpus index, and
(where applicable) the hand-written per-book README files for the
main-text entries.
