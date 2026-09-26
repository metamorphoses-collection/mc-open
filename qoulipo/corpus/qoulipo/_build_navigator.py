#!/usr/bin/env python3
"""
Build the QOuLiPo single-page navigator for Zenodo.

Generates exactly ONE file:
  INDEX.html — landing page, lists all texts grouped by category,
               with inline SVG graph thumbnails + direct links to
               source/, metadata.json, and graph JSON files.

No per-text subpages. No external dependencies. Works offline, works on
Zenodo, works opened locally.
"""

import json
import math
from pathlib import Path

try:
    import networkx as nx
except Exception:
    nx = None

ROOT = Path(__file__).parent


# ─── Text catalog ─────────────────────────────────────────────────────────
CATEGORIES = [
    {
        "id": "exact_udg_2d",
        "title": "Exact 2D / 2L unit-disk graphs",
        "subtitle": "Texts whose graph is the register by construction, realisable in 2D or 2-layer hardware",
        "texts": [
            "incarnate_graph",
            "venticinque_stanze", "twenty_five_rooms",
            "castello_49_destini",
            "pascal_apocryphe", "pascal_apocryphe_scholia",
        ],
    },
    {
        "id": "beyond_2d",
        "title": "3D / higher-dimensional geometry targets",
        "subtitle": "Texts whose graph requires 3D or 4D registers; not 2D-UDG, not bilayer-realisable",
        "texts": [
            "friars_notebook",
            "vita_nel_cubo",
            "sonetti_dal_tesseratto",
        ],
    },
    {
        "id": "archimedean_lattices",
        "title": "Archimedean lattice families",
        "subtitle": "Texts spanning kagome, triangular hexagonal, king, denser-king, and snub-square families, each designed against the Cazals hardness landscape with a clean spectral-gap UDG construction.",
        "texts": [
            "triangular_hex_91",
            "king_9x9_81",
            "ext_king_sqrt5_9x9_81",
            "kagome_100",
            "snub_square_100",
            "triangular_hex_37",
        ],
    },
    {
        "id": "prescribed",
        "title": "Prescribed-property designs",
        "subtitle": "Texts engineered to specific graph-theoretic invariants (rigidity, planarity, bipartiteness, …)",
        "texts": [
            "irreplaceable_book", "kaleidoscope",
            "carte_du_texte", "proces_de_nithard",
            "piege_du_lecteur", "livre_fractal",
            "jumeaux_en", "jumeaux_fr",
            "partition_du_texte",
        ],
    },
    {
        "id": "knn_engineered",
        "title": "Engineered k-NN texts",
        "subtitle": "Texts whose graph is a k-nearest-neighbour graph of sentence embeddings, with prose engineered to push (N, d) toward a target region of the Cazals hardness landscape.",
        "texts": [
            "nithards_wager_en", "nithards_wager_fr",
            "pari_de_nithard_II", "pari_de_nithard_III",
        ],
    },
]

LANG_FLAG = {"EN": "🇬🇧", "FR": "🇫🇷", "IT": "🇮🇹", "LA": "🇮🇹"}


# ─── Load per-text data ───────────────────────────────────────────────────
GRAPH_FILES_PREF = [
    "graph_designed.json",
    "graph.json",
    "graph_k8.json",
    "graph_k16.json",
]

# For higher-dimensional targets we override the 2D spring layout with the
# text's designed 3D coordinates, projected isometrically with depth cues.
# Coords are bundled inside each folder as coords_3d.json so the deposit
# is self-contained.
THREED_OVERRIDES = {
    "friars_notebook": {"coords_file": ROOT / "friars_notebook" / "coords_3d.json"},
    "vita_nel_cubo": {"coords_file": ROOT / "vita_nel_cubo" / "coords_3d.json"},
    "sonetti_dal_tesseratto": {"coords_file": ROOT / "sonetti_dal_tesseratto" / "coords_3d.json"},
}


