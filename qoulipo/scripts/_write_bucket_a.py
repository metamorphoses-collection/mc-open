#!/usr/bin/env python3
"""Write uniform canonical metadata.json for the 6 Bucket A folders.

Preserves existing identity / descriptive fields, adds the required canonical_*
fields by computing from the canonical graph file.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compute_canonical import canonical_metrics

HERE = Path(__file__).resolve().parent
QOULIPO = HERE / "qoulipo"

# (folder, canonical_graph_file, paper_table_row_label, graph_mode)
BUCKET_A = [
    ("nithards_wager_en",   "graph_designed.json", "Nithard's Wager EN",      "designed_knn"),
    ("nithards_wager_fr",   "graph_designed.json", "Le Pari de Nithard (FR)", "designed_knn"),
    ("pari_de_nithard_II",  "graph_designed.json", "Le Pari de Nithard II",   "designed_knn"),
    ("pari_de_nithard_III", "graph_designed.json", "Le Pari de Nithard III",  "designed_knn"),
    ("castello_49_destini", "graph.json",          "Il castello dei quarantanove destini", "exact_2D_UDG"),
    ("friars_notebook",     "graph_designed.json", "The Friar's Notebook",    "exact_3D_UBG"),
]

REQUIRED_FIELDS = [
    "text_id", "title", "lang", "canonical_N", "canonical_graph_file",
    "canonical_E", "canonical_density", "canonical_MIS",
    "canonical_rho", "canonical_optima", "paper_table_row", "graph_mode",
]


def normalize_lang(meta):
    # accept "lang" or "language"; output "lang"
    if "lang" in meta:
        return meta["lang"]
    if "language" in meta:
        v = meta["language"]
        m = {"it": "IT", "en": "EN", "fr": "FR", "la": "LA"}
        return m.get(v.lower(), v.upper()) if isinstance(v, str) else v
    return None


def update_one(folder_name, graph_file, paper_row, mode):
    folder = QOULIPO / folder_name
    meta_path = folder / "metadata.json"
    gpath = folder / graph_file
    if not gpath.exists():
        print(f"  MISSING graph {gpath}")
        return

    existing = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    print(f"  computing canonical metrics for {gpath.name}...")
    m = canonical_metrics(gpath, opt_cap=500, time_cap_s=180)
    if m is None:
        print(f"  ERROR: graph not parseable")
        return

    # Build uniform metadata: required fields first, then any preserved extras
    out = {
        "text_id": existing.get("text_id", folder_name),
        "title": existing.get("title", folder_name),
        "lang": normalize_lang(existing) or "EN",
        "canonical_N": m["canonical_N"],
        "canonical_graph_file": graph_file,
        "canonical_E": m["canonical_E"],
        "canonical_density": m["canonical_density"],
        "canonical_MIS": m["canonical_MIS"],
        "canonical_rho": m["canonical_rho"],
        "canonical_optima": m["canonical_optima"],
        "canonical_optima_cap_reached": m["canonical_optima_cap_reached"],
        "paper_table_row": paper_row,
        "graph_mode": mode,
    }
    # Carry over preserved descriptive fields
    for k in ("subtitle", "author", "author_attribution", "title_en", "date",
              "style", "description", "type", "designed_property",
              "register_target", "project", "paper", "graph_note",
              "source_pages", "graph_pages", "design_v2"):
        if k in existing:
            out[k] = existing[k]

    meta_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ {folder_name}: N={out['canonical_N']} E={out['canonical_E']} "
          f"d={out['canonical_density']} MIS={out['canonical_MIS']} "
          f"ρ={out['canonical_rho']} #opt={out['canonical_optima']}"
          f"{' (cap)' if out['canonical_optima_cap_reached'] else ''}")


def main():
    print("Bucket A metadata write — 6 folders\n")
    for folder, gf, row, mode in BUCKET_A:
        print(f"[{folder}]")
        update_one(folder, gf, row, mode)
        print()


if __name__ == "__main__":
    main()
