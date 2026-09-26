# Hours of the Day — a QOuLiPo cycle of 91 tercets

A constrained poem-cycle whose graph is a triangular-lattice patch of 91
vertices arranged in 6 concentric hexagonal rings (1 + 6 + 12 + 18 + 24 + 30).
The graph parameters (ℓ = 7.5 µm, blockade = 8 µm, density = 0.059, MIS = 31,
ρ = 1.0) are designed for a Pasqal Rydberg-atom embedding; this folder
contains the literary realisation.

## Frame chosen — A. *Hours of the Day*

The cycle reads inside-out. The centre tercet (vertex id 45 → `page_046.txt`)
is **midnight, the well of the now**: the still point. Each successive ring
is a later hour of the long day, expanding outward through pre-dawn, dawn,
morning labour, noon, and afternoon-into-dusk at the edge.

Why this frame:

- It maps cleanly onto the radial geometry of six rings. The pilgrimage
  variant works (centre = shrine), but a pilgrim's journey is *inward*; the
  Hours of the Day frame allows the cycle to *unfold outward* from a still
  point, which is what the graph itself does.
- It echoes the medieval **Books of Hours** tradition without imposing the
  strict eight-fold canonical office (matins–lauds–prime–terce–sext–none–
  vespers–compline), which would not divide naturally into six rings.
- It permits a Dantean *terza rima* posture (without the rhyme constraint):
  three lines per station, the cycle as a slow descent-and-ascent of the
  day's arc, with the centre as the *punto* — *the still point of the
  turning world*, in Eliot's phrase.

## Ring-to-theme mapping

| Ring | # tercets | Theme | Core anchor pool |
|------|-----------|-------|------------------|
| 0 | 1 | The still point — midnight, the silent now | midnight, silence, stillness, clock, heart, well, centre, unmoving |
| 1 | 6 | First breath — pre-dawn hush, the lit wick | candle, wick, hush, ember, breath, whisper, lamp, watch, dark blue |
| 2 | 12 | The threshold — dawn at the door, dew | dawn, threshold, dew, door, grey, cock, first bell, hinge, window, mist, sill |
| 3 | 18 | The labour — morning hands, bread, road | bread, oven, road, hand, loom, ploughshare, needle, hammer, mortar, field, sheaf, apron, yoke, grain |
| 4 | 24 | The height — noon, zenith, marketplace | noon, sun, zenith, marketplace, wheat, scales, crier, brass, midday, stone, awning, white heat, tongue, coin |
| 5 | 30 | The dispersal — afternoon into dusk, vespers | shadow, afternoon, return, vespers, owl, dusk, ash, lantern, fold, gate, river, cloak, hearth, star, sleep, cooling |

## QOuLiPo constraint

Each tercet contains:

1. **≥ 2 words drawn from the anchor pool of its own ring**, and
2. **≥ 1 word drawn from each adjacent ring** it has graph neighbours in
   (so interior ring-N tercets borrow one inner-ring word and one
   outer-ring word; the centre borrows only outward; ring 5 borrows only
   inward).

The intent: a sentence-transformer embedding of two graph-adjacent
tercets should land at cosine > 0.78, because they share at least one
ring's anchor family. Two non-adjacent tercets at graph distance ≥ 3
will typically share less anchor mass and embed further apart.

The structural constraint above was audited on all 91 files. **All 91
tercets pass** (0 failures): every tercet has the required own-ring and
adjacent-ring anchor coverage. See `audit.json` in the parent folder for
graph metadata; the audit script was run during composition.

## Form

- 3 lines per tercet (Dantean spirit; no enforced *terza rima* rhyme,
  no syllable count). Lines may run long; punctuation is part of the
  metric.
- The centre poem (page 046, vertex 45) was written last, with extra
  care: it is the only piece that borrows nothing from a ring inside it,
  because there is none.
- File naming: `page_NNN.txt` ↔ vertex id NNN − 1.

## File layout

```
source/
├── page_001.txt … page_091.txt   # one tercet per file
└── README.md                      # this file
```

## Validation summary

- Ring counts (BFS hop distance from centre id 45):
  `[(0, 1), (1, 6), (2, 12), (3, 18), (4, 24), (5, 30)]` — matches the
  designed geometry exactly.
- Anchor-coverage audit: **0 / 91 tercets fail** the own ≥ 2,
  inner ≥ 1, outer ≥ 1 constraint.
- Sample of 50 adjacent edges: 48 % share at least one surface anchor
  word; the rest share a ring-family anchor (different surface word,
  same semantic class — e.g. *noon* / *midday* / *zenith*) which the
  sentence-transformer will collapse.

## References

- *Terza rima*: Dante Alighieri, *La Commedia* (c. 1308–21). The
  enchained-tercet form is the structural model; the rhyme is omitted
  because graph adjacency, not aural chiming, is what enchains here.
- **Books of Hours** tradition: see e.g. *Très Riches Heures du Duc de
  Berry* (Limbourg brothers, c. 1412–16). The marriage of an hour to an
  image, and an image to a station, is the lineage this cycle joins.
- Pilgrimage stations: medieval Stations-of-the-Cross cycles, and Hindu
  *parikrama* / Buddhist circumambulation, where radial movement around
  a still centre is itself the contemplation.
- T. S. Eliot, *Burnt Norton* (1936): "*At the still point of the
  turning world… there the dance is.*" The frame's name for the centre.
- OuLiPo & QOuLiPo: Queneau, Perec, Calvino on constrained writing.
  The added Q is for *quantum*: the graph this cycle inhabits is built
  to be embedded on a Rydberg-atom register; its MIS (= 31) is a
  literary parameter as much as a physical one.

## How to read

- **Linearly**, page 1 → 91, traces the angle-sorted tour: it is not
  chronological (the centre at page 046 sits in the middle of the
  ring-sorted order). The reader experiences the rings as they are
  numbered on the lattice.
- **Radially**, centre outward (page 046 → ring 1 → ring 2 → … → ring
  5), traces the unfolding day: midnight → dusk.
- **As a graph**: any adjacent pair (one of the 240 edges) is a
  thematically continuous diptych. The whole cycle is the day; any
  edge is a lit moment of it.
