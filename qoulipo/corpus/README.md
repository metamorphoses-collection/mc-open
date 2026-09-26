# QOuLiPo Corpus — Canonical Text-Graph Data

**QOuLiPo** (*Quantum Ouvroir de Littérature Potentielle*) is a corpus of literary texts engineered so that each text *is* a graph: every page is a node, every page-pair with sufficient semantic or structural affinity is an edge, and a Maximum Independent Set (MIS) of that graph is a largest pairwise-dissimilar backbone that remains thematically faithful to the work.

This deposit holds 29 engineered QOuLiPo folders (28 standalone literary texts + 1 bilayer aggregate), 11 natural-text companion corpora (Augustine, Boethius, Dante, Galileo, Giambullari, Heptaméron, Lactantius, Ausonius ×3, Mishnah Avot), and a 12-paragraph reader-friendly mini-text (`pedagogy_demo/`). Every folder has a uniform `metadata.json`, an explicit-edge-list graph file, an ILP-verified MIS, and a clean source/paratext separation. State is enforced by `verify.py --strict --lint` (CI-style).

**Quick start.** Open `qoulipo/INDEX.html` in a browser for the single-page navigator (graph thumbnails with MIS pages highlighted, narrative summaries, design notes). Run `python3 verify.py --strict --lint --no-mis` for a fast structural check.

## Layout

```
corpus/
├── qoulipo/                 ← 29 folders: 28 literary texts + 1 bilayer aggregate (pascal_menil_bilayer)
│   ├── INDEX.html           ← single-page navigator (auto-built)
│   └── _summaries.json      ← narrative summaries per text
├── natural/                 ← 11 natural-text corpora (Augustine, Boethius, Dante, Galileo, Giambullari, Heptaméron, Lactantius, Ausonius ×3, Mishnah Avot)
├── pedagogy_demo/           ← 12-paragraph reader-friendly mini-text
├── instances.csv            ← master registry (this file's source of truth)
├── verify.py                ← consistency checker (M1/M2/G1-G5/S1-S3/P1-P2/R1-R3)
├── _compute_canonical.py    ← MIS+rho+optima helper
├── _build_readme.py         ← regenerates this file
├── mis_analysis_all.csv     ← per-text MIS solution + summary distance
└── README.md
```

## Per-folder contract

Every folder has:
- `metadata.json` with canonical fields: `text_id, title, lang, canonical_N, canonical_graph_file, canonical_E, canonical_density, canonical_MIS, canonical_rho, canonical_optima, graph_mode, source_contract`.
- `<canonical_graph_file>` (typically `graph_target.json`, `graph_designed.json`, or `graph_k8.json`) with explicit `nodes` + `edges` lists.
- `source/` containing one `.txt` file per graph node (under the declared `source_contract`). Source contracts in this deposit:
  - `node_aligned`: one source file per graph node, file stem = node id.
  - `chunked_canto_split`: source pages were chunked from a single full text by canto headers (Dante).
  - `chunked_400word_window`: 400-word sliding window from a single full text (Galileo).
  - `node_aligned_bilayer`: bilayer text+commentary, one source file per node, prefix encodes layer (Mishnah Avot).
  - `aggregate`: source/ holds the combined component pages (Pascal-Ménil bilayer).
  - `component`: layer of an aggregate; `canonical_graph_file` may point at `../<aggregate>/`.
- `paratext/` (optional): titles, constraint notes, thread tables, design archives.
- `mis_analysis.json` (optional): MIS solution, generated summary, embedding distances cos(MIS,summary)/cos(MIS,full)/cos(summary,full) using the corpus's `multilingual-e5-large-instruct` embedder.

Run `python3 verify.py --report` for the current pass/fail map.

## Texts with stronger standalone literary quality

Five pieces in this corpus are presented as readable standalone works rather than primarily as benchmark instances:

- `castello_49_destini` — Il castello dei quarantanove destini
- `friars_notebook` — The Friar's Notebook
- `pascal_apocryphe` — Les Aventures de Pascal: un roman apocryphe
- `pascal_apocryphe_scholia` — Scholies et remarques sur Les Aventures de Pascal
- `venticinque_stanze` — Le venticinque stanze

The remaining QOuLiPo folders are graph-engineered constrained texts whose primary purpose is to realise specific graph properties; they are readable but uneven as standalone literature.

## QOuLiPo engineered texts (29 folders)

Compute-instance graphs were submitted to Pasqal where applicable. Texts are grouped by graph class.

