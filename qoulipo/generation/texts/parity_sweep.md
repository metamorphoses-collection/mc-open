# Parity Sweep — Rydberg MIS vs Classical ILP

**Graph**: Giambullari 1544 topic-similarity (fine-tuned LightOnOCR, 156 paragraphs)

**Emulator**: Pulser QuTiP statevector · 1000 shots per run · 2 trials per size

**Subgraphs**: top-K by node degree


| N | ILP opt | Q mean | ratio | Jaccard | UDG fidelity |
|---|---|---|---|---|---|
| 8 | 6 | 2.5 | 0.42 ± 0.08 | 0.32 | 0.48 |
| 10 | 6 | 3.0 | 0.50 ± 0.00 | 0.39 | 0.69 |
| 12 | 7 | 4.5 | 0.64 ± 0.07 | 0.28 | 0.76 |
| 14 | 8 | 8.0 | 1.00 ± 0.00 | 1.00 | 0.80 |