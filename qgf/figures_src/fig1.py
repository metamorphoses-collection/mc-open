# PREFLIGHT-EXEMPT: figure script; reads deposited registers only, submits nothing.
"""Register panels for EPJ Fig. 1 (Folio window, Marseille mosaic, die-link graph).
The published figure also uses photographs of a Folio page, the pavement, three coins, and two
Eucharisticos copies. Those images are not in this deposit, and this script does not load them."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from palette import EVENT, INK, NEUTRAL, LIGHT, SECOND, seq

RED = EVENT

def register(ax, P, edges, red, title, s=46):
    P = np.asarray(P, float)
    for u, v in edges:
        ax.plot(P[[u, v], 0], P[[u, v], 1], "-", color="#c8c8c8", lw=0.9, zorder=1)
    red = np.asarray(red, bool)
    ax.scatter(P[~red, 0], P[~red, 1], s=s, c="white", edgecolors=INK, linewidths=0.8, zorder=2)
    ax.scatter(P[red, 0], P[red, 1], s=s * 1.25, c=RED, edgecolors=INK, linewidths=0.6, zorder=3)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    [sp.set_visible(False) for sp in ax.spines.values()]
    ax.set_title(title, fontsize=9, fontweight="bold", loc="left")

fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6))

# Folio window 60, from the deposited window file
W = {}
for l in (ROOT / "data/folio/windows.jsonl").read_text().splitlines():
    if l.strip():
        w = json.loads(l); W[w["id"]] = w
w = W[60]
P = np.array(w["coords_um"], float)
E = [tuple(e) for e in w["edges"]]
deg = np.zeros(w["N"], int)
for u, v in E:
    deg[u] += 1; deg[v] += 1
register(ax[0], P, E, deg < 4, "(b) Folio window", s=28)

# Marseille mosaic
rm = json.load(open(ROOT / "data/mosaic/reg_MHM_winA.json"))
# prefer dynamics register classes if present
REGS = {r["name"]: r for r in json.load(open(ROOT / "data/dynamics/fig2_regs.json"))}
rm_ = REGS.get("mosaic_MHM_winA", rm)
Pm = np.array(rm_.get("coords_um", rm.get("coords_um") if "coords_um" in rm else rm.get("positions")), float)
if "adj" in rm and "edges" not in rm:
    A = np.array(rm["adj"]); Em = [(i, j) for i in range(len(A)) for j in range(i + 1, len(A)) if A[i, j]]
else:
    D = np.linalg.norm(Pm[:, None] - Pm[None], axis=-1)
    Em = [(i, j) for i in range(len(Pm)) for j in range(i + 1, len(Pm)) if D[i, j] <= 6.5 * 1.05]
red_m = np.zeros(len(Pm), bool)
if "red" in rm_:
    red_m[rm_["red"]] = True
register(ax[1], Pm, Em, red_m, "(d) mosaic window", s=18)
if "black" in rm_:
    blk = np.zeros(len(Pm), bool); blk[rm_["black"]] = True
    ax[1].scatter(Pm[blk, 0], Pm[blk, 1], s=22, c=INK, edgecolors=INK, linewidths=0.8, zorder=4)

# Die-link unique? Published Fig 1h is the register as drawn; the paper now describes 55 combinations.
# Use the as-run file only if we want to match the published image (56 sites). README notes the 55/56 distinction.
# For the register panel corresponding to the study graph, use the dedup file.
d = json.load(open(ROOT / "data/die/qgf_dielink_a_dedup.json"))
Pd = np.array(d["positions"]); A = np.array(d["adj"])
Ed = [(i, j) for i in range(len(A)) for j in range(i + 1, len(A)) if A[i, j]]
degd = np.zeros(len(Pd), int)
for u, v in Ed:
    degd[u] += 1; degd[v] += 1
register(ax[2], Pd, Ed, degd == 1, "(h) die links (55 combinations)", s=28)
iso = degd == 0
ax[2].scatter(Pd[iso, 0], Pd[iso, 1], s=28, c=LIGHT, edgecolors=INK, linewidths=0.8, zorder=4)

plt.tight_layout()
out = HERE / "encodings_registers.png"
fig.savefig(out, dpi=200, bbox_inches="tight")
print("saved", out, "(register panels only; photographs are not deposited)")
