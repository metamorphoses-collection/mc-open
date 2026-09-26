#!/usr/bin/env python3
"""GPT-5.5 round-2 audit cleanup.

Source/paratext swaps + NLP graph rebuilds + registry regeneration."""
import json
import math
import shutil
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
QOULIPO = ROOT / "qoulipo"

PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
EMBEDDER = "intfloat/multilingual-e5-large-instruct"


def swap_jumeaux(folder):
    """source/001-003 (paratext) ↔ paratext/031-033 (literary)."""
    src = QOULIPO / folder / "source"
    para = QOULIPO / folder / "paratext"
    # Read content
    swaps = []
    for i in range(1, 4):
        s = src / f"page_{i:03d}.txt"
        p = para / f"page_{30 + i:03d}.txt"
        if s.exists() and p.exists():
            content_src = s.read_text(encoding="utf-8")
            content_para = p.read_text(encoding="utf-8")
            # Move source page → paratext (with original paratext name kept for clarity)
            (para / f"frontispiece_{i:03d}.txt").write_text(content_src, encoding="utf-8")
            # Move paratext literary → source (keeping graph node mapping page_01..page_30)
            s.write_text(content_para, encoding="utf-8")
            # Remove original paratext file (replaced by frontispiece naming)
            p.unlink()
            swaps.append(f"page_{i:03d}↔page_{30+i:03d}")
    print(f"  [{folder}] swapped: {', '.join(swaps)}")


def move_partition_dividers():
    """Move 4 divider/form pages to paratext."""
    src = QOULIPO / "partition_du_texte" / "source"
    para = QOULIPO / "partition_du_texte" / "paratext"
    para.mkdir(exist_ok=True)
    moved = []
    for n in (15, 26, 37, 48):
        f = src / f"page_{n:03d}.txt"
        if f.exists():
            shutil.move(str(f), str(para / f.name))
            moved.append(n)
    print(f"  [partition_du_texte] moved divider pages to paratext: {moved}")
    return len(moved)


def split_sonetti_page_016():
    """Move the cryptographic note from page_016.txt to paratext/nota_crittografica.md.
    Keep only the sonnet in page_016.txt."""
    f = QOULIPO / "sonetti_dal_tesseratto" / "source" / "page_016.txt"
    if not f.exists():
        return False
    text = f.read_text(encoding="utf-8")
    # Split on the Nota header
    import re
    m = re.search(r"\n+#+\s*Nota crittografica", text, re.IGNORECASE)
    if not m:
        # Try Italian variants
        m = re.search(r"\n+#+\s*Nota cifrata", text, re.IGNORECASE)
    if not m:
        print(f"  [sonetti] no Nota header found in page_016; nothing to split")
        return False
    sonnet = text[:m.start()].rstrip() + "\n"
    note = text[m.start():].lstrip()
    f.write_text(sonnet, encoding="utf-8")
    para = QOULIPO / "sonetti_dal_tesseratto" / "paratext"
    para.mkdir(exist_ok=True)
    (para / "nota_crittografica.md").write_text(note, encoding="utf-8")
    print(f"  [sonetti] cryptographic note → paratext/nota_crittografica.md ({len(note)} chars)")
    return True


def rebuild_k8_graph(folder, model, target_filename="graph_k8.json"):
    src = QOULIPO / folder / "source"
    files = sorted(src.glob("*.txt"))
    texts = [p.read_text(encoding="utf-8") for p in files]
    nodes = [p.stem for p in files]
    if not texts:
        return None
    print(f"  [{folder}] embedding {len(texts)} pages...", flush=True)
    emb = model.encode([PREFIX + t for t in texts], normalize_embeddings=True,
                       show_progress_bar=False, batch_size=8)
    sim = emb @ emb.T
    k = 8
    edges = set()
    for i in range(len(nodes)):
        order = np.argsort(-sim[i])
        for j in order[1:k + 1]:
            a, b = sorted((int(i), int(j)))
            edges.add((a, b))
    edges_out = [{"source": nodes[a], "target": nodes[b]} for a, b in sorted(edges)]
    N = len(nodes)
    E = len(edges_out)
    d = round(2 * E / (N * (N - 1)), 4) if N > 1 else 0
    out = {
        "N": N, "E": E, "density": d, "k": k, "embedder": EMBEDDER,
        "source": "Rebuilt by _audit2_cleanup.py from cleaned source/.",
        "nodes": nodes, "edges": edges_out,
    }
    (QOULIPO / folder / target_filename).write_text(json.dumps(out, indent=2))
    return N, E, d


