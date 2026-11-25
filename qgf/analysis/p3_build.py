# NOTE: this is the original pair-selection script, kept for the record.
# The twelve matched pairs and the test results are in data/p3_river/.
# The script cannot be rerun from this deposit: it needs the full Folio window bank and a helper that is not included.
"""P3 builder (PREREG_P3_RIVER_20261104.md): 12 matched split/whole pairs of 10x12 Folio blocks (95 atoms nominal) + the 3 bridge 6x10
pairs of river_regs.json. A split block is one cut by an EMPTY LINE into a top and a bottom component (the census found no block split by a
vertical river over 10 lines); cuts are therefore horizontal line boundaries, for the whole block the pseudo-cut is the line boundary whose
straddling-pair count is closest to the partner's. Deterministic selection as registered. Writes p3_regs.json (registers, cut, straddling pairs) and
qgf_p3_river.json (120 rows: FM 2/4/6 us + AFM 6 us per block, drives from each block's couplings, caps asserted). Nothing is re-cut later."""
import os, sys, json, subprocess, collections, numpy as np
Q = os.path.expanduser("~/code/qgf_humanities"); sys.path.insert(0, Q + "/g2_20261010"); from qgf_seq import couplings, regime_params
AMP_CAP, DET_CAP = 15.708, 62.8319
os.chdir(Q + "/folio"); pages = sorted({json.loads(l)["ident"] for l in open("runpod_bundle/f1_windows.jsonl")})
def comps(P, pitch=6.5):
    N = len(P); D = np.linalg.norm(P[:, None] - P[None], axis=-1); A = (D > 0) & (D <= pitch * 1.05); lab = -np.ones(N, int); k = 0
    for i in range(N):
        if lab[i] >= 0: continue
        st = [i]; lab[i] = k
        while st:
            u = st.pop()
            for v in np.where(A[u])[0]:
                if lab[v] < 0: lab[v] = k; st.append(v)
        k += 1
    return lab, sorted(collections.Counter(lab.tolist()).values(), reverse=True), A, D
def feats(P, A, D):
    R = D / 6.5; np.fill_diagonal(R, np.inf); F6 = (R ** -6).sum(1); deg = A.sum(1); return np.array([F6.mean(), F6.std(), (deg <= 2).mean()])
B = []
for p in pages:
    out = subprocess.run([sys.executable, "folio_windows.py", f"lat_{p.split()[-1]}_lattice.json", p, "--rows", "10", "--cols", "12", "--stride", "2", "--rnn", "6.5", "--disp_clip", "0", "--min_atoms", "80", "--max_vac_frac", "0.35"], capture_output=True, text=True).stdout
    for l in out.splitlines():
        w = json.loads(l); P = np.array(w["coords_um"], float); P -= P.mean(0); lab, sizes, A, D = comps(P); N = len(P)
        Dm = D.copy(); np.fill_diagonal(Dm, np.inf)
        if Dm.min() < 5.0 or np.linalg.norm(P, axis=1).max() > 50: continue
        split = len([s_ for s_ in sizes if s_ >= 15]) == 2 and sizes[0] + sizes[1] >= 0.9 * N and (len(sizes) < 3 or sizes[2] < 15)
        if split:   # registered rule: the two components are one entirely above the other with at least one EMPTY LINE between (gap >= 2 line pitches)
            big = [c for c, _ in collections.Counter(lab.tolist()).most_common(2)]; ly = np.array([n["line"] for n in w["nodes"]])
            a, b = ly[lab == big[0]], ly[lab == big[1]]; split = bool(a.max() + 1 < b.min() or b.max() + 1 < a.min())
        if split:   # registered rule: the two components must be one entirely above the other (an empty line), else the block is not used
            big = [c for c, _ in collections.Counter(lab.tolist()).most_common(2)]; ly = np.array([n["line"] for n in w["nodes"]])
            a, b = ly[lab == big[0]], ly[lab == big[1]]; split = bool(a.max() < b.min() or b.max() < a.min())
        whole = sizes[0] >= 0.97 * N
        if not (split or whole): continue
        B.append(dict(ident=p, id=w["id"], N=N, vac=w.get("n_vacancies", 0), split=bool(split), P=P, lab=lab, sizes=sizes, f=feats(P, A, D), nodes=w["nodes"]))
S = [b for b in B if b["split"]]; W = [b for b in B if not b["split"]]; pairs = []; used = set()
for s in sorted(S, key=lambda b: (b["ident"], b["id"])):
    cand = [w for w in W if w["ident"] == s["ident"] and abs(w["N"] - s["N"]) <= 2 and abs(w["vac"] - s["vac"]) <= 2 and (w["ident"], w["id"]) not in used]
    if not cand: continue
    w = min(cand, key=lambda w: np.linalg.norm((w["f"] - s["f"]) / 0.1)); used.add((w["ident"], w["id"])); pairs.append((s, w))
pairs.sort(key=lambda sw: (abs(sw[0]["N"] - 95) + abs(sw[1]["N"] - 95), sw[0]["ident"], sw[0]["id"])); pick = []; perpage = collections.Counter()
for s, w in pairs:
    if perpage[s["ident"]] >= 2: continue
    pick.append((s, w)); perpage[s["ident"]] += 1
    if len(pick) == 12: break
