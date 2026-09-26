# Il quadrato dei re
*Sedici brevi tavole per un libro scacchistico su grafo di re 4×4*

**Grafo**: king graph su scacchiera 4×4. 16 vertici `(i,j)` per i,j ∈
[0,3]. Due vertici sono adiacenti se e solo se distanti al più una
casa in entrambe le direzioni (mosse di un re degli scacchi). 42
spigoli, densità 0.35, insieme indipendente massimo = 4 (quattro re
non-attaccanti, uno per riga o configurazione equivalente). Realizzato
come **grafo di dischi unitari 2D esatto** con spaziatura s = 5.6 µm
e raggio di blocco R_b = 8.0 µm: s√2 = 7.92 < R_b (diagonali della
casa blocadate) e 2s = 11.2 > R_b (salti del re non blocadati). Questo
è il canonico grafo 2D-UDG per una dimostrazione del pitch Pasqal
FRESNEL.

**Omaggio**: Pedro Damiano, *Libro da imparare giuocare a scacchi*
(Roma, 1512) — il primo trattato di scacchi stampato in Europa,
edito pochi anni dopo il *De Divina Proportione* di Pacioli e poco
prima del *Gello* di Giambullari. L'accademico fiorentino Giacomo di
Tommaso, protagonista di *La vita nel cubo*, è anche il lettore
anonimo del Damiano in queste sedici tavole brevi.

---

### (0,0) — Il re bianco d'angolo
Sta il re bianco dove il nero non osa: angolo dell'ovest, ultima
casa del padrone della casa. Tre vicini soli gli pesano addosso —
la torre del nord (0,1), l'alfiere di nord-ovest (1,1), il pedone
di nord (1,0). Nessuno degli altri dodici lo tocca. Giacomo annota
a margine: *«il re che ha meno vicini ha più futuro.»*

### (0,1) — La torre del nord
Appoggiata al bordo ovest, la torre guarda cinque caselle: il re
d'angolo (0,0), il pedone del sud (0,2), l'alfiere di sud-ovest
(1,0), il cavallo di sud-est (1,1), l'alfiere di ovest (1,2). Ogni
mossa sua apre una ferita nel silenzio del vicino. Damiano diceva
che le torri non ragionano di eternità, ma di minuto presente.

### (0,2) — L'alfiere di sud-ovest
Dove l'ovest finisce e il sud comincia, l'alfiere siede come un
monaco. Cinque vicini: la torre (0,1), il pedone meridionale (0,3),
il cavallo del centro (1,1), l'alfiere interno (1,2), il re del
centro-ovest (1,3). Guarda il re d'angolo senza vederlo — la loro
distanza è due case, e la legge del blocco è dura.

### (0,3) — Il pedone del sud-ovest
Ultima casa della prima colonna, il pedone del sud-ovest ha tre
vicini come i re d'angolo: l'alfiere del nord (0,2), il cavallo
centrale (1,2), il re di sud-est (1,3). Non combatterà mai — il
gioco dei pedoni è di resistere. Ma il manoscritto di Damiano
ricorda che i pedoni promossi diventano regine, e la regina mangia
tutto.

### (1,0) — Il pedone del nord
Fra il re d'angolo (0,0) e il secondo re del nord (2,0), il pedone
del nord siede al centro di cinque vicini che non riesce a contare.
Gioca sempre con la paura degli uni e la speranza degli altri. Il
suo sogno è di avanzare di una casa soltanto, e di lì guardare la
battaglia come da una torre di vedetta.

### (1,1) — Il cavallo del nord-ovest
Otto vicini. È la prima casa centrale del libro e la prima con
l'intera corte del re attorno: (0,0), (0,1), (0,2), (1,0), (1,2),
(2,0), (2,1), (2,2). Otto. Damiano diceva che il cavallo è l'unico
pezzo che salta il vicino — ma nel grafo dei re, il cavallo è solo
un vicino come gli altri. La metafora del salto muore qui, e
rinasce altrove.

### (1,2) — L'alfiere di centro-ovest
Otto vicini, come il cavallo. La sua mossa diagonale serve solo a
pensare, perché nel grafo tutti i vicini — diagonali e ortogonali —
sono ugualmente vincolati. L'alfiere scopre qui di avere gli stessi
poteri di una regina minore. Il libro di Giacomo annota: *«ogni
pezzo, se ne trova il luogo, è re.»*

