# QOuLiPo: Prescribed-Property Text Designs

Three new constrained texts whose graph-theoretic properties are controlled by design.
Each text specifies a target graph topology; the writing constraint ensures
the semantic embedding graph matches that target.

Pipeline: intfloat/multilingual-e5-large (1024-dim), cosine sim threshold 0.78,
~370 words/page, 5 threads/page (unless noted), keyword density 2-3 terms/sentence.

---

## Design A: rho = 1.0 -- "Le Livre Irremplacable" (The Irreplaceable Book)

### Target Property

**Rigidity rho = 1.0**: every page in the MIS backbone is structurally
irreplaceable. There is exactly ONE maximum independent set. Removing any
backbone page and substituting any other page fails. This is the Dante extreme
of the rigidity spectrum.

### Mathematical Mechanism

A graph has unique MIS (rho=1.0) when every MIS node v satisfies: removing v
from the MIS, no other node can take its place while maintaining independence
from the remaining MIS nodes. Formally:

    For every MIS node v: N(v) intersect (V \ MIS \ N(MIS \ {v})) = empty

This is guaranteed by **double domination**: every non-MIS node is adjacent to
at least 2 MIS nodes. Then removing any single MIS node v still leaves every
non-MIS node blocked by at least 1 other MIS neighbor.

### Why Double Domination Works

Suppose non-MIS page u is adjacent to MIS pages v1 and v2. If we remove v1
from the MIS, page u is still adjacent to v2 (still in MIS), so u cannot
replace v1. This holds for EVERY non-MIS page, so no replacement exists for v1.
By symmetry, no MIS page is replaceable. QED: rho=1.0.

### Design Parameters

| Parameter | Value |
|-----------|-------|
| N (pages) | 50 |
| Thread pool | 12 |
| Threads per page | 6 |
| Edge criterion | overlap >= 4 (of 6 shared threads) |
| Non-edge criterion | overlap <= 3 |
| Target MIS | 17 |
| MIS/N | 0.340 |
| Expected density | 0.234 |
| Expected edges | ~287 |
| Recommended k | 8 or 12 |
| Recommended threshold | 0.80 (stricter than 0.78 to match 4/6 overlap) |

### Thread Pool (12 threads)

| # | Thread (EN) | Thread (FR) | Domain |
|---|-------------|-------------|--------|
| 0 | WAGER | PARI | Probability, risk, decision under uncertainty |
| 1 | CHRONICLE | CHRONIQUE | Historical record, witnessed events |
| 2 | CONSPIRACY | COMPLOT | Fabrication, forgery, hidden agendas |
| 3 | TONGUE | LANGUE | Language, translation, the birth of vernacular |
| 4 | NUMBER | NOMBRE | Mathematics, combinatorics, counting |
| 5 | FAITH | FOI | Belief, doubt, the silence of God |
| 6 | SWORD | EPEE | War, conflict, fratricidal violence |
| 7 | PARCHMENT | PARCHEMIN | Manuscripts, textual transmission |
| 8 | MALIETTE | MALIETTE | The teacher, ZaZiPo, the gift of reading |
| 9 | GAME | JEU | OuLiPo, ludic constraint, rules that free |
| 10 | MIRROR | MIROIR | Reflection, doubling, self-reference |
| 11 | INK | ENCRE | Writing, inscription, the physical act of text |

### Thread Assignment Table

Pages 1-17 are MIS nodes (backbone). Pages 18-50 are non-MIS nodes.
Each non-MIS page shares >= 4 threads with >= 2 MIS pages (double domination).