def slots(b): return np.array([[n["slot"], n["line"]] for n in b["nodes"]], float)
def straddle(b, side):
    S_ = slots(b); A_ = []
    for i in range(len(S_)):
        for j in range(i + 1, len(S_)):
            if 2 <= abs(S_[i, 0] - S_[j, 0]) + abs(S_[i, 1] - S_[j, 1]) <= 3 and side[i] >= 0 and side[j] >= 0 and side[i] != side[j]: A_.append((i, j))
    return A_
regs = []
def add(name, b, cut, side, pair, role):
    P = b["P"]; J, jnn, dinf = couplings(P); r = dict(name=name, pair=pair, role=role, page=b["ident"], win=b["id"], N=int(b["N"]), pitch_um=6.5, J_NN=float(jnn), delta_inf=float(dinf),
        coords_um=P.round(4).tolist(), nodes=b["nodes"], comp=[int(x) for x in b["lab"]], sizes=b["sizes"][:3], cut=cut, side=[int(x) for x in side], straddling=straddle(b, side), regimes={})
    for reg in ("AFM", "FM"):
        p = regime_params(P, reg); p = {k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in p.items()}
        assert p["omega"] <= AMP_CAP and abs(p["delta"]) <= DET_CAP, (name, reg, p); r["regimes"][reg] = p
    regs.append(r); return r
for k, (s, w) in enumerate(pick):
    big = [c for c, _ in collections.Counter(s["lab"].tolist()).most_common(2)]; side_s = np.where(s["lab"] == big[0], 0, np.where(s["lab"] == big[1], 1, -1))   # stray atoms (< 15, <= 10 %) are on no side
    ys = slots(s)[:, 1]; top = 0 if ys[side_s == 0].mean() < ys[side_s == 1].mean() else 1; cut_s = float((ys[side_s == top].max() + ys[side_s == 1 - top].min()) / 2)
    assert ys[side_s == top].max() + 1 < ys[side_s == 1 - top].min(), ("not an empty-line split", s["ident"], s["id"])
    rs = add(f"p3_pair{k:02d}_split", s, cut_s, side_s, k, "split"); n_s = len(rs["straddling"])
    yw = slots(w)[:, 1]; lines = sorted(set(yw)); best = min(((c0 + c1) / 2 for c0, c1 in zip(lines[:-1], lines[1:])), key=lambda c: abs(len(straddle(w, (yw > c).astype(int))) - n_s))
    rw = add(f"p3_pair{k:02d}_whole", w, float(best), (yw > best).astype(int), k, "whole")
    print(f"pair {k:2d} {s['ident']:12s} split win {s['id']:3d} N {s['N']} sizes {s['sizes'][:2]} straddling {n_s:3d} | whole win {w['id']:3d} N {w['N']} straddling {len(rw['straddling']):3d} | FM de {rs['regimes']['FM']['delta']:.2f}/{rw['regimes']['FM']['delta']:.2f}")
# bridge: the three 6x10 pairs already emulated
for r in json.load(open(Q + "/ruby_decisive/river/river_regs.json")):
    b = dict(ident=r["page"], id=r["win"], N=r["N"], P=np.array(r["coords_um"]), lab=np.array(r["comp"]), sizes=r["sizes"], nodes=r["nodes"])
    k = int(r["name"][4]); ys = slots(b)[:, 1]
    if r["name"].endswith("split"):
        big = [c for c, _ in collections.Counter(b["lab"].tolist()).most_common(2)]; side = np.where(b["lab"] == big[0], 0, np.where(b["lab"] == big[1], 1, -1))
        top = 0 if ys[side == 0].mean() < ys[side == 1].mean() else 1; cut = float((ys[side == top].max() + ys[side == 1 - top].min()) / 2)
        if not ys[side == top].max() < ys[side == 1 - top].min(): print("bridge", k, "split is not a clean horizontal cut; kept with component sides, cut =", cut)
        add(f"p3_bridge{k}_split", b, cut, side, 100 + k, "bridge_split")
    else:
        n_s = len([x for x in regs if x["name"] == f"p3_bridge{k}_split"][0]["straddling"]); lines = sorted(set(ys))
        best = min(((c0 + c1) / 2 for c0, c1 in zip(lines[:-1], lines[1:])), key=lambda c: abs(len(straddle(b, (ys > c).astype(int))) - n_s))
        add(f"p3_bridge{k}_whole", b, float(best), (ys > best).astype(int), 100 + k, "bridge_whole")
rows = []
for r in regs:
    for reg, t in (("FM", 2000), ("FM", 4000), ("FM", 6000), ("AFM", 6000)):
        p = r["regimes"][reg]; rows.append(dict(k=len(rows), register=r["name"], setting=reg, t_ns=t, omega=p["omega"], delta=p["delta"], J_NN=r["J_NN"], delta_inf=r["delta_inf"], N=r["N"], pitch_um=6.5, coords=r["coords_um"], cut=r["cut"], side=r["side"]))
out = Q + "/ruby_decisive/p3_river/"; json.dump(regs, open(out + "p3_regs.json", "w")); json.dump(rows, open(out + "qgf_p3_river.json", "w"))
print("registers", len(regs), "rows", len(rows), "candidate pairs", len(pairs), "split blocks", len(S), "whole", len(W))
