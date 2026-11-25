"""Residual agreement between hardware and emulator after a classical rate model is subtracted, on 24 Folio windows at 4 µs. The rate model is fit on the complementary windows. The statistic is the Spearman correlation of the residual hardware and residual emulator occupations."""
import os, sys, json, numpy as np
from pathlib import Path
from scipy.stats import spearmanr, binomtest
from sklearn.ensemble import GradientBoostingRegressor
ROOT = Path(__file__).resolve().parents[1]
C6 = 865723.0; A = 6.5; rng = np.random.default_rng(5)
W = {}
for l in (ROOT / "data/folio/windows.jsonl").read_text().splitlines():
    if l.strip():
        w = json.loads(l); W[w["id"]] = w
_CII = {int(k) if str(k).isdigit() else k: v for k, v in json.load(open(ROOT / "data/folio/occupations_final.json")).items()}
M = {(m["idx"], m["regime"]): m for m in map(json.loads, (ROOT / "data/folio/pulse_parameters.jsonl").read_text().splitlines()) if m}
def edges(w): return [(e["u"], e["v"]) if isinstance(e, dict) else tuple(e) for e in w["edges"]]
def zs(x): x = np.asarray(x, float); return (x - x.mean()) / (x.std() + 1e-12)
def rate_model(w, regime, g_rel, T=4.0, dt=0.02, traj=200, seed=0):
    m = M[(w["id"], regime)]; P = np.array(w["coords_um"], float); D = np.linalg.norm(P[:, None] - P[None], axis=-1); np.fill_diagonal(D, np.inf)
    V = C6 / D ** 6; Om, de = m["omega"], m["delta"]; g = g_rel * Om; r = np.random.default_rng(seed); n = np.zeros((traj, len(P)))
    for _ in range(int(round(T / dt))):
        Dl = de - n @ V; G = Om ** 2 * g / (g ** 2 + 4 * Dl ** 2); n = np.where(r.random(n.shape) < 1 - np.exp(-G * dt), 1 - n, n)
    return n.mean(0)
def feats(w, rate):
    P = np.array(w["coords_um"], float); D = np.linalg.norm(P[:, None] - P[None], axis=-1) / A; np.fill_diagonal(D, np.inf)
    deg = np.zeros(w["N"]); [deg.__setitem__(u, deg[u] + 1) or deg.__setitem__(v, deg[v] + 1) for u, v in edges(w)]
    diag = (np.abs(D - np.sqrt(2)) < 0.05).sum(1); two = (np.abs(D - 2) < 0.05).sum(1)
    q = (P - P.min(0)) / A; ext = q.max(0); edge = np.minimum(q, ext - q).min(1)
    f6 = (D ** -6.0).sum(1); f12 = (D ** -12.0).sum(1); f18 = (D ** -18.0).sum(1)
    return np.c_[f6, f12, f18, f6 ** 2, deg, diag, two, edge, np.full(w["N"], w["N"]), np.full(w["N"], w["n_vacancies"]), zs(rate)]
def emu_final(wid, regime): return np.array(_CII[wid][regime])
def from_counts(c):
    keys = list(c); B = np.array([[int(ch) for ch in s] for s in keys]); v = np.array([c[s] for s in keys], float); return (B * v[:, None]).sum(0) / v.sum()
def main(mode):
    if mode == "test":
        rows = json.load(open(ROOT / "data/residual_test/windows.json")); rdir = str(ROOT / "data/residual_test/shots"); row_of = lambda r: r["shot_id"]
    else:
        raise SystemExit("usage: python analysis/residual_agreement.py")
    test_ids = {r["win_id"] for r in rows}; train = [w for wid, w in W.items() if wid not in test_ids and wid in _CII]
    report = {"mode": mode}
    for regime in ("FM", "AFM"):
        best = None
        for g_rel in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0):
            rho = np.median([spearmanr(rate_model(w, regime, g_rel), emu_final(w["id"], regime))[0] for w in train[::6]])
            if best is None or rho > best[1]: best = (g_rel, rho)
        g_rel = best[0]
        Xtr = np.concatenate([feats(w, rate_model(w, regime, g_rel)) for w in train]); ytr = np.concatenate([zs(emu_final(w["id"], regime)) for w in train])
        gb = GradientBoostingRegressor(n_estimators=400, max_depth=3, learning_rate=0.05, subsample=0.8, random_state=0).fit(Xtr, ytr)
        res = []
        for r in [r for r in rows if r["setting"] == regime]:
            w = W[r["win_id"]]; d = json.load(open(f"{rdir}/job_{row_of(r)}.json")); assert d["job_idx"] == row_of(r) and d["n_atoms"] == w["N"]
            h = from_counts(d["results"]); e = emu_final(w["id"], regime); ghat = gb.predict(feats(w, rate_model(w, regime, g_rel)))
            res.append(dict(win=w["id"], N=w["N"], rh=zs(h) - ghat, re=zs(e) - ghat, skill=float(spearmanr(ghat, e)[0]), raw=float(spearmanr(h, e)[0])))
        rho = np.array([spearmanr(x["rh"], x["re"])[0] for x in res]); med = float(np.median(rho)); pos = int((rho > 0).sum()); n = len(rho)
        null = np.array([np.median([spearmanr(rng.permutation(x["rh"]), x["re"])[0] for x in res]) for _ in range(2000)]); p_perm = float(np.mean(null >= med))
        order = rng.permutation(n); sanity = float(np.median([spearmanr(res[i]["rh"][:min(len(res[i]["rh"]), len(res[j]["re"]))], res[j]["re"][:min(len(res[i]["rh"]), len(res[j]["re"]))])[0] for i, j in zip(range(n), order) if i != j]))
        ok = med >= 0.30 and pos >= int(np.ceil(19 / 24 * n)) and p_perm < 0.01 and (med - sanity) >= 0.25
        report[regime] = dict(g_rel=g_rel, rate_rho_train=float(best[1]), classical_skill_median=float(np.median([x["skill"] for x in res])), raw_hw_emu_median=float(np.median([x["raw"] for x in res])),
                              residual_rho=rho.round(3).tolist(), median=med, positive=f"{pos}/{n}", sign_p=float(binomtest(pos, n, 0.5, alternative="greater").pvalue), perm_p=p_perm,
                              sanity_mismatched_median=sanity, PASS=bool(ok))
        print(f"{mode} {regime}: rate g={g_rel}Om (train rho {best[1]:.2f}); classical skill on test {report[regime]['classical_skill_median']:.2f}; raw hw-emu {report[regime]['raw_hw_emu_median']:.2f}; "
              f"residual rho median {med:+.2f}, positive {pos}/{n}, perm p {p_perm:.4f}, sanity {sanity:+.2f} -> {'PASS' if ok else 'fail'}", flush=True)
    out = ROOT / "data/residual_test/result.json"; json.dump(report, open(out, "w"), indent=1); print("wrote", out)
if __name__ == "__main__": main("test")