| Page | Role | Threads |
|------|------|---------|
| P01 | MIS | CHRONICLE, CONSPIRACY, FAITH, GAME, MIRROR, PARCHMENT |
| P02 | MIS | FAITH, GAME, INK, MALIETTE, MIRROR, WAGER |
| P03 | MIS | CHRONICLE, GAME, INK, MIRROR, NUMBER, TONGUE |
| P04 | MIS | FAITH, GAME, INK, NUMBER, PARCHMENT, SWORD |
| P05 | MIS | CHRONICLE, CONSPIRACY, MALIETTE, MIRROR, TONGUE, WAGER |
| P06 | MIS | CHRONICLE, FAITH, GAME, MALIETTE, SWORD, TONGUE |
| P07 | MIS | INK, MALIETTE, NUMBER, SWORD, TONGUE, WAGER |
| P08 | MIS | FAITH, MALIETTE, MIRROR, NUMBER, PARCHMENT, TONGUE |
| P09 | MIS | CONSPIRACY, GAME, MALIETTE, MIRROR, NUMBER, SWORD |
| P10 | MIS | GAME, MIRROR, PARCHMENT, SWORD, TONGUE, WAGER |
| P11 | MIS | CONSPIRACY, GAME, INK, MALIETTE, PARCHMENT, TONGUE |
| P12 | MIS | CONSPIRACY, FAITH, GAME, NUMBER, TONGUE, WAGER |
| P13 | MIS | CONSPIRACY, INK, MIRROR, NUMBER, PARCHMENT, WAGER |
| P14 | MIS | CHRONICLE, GAME, MALIETTE, NUMBER, PARCHMENT, WAGER |
| P15 | MIS | CONSPIRACY, FAITH, INK, MIRROR, SWORD, TONGUE |
| P16 | MIS | CHRONICLE, INK, MALIETTE, MIRROR, PARCHMENT, SWORD |
| P17 | MIS | CHRONICLE, FAITH, MIRROR, NUMBER, SWORD, WAGER |
| P18 | --- | FAITH, NUMBER, PARCHMENT, SWORD, TONGUE, WAGER |
| P19 | --- | CHRONICLE, FAITH, MALIETTE, SWORD, TONGUE, WAGER |
| P20 | --- | CHRONICLE, CONSPIRACY, FAITH, GAME, SWORD, WAGER |
| P21 | --- | CONSPIRACY, FAITH, INK, MIRROR, PARCHMENT, SWORD |
| P22 | --- | CHRONICLE, CONSPIRACY, INK, NUMBER, SWORD, WAGER |
| P23 | --- | CONSPIRACY, FAITH, INK, MALIETTE, MIRROR, TONGUE |
| P24 | --- | INK, MALIETTE, MIRROR, NUMBER, PARCHMENT, SWORD |
| P25 | --- | CHRONICLE, CONSPIRACY, GAME, INK, NUMBER, TONGUE |
| P26 | --- | CHRONICLE, FAITH, MALIETTE, NUMBER, TONGUE, WAGER |
| P27 | --- | CONSPIRACY, FAITH, GAME, SWORD, TONGUE, WAGER |
| P28 | --- | FAITH, GAME, NUMBER, PARCHMENT, SWORD, TONGUE |
| P29 | --- | FAITH, GAME, MALIETTE, MIRROR, PARCHMENT, TONGUE |
| P30 | --- | CHRONICLE, CONSPIRACY, INK, MIRROR, NUMBER, SWORD |
| P31 | --- | CONSPIRACY, GAME, MALIETTE, PARCHMENT, SWORD, WAGER |
| P32 | --- | FAITH, INK, MALIETTE, NUMBER, SWORD, WAGER |
| P33 | --- | CHRONICLE, MALIETTE, MIRROR, PARCHMENT, TONGUE, WAGER |
| P34 | --- | CHRONICLE, FAITH, INK, MALIETTE, NUMBER, WAGER |
| P35 | --- | CHRONICLE, FAITH, GAME, MIRROR, SWORD, TONGUE |
| P36 | --- | CHRONICLE, CONSPIRACY, GAME, MALIETTE, NUMBER, PARCHMENT |
| P37 | --- | CHRONICLE, CONSPIRACY, INK, MALIETTE, MIRROR, PARCHMENT |
| P38 | --- | CHRONICLE, GAME, INK, PARCHMENT, SWORD, TONGUE |
| P39 | --- | CONSPIRACY, MALIETTE, NUMBER, SWORD, TONGUE, WAGER |
| P40 | --- | CHRONICLE, CONSPIRACY, GAME, INK, MIRROR, WAGER |
| P41 | --- | CHRONICLE, CONSPIRACY, INK, PARCHMENT, TONGUE, WAGER |
| P42 | --- | CHRONICLE, FAITH, INK, MIRROR, PARCHMENT, TONGUE |
| P43 | --- | CHRONICLE, CONSPIRACY, FAITH, INK, MIRROR, PARCHMENT |
| P44 | --- | CHRONICLE, CONSPIRACY, GAME, MALIETTE, NUMBER, SWORD |
| P45 | --- | CHRONICLE, FAITH, INK, PARCHMENT, SWORD, WAGER |
| P46 | --- | MIRROR, NUMBER, PARCHMENT, SWORD, TONGUE, WAGER |
| P47 | --- | CONSPIRACY, FAITH, GAME, INK, MALIETTE, PARCHMENT |
| P48 | --- | CONSPIRACY, GAME, INK, MIRROR, NUMBER, TONGUE |
| P49 | --- | CONSPIRACY, FAITH, GAME, MALIETTE, NUMBER, WAGER |
| P50 | --- | GAME, MALIETTE, MIRROR, NUMBER, PARCHMENT, WAGER |

