#!/usr/bin/env python3
"""Friar's Notebook v2 — thread-matrix builder and verifier.

Emits:
  - thread_matrix_v2.json   : the (page, motif) assignment + edge map
  - adjacency_check.txt     : confirms designed adjacency = dodecahedron

Usage:
  python3 build_friars_v2.py
"""
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Dodecahedron edge list (pages 1..20 correspond to vertices v00..v19)
DODEC_EDGES = [
    (1, 9), (1, 10), (1, 11),       # v00 neighbors: v08, v09, v10
    (2, 11), (2, 12), (2, 16),      # v01 neighbors: v10, v11, v15
    (3, 10), (3, 14), (3, 15),      # v02 neighbors: v09, v13, v14
    (4, 14), (4, 16), (4, 18),      # v03 neighbors: v13, v15, v17
    (5, 9), (5, 13), (5, 17),       # v04 neighbors: v08, v12, v16
    (6, 12), (6, 17), (6, 19),      # v05 neighbors: v11, v16, v18
    (7, 13), (7, 15), (7, 20),      # v06 neighbors: v12, v14, v19
    (8, 18), (8, 19), (8, 20),      # v07 neighbors: v17, v18, v19
    (9, 12),                        # v08-v11
    (10, 13),                       # v09-v12
    (11, 14),                       # v10-v13
    (15, 18),                       # v14-v17
    (16, 19),                       # v15-v18
    (17, 20),                       # v16-v19
]

# Motif map: edge_id -> (page_a, page_b, motif_title, keywords)
MOTIFS = {
    "e01": (1, 9,   "The Rose Window",         ["rose-window", "twelve-petal", "Sext-hour", "counting-the-points"]),
    "e02": (1, 10,  "The Host Inscribed",      ["inscribed-square", "elevation-wafer", "nested-circles", "three-breaths"]),
    "e03": (1, 11,  "Breviary Marks",          ["Psalm-103", "pricked-margin", "five-bodies", "breviary-corner"]),
    "e04": (2, 11,  "Mule-Train Account",      ["pack-mule", "Milan-road", "carriage-fee", "scudi"]),
    "e05": (2, 12,  "Monte dei Paschi Entry",  ["Monte-dei-Paschi", "Siena-bank", "compound-interest", "florin"]),
    "e06": (2, 16,  "The Closing Balance",     ["final-reckoning", "debit-column", "credit-column", "balanced-book"]),
    "e07": (3, 10,  "Sansepolcro Keystone",    ["keystone", "sandstone-ashlar", "Borgo-arch", "stonemason-mark"]),
    "e08": (3, 14,  "The Gold-Leaf Angel",     ["gold-leaf", "gilded-halo", "angel-panel", "illumined-margin"]),
    "e09": (3, 15,  "Saturn's Quartering",     ["Saturn", "quartering", "seventh-house", "orbital-arc"]),
    "e10": (4, 14,  "Euclid VI.30",            ["division-extreme-mean", "Euclid-VI.30", "golden-section", "phi-ratio"]),
    "e11": (4, 16,  "Demonstration Interrupted", ["Q.E.D.", "demonstration-broken", "Euclid-lemma", "proof-margin"]),
    "e12": (4, 18,  "Manuscript V.27",         ["folio-V.27", "vellum-codex", "manuscript-hand", "codex-shelf"]),
    "e13": (5, 9,   "Leonardo's Lamp",         ["Leonardo", "oil-lamp", "chiaroscuro-studio", "studio-flame"]),
    "e14": (5, 13,  "The Milan Conversation",  ["Milan-walk", "Sforza-court", "conversation-at-dusk", "dialogue-street"]),
    "e15": (5, 17,  "The String Ratio",        ["gut-string", "2:3-fifth", "Pythagorean-tuning", "monochord"]),
    "e16": (6, 12,  "The Apprentice's Bet",    ["apprentice", "wager-pot", "dice-throw", "triple-six"]),
    "e17": (6, 17,  "Brush and Lute",          ["sable-brush", "lute-fret", "workshop-lute", "varnish-lute"]),
    "e18": (6, 19,  "The Tempera Vision",      ["egg-yolk", "tempera-jar", "binder-recipe", "pigment-grind"]),
    "e19": (7, 13,  "Jacob's Ladder",          ["Jacob-ladder", "ladder-rungs", "ascending-angels", "oneiric-step"]),
    "e20": (7, 15,  "The Seven Planets",       ["seven-planets", "planetary-hour", "Venus-dream", "Mars-augury"]),
    "e21": (7, 20,  "The Dodecahedron Unfinished", ["dodecahedron-dream", "twelve-face", "aether-fifth", "unfinished-vision"]),
    "e22": (8, 18,  "The Pigment Catalogue",   ["lapis-lazuli", "malachite-green", "cinnabar-vermilion", "pigment-receipt"]),
    "e23": (8, 19,  "The Gilder's Vision",     ["gold-leaf-gilder", "bole-red", "agate-burnisher", "gilding-light"]),
    "e24": (8, 20,  "Recipe Broken Off",       ["yolk-measure", "vinegar-drop", "recipe-breaks", "ingredient-list"]),
    "e25": (9, 12,  "Pascal Before Pascal",    ["probability-of-salvation", "wager-for-soul", "infinite-gain", "finite-stake"]),
    "e26": (10, 13, "The Borgo Facade",        ["borgo-facade", "pilaster-order", "entablature-line", "proportional-elevation"]),
    "e27": (11, 14, "The Franciscan Road",     ["Franciscan-rule-road", "wayside-shrine", "pilgrim-step", "tertiary-cord"]),
    "e28": (15, 18, "The Almagest Margin",     ["Ptolemy-Almagest", "star-chart", "margin-note", "zodiac-table"]),
    "e29": (16, 19, "The Tomb of Light",       ["tomb-inscription", "light-beam-tomb", "stone-lettering", "last-light"]),
    "e30": (17, 20, "The Unfinished Fugue",    ["fugue-subject", "counterpoint-line", "interval-9:8", "broken-cadence"]),
}

