# QOuLiPo — literary text-graphs for Maximum Independent Set on neutral-atom hardware

Paper: *QOuLiPo* (arXiv, 2026) — source in `paper/`. Companion data: Zenodo
[10.5281/zenodo.20074378](https://doi.org/10.5281/zenodo.20074378) (CC BY 4.0).

- `corpus/` — 28 engineered QOuLiPo texts + 1 bilayer aggregate, 11 natural-text corpora, graph data, MIS analyses,
  `verify.py` consistency checker, `qpu/` run summaries. See `corpus/README.md`.
- `generation/` — the inverse pipeline: writing texts whose graph matches the hardware's native geometry.
- `scripts/` — analysis and plotting scripts (working code, as used for the paper).
