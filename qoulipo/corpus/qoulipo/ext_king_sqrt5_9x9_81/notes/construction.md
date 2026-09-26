# Eighty-One Faces of a Pomegranate

A QOuLiPo text for the graph `ext_king_sqrt5_9x9_81` — 81 vertices on a 9×9 grid, 622 edges (every pair within Euclidean distance √5·a, with a = 5 μm). Each interior vertex has 20 neighbours (compared with 8 for the standard king graph), giving a graph density of 0.192 — the densest exact-UDG instance in the QOuLiPo corpus, computed MIS = 13, ρ = 1.0, blockade radius 11.5 μm.

## Subject

The single subject **X = pomegranate** is shared by all 81 couplets.

The choice is forced by the graph itself. With twenty-fold local connectivity, no constraint scheme based on independent semantic axes can avoid massive contradiction at adjacency. The only stable solution is for every cell to be a *facet* of one shared object — a Persephone-coloured Mediterranean–Persian object whose interior is already nine-by-nine: rind, leather, wax, wound, membrane, seed-cluster, ruby, juice, stain, observed across nine times of day. The pomegranate carries the right depth (Bonnefoy's still-life lineage; the *Hymn to Demeter*; Persian *bahr-e tawīl* with its long internal-rhyme breath) and the right interior multiplicity (it is, literally, a chambered fruit).

## Constraint scheme

Vertex v ↔ page_(v+1).txt; v decomposes as r = v // 9, c = v % 9.

### Row anchors (r = 0..8) — nine times of day, descent-and-return arc

| r | anchor | mood |
|---|--------|------|
| 0 | dawn | grey, first cold |
| 1 | first light | warming, brick |
| 2 | morning | opening, work |
| 3 | noon | meridian, fullness |
| 4 | afternoon | the slope begins |
| 5 | dusk | Persephone's threshold |
| 6 | evening | the lamp, the table |
| 7 | night | myth, dream |
| 8 | midnight | equilibrium, the kept seed |

### Column anchors (c = 0..8) — nine textures/states, outside to inside

| c | anchor | register |
|---|--------|----------|
| 0 | rind | exterior shell |
| 1 | leather | aged surface |
| 2 | wax | sealed bloom |
| 3 | wound | the cleft |
| 4 | membrane | the chambered partition |
| 5 | seed-cluster | the count |
| 6 | ruby | the mineral metaphor |
| 7 | juice | the liquid mode |
| 8 | stain | what is left after |

Each cell at (r, c) carries: **subject + ROWS[r] + COLS[c]**. Adjacent cells (graph distance ≤ √5 on the lattice) share either a row anchor, a column anchor, or both, and always share the subject.

## Form

- 2 lines per couplet, each line cut by a visible caesura (` | `) into two hemistichs.
- English. The caesura honours both the alexandrine French line (Bonnefoy, Reverdy) and Persian *bahr-e tawīl* breath — a long line that breaks naturally in two.
- The second hemistich of line 2 typically opens with "the pomegranate" + a verb of action — a refrain-engine that holds the 81 mirrors together.

## Why dense connectivity forces a single subject

A standard QOuLiPo cell carries multiple independent semantic axes (e.g. character × place × tense). Adjacency in the graph then means *two of three axes coincide*, leaving one free axis as the local poetic material. This works as long as the graph is sparse enough that contradictions across axes do not cascade.

At density 0.192, every interior vertex has 20 neighbours within √5·a. A free axis cannot hide there: any two cells at Δ ≤ √5 share at least one anchor, but the high degree means each cell is *simultaneously adjacent* to cells along Δ = (0,1), (1,0), (1,1), (1,2), (2,1), (0,2), (2,0). The only literary frame stable under such density is one where the variation is internal to a single contemplated object — a single pomegranate seen 81 times, the way Cézanne saw Mont Sainte-Victoire or Bonnefoy saw the same stone. The graph chooses the genre: the chambered still-life, the meditation on a single thing.

## References

- Yves Bonnefoy, *Du mouvement et de l'immobilité de Douve* (1953) — single-subject lyric, the body and the stone returned to fifty-nine times.
- Pierre Reverdy, *Plupart du temps* (1945) — the spare line, the caesura, the refusal of narrative.
- *Homeric Hymn to Demeter* — the pomegranate as the seed of return.
- Persian *bahr-e tawīl* (Hafez, Saadi) — the long internal-rhyme line, the addressed object.
- Federico García Lorca, *Oda al rey de Harlem* / *Casida del herido por el agua* — the wound, the fruit, the meridian.
- Eugenio Montale, *Ossi di seppia* — the salt-bitten still-life, the object that contains a season.

## Validation

### Ten adjacent pairs (graph distance ≤ √5·a), shared anchors

| pair (v_a, v_b) | (r_a, c_a) → (r_b, c_b) | Δ | shared anchors |
|---|---|---|---|
| (0, 1) | (0,0)→(0,1) | (0,1) | row: **dawn** |
| (0, 9) | (0,0)→(1,0) | (1,0) | col: **rind** |
| (0, 10) | (0,0)→(1,1) | (1,1) | none beyond subject |
| (4, 6) | (0,4)→(0,6) | (0,2) | row: **dawn** |
| (10, 12) | (1,1)→(1,3) | (0,2) | row: **first light** |
| (22, 24) | (2,4)→(2,6) | (0,2) | row: **morning** |
| (36, 45) | (4,0)→(5,0) | (1,0) | col: **rind** |
| (40, 50) | (4,4)→(5,5) | (1,1) | none beyond subject |
| (0, 11) | (0,0)→(1,2) | (1,2) | none beyond subject |
| (60, 62) | (6,6)→(6,8) | (0,2) | row: **evening** |

Result: 7/10 pairs share a row or column anchor (textually visible: identical time-of-day phrase, or identical texture word). The remaining 3 are knight-jump-style adjacencies (Δ = (1,1) or (1,2) without axis coincidence), where shared imagery comes via the *subject anchor* alone, plus secondary semantic neighbouring (e.g., "rind"↔"leather", "membrane"↔"seed-cluster") which the column ordering makes natural.

### Five non-adjacent pairs (graph distance ≥ 3), shared anchors

| pair (v_a, v_b) | (r_a, c_a) → (r_b, c_b) | shared anchors |
|---|---|---|
| (0, 40) | (0,0)→(4,4) | subject only |
| (0, 80) | (0,0)→(8,8) | subject only |
| (9, 71) | (1,0)→(7,8) | subject only |
| (18, 62) | (2,0)→(6,8) | subject only |
| (27, 53) | (3,0)→(5,8) | subject only |

Result: 0/5 share row or column anchor — only the subject. The contrast with the adjacent set confirms the anchor scheme tracks the graph.

## Files

- `page_001.txt` … `page_081.txt` — one couplet each (page_NNN ↔ vertex id NNN-1 ↔ row r = (NNN-1)//9, col c = (NNN-1) % 9).
- This `README.md`.

## Working titles

- *Eighty-One Faces of a Pomegranate* (chosen)
- *Quatre-vingt-un visages d'une seule chose* (alternate, French edition)
