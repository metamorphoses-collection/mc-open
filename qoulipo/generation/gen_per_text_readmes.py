#!/usr/bin/env python3
"""
Generate one README_<texname>.md file per text file in 3_MIS/oulipo/texts/.

Each README is a one-pager with:
  - proper name (filename + language + N + k*)
  - source provenance (author, year, constraint family)
  - graph invariants (N, density, designed MIS, F1 from pipeline_inverse_db)
  - role in the paper (main text / appendix / literary artifact)
  - where to find the graph file, coords, quantum runs

Reads pipeline_inverse_db.json and the text file itself for metadata.
Skips files that already have a hand-written README.
"""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
TEXTS = BASE / "texts"

DB_PATH = BASE / "pipeline_inverse_db.json"

# Files with hand-written READMEs — skip these
HAND_WRITTEN = {
    "kaleidoscope.md",
    "nithards_wager_65p_en.md",
    "proces_de_nithard.md",
    "livre_irremplacable_v2.md",
    "oulipo_udg65_text.md",
}

# Text-family metadata. For each text give a 3-line blurb: constraint
# family, language, role. If a file is not here, the generator still
# produces a README from whatever it can read, just with a generic blurb.
FAMILY_META = {
    # 50-page designed-graph corpus
    "carte_du_texte.md": ("planar 5×10 grid", "FR", "appendix"),
    "il_quadrato_dei_re.md": ("2D 4×4 king graph showcase (Italian)", "IT", "showcase companion to SHOWCASE_2d_king_4x4"),
    "incarnate_graph_50_en.md": ("UDG-50 incarnate variant", "EN", "appendix"),
    "incarnate_graph_50p_en.md": ("UDG-50 incarnate variant (parallel)", "EN", "appendix"),
    "jumeaux_en.md": ("mirror/twin constraint", "EN", "appendix"),
    "jumeaux_fr.md": ("mirror/twin constraint (French)", "FR", "appendix — threads inherited from EN parent"),
    "la_vita_nel_cubo.md": ("truncated-cube + 6 thematic long-range edges (literary artifact only, NOT unit-ball realizable)", "IT", "S3 literary-artifact appendix"),
    "le_otto_dimore.md": ("Q_3 bi-layer showcase (Italian)", "IT", "showcase companion"),
    "livre_fractal.md": ("fractal hierarchy", "EN", "appendix"),
    "livre_irremplacable.md": ("dense-cluster v1 (superseded by v2)", "FR", "appendix"),
    "nithards_wager_100_v3_en.md": ("100p v3 Nithard+Pascal", "EN", "appendix"),
    "nithards_wager_100p_en.md": ("100p hard-zone Nithard's Wager", "EN", "appendix"),
    "oulipo_100_hardzone.md": ("100p FR hard-zone", "FR", "appendix"),
    "oulipo_65_hardzone.md": ("65p FR hard-zone (French variant of the main-text EN hardzone)", "FR", "appendix"),
    "oulipo_65_hardzone_en.md": ("65p EN hard-zone", "EN", "appendix — alternate to main-text nithards_wager_65p_en"),
    "oulipo_65_hardzone_en_v2.md": ("65p EN hard-zone revision", "EN", "appendix"),
    "oulipo_65_pages51_57.md": ("65p partial (pages 51–57)", "EN", "appendix fragment"),
    "oulipo_65_pages58_65.md": ("65p partial (pages 58–65)", "EN", "appendix fragment"),
    "oulipo_nithard_pascal.md": ("Nithard+Pascal 50p fused voices", "EN", "appendix"),
    "oulipo_nithard_pascal_v1_original.md": ("Nithard+Pascal 50p v1 original", "EN", "appendix"),
    "oulipo_udg100_text.md": ("100p UDG text", "EN", "appendix (parser missing threads)"),
    "oulipo_udg_50pages.md": ("50p UDG FR", "FR", "appendix"),
    "oulipo_udg_50pages_en.md": ("50p UDG EN", "EN", "appendix"),
    "oulipo_v1b_50pages_fr.md": ("v1b 50p FR", "FR", "appendix early draft"),
    "oulipo_v1b_fr_part1.md": ("v1b FR part 1", "FR", "appendix draft fragment"),
    "oulipo_v1b_fr_part2.md": ("v1b FR part 2", "FR", "appendix draft fragment"),
    "oulipo_v2_100pages.md": ("v2 100p EN", "EN", "appendix"),
    "oulipo_v2_100pages_revised.md": ("v2 100p EN revised", "EN", "appendix"),
    "oulipo_v2_part1.md": ("v2 25p part 1", "EN", "appendix draft fragment"),
    "oulipo_v2_part2.md": ("v2 25p part 2", "EN", "appendix draft fragment"),
    "oulipo_v2_part3.md": ("v2 25p part 3", "EN", "appendix draft fragment"),
    "oulipo_v2_part4.md": ("v2 25p part 4", "EN", "appendix draft fragment"),
    "oulipo_v2b_100pages_fr.md": ("v2b 100p FR (EN-inherited threads)", "FR", "appendix"),
    "oulipo_v2b_100pages_fr_revised.md": ("v2b 100p FR revised (EN-inherited threads)", "FR", "appendix"),
    "oulipo_v2b_fr_part1.md": ("v2b FR part 1", "FR", "appendix draft fragment"),
    "oulipo_v2b_fr_part2.md": ("v2b FR part 2", "FR", "appendix draft fragment"),
    "oulipo_v2br_fr_part1.md": ("v2b revised FR part 1", "FR", "appendix draft fragment"),
    "oulipo_v2br_fr_part2.md": ("v2b revised FR part 2", "FR", "appendix draft fragment"),
    "oulipo_v2r_part1.md": ("v2 revised 25p part 1", "EN", "appendix draft fragment"),
    "oulipo_v2r_part2.md": ("v2 revised 25p part 2", "EN", "appendix draft fragment"),
    "oulipo_v2r_part3.md": ("v2 revised 25p part 3", "EN", "appendix draft fragment"),
    "oulipo_v2r_part4.md": ("v2 revised 25p part 4", "EN", "appendix draft fragment"),
    "parity_sweep.md": ("parity-sweep engineered graph test", "EN", "appendix methodology test"),
    "partition_du_texte.md": ("partitioned text constraint", "FR", "appendix"),
    "piege_du_lecteur.md": ("reader-trap constraint, very sparse", "FR", "appendix"),
    "sonetti_dal_tesseratto.md": ("Q_4 tesseract (literary artifact only, NOT unit-ball realizable — Q_4 requires 4 orthogonal axes)", "IT", "S3 literary-artifact appendix"),
    "topic_clusters.md": ("topic-cluster methodology notes", "EN", "appendix methodology"),
}


