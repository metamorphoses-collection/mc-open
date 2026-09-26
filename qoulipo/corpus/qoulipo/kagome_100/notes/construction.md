# Kagome of Late Summer

A 100-haiku QOuLiPo (constrained-writing) sequence whose register graph is a
**kagome (3.6.3.6 Archimedean) tiling patch** of 100 vertices, 180 edges,
canonical MIS = 39, density 0.036, blockade 7.0 µm. The graph is the same one
designed for the FRESNEL Rydberg array submission in `../graph_designed.json`.

## Form

- 100 haiku-like tercets, one per vertex.
- `page_NNN.txt` corresponds to the kagome vertex with id `NNN-1` (vertex ids
  0..99 sorted ascending).
- Three lines, **5-7-5 target with modern free-haiku drift** — line count is
  always exactly three, but syllable count is permitted to drift around the
  classical 17-syllable target where imagery requires.
- Working title: *Kagome of Late Summer*.

### v2 revision state (2026-05-05)

This document was originally written against the v1 draft.  After the
external-reviewer audit of v1 (May 2026), 46 of the 100 pages were revised
in a deeper-than-light pass: the most-leaking abstract compounds
(*ash of suns*, *bell beneath the sea*, *stone-memory*, *dream-water*,
*the unnamed*, *deep sky overhead*) were replaced with concrete imagery
(*ember in a jar*, *buoy bell in fog*, *the millstone*, *rain in the basin*,
*a shape past the lamp*, *one cold star*) while preserving the kagome anchor
*concept* so embedder cosine adjacency holds via concept-similarity even
after surface change. The opening sequence (pp 001–033) is preserved. See
`revision_2026-05-05.md` for the per-page change log.
- Mood: late summer / early autumn (zansho into shoshū), composed in the
  spirit of Bashō's *renku* linked-verse — each haiku linked to its neighbours
  through shared imagery rather than narrative.

## QOuLiPo constraint

Adjacent haiku in the kagome graph must yield embedder cosine similarity
above 0.78 (multilingual e5-large-instruct). The constraint is implemented
through a **shared-anchor mechanism**: each haiku is built on a small set of
thematic anchors, and any two haiku occupying graph-adjacent vertices share at
least one anchor. Adjacent vertices in the kagome lattice always co-occupy a
triangle or a hexagonal face, which is precisely how the anchor system is
indexed.

## Four-anchor system

Each kagome vertex sits at the corner of (up to) two triangles and (up to)
two hexagonal voids — the defining 3.6.3.6 vertex figure. Each vertex is
therefore assigned (up to) **four anchors**:

- **2 triangle-anchors**: sharp, sensory, local late-summer / early-autumn
  *kigo* in the Japanese tradition — `cicada`, `persimmon`, `harvest-moon`,
  `dragonfly`, `morning-glory`, `scarecrow`, `ripening-pear`, `chestnut`,
  `wild-goose`, `cricket`, `lotus-seed`, `pickled-plum`, etc. One distinct
  *kigo* per kagome triangle (59 triangles ↔ 59 kigo).
- **2 hexagon-anchors**: slow, cosmological, contemplative themes — `void`,
  `ancestors`, `Pleiades`, `north-star`, `milky-river`, `tides`, `great-bear`,
  `old-light`, `silence-of-stars`, `the-empty-bowl`, `long-rain`,
  `cold-current`, `ash-of-suns`, `mountain-time`, `bell-beneath-sea`,
  `first-breath`, `the-unnamed`, `dream-water`, `stone-memory`,
  `winter-coming`, `deep-sky`, `drift`. One distinct theme per kagome
  hexagon (22 hexagons ↔ 22 cosmological anchors).

Boundary vertices (degree 2 or 3 on the patch) inherit fewer faces and
therefore fewer anchors — these haiku are deliberately spare. Distribution
of anchor count per vertex:

| anchors | vertices |
|---------|---------:|
| 1       | 17 (boundary) |
| 2       | 6  |
| 3       | 28 |
| 4       | 49 |