### (1,3) — Il re del centro-sud
Sta fra quattro vicini: (0,2), (0,3), (1,2), (2,2), (2,3). Cinque
vicini. Non è più angolo, non è ancora centro. Il re del
centro-sud è il primo che ricorda di essere stato altro.

### (2,0) — Il re del centro-nord
Simmetrico al (1,3): cinque vicini, (1,0), (1,1), (2,1), (3,0),
(3,1). Guarda verso il sud come il (1,3) guarda verso il nord, ma
i loro sguardi non si incrociano — sono troppo distanti nel grafo.
Il lettore attento noterà che due re del centro non si vedono mai.

### (2,1) — L'alfiere di centro-est
Otto vicini, come (1,1) e (1,2). È la terza casa piena del libro,
e la terza volta che il tema della "corte completa" ritorna. Ogni
casa interna ha otto vicini; ogni casa interna è un re mascherato
da alfiere.

### (2,2) — Il cavallo di sud-est
Otto vicini. Il quarto e ultimo vertice interno. Giacomo annota:
*«quattro cavalli, quattro alfieri, quattro re, quattro pedoni, non
è forse la distribuzione perfetta?»* No, risponde il grafo: la
distribuzione perfetta è quella dove solo quattro pezzi non si
toccano mai. Quella è l'insieme indipendente massimo. Quella è la
soluzione.

### (2,3) — L'alfiere di sud-est
Cinque vicini: (1,2), (1,3), (2,2), (3,2), (3,3). Specchio del
(2,0) rispetto alla diagonale del quadrato. Giacomo disegna nel
margine due linee parallele e scrive: *«la simmetria del re è la
simmetria del vuoto.»*

### (3,0) — Il pedone del sud-est
Tre vicini soli: (2,0), (2,1), (3,1). Ha la stessa impronta del
(0,3): due re d'angolo sud di due diagonali diverse. I pedoni
d'angolo sono fratelli in isolamento, e quando Damiano descrive
le finali di pedone, parla esattamente di questo momento.

### (3,1) — Il cavallo del bordo sud
Cinque vicini: (2,0), (2,1), (2,2), (3,0), (3,2). Primo cavallo
del bordo meridionale. Il suo salto non può più essere un salto —
il gioco si è ridotto a un grafo, e il grafo non conosce che
distanze.

### (3,2) — L'alfiere del bordo sud
Cinque vicini: (2,1), (2,2), (2,3), (3,1), (3,3). Simmetrico al
(3,1). Guarda la stanza (3,3) come l'ultimo respiro del libro.

### (3,3) — Il re nero d'angolo
Estremo sud-est della scacchiera. Tre vicini: (2,2), (2,3), (3,2).
Specchio esatto del re bianco d'angolo (0,0) con cui il libro ha
cominciato. Quattro re non-attaccanti esistono su questo quadrato
— (0,0), (0,3), (3,0), (3,3) è una soluzione canonica, i quattro
angoli. Il re nero d'angolo chiude il libro come il re bianco
d'angolo l'ha aperto: con tre vicini e molta distanza, e con il
quieto orgoglio di sapere che la distanza è, in fondo, l'unica
cosa che un re non può negoziare.

---

### Nota strutturale

Il grafo è il **4×4 king graph**, 16 vertici e 42 spigoli, densità
0.350, insieme indipendente massimo α = 4. Quattro le soluzioni
canoniche: i quattro re non-attaccanti nei quattro angoli (0,0),
(0,3), (3,0), (3,3); i quattro del secondo strato (1,1), (1,3),
(3,1), (3,3) — no, questa ha vicini (1,1) e (1,3), quindi non è IS
valida. La prima è la soluzione pura; le altre le lascia il lettore
al cui spirito scacchistico piaccia esplorare.

Realizzato sulla macchina neutral-atom Pasqal FRESNEL come grafo di
dischi unitari 2D esatto con spaziatura 5.6 µm. MIS ottenibile per
via classica in 42 edge-check (istantaneo) o per via quantistica
via impulso adiabatico di Rydberg (protocollo standard). Questo è
il pitch 2D del libro: sedici sonetti brevi, quattro re, un
trattato del 1512.