def load_text_data(folder):
    d = ROOT / folder
    if not d.exists():
        return None
    meta_path = d / "metadata.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    # Find graph file: prioritise the canonical_graph_file declared in metadata
    # (this is what the paper, registry, and verifier all agree on). Only fall
    # back to GRAPH_FILES_PREF heuristic if metadata doesn't declare it.
    graph_data = None
    graph_file = None
    canonical_graph = meta.get("canonical_graph_file")
    candidate_files = []
    if canonical_graph:
        candidate_files.append(canonical_graph)
    candidate_files.extend([f for f in GRAPH_FILES_PREF if f != canonical_graph])
    for fname in candidate_files:
        # Handle relative paths like "../pascal_menil_bilayer/graph_bilayer.json"
        gp = (d / fname).resolve() if fname.startswith("..") else d / fname
        if not gp.exists():
            continue
        try:
            candidate = json.loads(gp.read_text())
        except Exception:
            continue
        # Accept only if it looks like a graph with nodes + edges
        has_nodes = "nodes" in candidate and candidate["nodes"]
        has_edges = "edges" in candidate and candidate["edges"]
        nested = isinstance(candidate.get("graph"), dict) and \
                 "nodes" in candidate["graph"] and "edges" in candidate["graph"]
        if (has_nodes and has_edges) or nested:
            graph_data = candidate
            graph_file = fname
            break

    # Count source pages
    source_dir = d / "source"
    n_pages = len(list(source_dir.glob("*.txt"))) if source_dir.exists() else 0

    # Extra files available for download
    extra_files = []
    for fn in [
        "graph_designed.json", "graph_k3.json", "graph_k8.json",
        "graph_k16.json", "rigidity.json",
    ]:
        if (d / fn).exists():
            extra_files.append(fn)

    FLAGSHIPS = {"castello_49_destini", "venticinque_stanze", "pascal_apocryphe",
                 "pascal_apocryphe_scholia", "friars_notebook", "triangular_hex_37"}
    return {
        "folder": folder,
        "title": meta.get("title", folder),
        "subtitle": meta.get("subtitle", ""),
        "lang": meta.get("lang", "?"),
        "N": meta.get("N", n_pages),
        "designed_property": meta.get("designed_property", ""),
        "graph": graph_data,
        "graph_file": graph_file,
        "n_pages": n_pages,
        "has_source": source_dir.exists() and n_pages > 0,
        "extra_files": extra_files,
        "flagship": folder in FLAGSHIPS,
    }


# ─── Graph SVG thumbnail ──────────────────────────────────────────────────
def _extract_graph(graph_data):
    """Return (nodes: list[str], edges: list[(str, str)]) or None."""
    if not graph_data:
        return None
    # Some files nest the graph under a "graph" key
    inner = graph_data.get("graph") if isinstance(graph_data.get("graph"), dict) \
        else graph_data
    raw_nodes = inner.get("nodes", [])
    nodes = []
    if raw_nodes:
        if isinstance(raw_nodes[0], dict):
            nodes = [str(n.get("id", i)) for i, n in enumerate(raw_nodes)]
        else:
            nodes = [str(n) for n in raw_nodes]
    else:
        N = inner.get("N", 0)
        nodes = [f"v{i}" for i in range(N)]

    edges = []
    for e in inner.get("edges", []):
        if isinstance(e, dict):
            a, b = e.get("source"), e.get("target")
        elif isinstance(e, (list, tuple)):
            a, b = e[0], e[1]
        else:
            continue
        edges.append((str(a), str(b)))
    return nodes, edges


def _spring_layout(nodes, edges, width=260, height=180, pad=12):
    """Return {node: (x_px, y_px)} via networkx spring layout, fitted."""
    if nx is None or not nodes:
        return {}
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from([(a, b) for a, b in edges if a in nodes and b in nodes])
    # seed for reproducibility
    pos = nx.spring_layout(G, seed=42, iterations=80, k=None)
    if not pos:
        return {}
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    if not xs:
        return {}
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    dx = max(x_max - x_min, 1e-6)
    dy = max(y_max - y_min, 1e-6)
    w = width - 2 * pad
    h = height - 2 * pad
    out = {}
    for n, (x, y) in pos.items():
        out[n] = (
            pad + (x - x_min) / dx * w,
            pad + (y - y_min) / dy * h,
        )
    return out