**Constraint verification (SA cost = 0.0)**:
- MIS independence: all 136 MIS pairs have overlap <= 3. PASS.
- Double domination: all 33 non-MIS pages have >= 2 MIS neighbors. PASS.
- Thread balance: all 12 threads used exactly 25 times. PERFECT.
- All 33 non-MIS configurations are distinct. PASS.

### Literary Framing

Title: **"Le Livre Irremplacable"** (The Irreplaceable Book)

Three voices, as in the original Nithard-Pascal text, but now the constraint
is different: every page of the backbone is unique and essential. No page can
be substituted. The literary metaphor: a book where every chapter is load-bearing,
where removing any single chapter causes the entire argument to collapse.

Structure: the 17 backbone pages form a "cathedral" -- each is a pillar.
The 33 surrounding pages are the "buttresses" -- they support the pillars
but can be rearranged. The pillar pages carry the irreducible argument;
the buttress pages elaborate, ornament, contextualize.

Voices:
- NITHARD: the irreplaceable witness (he was the ONLY source)
- PASCAL: the irreplaceable proof (mathematical necessity)
- THE PROFESSOR: the irreplaceable teacher (what only one person can teach)

### Difference from Existing Texts

The OuLiPo 50 EN text uses 10 threads with 5/page. This design uses **12 threads
with 6/page** to create enough combinatorial space for double domination. The
higher overlap threshold (4/6 vs 3/5) provides cleaner edge/non-edge separation.

---

## Design B: rho ~ 0.0 -- "Le Kaleidoscope" (The Kaleidoscope)

### Target Property

**Rigidity rho = 0.000**: every page in the MIS backbone can be replaced by
an alternative. The maximum number of MIS solutions: 3^17 = 129,140,163.
This is the extreme opposite of Dante -- a text with no structural determinism,
where every reading path has equally valid alternatives.

### Mathematical Mechanism

The graph is a **disjoint union of 17 triangles (K_3)**. Each triangle is a
clique of 3 pages that are mutually adjacent (share same thread signature).
MIS picks exactly 1 page from each triangle. Since any of the 3 can be chosen,
there are 3 choices per triangle, giving 3^17 total MIS solutions.

No page appears in ALL solutions, so the set of essential nodes is empty: rho=0.

### Why Clique Decomposition Works

In a disjoint union of k copies of K_s:
- MIS size = k (one from each clique)
- Number of MIS solutions = s^k
- Every MIS node can be replaced by any of (s-1) alternatives in its clique
- Essential nodes = 0
- rho = 0/k = 0

For s=3, k=17: MIS=17, solutions=3^17, rho=0.000.

### Design Parameters