REGISTERS = {
    1:  "confession",
    2:  "ledger entry",
    3:  "sonnet",
    4:  "mathematical demonstration",
    5:  "letter (to Leonardo)",
    6:  "workshop inventory",
    7:  "dream",
    8:  "recipe (egg tempera and gold leaf)",
    9:  "sermon fragment",
    10: "architectural specification",
    11: "travel diary",
    12: "wager / probability problem",
    13: "dialogue (Platonic manner)",
    14: "prayer",
    15: "astrological note",
    16: "epitaph",
    17: "musical proportion table",
    18: "library catalogue",
    19: "vision",
    20: "last page (unfinished)",
}


def build_page_motifs():
    """Return {page: [motif_id, ...]}."""
    pm = {p: [] for p in range(1, 21)}
    for mid, (a, b, _, _) in MOTIFS.items():
        pm[a].append(mid)
        pm[b].append(mid)
    return pm


def adjacency_from_motifs(page_motifs):
    """Return the set of edges implied by shared motifs (τ=1)."""
    edges = set()
    for i, j in combinations(range(1, 21), 2):
        shared = set(page_motifs[i]) & set(page_motifs[j])
        if shared:
            edges.add(tuple(sorted((i, j))))
    return edges


def main():
    page_motifs = build_page_motifs()

    # Per-page motif count
    for p, motifs in page_motifs.items():
        assert len(motifs) == 3, f"page {p} has {len(motifs)} motifs, expected 3"

    # Per-motif appearance count
    counts = {mid: 0 for mid in MOTIFS}
    for motifs in page_motifs.values():
        for mid in motifs:
            counts[mid] += 1
    for mid, c in counts.items():
        assert c == 2, f"motif {mid} appears on {c} pages, expected 2"

    # Designed adjacency vs dodecahedron
    designed = adjacency_from_motifs(page_motifs)
    target = {tuple(sorted(e)) for e in DODEC_EDGES}
    assert designed == target, (
        f"MISMATCH: designed={len(designed)} target={len(target)} "
        f"diff={designed ^ target}"
    )

    # Emit artefacts
    out = {
        "version": "v2",
        "N": 20,
        "target_graph": "regular_dodecahedron",
        "num_edges": len(target),
        "density": round(2 * len(target) / (20 * 19), 4),
        "expected_MIS": 8,
        "expected_n_optima": 5,
        "expected_rho": 0.0,
        "T_motifs": len(MOTIFS),
        "m_motifs_per_page": 3,
        "tau_edge_threshold": 1,
        "registers": REGISTERS,
        "motifs": {
            mid: {
                "pages": [a, b],
                "title": title,
                "keywords": kws,
            }
            for mid, (a, b, title, kws) in MOTIFS.items()
        },
        "page_motifs": page_motifs,
        "designed_edges": sorted(target),
    }
    out_path = HERE / "thread_matrix_v2.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")

    # Readable adjacency summary
    summary = [
        f"Friar's Notebook v2 — adjacency check",
        f"  N = 20, motifs T = {len(MOTIFS)}, per-page m = 3, tau = 1",
        f"  designed edges: {len(designed)} (target: {len(target)})",
        f"  designed == dodecahedron: {designed == target}",
        f"  density = {2 * len(designed) / (20 * 19):.4f}",
        "",
        "Per-page motif assignments:",
    ]
    for p in range(1, 21):
        summary.append(f"  page {p:2d} ({REGISTERS[p]}): {page_motifs[p]}")
    (HERE / "adjacency_check.txt").write_text("\n".join(summary) + "\n")
    print(f"Wrote {HERE / 'adjacency_check.txt'}")
    print()
    print("\n".join(summary))


if __name__ == "__main__":
    main()
