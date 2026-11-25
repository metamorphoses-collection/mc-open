# qgf — historical objects as native registers

Data and analysis code for the paper *The page is already a lattice: historical objects as native registers on neutral-atom quantum processors* (Jurczak, submitted to *EPJ Quantum Technology*).

The folder holds what is needed to reproduce the paper's figures, tables and quoted numbers: the registers, the hardware bitstrings and emulator traces used in the figures, the derived measurements behind the tables, the analysis and figure scripts, and a public copy of the supplement. Page photographs, transcriptions and manuscript images are not stored here. The nine-copy deposit is limited to the derived contrasts, intervals and site loci of Figure 3, with short library labels.

## Layout

- `data/folio/` — 240 Folio window graphs and final emulator occupations; the light-cone aggregate and the four windows run on Ruby, with their bitstrings.
- `data/t1/` — the 24-window residual-agreement test at 4 µs (registers, final occupations, Ruby bitstrings, and the published result).
- `data/p3_river/` — the twelve matched Folio block pairs and the empty-line test results.
- `data/mosaic/` — the Marseille pavement register and the local-addressing simulation on eight small coloured patches.
- `data/die/` — the unique 55-combination die-link graph and the 56-site register as run; see `data/die/README.md`.
- `data/dynamics/` — Figure 4 occupation traces (Folio, mosaic, die-link).
- `data/ninecopy/` — derived Figure 3 measurements only; see `data/ninecopy/README.md`.
- `data/table/` — compact features and the cross-validation output behind Table 3.
- `data/t3/` — readout-phase witness on the ten-atom interferometer.
- `data/synthetic/` — scores from the synthetic cycle-parity test.
- `analysis/` — scripts used to produce the paper's numbers, with paths into this folder. `p3_build.py` is the original pair-selection script and cannot be rerun from the files here; the results are in `data/p3_river/`.
- `figures_src/` — figure scripts. See `figures_src/README.md`.
- `supplement/` — public supplement source. Two 1579-page sections have been removed; see `supplement/README.md`.

## Licence

Code in this folder (Python scripts and similar) is MIT, as in the rest of this repository. Data are CC BY 4.0. Folio page photographs are not included; they are those of the Bodleian Libraries, Arch. G c.7, CC-BY 3.0, and can be obtained from the Bodleian.

## What is not in the folder

Generator pools and full emulator correlation tensors for the 240 Folio windows and the 100 + 101 generated mosaic windows are not included. The light-cone panel uses a deposited aggregate over those 240 windows; Table 3 can be checked from the compact features and the saved cross-validation output. Raw Fresnel bitstrings are not included; the Fresnel agreement table and figure are in the supplement. Photographs used in Figure 1 are not included.
