#!/usr/bin/env python3
"""Phase 1 redesigns: 5 mechanical fixes that don't require text rewriting.

  twenty_five_rooms     — copy king-5x5 coords from venticinque_stanze
  kaleidoscope          — regenerate 17 disjoint K3 clusters (clean coords)
  carte_du_texte        — replace coords with clean 5x10 grid (4-NN edges)
  proces_de_nithard     — declare K_{25,25} edge list (purely combinatorial)
  partition_du_texte    — induce graph_k8.json subgraph on first 50 nodes
"""
import json
import math
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _compute_canonical import canonical_metrics

QOULIPO = Path(__file__).resolve().parent / "qoulipo"


def write_metadata(folder, canonical_graph, paper_row, mode, extra=None):
    base = QOULIPO / folder
    existing = json.loads((base / "metadata.json").read_text()) if (base / "metadata.json").exists() else {}
    print(f"  computing metrics for {canonical_graph}...")
    m = canonical_metrics(base / canonical_graph, opt_cap=500, time_cap_s=180)
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
    (base / "metadata.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"  ✓ {folder}: N={m['canonical_N']} E={m['canonical_E']} d={m['canonical_density']} "
          f"MIS={m['canonical_MIS']} ρ={m['canonical_rho']} #opt={m['canonical_optima']}"
          f"{' (cap)' if m['canonical_optima_cap_reached'] else ''}")
    return m


def redesign_twenty_five_rooms():
    print("\n[twenty_five_rooms] copying king 5x5 coords from venticinque_stanze")
    src = QOULIPO / "venticinque_stanze" / "coords_2d_king5x5.json"
    coords_data = json.loads(src.read_text())
    coords = coords_data["coords_2d"]
    R_b = coords_data["R_b_um"]
    # Rename node ids from "stanza_NN" to "room_NN"
    new_coords = {}
    rename = {}
    for k, v in coords.items():
        new_k = k.replace("stanza", "room")
        new_coords[new_k] = v
        rename[k] = new_k
    nodes = list(new_coords.keys())
    pts = [new_coords[k] for k in nodes]
    edges = []
    for i, j in combinations(range(len(nodes)), 2):
        if math.dist(pts[i], pts[j]) <= R_b + 1e-9:
            edges.append({"source": nodes[i], "target": nodes[j]})
    graph = {
        "N": len(nodes), "E": len(edges),
        "density": round(2 * len(edges) / (len(nodes) * (len(nodes) - 1)), 4),
        "R_b_um": R_b,
        "geometry": "5x5 king grid (exact 2D UDG, EN twin of venticinque_stanze)",
        "source": "Copied from venticinque_stanze/coords_2d_king5x5.json with node ids renamed.",
        "nodes": nodes,
        "coords_2d": new_coords,
        "edges": edges,
    }
    base = QOULIPO / "twenty_five_rooms"
    (base / "graph_target.json").write_text(json.dumps(graph, indent=2) + "\n")
    coords_out = {"node_ids": nodes, "coords_2d": new_coords, "R_b_um": R_b,
                  "spacing_um": coords_data.get("spacing_um"),
                  "source": "Copied from venticinque_stanze with node renaming."}
    (base / "coords_2d_king5x5.json").write_text(json.dumps(coords_out, indent=2) + "\n")
    write_metadata("twenty_five_rooms", "graph_target.json",
                   "The Twenty-Five Rooms", "exact_2D_UDG_king5x5",
                   extra={"designed_property": "King 5x5 exact 2D UDG (EN twin of venticinque_stanze)",
                          "register_target": "2D, exact",
                          "twin_of": "venticinque_stanze",
                          "type": "qoulipo_engineered",
                          "project": "QOuLiPo",
                          "paper": "Jurczak 2026, arXiv"})


