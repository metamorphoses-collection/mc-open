# 3_MIS/oulipo -- OuLiPo Constrained Texts

Literary texts written under graph-theoretic constraints: the structure comes first, the text follows.

---

## Core Concept

**Literary constraint = graph constraint.** In traditional OuLiPo, a formal rule (lipogram, prisoner's constraint, etc.) governs what the author may write. Here, the constraint is a target graph topology:

- Each page is assigned 5 threads drawn from a pool of 10.
- **Connected pages** (neighbors in the graph) must share >= 3 threads.
- **Disconnected pages** (non-neighbors) must share <= 1 thread.

The author writes each page so that its content naturally evokes exactly its assigned threads. If the constraint is satisfied, the resulting text's semantic embedding graph will match the target topology.

---

## What Worked

### v1: "Le Pari de Nithard" (50 pages, English)

- **Graph**: d = 0.31 at k=16 (THE instrument -- the text that validates the whole MIS framework)
- **Thread satisfaction**: high -- the 5-thread-per-page, 10-thread-pool design gives enough semantic contrast
- **MIS properties**: matches target graph structure. Demonstrates that MIS captures designed thematic architecture.
- **French translation**: v1b (50 pages, same structure, translated to French). Graph structure preserved across languages.
- **Files**: `texts/oulipo_nithard_pascal.md`, `texts/oulipo_v1b_50pages_fr.md`
- **Graphs**: `graphs/graph_oulipo_v1_50pages.json` (+ k8, k12, k16 variants)

---

## What Failed

### v2 / v2b (100 pages, English + French)

- **Problem**: scaled to 100 pages but reduced to 3 threads per page at 100 words per page.
- **Result**: mean cosine similarity = 0.49 -- too uniform. No graph structure emerges. The embedding cannot distinguish connected from disconnected pages when thread overlap is so low and pages so short.
- **Lesson**: the constraint design must ensure sufficient semantic contrast. 5 threads from 10 works; 3 threads from 10 at 100 words does not.
- **Revised versions** (v2r, v2br): attempted fixes, still insufficient contrast.
- **Files**: `texts/oulipo_v2_100pages.md`, `texts/oulipo_v2b_100pages_fr.md` (+ revised variants)

---

## UDG Texts: "Le Graphe Incarne"

A more radical approach: start from a pre-existing **Unit Disk Graph** (UDG) and write text to match it exactly.

| Text | Pages | Edge fidelity | Thread satisfaction | Status |
|------|-------|---------------|--------------------|---------| 
| UDG 65 | 65 | 99.4% edges correct | OK | Good |
| UDG 100 | 100 | varies | 44.4% thread satisfaction | Needs redo |
| UDG 50 (FRESNEL) | 50 | 1.0 by construction | OK | Submitted to QPU |

- **UDG 50 (FRESNEL)**: specifically designed for R_b = 8.0 um to satisfy FRESNEL_CAN1 QPU constraints. EMU running.
- **UDG 100**: thread satisfaction only 44.4% -- the 100-page scale with current thread design does not work. Needs redesign with more threads or longer pages.
- **UDG 65**: solid result, 99.4% edge fidelity.

---

## Quality Issues

The fundamental tension: embedding similarity is a continuous measure, but graph adjacency is binary. At 50 pages with 5 threads from 10, there is enough contrast. At 100 pages with 3 threads from 10, the embeddings become too similar across all page pairs, and the k-NN graph loses structure.

**Scaling OuLiPo texts beyond 50 pages requires either more threads, longer pages, or a fundamentally different constraint design.**

---

## File Layout

```
oulipo/
  texts/                              # All text files (.md)
    oulipo_nithard_pascal.md           # v1 EN (50 pages) -- THE successful text
    oulipo_nithard_pascal_v1_original.md
    oulipo_v1b_50pages_fr.md           # v1b FR (50 pages)
    oulipo_v1b_fr_part1.md / part2.md  # FR parts
    oulipo_v2_100pages.md              # v2 EN (100 pages) -- FAILED
    oulipo_v2_100pages_revised.md
    oulipo_v2b_100pages_fr.md          # v2b FR (100 pages) -- FAILED
    oulipo_v2b_100pages_fr_revised.md
    oulipo_v2_part1..4.md              # v2 parts
    oulipo_v2r_part1..4.md             # v2 revised parts
    oulipo_v2br_fr_part1..2.md         # v2b revised FR parts
    oulipo_udg100_text.md              # UDG 100 -- needs redo
    oulipo_udg65_text.md               # UDG 65 -- OK
    oulipo_udg_50pages.md              # UDG 50 (FRESNEL) -- submitted to QPU
  graphs/                              # Graph JSONs (nodes, edges, MIS)
    graph_oulipo_v1_50pages.json       # v1 base graph
    graph_oulipo_v1_50pages_k8_strict.json
    graph_oulipo_v1_50pages_k12.json
    graph_oulipo_v1_50pages_k16.json
    graph_oulipo_v1b_50pages_fr.json   # v1b FR graphs
    graph_oulipo_v1b_50pages_fr_k8.json
    graph_oulipo_v2_100pages.json      # v2 (failed)
    graph_oulipo_v2b_100pages_fr.json
    graph_oulipo_v2r_100pages_en.json
    graph_oulipo_v2br_100pages_fr.json
    graph_udg_65.json                  # UDG graphs
    graph_udg_100.json
    graph_udg50_fresnel.json           # UDG 50 designed for FRESNEL R_b=8.0um
    graph_oulipo_65.json
    graph_oulipo_udg.json
    oulipo_analysis_*.json             # Analysis results per variant
  threads/                             # Thread assignment files
    oulipo_udg65_threads.json          # Which threads assigned to which pages
    oulipo_udg100_threads.json
  generators/                          # UDG generation scripts
    gen_udg_fast.py
    gen_udg_v2.py
    gen_udg_100.py
    gen_udg50_fresnel.py               # FRESNEL-specific UDG generator
    generate_oulipo_udg.py
```
