# README — Le Pari de Nithard

**File**: `oulipo_nithard_pascal.md`
**Display name**: *oulipo_nithard_pascal (EN) N=65 k=6*
**Role**: appendix

---

## At a glance

- **Language**: EN
- **Constraint family**: Nithard+Pascal 50p fused voices
- **Word count**: 26900
- **N (pages)**: 65
- **Designed edges**: 183
- **Density**: 0.088
- **Adaptive k\***: 6
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.254

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/oulipo_nithard_pascal.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `oulipo_nithard_pascal.md`
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