| Parameter | Value |
|-----------|-------|
| N (pages) | 51 (17 groups x 3) |
| Thread pool | 15 |
| Threads per page | 5 |
| Edge criterion | overlap >= 3 (within-group, identical threads) |
| Non-edge criterion | overlap <= 2 (between-group signatures) |
| Target MIS | 17 |
| MIS/N | 0.333 |
| MIS solutions | 129,140,163 |
| Rigidity | 0.000 |
| Expected density | 0.040 |
| Expected edges | 51 (3 per group x 17) |
| Recommended k | 4 or 8 |
| Recommended threshold | 0.78 |

### Thread Pool (15 threads)

| # | Thread (EN) | Thread (FR) | Domain |
|---|-------------|-------------|--------|
| 0 | WAGER | PARI | Probability, risk |
| 1 | CHRONICLE | CHRONIQUE | Historical record |
| 2 | CONSPIRACY | COMPLOT | Fabrication, forgery |
| 3 | TONGUE | LANGUE | Language, vernacular |
| 4 | NUMBER | NOMBRE | Mathematics |
| 5 | FAITH | FOI | Belief, doubt |
| 6 | SWORD | EPEE | War, conflict |
| 7 | PARCHMENT | PARCHEMIN | Manuscripts |
| 8 | MALIETTE | MALIETTE | The teacher |
| 9 | GAME | JEU | Ludic constraint |
| 10 | MIRROR | MIROIR | Reflection |
| 11 | INK | ENCRE | Writing |
| 12 | SHADOW | OMBRE | Hidden meaning, the unsaid |
| 13 | FIRE | FEU | Destruction, purification, passion |
| 14 | STONE | PIERRE | Permanence, architecture, foundation |

### Thread Assignment Table

Within each group of 3, all pages share IDENTICAL thread sets. The pages
differ only in their textual content, not their thematic threads. This creates
perfect K_3 cliques within groups and guarantees rho=0.

17 group signatures, pairwise overlap <= 2 (verified):

| Group | Pages | Threads |
|-------|-------|---------|
| G00 | P01-P03 | CHRONICLE, CONSPIRACY, GAME, FIRE, STONE |
| G01 | P04-P06 | CONSPIRACY, PARCHMENT, INK, SHADOW, STONE |
| G02 | P07-P09 | CHRONICLE, CONSPIRACY, NUMBER, FAITH, PARCHMENT |
| G03 | P10-P12 | CHRONICLE, TONGUE, NUMBER, GAME, INK |
| G04 | P13-P15 | CONSPIRACY, SWORD, MIRROR, SHADOW, FIRE |
| G05 | P16-P18 | FAITH, MALIETTE, INK, FIRE, STONE |
| G06 | P19-P21 | WAGER, NUMBER, SWORD, GAME, FIRE |
| G07 | P22-P24 | CHRONICLE, NUMBER, SWORD, MALIETTE, MIRROR |
| G08 | P25-P27 | WAGER, TONGUE, FAITH, MIRROR, SHADOW |
| G09 | P28-P30 | TONGUE, MALIETTE, GAME, MIRROR, FIRE |
| G10 | P31-P33 | WAGER, TONGUE, SWORD, PARCHMENT, STONE |
| G11 | P34-P36 | FAITH, PARCHMENT, GAME, MIRROR, INK |
| G12 | P37-P39 | WAGER, CONSPIRACY, SWORD, MALIETTE, INK |
| G13 | P40-P42 | WAGER, CHRONICLE, PARCHMENT, MIRROR, FIRE |
| G14 | P43-P45 | NUMBER, PARCHMENT, MALIETTE, GAME, SHADOW |
| G15 | P46-P48 | CONSPIRACY, TONGUE, FAITH, SWORD, GAME |
| G16 | P49-P51 | NUMBER, FAITH, SWORD, SHADOW, STONE |

**Constraint verification**:
- Within-group edges: 51/51 (all 3 pairs per group connected). PASS.
- Between-group isolation: 1224/1224 (all inter-group pairs have overlap <= 2). PASS.
- Rigidity: 0.000 (every MIS node replaceable by 2 alternatives). PASS.

### Literary Framing

Title: **"Le Kaleidoscope"** (The Kaleidoscope)

