# PREFLIGHT-EXEMPT: figure script; reads saved results and register coordinates only, submits nothing.
"""Fig. 3: the press state of nine copies, from the derived contrasts and window loci in data/ninecopy/."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from palette import EVENT, INK, NEUTRAL, LIGHT, SECOND, seq

R = json.load(open(ROOT / "data/ninecopy/fig3_contrasts.json"))
P = R["primary_6000ns_locus2_2000shots"]
S = R["secondary"]
order_labels = ["MC-C-109", "Prague", "London BL", "Lyon", "Madrid UCM", "Munich BSB", "Rome Aless.", "Rome BNC", "Vienna ONB"]
# preserve the published sort: P1 first, then original copy-name order
col_of = {c["label"]: (EVENT if c["state"] == "P1" else NEUTRAL) for c in P["copies"]}
# published order from sorting (state != P1, original long name)
names = [n for n in order_labels]
col = [col_of[n] for n in names]
xs = np.arange(9)

REG = {r["label"]: r for r in json.load(open(ROOT / "data/ninecopy/fig3_registers.json"))}
def f6c(r, key):
    X = np.array(r["coords_um"]) / float(r["pitch_um"])
    D = np.linalg.norm(X[:, None] - X[None], axis=-1); np.fill_diagonal(D, np.inf)
    f = (D ** -6.0).sum(1); L = np.zeros(len(X), bool); L[r[key]] = True
    return float(f[L].mean() - f[~L].mean())
F2 = np.array([f6c(REG[n], "locus2") for n in names])
F5 = np.array([f6c(REG[n], "locus31") for n in names])

def vals(block):
    d = {c["label"]: c for c in block["copies"]}
    v = np.array([d[n]["contrast"] for n in names])
    return v, np.array([d[n]["lo"] for n in names]), np.array([d[n]["hi"] for n in names])

def frame(a, title, ylab):
    a.axhline(0, color="#999999", lw=0.8, ls="--", zorder=0); a.axvline(1.5, color=LIGHT, lw=0.9, zorder=0)
    a.set_xticks(xs); a.set_xticklabels(names, rotation=90, fontsize=8.5)
    a.set_title(title, loc="left", fontsize=11); a.set_ylabel(ylab, fontsize=9); a.tick_params(axis="y", labelsize=8.5)
    [sp.set_visible(False) for sp in (a.spines["top"], a.spines["right"])]

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 3, figsize=(7.41, 3.45))
a = ax[0]; v, lo, hi = vals(P); v4, lo4, hi4 = vals(S["4000ns_locus2_2000shots"])
a.errorbar(xs - 0.14, v, yerr=[v - lo, hi - v], fmt="none", ecolor="k", elinewidth=0.9, capsize=2.2, zorder=2)
a.scatter(xs - 0.14, v, s=52, c=col, edgecolors="k", linewidths=0.5, zorder=3)
for blk, mk in ((S["6000ns_locus2_pass1_1000shots"], "^"), (S["6000ns_locus2_pass2_1000shots"], "v")):
    pv, _, _ = vals(blk); a.scatter(xs - 0.14, pv, marker=mk, s=18, color="w", edgecolors="k", linewidths=0.5, zorder=4)
a.errorbar(xs + 0.2, v4, yerr=[v4 - lo4, hi4 - v4], fmt="none", ecolor="#555555", elinewidth=0.8, capsize=1.8, zorder=2)
a.scatter(xs + 0.2, v4, marker="s", s=26, facecolors="white", edgecolors=col, linewidths=1.2, zorder=3)
frame(a, "(a)", "two-atom contrast")
a = ax[1]; v5, lo5, hi5 = vals(S["6000ns_locus31_2000shots"])
a.errorbar(xs, v5, yerr=[v5 - lo5, hi5 - v5], fmt="none", ecolor="k", elinewidth=0.9, capsize=2.2, zorder=2)
a.scatter(xs, v5, s=52, c=col, edgecolors="k", linewidths=0.5, zorder=3)
frame(a, "(b)", "five-atom contrast, 6 µs")
a = ax[2]
a.scatter(xs, F2, marker="D", s=34, c=col, edgecolors="k", linewidths=0.5, zorder=3)
a.scatter(xs, F5, marker="D", s=30, facecolors="white", edgecolors=col, linewidths=1.2, zorder=3)
frame(a, "(c)", r"$F_6$ contrast (classical sum)")
fig.legend([Line2D([], [], ls="none", marker="o", ms=7, mfc=EVENT, mec="k"), Line2D([], [], ls="none", marker="o", ms=7, mfc=NEUTRAL, mec="k"),
            Line2D([], [], ls="none", marker="o", ms=6, mfc="w", mec="k"), Line2D([], [], ls="none", marker="^", ms=5, mfc="w", mec="k"),
            Line2D([], [], ls="none", marker="s", ms=5, mfc="w", mec="k"), Line2D([], [], ls="none", marker="D", ms=5.5, mfc="k", mec="k"),
            Line2D([], [], ls="none", marker="D", ms=5.5, mfc="w", mec="k")],
           ["uncorrected (P$^1$)", "corrected (P$^2$)", "6 µs, 2000 shots", "one 1000-shot pass", "4 µs, 2000 shots",
            "$F_6$, two-atom locus", "$F_6$, five-atom locus"],
           fontsize=8.3, loc="lower center", bbox_to_anchor=(0.5, -0.135), ncol=4, frameon=False, columnspacing=1.1, handletextpad=0.3)
plt.tight_layout()
out = HERE / "fig3_nine_copies.png"
plt.savefig(out, dpi=220, bbox_inches="tight")
print("saved", out, "F6 two-atom", dict(zip(names, np.round(F2, 3))), "five-atom", dict(zip(names, np.round(F5, 3))))
