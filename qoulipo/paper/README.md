# Native

A platform-by-platform cartography of native observables on analog quantum hardware, the classical primitives they instantiate, the tasks those primitives serve, and the certification status of each pairing.

## What this is

**Native** is the umbrella initiative for the *applications-discovery* line of work spun out of the QOuLiPo programme. The doctrine in one line:

> *physical attribute → native observable → classical primitive → useful task*

with two constraints: the classical primitive must be hard to fake cheaply, and the task must benefit measurably from access to the primitive.

The position paper in this folder (`main.tex`) articulates the doctrine, the discovery methodology (*enumerate → abstract → propose → triage → certify*), the ten-row inventory of currently-accessible native observables on neutral-atom Rydberg hardware, the unit-disk-graph constraint and how the doctrine softens it, two routes to XY/XXZ effective dynamics (microwave Floquet on dipole-dipole-coupled states; strong-drive dressing of the Ising chip), and local addressability via the Pulser DMM channel.

## Current state (2026-05-18, 15 pages)

The Native paper has been extended with a new §10 "Industry validation" that ties together:
- Real-data external validation on SemEval-2016 stance-detection corpora (AtomRank beats cosine by +0.08 absolute AUROC on 3 of 4 polarised Twitter targets) — confirming the doctrine on data the methodology had not seen during development.
- IRA tweets archive as negative control (correct null behaviour on same-source manufactured opposition).
- Commercial archetype mapping: three of Graphika's six published report types reduce cleanly to AtomRank readouts, with a 90-day first-pilot scope at N ≤ 100.

All next-step certifications in §8 now carry status flags reflecting the AtomRank Part II progress: Item 1 (DMM re-ranker) EMU-certified; Item 2 (three-point cumulants) honest null reported; Item 5 (signed-community) partial cross-row certification on Tractatus.

## The first certified instance

The AtomRank paper at `../02_quench_paper/` is the first stage-5 certification under the methodology: row 2 of the inventory (quench-correlator signed centrality on argument corpora), with EMU AUROC 0.980 ± 0.005 matching QPU AUROC 0.973 on the Tractatus Antithesis corpus, against cosine 0.43 and DeBERTa-NLI 0.60 baselines. Since the first draft of the present paper, that certification has expanded to **six application readouts on the same shot data** (AtomRank Part II); the Native paper §3 summarises them, the AtomRank paper details them.

This `native/` folder generalises the doctrine that produced AtomRank, identifies the next instances to certify, and provides a commercial archetype (Graphika-style influence-network analytics) as the first concrete pilot target.

## Folder layout

```
native/
├── main.tex          ── position paper (Overleaf-syncable)
├── references.bib    ── bibliography
├── main.bbl          ── compiled bibliography (synced for Overleaf reliability)
├── overleaf_sync.py  ── two-way git sync with Overleaf project
├── README.md         ── this file
└── (future) figures/ ── methodology pipeline schematic, inventory diagram
└── (future) drafts/  ── working drafts of successor papers
```

## Overleaf

`main.tex` uses standard packages (article, amsmath, booktabs, natbib, hyperref, tikz). Compile order: pdflatex → bibtex → pdflatex × 2. Bibliography is synced as `main.bbl` to ensure rendering even on Overleaf's first compile pass.

Project: `6a0a232fc5f8b090a582317a`. Sync via `python3 overleaf_sync.py {pull,push}`.

## Next artefacts (per §9 of the paper)

1. **Hardware-native re-ranker** via DMM local detuning (row 4) — strongest queue-ready candidate.
2. **3-point signed-graph extension** — free post-processing of existing Tractatus / Multimodal shots, ~2 weeks.
3. **AtomRank under XY** via either Route A (microwave Floquet) or Route B (boost-drive) — strong-drive paper.
4. **CTQW realisation** — split into 4a (programmable polynomial CTQW with matched classical baseline) and 4b (bilayer-contingent welded-tree exponential speedup).
5. **Signed-community detection** — joint correlator + persistence readout against SPONGE / signed-Louvain baselines on Wikipedia-RfA / Bitcoin-Alpha / signed LFR.
6. **Bilayer position note** — programmatic case for bilayer hardware on multilayer-knowledge-graph tasks (Cecilia, multimodal corpora).

## Relationship to the QOuLiPo programme

QOuLiPo originated as a corpus-and-MIS pipeline on textual artefacts; the quench paper (02_quench_paper) was its first analog-native instance. Native is the abstraction layer above both: the methodology that produced AtomRank, applicable to platforms beyond Rydberg and to tasks beyond contradiction detection.
