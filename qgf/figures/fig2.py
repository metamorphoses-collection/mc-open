"""Figure 2: (a) emulated light cone over 240 Folio windows; (b) hardware light cone, four windows; (c) mean-square correlation across a filled line versus an empty line for twelve matched pairs, with the independent-atom interval."""
import json, numpy as np, networkx as nx, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from palette import EVENT, INK, NEUTRAL, LIGHT, SECOND, seq

def edges(w):
    return [tuple(e) if not isinstance(e, dict) else (e["u"], e["v"]) for e in w["edges"]]

W = {}
for l in (ROOT / "data/folio/windows.jsonl").read_text().splitlines():
    if l.strip():
        w = json.loads(l); W[w["id"]] = w
LC = json.load(open(ROOT / "data/lightcone/campaign.json"))
T4 = {r["win_id"]: r["shot_id_4000us"] for r in LC}
F = {r["id"]: r for r in json.load(open(ROOT / "data/lightcone/window_features.json"))}
AGG = json.load(open(ROOT / "data/lightcone/aggregate.json"))["aggregate"]
EL = json.load(open(ROOT / "data/empty_line/result.json"))
t = np.array(F[sorted(T4)[0]]["t_us"])

def cmat_from(row):
    d = json.load(open(ROOT / "data/lightcone/shots" / f"job_{row}.json"))
    keys = list(d["results"]); B = np.array([[int(c) for c in s_] for s_ in keys])
    wt = np.array([d["results"][s_] for s_ in keys], float)
    p = wt / wt.sum(); n = p @ B
    return (B.T * p) @ B - np.outer(n, n)

hw, em = {}, {}
for wid in sorted(T4):
    w = W[wid]; Nw = w["N"]
    G = nx.Graph(); G.add_nodes_from(range(Nw)); G.add_edges_from(edges(w))
    D = dict(nx.all_pairs_shortest_path_length(G))
    pairs = [(a_, b_) for a_ in range(Nw) for b_ in range(a_ + 1, Nw)]
    dist = np.array([D[a_].get(b_, -1) for a_, b_ in pairs])
    rows = {r["t_ns"]: r["shot_id"] for r in LC if r["win_id"] == wid}; rows[4000] = T4[wid]
    for tn, row in rows.items():
        C = cmat_from(row); hw.setdefault(tn, {d: [] for d in range(1, 7)})
        for d in range(1, 7):
            hw[tn][d].append(np.mean([abs(C[a_, b_]) for (a_, b_), dd in zip(pairs, dist) if dd == d]))
    Ca = np.abs(np.array(F[wid]["Cij_all"]))
    for d in range(1, 7):
        em.setdefault(d, []).append(Ca[:, dist == d].mean(1))

plt.rcParams.update({"font.size": 9})
fig = plt.figure(figsize=(7.02, 6.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1], hspace=0.38, wspace=0.3)
ax = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]
cm = seq(6)

dd = np.array(AGG["distances"])
th_med = np.array(AGG["t_half_median"])
q25 = np.array(AGG["t_half_q25"])
q75 = np.array(AGG["t_half_q75"])
slope, icpt = np.polyfit(dd, th_med, 1); speed = 1.0 / slope
a0 = ax[0]
a0.fill_between(dd, q25, q75, color=LIGHT, zorder=1, lw=0, label="middle half of the 240 windows")
a0.plot(dd, icpt + slope * dd, "-", color=INK, lw=1.0, zorder=2)
a0.scatter(dd, th_med, s=46, c=cm, edgecolors="k", linewidths=0.5, zorder=3, label="median curve")
a0.text(0.97, 0.06, f"front: {speed:.1f} letter slots per µs", transform=a0.transAxes, ha="right", va="bottom", fontsize=8.5, color=INK)
a0.set_xlabel("letter distance"); a0.set_ylabel("time to half-maximum $|C_{ij}|$ (µs)"); a0.set_title("(a)", fontsize=11, loc="left")
a0.set_xticks(dd); a0.set_ylim(0, None); a0.legend(fontsize=7.8, frameon=False, loc="upper left")
[sp.set_visible(False) for sp in (a0.spines["top"], a0.spines["right"])]
print("t_half median curves", np.round(th_med, 3), "IQR", np.round(q25, 2), np.round(q75, 2), "speed %.2f letters/us" % speed)