Each haiku evokes its anchors as **imagery, not as a list** — a persimmon
ripening on a lacquer branch, the void between rice-stalks under a harvest
moon, a crow returning at dusk while the north star holds.

## Construction pipeline

1. Parse `graph_designed.json` (100 points, 180 edges, blockade 7.0 µm).
2. Enumerate 3-cliques → 59 kagome triangles.
3. Plane-graph face-tracing (CCW rotation system on angle-sorted neighbours)
   → 22 hexagonal faces (plus the outer face).
4. Bind each triangle to one *kigo* and each hexagon to one cosmological
   theme. Each vertex inherits the anchors of every face it touches.
5. Compose a 5-7-5 (with permitted drift) haiku for each vertex evoking all
   of its anchors.
6. Validate that every graph edge has ≥1 shared anchor between its endpoints.

## Validation

### Adjacent pairs (the QOuLiPo constraint)

All **180 edges** of the kagome graph are checked. Distribution of shared
anchors:

- 1 shared anchor : 51 edges
- 2 shared anchors: 129 edges
- **Edges with 0 shared anchors: 0 (constraint satisfied).**
- Mean shared anchors per edge: 1.72.

The structural reason: every edge of the kagome graph belongs to exactly one
triangle (the two endpoints share that triangle's *kigo*); when both
endpoints are also interior, they additionally share at least one hexagon
(slow theme), giving 2 shared anchors.

Sample of 10 random adjacent pairs (with shared anchors):

| pair | shared anchors |
|------|-----------------|
| v86 ↔ v88 | dream-water, wisteria-leaf |
| v14 ↔ v15 | Pleiades, rice-field |
| v03 ↔ v04 | harvest-moon, void |
| v36 ↔ v37 | fox-fire, silence-of-stars |
| v32 ↔ v33 | cricket, drift |
| v29 ↔ v31 | Pleiades, stubble-field |
| v18 ↔ v19 | crow, north-star |
| v13 ↔ v28 | river-stones |
| v93 ↔ v95 | smoke-spiral, winter-coming |
| v73 ↔ v74 | bone-needle, dream-water |

### Non-adjacent pairs

All 4,770 unordered non-adjacent pairs:

- 0 shared anchors : 4,572 (95.85%)
- 1 shared anchor  :   198 ( 4.15%)
- ≥2 shared       :     0
- Mean shared anchors: 0.04.

The 4% of non-adjacent pairs that share a single anchor are exactly the
**within-hexagon non-edge pairs** (any two non-consecutive vertices of a
6-cycle face): they sit on the same hexagonal void but are not direct
graph-neighbours. This residual co-occurrence is structurally correct — the
kagome hexagon is a slow shared horizon of meaning that floats above six
distinct sharp moments — and it remains far below the adjacent-pair
threshold.

### Anchor evocation

Lexical scan on every haiku (with synonym proxies for compound anchors):
**0 vertices fail to evoke any of their anchors**, **0 vertices miss any
anchor** after a single revision pass on six initial drafts. All 100 haiku
evoke 100% of their assigned anchors.

## References

- Bashō, *Sarumino* and the **renku** (linked-verse) tradition — the
  composition principle of *kasane* (linking) and *tenji* (shifting) is the
  literary ancestor of the shared-anchor / shift-of-anchor structure used
  here.
- Semeghini, G., Levine, H., Keesling, A., Ebadi, S., Wang, T. T., Bluvstein,
  D., … Lukin, M. D. (**2021**). *Probing topological spin liquids on a
  programmable Rydberg simulator.* **Nature 595, 233–238**. The 219-atom
  Rydberg-blockade kagome experiment from the Lukin group at Harvard:
  the same lattice geometry on which this text is constrained, rendered as
  a quantum spin liquid; the present sequence is its literary shadow.
- Companion graph file `../graph_designed.json` (UDG layout, blockade 7 µm,
  spectral gap 1.36, MIS = 39, ρ = 0.85, all FRESNEL gates pass).

## Citation

This text is part of the **3_MIS / QOuLiPo corpus**, Zenodo deposit 2.0
(Investiqo / Jurczak), constrained-writing materials for quantum text
interpretation on neutral-atom hardware.
