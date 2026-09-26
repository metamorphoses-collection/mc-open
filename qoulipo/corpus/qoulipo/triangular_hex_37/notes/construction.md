# triangular_hex_37 — construction notes

## The graph

Triangular lattice cut to a regular hexagon at radius R=3 cells. 37 atoms
arranged in 4 concentric rings (1 + 6 + 12 + 18 = 37). Edge length ℓ =
7.5 µm, blockade radius R_b = 8.0 µm — a clean 2D unit-disk graph by
construction. 90 edges total, density 0.135. The smallest non-edge
distance is ℓ√3 ≈ 12.99 µm, giving a spectral-gap factor of 1.62 (well
above the 1.20 design floor).

## Why this shape

37 is the 4th centered hexagonal number (1, 7, 19, 37, 61, …). It is
the smallest hexagonal patch large enough to expose the full 6-fold
symmetry while remaining small enough to write as a coherent récit-prose
work (~2,800 words). The unique maximum independent set has 13
vertices (ρ = 1.0, single optimum) and traces a Star-of-David figure
inscribed in the outer hexagon: six corners, one centre, six inner
positions.

## Literary constraint stack

The book is composed under five Roubaudian constraints, all strictly
verifiable on the artefact:

### 1. Narrative-tense layers (informed by the geometric rings)

The four concentric rings of the graph (sizes 1/6/12/18) inspire four
French tense strata, running from the moment of writing outward in time:

