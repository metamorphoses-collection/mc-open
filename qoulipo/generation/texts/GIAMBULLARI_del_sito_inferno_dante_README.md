# Giambullari — *Del sito, forma, & misure, dello Inferno di Dante*

> **Filename note**: the README path still contains `_gello_` for historical reasons (legacy filename from an earlier draft where I misremembered the title). The book is **not** *Il Gello* (a different, later Giambullari text). The correct title is below, confirmed from the 1544 title-page facsimile and the published OCR preprint.

**Proper name (main text)**: *Giambullari, Del sito, forma, & misure dello Inferno di Dante (IT) N=65 k=8*

**Role in the paper**: **sparse natural-text anchor** (d=0.104), the 2D→2L→3D ladder's sparse endpoint. The **only book in the main corpus with the full provenance arc**: facsimile → LightOn fine-tune OCR → published preprint → k-NN graph → 3D Rydberg register → quantum output. Subject of the paper's pipeline workflow figure.

---

## Source text

- **Author**: Pierfrancesco Giambullari, *Accademico Fiorentino* (1495–1555)
- **Title** (from the 1544 title page): *Del sito, forma, & misure, dello Inferno di Dante*
- **Epigraph on the title-page woodcut**: *"L'acqua ch'io prendo gia mai non si corse"* — Dante, *Paradiso* II.7
- **Short title**: *Del sito dell'Inferno*, or *Del sito, forma, e misure*
- **Year**: 1544 (MDXLIIII)
- **Place**: Florence — *In Firenze*
- **Printer**: **Neri Dortelata** — a Florentine press associated with the Accademia Fiorentina circle. Sometimes considered a pseudonymous or house-imprint of the Accademia Fiorentina network itself (scholarship has attributed it variously to Anton Francesco Doni, Cosimo Bartoli, or Giambullari himself as self-publisher). **Not Aldine**: the Manutius Aldine press operated in Venice, not Florence.
- **Language**: Renaissance Florentine Italian, in the experimental dense stress-accent orthography that Neri Dortelata's press adopted for the Accademia Fiorentina imprints
- **Typographic features**: long-s ß ligatures, scribal tilde abbreviations (úno, víaggio), stress-accent marking on nearly every vowel (fórma, síto, misúra, fondáre, profóndo)
- **Dedicatee**: Cosimo I de' Medici, Duke of Florence (the dedicatory epistle is on pages 3–4)

## Subject and intellectual context

The treatise is a **systematic geometric and architectural reconstruction of Dante's *Inferno*** — the site, the shape, and the measurements of the infernal cavity, derived from evidence internal to the *Commedia*. Giambullari opens by acknowledging Antonio Manetti's earlier (unfinished and partially lost) work on the same topic and explicitly positions himself as completing what Manetti began.

Giambullari's central interpretive move (in the first chapter, on the word *alto*): Dante's *alto* in *inferno* context does NOT mean "elevated like a mountain" but "deep, hollowed downward" — a literal cavity, not an inverted cone above ground. This distinction allows the whole topographic argument to proceed: if *alto* = depth, then the *Inferno*'s measures are verifiable from the text by taking Dante's own figures at face value and computing downward through the seven circles, the Well of the Giants, and the bolge.

This is the Florentine-Academy tradition of treating Dante as a measurable object whose geometry can be reconstructed. **Galileo's famous two lectures on the dimensions of Dante's Inferno (1588)** — delivered to the Accademia Fiorentina — cite exactly this tradition and build on Manetti and Giambullari. In that sense, *Del sito dell'Inferno* is a direct intellectual precursor to the Galileo text that is also in our corpus.

## OCR provenance (published preprint)

Prior to the paper's graph analysis, we OCR'd the 155-page 1544 Neri Dortelata edition ourselves using a **LightOn fine-tuned vision-language model** on ~10 hand-verified gold pages:

- **Character error rate**: **2.48%** on 7,660 characters / 7 validation pages
- **Preprint title**: *A 2.48% CER VLM-OCR Pipeline for a Heavily Accented 1544 Florentine Treatise*
- **Author**: Christophe Jurczak
- **Published**: Zenodo v0.1.0, 2026
- **Zenodo record**: https://zenodo.org/records/19503091
- **DOI**: 10.5281/zenodo.19503091
- **License**: CC-BY 4.0
- **Cited in this paper as**: `@jurczak2026lightonocr`
- **Raw OCR text files**: `1_OCR/ocr_output/lightonocr_ft_norm/003.txt..157.txt`

**Key methodological point**: no public-domain transcription of this treatise exists in any form (critical or diplomatic) — not on Bibliotheca Italiana, not on the digital Crusca, not on Wikisource, not on Google Books as verified OCR. Our LightOn fine-tune is the first open transcription of the 1544 Dortelata *editio princeps*. See `reference_transcription_gaps_ausonius_giambullari.md`.

## How the k-NN graph was built

Via `3_MIS/classical/core/build_topic_graph.py`:

