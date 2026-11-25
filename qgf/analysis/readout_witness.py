"""Readout-phase witness on a ten-atom interferometer register. A 2 µs facilitation pulse is followed by a π/2 readout pulse whose phase is 0 or π/2 relative to the drive. The one-body contrast witnesses coherence of the atoms at readout; the two-body contrast witnesses correlated coherence between them."""
import os, json, numpy as np
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; HERE = str(ROOT / "data/readout_witness"); rng = np.random.default_rng(7)
LA, LB = 3, 5; N = 10; T = N - 1
BONDS = [(0, 1), (0, LA + 1), (LA, T), (LA + LB, T)] + [(i, i + 1) for i in range(1, LA)] + [(i, i + 1) for i in range(LA + 1, LA + LB)]


def main():
    rows = json.load(open(str(ROOT / "data/readout_witness/campaign.json")))
    def counts(k):
        d = json.load(open(str(ROOT / f"data/readout_witness/shots/job_{rows[k]['shot_id']}.json"))); assert d["job_idx"] == rows[k]["shot_id"] and d["n_atoms"] == N
        keys = list(d["results"]); return np.array([[int(ch) for ch in s] for s in keys]), np.array([d["results"][s] for s in keys], float)
    def obs(B, w):
        p = w / w.sum(); n = p @ B; return np.r_[n, [p @ (B[:, i] * B[:, j]) - n[i] * n[j] for i, j in BONDS]]
    def pooled(ks, boot=False):
        Bs, ws = [], []
        for k in ks:
            B, w = counts(k)
            if boot: w = rng.multinomial(int(w.sum()), w / w.sum()).astype(float)
            Bs.append(B); ws.append(w)
        return obs(np.concatenate(Bs), np.concatenate(ws))
    def contrast(ka, kb, label):
        d = pooled(ka) - pooled(kb); D = np.array([pooled(ka, True) - pooled(kb, True) for _ in range(2000)]); se = D.std(0); sig = np.abs(d) > 3 * se
        r = dict(label=label, dn=d[:N].tolist(), dC=d[N:].tolist(), se_n=se[:N].tolist(), se_C=se[N:].tolist(), sites_sig=int(sig[:N].sum()), bonds_sig=int(sig[N:].sum()))
        print(f"{label}: sites {r['sites_sig']}/10 (max |dn| {np.abs(d[:N]).max():.3f}, SE {np.median(se[:N]):.4f}) | bonds {r['bonds_sig']}/10 (max |dC| {np.abs(d[N:]).max():.4f}, SE {np.median(se[N:]):.4f})")
        return r
    k0 = [k for k in range(20) if k % 2 == 0]; k1 = [k for k in range(20) if k % 2 == 1]
    main = contrast(k0, k1, "phi 0 vs pi/2")
    drift = [contrast([k for k in ks if k // 2 < 5], [k for k in ks if k // 2 >= 5], f"drift phi {ph}") for ks, ph in ((k0, "0"), (k1, "pi/2"))]
    drift_ok = all(x["bonds_sig"] <= 1 and x["sites_sig"] <= 1 for x in drift)
    res = dict(main=main, drift=drift, drift_ok=drift_ok, PRIMARY_two_body=bool(drift_ok and main["bonds_sig"] >= 5), SECONDARY_one_body=bool(drift_ok and main["sites_sig"] >= 5))
    print("drift ok:", drift_ok, "| PRIMARY two-body:", res["PRIMARY_two_body"], "| SECONDARY one-body:", res["SECONDARY_one_body"])
    json.dump(res, open(str(ROOT / "data/readout_witness/result.json"), "w"), indent=1)


if __name__ == '__main__':
    main()