| Ring | Atoms | Suggested tense |
|------|------|-------|
| 0 | 1 (centre) | présent indicatif (the moment of writing) |
| 1 | 6 (inner ring) | passé composé (le mois écoulé) |
| 2 | 12 (middle ring) | imparfait (l'année qui s'achève) |
| 3 | 18 (outer ring) | passé simple (le reste d'une vie) |

The actual prose tense distribution does not strictly follow the
geometric rings: the narrator drifts between tenses where the
narrative situation requires (e.g. an outer-ring memory sometimes
takes the imparfait when its content is iterative; an inner-ring
recent event sometimes takes the passé simple when its content is
punctual). The rings/tenses correspondence is a **narrative
inspiration**, not a strict mechanical assignment. The actual tense
classification per cell is in `reading_orders.json` under
`narrative_tense_layers`; the strict geometric ring grouping is under
`geometric_rings`.

The single centre cell (VII, atom 18) is the only cell in the present
indicative — the act of writing itself, the convergence of all six
directions of memory.

### 2. Wedges = themes (the M-axis)

The 6-fold rotational symmetry maps onto six thematic wedges of 60°
each. All six theme words begin with M, after Roubaud's habitual
letter-selection conceit:

| Wedge | Theme |
|------|------|
| 1 (E) | **M**er |
| 2 (NE) | **M**émoire |
| 3 (NW) | **M**arche |
| 4 (W) | **M**ort |
| 5 (SW) | **M**aison |
| 6 (SE) | **M**athématique |

### 3. Edges = exact surface-token lexical exclusions

The graph's 90 edges enforce **exact surface-token lexical exclusions**:
no two adjacent cells share a non-stoplisted content token under the
audit method documented in `notes/lexical_audit.md`. The blockade
constraint of the Rydberg Hamiltonian (no two adjacent atoms can be
simultaneously excited) is mirrored in the lexicon: no two adjacent
cells contain the same content token (after function-word filtering).

**Important precision.** This is an exact surface-token constraint
after a comprehensive French function-word stop-list, *not* a certified
French noun/verb lemma-disjointness theorem. A full lemma-level
guarantee would require integrating a French POS/lemmatizer (e.g.
spaCy `fr_core_news_lg` or treetagger) into the writing loop. That is
left as future work. What is verified is the surface-token constraint
under the documented audit, which catches all noun and verb
inflections that share a surface form.

**Verification (2026-05-06)**: independent French content-token audit
finds **0 of 90 edges** with any shared surface content token after
function-word filtering. **100% strict discharge.**

A residual stem-level overlap exists on **11 of 90 edges** (88% strictly
clean at stem level), where two adjacent cells share a morphological
root through inflection (e.g. *écrites/écris* across the centre cell
VII — the same verb in different tenses, which the constraint cannot
prohibit without breaking the present-indicative tense of the centre).
This is documented honestly and treated as acceptable residue.

### 4. MIS = the spine

The 13 MIS thèses, numbered I–XIII in Roman numerals (in `mis_analysis.json`,
not in the source files themselves), are the readable book. Each is a
brief declarative passage (~95–135 words) that opens on a date or a
place. The 24 non-MIS interstices, numbered 2–36 in arabic numerals, are
the connective tissue between the thèses they border on the graph; each
is shorter (~50–80 words).

### 5. Acrostic OLIVIER

The first letters of the opening MIS thèses I, II, III, IV, V, VI, VII
spell O-L-I-V-I-E-R — the dedicatee's name. The acrostic is silent:
visible only to those told it is there.

| Cell | First word | Letter |
|------|------|------|
| I    | Or | O |
| II   | Longtemps | L |
| III  | Il | I |
| IV   | Vivre | V |
| V    | Il | I |
| VI   | En | E |
| VII  | Rien | R |

## The Roubaud arc (cells V and VIII)

Cell **V** (atom 13, ring 2 imparfait, wedge Mémoire) plants the
meeting through Roubaud's *ε* (1967): a copy posed at coup soixante-
treize on a student's table at the rue Saint-Jacques. The book
precedes the man.

Cell **VIII** (atom 21, ring 3 passé simple, wedge Mémoire) closes
the arc thirty years later: the same copy, the same marked move, read
together. *"La jeunesse de l'un devint le souvenir de l'autre."*

These two cells are tied by the proper noun *ε* and by the move number
73, an actual move from the Go-game that orders Roubaud's sonnet
sequence.

The prose contains other proper nouns (place-names: Saint-Jacques, rue
de l'Ourcq, Villette, Lisbonne, Bretagne, Trez Bellec, Belle-Île),
serving as concrete anchors for the récit-prose register.

## Reading orders provided

A machine-readable list of all five reading orders is in
`reading_orders.json`.

1. **Linear:** `page_001` → `page_037` (table-of-contents reading)
2. **Concentric:** ring 0 → 1 → 2 → 3 (now → month → year → life)
3. **Sectorial:** traverse one wedge at a time (six themes)
4. **MIS-only spine:** read just the 13 thèses I → II → … → XIII
5. **Hex spiral:** graph traversal, every cell once

## Intertexts

- **Jacques Roubaud, ε** (1967, Gallimard) — 361 sonnets ordered by an
  actual Go game played on a 19×19 board. Cell V opens the copy at coup
  73; cell VIII returns to the same move three decades later. The
  number 73 is preserved exactly.
- **Jacques Roubaud, La Forme d'une ville change plus vite, hélas, que
  le cœur des humains** (1999) — the short-cell prose template, the
  arrangement of memory in numbered fragments.
- **Jacques Roubaud, Le Grand Incendie de Londres** (1989–) — récit-
  prose register, the architecture of branching memory.
- **Jacques Roubaud, Quelque chose noir** (1986) — the elegiac
  short-cell register adopted by the Mort wedge.
- **Marcel Proust, Du côté de chez Swann** — cell II opens with
  *Longtemps* (the first word of the *Recherche*).

## Validation

* **Graph layer**: N=37, E=90, MIS=13 unique (ρ=1.0), spectral gap 1.62×.
  ChatGPT independent audit (2026-05-06) confirms all graph-layer claims.
* **Acrostic**: O-L-I-V-I-E-R verified on first letters of MIS I–VII
  (`Or`, `Longtemps`, `Il`, `Vivre`, `Il`, `En`, `Rien`).
* **Edge constraint**: all 90 edges verified clean of shared surface
  content tokens (independent French stop-list audit, 2026-05-06,
  rounds 1 + 2 review; see `notes/lexical_audit.md`).
* **Olivier arc**: cells V and VIII both reference *ε* and the move
  *coup soixante-treize* explicitly; verifiable from the source.

## Revision history

* **2026-05-06 morning**: first draft (~1,400 words, compact-prose register).
* **2026-05-06 afternoon**: récit-prose expansion to ~2,900 words; ChatGPT
  round-1 review flagged a strict-claim/realised-prose gap (only 17%
  edges actually clean under audit).
* **2026-05-06 evening**: constraint-preserving revision in 3 passes;
  35 cells revised to discharge edge-level lexical exclusion (preserving
  OLIVIER acrostic, V/VIII Olivier arc, wedge themes, ring tenses).
  Re-audit reached 100% strict edge cleanness.
* **2026-05-06 late evening**: ChatGPT round-2 review flagged 3 remaining
  exact noun-like overlaps (`reste`, `fois`, `porte`); patched in
  pages 7, 15, 17. Constraint wording tightened from a lemma-level
  claim to an exact surface-token claim. `reading_orders.json` added.
