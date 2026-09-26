# *Le Procès de Nithard* — bipartite trial constraint

**Proper name (main text)**: *Le Procès de Nithard (FR) N=50 k=2*

**Role in the paper**: **the fine-tuning methodology story**. Plain e5-large-instruct gives a disastrous F1 = 0.093 on this text; the contrastively-fine-tuned `e5-large-oulipo` model lifts it to **F1 = 0.732** (at threshold ≥ 3) — an **8× improvement**. This is the paper's single clearest demonstration that specifically-engineered constraint corpora need specifically-trained embedders.

---

## Text

- **Author**: (engineered by the project)
- **Language**: French
- **Page count**: 50 (25 prosecution + 25 defense)
- **Word count**: ~17,000
- **File**: `3_MIS/oulipo/texts/proces_de_nithard.md`
- **Homage**: Bernard Maréchal, "who taught that constraint liberates"
- **Narrative frame**: a mock trial over whether the bones of Nithard the Carolingian historian — said to have been discovered at the Abbey of Saint-Riquier in 1989 — are genuine or a fabrication.

## Constraint (bipartite by design)

**Two voices, 25 pages each**:

- **THE PROSECUTOR** (25 pages, ratione critica): forensic, skeptical, analytical. A modern archaeologist who has examined the evidence and concluded that the monks of Saint-Riquier fabricated the 1989 "discovery". Every argument is grounded in carbon-14 dating, ink analysis, paleographic inconsistency.
- **THE DEFENDER** (25 pages, ratione fidei): passionate, faithful, reverent. A church historian who argues the bones are genuine, the tradition unbroken, and faith itself a form of evidence.

**The bipartite mechanism**: the k-NN graph at threshold 0.78 connects **only pages from opposite voices** (each side addresses the same piece of evidence from the opposite point of view). No prosecution page is similar enough to another prosecution page (each makes a distinct forensic argument). No defense page is similar enough to another defense page (each invokes a different relic or tradition). But every prosecution argument has a corresponding defense counterpart, so the graph connects them.

## Thread vocabulary (12 threads, 5 per page)

BONE, CHRONICLE, CONSPIRACY, FAITH, CARBON, FORGERY, INK, JUDGE, OATH, PARCHMENT, SWORD, TONGUE.

## Graph invariants

- **N**: 50 (25 + 25)
- **Designed edges at threshold ≥ 4**: 37 (very sparse)
- **Density**: **0.030** — **the sparsest main-text engineered book**
- **Average designed degree**: 1.48 (adaptive **k*=2**)
- **MIS of a bipartite graph equals the size of the larger partition** = 25 — exactly one complete voice. **The MIS is either the whole prosecution or the whole defense**.
- **Rigidity ρ**: maximum within its voice class (both voices are monolithic).

## Pipeline-inverse recovery — the repair story

This is where Procès de Nithard is unique in the corpus.

### With plain e5-large-instruct (failure)

| k | recall | precision | F1 |
|---|---|---|---|
| 2 | 0.135 | 0.065 | 0.088 |
| 8 | 0.405 | 0.052 | 0.091 |
| 16 | 0.676 | 0.046 | 0.086 |

**Best F1 ≈ 0.09**. Catastrophic failure.

**Why**: plain e5-large-instruct treats within-voice pairs as more semantically similar than between-voice pairs. Two prosecution pages share the "forensic register" and end up as top-k neighbours even though they're not connected in the designed graph. The pipeline has no way to know that the designed structure is *bipartite*.

### With the fine-tuned `e5-large-oulipo` model

| threshold | k | recall | precision | F1 |
|---|---|---|---|---|
| ≥ 4 | 2 | 0.730 | 0.375 | 0.495 |
| ≥ 4 | 8 | 0.919 | 0.149 | 0.257 |
| **≥ 3** | **8** | 0.519 | 0.825 | **0.637** |
| **≥ 3** | **14** | 0.776 | 0.692 | **0.732** |

**Best F1 = 0.732** at threshold ≥ 3, k = 14. **An 8× improvement over plain e5-large-instruct** (0.093 → 0.732). The fine-tune was trained contrastively on thread-overlap pairs across ~10 engineered texts; it learned to distinguish within-voice from between-voice similarity, which is exactly what the Procès de Nithard constraint required.

Full run results: `3_MIS/oulipo/proces_repair_results.json`.

## Quantum status (2026-04-11)

Not currently submitted to any EMU / QPU target. The very sparse designed graph (d=0.030, avg degree 1.48) makes this a **literary-structural** case, not a quantum one: the classical MIS is trivially the larger partition (25), and there is no quantum advantage to demonstrate. **The Procès's role is purely in the methodology section as the fine-tune repair anchor**, not in the quantum hardware results.

## Why this book and this book only

1. **The strongest case for fine-tuning in the paper**: plain embedder → 0.09, fine-tuned embedder → 0.73. Nothing else shows a comparable lift.
2. **Bipartite graphs are a structurally interesting engineered-text class** that no other main-text book covers. It shows the pipeline-inverse framework applies beyond dense-cluster constraints.
3. **French language** in the main corpus: balances against Kaléidoscope (EN), Hardzone Nithard's Wager (EN), and Livre irremplaçable v2 (FR).
4. **Hermeneutically interpretable**: the prosecution/defense frame is easy to explain to non-specialists, and the "MIS = one complete voice" result is a clear literary metric.
5. **Fine-tune methodology recipe**: the project's `finetune_embedder.py` was developed essentially for this text's failure case. The repair story is traceable end to end.

## Not to be confused with

- **oulipo_nithard_pascal.md** — a related earlier text using Nithard + Pascal voices but with a different (non-bipartite) thread design, F1 = 0.254
- **proces_de_nithard.validation.json** — pre-existing thread-assignment validation file, not a separate text
