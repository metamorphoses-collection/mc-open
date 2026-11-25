"""Figure 4: each register's mean occupation on hardware against its χ=600 emulation, by class of atom, under the AFM and FM-like drives."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from palette import EVENT, INK, NEUTRAL, LIGHT, SECOND, seq

RED, GREY = EVENT, NEUTRAL
HW = json.load(open(ROOT / "data/dynamics/hardware_curves.json"))
FH = ROOT / "data/dynamics/emulation"
REGS = {r["name"]: r for r in json.load(open(ROOT / "data/dynamics/registers.json"))}

def emu(name, reg):
    z = np.load(FH / f"{name}_{reg}_chi600.npz")
    return z["times_us"], z["occ"]

def dyn(ax, reg, title, series):
    for name, lab, idx, col, ls, leg in series:
        t, o = emu(name, reg)
        ax.plot(t, o[:, idx].mean(1), ls, color=col, lw=1.5, alpha=0.9, zorder=3, label=leg)
        p = [x for x in HW.get(name, {}).get(reg, []) if lab in x["cls"]]
        if p:
            th = np.array([x["t_us"] for x in p])
            m = np.array([x["cls"][lab]["mean"] for x in p])
            lo = np.array([x["cls"][lab]["lo"] for x in p])
            hi = np.array([x["cls"][lab]["hi"] for x in p])
            ax.errorbar(th, m, yerr=[m - lo, hi - m], fmt="o", color=col, ms=4.6,
                        mfc=col if ls == "-" else "white", mec=col, mew=1.2, elinewidth=0.9, capsize=0, zorder=5)
    ax.set_xlim(0, 6.0 * 1.02); ax.set_xlabel("time (µs)", fontsize=12)
    ax.set_ylabel(r"$\langle n_i\rangle$", fontsize=13); ax.tick_params(labelsize=11)
    ax.set_title(title, fontsize=13, loc="left")
    [sp.set_visible(False) for sp in (ax.spines["top"], ax.spines["right"])]

figB = plt.figure(figsize=(7.15, 9.0))
gsB = figB.add_gridspec(3, 2, hspace=0.95, wspace=0.3)
AX = [[figB.add_subplot(gsB[r, 0]), figB.add_subplot(gsB[r, 1])] for r in range(3)]

# Folio
rf = REGS["folio_w60"]
redf = np.zeros(rf["N"], bool); redf[rf["red"]] = True
for c, reg in enumerate(("AFM", "FM")):
    dyn(AX[0][c], reg, "(a)" if c == 0 else "(b)", [
        ("folio_w60", "beside a space", np.where(redf)[0], RED, "-", "beside a space"),
        ("folio_w60", "inside a word", np.where(~redf)[0], INK, "-", "inside a word"),
    ])

# Mosaic
rm_ = REGS["mosaic_marseille"]
red_m = np.zeros(rm_["N"], bool); red_m[rm_["red"]] = True
blk_m = np.zeros(rm_["N"], bool); blk_m[rm_["black"]] = True
for c, reg in enumerate(("AFM", "FM")):
    dyn(AX[1][c], reg, "(c)" if c == 0 else "(d)", [
        ("mosaic_marseille", "course terminations", np.where(red_m)[0], RED, "-", "course terminations"),
        ("mosaic_marseille", "figure tesserae", np.where(blk_m)[0], INK, "--", "figure (black)"),
        ("mosaic_marseille", "plain courses", np.where(~red_m & ~blk_m)[0], GREY, "-", "plain courses"),
    ])

# Die-link
d = json.load(open(ROOT / "data/die/as_run_56.json"))
Pd = np.array(d["positions"]); A = np.array(d["adj"])
Ed = [(i, j) for i in range(len(A)) for j in range(i + 1, len(A)) if A[i, j]]
degd = np.zeros(len(Pd), int)
for u, v in Ed:
    degd[u] += 1; degd[v] += 1
iso, end, mid = degd == 0, degd == 1, degd == 2
for c, reg in enumerate(("AFM", "FM")):
    dyn(AX[2][c], reg, "(e)" if c == 0 else "(f)", [
        ("dielink", "end of a chain", np.where(end)[0], RED, "-", "chain end"),
        ("dielink", "inside a chain", np.where(mid)[0], INK, "-", "chain interior"),
        ("dielink", "isolated", np.where(iso)[0], GREY, ":", "isolated"),
    ])

for r_, (la, lb) in ((0, ("(a)", "(b)")), (1, ("(c)", "(d)")), (2, ("(e)", "(f)"))):
    AX[r_][0].set_title(la, fontsize=13, fontweight="bold", loc="left")
    AX[r_][1].set_title(lb, fontsize=13, fontweight="bold", loc="left")
    h_, l_ = AX[r_][0].get_legend_handles_labels()
    h_ = [Line2D([], [], color=h.get_color(), ls=h.get_linestyle(), lw=1.5, marker="o", ms=5,
                 mfc=h.get_color() if h.get_linestyle() == "-" else "white", mec=h.get_color()) for h in h_]
    AX[r_][0].legend(h_, l_, loc="upper center", bbox_to_anchor=(1.15, -0.27), ncol=len(l_), frameon=False, fontsize=11, columnspacing=1.0, handlelength=2.0)
AX[0][0].annotate("AFM drive", xy=(0.5, 1.12), xycoords="axes fraction", ha="center", fontsize=13, color=INK)
AX[0][1].annotate("FM-like drive", xy=(0.5, 1.12), xycoords="axes fraction", ha="center", fontsize=13, color=INK)
figB.legend([Line2D([], [], color=NEUTRAL, lw=1.5), Line2D([], [], color=NEUTRAL, ls="none", marker="o", ms=5)],
            ["emulation ($\\chi=600$)", "Ruby, 1000 shots"],
            loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=2, frameon=False, fontsize=11.5)
out = Path(sys.argv[sys.argv.index('-o') + 1]) if '-o' in sys.argv else (HERE / "fig4.png")
figB.savefig(out, dpi=200, bbox_inches="tight")
print("saved", out)