def redesign_kaleidoscope():
    print("\n[kaleidoscope] regenerating 17 disjoint K3 clusters with clean coords")
    base = QOULIPO / "kaleidoscope"
    # 17 K3 clusters in the plane. Each cluster: 3 points spaced ~3 um apart in
    # an equilateral triangle, clusters separated by ~25 um >> R_b=8.
    R_b = 8.0
    intra = 4.0  # within-cluster spacing (well below R_b)
    inter_x = 25.0  # between-cluster spacing along x
    inter_y = 25.0  # between-cluster spacing along y
    coords = {}
    cluster_size = 3
    cols = 5  # 17 clusters in a 5-wide grid (4 rows + 1 partial)
    nodes = []
    for c in range(17):
        cx = (c % cols) * inter_x
        cy = (c // cols) * inter_y
        # Equilateral triangle of side `intra`
        triangle = [
            (cx, cy),
            (cx + intra, cy),
            (cx + intra / 2, cy + intra * math.sqrt(3) / 2),
        ]
        for k, (x, y) in enumerate(triangle):
            nid = f"p{c * 3 + k + 1:03d}"  # p001..p051
            coords[nid] = [x, y]
            nodes.append(nid)
    pts = [coords[n] for n in nodes]
    edges = []
    for i, j in combinations(range(len(nodes)), 2):
        if math.dist(pts[i], pts[j]) <= R_b + 1e-9:
            edges.append({"source": nodes[i], "target": nodes[j]})
    graph = {
        "N": len(nodes), "E": len(edges),
        "density": round(2 * len(edges) / (len(nodes) * (len(nodes) - 1)), 4),
        "R_b_um": R_b,
        "geometry": "17 disjoint K3 cliques (each: equilateral triangle of side 4 um, clusters 25 um apart)",
        "source": "Regenerated from clean K3-cluster coordinates (intra=4 um, inter=25 um, R_b=8 um).",
        "nodes": nodes, "coords_2d": coords, "edges": edges,
    }
    (base / "graph_target.json").write_text(json.dumps(graph, indent=2) + "\n")
    # Update coords_designed.json to match the new clean placement
    (base / "coords_designed.json").write_text(json.dumps(coords, indent=2) + "\n")
    write_metadata("kaleidoscope", "graph_target.json",
                   "The Kaleidoscope", "designed_K3_unions",
                   extra={"designed_property": "Maximal degeneracy via 17 disjoint K3 cliques (3^17 ≈ 1.3e8 valid backbones)",
                          "register_target": "2D, exact",
                          "type": "qoulipo_engineered",
                          "project": "QOuLiPo",
                          "paper": "Jurczak 2026, arXiv"})


def redesign_carte_du_texte():
    print("\n[carte_du_texte] replacing coords with clean 5x10 grid (4-NN edges)")
    base = QOULIPO / "carte_du_texte"
    R_b = 5.5  # spacing 5; R_b just above so only 4-NN, no diagonals
    spacing = 5.0
    coords = {}
    nodes = []
    for r in range(5):
        for c in range(10):
            nid = f"p{r * 10 + c + 1:03d}"
            coords[nid] = [c * spacing, r * spacing]
            nodes.append(nid)
    pts = [coords[n] for n in nodes]
    edges = []
    for i, j in combinations(range(len(nodes)), 2):
        if math.dist(pts[i], pts[j]) <= R_b + 1e-9:
            edges.append({"source": nodes[i], "target": nodes[j]})
    graph = {
        "N": len(nodes), "E": len(edges),
        "density": round(2 * len(edges) / (len(nodes) * (len(nodes) - 1)), 4),
        "R_b_um": R_b,
        "geometry": "5x10 planar grid (4-nearest-neighbour edges only, bipartite)",
        "source": "Regenerated from clean 5x10 grid coordinates (spacing=5 um, R_b=5.5 um → 4-NN only).",
        "nodes": nodes, "coords_2d": coords, "edges": edges,
    }
    (base / "graph_target.json").write_text(json.dumps(graph, indent=2) + "\n")
    (base / "coords_designed.json").write_text(json.dumps(coords, indent=2) + "\n")
    write_metadata("carte_du_texte", "graph_target.json",
                   "The Map of the Text", "designed_planar_grid",
                   extra={"designed_property": "5x10 planar grid (bipartite, 85 edges, MIS=25)",
                          "register_target": "2D, exact",
                          "type": "qoulipo_engineered",
                          "project": "QOuLiPo",
                          "paper": "Jurczak 2026, arXiv"})


def redesign_proces_de_nithard():
    print("\n[proces_de_nithard] declaring K_{25,25} bipartite edge list")
    base = QOULIPO / "proces_de_nithard"
    nodes = [f"p{i + 1:03d}" for i in range(50)]
    # Pages 1..25 = prosecution (left partition); pages 26..50 = defense (right partition)
    edges = []
    for i in range(25):
        for j in range(25, 50):
            edges.append({"source": nodes[i], "target": nodes[j]})
    # No coordinate constraint — this is a pure combinatorial design.
    # For visualisation we lay out the two partitions on two parallel lines.
    coords = {}
    for i in range(25):
        coords[nodes[i]] = [0.0, i * 5.0]      # prosecution column
        coords[nodes[i + 25]] = [40.0, i * 5.0]  # defense column
    graph = {
        "N": 50, "E": len(edges),
        "density": round(2 * len(edges) / (50 * 49), 4),
        "geometry": "K_{25,25} complete bipartite (prosecution × defense)",
        "source": "Declared edge list: every page in pages 1-25 (prosecution) is adjacent to every page in pages 26-50 (defense).",
        "nodes": nodes,
        "coords_2d_visualisation": coords,
        "edges": edges,
        "partition_left":  nodes[:25],
        "partition_right": nodes[25:],
    }
    (base / "graph_target.json").write_text(json.dumps(graph, indent=2) + "\n")
    write_metadata("proces_de_nithard", "graph_target.json",
                   "The Trial of Nithard", "designed_bipartite_K25_25",
                   extra={"designed_property": "Complete bipartite K_{25,25} (prosecution vs defense)",
                          "register_target": "2D embedding requires SA (not exact UDG)",
                          "type": "qoulipo_engineered",
                          "project": "QOuLiPo",
                          "paper": "Jurczak 2026, arXiv"})


def redesign_partition_du_texte():
    print("\n[partition_du_texte] inducing graph_k8 subgraph on first 50 (canonical) nodes")
    base = QOULIPO / "partition_du_texte"
    g = json.loads((base / "graph_k8.json").read_text())
    all_nodes = g["nodes"]
    if all_nodes and isinstance(all_nodes[0], dict):
        all_nodes = [n.get("id", str(i)) for i, n in enumerate(all_nodes)]
    all_nodes = [str(n) for n in all_nodes]
    canonical = all_nodes[:50]
    canon_set = set(canonical)
    edges_in = []
    for e in g["edges"]:
        if isinstance(e, dict):
            a, b = str(e["source"]), str(e["target"])
        else:
            a, b = str(e[0]), str(e[1])
        if a in canon_set and b in canon_set:
            edges_in.append({"source": a, "target": b})
    induced = {
        "N": 50, "E": len(edges_in),
        "density": round(2 * len(edges_in) / (50 * 49), 4),
        "geometry": "Induced subgraph of graph_k8.json on canonical 50 source pages (paratext stripped).",
        "source": "Induced from graph_k8.json by restricting to nodes page_001..page_050.",
        "k": 8, "embedder": g.get("embedder", "multilingual-e5-large-instruct"),
        "nodes": canonical, "edges": edges_in,
    }
    (base / "graph_canonical_50.json").write_text(json.dumps(induced, indent=2) + "\n")
    write_metadata("partition_du_texte", "graph_canonical_50.json",
                   "La Partition du Texte", "NLP_k8_canonical_subgraph",
                   extra={"designed_property": "5 poetic-form communities (sonnet, villanelle, rondeau, ballade, haiku)",
                          "register_target": "2D embedding requires SA",
                          "induced_from": "graph_k8.json (60-node graph on full source/, restricted to canonical 50)",
                          "type": "qoulipo_engineered",
                          "project": "QOuLiPo",
                          "paper": "Jurczak 2026, arXiv"})


def main():
    print("Phase 1 redesigns — 5 mechanical fixes\n")
    redesign_twenty_five_rooms()
    redesign_kaleidoscope()
    redesign_carte_du_texte()
    redesign_proces_de_nithard()
    redesign_partition_du_texte()


if __name__ == "__main__":
    main()