### Exact UDG / UBG (atom positions = page positions)

| folder | title | N | E | d | MIS | ρ | optima | Δmax |
|---|---|---|---|---|---|---|---|---|
| `qoulipo/castello_49_destini` | Il castello dei quarantanove destini | 49 | 396 | 0.3367 | 9 | 1.0 | 1 | 24 |
| `qoulipo/friars_notebook` | The Friar's Notebook | 20 | 30 | 0.1579 | 8 | 0.0 | 5 | 3 |
| `qoulipo/incarnate_graph` | The Incarnate Graph | 65 | 155 | 0.0745 | 22 | 0.0 | 385 | 7 |
| `qoulipo/pascal_apocryphe` | Les Aventures de Pascal: un roman apocryphe | 40 | 240 | 0.3077 | 6 | 0.0 | ≥500 | 17 |
| `qoulipo/pascal_apocryphe_scholia` | Scholies et remarques sur Les Aventures de Pascal | 40 | 240 | 0.3077 | 6 | 0.0 | ≥500 | 17 |
| `qoulipo/pascal_menil_bilayer` | Les Aventures de Pascal / Scholia de Ménil (bilayer) | 40 | 240 | 0.3077 | 6 | 0.0 | ≥500 | 17 |
| `qoulipo/twenty_five_rooms` | The Twenty-Five Rooms | 25 | 72 | 0.24 | 9 | 1.0 | 1 | 8 |
| `qoulipo/venticinque_stanze` | Le venticinque stanze | 25 | 72 | 0.24 | 9 | 1.0 | 1 | 8 |
| `qoulipo/triangular_hex_91` | Hours of the Day | 91 | 240 | 0.0586 | 31 | 1.0 | 1 | 6 |
| `qoulipo/king_9x9_81` | The Book of Eighty-One Squares | 81 | 272 | 0.084 | 25 | 1.0 | 1 | 8 |
| `qoulipo/ext_king_sqrt5_9x9_81` | Eighty-One Mirrors of a Single Pomegranate | 81 | 622 | 0.192 | 13 | 1.0 | 1 | 20 |
| `qoulipo/kagome_100` | Kagome of Late Summer | 100 | 180 | 0.0364 | 39 | 0.8462 | 8 | 4 |
| `qoulipo/snub_square_100` | The Postman's Songbook | 100 | 220 | 0.0444 | 36 | 0.3333 | 97 | 5 |
| `qoulipo/triangular_hex_37` | Treize sur trente-sept | 37 | 90 | 0.1351 | 13 | 1.0 | 1 | 6 |

### Designed via thread overlap (k-NN engineered)

| folder | title | N | E | d | MIS | ρ | optima | Δmax |
|---|---|---|---|---|---|---|---|---|
| `qoulipo/nithards_wager_en` | Nithard's Wager | 50 | 374 | 0.3053 | 14 | 0.5714 | 6 | 30 |
| `qoulipo/nithards_wager_fr` | Le Pari de Nithard | 50 | 427 | 0.3486 | 10 | 0.4 | 19 | 46 |
| `qoulipo/pari_de_nithard_II` | Le Pari de Nithard II | 65 | 631 | 0.3034 | 8 | 0.25 | 255 | 46 |
| `qoulipo/pari_de_nithard_III` | Le Pari de Nithard III | 100 | 691 | 0.1396 | 26 | 0.9231 | 4 | 36 |

### Designed via direct edge-list construction

| folder | title | N | E | d | MIS | ρ | optima | Δmax |
|---|---|---|---|---|---|---|---|---|
| `qoulipo/carte_du_texte` | The Map of the Text | 50 | 85 | 0.0694 | 25 | 0.0 | 2 | 4 |
| `qoulipo/irreplaceable_book` | The Irreplaceable Book | 50 | 290 | 0.2367 | 17 | 1.0 | 1 | 19 |
| `qoulipo/jumeaux_en` | Les Jumeaux du Graphe (English) | 30 | 38 | 0.0874 | 14 | 0.0 | 21 | 4 |
| `qoulipo/jumeaux_fr` | Les Jumeaux du Graphe (French) | 30 | 38 | 0.0874 | 14 | 0.0 | 21 | 4 |
| `qoulipo/kaleidoscope` | The Kaleidoscope | 51 | 51 | 0.04 | 17 | 0.0 | 129140163 | 2 |
| `qoulipo/livre_fractal` | The Fractal Book | 50 | 102 | 0.0833 | 19 | 0.3158 | 267 | 6 |
| `qoulipo/piege_du_lecteur` | The Reader's Trap | 50 | 72 | 0.0588 | 24 | 0.4167 | ≥500 | 6 |
| `qoulipo/proces_de_nithard` | The Trial of Nithard | 50 | 625 | 0.5102 | 25 | 0.0 | 2 | 25 |

