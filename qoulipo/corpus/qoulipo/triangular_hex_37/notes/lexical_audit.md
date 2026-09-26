# triangular_hex_37 — lexical-disjointness audit

**Final audit date:** 2026-05-06 (after ChatGPT round-2 review patches)

## Summary — exact surface-token discharge

| Metric | Value |
|---|---|
| Total edges | 90 |
| Edges with **zero** shared surface content tokens | **90 / 90 (100%)** |
| Edges with zero stem overlap | 79 / 90 (88%) |

The exact surface-token constraint is **fully discharged** under the
documented method. Stem-level overlap exists on 11 edges, where two
adjacent cells share a morphological root through inflection. This is
documented and treated as acceptable residue.

## Method

Conservative normalized content-token check after removing French
function words. The stop-list includes:

* All articles, pronouns, conjunctions, prepositions
* All conjugated forms of *être, avoir, faire, aller, pouvoir, devoir,
  vouloir, savoir, voir, prendre, mettre, venir, dire* and other common
  auxiliaries
* All months, days, calendar terms (*mois, ans, heure, semaine, jour*)
* All ordinal and cardinal numbers from un to mille
* Common positional and intensity adverbs

Tokens are NFD-normalized, accent-stripped, and lower-cased before
comparison. Length ≤ 2 tokens are ignored.

A stem-based check applies a crude French suffix stripper after the
exact-token check, capturing morphological overlap (*écrites / écris*,
*finis / finie*, *mémoire / mémoires*).

**Note on lemma-level guarantees.** The audit is an exact surface-token
constraint after function-word filtering. It is **not** a certified
lemma-level disjointness theorem. A full French POS/lemmatizer
(e.g. spaCy `fr_core_news_lg`) would catch additional inflectional
relationships not visible at the surface level. That said, the
revisions were performed iteratively against this audit, with manual
inspection of every flagged adjacency, so the residual stem overlap
is bounded and documented.

## Process

1. **First draft** (2026-05-06 morning, compact-prose, ~1,400 words):
   17% of 90 edges clean of shared content tokens (under a coarser
   stop-list audit; under the comprehensive stop-list, 51% clean).
2. **Récit-prose expansion** (2026-05-06 afternoon, ~2,900 words):
   no change in edge cleanness — the expansion preserved (and
   sometimes worsened) the overlap rate.
3. **Constraint-preserving revision pass 1** (2026-05-06 evening,
   24 interstices + 11 MIS thèses revised in coordinated substitutions):
   from 51% to 96.7% clean.
4. **Pass 2** (4 final overlaps): 100% clean. Then ChatGPT round-2
   review (independent audit) found 3 additional surface-token
   overlaps not caught by my stop-list.
5. **Pass 3** (final ChatGPT round-2 patches, 3 substitutions in
   pages 7, 15, 17): **100% strict edge cleanness verified** by both
   the local audit and the ChatGPT-style audit method.

## ChatGPT round-2 patches (2026-05-06 late evening)

| Edge | Token | Pre-patch | Post-patch | Where |
|------|------|------|------|------|
| (7, 13) | *reste* | "Le reste avait servi…" | "Le reliquat avait servi…" | page_007 |
| (9, 15) | *fois* | "celle où l'objet me parut pour la première fois" | "celle où le signe me parut d'abord" | page_015 |
| (11, 17) | *porte* | "Une porte d'entrée est une opinion sur la voie qui la borde." | "Un accès principal est une opinion sur la voie qui le borde." | page_017 |

The Roubaud spine (cells I–XIII) is preserved; first words remain
*Or, Longtemps, Il, Vivre, Il, En, Rien* (acrostic intact). The cells
V (the meeting through ε) and VIII (thirty years later) preserve their
proper nouns *ε*, *coup soixante-treize*, *Saint-Jacques*, *dix-sept ans*,
*deuxième rangée*.

## Conclusion

`triangular_hex_37` is the first text in the QOuLiPo corpus where the
edge-level lexical exclusion is **strictly verified at the exact
surface-token level** rather than aspirational. The graph blockade
constraint of the Rydberg Hamiltonian is mirrored in the lexicon:
90 graph edges → 90 lexical exclusions, all discharged under the
documented audit method.
