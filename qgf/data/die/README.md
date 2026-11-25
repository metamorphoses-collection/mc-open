# Die-link register

Two versions of the same register are included.

- `unique_55.json` is the unique graph of 55 die combinations (30 shared-die edges, independence number 32). These are the counts in the paper.
- `as_run_56.json` is the 56-site register that was run, and the register of the Figure 4 emulation. One combination (V347/R690) was entered twice; the extra site is isolated and adds no bond. The independence number of the as-run register is 33, because that isolated site can be co-selected.

`python analysis/die_counts.py` prints both sets of counts.