F_RO = (1 - 0.031 - 0.136) ** 2
for d, c in [(d_, cm[d_ - 1]) for d_ in (1, 3, 6)]:
    ax[1].plot(t, F_RO * np.mean(em[d], 0), color=c, lw=2)
    ax[1].scatter([tn / 1000 for tn in sorted(hw)], [np.mean(hw[tn][d]) for tn in sorted(hw)], color=c, s=42, edgecolors="black", linewidths=0.5, zorder=3)
ax[1].plot([], [], color=NEUTRAL, lw=2, label="emulator (incl. readout)"); ax[1].scatter([], [], color=NEUTRAL, s=42, edgecolors="black", linewidths=0.5, label="Ruby")
ax[1].set_xlabel("pulse length (µs)"); ax[1].set_ylabel(r"mean $|C_{ij}|$"); ax[1].set_title("(b)", fontsize=11, loc="left"); ax[1].legend(fontsize=8, loc="upper left", frameon=False)
ax[1].set_xlim(0, 4.2); ax[1].set_ylim(0, 0.084)
for d_, y_ in ((1, 0.066), (3, 0.033), (6, 0.0105)):
    ax[1].text(4.12, y_, f"{d_}", fontsize=8.5, color=cm[d_ - 1], va="center", ha="left")
ax[1].text(4.12, 0.071, "distance", fontsize=7.5, color=INK, ha="left", va="bottom")
[sp.set_visible(False) for sp in (ax[1].spines["top"], ax[1].spines["right"])]

a = ax[2]; pairs = EL["primary_FM_6000ns_pooled3"]["pairs"]; xs = np.arange(len(pairs))
pp = {r["pair"]: r for r in pairs}
null_lo = np.array([r["S_split_null_ci"][0] for r in pairs]); null_hi = np.array([r["S_split_null_ci"][1] for r in pairs])
a.fill_between(np.concatenate([[-0.5], xs + 0.5]), np.concatenate([null_lo, [null_lo[-1]]]), np.concatenate([null_hi, [null_hi[-1]]]), step="post", color=LIGHT, zorder=1, label="95% range for independent atoms")
Sw = np.array([pp[k]["S_whole"] for k in range(12)]); Ss = np.array([pp[k]["S_split"] for k in range(12)])
a.scatter(xs, Sw, marker="o", s=58, color=INK, edgecolors="k", linewidths=0.4, zorder=3, label="across a filled line (whole block)")
a.scatter(xs, Ss, marker="o", s=58, color=EVENT, edgecolors="k", linewidths=0.4, zorder=3, label="across an empty line (split block)")
mw, ms_ = np.median(Sw), np.median(Ss); xb = 11.75; rr = float(f"{mw / ms_:.2g}")
a.plot([xb - 0.08, xb, xb, xb - 0.08], [mw, mw, ms_, ms_], "-", color=INK, lw=1.0, clip_on=False)
a.text(xb + 0.1, np.sqrt(mw * 1e-5), f"medians\n≈{rr:.0f}×\napart", fontsize=8.3, va="center", ha="left", color=INK, clip_on=False)
a.set_yscale("symlog", linthresh=1e-5, linscale=0.6); a.set_ylim(-1.6e-5, 5e-3); a.set_xlim(-0.6, 11.55)
a.set_xticks(xs); a.set_xticklabels([str(k + 1) for k in xs])
a.set_xlabel("block pair (92–97-atom Folio blocks)")
a.set_ylabel(r"$S_{\rm across}$"); a.set_title("(c)", fontsize=11, loc="left")
[sp.set_visible(False) for sp in (a.spines["top"], a.spines["right"])]
a.legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, frameon=False, columnspacing=1.0, handletextpad=0.3)
print("median S whole %.2e split %.2e ratio %.0f" % (mw, ms_, mw / ms_))
out = Path(sys.argv[sys.argv.index('-o') + 1]) if '-o' in sys.argv else (HERE / "fig2.png")
plt.savefig(out, dpi=220, bbox_inches="tight"); print("saved", out)