def _project_3d(coords3d, width=260, height=180, pad=12):
    """Isometric-ish projection of 3D coords to 2D pixel space.
    Returns {node: (x_px, y_px, z_depth)} where z_depth is in [0,1] — 0=back, 1=front.
    Uses a simple cabinet projection with a mild tilt so the 3D shape reads."""
    if not coords3d:
        return {}
    # Cabinet projection: x' = x + z*0.5*cos(35°), y' = y + z*0.5*sin(35°)
    cos_a = math.cos(math.radians(35))
    sin_a = math.sin(math.radians(35))
    k = 0.45
    projected = {}
    zs = []
    for n, (x, y, z) in coords3d.items():
        xp = x + z * k * cos_a
        yp = -y + z * k * sin_a  # flip y so +y renders up
        projected[n] = (xp, yp, z)
        zs.append(z)
    # normalise z_depth to [0, 1]
    z_min, z_max = (min(zs), max(zs)) if zs else (0.0, 1.0)
    dz = max(z_max - z_min, 1e-6)
    # fit to pixel box
    xs = [v[0] for v in projected.values()]
    ys = [v[1] for v in projected.values()]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    w = width - 2 * pad
    h = height - 2 * pad
    sx = w / max(x_max - x_min, 1e-6)
    sy = h / max(y_max - y_min, 1e-6)
    s = min(sx, sy)
    cx = (x_min + x_max) / 2
    cy = (y_min + y_max) / 2
    out = {}
    for n, (xp, yp, z) in projected.items():
        px = width / 2 + (xp - cx) * s
        py = height / 2 + (yp - cy) * s
        out[n] = (px, py, (z - z_min) / dz)
    return out


def render_3d_svg(coords3d, edges, width=260, height=180, mis_pages=None):
    """Render a 3D-looking graph SVG with depth cues (back nodes/edges faded).
    MIS-set nodes are highlighted in gold."""
    mis_pages = mis_pages or set()
    proj = _project_3d(coords3d, width, height)
    if not proj:
        return f'<div class="no-graph">(3d projection unavailable)</div>'

    edge_els = []
    # sort edges by mean-z (back first) for painter's algorithm
    eds = [(a, b) for a, b in edges if a in proj and b in proj]
    eds.sort(key=lambda e: (proj[e[0]][2] + proj[e[1]][2]) / 2)
    for a, b in eds:
        x1, y1, z1 = proj[a]
        x2, y2, z2 = proj[b]
        z_mean = (z1 + z2) / 2
        op = 0.15 + 0.70 * z_mean
        edge_els.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
            f'x2="{x2:.1f}" y2="{y2:.1f}" stroke-opacity="{op:.2f}" />'
        )

    # Sort nodes back-to-front
    nodes_sorted = sorted(proj.items(), key=lambda kv: kv[1][2])
    node_els = []
    mis_node_els = []
    r_base = max(1.6, min(4.5, 80 / max(1, math.sqrt(len(proj)))))
    for n, (x, y, z) in nodes_sorted:
        r = r_base * (0.65 + 0.55 * z)
        op = 0.45 + 0.55 * z
        if n in mis_pages:
            r_mis = r * 1.6
            mis_node_els.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_mis:.2f}" '
                f'fill="#d4a017" stroke="#7a5a0a" stroke-width="0.8" '
                f'fill-opacity="{op:.2f}" />'
            )
        else:
            node_els.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" '
                f'fill-opacity="{op:.2f}" />'
            )

    return (
        f'<svg class="graph-thumb graph-3d" viewBox="0 0 {width} {height}" '
        f'width="100%" height="auto" preserveAspectRatio="xMidYMid meet">'
        f'<g class="edges">{"".join(edge_els)}</g>'
        f'<g class="nodes">{"".join(node_els)}</g>'
        f'<g class="mis-nodes">{"".join(mis_node_els)}</g>'
        f'</svg>'
    )