def word_count(path):
    try:
        return len(Path(path).read_text(encoding="utf-8", errors="ignore").split())
    except Exception:
        return None


def load_db():
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {}


def get_db_entry(db, text_name):
    for e in db.get("engineered", []):
        if e.get("file") == text_name:
            return e
    return None


def header_from_file(path):
    try:
        content = Path(path).read_text(encoding="utf-8", errors="ignore")
        # First markdown H1 heading = title
        m = re.search(r"^#\s+(.+?)$", content, re.M)
        return m.group(1).strip() if m else None
    except Exception:
        return None


def render_readme(text_name, path, db):
    text_entry = get_db_entry(db, text_name)
    family, lang, role = FAMILY_META.get(text_name,
                                          ("(undocumented family)", "?", "appendix"))
    title = header_from_file(path) or text_name.replace(".md", "").replace("_", " ")
    wc = word_count(path)

    if text_entry:
        N = text_entry["N"]
        density = text_entry["density"]
        designed_edges = text_entry["designed_edges"]
        k_star = text_entry.get("k_star", "?")
        best_f1 = text_entry.get("best_f1", "?")
        display = text_entry.get("display", text_name)
    else:
        N = "?"
        density = "?"
        designed_edges = "?"
        k_star = "?"
        best_f1 = "?"
        display = f"{text_name.replace('.md','')} ({lang})"

    readme = f"""# README — {title}

**File**: `{text_name}`
**Display name**: *{display}*
**Role**: {role}

---

## At a glance

- **Language**: {lang}
- **Constraint family**: {family}
- **Word count**: {wc if wc is not None else "?"}
- **N (pages)**: {N}
- **Designed edges**: {designed_edges}
- **Density**: {density}
- **Adaptive k\\***: {k_star}
- **Pipeline-inverse best F1 (e5-large-instruct)**: {best_f1}

## Where everything lives

- **Text file**: `3_MIS/oulipo/texts/{text_name}`
- **Graph file**: (varies by text — see `pipeline_inverse_db.json` entry)
- **Classical-pipeline recovery result**: `3_MIS/oulipo/pipeline_inverse_db.json`
  entry `{text_name}`
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

{role}

See `3_MIS/oulipo/texts/README.md` for the full corpus index, and
(where applicable) the hand-written per-book README files for the
main-text entries.
"""
    return readme


def main():
    db = load_db()
    written = 0
    skipped = 0
    for text_file in sorted(TEXTS.glob("*.md")):
        name = text_file.name
        if name in HAND_WRITTEN:
            skipped += 1
            continue
        if name == "README.md":
            continue
        if name.endswith("_README.md"):
            continue
        readme_path = TEXTS / f"{text_file.stem}_README.md"
        if readme_path.exists():
            skipped += 1
            continue
        content = render_readme(name, text_file, db)
        readme_path.write_text(content)
        written += 1
        print(f"  ✓ {readme_path.name}")

    print(f"\nWrote {written} new READMEs, skipped {skipped}")


if __name__ == "__main__":
    main()
