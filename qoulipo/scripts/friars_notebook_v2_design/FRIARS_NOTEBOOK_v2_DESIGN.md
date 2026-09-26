# The Friar's Notebook — v2 design

Reengineered thread-assignment for recovery of the Pacioli dodecahedron graph
at k=3 cosine k-NN (and cleanly near-dodecahedral at k≤8).

## Target graph

Regular dodecahedron, 3-regular on N=20: 30 edges, density 0.158, α=8 (MIS=8),
five maximum independent sets (ρ=0 on the 5-MIS set).

## v1 diagnosis (why current text fails)

v1 used 10 broad thematic threads (Franciscan rule, divine proportion, gold
leaf, ledger, perspective, Platonic solids, friendship with Leonardo, light,
mortality, Sansepolcro). Every page drew from the same small well, so
`multilingual-e5-large-instruct` cosine similarity between any two pages
reflected the shared Pacioli–Franciscan–geometry style signal, not specific
edge-level sharing. Measured at k=8: d=0.511 (~97 edges vs. the target 30),
MIS=6 (not 8), ρ=0.667 (not 0).

## v2 principle

**One motif per dodecahedron edge, not per page.** Edges are the primitive.
Each page carries exactly 3 motifs, one per incident edge. Motifs are narrow,
concrete, keyword-distinctive. Non-adjacent pages share 0 motifs; adjacent
pages share exactly 1.

Parameters:
- T = 30 motifs (one per edge)
- m = 3 motifs per page
- τ = 1 (edge iff ≥1 shared motif)
- Each motif is saturated in its 2 endpoint pages (2–3 keyword mentions each)
  and absent from the other 18.

Expected graph at k=3: exact dodecahedron (30 edges, d=0.158).
At k=8: dodecahedron plus residual style-similarity edges — tighter than v1
but probably still >30 edges. Report at k=3 as a "register-geometry target
at the construction-specified k" per main.tex:492.

## 20 pages × 20 registers (unchanged from v1)

| Page | Register (v1) | Dodec. vertex |
|------|---------------|---------------|
| 1 | confession | v00 |
| 2 | ledger entry | v01 |
| 3 | sonnet | v02 |
| 4 | mathematical demonstration | v03 |
| 5 | letter to Leonardo | v04 |
| 6 | workshop inventory | v05 |
| 7 | dream | v06 |
| 8 | recipe (egg tempera & gold leaf) | v07 |
| 9 | sermon fragment | v08 |
| 10 | architectural specification | v09 |
| 11 | travel diary | v10 |
| 12 | wager / probability problem | v11 |
| 13 | dialogue (Platonic manner) | v12 |
| 14 | prayer | v13 |
| 15 | astrological note | v14 |
| 16 | epitaph | v15 |
| 17 | musical proportion table | v16 |
| 18 | library catalogue | v17 |
| 19 | vision | v18 |
| 20 | last page (unfinished) | v19 |

## 30 motifs (one per edge)

Each motif lists the two endpoint pages and 4 keyword anchors. The keywords
must appear 2–3 times in each endpoint page, saturated enough to dominate
the cosine signal over the shared-register background.

| Edge ID | Pages (register pair) | Motif title | Keyword anchors |
|---|---|---|---|
| e01 | 1 · 9 (confession · sermon) | The Rose Window | rose-window, twelve-petal, Sext-hour, counting-the-points |
| e02 | 1 · 10 (confession · architectural) | The Host Inscribed | inscribed-square, elevation-wafer, nested-circles, three-breaths |
| e03 | 1 · 11 (confession · travel) | Breviary Marks | Psalm-103, pricked-margin, five-bodies, breviary-corner |
| e04 | 2 · 11 (ledger · travel) | Mule-Train Account | pack-mule, Milan-road, carriage-fee, scudi |
| e05 | 2 · 12 (ledger · wager) | Monte dei Paschi Entry | Monte-dei-Paschi, Siena-bank, compound-interest, florin |
| e06 | 2 · 16 (ledger · epitaph) | The Closing Balance | final-reckoning, debit-column, credit-column, balanced-book |
| e07 | 3 · 10 (sonnet · architectural) | Sansepolcro Keystone | keystone, sandstone-ashlar, Borgo-arch, stonemason-mark |
| e08 | 3 · 14 (sonnet · prayer) | The Gold-Leaf Angel | gold-leaf, gilded-halo, angel-panel, illumined-margin |
| e09 | 3 · 15 (sonnet · astrological) | Saturn's Quartering | Saturn, quartering, seventh-house, orbital-arc |
| e10 | 4 · 14 (math · prayer) | Euclid VI.30 | division-extreme-mean, Euclid-VI.30, golden-section, φ-ratio |
| e11 | 4 · 16 (math · epitaph) | Demonstration Interrupted | Q.E.D., demonstration-broken, Euclid-lemma, proof-margin |
| e12 | 4 · 18 (math · library) | Manuscript V.27 | folio-V.27, vellum-codex, manuscript-hand, codex-shelf |
| e13 | 5 · 9 (letter · sermon) | Leonardo's Lamp | Leonardo, oil-lamp, chiaroscuro-studio, studio-flame |
| e14 | 5 · 13 (letter · dialogue) | The Milan Conversation | Milan-walk, Sforza-court, conversation-at-dusk, dialogue-street |
| e15 | 5 · 17 (letter · musical) | The String Ratio | gut-string, 2:3-fifth, Pythagorean-tuning, monochord |
| e16 | 6 · 12 (workshop · wager) | The Apprentice's Bet | apprentice, wager-pot, dice-throw, triple-six |
| e17 | 6 · 17 (workshop · musical) | Brush and Lute | sable-brush, lute-fret, workshop-lute, varnish-lute |
| e18 | 6 · 19 (workshop · vision) | The Tempera Vision | egg-yolk, tempera-jar, binder-recipe, pigment-grind |
| e19 | 7 · 13 (dream · dialogue) | Jacob's Ladder | Jacob-ladder, ladder-rungs, ascending-angels, oneiric-step |
| e20 | 7 · 15 (dream · astrological) | The Seven Planets | seven-planets, planetary-hour, Venus-dream, Mars-augury |
| e21 | 7 · 20 (dream · last-page) | The Dodecahedron Unfinished | dodecahedron-dream, twelve-face, aether-fifth, unfinished-vision |
| e22 | 8 · 18 (recipe · library) | The Pigment Catalogue | lapis-lazuli, malachite-green, cinnabar-vermilion, pigment-receipt |
| e23 | 8 · 19 (recipe · vision) | The Gilder's Vision | gold-leaf-gilder, bole-red, agate-burnisher, gilding-light |
| e24 | 8 · 20 (recipe · last-page) | Recipe Broken Off | yolk-measure, vinegar-drop, recipe-breaks, ingredient-list |
| e25 | 9 · 12 (sermon · wager) | Pascal Before Pascal | probability-of-salvation, wager-for-soul, infinite-gain, finite-stake |
| e26 | 10 · 13 (architectural · dialogue) | The Borgo Façade | borgo-façade, pilaster-order, entablature-line, proportional-elevation |
| e27 | 11 · 14 (travel · prayer) | The Franciscan Road | Franciscan-rule-road, wayside-shrine, pilgrim-step, tertiary-cord |
| e28 | 15 · 18 (astrological · library) | The Almagest Margin | Ptolemy-Almagest, star-chart, margin-note, zodiac-table |
| e29 | 16 · 19 (epitaph · vision) | The Tomb of Light | tomb-inscription, light-beam-tomb, stone-lettering, last-light |
| e30 | 17 · 20 (musical · last-page) | The Unfinished Fugue | fugue-subject, counterpoint-line, interval-9:8, broken-cadence |

