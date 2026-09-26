#!/usr/bin/env python3
"""Write canonical metadata for Group 1 folders (good-fit non-QPU texts).

Plan:
  livre_fractal    — reconstruct from coords_designed.json at R_b=8   → graph_target.json
  kaleidoscope     — reconstruct from coords_designed.json at R_b=8   → graph_target.json (E=48, drift flag)
  carte_du_texte   — reconstruct from coords_designed.json at R_b=10  → graph_target.json
  incarnate_graph  — repackage coords_2d_udg.json (already has edges) → graph_target.json
  vita_nel_cubo    — canonical = graph_k8.json (numerics match paper)
  sonetti_dal_tesseratto — canonical = graph_k8.json (numerics match paper)

piege_du_lecteur was already done in an earlier pass.
"""
import json
import math
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compute_canonical import canonical_metrics

HERE = Path(__file__).resolve().parent
QOULIPO = HERE / "qoulipo"


def reconstruct_from_coords(coords_dict, R_b):
    nodes = list(coords_dict.keys())
    pts = [coords_dict[k] for k in nodes]
    edges = []
    for i, j in combinations(range(len(nodes)), 2):
        if math.dist(pts[i], pts[j]) <= R_b + 1e-9:
            edges.append({"source": nodes[i], "target": nodes[j]})
    return nodes, edges


def write_reconstructed_graph(folder, coords_file, R_b, geometry_label, paper_target):
    base = QOULIPO / folder
    coords = json.loads((base / coords_file).read_text())
    # strip any non-coord top-level keys
    coords = {k: v for k, v in coords.items()
              if isinstance(v, (list, tuple)) and len(v) in (2, 3)}
    nodes, edges = reconstruct_from_coords(coords, R_b)
    N = len(nodes)
    E = len(edges)
    d = round(2 * E / (N * (N - 1)), 4) if N > 1 else 0
    graph = {
        "N": N,
        "E": E,
        "density": d,
        "R_b_um": R_b,
        "geometry": geometry_label,
        "source": f"Reconstructed from {coords_file} at R_b={R_b} um (deterministic UDG; same as compute instance would be).",
        "paper_target": paper_target,
        "nodes": nodes,
        "coords_2d": coords,
        "edges": edges,
    }
    out = base / "graph_target.json"
    out.write_text(json.dumps(graph, indent=2) + "\n")
    return out


def write_metadata(folder, canonical_graph, paper_row, mode, extra=None, drift_note=None):
    base = QOULIPO / folder
    existing = json.loads((base / "metadata.json").read_text()) if (base / "metadata.json").exists() else {}
    print(f"  computing metrics for {canonical_graph}...")
    m = canonical_metrics(base / canonical_graph, opt_cap=500, time_cap_s=180)
    if m is None:
        print(f"  ERROR: graph not parseable")
        return None

    out = {
        "text_id": existing.get("text_id", folder),
        "title": existing.get("title", folder),
        "lang": existing.get("lang", existing.get("language", "EN")),
        "canonical_N": m["canonical_N"],
        "canonical_graph_file": canonical_graph,
        "canonical_E": m["canonical_E"],
        "canonical_density": m["canonical_density"],
        "canonical_MIS": m["canonical_MIS"],
        "canonical_rho": m["canonical_rho"],
        "canonical_optima": m["canonical_optima"],
        "canonical_optima_cap_reached": m["canonical_optima_cap_reached"],
        "paper_table_row": paper_row,
        "graph_mode": mode,
    }
    for k in ("subtitle", "author", "title_en", "description", "type",
              "designed_property", "register_target", "project", "paper",
              "graph_note", "source_pages", "graph_pages"):
        if k in existing:
            out[k] = existing[k]
    if extra:
        out.update(extra)
    if drift_note:
        out["paper_table5_drift_note"] = drift_note
    (base / "metadata.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ {folder}: N={m['canonical_N']} E={m['canonical_E']} d={m['canonical_density']} "
          f"MIS={m['canonical_MIS']} ρ={m['canonical_rho']} #opt={m['canonical_optima']}"
          f"{' (cap)' if m['canonical_optima_cap_reached'] else ''}")
    return m


