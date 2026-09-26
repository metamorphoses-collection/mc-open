# 02_corpus — master corpus working copy

Mutable working copy of the QOuLiPo corpus.

**For citation, use the Zenodo deposit** (`../04_zenodo/`, DOI 10.5281/zenodo.20074378), not this folder.

## What's here

- **`mis_analysis_all.csv`** — master index. One row per text, with: folder, corpus_kind (qoulipo/natural), title, language, N, MIS size, MIS pages, MIS_words, full_words, summary_words, cosine similarities, MIS page IDs.
- **`instances.csv`** — light index keyed by folder name.
- **Per-text folders** — same schema as the Zenodo deposit (metadata.json, graph_*.json, mis_analysis.json, source/page_NNN.txt, coords_*.json).

## Relationship to the rest of the tree

- **`../05_oulipo_generation/`** — the *generation pipeline* (LLM design + scaffolding). The output of generation lands here.
- **`../04_zenodo/`** — frozen, deposited versions. Public.
- **`../03_quantum_runs/`** — what got submitted to FRESNEL\_CAN1 / EMU\_MPS based on these graphs.
- **`../01_arxiv_paper/`** — paper that cites this corpus.

## Schema (for any per-text folder)

```
<text_folder>/
├── metadata.json              — title, language, N, design tier, ρ, etc.
├── graph_designed.json        — prescribed adjacency (design-led or register-led)
├── graph_target.json          — target adjacency (alias for graph_designed in some cases)
├── graph_k8.json              — k-NN graph from the final prose, k=8
├── mis_analysis.json          — MIS solutions, ρ, # optima
├── coords_2d_*.json           — register coordinates (when register-led)
├── coords_3d_*.json           — register coordinates for bilayer/3D texts
├── source/
│   └── page_NNN.txt           — one page per file, the canonical text
└── _build_metadata.py,        — local generators (some folders)
    _plan.json, _plan.py,
    _verify.py, _verify_report.json
```

## Working policy

- **Don't edit deposited texts** without bumping the Zenodo version (see `../04_zenodo/README_FOLDER.md`).
- **Edits during paper revision** that don't change the canonical corpus are fine here; just don't push a new Zenodo without coordination.
- **Master index regeneration**: when MIS data changes, regenerate `mis_analysis_all.csv` via the scripts in `../05_oulipo_generation/`.
