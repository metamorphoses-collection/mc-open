# README — Les Jumeaux du Graphe -- Text A (English)

**File**: `jumeaux_en.md`
**Display name**: *jumeaux_en (EN) N=30 k=2*
**Role**: appendix

---

## At a glance

- **Language**: EN
- **Constraint family**: mirror/twin constraint
- **Word count**: 11057
- **N (pages)**: 30
- **Designed edges**: 37
- **Density**: 0.0851
- **Adaptive k\***: 2
- **Pipeline-inverse best F1 (e5-large-instruct)**: 0.487

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/jumeaux_en.md`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `jumeaux_en.md`
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