### NLP-derived (k=8 graphs as canonical)

| folder | title | N | E | d | MIS | ρ | optima | Δmax |
|---|---|---|---|---|---|---|---|---|
| `qoulipo/partition_du_texte` | La Partition du Texte | 46 | 244 | 0.2357 | 11 | 0.0909 | 154 | 24 |
| `qoulipo/sonetti_dal_tesseratto` | Sonetti dal Tesseratto | 16 | 79 | 0.6583 | 4 | 1.0 | 1 | 13 |
| `qoulipo/vita_nel_cubo` | La Vita nel Cubo | 23 | 128 | 0.5059 | 7 | 0.5714 | 5 | 21 |

## Natural texts (11 folders)

Companion natural-text corpora. All graphs computed with the same `multilingual-e5-large-instruct` embedder used for the QOuLiPo NLP-canonical instances.

| folder | title | author | lang | N | E | d | MIS | ρ | source_contract |
|---|---|---|---|---|---|---|---|---|---|
| `natural/augustine_conf13` | Confessiones, Book XIII | _LA_ | LA | 38 | 206 | 0.293 | 9 | 0.3333 | node_aligned |
| `natural/ausonius_engineered` | Technopaegnion + Griphus + Cento Nuptialis (constraint poetry) | _LA_ | LA | 10 | 44 | 0.9778 | 2 | 1.0 | node_aligned |
| `natural/ausonius_epigrammata` | Epigrammata | _LA_ | LA | 27 | 163 | 0.4644 | 8 | 0.75 | node_aligned |
| `natural/ausonius_mosella` | Mosella | _LA_ | LA | 8 | 28 | 1.0 | 1 | 0.0 | node_aligned |
| `natural/boethius_consolatio` | De Consolatione Philosophiae | _LA_ | LA | 72 | 372 | 0.1455 | 14 | 0.0 | node_aligned |
| `natural/dante_inferno` | Inferno (Commedia I) | _IT_ | IT | 34 | 185 | 0.3298 | 9 | 0.4444 | chunked_canto_split |
| `natural/galileo_dialogo` | Dialogo sopra i due massimi sistemi del mondo | _IT_ | IT | 65 | 165 | 0.0793 | 23 | 0.3913 | chunked_400word_window |
| `natural/giambullari_inferno` | Del sito, forma, & misure dello Inferno di Dante | _IT_ | IT | 151 | 866 | 0.0765 | 41 | 0.878 | node_aligned_page |
| `natural/heptameron_1559` | L'Heptaméron | _FR_ | FR | 72 | 422 | 0.1651 | 19 | 0.0526 | node_aligned |
| `natural/lactantius_demort` | De mortibus persecutorum | _LA_ | LA | 52 | 308 | 0.2323 | 13 | 0.0 | node_aligned |
| `natural/mishnah_avot` | Mishnah Avot (single-layer canonical) | _HE+IT_ | HE+IT | 34 | 199 | 0.3547 | 9 | 0.3333 | node_aligned_bilayer |

## QPU compute instances

These QOuLiPo texts were submitted as Rydberg compute instances on FRESNEL_CAN1 QPU or EMU_MPS:

- `nithards_wager_en` (k=16)
- `nithards_wager_fr` (k=16)
- `pari_de_nithard_II` (k=8)
- `pari_de_nithard_III` (k=8, quench)
- `venticinque_stanze` (exact king 5×5)
- `castello_49_destini` (exact king 7×7 extended)
- `friars_notebook` (3D dodecahedron, design discussion)
- `pascal_menil_bilayer` (EMU_MPS bilayer)

## Embedder

All NLP-derived graphs use `intfloat/multilingual-e5-large-instruct` with prefix `"Instruct: Retrieve semantically similar passages.\nQuery: {text}"`, normalised embeddings, k as specified per text in metadata. The same embedder is used for the `mis_analysis.json` distance computations.

## Verification

```bash
python3 verify.py --strict --lint --no-mis  # fast structural CI (no ILP)
python3 verify.py --report                  # human-readable, full state
python3 verify.py --strict --lint           # full CI with ILP MIS re-check (slower)
```

Current state: **29/29 QOuLiPo folders pass + R1/R2/R3 consistent**.
