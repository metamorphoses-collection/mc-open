# README — Le Pari de Nithard

**File**: `oulipo_v2b_100pages_fr_revised.md`
**Display name**: *oulipo_v2b_100pages_fr_revised (FR) N=100 k=8*
**Role**: appendix

---

## At a glance

- **Language**: FR
- **Constraint family**: v2b 100p FR revised (EN-inherited threads)
- **Word count**: 26852
- **N (pages)**: 100
- **Designed edges**: 398
- **Density**: 0.0804
- **Adaptive k\***: 8
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.411

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/oulipo_v2b_100pages_fr_revised.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `oulipo_v2b_100pages_fr_revised.md`
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

appendix

See `3_MIS/oulipo/texts/README.md` for the full corpus index, and
(where applicable) the hand-written per-book README files for the
main-text entries.
