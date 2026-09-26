# Nota: il tesseratto come metafora, non come grafo canonico

Il titolo *Sonetti dal Tesseratto* evoca un Q₄ — sedici vertici, trentadue spigoli — ma il **grafo canonico depositato qui non è Q₄**. È il grafo NLP k=8 ricostruito dalle similarità di embedding fra i sedici sonetti effettivamente scritti, e ha:

- N = 16
- E = 79
- d ≈ 0.658
- MIS = 4
- ρ = 1.0

(Il Q₄ ideale avrebbe E = 32 e MIS = 8 con ρ=1.0. Le proprietà di adiacenza-binaria del Q₄ funzionano come idea poetica, non come struttura del grafo computazionale.)

I sonetti seguono nondimeno una mappa binaria di quattro coordinate `v₀v₁v₂v₃` (terra/cielo, diurno/notturno, solitudine/incontro, memoria/profezia), e la lettura per "lati del tesseratto" — sonetti che differiscono in una sola coordinata — rimane una linea critica suggerita.

Per il grafo canonico effettivo, vedere `graph_k8.json` e i campi `canonical_*` in `metadata.json`.
