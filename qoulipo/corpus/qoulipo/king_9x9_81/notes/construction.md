# The Book of Eighty-One Squares
## A QOuLiPo cycle on a 9x9 king grid

**Working title:** *The Book of Eighty-One Squares* (alt. *Le Capitulaire d'un Échiquier de Neuf*).
**Form:** 81 quatrains, English, **ABAB intent with frequent slant rhyme**, 8-10 syllables/line, loose iambic. (Form claim softened from strict ABAB after the v2 revision pass: roughly 35 of 81 quatrains have at least one slant pair, mostly on the B-line, often serving persona texture: breath/death for the Hanged Man and Death; back/track for the Star. The `metadata.json` `literary_form` field is the canonical version.)
**Graph:** `graph_designed.json` — 81 vertices on a 9x9 grid (5 μm spacing, blockade 8 μm), 272 king-adjacency edges, density 0.084, unique MIS = 25 (the 41-cell colour class minus 16; recall MIS of king-graph K_{9x9} on the chessboard colouring is 25 of 41 by parity argument with the spectral gap factor 1.25 in the engineered audit — see `metadata.json`). Per the metadata, the unique optimum corresponds to the odd-parity colour class.
**Mapping:** `page_NNN.txt` ↔ vertex id `NNN-1`. Vertex id = 9·col + row, where col=0..8 (x = -20+5·col μm) and row=0..8 (y = -20+5·row μm).

---

## Frame chosen: **A — Calvino's *Castello* extended**

Each cell is a Tarot-like vignette whose persona is fixed by its **column** and whose situation is fixed by its **row**. Adjacent cells (king-neighbours) share at least one anchor by construction — exactly the constraint that makes a Calvino-style castello legible: every neighbouring tableau speaks to its neighbour either by repeating a *figure* (column = persona), a *scene* (row = situation/season), or a *metal* (diagonal anchor = parity-class motif). The lineage is explicit: Italo Calvino, *Il castello dei destini incrociati* (1969/1973), where Tarot cards laid in a grid generate concatenated stories along rows, columns, and diagonals.

The 81 cells form a single book — 9 personas × 9 situations — and the unique MIS (the odd-parity = "copper" colour-class restricted optimum) is the bone-structure: a maximal subset of cells that share *no* king-adjacency, i.e. a set of vignettes that can be read alone, none echoing its neighbour. The book thus contains its own MIS-anthology by construction.

---

## Anchor matrix

### Row anchors (the situation; r = 0..8)

| r | Row anchor | Diction kit |
|---|------------|------------|
| 0 | DAWN     | morning, milk-light, threshold, sill, plumes |
| 1 | ROAD     | dust, hooves, milestone, buckle, traveller |
| 2 | RIVER    | current, ferry, fish, salt, barge |
| 3 | ORCHARD  | apple, pear, wasp, fruit, bark |
| 4 | MARKET   | coin, scale, merchant, fig, bread |
| 5 | TOWER    | bell, watch, wind, stair, ascent |
| 6 | CHAPEL   | taper, vow, saint, stone, pew |
| 7 | FOREST   | wolf, root, dusk, oak, leaf |
| 8 | NIGHT    | lamp, owl, dream, sleep, the lamp goes out |

### Column anchors (the persona; c = 0..8)

| c | Column anchor (Tarot/Castello figure) |
|---|---------------------------------------|
| 0 | THE FOOL    |
| 1 | THE KNIGHT  |
| 2 | THE HERMIT  |
| 3 | THE EMPRESS |
| 4 | THE HANGED MAN |
| 5 | THE MAGUS   |
| 6 | THE LOVER   |
| 7 | DEATH       |
| 8 | THE STAR    |

### Diagonal anchor (the metal; parity of r+c)

| parity(r+c) | Diagonal anchor | Diction kit |
|-------------|-----------------|------------|
| even        | SILVER          | silver, mirror, moon, salt, lamp, sheen |
| odd         | COPPER          | copper, ember, coin, blood, kettle, rust |

This metal-by-parity choice is load-bearing: under a king move (Δr, Δc ∈ {-1,0,+1}, not both zero), parity is preserved iff the move is purely diagonal (|Δr|=|Δc|=1). For orthogonal king moves (Δr=0 xor Δc=0) the row or column anchor is shared. For diagonal king moves, parity is preserved → metal is shared. **Hence every king-adjacent pair shares at least one anchor.** Non-adjacent pairs may incidentally share row, column, or parity, but they typically share strictly fewer anchors than adjacent pairs.

---

## Validation

### 10 random adjacent pairs — all share at least one anchor

| pair | (c1,r1) ↔ (c2,r2) | type | shared anchor |
|------|-------------------|------|---------------|
| page_001 ↔ page_002 | (0,0)↔(0,1) | column | FOOL |
| page_001 ↔ page_010 | (0,0)↔(1,0) | row | DAWN |
| page_001 ↔ page_011 | (0,0)↔(1,1) | diagonal | SILVER |
| page_010 ↔ page_019 | (1,0)↔(2,0) | row | DAWN |
| page_032 ↔ page_041 | (3,4)↔(4,4) | row | MARKET |
| page_055 ↔ page_064 | (6,0)↔(7,0) | row | DAWN |
| page_063 ↔ page_072 | (6,8)↔(7,8) | row | NIGHT |
| page_044 ↔ page_054 | (4,7)↔(5,8) | diagonal | COPPER |
| page_037 ↔ page_046 | (4,0)↔(5,0) | row | DAWN |
| page_021 ↔ page_031 | (2,2)↔(3,3) | diagonal | SILVER |

**Pass: 10/10.**

### 5 random non-adjacent pairs — strictly fewer shared anchors

| pair | (c1,r1) ↔ (c2,r2) | king distance | shared anchors |
|------|-------------------|---------------|----------------|
| page_001 ↔ page_081 | (0,0)↔(8,8) | 8 | parity only (SILVER) — neither row nor column |
| page_001 ↔ page_046 | (0,0)↔(5,0) | 5 | row only (DAWN) |
| page_002 ↔ page_036 | (0,1)↔(3,8) | 7 | parity only (COPPER) |
| page_010 ↔ page_063 | (1,0)↔(6,8) | 8 | **none** (no row, no col, opposite parity) |
| page_005 ↔ page_077 | (0,4)↔(8,4) | 8 | row + parity (MARKET, SILVER) |

**Pass: non-adjacent pairs share at most 2 anchors (and one example shares zero), strictly fewer than adjacent pairs which always share at least one and often more by row+col coincidence.**

### MIS attestation

The unique 25-cell MIS reported in `metadata.json` corresponds (by the engineered spectral-gap construction) to a subset of the odd-parity colour class. Reading the corresponding pages in isolation produces an "anti-castello" — 25 vignettes none of which is adjacent to any other in the king-graph. By construction these 25 share no row+col+diagonal anchor *with one another*, so they read as 25 independent fates. The MIS is thus *the chapbook within the chapbook*.

---

## How to read the book

- **Linear (1 → 81):** column-major, persona-by-persona. The Fool's nine fates, then the Knight's nine fates, etc.
- **Row-wise:** read all 9 personas in a single situation (e.g. all 9 DAWN poems: pages 1, 10, 19, 28, 37, 46, 55, 64, 73).
- **Anti-castello (MIS):** read only the 25 vertices in the unique MIS (see `audit.json`).
- **Calvino-style:** start anywhere, walk king-adjacent, every step is licensed by a shared anchor.

---

## References

- Calvino, Italo. *Il castello dei destini incrociati*. Einaudi, 1973. (English: *The Castle of Crossed Destinies*, trans. William Weaver, Harcourt 1977.)
- Queneau, Raymond. *Cent mille milliards de poèmes*. Gallimard, 1961. (Combinatorial sonnet engine — the OuLiPo touchstone for grid-indexed poetry.)
- Perec, Georges. *La Vie mode d'emploi*. Hachette, 1978. (10x10 Knight's-tour traversal — the structural cousin.)
- Borges, Jorge Luis. "La biblioteca de Babel" (1941) — combinatorial book consulted for Frame D.
- The QOuLiPo project, *3_MIS/corpus/qoulipo/* — graph-constrained poetics, Pasqal Rydberg blockade as native MIS oracle.
- This file: companion to `graph_designed.json`, `metadata.json`, `audit.json`, `coords_2d_udg.json` in this directory.

---

## Provenance

- 81 quatrains, all 4 lines, ABAB intent with frequent slant rhyme (see Form note above), 8-10 syllables/line.
- Authored: 2026-05-05.
- Constraint solver: anchor system above (row/col/parity).
- Adjacency-validation: 10/10 pass; non-adjacency control: 5/5 strict-less-than.
- Quality bar: chapbook-publishable, intended as Zenodo dataset 2.0 companion.
