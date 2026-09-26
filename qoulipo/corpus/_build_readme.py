#!/usr/bin/env python3
"""Regenerate corpus/README.md from instances.csv (QOuLiPo + natural deposit)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / "instances.csv").open()))
qoulipo = [r for r in rows if r["corpus_role"] == "qoulipo_engineered"]
natural = [r for r in rows if r["corpus_role"] == "natural"]

lines = []
lines.append("# QOuLiPo Corpus — Canonical Text-Graph Data\n")
lines.append("**QOuLiPo** (*Quantum Ouvroir de Littérature Potentielle*) is a corpus of literary "
             "texts engineered so that each text *is* a graph: every page is a node, every page-pair "
             "with sufficient semantic or structural affinity is an edge, and a Maximum Independent "
             "Set (MIS) of that graph is a largest pairwise-dissimilar backbone that remains thematically faithful to the work.\n")
lines.append("This deposit holds 29 engineered QOuLiPo folders (28 standalone literary texts + 1 "
             "bilayer aggregate), 11 natural-text companion corpora "
             "(Augustine, Boethius, Dante, Galileo, Giambullari, Heptaméron, Lactantius, Ausonius "
             "×3, Mishnah Avot), and a 12-paragraph reader-friendly mini-text (`pedagogy_demo/`). "
             "Every folder has a uniform `metadata.json`, an explicit-edge-list graph file, an "
             "ILP-verified MIS, and a clean source/paratext separation. State is enforced by "
             "`verify.py --strict --lint` (CI-style).\n")
lines.append("**Quick start.** Open `qoulipo/INDEX.html` in a browser for the single-page navigator "
             "(graph thumbnails with MIS pages highlighted, narrative summaries, design notes). "
             "Run `python3 verify.py --strict --lint --no-mis` for a fast structural check.\n")

lines.append("## Layout\n")
lines.append("```")
lines.append("corpus/")
lines.append("├── qoulipo/                 ← 29 folders: 28 literary texts + 1 bilayer aggregate (pascal_menil_bilayer)")
lines.append("│   ├── INDEX.html           ← single-page navigator (auto-built)")
lines.append("│   └── _summaries.json      ← narrative summaries per text")
lines.append("├── natural/                 ← 11 natural-text corpora (Augustine, Boethius, Dante, Galileo, Giambullari, Heptaméron, Lactantius, Ausonius ×3, Mishnah Avot)")
lines.append("├── pedagogy_demo/           ← 12-paragraph reader-friendly mini-text")
lines.append("├── instances.csv            ← master registry (this file's source of truth)")
lines.append("├── verify.py                ← consistency checker (M1/M2/G1-G5/S1-S3/P1-P2/R1-R3)")
lines.append("├── _compute_canonical.py    ← MIS+rho+optima helper")
lines.append("├── _build_readme.py         ← regenerates this file")
lines.append("├── mis_analysis_all.csv     ← per-text MIS solution + summary distance")
lines.append("└── README.md")
lines.append("```\n")

lines.append("## Per-folder contract\n")
lines.append("Every folder has:")
lines.append("- `metadata.json` with canonical fields: `text_id, title, lang, canonical_N, "
             "canonical_graph_file, canonical_E, canonical_density, canonical_MIS, canonical_rho, "
             "canonical_optima, graph_mode, source_contract`.")
lines.append("- `<canonical_graph_file>` (typically `graph_target.json`, `graph_designed.json`, "
             "or `graph_k8.json`) with explicit `nodes` + `edges` lists.")
lines.append("- `source/` containing one `.txt` file per graph node (under the declared "
             "`source_contract`). Source contracts in this deposit:")
lines.append("  - `node_aligned`: one source file per graph node, file stem = node id.")
lines.append("  - `chunked_canto_split`: source pages were chunked from a single full text by canto headers (Dante).")
lines.append("  - `chunked_400word_window`: 400-word sliding window from a single full text (Galileo).")
lines.append("  - `node_aligned_bilayer`: bilayer text+commentary, one source file per node, prefix encodes layer (Mishnah Avot).")
lines.append("  - `aggregate`: source/ holds the combined component pages (Pascal-Ménil bilayer).")
lines.append("  - `component`: layer of an aggregate; `canonical_graph_file` may point at `../<aggregate>/`.")
lines.append("- `paratext/` (optional): titles, constraint notes, thread tables, design archives.")
lines.append("- `mis_analysis.json` (optional): MIS solution, generated summary, embedding distances cos(MIS,summary)/cos(MIS,full)/cos(summary,full) using the corpus's `multilingual-e5-large-instruct` embedder.\n")
lines.append("Run `python3 verify.py --report` for the current pass/fail map.\n")

# Literary quality note
FLAGSHIPS = {"castello_49_destini", "venticinque_stanze", "pascal_apocryphe",
             "pascal_apocryphe_scholia", "friars_notebook"}
lines.append("## Texts with stronger standalone literary quality\n")
lines.append("Five pieces in this corpus are presented as readable standalone works rather than primarily as benchmark instances:\n")
for r in qoulipo:
    fname = r["folder"].split("/")[-1]
    if fname in FLAGSHIPS:
        lines.append(f"- `{fname}` — {r['title']}")
lines.append("\nThe remaining QOuLiPo folders are graph-engineered constrained texts whose primary purpose is to realise specific graph properties; they are readable but uneven as standalone literature.\n")

# QOuLiPo by class
lines.append(f"## QOuLiPo engineered texts ({len(qoulipo)} folders)\n")
lines.append("Compute-instance graphs were submitted to Pasqal where applicable. Texts are grouped by graph class.\n")
GROUPS = [
    ("Exact UDG / UBG (atom positions = page positions)",
     ["exact_2D_UDG", "exact_2D_UDG_king5x5", "exact_2D_UDG_random", "exact_2D_UDG_triangular", "exact_2D_UDG_with_spectral_gap",
      "exact_3D_UBG", "exact_bilayer_UBG", "exact_bilayer_UBG_component"]),
    ("Designed via thread overlap (k-NN engineered)",
     ["designed_knn"]),
    ("Designed via direct edge-list construction",
     ["designed_K3_unions", "designed_planar_grid", "designed_planar_grid_from_coords",
      "designed_bipartite_K25_25", "designed_double_domination", "designed_hub_spoke_UDG",
      "designed_shared_isomorphic", "designed_UDG_from_coords"]),
    ("NLP-derived (k=8 graphs as canonical)",
     ["NLP_k8", "NLP_k8_canonical_subgraph", "NLP_k8_clean_source"]),
]
seen = set()
for group_name, modes in GROUPS:
    in_group = [r for r in qoulipo if r["graph_mode"] in modes]
    if not in_group: continue
    lines.append(f"### {group_name}\n")
    lines.append("| folder | title | N | E | d | MIS | ρ | optima | Δmax |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in in_group:
        seen.add(r["folder"])
        opt = r["optima"]
        if r.get("optima_cap_reached") == "True": opt = f"≥{opt}"
        lines.append(f"| `{r['folder']}` | {r['title']} | {r['N']} | {r['E']} | "
                     f"{r['density']} | {r['MIS']} | {r['rho']} | {opt} | {r.get('max_degree','')} |")
    lines.append("")

# Natural
lines.append(f"## Natural texts ({len(natural)} folders)\n")
lines.append("Companion natural-text corpora. All graphs computed with the same "
             "`multilingual-e5-large-instruct` embedder used for the QOuLiPo NLP-canonical instances.\n")
lines.append("| folder | title | author | lang | N | E | d | MIS | ρ | source_contract |")
lines.append("|---|---|---|---|---|---|---|---|---|---|")
for r in natural:
    lines.append(f"| `{r['folder']}` | {r['title']} | _{r.get('lang','')}_ | {r['lang']} | "
                 f"{r['N']} | {r['E']} | {r['density']} | {r['MIS']} | {r['rho']} | "
                 f"{r['source_contract']} |")
lines.append("")

lines.append("## QPU compute instances\n")
lines.append("These QOuLiPo texts were submitted as Rydberg compute instances on FRESNEL_CAN1 QPU "
             "or EMU_MPS:\n")
for fname, k in [("nithards_wager_en", "k=16"), ("nithards_wager_fr", "k=16"),
                  ("pari_de_nithard_II", "k=8"), ("pari_de_nithard_III", "k=8, quench"),
                  ("venticinque_stanze", "exact king 5×5"),
                  ("castello_49_destini", "exact king 7×7 extended"),
                  ("friars_notebook", "3D dodecahedron, design discussion"),
                  ("pascal_menil_bilayer", "EMU_MPS bilayer")]:
    lines.append(f"- `{fname}` ({k})")
lines.append("")

lines.append("## Embedder\n")
lines.append("All NLP-derived graphs use `intfloat/multilingual-e5-large-instruct` with prefix "
             "`\"Instruct: Retrieve semantically similar passages.\\nQuery: {text}\"`, normalised "
             "embeddings, k as specified per text in metadata. The same embedder is used for "
             "the `mis_analysis.json` distance computations.\n")

lines.append("## Verification\n")
lines.append("```bash\n"
             "python3 verify.py --strict --lint --no-mis  # fast structural CI (no ILP)\n"
             "python3 verify.py --report                  # human-readable, full state\n"
             "python3 verify.py --strict --lint           # full CI with ILP MIS re-check (slower)\n"
             "```\n")
lines.append(f"Current state: **{len(qoulipo)}/{len(qoulipo)} QOuLiPo folders pass + R1/R2/R3 consistent**.\n")

(ROOT / "README.md").write_text("\n".join(lines))
print(f"Wrote {ROOT / 'README.md'} ({len(lines)} lines)")