def repackage_incarnate_graph():
    """coords_2d_udg.json already contains points + edges; just re-emit in standard form."""
    base = QOULIPO / "incarnate_graph"
    src = json.loads((base / "coords_2d_udg.json").read_text())
    pts = src["points"]
    edges_raw = src["edges"]
    nodes = [str(p["id"]) for p in pts]
    coords = {str(p["id"]): [p["x"], p["y"]] for p in pts}
    name_to_idx = {n: i for i, n in enumerate(nodes)}
    edges = []
    for e in edges_raw:
        if isinstance(e, dict):
            a, b = str(e.get("source", e.get(0))), str(e.get("target", e.get(1)))
        else:
            a, b = str(e[0]), str(e[1])
        edges.append({"source": a, "target": b})
    out = {
        "N": len(nodes),
        "E": len(edges),
        "density": src.get("density"),
        "R_b_um": src.get("blockade_um"),
        "geometry": "UDG by construction (random uniform placement, blockade R_b=8 um)",
        "seed": src.get("seed"),
        "source": "Repackaged from coords_2d_udg.json (the original placement file is the canonical compute instance).",
        "nodes": nodes,
        "coords_2d": coords,
        "edges": edges,
    }
    (base / "graph_target.json").write_text(json.dumps(out, indent=2) + "\n")
    return out["N"], out["E"]


def main():
    print("Group 1 metadata write — 6 folders\n")

    # 1. livre_fractal — R_b=8 reconstruction matches paper (E=102, d=0.083)
    print("[livre_fractal]")
    write_reconstructed_graph("livre_fractal", "coords_designed.json", 8.0,
                              "Sierpinski-inspired self-similar communities",
                              {"N": 50, "d": 0.083, "MIS": 19, "rho": 0.316})
    write_metadata("livre_fractal", "graph_target.json",
                   "The Fractal Book", "designed_UDG_from_coords")
    print()

    # 2. kaleidoscope — R_b=8 → E=48 (paper says 51, drift)
    print("[kaleidoscope]")
    write_reconstructed_graph("kaleidoscope", "coords_designed.json", 8.0,
                              "17 disjoint K3 cliques (target: E=51; deposit coords realise E=48, three edges short)",
                              {"N": 51, "d": 0.040, "MIS": 17, "rho": 0.0})
    write_metadata("kaleidoscope", "graph_target.json",
                   "The Kaleidoscope", "designed_UDG_from_coords",
                   drift_note=("Paper Table 5 lists E=51 (17 disjoint K3). Deposit coords at R_b=8 "
                               "realise E=48; three K3 edges are missing. Either fix coords or update "
                               "Table 5 to E=48, d=0.0376."))
    print()

    # 3. carte_du_texte — R_b=10 → E=84 (paper says 85, off by 1)
    print("[carte_du_texte]")
    write_reconstructed_graph("carte_du_texte", "coords_designed.json", 10.0,
                              "5x10 planar grid (target: E=85; deposit coords realise E=84 at R_b=10)",
                              {"N": 50, "d": 0.069, "MIS": 25, "rho": 0.0})
    write_metadata("carte_du_texte", "graph_target.json",
                   "The Map of the Text", "designed_planar_grid_from_coords",
                   drift_note=("Paper Table 5 lists E=85, d=0.069 (5x10 grid). Deposit coords at R_b=10 "
                               "realise E=84, d=0.0686 — off by one boundary edge. Acceptably close; "
                               "Table 5 numerics still round to d=0.069."))
    print()

    # 4. incarnate_graph — repackage existing coords_2d_udg.json
    print("[incarnate_graph]")
    n, e = repackage_incarnate_graph()
    print(f"  repackaged: N={n} E={e}")
    write_metadata("incarnate_graph", "graph_target.json",
                   "The Incarnate Graph", "exact_2D_UDG_random",
                   extra={"note": "The text claims '50 pages / 466 edges' internally; canonical deposit graph is N=65, E=155. "
                                  "Internal text references should be updated to match deposit (separate task)."})
    print()

    # 5. vita_nel_cubo — graph_k8 numerics match paper
    print("[vita_nel_cubo]")
    write_metadata("vita_nel_cubo", "graph_k8.json",
                   "La Vita nel Cubo", "NLP_k8",
                   extra={"design_intent": "Truncated cube graph (target geometry); the deposited "
                                          "graph is the NLP k=8 graph whose numerics happen to "
                                          "match the paper's d=0.413 row by coincidence. The "
                                          "geometric label in Table 5 is aspirational."})
    print()

    # 6. sonetti_dal_tesseratto — graph_k8 numerics match paper
    print("[sonetti_dal_tesseratto]")
    write_metadata("sonetti_dal_tesseratto", "graph_k8.json",
                   "Sonetti dal Tesseratto", "NLP_k8",
                   extra={"design_intent": "Tesseract Q4 (target geometry); the deposited "
                                          "graph is the NLP k=8 graph at d=0.592, matching "
                                          "the paper's Table 5 row numerics. The Q4 label is "
                                          "aspirational."})
    print()


if __name__ == "__main__":
    main()
