"""SYN-1 gate 1: can the quench see the cycle parity where local features cannot, and at what Jt? (pre-registered, 29 Oct 2026)

Feature families, each scored by AUROC under 5-fold stratified CV x 3 repeats (logistic regression, standardised; GradientBoosting
as a second learner for the classical families so a non-linear learner gets its chance):
  LOCAL  : pooled (mean, std, min, max) per-site degree, F6 = sum r^-6, F12 = sum r^-12, plus pendant fraction k/N.
  RRWP-K : pooled diagonal return probabilities of the degree-normalised random walk at step K, K = 1..20, scored per K.
  QUENCH : per readout Jt, pooled <n_i> stats + mean C_ij at graph distance d = 1..6 (ring metric: shortest path) + all-pair C stats.
  SHORT  : the quench features at Jt <= 2 regressed on F6/F12 (the paper's short-time lemma, sanity).
Pass rules are in PREREG_SYN1_CYCLE_PARITY_20261029.md and printed here. Usage: python3 gate1.py windows.jsonl quench.jsonl out.json
"""
import json, sys, numpy as np, networkx as nx
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

CV = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=0)


def pooled(M):
    M = np.asarray(M, float)
    if M.ndim == 1:
        M = M[:, None]
    return np.r_[M.mean(0), M.std(0), M.min(0), M.max(0)]


def graph(w):
    G = nx.Graph(); G.add_nodes_from(range(w["N"])); G.add_edges_from([tuple(e) for e in w["edges"]]); return G


def local_feats(w):
    X = np.array(w["coords"], float); D = np.linalg.norm(X[:, None] - X[None], axis=-1); np.fill_diagonal(D, np.inf)
    deg = np.array([d for _, d in sorted(graph(w).degree())], float)
    return np.r_[pooled(np.c_[deg, (D ** -6).sum(1), (D ** -12).sum(1)]), w["k"] / w["N"]]


def rrwp_feats(w, K=20):
    A = nx.to_numpy_array(graph(w), nodelist=range(w["N"])); M = A / np.maximum(A.sum(1), 1)[:, None]
    P = np.eye(w["N"]); out = []
    for _ in range(K):
        P = P @ M; out.append(pooled(np.diag(P)))
    return np.array(out)                                   # K x 4


def quench_feats(w, readout, dmax=6):
    G = graph(w); sp = dict(nx.all_pairs_shortest_path_length(G))
    C = np.array(readout["C"]); n = np.array(readout["n"]); N = w["N"]
    byd = []
    for d in range(1, dmax + 1):
        vals = [C[i, j] for i in range(N) for j in range(i + 1, N) if sp[i].get(j) == d]
        byd.append(np.mean(vals) if vals else 0.0)
    iu = np.triu_indices(N, 1)
    return np.r_[pooled(n), byd, pooled(C[iu])]


def auroc(X, y, learner="lr"):
    X = np.asarray(X, float)
    if np.allclose(X.std(0), 0):
        return 0.5                                          # constant features: chance by definition
    if learner == "lr":
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
    else:
        m = GradientBoostingClassifier(n_estimators=100, max_depth=2, random_state=0)
    return float(cross_val_score(m, X, y, cv=CV, scoring="roc_auc").mean())


def auroc_paired(X, y, pairs, learner="lr"):
    """Amendment 2: antisymmetric paired design. For each pair, (x_odd - x_even, 1) and (x_even - x_odd, 0); GroupKFold by pair."""
    from sklearn.model_selection import GroupKFold
    X = np.asarray(X, float); y = np.asarray(y); pairs = np.asarray(pairs)
    D, yy, g = [], [], []
    for pr in np.unique(pairs):
        ii = np.where(pairs == pr)[0]
        if len(ii) != 2 or y[ii].sum() != 1:
            continue
        o, e = ii[y[ii] == 1][0], ii[y[ii] == 0][0]
        D += [X[o] - X[e], X[e] - X[o]]; yy += [1, 0]; g += [pr, pr]
    D, yy, g = np.array(D), np.array(yy), np.array(g)
    if np.allclose(D.std(0), 0):
        return 0.5
    if learner == "lr":
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0, fit_intercept=False))
    else:
        m = GradientBoostingClassifier(n_estimators=100, max_depth=2, random_state=0)
    scores = []
    for rep in range(3):
        rng = np.random.RandomState(rep); perm = rng.permutation(np.unique(g)); gmap = {p: i for i, p in enumerate(perm)}
        gg = np.array([gmap[x] for x in g])
        scores.append(cross_val_score(m, D, yy, cv=GroupKFold(n_splits=5), groups=gg, scoring="roc_auc").mean())
    return float(np.mean(scores))