Each group of 3 pages tells the "same" story from 3 equally valid perspectives.
The 17 groups cover 17 themes; the reader must choose one perspective per theme.
Any combination is a complete reading. There is no "correct" path.

Structure: 17 triptychs. Each triptych presents the same thematic material
through three different lenses:
- Version A: the WITNESS (first person, sensory, immediate)
- Version B: the ANALYST (third person, critical, distant)  
- Version C: the DREAMER (second person, speculative, counterfactual)

The literary constraint: the three versions of each triptych must use the same
5 thematic threads with equal density, so that the embedding cannot distinguish
them by topic -- only by voice and style. This forces the graph to see them
as interchangeable.

This is the anti-Dante: a text where no reading is privileged, where every
backbone page has an equally valid substitute, where the author deliberately
builds structural redundancy rather than structural necessity.

---

## Design C: Planar Graph -- "La Carte du Texte" (The Map of the Text)

### Target Property

**Planar graph**: the similarity graph can be embedded in the plane without
edge crossings. This has three important consequences:

1. **QPU native**: 2D atom arrays ARE planar graphs. A planar text's similarity
   graph can be directly encoded on a neutral-atom QPU (Pasqal FRESNEL) with
   SA fidelity = 1.0 by construction. No embedding optimization needed.

2. **Four-color theorem**: the graph is 4-colorable, so MIS >= N/4.

3. **Structural sparsity**: planar graphs satisfy E <= 3N-6. For N=50:
   at most 144 edges, density <= 0.118.

### Mathematical Mechanism

Use a **5x10 grid graph** (50 nodes, 85 edges). Each node connects to its
horizontal and vertical neighbors only. Grid graphs are planar (trivially
embeddable), bipartite, and have well-understood MIS properties.

The grid structure is enforced through thread assignment: adjacent grid
positions share >= 3 of their 5 threads; non-adjacent positions share <= 2.
With 20 threads and 5 per page, the combinatorial space is large enough to
achieve perfect edge/non-edge separation (0 violations in SA optimization).

### Why 20 Threads Are Needed

With T threads, t per page, the probability of accidental overlap >= 3 between
two random pages is:

| T | t | P(overlap >= 3) | Expected false edges (of 1140) |
|---|---|-----------------|-------------------------------|
| 10 | 5 | 0.500 | 570 |
| 15 | 5 | 0.073 | 83 |
| 20 | 5 | 0.026 | 30 |
| 25 | 5 | 0.010 | 11 |

With 10 threads: 570 false edges swamp the 85 real edges. Impossible.
With 15 threads: 83 false edges is close to 85 real edges. Tight.
With 20 threads: 30 false edges vs 85 real. SA can eliminate all 30. Works.

The SA optimizer found a solution with **85/85 edges correct, 0 false edges**.

### Design Parameters

| Parameter | Value |
|-----------|-------|
| N (pages) | 50 |
| Graph topology | 5x10 grid |
| Thread pool | 20 |
| Threads per page | 5 |
| Edge criterion | overlap >= 3 |
| Non-edge criterion | overlap <= 2 |
| Edges | 85 |
| Density | 0.069 |
| MIS (greedy) | 23 |
| MIS/N | 0.460 |
| Chromatic number | 2 (bipartite) |
| Recommended k | 4 |
| Recommended threshold | 0.78 |

Note: MIS/N = 0.46 is higher than the natural-text ratio (~0.37) because grid
graphs are bipartite with MIS = N/2 for even grids. The checkerboard coloring
gives MIS = 25; greedy finds 23. This elevated ratio is a PREDICTION of the
planar constraint -- it should be verifiable after text generation.

### Thread Pool (20 threads)

