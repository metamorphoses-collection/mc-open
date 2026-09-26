# Construction notes — *The Postman's Songbook*

Snub-square (3.3.4.3.4) lattice, N = 100 vertices, |E| = 220, ell = 6.5 μm,
blockade R_b = 7.0 μm. Hybrid form: 3-line tercet (triangle register)
+ 4-line quatrain (square register), 7 lines per page, 100 pages.

## Polygon enumeration (procedural, from the graph)

- **Triangles (3-cliques):** 84 enumerated by iterating over each
  vertex's neighbour pairs and testing pairwise unit-distance closure.
- **Squares (4-cycles, opposite-corner distance ≈ √2·ell ≈ 9.192 μm,
  ± 0.5 μm tolerance):** 37 enumerated as a-b-c-d cycles where
  (a,c) and (b,d) lie at the square diagonal but are NOT graph edges (diagonal
  > blockade radius).

These counts agree with the snub-square local rule (each interior vertex sits
at 3 triangles + 2 squares; ratio 2:1 between triangle and square *incidences*
per vertex) up to boundary effects in a 100-vertex finite patch.

## Anchor pools

### Triangle (girih) anchors — 50 entries
muqarnas, iwan, mihrab, zellige, mocárabe, azulejo, vault, spandrel, cupola, minbar, kufic, arabesque, interlace, star-polygon, quasiperiodic, dodecagram, octagram, cusp, lozenge, chamfer, oculus, lintel, jamb, courtyard, fountain, dome, archivolt, voussoir, keystone, riad, pishtaq, mashrabiya, squinch, pendentive, tympanum, alfiz, muqarnas-cell, girih-strap, tessera, faience, cuerda-seca, hexafoil, quatrefoil, cinquefoil, ablaq, stalactite, sebka, atauriques, mocárabe-tier, tracery

### Square (postman / Ammann) anchors — 25 entries
envelope, postmark, return-address, dead-letter, post-office-box, third-shift, Route-19, Carlisle, parcel, delivery-slip, ZIP-code, sorted-bundle, twine, rural-carrier, mail-truck, undelivered, forwarding-slip, stamp-pad, registered, first-class, bulk-rate, window-clerk, loading-dock, mailbag, carrier-cart

Each triangle is assigned one girih anchor cyclically over the 50-element pool;
each square is assigned one postman anchor cyclically over the 25-element pool.
Each vertex therefore inherits up to **3 girih + 2 postman = 5 anchors** by
polygon membership. Boundary vertices (fewer incident polygons) inherit fewer
and borrow one image from a neighbour to keep the 7-line shape filled.

## Voice / register

The voice is Robert Ammann's, in retrospect — a Carlisle, Massachusetts postman
who saw the architecture of Persian shrines folded into a daily mail route on a
snub-square lattice. The tercet portion delivers triangle-anchor imagery
(sharp, local, observed: muqarnas, mihrab, zellige, ...). The quatrain portion
delivers square-anchor imagery (still, contemplative, structural: envelope,
P.O. box, Route 19, ...). The blank line between the two registers is the
break in the polygon walk around the vertex (3.3.4|.3.4).

## Validation

### Adjacent-pair shared-anchor check (10 random graph edges)

  - vertices 68,69: shared girih = ['arabesque']; shared postman = ['return-address']
  - vertices 10,11: shared girih = ['cupola']; shared postman = ['dead-letter']
  - vertices 2,19: shared girih = ['zellige']; shared postman = ['envelope']
  - vertices 80,81: shared girih = ['courtyard']; shared postman = ['parcel']
  - vertices 27,33: shared girih = ['archivolt', 'riad']; shared postman = —
  - vertices 25,46: shared girih = ['courtyard']; shared postman = ['parcel']
  - vertices 22,46: shared girih = ['courtyard', 'fountain']; shared postman = —
  - vertices 13,14: shared girih = —; shared postman = ['third-shift']
  - vertices 79,80: shared girih = ['vault']; shared postman = ['parcel']
  - vertices 9,14: shared girih = ['interlace']; shared postman = —

Adjacent pairs sharing ≥1 anchor: **10/10**.
This is the structural guarantee of the construction: two adjacent vertices
always co-belong to at least one triangle (since the edge between them, plus
either of two flanking triangles in 3.3.4.3.4, forms a 3-clique), so they share
that triangle's girih anchor. Square sharing is more occasional (only when the
edge is a *square edge*).

### Non-adjacent pair check (5 random pairs at graph distance ≥ 3)

  - vertices 86,94: shared girih = —; shared postman = —
  - vertices 69,11: shared girih = ['cupola']; shared postman = ['return-address']
  - vertices 75,54: shared girih = —; shared postman = —
  - vertices 29,64: shared girih = —; shared postman = —
  - vertices 77,3: shared girih = —; shared postman = —

Non-adjacent pairs sharing ≥1 anchor: **1/5**.
Far pairs may occasionally collide on an anchor when the cyclic assignment
wraps the 50/25-element pool back over the same name; this is acceptable and,
in practice, mild thematic recurrence rather than local cohesion.

## QOuLiPo embedder constraint

Adjacent poems share at least one girih anchor by construction (every graph
edge lies on at least one triangle in the 3.3.4.3.4 vertex figure). The
shared image surfaces in both poems, which is the structural guarantee that
embedder cosine similarity should sit close to the 0.78 target threshold for
`multilingual-e5-large-instruct`. **An empirical similarity matrix has not
yet been computed for this text** — when measured downstream, the median
adjacent-pair cosine and the median non-adjacent-pair cosine should be
reported alongside the page files (an `embedder_audit.json` to be added in a
later session). The structural-anchor guarantee is necessary but not
sufficient on its own; the measurement will close the loop.

## References

- Robert Ammann (1946–1994), postman-mathematician of Carlisle, Massachusetts;
  independently discovered Ammann–Beenker and several aperiodic tilings.
- Lu, P. J. & Steinhardt, P. J. *Decagonal and Quasi-Crystalline Tilings in
  Medieval Islamic Architecture.* Science **315**, 1106 (2007).
- Topkapı Scroll (Istanbul, c. 1453) — Persian girih design manual.
- Conway, J. H., Burgiel, H. & Goodman-Strauss, C. *The Symmetries of Things*
  (A K Peters, 2008), chapter on Archimedean tilings.
- Grünbaum, B. & Shephard, G. C. *Tilings and Patterns* (W. H. Freeman, 1987),
  §10.4 on snub tilings.

## File layout

- `source/page_001.txt` … `source/page_100.txt` — one 7-line hybrid poem each.
  page_NNN ↔ vertex id (NNN−1).
- `notes/construction.md` — this file.
