# README — Parity Sweep — Rydberg MIS vs Classical ILP

**File**: `parity_sweep.md`
**Display name**: *parity_sweep (EN)*
**Role**: appendix methodology test

---

## At a glance

- **Language**: EN
- **Constraint family**: parity-sweep engineered graph test
- **Word count**: 113
- **N (pages)**: ?
- **Designed edges**: ?
- **Density**: ?
- **Adaptive k\***: ?
- **Pipeline-inverse best F1 (e5-large-instruct)**: ?

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/parity_sweep.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `parity_sweep.md`
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

appendix methodology test

See `3_MIS/oulipo/texts/README.md` for the full corpus index, and
(where applicable) the hand-written per-book README files for the
main-text entries.
