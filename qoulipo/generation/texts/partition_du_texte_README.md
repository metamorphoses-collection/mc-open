# README — La Partition du Texte

**File**: `partition_du_texte.md`
**Display name**: *partition_du_texte (FR) N=50 k=4*
**Role**: appendix

---

## At a glance

- **Language**: FR
- **Constraint family**: partitioned text constraint
- **Word count**: 15285
- **N (pages)**: 50
- **Designed edges**: 106
- **Density**: 0.0865
- **Adaptive k\***: 4
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.643

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/partition_du_texte.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `partition_du_texte.md`
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
