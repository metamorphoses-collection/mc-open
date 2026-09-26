# README — Le Livre Irremplaçable

**File**: `livre_irremplacable.md`
**Display name**: *livre_irremplacable (FR) N=50 k=11*
**Role**: appendix

---

## At a glance

- **Language**: FR
- **Constraint family**: dense-cluster v1 (superseded by v2)
- **Word count**: 17402
- **N (pages)**: 50
- **Designed edges**: 287
- **Density**: 0.2343
- **Adaptive k\***: 11
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.627

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/livre_irremplacable.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `livre_irremplacable.md`
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