| # | Thread (EN) | Thread (FR) | Domain |
|---|-------------|-------------|--------|
| 0 | WAGER | PARI | Probability, risk |
| 1 | CHRONICLE | CHRONIQUE | Historical record |
| 2 | CONSPIRACY | COMPLOT | Fabrication |
| 3 | TONGUE | LANGUE | Language |
| 4 | NUMBER | NOMBRE | Mathematics |
| 5 | FAITH | FOI | Belief |
| 6 | SWORD | EPEE | War |
| 7 | PARCHMENT | PARCHEMIN | Manuscripts |
| 8 | MALIETTE | MALIETTE | The teacher |
| 9 | GAME | JEU | Constraint |
| 10 | MIRROR | MIROIR | Reflection |
| 11 | INK | ENCRE | Writing |
| 12 | SHADOW | OMBRE | Hidden meaning |
| 13 | FIRE | FEU | Destruction, passion |
| 14 | STONE | PIERRE | Permanence |
| 15 | WATER | EAU | Flow, time, erosion |
| 16 | WIND | VENT | Change, inspiration, breath |
| 17 | IRON | FER | Industry, tools, forge |
| 18 | SILK | SOIE | Luxury, trade, texture |
| 19 | BONE | OS | Mortality, relics, archaeology |

### Thread Assignment Table

5x10 grid layout (row, column). Each page connects to its 2-4 grid neighbors.

| Page | Grid | MIS | Threads |
|------|------|-----|---------|
| P01 | r0c0 | MIS | BONE, CHRONICLE, FIRE, GAME, WATER |
| P02 | r0c1 | --- | BONE, FIRE, GAME, NUMBER, WIND |
| P03 | r0c2 | MIS | BONE, CONSPIRACY, FIRE, IRON, WIND |
| P04 | r0c3 | --- | BONE, FIRE, IRON, MIRROR, WAGER |
| P05 | r0c4 | MIS | CHRONICLE, FAITH, FIRE, MIRROR, WAGER |
| P06 | r0c5 | --- | CONSPIRACY, FAITH, FIRE, MIRROR, STONE |
| P07 | r0c6 | MIS | FAITH, FIRE, MALIETTE, NUMBER, STONE |
| P08 | r0c7 | --- | FAITH, NUMBER, PARCHMENT, STONE, WAGER |
| P09 | r0c8 | --- | FAITH, PARCHMENT, SILK, WAGER, WIND |
| P10 | r0c9 | MIS | BONE, CHRONICLE, FAITH, SILK, WIND |
| P11 | r1c0 | --- | BONE, CHRONICLE, INK, NUMBER, WATER |
| P12 | r1c1 | MIS | CHRONICLE, FIRE, INK, NUMBER, WIND |
| P13 | r1c2 | --- | CHRONICLE, FIRE, IRON, SHADOW, WIND |
| P14 | r1c3 | MIS | BONE, CHRONICLE, IRON, MIRROR, SHADOW |
| P15 | r1c4 | --- | CHRONICLE, FAITH, INK, IRON, MIRROR |
| P16 | r1c5 | MIS | FAITH, INK, MIRROR, SILK, STONE |
| P17 | r1c6 | --- | FAITH, IRON, MALIETTE, SILK, STONE |
| P18 | r1c7 | MIS | IRON, NUMBER, PARCHMENT, SILK, STONE |
| P19 | r1c8 | --- | NUMBER, PARCHMENT, SILK, TONGUE, WIND |
| P20 | r1c9 | --- | BONE, SILK, SWORD, TONGUE, WIND |
| P21 | r2c0 | MIS | BONE, FAITH, INK, NUMBER, SHADOW |
| P22 | r2c1 | --- | INK, MALIETTE, NUMBER, SHADOW, WIND |
| P23 | r2c2 | MIS | INK, IRON, PARCHMENT, SHADOW, WIND |
| P24 | r2c3 | --- | IRON, MIRROR, PARCHMENT, SHADOW, WATER |
| P25 | r2c4 | MIS | INK, IRON, MIRROR, SWORD, WATER |
| P26 | r2c5 | --- | FAITH, INK, STONE, SWORD, WATER |
| P27 | r2c6 | MIS | FAITH, GAME, IRON, STONE, SWORD |
| P28 | r2c7 | --- | IRON, PARCHMENT, STONE, SWORD, TONGUE |
| P29 | r2c8 | --- | NUMBER, PARCHMENT, SHADOW, SWORD, TONGUE |
| P30 | r2c9 | MIS | CHRONICLE, SHADOW, SILK, SWORD, TONGUE |
| P31 | r3c0 | --- | BONE, GAME, INK, SHADOW, TONGUE |
| P32 | r3c1 | MIS | GAME, INK, MALIETTE, SHADOW, SILK |
| P33 | r3c2 | --- | GAME, INK, IRON, MALIETTE, PARCHMENT |
| P34 | r3c3 | MIS | CHRONICLE, IRON, MALIETTE, PARCHMENT, WATER |
| P35 | r3c4 | --- | CONSPIRACY, IRON, MALIETTE, SWORD, WATER |
| P36 | r3c5 | MIS | CONSPIRACY, SHADOW, STONE, SWORD, WATER |
| P37 | r3c6 | --- | CONSPIRACY, GAME, STONE, SWORD, WAGER |
| P38 | r3c7 | MIS | MALIETTE, STONE, SWORD, TONGUE, WAGER |
| P39 | r3c8 | --- | MALIETTE, MIRROR, NUMBER, SWORD, TONGUE |
| P40 | r3c9 | --- | CHRONICLE, GAME, MIRROR, SWORD, TONGUE |
| P41 | r4c0 | MIS | FIRE, GAME, INK, TONGUE, WAGER |
| P42 | r4c1 | --- | CONSPIRACY, FIRE, GAME, INK, SILK |
| P43 | r4c2 | MIS | CONSPIRACY, FIRE, GAME, MALIETTE, PARCHMENT |
| P44 | r4c3 | --- | CHRONICLE, CONSPIRACY, MALIETTE, PARCHMENT, WIND |
| P45 | r4c4 | MIS | CONSPIRACY, MALIETTE, WAGER, WATER, WIND |
| P46 | r4c5 | --- | BONE, CONSPIRACY, SHADOW, WAGER, WATER |
| P47 | r4c6 | MIS | BONE, CONSPIRACY, SILK, STONE, WAGER |
| P48 | r4c7 | --- | SILK, STONE, TONGUE, WAGER, WATER |
| P49 | r4c8 | --- | MIRROR, NUMBER, TONGUE, WAGER, WATER |
| P50 | r4c9 | MIS | CONSPIRACY, GAME, MIRROR, TONGUE, WATER |