def render_graph_svg(graph_data, width=260, height=180, folder=None):
    """Return an inline SVG string for the graph thumbnail.
    For 3D/higher-dim targets (via THREED_OVERRIDES), uses an isometric
    projection of the designed 3D coords instead of a 2D spring layout."""
    # 3D override path: use canonical graph_data edges + bundled coords_3d.json
    if folder and folder in THREED_OVERRIDES:
        ov = THREED_OVERRIDES[folder]
        try:
            coords_data = json.loads(Path(ov["coords_file"]).read_text())
            coords3d = {k: tuple(v) for k, v in
                        coords_data.get("coords_3d", {}).items()}
        except Exception:
            coords3d = None
        extracted = _extract_graph(graph_data)
        edges = extracted[1] if extracted else []
        if coords3d and edges:
            mis_pages_3d = set()
            mis_path = ROOT / folder / "mis_analysis.json"
            if mis_path.exists():
                try:
                    mis_pages_3d = set(json.loads(mis_path.read_text()).get("MIS_pages", []))
                except Exception:
                    pass
            return render_3d_svg(coords3d, edges, width, height,
                                 mis_pages=mis_pages_3d)
        # fall through to 2D if 3D load failed

    # Standard 2D spring layout
    extracted = _extract_graph(graph_data)
    if not extracted:
        return f'<div class="no-graph">(no graph)</div>'
    nodes, edges = extracted
    if not nodes:
        return f'<div class="no-graph">(empty graph)</div>'
    pos = _spring_layout(nodes, edges, width, height)
    if not pos:
        return f'<div class="no-graph">(layout unavailable)</div>'

    # Edges first (so nodes draw on top)
    edge_els = []
    for a, b in edges:
        if a in pos and b in pos:
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            edge_els.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                f'x2="{x2:.1f}" y2="{y2:.1f}" />'
            )
    # Node dots — MIS pages highlighted (gold fill) if mis_pages provided.
    # For Pascal layer cards, the canonical graph is the bilayer aggregate;
    # so we load MIS_pages from the bilayer's mis_analysis, not the layer's.
    mis_pages = set()
    if folder:
        mis_source_folder = folder
        if folder in {"pascal_apocryphe", "pascal_apocryphe_scholia"}:
            mis_source_folder = "pascal_menil_bilayer"
        mis_path = ROOT / mis_source_folder / "mis_analysis.json"
        if mis_path.exists():
            try:
                mis_pages = set(json.loads(mis_path.read_text()).get("MIS_pages", []))
            except Exception:
                pass
    node_els = []
    mis_node_els = []
    r = max(1.4, min(4.0, 80 / max(1, math.sqrt(len(nodes)))))
    r_mis = r * 1.6
    for n, (x, y) in pos.items():
        if n in mis_pages:
            mis_node_els.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r_mis:.1f}" '
                f'fill="#d4a017" stroke="#7a5a0a" stroke-width="0.8" />'
            )
        else:
            node_els.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" />')

    return (
        f'<svg class="graph-thumb" viewBox="0 0 {width} {height}" '
        f'width="100%" height="auto" preserveAspectRatio="xMidYMid meet">'
        f'<g class="edges">{"".join(edge_els)}</g>'
        f'<g class="nodes">{"".join(node_els)}</g>'
        f'<g class="mis-nodes">{"".join(mis_node_els)}</g>'
        f'</svg>'
    )


