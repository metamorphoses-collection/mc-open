# Die-link registers

Two register files are included.

- `qgf_dielink_a_dedup.json` is the unique graph used for the counts in the paper: 55 die combinations, 30 shared-die edges, and a maximum independent set of 32.
- `qgf_dielink_a.json` is the register as run on Ruby and in the Figure 4 emulation: 56 sites, because the combination V347/R690 was entered twice. The extra site is isolated and does not change the bonds. The 56-site graph has a maximum independent set of 33, since that extra isolated site can be co-selected.

Hardware bitstrings in `results_ruby_dielink/` are those of the 56-site register.
