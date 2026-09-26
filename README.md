# Metamorphoses of Civilization — open texts, data and code

Released texts, datasets and code from [Metamorphoses of Civilization](https://metamorphoses-collection.org), a
collection and research programme on how civilisations transform by recombination (Greek → Roman, pagan → Christian,
manuscript → print).

**TEI P5 (validated against `tei_all`):**
[Bavarius](editions/bavarius/bavarius.tei.xml) ·
[Capilupi](editions/capilupi/capilupi.tei.xml) ·
[Ross](editions/ross/ross.tei.xml)

| Folder | What | Licence |
|---|---|---|
| [`editions/`](editions/) | MC Editions: diplomatic Latin texts with English translation, apparatus, IIIF manifests and **TEI P5** — Bavarius, *Musa Catholica* (1622); Capilupi, *Centones ex Virgilio* (c. 1555); Ross, *Christiados libri XIII* (1653) — and the tools used to establish them | texts & data CC BY 4.0 · code MIT |
| [`qoulipo/`](qoulipo/) | QOuLiPo: literary text-graphs for Maximum Independent Set on neutral-atom quantum hardware — corpus, generation pipeline, analysis scripts, paper source | CC BY 4.0 · code MIT |
| [`orsini/`](orsini/) | Orsini concordance: the Roman Republican coins of Orsini's *Familiae Romanae* (1577) linked to modern references — mirror of the Zenodo release v2.0 | CC BY 4.0 |
| [`gis/paestum/`](gis/paestum/) | A georeferenced GIS of ancient Poseidonia / Paestum (EPSG:32633), an interactive web map, and the collection's GPS-placed site photographs | vectors © OpenStreetMap contributors, ODbL · photographs CC BY 4.0 · code MIT |
| [`gis/surius-vade-vade/`](gis/surius-vade-vade/) | Roads, routes and the Mautern / Favianis site for the late-Roman Norican frontier | Itiner-e CC BY 4.0 · OSM ODbL · own routes CC BY 4.0 |

Page images of the collection copies are CC0 and served by IIIF from `cdn.metamorphoses-collection.org`
(see each edition's `manifest.json`); they are not stored here.

**How the texts were established.** Every verse was read twice, independently, by machine from native-resolution
crops of the page photographs; the readings were compared letter by letter with the transcription; each divergence
was adjudicated against the image (with hidden control items to test the readers) and corrections were checked by eye
before being applied. Translations were checked by two independent full retranslations and a blind referee, with
human review of the unresolved lines. See [`editions/README.md`](editions/README.md).

**Related deposits.** Bavarius study — measurement code and data (*centotiler*): Zenodo [10.5281/zenodo.22983865](https://doi.org/10.5281/zenodo.22983865).

**Cite:** see [`CITATION.cff`](CITATION.cff).
