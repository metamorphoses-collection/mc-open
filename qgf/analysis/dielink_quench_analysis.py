from pathlib import Path
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DIE = ROOT / 'data/die'
# PREFLIGHT-EXEMPT: read-only scoring of saved Ruby result files against the emulated die-link quench; builds and submits nothing.
"""PREREG_DIELINK_20261101, rules Q1/Q2 + diagnostic. Frozen before hardware data.
Usage: python3 dielink_quench_analysis.py results_ruby_dielink/ruby_diag_job_329.json results_ruby_dielink/ruby_diag_job_330.json
Emulator files: runpod_dielink/out/dielink_<AFM|FM>_chi<300|600>.npz (occ[t,i], cm[t,i,j], times). Comparison at the last readout
(1640 ns): chi600 if converged by the paper criterion (mean|dn|<0.005, mean|dC| over the 30 edges <0.002), else chi600 flagged unconverged."""
import json, sys, os, collections, numpy as np
from scipy.stats import spearmanr
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(str(DIE / "qgf_dielink_a.json"))); A = np.array(R["adj"]); N = len(A)
E = [(i, j) for i in range(N) for j in range(i + 1, N) if A[i, j]]; deg = A.sum(1); rows = {r["k"]: r for r in json.load(open(str(DIE / "qgf_dielink_quench.json")))}
grp = np.array([l.split("|")[0] for l in R["labels"]])
def emu(regime):
    o = {}
    for chi in (300, 600):
        f = os.path.join(H, "runpod_dielink", "out", f"dielink_{regime}_chi{chi}.npz")
        if os.path.exists(f): d = np.load(f); o[chi] = (d["occ"][-1], d["cm"][-1])
    if 300 in o and 600 in o:
        n3, c3 = o[300]; n6, c6 = o[600]; cc3 = c3 - np.outer(n3, n3); cc6 = c6 - np.outer(n6, n6)
        dn = float(np.mean(np.abs(n6 - n3))); dc = float(np.mean([abs(cc6[i, j] - cc3[i, j]) for i, j in E])); conv = dn < 0.005 and dc < 0.002
    else: dn = dc = None; conv = None
    chi = 600 if 600 in o else 300; n, c = o[chi]; return n, c - np.outer(n, n), dict(chi=chi, converged=conv, dn=dn, dC=dc)
def hw(f):
    d = json.load(open(f)); idx = [int(q[1:]) for q in d["qubit_order"]]; cnt = d["results"] if isinstance(d["results"], dict) else collections.Counter(d["results"])
    X = []; W = []
    for b, c in cnt.items():
        x = np.zeros(N); x[idx] = [int(ch) for ch in b]; X.append(x); W.append(c)
    X = np.array(X); W = np.array(W, float); p = W / W.sum(); n = p @ X; nn = (X.T * p) @ X; return d, X, W, n, nn - np.outer(n, n)
def boot(X, W, emu_n, emu_c, draws=2000, seed=1):
    rng = np.random.default_rng(seed); tot = int(W.sum()); pr = W / tot; r1 = []; r2 = []
    for _ in range(draws):
        k = rng.multinomial(tot, pr); p = k / tot; n = p @ X; c = (X.T * p) @ X - np.outer(n, n)
        r1.append(spearmanr(n, emu_n)[0]); r2.append(spearmanr([c[i, j] for i, j in E], [emu_c[i, j] for i, j in E])[0])
    return [float(np.percentile(r1, q)) for q in (2.5, 97.5)], [float(np.percentile(r2, q)) for q in (2.5, 97.5)]
out = {}; feats = {}
for f in sys.argv[1:]:
    d, X, W, n, C = hw(f); k = int(d["block"][-2:]); regime = rows[k]["setting"]; en, ec, meta = emu(regime)
    rho1 = float(spearmanr(n, en)[0]); rho2 = float(spearmanr([C[i, j] for i, j in E], [ec[i, j] for i, j in E])[0]); ci1, ci2 = boot(X, W, en, ec)
    out[regime] = dict(row=d["job_idx"], batch=d.get("batch_id"), shots=int(W.sum()), rho_one_body=round(rho1, 3), ci95=ci1, rho_two_body_edges=round(rho2, 3), ci95_two_body=ci2,
                       hw_mean_n=round(float(n.mean()), 4), emu_mean_n=round(float(en.mean()), 4), emulator=meta)
    feats[regime] = np.c_[n, (A * C).sum(1)]
# diagnostic: neighbour count from hardware features, leave-one-group-out ridge, vs F6
if feats:
    from sklearn.linear_model import Ridge
    P = np.array(R["positions"]); D = np.linalg.norm(P[:, None] - P[None], axis=-1); np.fill_diagonal(D, np.inf); F6 = ((5.6 / D) ** 6).sum(1)
    Xf = np.hstack(list(feats.values())); y = deg.astype(float); res = {}
    for name, Z in (("hardware", Xf), ("F6", F6[:, None])):
        err = []
        for g in np.unique(grp):
            tr = grp != g; m = Ridge(alpha=1.0).fit(Z[tr], y[tr]); err.extend(np.abs(m.predict(Z[~tr]) - y[~tr]))
        res[name] = round(float(np.mean(err)), 3)
    out["diagnostic_neighbour_MAE_LOGO"] = res
q1 = all(out[r]["rho_one_body"] >= 0.80 for r in ("AFM", "FM") if r in out) and len([r for r in ("AFM", "FM") if r in out]) == 2
out["verdict_Q1"] = "PASS" if q1 else "FAIL (or incomplete)"
out["Q2"] = {r: ("PASS" if out[r]["rho_two_body_edges"] >= 0.5 else "FAIL") for r in out if r in ("AFM", "FM")}
print(json.dumps(out, indent=1)); json.dump(out, open(str(DIE / "dielink_quench_result.json"), "w"), indent=1)
