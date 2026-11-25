# qgf — historical objects as native registers

Data and analysis code for *The page is already a lattice: historical objects as native registers on neutral-atom quantum processors* (C. Jurczak, 2026).

The folder holds the registers, the hardware bitstrings and emulator traces used in the figures, the derived measurements behind the tables, and the analysis and figure scripts.

## Layout

```
qgf/
  figures/                 figure scripts (Fig. 1 register panels, Figs. 2–4)
  analysis/                residual agreement, readout-phase witness, die-link counts, local addressing
  data/
    folio/                 Folio windows, occupations and pulse parameters
    lightcone/             Figure 2a–b aggregate, window features, campaign index and shots
    empty_line/            Figure 2c twelve matched pairs
    residual_test/         24-window residual agreement at 4 µs
    readout_witness/       ten-atom readout-phase witness
    dynamics/              Figure 4 hardware curves, registers and χ=600 traces
    mosaic/                Marseille pavement register and local-addressing output
    die/                   unique 55-combination graph and the 56-site register as run
    press_state/           Figure 3 contrasts and window loci of nine copies
    encodings/             Table 3 features, cross-validation errors and summary
    synthetic/             cycle-parity scores on constructed windows
```

## Figures and main results

| Item | Where | What it reproduces |
| --- | --- | --- |
| Figure 1 register panels | `figures/fig1.py` | Folio, mosaic and die-link registers |
| Figure 2 | `figures/fig2.py`, `data/lightcone`, `data/empty_line` | Light-cone times; empty-line test (12 pairs, median suppression about 280) |
| Figure 3 | `figures/fig3.py`, `data/press_state` | Press-state contrasts of nine copies |
| Figure 4 | `figures/fig4.py`, `data/dynamics` | Hardware occupations against the χ=600 emulation |
| Table 3 | `data/encodings/` | Neighbour-count MAE and dislocation AUROC |
| Residual agreement | `analysis/residual_agreement.py`, `data/residual_test` | +0.75 (FM-like) and −0.09 (AFM) at 4 µs on 24 windows |
| Readout-phase witness | `analysis/readout_witness.py`, `data/readout_witness` | One-body and two-body phase witnesses |
| Die-link counts | `analysis/die_counts.py`, `data/die` | 55 combinations, 30 edges, independence number 32; 56-site register as run |
| Local addressing | `analysis/mosaic_addressing.py`, `data/mosaic/addressing.json` | Simulation pointed to in the Discussion |
| Cycle-parity scores | `data/synthetic` | Constructed-task AUROC |

## How to run

Python 3.10 or later. From this folder:

```
python -m pip install -r requirements.txt
python figures/fig1.py -o fig1_registers.png
python figures/fig2.py -o fig2.png
python figures/fig3.py -o fig3.png
python figures/fig4.py -o fig4.png
```

`torch` is needed only for `analysis/mosaic_addressing.py`.

Analysis scripts write their result JSON next to the corresponding data:

```
python analysis/residual_agreement.py
python analysis/readout_witness.py
python analysis/die_counts.py
python analysis/mosaic_addressing.py data/mosaic/addressing.json
```

The residual-agreement script refits the classical rate model and may take several minutes.

## Licence

Code is MIT, as in the rest of this repository. Data are CC BY 4.0.
