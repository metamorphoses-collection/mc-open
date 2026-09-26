# Le otto dimore
*Ottave tavole per Q₃, il cubo degli elementi, in configurazione bi-strato*

**Grafo**: Q₃, il 3-cubo. Otto vertici etichettati da stringhe binarie
di tre bit, dodici spigoli (pari a distanza di Hamming 1). Bipartito,
regolare di grado 3, insieme indipendente massimo α = 4 (una delle
due classi di parità). **Non realizzabile come grafo di dischi
unitari nel piano** (se si prova a porre `000` con tre vicini a 120°
in 2D, il vertice `011` cade troppo vicino a `000`); **realizzabile
esattamente come grafo di palle unitarie in un registro bi-strato**
con due quadrati paralleli di lato s = 7.0 µm collegati da quattro
barre verticali di altezza h = 7.0 µm, raggio di blocco R_b = 8.0 µm.
Ogni vertice corrisponde a una dimora; il primo bit `v₀` seleziona il
livello (basso/alto), il secondo `v₁` la dimora sulla terra o nel
cielo, il terzo `v₂` il regime di solitudine o di incontro.

**Omaggio**: Ficino, *De triplici vita* (Firenze, 1489) — libro in
tre libri sulla vita dell'umanista tra terra, cielo, e i loro
incroci. Le otto dimore del nostro libro sono le otto possibili
combinazioni di un Ficino portato a tre dimensioni binarie.

---

### `000` — La cella dell'eremita
*basso, terra, solitudine; memoria*

Nell'angolo più basso della casa di Giacomo c'è una cella che il
maestro aveva destinato ai suoi ritiri invernali. Un crocifisso, un
inginocchiatoio, una piccola finestra verso il giardino interno.
Tre vicini la toccano: `001` (basso, terra, incontro — il refettorio
contiguo), `010` (basso, cielo, solitudine — la cappellina del
piano) e `100` (alto, terra, solitudine — lo studiolo del tetto).
Ognuno chiama l'eremita in modo diverso: uno con il sussurro dei
confratelli a tavola, uno con la campanella del vespro, uno con il
richiamo dei libri chiusi.

### `001` — Il refettorio contiguo
*basso, terra, incontro*

Subito accanto alla cella, il refettorio dei confratelli. Una tavola
di pietra, dieci scanni di legno, una brocca d'acqua e del pane di
ieri. Tre vicini: `000` (la cella), `011` (basso, cielo, incontro —
la loggia del coro) e `101` (alto, terra, incontro — la sala di
ricevimento del piano nobile). La legge dell'incontro è dura: chi
entra qui non può tornare alla cella senza pentirsi, né salire alla
loggia senza purificarsi.

### `010` — La cappellina del piano
*basso, cielo, solitudine*

Una cappellina minuta al piano terra, dedicata alla Madonna della
Neve. Unica abitante: un'icona bizantina scurita dal tempo. Tre
vicini: `000` (la cella), `011` (la loggia del coro) e `110` (alto,
cielo, solitudine — la mansarda astronomica di Giacomo). Qui i
vapori della terra cessano e comincia l'aria.

### `011` — La loggia del coro
*basso, cielo, incontro*

Una loggia interna dove i confratelli si radunano per cantare
l'ufficio. Volta affrescata a stelle, quattro candelabri di ferro,
una piccola organa di pochi registri. Tre vicini: `001` (il
refettorio), `010` (la cappellina) e `111` (alto, cielo, incontro —
il salone delle udienze). Il canto unisce terra e cielo ma solo in
compagnia — chi prega solo qui sbaglia stanza.

### `100` — Lo studiolo del tetto
*alto, terra, solitudine*

Al piano superiore, una camera piccola che affaccia sull'orto
murato. Qui Giacomo lavorava ai suoi manoscritti nei giorni di
pioggia. Tre vicini: `000` (la cella, per una scala interna di legno
che scricchiola), `101` (la sala di ricevimento) e `110` (la
mansarda astronomica). Lo studiolo è quello di un umanista che non
ha ancora rinunciato alla terra ma non ha più bisogno degli altri.

### `101` — La sala di ricevimento del piano nobile
*alto, terra, incontro*

Sala lunga e luminosa, dipinta a grottesche, con un ritratto di
Pico della Mirandola al muro (copia da Domenico Ghirlandaio, non
attribuita con certezza). Tre vicini: `001` (il refettorio), `100`
(lo studiolo) e `111` (il salone delle udienze). Qui Giacomo
riceveva i suoi corrispondenti — fra loro, un anonimo mittente dalla
stella a otto punte che nessuno ha mai visto in volto.

### `110` — La mansarda astronomica
*alto, cielo, solitudine*

La mansarda più alta della casa. Un telescopio di Murano puntato
verso la stella polare, una tavola coperta di efemeridi, e una
carta celeste dipinta a mano dal Giacomo ventenne. Tre vicini:
`010` (la cappellina), `100` (lo studiolo) e `111` (il salone delle
udienze). Il più distante degli elementi, il più vicino alla
ragione. *«Qui — annota Giacomo — la solitudine del cielo è una
dimostrazione.»*

### `111` — Il salone delle udienze
*alto, cielo, incontro*

Il salone principale del piano nobile: soffitto a cassettoni
dorati, affreschi del Pontormo (copia bottega, anonima), una
cattedra di noce scuro per gli ospiti di riguardo. Tre vicini: `011`
(la loggia del coro), `101` (la sala di ricevimento) e `110` (la
mansarda astronomica). Il vertice opposto alla cella dell'eremita.
Chi entra qui ha attraversato tutti e tre i cambi di parità — è
salito, è uscito dalla terra, ha accettato l'incontro — e ora siede
al posto del padrone di casa. Il re d'angolo, l'ultima stanza.

---

### Nota strutturale

Il grafo è **Q₃, il 3-cubo**, realizzato come bi-strato di due
quadrati di lato 7.0 µm separati da 7.0 µm. Verifica numerica:
esatto grafo di palle unitarie (tp=12, fp=0, fn=0, min distanza =
7.0 µm, R_b = 8.0 µm). L'insieme indipendente massimo ha quattro
elementi ed è una delle due classi di parità:

- **Parità pari** (bit 0): `000`, `011`, `101`, `110` — l'eremita,
  la loggia del coro, la sala di ricevimento, la mansarda
  astronomica.
- **Parità dispari** (bit 1): `001`, `010`, `100`, `111` — il
  refettorio, la cappellina, lo studiolo, il salone delle udienze.

Ciascuna classe descrive una "vita buona" possibile: quattro dimore
mai adiacenti, quattro vite non-attaccanti. Il lettore può leggere
il libro nell'ordine dell'una o dell'altra.

**Non-UDG in 2D**: dimostrato dal fatto che ponendo `000` con tre
vicini `001, 010, 100` attorno a lui a 120° nel piano, la quarta
dimora `011` viene forzata entro il raggio di blocco di `000` — e
`011` non è vicino di `000` nel grafo. In bi-strato questa
contraddizione sparisce, perché `011` vive nell'altro livello e la
distanza verticale è abbastanza grande da evitare il blocco
spurio. **Questa è la dimostrazione geometrica più corta che la
bi-stratificazione aggiunge potere espressivo rispetto al piano
semplice.**