def update_metadata_from_graph(folder, graph_file=None):
    """Compute canonical metrics from the canonical graph and update metadata."""
    sys.path.insert(0, str(ROOT))
    from _compute_canonical import canonical_metrics
    base = QOULIPO / folder
    meta_path = base / "metadata.json"
    meta = json.loads(meta_path.read_text())
    g = graph_file or meta["canonical_graph_file"]
    print(f"  [{folder}] computing metrics on {g}...")
    m = canonical_metrics(base / g, opt_cap=500, time_cap_s=180)
    meta.update({
        "canonical_N": m["canonical_N"],
        "canonical_E": m["canonical_E"],
        "canonical_density": m["canonical_density"],
        "canonical_MIS": m["canonical_MIS"],
        "canonical_rho": m["canonical_rho"],
        "canonical_optima": m["canonical_optima"],
        "canonical_optima_cap_reached": m["canonical_optima_cap_reached"],
    })
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"    → N={m['canonical_N']} E={m['canonical_E']} d={m['canonical_density']} "
          f"MIS={m['canonical_MIS']} ρ={m['canonical_rho']} #opt={m['canonical_optima']}")
    return m


def fix_kaleidoscope_optima():
    """Kaleidoscope is exactly 17 disjoint K3 → 3^17 = 129140163 optima."""
    p = QOULIPO / "kaleidoscope" / "metadata.json"
    m = json.loads(p.read_text())
    m["canonical_optima"] = 3 ** 17  # exact
    m["canonical_optima_cap_reached"] = False
    m["canonical_optima_note"] = ("Exact: 3^17 = 129,140,163 (17 disjoint K3 cliques, "
                                   "each contributing 3 independent choices). "
                                   "verify.py's 500-cap enumeration counted up to 500.")
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("  [kaleidoscope] optima → 3^17 (exact)")


