# `corpus/qpu/` — FRESNEL QPU output bundles

This folder collects the bitstring outputs of FRESNEL_CAN1 (Pasqal Cloud,
neutral-atom 100-qubit) campaigns supporting the QOuLiPo paper. Two
complementary views of the same data:

1. **By campaign** (this folder): one subfolder per submission campaign,
   each containing `batches.json` with submission metadata + `bitstrings/`
   with raw `{bitstring -> count}` per batch.
2. **By corpus item** (symlinks at `corpus/<natural|qoulipo>/<text>/qpu/`):
   each text carries a `qpu/` folder with symlinks back to its relevant
   campaign-folder bitstring files.

Both views index the same on-disk JSON files; symlinks have the form
`<run_name>__<batch_name>.json` to preserve campaign provenance.

## Migrated campaigns

| Campaign | Date | Account | Texts | Batches | Notes |
|---|---|---|---|---|---|
| `20260417_pari_III_quench_qpu` | 2026-04-17 | gmail | Pari III (N=100) | 4 | Original quench at T=1/2/4 µs (600 shots each) + adiabatic ref (700 shots) |
| `20260417_investiqo_phase_B` | 2026-04-17 | investiqo | Stanze, Pari II, Dante, Ausonius | 8 submitted | Only `pari_II_b1` and `dante_b1` actually ran (DONE, 1000 shots each); the other 6 were CANCELED before execution |
| `20260418_investiqo_phase_C` | 2026-04-18 | investiqo | Stanze, Pari II, Dante, Ausonius | 4 submitted | All four CANCELED |
| `20260430_asterisk_fixes_gmail` | 2026-04-30 | gmail | Galileo k=16, Stanze, Castello 49 | 3 | Cleanup campaign for Table 3 footnotes |
| `20260430_q1_pari_II_quench_gmail` | 2026-04-30 | gmail | Pari II | 4 | Quench at T=0.5/1/2/4 µs × 937 shots; multi-text §6.2 figure |
| `20260430_q2_pari_III_step_investiqo` | 2026-04-30 | investiqo | Pari III | 3 | Stepped 500-shot batches at T=2/1/4 µs; correlator follow-up |
| `20260430_decoded` | 2026-04-30 | — | — | — | Per-batch decoded summaries (valid %, best IS, ratio, weight histograms) for all the above |

## Per-batch JSON schema

Each `bitstrings/<name>.json` file:
```json
{
  "batch_id": "uuid",
  "name": "...",
  "status": "DONE | CANCELED",
  "total_shots": 937,
  "n_unique_bitstrings": 638,
  "T_ns": 2000,
  "protocol": "quench | adiabatic",
  "counts": {"01001...": 5, "10010...": 3, ...}
}
```

The `counts` dict is the full FRESNEL bitstring distribution. Bit position
`i` in each key string corresponds to qubit `q_i`, which in turn corresponds
to atom `i` in the register (active atoms only; FRESNEL dummy traps are
not in the bitstring).

## Pre-April-2026 campaigns

Earlier exploratory campaigns from April 8–14 (EMU baselines, ablation
studies, partial bilayer experiments) are kept under `quantum/runs/`
in the source tree but are not migrated here, because their numbers
either do not appear in the paper or are superseded by the campaigns
listed above. Run-by-run provenance for those is at
`quantum/runs/PROVENANCE.md`.

## Reproducibility

Per-text decoded statistics (valid %, best IS, ratio, Hamming-weight
histogram) are at `corpus/qpu/20260430_decoded/decoded.json`.

The submission scripts that produced these batches are at
`quantum/core/submit_*.py`, with credentials reading the gmail (free)
and investiqo (GCP-billed) accounts from the `ACCOUNTS` dict in
`quantum/core/qpu_submit_all.py`. The investiqo password is read from
`PASQAL_INVESTIQO_PASSWORD` (env var); gmail credentials are embedded
for free-credit access. Re-running any campaign produces a new
batch ID (Pasqal-side); bitstrings are deterministic up to QPU shot noise.
