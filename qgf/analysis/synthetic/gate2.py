"""SYN-1 gate 2 analysis (amendment 3, 29 Oct 2026). Paired antisymmetric design throughout (amendment 2). Families as gate1.py, with:
  RRWP to K = kmax (default 60); nan-safe quench features (the light-cone control leaves C_ij undefined beyond r);
  RESIDUAL: every quench feature regressed (least squares, unsupervised) on the LOCAL features, the residual scored (rule D);
  LIGHTCONE(r, Jt): the same quench features built from the r-truncated exact readings (lightcone_control.py), raw and residual (rule E).
Rules (fixed in the pre-registration):
  A local <= 0.65 (both learners)        B RRWP <= 0.60 for all K < L_min, >= 0.95 (LR) for some K > L_max
  C quench >= 0.90 at some Jt <= 150 and <= 0.65 at every Jt <= 2 (LR)      D residual >= 0.85 at some Jt <= 150 (LR)
  E residual light-cone features at every r <= R_E score <= 0.65 at every Jt <= 150 (LR): the parity is not readable within R_E hops
Usage: python3 gate2.py windows.jsonl quench.jsonl out.json [--lightcone lc.jsonl] [--kmax 60] [--RE 4]"""
import json, sys, argparse, numpy as np, networkx as nx
from gate1 import pooled, graph, local_feats, auroc, auroc_paired


def rrwp_feats(w, K):
    A = nx.to_numpy_array(graph(w), nodelist=range(w["N"])); M = A / np.maximum(A.sum(1), 1)[:, None]
    P = np.eye(w["N"]); out = []
    for _ in range(K):
        P = P @ M; out.append(pooled(np.diag(P)))
    return np.array(out)


def quench_feats(w, readout, dmax=6):
    sp = dict(nx.all_pairs_shortest_path_length(graph(w)))
    C = np.array(readout["C"], float); n = np.array(readout["n"], float); N = w["N"]
    byd = []
    for d in range(1, dmax + 1):
        vals = [C[i, j] for i in range(N) for j in range(i + 1, N) if sp[i].get(j) == d and np.isfinite(C[i, j])]
        byd.append(np.mean(vals) if vals else 0.0)
    iu = np.triu_indices(N, 1); cu = C[iu]; cu = cu[np.isfinite(cu)]
    return np.r_[pooled(n[np.isfinite(n)]), byd, pooled(cu) if len(cu) else np.zeros(4)]