**Constraint verification (SA cost = 3.0, effectively 0)**:
- Edge satisfaction: 85/85 grid edges have overlap >= 3. PERFECT.
- Non-edge violations: 0 (no non-adjacent pair has overlap >= 3). PERFECT.
- Thread balance: min=12, max=15, mean=12.5 per thread.

### How Planarity Interacts with k-NN

The critical insight: with k=4 (or even k=8), the k-NN graph on this text
should closely match the designed grid graph, because:

1. Each page has 2-4 grid neighbors with high similarity (overlap 3/5).
2. All non-neighbors have low similarity (overlap <= 2/5).
3. With k=4, each page selects its 4 most similar neighbors -- which are
   exactly its grid neighbors.

At k=8, some non-neighbor pages might enter the top-8 due to random
similarity variation, but the SA optimization eliminated ALL overlap >= 3
violations, so this risk is minimal. Use k=4 for purest planarity.

### QPU Implications

A planar graph is directly embeddable in a 2D atom array. For the 5x10 grid:
- Place 50 atoms in a 5x10 rectangular lattice
- Set inter-atom spacing = R_blockade (e.g., 8.0 um for FRESNEL)
- The Rydberg blockade naturally creates the grid adjacency
- SA fidelity = 1.0 by construction (no embedding gap)
- The QPU solves the MIS problem on the exact designed graph

This eliminates the fidelity-density anticorrelation that plagues
non-planar graphs on 2D hardware.

### Literary Framing

Title: **"La Carte du Texte"** (The Map of the Text)

The constraint is geographical: each page occupies a position on a 5x10 map.
Adjacent pages (sharing a border on the map) must be thematically connected.
Non-adjacent pages must be thematically distinct.