def main():
    W = {w["id"]: w for w in (json.loads(l) for l in open(sys.argv[1]))}
    Q = {q["id"]: q for q in (json.loads(l) for l in open(sys.argv[2]))}
    ids = sorted(set(W) & set(Q)); y = np.array([W[i]["label"] for i in ids])
    res = dict(n_windows=len(ids), n_pos=int(y.sum()), max_norm_err=max(Q[i]["norm_err"] for i in ids))
    pairs = np.array([W[i].get("pair", -1) for i in ids]); paired = bool((pairs >= 0).all())
    res["design"] = "paired (amendment 2)" if paired else "unpaired"
    A = (lambda X, l="lr": auroc_paired(X, y, pairs, l)) if paired else (lambda X, l="lr": auroc(X, y, l))

    XL = np.array([local_feats(W[i]) for i in ids])
    res["local"] = dict(lr=A(XL, "lr"), gb=A(XL, "gb"))
    res["local_unpaired"] = dict(lr=auroc(XL, y, "lr"), gb=auroc(XL, y, "gb"))

    R = np.array([rrwp_feats(W[i]) for i in ids])          # n x K x 4
    res["rrwp_by_K"] = {str(k + 1): dict(lr=A(R[:, k, :], "lr"), gb=A(R[:, k, :], "gb")) for k in range(R.shape[1])}
    res["rrwp_all_K"] = dict(lr=A(R.reshape(len(ids), -1), "lr"), gb=A(R.reshape(len(ids), -1), "gb"))

    jts = [r["Jt"] for r in Q[ids[0]]["readouts"]]
    res["quench_by_Jt"] = {}
    for ti, jt in enumerate(jts):
        XQ = np.array([quench_feats(W[i], Q[i]["readouts"][ti]) for i in ids])
        res["quench_by_Jt"][str(jt)] = dict(lr=A(XQ, "lr"), gb=A(XQ, "gb"), lr_plus_local=A(np.c_[XQ, XL], "lr"),
                                            lr_unpaired=auroc(XQ, y, "lr"))
    # short-time sanity: how much of the Jt<=2 quench features F6/F12 explain (R^2 of pooled n mean on F6 mean)
    short = {}
    for ti, jt in enumerate(jts):
        if jt > 2:
            continue
        nm = np.array([np.mean(Q[i]["readouts"][ti]["n"]) for i in ids]); f6 = XL[:, 1]   # pooled order: means of [deg, F6, F12] first, so mean F6 is column 1
        A = np.c_[np.ones_like(f6), f6]; b, *_ = np.linalg.lstsq(A, nm, rcond=None)
        short[str(jt)] = float(1 - ((nm - A @ b) ** 2).sum() / ((nm - nm.mean()) ** 2).sum())
    res["short_time_R2_nmean_on_F6"] = short

    # pre-registered rules
    qbest = max(v["lr"] for v in res["quench_by_Jt"].values())
    qearly = max(v["lr"] for k, v in res["quench_by_Jt"].items() if float(k) <= 2)
    rr_lowK = max(max(v.values()) for k, v in res["rrwp_by_K"].items() if int(k) < 7)
    rr_highK = max(v["lr"] for k, v in res["rrwp_by_K"].items() if int(k) >= 13)
    res["rules"] = dict(
        A_local_blind=max(res["local"].values()) <= 0.65,
        B_rrwp_range=(rr_lowK <= 0.6) and (rr_highK >= 0.95),
        C_quench_sees_it=(qbest >= 0.90) and (qearly <= 0.65),
        values=dict(local_max=max(res["local"].values()), rrwp_K_lt7_max=rr_lowK, rrwp_K_ge13_lr=rr_highK,
                    quench_best_lr=qbest, quench_Jt_le2_max_lr=qearly))
    res["rules"]["PASS"] = all(v for k, v in res["rules"].items() if k != "values")
    json.dump(res, open(sys.argv[3], "w"), indent=1)
    print(json.dumps(res["rules"], indent=1))
    print("quench AUROC (lr) by Jt:", {k: round(v["lr"], 3) for k, v in res["quench_by_Jt"].items()})
    print("rrwp AUROC (lr) by K:", {k: round(v["lr"], 3) for k, v in res["rrwp_by_K"].items()})


if __name__ == "__main__":
    main()
