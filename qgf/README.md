# qgf — historical objects as native registers

Data and analysis code for the paper *The page is already a lattice: historical objects as native registers on neutral-atom quantum processors* (C. Jurczak, 2026).

The folder holds the registers, the hardware bitstrings and emulator traces used in the figures, the derived measurements behind the tables, the analysis and figure scripts, and the supplement.

## Layout

- `data/folio/` — 240 Folio window graphs and final emulator occupations; the light-cone aggregate and the four windows run on Ruby, with their bitstrings.
- `data/t1/` — the 24-window residual-agreement test at 4 µs (registers, final occupations, Ruby bitstrings, and the result).
- `data/p3_river/` — the twelve matched Folio block pairs and the empty-line test results.
- `data/mosaic/` — the Marseille pavement register and the local-addressing simulation on eight small coloured patches.
- `data/die/` — the 55-combination die-link graph and the 56-site register as run; see `data/die/README.md`.
- `data/dynamics/` — Figure 4 occupation traces (Folio, mosaic, die-link).
- `data/ninecopy/` — Figure 3 measurements.
- `data/table/` — compact features and the cross-validation output behind Table 3.
- `data/t3/` — readout-phase witness on the ten-atom interferometer.
- `data/synthetic/` — scores from the synthetic cycle-parity test.
- `analysis/` — scripts that produce the paper's numbers, with paths into this folder.
- `figures_src/` — figure scripts.
- `supplement/` — supplement source.

## Licence

Code is MIT, as in the rest of this repository. Data are CC BY 4.0.