# ─── CSS + layout ─────────────────────────────────────────────────────────
CSS = """
<style>
  :root {
    --bg: #f5f1e8;
    --card: #fafaf6;
    --ink: #2a2a2a;
    --brown: #6a4f1e;
    --gold: #c9a14a;
    --rule: #d4c8a8;
    --muted: #8a7a5a;
  }
  * { box-sizing: border-box; }
  body {
    font-family: 'Cormorant Garamond', Georgia, serif;
    background: var(--bg); color: var(--ink);
    max-width: 1280px; margin: 2em auto; padding: 1em 2em;
    line-height: 1.55;
  }
  header { display: flex; align-items: center; gap: 1.2em; margin-bottom: 0.4em; }
  header svg { flex-shrink: 0; }
  header h1 {
    font-family: 'Cinzel', serif; font-weight: 500;
    letter-spacing: 0.16em; margin: 0; font-size: 1.9em;
  }
  header p {
    margin: 0; color: var(--brown); font-style: italic; font-size: 1em;
    letter-spacing: 0.08em;
  }
  .lede { color: #555; max-width: 100%; margin: 1.5em 0 2em; font-size: 1.05em; }
  h2 {
    font-family: 'Cinzel', serif; font-weight: 400;
    color: var(--brown); letter-spacing: 0.06em;
    border-bottom: 1px solid var(--rule); padding-bottom: 0.3em;
    margin-top: 2.5em;
  }
  h2 + .subtitle {
    color: #888; font-style: italic; margin-top: -0.3em; margin-bottom: 1.2em;
  }
  .grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.2em;
  }
  .card {
    background: var(--card); border: 1px solid var(--rule);
    border-radius: 4px; padding: 1.2em;
    display: flex; flex-direction: column; gap: 0.6em;
  }
.card.flagship { border-left: 4px solid #f59e0b; background: #fffbeb; }
  .card .head {
    display: flex; justify-content: space-between; align-items: baseline;
  }
  .card .title {
    font-family: 'Cinzel', serif; font-weight: 500;
    font-size: 1.08em; letter-spacing: 0.04em;
  }
  .card .meta { color: var(--brown); font-size: 0.85em; font-style: italic; }
  .card .property {
    color: #777; font-size: 0.82em; margin-top: 0.6em;
  }
  .card .why {
    color: #333; font-size: 0.97em; line-height: 1.5;
    border-left: 2px solid var(--gold); padding-left: 0.7em;
    margin: 0.1em 0 0.2em;
  }
  .card .narrative-details {
    margin-top: 0.4em; font-size: 0.85em;
  }
  .card .narrative-details summary {
    color: var(--brown); cursor: pointer; font-style: italic;
    padding: 0.2em 0;
  }
  .card .narrative-details summary:hover { color: var(--gold); }
  .card .narrative {
    color: #555; font-size: 0.92em; line-height: 1.45; padding-top: 0.4em;
  }
  .card .graph-box {
    background: white; border: 1px solid var(--rule); border-radius: 3px;
    padding: 0.3em; display: flex; align-items: center; justify-content: center;
    min-height: 120px;
  }
  .graph-thumb .edges line {
    stroke: #c9a14a; stroke-width: 0.4; stroke-opacity: 0.45;
  }
  .graph-thumb .nodes circle {
    fill: #6a4f1e; stroke: #2a2a2a; stroke-width: 0.3;
  }
  .no-graph {
    color: #aaa; font-style: italic; font-size: 0.8em; padding: 2em 0;
  }
  .links {
    display: flex; flex-wrap: wrap; gap: 0.3em;
    font-size: 0.78em; border-top: 1px dotted var(--rule); padding-top: 0.5em;
    margin-top: auto;
  }
  .links a {
    background: var(--bg); border: 1px solid var(--rule); border-radius: 3px;
    padding: 0.15em 0.5em; color: var(--brown); text-decoration: none;
    font-family: 'Courier New', monospace; font-size: 0.9em;
  }
  .links a:hover { background: var(--gold); color: white; }
  footer {
    margin-top: 4em; padding-top: 1em; border-top: 1px solid var(--rule);
    color: #888; font-size: 0.9em; font-style: italic;
  }
  footer a { color: var(--brown); }
</style>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
"""