Structure: the map represents a physical landscape:
- Row 0 (north): the MOUNTAIN (FIRE, STONE, BONE, WIND)
- Row 1 (uplands): the SCRIPTORIUM (CHRONICLE, INK, IRON, SHADOW)
- Row 2 (valley): the BATTLEFIELD (SWORD, FAITH, PARCHMENT, WATER)
- Row 3 (lowlands): the MARKET (GAME, MALIETTE, CONSPIRACY, SILK)
- Row 4 (south): the SEA (WATER, WIND, TONGUE, WAGER)

The reader traverses the map. The MIS backbone (23 pages) forms a checkerboard
pattern: reading only the MIS pages covers the entire landscape without
redundancy. But the 27 non-MIS pages fill in details between the landmarks.

The four-color theorem metaphor: the text needs only 4 "voices" to ensure
no two adjacent pages share the same narrator. This is guaranteed by the
bipartite structure of the grid (which needs only 2 colors).

---

## Comparative Summary

| Property | Design A | Design B | Design C |
|----------|----------|----------|----------|
| Title | Le Livre Irremplacable | Le Kaleidoscope | La Carte du Texte |
| Target rho | 1.000 | 0.000 | N/A (MIS/N focus) |
| N | 50 | 51 | 50 |
| Thread pool | 12 | 15 | 20 |
| Threads/page | 6 | 5 | 5 |
| MIS | 17 | 17 | 23 |
| MIS/N | 0.340 | 0.333 | 0.460 |
| MIS solutions | 1 | 129 million | TBD |
| Density | 0.234 | 0.040 | 0.069 |
| Graph type | Heterogeneous | 17 x K_3 | 5x10 grid |
| Key constraint | Double domination | Clique isolation | Planarity |
| Recommended k | 8-12 | 4-8 | 4 |
| SA fidelity (2D QPU) | < 1.0 | 1.0 (trivial) | 1.0 (native) |

### Key Mathematical Insight: Thread Pool Size Controls Graph Complexity

The fundamental trade-off discovered during this design process:

- **10 threads, 5/page**: P(accidental edge) = 50%. Only works for DENSE graphs
  (d > 0.30). This is why the original OuLiPo 50 EN works at k=16.

- **12 threads, 6/page**: P(accidental edge with overlap >= 4) ~ 5%.
  Works for moderate density with strong edge criterion.

- **15 threads, 5/page**: P(accidental edge) = 7%. Works for ISOLATED
  clusters (rho=0 design) with well-separated signatures.

- **20 threads, 5/page**: P(accidental edge) = 2.6%. Works for SPARSE
  planar graphs (d < 0.10) requiring near-perfect edge/non-edge separation.

**General rule**: sparse, structured graphs require more threads.
Dense, uniform graphs can use fewer threads.

---

## Implementation Notes

### Writing Constraints

All three texts must follow the established OuLiPo writing rules:
- ~370 words per page (E5-large requires this for reliable embedding)
- 2-3 thread keywords per sentence
- Pages sharing >= (edge threshold) threads must achieve cosine sim > 0.78
- Pages sharing <= (non-edge threshold) threads must achieve cosine sim < 0.78
- Thread keywords must be the THEMATIC terms (from the thread domain), not
  just the thread name itself

### Validation Pipeline

After text generation:
1. Run `build_topic_graph.py` with appropriate k and threshold
2. Verify edge fidelity (designed edges present, designed non-edges absent)
3. Run ILP MIS solver to enumerate all MIS solutions
4. Compute rigidity rho = |essential nodes| / |MIS|
5. For Design C: verify planarity (e.g., Boyer-Myrvold algorithm)
6. Submit to EMU_MPS for quantum validation
7. For Design C: submit directly to FRESNEL QPU (no SA embedding needed)

### File Dependencies

- Embedder: `intfloat/multilingual-e5-large` (1024-dim)
- Graph builder: `3_MIS/classical/core/build_topic_graph.py`
- MIS solver: PuLP/CBC via `3_MIS/classical/core/pasqal_emulator.py`
- SA embedding: `3_MIS/classical/core/pasqal_emulator.py`
- UDG generator: `3_MIS/oulipo/generators/gen_udg_fast.py`