def add_castello_triangular_42():
    """Create deposit folder for the QPU 'Castello triangular 42' instance.
    Reproduces the construction from quantum/core/submit_emu_baselines.py."""
    folder = QOULIPO / "castello_triangular_42"
    folder.mkdir(exist_ok=True)
    (folder / "source").mkdir(exist_ok=True)

    # Build coordinates: 6×7 triangular lattice, a=5.0 μm, R_b=10.0 μm
    ROWS, COLS, A, R_B = 6, 7, 5.0, 10.0
    coords = {}
    nodes = []
    for i in range(ROWS):
        for c in range(COLS):
            nid = f"q{i*COLS + c:02d}"
            x = c * A + (i % 2) * 0.5 * A
            y = i * A * math.sqrt(3) / 2
            coords[nid] = [round(x, 4), round(y, 4)]
            nodes.append(nid)
    edges = []
    for a, b in combinations(nodes, 2):
        ca, cb = coords[a], coords[b]
        if math.hypot(ca[0] - cb[0], ca[1] - cb[1]) <= R_B + 1e-9:
            edges.append({"source": a, "target": b})
    N, E = len(nodes), len(edges)
    d = round(2 * E / (N * (N - 1)), 4)

    graph = {
        "N": N, "E": E, "density": d, "R_b_um": R_B, "spacing_um": A,
        "geometry": "6×7 triangular lattice, exact 2D UDG (Cazals hard-zone register)",
        "source": "Generated by _audit2_cleanup.py to reproduce the Phase-B QPU instance "
                  "submitted from submit_emu_baselines.py (gmail account, 2026-04-15, "
                  "batch c194460d, ratio 0.75 valid 1.4%).",
        "nodes": nodes, "coords_2d": coords, "edges": edges,
    }
    (folder / "graph_target.json").write_text(json.dumps(graph, indent=2))

    # Coords sidecar
    (folder / "coords_2d_triangular.json").write_text(json.dumps({
        "node_ids": nodes, "coords_2d": coords, "R_b_um": R_B, "spacing_um": A,
        "rows": ROWS, "cols": COLS,
        "source": "6×7 triangular lattice register for Castello triangular 42 QPU run.",
    }, indent=2))

    # Compute MIS / rho / optima for metadata
    sys.path.insert(0, str(ROOT))
    from _compute_canonical import canonical_metrics
    m = canonical_metrics(folder / "graph_target.json", opt_cap=500, time_cap_s=120)

    # Minimal placeholder source — the Castello tri 42 is a register-only QPU instance,
    # not a literary text. We mark it explicitly as such.
    for i, nid in enumerate(nodes):
        f = folder / "source" / f"{nid}.txt"
        f.write_text(
            f"[REGISTER NODE {nid}]\n\nThis is a register-only node of the Castello "
            f"triangular 42 compute instance (6×7 triangular lattice, R_b=10 μm). "
            f"The Castello triangular 42 instance has no literary content; it is a "
            f"register showcase used in the FRESNEL_CAN1 QPU campaign.\n", encoding="utf-8"
        )

    meta = {
        "text_id": "castello_triangular_42",
        "title": "Castello triangular 42",
        "lang": "—",
        "canonical_N": m["canonical_N"],
        "canonical_graph_file": "graph_target.json",
        "canonical_E": m["canonical_E"],
        "canonical_density": m["canonical_density"],
        "canonical_MIS": m["canonical_MIS"],
        "canonical_rho": m["canonical_rho"],
        "canonical_optima": m["canonical_optima"],
        "canonical_optima_cap_reached": m["canonical_optima_cap_reached"],
        "paper_table_row": "Castello triangular 42",
        "graph_mode": "exact_2D_UDG_triangular",
        "type": "register_showcase",
        "qpu_run": {
            "campaign": "Phase B (gmail account)",
            "date": "2026-04-15",
            "batch_id": "c194460d",
            "ratio": 0.75,
            "valid_pct": 1.4,
            "shots": 1000,
        },
        "designed_property": "6×7 triangular lattice, exact 2D UDG, Cazals hard zone",
        "register_target": "2D, exact",
        "literary_content": "none (register showcase)",
        "project": "QOuLiPo",
        "paper": "Jurczak 2026, arXiv (QOuLiPo)",
    }
    (folder / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(f"  [castello_triangular_42] N={N} E={E} d={d} MIS={m['canonical_MIS']}")


def main():
    print("=== Audit-2 cleanup ===\n")

    print("1. Jumeaux source/paratext swap (EN + FR)")
    swap_jumeaux("jumeaux_en")
    swap_jumeaux("jumeaux_fr")

    print("\n2. Partition divider pages → paratext")
    n_moved = move_partition_dividers()

    print("\n3. Sonetti page_016 cryptographic note split")
    split_sonetti_page_016()

    print("\n4. Kaleidoscope optima fix")
    fix_kaleidoscope_optima()

    print("\n5. Castello triangular 42 deposit folder")
    add_castello_triangular_42()

    # Now load embedder for graph rebuilds
    print("\n6. Rebuilding NLP graphs (partition + sonetti)")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBEDDER)
    rebuild_k8_graph("partition_du_texte", model)
    rebuild_k8_graph("sonetti_dal_tesseratto", model)

    print("\n7. Updating metadata for rebuilt folders")
    update_metadata_from_graph("partition_du_texte", "graph_k8.json")
    update_metadata_from_graph("sonetti_dal_tesseratto", "graph_k8.json")

    print("\nDONE.")


if __name__ == "__main__":
    main()