QOULIPO_LOGO = """<svg viewBox="0 0 120 120" width="88" height="88" aria-label="Metamorphoses of Civilization mark — Stomachion (14 pieces)" role="img">
  <g transform="scale(10)" stroke="#2a2a2a" stroke-width="0.16" stroke-linejoin="round" stroke-linecap="round">
    <rect x="0" y="0" width="12" height="12" fill="none" stroke="#2a2a2a" stroke-width="0.22"/>
    <polygon points="6,0 0,0 2,2 4,4"        fill="#fafaf6"/>
    <polygon points="12,0 6,0 9,6 12,4"      fill="#e8dcc0"/>
    <polygon points="12,6 12,4 9,6"          fill="#fafaf6"/>
    <polygon points="12,12 12,6 9,6"         fill="#e8dcc0"/>
    <polygon points="6,12 12,12 8,8"         fill="#fafaf6"/>
    <polygon points="3,12 6,12 6,6 4,4 3,6"  fill="#e8dcc0"/>
    <polygon points="0,12 3,12 2,8"          fill="#fafaf6"/>
    <polygon points="0,0 0,12 2,2"           fill="#e8dcc0"/>
    <polygon points="4,4 2,2 0,12 2,8 3,6"   fill="#fafaf6"/>
    <polygon points="4,4 6,6 6,0"            fill="#e8dcc0"/>
    <polygon points="6,6 8,8 9,6 6,0"        fill="#fafaf6"/>
    <polygon points="8,8 6,6 6,12"           fill="#e8dcc0"/>
    <polygon points="8,8 12,12 9,6"          fill="#fafaf6"/>
    <polygon points="3,6 2,8 3,12"           fill="#e8dcc0"/>
  </g>
</svg>"""


# ─── Card rendering ───────────────────────────────────────────────────────
def build_card(data, summary):
    folder = data["folder"]
    narrative = summary.get("narrative", "—")
    why = summary.get("why_interesting", "")
    flag = LANG_FLAG.get(data["lang"], "")
    svg = render_graph_svg(data["graph"], folder=folder)
    # Small per-file link chips
    link_chips = []
    if data["has_source"]:
        link_chips.append(
            f'<a href="{folder}/source/" title="source prose">source/</a>'
        )
    link_chips.append(
        f'<a href="{folder}/metadata.json">metadata</a>'
    )
    for f in data["extra_files"]:
        short = f.replace("graph_", "g_").replace(".json", "")
        link_chips.append(f'<a href="{folder}/{f}">{short}</a>')
    # Graph info line
    g = data["graph"] or {}
    E = g.get("E") or g.get("num_edges") or len(g.get("edges", []))
    dens = g.get("density")
    dens_str = f"d={dens:.3f}" if isinstance(dens, (int, float)) else ""
    graph_meta = ""
    if data["graph_file"] and E:
        # For component folders (Pascal layers), the canonical graph is the
        # AGGREGATE bilayer (40 atoms); the local source folder is just the layer.
        IS_COMPONENT = folder in {"pascal_apocryphe", "pascal_apocryphe_scholia"}
        if IS_COMPONENT:
            graph_meta = (
                f'<div class="property" style="color:#999;font-size:0.75em;'
                f'border:none;padding-top:0.1em;">'
                f'Layer source: {data["N"]} pages · '
                f'Aggregate canonical graph: {data["graph_file"]} · '
                f'N=40 E={E} {dens_str}</div>'
            )
        else:
            graph_meta = (
                f'<div class="property" style="color:#999;font-size:0.75em;'
                f'border:none;padding-top:0.1em;">'
                f'{data["graph_file"]} · N={data["N"]} E={E} {dens_str}</div>'
            )

    # (Per-graph ★ layout notes were removed as stale; kept here for future reuse.)
    layout_note = ""
    why_block = f'<div class="why">{why}</div>' if why else ""
    flagship_badge = ('<div style="margin-top:4px;"><span style="background:#fef3c7;'
                       'color:#92400e;padding:2px 8px;border-radius:6px;font-size:0.75em;'
                       'font-weight:600;border:1px solid #fcd34d;letter-spacing:0.05em;" '
                       'title="Flagship instance: more development effort and revision passes than the benchmark-only entries">'
                       '★ flagship</span></div>') if data.get("flagship") else ""
    card_class = "card flagship" if data.get("flagship") else "card"
    return f'''
      <div class="{card_class}" id="{folder}">
        <div class="head">
          <div class="title">{data["title"]}{flagship_badge}</div>
          <div class="meta">{flag} N={data["N"]}</div>
        </div>
        {why_block}
        <div class="graph-box">{svg}</div>
        {graph_meta}
        {layout_note}
        <details class="narrative-details">
          <summary>Constraint &amp; theme notes</summary>
          <div class="narrative">{narrative}</div>
        </details>
        <div class="links">{"".join(link_chips)}</div>
      </div>'''