1. OCR'd chunks loaded from `1_OCR/ocr_output/lightonocr_ft_norm/`, plus hand-enriched descriptions for diagram/table pages (the book contains geometric diagrams of Dante's *Inferno* — cones, chambers, the Pit of the Giants, Malebolge — which are hand-described rather than OCR'd)
2. Excluded 2 paratextual pages (the dedicatory epistle to Cosimo on pp 3–4)
3. Chunked into paragraphs; dropped anything under 40 characters (running heads, folios)
4. **65 surviving paragraphs** out of 155 candidate pages; each embedded with `intfloat/multilingual-e5-large`
5. k-NN graph at k=8, cosine threshold 0.78 → `graph_giambullari_65.json`
6. Full-book graph (155 paragraphs, no chunk filter) also built: `topic_graph.json` with N=155 and 629 edges

## Invariants (k=8 version — main text, N=65)

- **N**: 65
- **E**: 216
- **Density**: **0.104** — **the sparsest natural text in the main corpus**
- **Node labels**: `p005_0, p006_0, ..., p152_0` (format `p{page:03d}_{paragraph_idx}`)
- **Classical MIS (ILP)**: tractable; not yet recorded in this README
- **Gradient-MDS 3D fidelity**: 0.616 (recall 0.616, precision 0.937) — `giambullari_65_coords_3d_gradient.json`

## Pipeline-inverse recovery

Using e5-large-instruct at k=3, 8, 16, 24:

| k | recall | precision | F1 |
|---|---|---|---|
| 3* (adaptive) | 0.319 | 0.201 | **0.247** |
| 8 | 0.616 | 0.151 | 0.242 |
| 16 | 0.801 | 0.099 | 0.176 |
| 24 | 0.898 | 0.074 | 0.136 |

**Best F1 = 0.247** — **the lowest natural-text recovery in the database**. Why it's low:

1. **The e5 embedder was not trained on 16th-century Florentine experimental orthography**.
2. The source has heavy Renaissance stress accents (fóße, úso, víaggio) and tilde abbreviations that the tokenizer handles poorly — the lexical signal is diluted by orthography noise.
3. The graph is sparse (d=0.104), so k-NN recovery is inherently limited.
4. **The book is a technical treatise on geometry and measurement** — not a narrative or argumentative text. Thematic recurrences are dominated by a small shared vocabulary (*sito, forma, misura, pozzo, cerchio, bolgia, profondo, cono*), producing many pairs of pages that are topically similar on the surface but not connected in the designed k-NN graph (which uses a cosine threshold that is also dominated by the same vocabulary).

**This low F1 is a measurement, not a failure.** It shows that 16th-century Italian-OCR plus modern NLP preserves enough thematic structure to find ~1/3 of the designed edges — and it motivates the paper's methodology-appendix discussion of **the embedder-choice problem for natural historical texts**.

## Quantum status (2026-04-11)

### 3D noiseless scaling sweep (`20260411_3d_scaling_giambullari`)

Sequential-prefix results on the full N=65 gradient 3D embedding, noiseless EMU_MPS, 500 shots per prefix:

| N | edges | density | classical MIS | valid% | best IS | ratio | ⟨w⟩ |
|---|---|---|---|---|---|---|---|
| 20 | 13 | 0.068 | 11 | 99.8% | 10 | **0.909** | 8.80 |
| 30 | 31 | 0.071 | 17 | 100.0% | 13 | 0.765 | 10.42 |
| 40 | 47 | 0.060 | 22 | 99.4% | 16 | 0.727 | 13.03 |
| 50 | 64 | 0.052 | 26 | 100.0% | 17 | 0.654 | 14.60 |

**At N=20, ratio = 0.909** — the "quantum output" panel in `fig_giambullari_workflow.png`.

## Why this book and this book only

1. **The only book in the main corpus we OCR'd ourselves**, with a published preprint documenting the OCR pipeline. This gives the paper a self-contained arc from facsimile to quantum output that no other book in the corpus has.
2. **Renaissance Italian**: the corpus's only Italian text in the main section; provides linguistic diversity (alongside Latin Augustine/Lactantius, and the French/English engineered texts).
3. **Self-reflexive match**: the book is *about the measurement of a literary object* (Dante's *Inferno* as a geometric cavity). Analysing it via the geometry of a neutral-atom register closes a thematic loop the paper can draw attention to.
4. **Period-matched** to the Pacioli dodecahedron showcase (Pacioli 1509, Dortelata 1544), anchoring both sides of the paper (natural + engineered) in the Italian Renaissance's tradition of geometrizing literary and natural objects.
5. **Intellectual precursor to Galileo's 1588 Inferno lectures** (also in the corpus), so the paper has a direct two-author Florentine lineage Giambullari → Galileo on the same topic.
6. **Sparse endpoint of the ladder**: at d=0.104 it is the case where the 2D cap is least binding and the 2L→3D step is largest (+0.190 on the SA ladder v3 comparison).

## Not to be confused with

- **Giambullari's *Il Gello*** (later, separate work) — a philosophical dialogue in which the shoemaker-philologist Giovanni Battista Gelli is the interlocutor. Different book, different subject, **not the one we OCR'd**.
- **Giambullari's treatises on the Florentine language** and on the *questione della lingua* — separate works, not in our corpus.
- **giambullari_155** (N=155, same book, no 40-char chunk filter) — full-book graph derived from the same OCR output; used only in the pipeline-inverse database as a supplementary comparison (F1 = 0.528 — higher than N=65 because more nodes give more thematic anchors).
- The `topic_graph.json` file in `classical/graphs/giambullari/` is the N=155 version; `graph_giambullari_65.json` is the N=65 main-text version.
