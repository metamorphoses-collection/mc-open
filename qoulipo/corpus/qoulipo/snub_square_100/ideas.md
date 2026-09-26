# snub_square_100: literary ideas

**Status (2026-05-05):** geometry verified via the Wikipedia
Cartesian-coordinate formula `s = √(2+√3)/4` with prototype offsets
`±(3-√3, √3-1)` and `±(-√3+1, 3-√3)` indexed by integer (4i, 4j).
N=100, edges=220, density 0.044, MIS=36, ρ=0.33, 97 optima, spectral
gap 1.31×. All 5 audit gates PASS. Submitted to FRESNEL_CAN1 as
batch `ee9b7c8e-5488-4f4e-8599-436618e810f7` (2026-05-05). Poetry
drafted 2026-05-05 (100 hybrid 7-line poems); a round-3 copy-edit
pass followed an external review.

## Title — *The Postman's Songbook*

(Working FR title was *Le Canzoniere de Robert Ammann*, retired in favour
of an English-language title 2026-05-05.)

Robert Ammann (1946–1994), postman by trade and autodidact mathematician,
independently discovered several aperiodic tilings (the Ammann–Beenker
tiling among them) and contributed to the Penrose-tile literature.
Published through Branko Grünbaum's encouragement in the 1980s.
A *canzoniere* of his — 100 short pieces alternating between two
prosodic forms, arranged on a snub-square (3.3.4.3.4) lattice — honours
both the mathematician and the medieval *girih* tradition
(Lu & Steinhardt, *Science* 315, 1106 (2007), revealed that
15th-century Persian craftsmen anticipated Penrose-style quasiperiodic
decoration on architectural surfaces, e.g. the Darb-i Imam shrine in
Isfahan, c. 1453).

## Form

Around every snub-square vertex, the polygon sequence is
**triangle, triangle, square, triangle, square** (3.3.4.3.4). The
literary form mirrors this with **two prosodic registers** mapped to
the two polygon types — short (triangle, 3 lines / tercet) and long
(square, 4 lines / quatrain).

- **Form B**: every poem is a hybrid: 3 lines (triangle register) +
  4 lines (square register), 7 lines total per vertex. 100 poems,
  uniform shape; the alternation between registers happens *within*
  each poem, mirroring the polygon-mix at each vertex.

## Anchor system

Each vertex sits at the corner of 3 triangles + 2 squares. Anchors:
- **50 girih-style geometric/architectural anchors** (one per triangle,
  ~50 triangles in the 100-vertex patch): *muqarnas, iwan, mihrab,
  zellige, mocárabe, azulejo, vault, spandrel, cupola, minbar, kufic,
  arabesque, interlace, star-polygon, quasiperiodic, dodecagram, octagram,
  cusp, lozenge, chamfer, oculus, lintel, jamb, courtyard, fountain, dome,
  archivolt, voussoir, keystone, riad, pishtaq, mashrabiya, squinch,
  pendentive, tympanum, alfiz, muqarnas-cell, girih-strap, tessera,
  faience, cuerda-seca, hexafoil, quatrefoil, cinquefoil, ablaq,
  stalactite, sebka, atauriques, mocárabe-tier, tracery*.
- **25 epistolary/postman anchors** (one per square): *envelope, postmark,
  return-address, dead-letter, post-office-box, third-shift, Route-19,
  Carlisle, parcel, delivery-slip, ZIP-code, sorted-bundle, twine,
  rural-carrier, mail-truck, undelivered, forwarding-slip, stamp-pad,
  registered, first-class, bulk-rate, window-clerk, loading-dock, mailbag,
  carrier-cart*.

Each vertex inherits up to 5 anchors (3 girih + 2 postman) by polygon
membership. Adjacent vertices share ≥1 anchor.

## Geometry path — solved 2026-05-05

The third attempt succeeded: explicit Cartesian coordinates from
Wikipedia's snub-square page, scale `s = √(2+√3)/4 ≈ 0.483`,
four prototype vertices per unit cell at `±s·(3-√3, √3-1)` and
`±s·(-√3+1, 3-√3)`, lattice constant `4s = √(2+√3) ≈ 1.932`. All four
prototype vertices form a unit-side rotated square; cross-cell unit
edges fall out of the integer indexing.

(Two earlier hand-rolled attempts had failed: vertex-walk with a
single chirality rule `α' = α + da - 90` gave collisions at ≈ 0.27ℓ
because chirality propagation depends on edge type (T→S, T→T, S→T)
across 3.3.4.3.4; square-first BFS with deterministic triangle-gluing
gave collisions at ≈ 1.5ℓ. The Wikipedia formula sidesteps the
chirality bookkeeping by providing the explicit per-orbit positions.)

## References (paper)

- Lu & Steinhardt, *Decagonal and Quasi-Crystalline Tilings in
  Medieval Islamic Architecture*, Science **315**, 1106 (2007).
- Conway, Burgiel, Goodman-Strauss, *The Symmetries of Things* (2008).
- Branko Grünbaum & G.C. Shephard, *Tilings and Patterns* (1987),
  §10.4 on snub tilings.
- Topkapı Scroll (Istanbul, c. 1453) — Persian girih design manual.
- Wikipedia, *Snub square tiling*, retrieved 2026-05-05 — explicit
  Cartesian coordinate formula.