# ─── Full page ────────────────────────────────────────────────────────────
def build_index(summaries):
    sections = []
    total = 0
    for cat in CATEGORIES:
        cards_html = []
        for folder in cat["texts"]:
            data = load_text_data(folder)
            if data is None:
                continue
            cards_html.append(build_card(data, summaries.get(folder, {})))
            total += 1
        sections.append(
            f'<h2>{cat["title"]}</h2>'
            f'<div class="subtitle">{cat["subtitle"]}</div>'
            f'<div class="grid">{"".join(cards_html)}</div>'
        )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>QOuLiPo Corpus — Metamorphoses of Civilization</title>
{CSS}
</head>
<body>

<header>
  {QOULIPO_LOGO}
  <div>
    <h1>QOuLiPo Corpus</h1>
    <p>Metamorphoses of Civilization · 2026</p>
  </div>
</header>

<p class="lede">
This page is the QOuLiPo Corpus, a strand of the
<a href="/" style="color:#7a5a0a;">Metamorphoses Collection</a>: the
constrained-writing companion to the natural-text corpus the collection
has been building around its anchor edition (Pier Francesco Giambullari's
1544 reconstruction of Dante's Inferno). The natural-text companions —
Augustine, Boethius, Dante, Galileo, Giambullari, Marguerite de Navarre,
Lactantius, Ausonius, Mishnah Avot — are computed with the same
graph/MIS pipeline; their full data, alongside the constrained corpus
shown here, is in the
<a href="https://zenodo.org/records/20074378" style="color:#7a5a0a;">Zenodo deposit</a>.
</p>

<p class="lede">
The corpus comprises {total} literary works engineered as quantum-benchmark
instances on neutral-atom hardware, each both a readable book and a graph
whose structural properties (density, rigidity, planarity, bipartiteness)
are controlled by design. Each card below shows the canonical compute-instance
graph and links to the text's source files, metadata, and graph data.
</p>

<p class="lede">
Six cards carry a <span style="background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:5px;font-size:0.85em;font-weight:600;border:1px solid #fcd34d;">★ flagship</span> badge. The badge marks editorial attention — texts that received more
development effort and revision passes — not a finished-literary-quality verdict. The prose in this corpus is
generated under graph-topological constraints with substantial human revision; the flagship pieces are
first attempts pursued further than the benchmark-only entries, and the author looks forward to
contributions from writers, poets, and OuLiPian collaborators that turn these graph-bound exercises
into more developed works.
</p>


{"".join(sections)}

<footer>
QOuLiPo Corpus · 2026.
Texts released under CC-BY-4.0; reuse with attribution.
Built with <code>_build_navigator.py</code>.
</footer>

</body>
</html>
'''


# ─── Main ────────────────────────────────────────────────────────────────
def main():
    summaries_path = ROOT / "_summaries.json"
    if summaries_path.exists():
        summaries = json.loads(summaries_path.read_text())
        print(f"Loaded {len(summaries)} summaries")
    else:
        print("No _summaries.json yet — using empty narratives")
        summaries = {}

    index_html = build_index(summaries)
    out_path = ROOT / "INDEX.html"
    out_path.write_text(index_html)
    print(f"Built {out_path} ({len(index_html):,} chars)")

    # Remove any stale per-text index.html from the earlier two-level design
    stale = 0
    for cat in CATEGORIES:
        for folder in cat["texts"]:
            p = ROOT / folder / "index.html"
            if p.exists():
                p.unlink()
                stale += 1
    if stale:
        print(f"Removed {stale} stale per-text index.html files")


if __name__ == "__main__":
    main()