def residual(XQ, XL):
    A = np.c_[np.ones(len(XL)), XL]; B, *_ = np.linalg.lstsq(A, XQ, rcond=None)
    return XQ - A @ B


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("windows"); ap.add_argument("quench"); ap.add_argument("out")
    ap.add_argument("--lightcone", default=None); ap.add_argument("--kmax", type=int, default=60); ap.add_argument("--RE", type=int, default=4)
    a = ap.parse_args()
    W = {w["id"]: w for w in (json.loads(l) for l in open(a.windows))}
    Q = {q["id"]: q for q in (json.loads(l) for l in open(a.quench))}
    ids = sorted(set(W) & set(Q)); y = np.array([W[i]["label"] for i in ids]); pairs = np.array([W[i]["pair"] for i in ids])
    keep = np.array([np.sum(pairs == p) == 2 for p in pairs]); ids = [i for i, k in zip(ids, keep) if k]
    y = np.array([W[i]["label"] for i in ids]); pairs = np.array([W[i]["pair"] for i in ids])
    A = lambda X, l="lr": auroc_paired(X, y, pairs, l)
    Lmin, Lmax = min(W[i]["L"] for i in ids), max(W[i]["L"] for i in ids)
    res = dict(n_windows=len(ids), n_pairs=int(len(ids) // 2), L_range=[Lmin, Lmax], N_range=[min(W[i]["N"] for i in ids), max(W[i]["N"] for i in ids)],
               max_norm_err=max(Q[i].get("norm_err", 0) for i in ids))
    XL = np.array([local_feats(W[i]) for i in ids]); res["local"] = dict(lr=A(XL, "lr"), gb=A(XL, "gb"))
    R = np.array([rrwp_feats(W[i], a.kmax) for i in ids])
    res["rrwp_by_K"] = {str(k + 1): dict(lr=A(R[:, k, :], "lr"), gb=A(R[:, k, :], "gb")) for k in range(a.kmax)}
    jts = [r["Jt"] for r in Q[ids[0]]["readouts"]]; res["quench_by_Jt"] = {}; res["residual_by_Jt"] = {}
    for ti, jt in enumerate(jts):
        XQ = np.array([quench_feats(W[i], Q[i]["readouts"][ti]) for i in ids])
        res["quench_by_Jt"][str(jt)] = dict(lr=A(XQ, "lr"), gb=A(XQ, "gb"))
        XR = residual(XQ, XL); res["residual_by_Jt"][str(jt)] = dict(lr=A(XR, "lr"), gb=A(XR, "gb"))
        print(f"Jt {jt:6.1f} quench {res['quench_by_Jt'][str(jt)]['lr']:.3f} residual {res['residual_by_Jt'][str(jt)]['lr']:.3f}", flush=True)
    if a.lightcone:
        LC = {}
        for l in open(a.lightcone):
            d = json.loads(l); LC.setdefault(d["r"], {})[d["id"]] = d
        res["lightcone"] = {}
        for r in sorted(LC):
            if not all(i in LC[r] for i in ids): print("lightcone r", r, "incomplete, skipped"); continue
            res["lightcone"][str(r)] = {}
            for ti, jt in enumerate(jts):
                XQ = np.array([quench_feats(W[i], LC[r][i]["readouts"][ti]) for i in ids]); XR = residual(XQ, XL)
                res["lightcone"][str(r)][str(jt)] = dict(lr=A(XQ, "lr"), res_lr=A(XR, "lr"), res_gb=A(XR, "gb"))
            print(f"r {r}: raw max {max(v['lr'] for v in res['lightcone'][str(r)].values()):.3f} residual max {max(v['res_lr'] for v in res['lightcone'][str(r)].values()):.3f}", flush=True)
    q = res["quench_by_Jt"]; rr = res["rrwp_by_K"]; rd = res["residual_by_Jt"]
    vals = dict(local_max=max(res["local"].values()),
                rrwp_K_lt_Lmin_max=max(max(v.values()) for k, v in rr.items() if int(k) < Lmin),
                rrwp_K_gt_Lmax_lr_max=max([v["lr"] for k, v in rr.items() if int(k) > Lmax] or [float("nan")]),
                quench_best_lr=max(v["lr"] for v in q.values()), quench_Jt_le2_max_lr=max(v["lr"] for k, v in q.items() if float(k) <= 2),
                residual_best_lr=max(v["lr"] for v in rd.values()))
    rules = dict(A_local_blind=vals["local_max"] <= 0.65, B_rrwp_range=vals["rrwp_K_lt_Lmin_max"] <= 0.60 and vals["rrwp_K_gt_Lmax_lr_max"] >= 0.95,
                 C_quench_sees_it=vals["quench_best_lr"] >= 0.90 and vals["quench_Jt_le2_max_lr"] <= 0.65, D_residual=vals["residual_best_lr"] >= 0.85)
    if a.lightcone and res.get("lightcone"):
        vals["lightcone_res_max_r_le_RE"] = max(v["res_lr"] for r, d in res["lightcone"].items() if int(r) <= a.RE for v in d.values())
        rules["E_not_local"] = vals["lightcone_res_max_r_le_RE"] <= 0.65
    rules["values"] = vals; rules["PASS"] = all(v for k, v in rules.items() if k != "values")
    res["rules"] = rules; json.dump(res, open(a.out, "w"), indent=1); print(json.dumps(rules, indent=1))


if __name__ == "__main__":
    main()