## Per-page motif assignment (the thread matrix)

Each page carries 3 motifs — one per incident dodecahedron edge.

| Page | Register | Motifs (3) |
|------|----------|------------|
| 1 | confession | e01, e02, e03 |
| 2 | ledger entry | e04, e05, e06 |
| 3 | sonnet | e07, e08, e09 |
| 4 | math demo | e10, e11, e12 |
| 5 | letter to Leonardo | e13, e14, e15 |
| 6 | workshop inventory | e16, e17, e18 |
| 7 | dream | e19, e20, e21 |
| 8 | recipe | e22, e23, e24 |
| 9 | sermon | e01, e13, e25 |
| 10 | architectural spec | e02, e07, e26 |
| 11 | travel diary | e03, e04, e27 |
| 12 | wager | e05, e16, e25 |
| 13 | dialogue (Platonic) | e14, e19, e26 |
| 14 | prayer | e08, e10, e27 |
| 15 | astrological note | e09, e20, e28 |
| 16 | epitaph | e06, e11, e29 |
| 17 | musical proportion | e15, e17, e30 |
| 18 | library catalogue | e12, e22, e28 |
| 19 | vision | e18, e23, e29 |
| 20 | last page (unfinished) | e21, e24, e30 |

Verification: each motif appears on exactly 2 pages; each page has exactly 3
motifs. Shared-motif count between pages i,j equals 1 if (i,j) is a dodec. edge
and 0 otherwise — identical to the dodecahedron adjacency matrix by construction.

## Prose-writing brief (applied per page)

For each page:

1. **Register discipline.** Keep the register voice pure (a confession must
   sound like a confession; a ledger entry must have dates, columns, debits;
   a sonnet must be 14 metrical lines; an epitaph must be lapidary).
2. **Motif saturation.** Each of the 3 motifs must surface 2–3 times in the
   ~370 words of the page, with at least 2 of its keyword anchors used
   verbatim or near-verbatim. Keywords should feel native to the register,
   not bolted on (e.g. a ledger entry uses "scudi" and "compound interest"
   naturally; a sonnet uses "Saturn" and "quartering" naturally).
3. **No motif leakage.** A page should NOT mention any keyword anchor from
   any motif it does not carry. This is the strictest constraint — it keeps
   non-adjacent pages at 0 shared motifs.
4. **Shared vocabulary budget.** Pacioli-world vocabulary that is not a motif
   keyword (e.g. "friar", "Sansepolcro", "proportion", "Leonardo", "brother")
   may recur across pages and will contribute to the style-similarity
   background. Keep the background bounded — prefer register-specific
   vocabulary where possible.
5. **Length.** 350–390 words per page, as in v1.

## Post-generation verification plan

After prose generation:
1. Embed all 20 pages with `intfloat/multilingual-e5-large-instruct`.
2. Build cosine-similarity matrix and top-k adjacency at k=3, k=5, k=8.
3. Check k=3 recovers the 30 dodecahedron edges exactly (target: TP=30, FP=0).
4. Compute MIS on the k=3 graph; target α=8, five optima, ρ=0.
5. If k=3 is not exact, diagnose which edges leaked and strengthen motif
   keywords in the offending pair.

## Table 5 update (when prose lands)

Current row (v1, k=8):
`The Friar's Notebook & 20 & 0.667 & 6 & 2 & 0.511 & Pacioli dodecahedron (target)`

Target row (v2, k=3):
`The Friar's Notebook & 20 & 0.000 & 8 & 5 & 0.158 & Pacioli dodecahedron (exact, k=3)`

Footnote in Appendix A.3: the text was reengineered after v1 measurement
showed register-style similarity dominating over thread-level signal; v2 uses
30 edge-specific motifs (one per dodecahedron edge) to make the designed
adjacency the dominant similarity signal.
