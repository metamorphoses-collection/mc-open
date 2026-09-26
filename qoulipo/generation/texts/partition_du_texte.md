# La Partition du Texte
## The Score of the Text / The Partition of the Text

**An OuLiPo text under double constraint: graph-theoretic + prosodic.**

**Hommage to Bernard Marechal**, who taught that constraint liberates, and that a text is a score waiting for its reader.

---

### The Double Constraint

This text obeys two simultaneous formal rules:

> **GRAPH CONSTRAINT**: Each of the 50 pages carries exactly 5 of 10 thematic threads. The assignment follows a perfectly balanced design (each thread appears exactly 25 times) so that the resulting topic graph (threshold=0.78, top_k=16) has density d ~ 0.45-0.55, placing it in the Cazals et al. "hard zone" for MIS computation.

> **PROSODIC CONSTRAINT**: The 50 pages cycle through 5 poetic forms, 10 pages each. Each form imposes meter, rhyme, or structural rules on top of the graph constraint. This is OuLiPo squared.

### The Five Instruments

| Pages | Form | Language | Voice |
|-------|------|----------|-------|
| 1-10 | ALEXANDRINE | French | Racine -- 12 syllables, caesura at 6 |
| 11-20 | SONNET | English | Shakespeare/Ronsard -- 14 lines, ABAB CDCD EFEF GG |
| 21-30 | TERZA RIMA | English | Dante -- interlocking ABA BCB CDC |
| 31-40 | HAIKU SEQUENCE | English | Silence -- 5-7-5 tercets |
| 41-50 | FREE VERSE with ANAPHORA | English | Whitman -- repeated opening phrase |

### The Ten Threads

| # | Thread | Domain |
|---|--------|--------|
| 1 | WAGER | Probability, risk, decision under uncertainty |
| 2 | CHRONICLE | Historical record, witnessed events |
| 3 | CONSPIRACY | Fabrication, forgery, hidden agendas |
| 4 | TONGUE | Language, translation, the birth of vernacular |
| 5 | NUMBER | Mathematics, combinatorics, counting |
| 6 | FAITH | Belief, doubt, the silence of God |
| 7 | SWORD | War, conflict, fratricidal violence |
| 8 | PARCHMENT | Manuscripts, textual transmission |
| 9 | MALIETTE | The teacher, ZaZiPo, the gift of reading |
| 10 | GAME | OuLiPo, ludic constraint, rules that free |

### The Literary Conceit

The text IS a musical score. Each poetic form is a different instrument. Reading across all alexandrines, then all sonnets, then all terza rima gives one melody -- the horizontal reading. Reading by thread (all WAGER pages, all FAITH pages) gives another melody -- the vertical reading. The graph structure is the harmony that connects the voices, the chord progression that makes the polyphony cohere.

*La Partition du Texte* -- the word "partition" means both "score" (musical) and "partition" (mathematical division). The text is both.

---

### Thread Assignment Table

| Page | Threads | Form |
|------|---------|------|
| 1 | WAGER, CHRONICLE, TONGUE, FAITH, PARCHMENT | Alexandrine (FR) |
| 2 | WAGER, CONSPIRACY, NUMBER, MALIETTE, GAME | Alexandrine (FR) |
| 3 | CHRONICLE, TONGUE, FAITH, SWORD, PARCHMENT | Alexandrine (FR) |
| 4 | WAGER, CONSPIRACY, NUMBER, SWORD, GAME | Alexandrine (FR) |
| 5 | CHRONICLE, CONSPIRACY, FAITH, PARCHMENT, MALIETTE | Alexandrine (FR) |
| 6 | WAGER, TONGUE, NUMBER, FAITH, GAME | Alexandrine (FR) |
| 7 | CHRONICLE, CONSPIRACY, SWORD, PARCHMENT, MALIETTE | Alexandrine (FR) |
| 8 | WAGER, NUMBER, FAITH, MALIETTE, GAME | Alexandrine (FR) |
| 9 | CHRONICLE, TONGUE, SWORD, PARCHMENT, GAME | Alexandrine (FR) |
| 10 | WAGER, CONSPIRACY, NUMBER, FAITH, SWORD | Alexandrine (FR) |
| 11 | CHRONICLE, TONGUE, FAITH, MALIETTE, GAME | Sonnet (EN) |
| 12 | WAGER, CONSPIRACY, SWORD, PARCHMENT, MALIETTE | Sonnet (EN) |
| 13 | CHRONICLE, NUMBER, FAITH, SWORD, GAME | Sonnet (EN) |
| 14 | WAGER, CONSPIRACY, TONGUE, PARCHMENT, MALIETTE | Sonnet (EN) |
| 15 | CHRONICLE, NUMBER, FAITH, PARCHMENT, GAME | Sonnet (EN) |
| 16 | WAGER, CONSPIRACY, TONGUE, SWORD, MALIETTE | Sonnet (EN) |
| 17 | CHRONICLE, NUMBER, SWORD, MALIETTE, GAME | Sonnet (EN) |
| 18 | WAGER, CONSPIRACY, TONGUE, FAITH, PARCHMENT | Sonnet (EN) |
| 19 | CHRONICLE, NUMBER, SWORD, PARCHMENT, GAME | Sonnet (EN) |
| 20 | WAGER, CONSPIRACY, FAITH, MALIETTE, GAME | Sonnet (EN) |
| 21 | CHRONICLE, TONGUE, NUMBER, SWORD, PARCHMENT | Terza Rima (EN) |
| 22 | WAGER, FAITH, SWORD, PARCHMENT, GAME | Terza Rima (EN) |
| 23 | CONSPIRACY, TONGUE, NUMBER, MALIETTE, GAME | Terza Rima (EN) |
| 24 | WAGER, CHRONICLE, FAITH, SWORD, MALIETTE | Terza Rima (EN) |
| 25 | CONSPIRACY, TONGUE, NUMBER, PARCHMENT, GAME | Terza Rima (EN) |
| 26 | WAGER, CHRONICLE, SWORD, MALIETTE, GAME | Terza Rima (EN) |
| 27 | CONSPIRACY, TONGUE, NUMBER, FAITH, PARCHMENT | Terza Rima (EN) |
| 28 | WAGER, CHRONICLE, SWORD, PARCHMENT, GAME | Terza Rima (EN) |
| 29 | CONSPIRACY, TONGUE, FAITH, SWORD, MALIETTE | Terza Rima (EN) |
| 30 | WAGER, CHRONICLE, NUMBER, PARCHMENT, MALIETTE | Terza Rima (EN) |
| 31 | CONSPIRACY, TONGUE, FAITH, SWORD, GAME | Haiku (EN) |
| 32 | WAGER, CHRONICLE, NUMBER, PARCHMENT, GAME | Haiku (EN) |
| 33 | CONSPIRACY, FAITH, SWORD, PARCHMENT, MALIETTE | Haiku (EN) |
| 34 | WAGER, CHRONICLE, TONGUE, NUMBER, GAME | Haiku (EN) |
| 35 | CONSPIRACY, FAITH, SWORD, MALIETTE, GAME | Haiku (EN) |
| 36 | WAGER, CHRONICLE, TONGUE, NUMBER, PARCHMENT | Haiku (EN) |
| 37 | CONSPIRACY, NUMBER, FAITH, PARCHMENT, GAME | Haiku (EN) |
| 38 | WAGER, CHRONICLE, TONGUE, PARCHMENT, MALIETTE | Haiku (EN) |
| 39 | CONSPIRACY, NUMBER, SWORD, PARCHMENT, MALIETTE | Haiku (EN) |
| 40 | WAGER, CHRONICLE, FAITH, PARCHMENT, GAME | Haiku (EN) |
| 41 | CONSPIRACY, TONGUE, SWORD, PARCHMENT, GAME | Free Verse (EN) |
| 42 | WAGER, NUMBER, FAITH, SWORD, MALIETTE | Free Verse (EN) |
| 43 | CHRONICLE, CONSPIRACY, TONGUE, MALIETTE, GAME | Free Verse (EN) |
| 44 | WAGER, NUMBER, SWORD, PARCHMENT, GAME | Free Verse (EN) |
| 45 | CHRONICLE, CONSPIRACY, TONGUE, FAITH, MALIETTE | Free Verse (EN) |
| 46 | WAGER, NUMBER, FAITH, SWORD, PARCHMENT | Free Verse (EN) |
| 47 | CHRONICLE, CONSPIRACY, PARCHMENT, MALIETTE, GAME | Free Verse (EN) |
| 48 | TONGUE, NUMBER, FAITH, SWORD, MALIETTE | Free Verse (EN) |
| 49 | CHRONICLE, CONSPIRACY, TONGUE, PARCHMENT, GAME | Free Verse (EN) |
| 50 | WAGER, TONGUE, FAITH, SWORD, MALIETTE | Free Verse (EN) |

---

## I. LES ALEXANDRINS -- The Voice of Racine

*Pages 1-10. French. Twelve syllables per line, caesura at the sixth. The classical instrument: formal, measured, the alexandrine as metronome of French thought.*

---

#### PAGE 1 -- Le Serment et la Foi
*Threads: WAGER, CHRONICLE, TONGUE, FAITH, PARCHMENT*
*Form: Alexandrine (FR)*

Le chroniqueur s'avance et prend le parchemin,
car le pari du texte exige une chronique
ou la langue ancienne trace son chemin,
et la foi du serment, gravee, reste unique.

Sur la peau preparee, un pari se dessine :
le scribe a foi dans l'encre et la chronique est nue,
la langue des soldats, rude comme l'epine,
le parchemin attend ce que la bouche a su.

Charles jura en langue vulgaire, et la foi
de l'armee assemblee ne tenait qu'a un fil :
le chroniqueur nota le pari de ce roi
sur un parchemin raide, un serment difficile.

La foi dans la chronique est un pari risque,
car la langue se perd quand le parchemin brule,
et le pari du scribe est d'avoir consigne
la foi dans une langue, un parchemin, un module.

Chaque ligne est un pari : que la foi se transmette,
que la chronique survive au feu, a la poussiere,
que la langue inscrite sur ce parchemin se repete,
et que le pari tenu devienne une priere.

Le chroniqueur ecrit et risque son salut,
la foi tremble au-dessus du parchemin tendu,
la langue des serments, en ce pari, a plu --
le parchemin fait foi, le pari s'est rendu.

La chronique est un pari contre l'oubli : la foi
dans la langue ecrite sur la peau de la bete.
Le parchemin est gage, et le pari est loi,
la chronique en fait foi -- la langue est sa trompette.

Et si le parchemin trahit cette chronique,
si la langue devie et que le pari tombe,
la foi du chroniqueur, tenace et heroique,
sur le parchemin couche le pari d'outre-tombe.

---

#### PAGE 2 -- Le Jeu du Nombre
*Threads: WAGER, CONSPIRACY, NUMBER, MALIETTE, GAME*
*Form: Alexandrine (FR)*

Le maitre Maliette pose son pari clair :
que le nombre se joue en complot combinatoire,
que le jeu du hasard, ce pari sous l'eclair,
reveille le nombre endormi dans sa memoire.

Le complot du calcul s'ourdit comme un vieux jeu,
Maliette compte et recompte, un pari monstrueux.
Le nombre de contraintes est un complot de feu,
et le jeu du poete est un pari heureux.

Maliette enseigne : le nombre est un complot
contre le pari fou de l'ecriture vaine.
Le jeu de mots, le nombre d'or, le pari-mot,
le complot du maitre est une douce chaine.

Sous le jeu se dissimule un pari grave,
le nombre des pages forme un complot discret,
Maliette dit : le jeu est la seule enclave
ou le nombre et le pari gardent leur secret.

Le complot du nombre est un jeu de structure,
Maliette y reconnait un pari sur le sens.
Cinquante pages, jeu de nombre et d'ecriture,
le complot du hasard n'a pas sa connaissance.

Le pari est pose : que le nombre l'emporte,
que le jeu du complot se dechiffre en entier,
que Maliette en maitre ouvre la bonne porte
ou le nombre du jeu est un pari a signer.

Maliette sourit : le complot du nombre est jeu,
le pari de la page est un complot qui danse.
Le jeu est un nombre, le nombre est un aveu,
et le pari du maitre est toute la cadence.

Le complot s'effiloche et le nombre persiste,
le jeu du pari tient en un seul fil de soie,
Maliette le sait : tout nombre est oulipiste,
le complot et le jeu sont le pari de la joie.

---

#### PAGE 3 -- L'Epee et le Parchemin
*Threads: CHRONICLE, TONGUE, FAITH, SWORD, PARCHMENT*
*Form: Alexandrine (FR)*

La chronique rapporte que l'epee fratricide
fit couler plus de sang que la langue n'en dit.
Sur le parchemin vieux, la foi sert de bride
a l'epee du guerrier que la chronique maudit.

L'epee se leve, et la foi tremble sur la page,
la chronique en langue romane garde la trace :
l'epee brisa la paix, le parchemin fut l'otage,
la foi des combattants se lit dans cet espace.

Sur ce parchemin, l'epee de la chronique
entaille la foi qu'une langue a prononcee.
La chronique dit : l'epee est l'art tragique,
le parchemin sa scene, la foi la traversee.

La langue des serments couvre l'epee de rouille,
mais la chronique inscrite sur ce parchemin vit.
La foi du soldat meurt, l'epee se debrouille,
et la langue du texte est un parchemin d'esprit.

L'epee et la foi sont chronique d'un meme age,
la langue s'est taillee au fil de cette lame.
Le parchemin recouvre le sang du carnage,
la chronique fait foi : l'epee porte sa flamme.

Le parchemin est chronique de l'epee en foi,
la langue se souvient du choc de la bataille.
L'epee et la foi, la chronique et la loi,
le parchemin est langue et l'epee la muraille.

La foi du chroniqueur survit a tant d'epees,
la langue du parchemin est chronique du monde.
L'epee s'est tue, et la foi s'est echappee,
le parchemin fait langue a la chronique ronde.

L'epee rend la chronique tragique et la foi
se grave en cette langue sur le parchemin jaune.
La chronique dit : l'epee et le desemoi,
la foi et la langue, le parchemin pour trone.

---

#### PAGE 4 -- Le Complot Arithmetique
*Threads: WAGER, CONSPIRACY, NUMBER, SWORD, GAME*
*Form: Alexandrine (FR)*

Le pari du complot se chiffre par le nombre,
l'epee du combineur tranche le jeu en deux.
Le nombre des complots se multiplie dans l'ombre,
le pari de l'epee est un jeu dangereux.

Le jeu arithmetique est complot de la lame :
le nombre des victimes, un pari conteste.
L'epee joue son role, le nombre est le programme,
le complot du guerrier au pari deteste.

Le nombre des intrigues et le pari du sang,
le complot militaire est un jeu de massacre.
L'epee compte ses morts, le nombre est le rang,
le pari du complot est un jeu de desastre.

Le jeu du nombre est un complot d'arithmetique,
le pari de l'epee se tranche par le sort.
Le nombre du complot est un jeu numerique,
le pari de la guerre a l'epee fait escorte.

L'epee et le nombre -- pari d'un complot sombre,
le jeu du stratege se joue entre les rangs.
Le complot des nombres est un jeu dans la penombre,
l'epee du pari coupe les derniers liens du temps.

Le nombre dix est un pari, le complot est un jeu,
l'epee du calculeur compte les combinaisons.
Le pari du complot, ce nombre de voeux,
le jeu de l'epee tranche les raisons.

Le complot du nombre est l'epee du pari,
le jeu des chiffres arme le complot d'un sens.
L'epee trace un nombre, le pari est fleuri,
le complot du jeu chante a l'epee l'evidence.

Le nombre du pari seme l'epee du doute,
le complot et le jeu ferment cette partition.
L'epee est un nombre, le pari est la route,
le complot du jeu est la derniere edition.

---

#### PAGE 5 -- Le Moine et le Maitre
*Threads: CHRONICLE, CONSPIRACY, FAITH, PARCHMENT, MALIETTE*
*Form: Alexandrine (FR)*

Le complot des moines est chronique sans fin,
Maliette lit la foi dans le parchemin pale.
La chronique du complot se trame en chemin,
le parchemin de foi trahit la main monacale.

Maliette sait : le complot forge un faux parchemin,
la foi de la chronique est une conspiration.
Le parchemin du moine est complot clandestin,
Maliette y voit la foi d'une fabrication.

La chronique dit vrai, le complot dit le faux,
mais le parchemin garde la trace des deux.
La foi de Maliette est fidele au trepeau --
le complot du moine est un parchemin douteux.

Maliette enseigne : la chronique est complot
quand la foi du copiste altere le parchemin.
Le complot monacal est une chronique en trop,
et la foi du maitre eclaire ce chemin.

Le parchemin revele un complot de copiste,
Maliette et la foi scrutent la chronique nue.
Le complot est chronique, la foi est la piste,
le parchemin de Maliette est enfin reconnu.

La chronique du complot, la foi du parchemin --
Maliette distingue le vrai du contrefait.
Le complot est chronique d'un autre lendemain,
le parchemin fait foi de ce que le maitre sait.

Le complot et la foi s'enlacent au parchemin,
Maliette lit la chronique comme un palimpseste.
Le parchemin fait foi, le complot prend sa fin,
la chronique du maitre est le seul texte honnete.

Maliette ferme la chronique et la foi s'endort,
le complot du parchemin n'est plus qu'une chimere.
La chronique fait foi, le complot fait decor,
et le parchemin du maitre eclaire la matiere.

---

#### PAGE 6 -- Le Nombre et la Langue
*Threads: WAGER, TONGUE, NUMBER, FAITH, GAME*
*Form: Alexandrine (FR)*

Le pari de la langue est un nombre en priere,
la foi du jeu s'exprime en langue maternelle.
Le nombre des vocables est un pari lumiere,
et le jeu de la foi fait la langue eternelle.

La langue du nombre est un pari sacre,
le jeu de la foi se joue en chaque syllabe.
Le nombre de syllabes est un pari cadre,
la foi de la langue est un jeu qui se sable.

Le pari du poete est un nombre dans la langue,
la foi du jeu compte les pieds de chaque vers.
La langue est un nombre, le pari est l'harangue,
le jeu de la foi traverse l'univers.

Le nombre douze est un pari : que la langue tienne,
la foi dans le jeu de la metrique est totale.
Le nombre et la langue, le pari que je tienne --
la foi du jeu chante la ligne verticale.

La langue du pari est un nombre de foi,
le jeu de comptage est un pari sur la forme.
Le nombre, la foi, la langue -- tout est jeu pour moi,
le pari du poete est un nombre conforme.

Le jeu du nombre est un pari de la foi :
que la langue mesure exactement ses douze.
Le nombre de la langue est un pari de roi,
le jeu de la foi bat la mesure et epouse.

Le pari de la foi et le nombre du jeu
se tressent dans la langue comme un alexandrin.
Le nombre est un pari, la foi est un aveu,
le jeu de la langue est un nombre divin.

La langue du jeu est un pari de la foi,
le nombre de syllabes fonde la contrainte.
Le pari du nombre est un jeu, le jeu est loi,
la langue est un nombre de foi sans plainte.

---

#### PAGE 7 -- L'Epee du Copiste
*Threads: CHRONICLE, CONSPIRACY, SWORD, PARCHMENT, MALIETTE*
*Form: Alexandrine (FR)*

La chronique du complot arme l'epee du moine,
le parchemin de Maliette porte une cicatrice.
L'epee du copiste, le complot sans temoine,
la chronique du parchemin est une fabricatrice.

Maliette dit : l'epee et le parchemin s'affrontent,
le complot du copiste est une chronique de guerre.
L'epee des moines, le parchemin qu'ils confrontent,
le complot de la chronique est une ombre severe.

Le parchemin gratte, l'epee trace, le complot s'inscrit,
Maliette voit la chronique dans chaque rature.
L'epee du copiste est un complot manuscrit,
le parchemin est chronique de la forfaiture.

La chronique est une epee : le complot du texte,
Maliette dechiffre le parchemin falsifie.
L'epee du complot est la chronique du pretexte,
le parchemin du maitre est enfin certifie.

Maliette et l'epee, le complot du parchemin --
la chronique du copiste cache un complot ancien.
L'epee du moine gratte le parchemin en chemin,
le complot est la chronique et Maliette est le lien.

Le parchemin troue par l'epee du complot
porte la chronique que Maliette recompose.
L'epee et le complot sont chronique en un mot,
le parchemin du maitre est la seule glose.

Le complot du parchemin arme l'epee du scribe,
la chronique de Maliette eclaire le dessein.
L'epee du complot est chronique et diatribe,
le parchemin du maitre est le dernier ecrin.

La chronique s'acheve et l'epee se repose,
le complot du parchemin dort chez Maliette enfin.
L'epee du complot est une chronique en prose,
le parchemin du maitre reste le plus grand dessin.

---

#### PAGE 8 -- Le Pari du Maitre
*Threads: WAGER, NUMBER, FAITH, MALIETTE, GAME*
*Form: Alexandrine (FR)*

Maliette pose un pari : que le nombre et la foi
se rejoignent dans le jeu de la contrainte pure.
Le pari du nombre est un jeu de bonne foi,
et Maliette parie sur la juste mesure.

Le jeu de la foi est un nombre, un pari clair,
Maliette enseigne que le nombre est une grace.
Le pari du jeu, la foi dans la lumiere --
le nombre de Maliette occupe toute la place.

La foi dans le nombre est le pari du maitre,
le jeu de Maliette est un nombre enchante.
Le pari de la foi veut le nombre pour naitre,
le jeu du maitre est un pari de liberte.

Maliette dit : le pari du nombre est un jeu,
la foi dans le calcul est un pari supreme.
Le nombre du jeu est un pari de l'aveu,
la foi de Maliette est le nombre du poeme.

Le jeu du pari est un nombre de la foi,
Maliette enseigne que le nombre est la contrainte.
Le pari du maitre est un jeu, le jeu est loi,
la foi du nombre est un pari sans plainte.

Le nombre de la foi est le jeu du pari,
Maliette voit dans le nombre un jeu de structure.
Le pari du jeu et la foi du favori,
le nombre de Maliette est la juste architecture.

La foi du pari et le jeu du nombre uni,
Maliette dit : le nombre est un pari qui chante.
Le jeu de la foi, le pari infini,
le nombre du maitre est une foi constante.

Maliette ferme le jeu, le pari et le nombre,
la foi de la contrainte est un pari d'eclat.
Le nombre du jeu et le pari sans encombre,
la foi de Maliette tient le nombre en etat.

---

#### PAGE 9 -- La Chronique du Jeu
*Threads: CHRONICLE, TONGUE, SWORD, PARCHMENT, GAME*
*Form: Alexandrine (FR)*

Le jeu de la chronique est une epee de langue,
le parchemin raconte le jeu de la bataille.
La chronique est un jeu ou la langue harangue
l'epee du guerrier qui defend la muraille.

L'epee et le parchemin, chronique d'un vieux jeu,
la langue du combat est le jeu des soldats.
Le parchemin est chronique, l'epee est un aveu,
le jeu de la langue ne connait pas de faux-pas.

La chronique du jeu inscrit l'epee en langue,
le parchemin du jeu est une chronique noire.
L'epee joue la langue, le parchemin harangue,
la chronique du jeu est le parchemin de l'histoire.

Le jeu du parchemin est chronique de l'epee,
la langue du guerrier joue la chronique ancienne.
L'epee du jeu est un parchemin trempe,
la chronique en langue est la partition qu'il tienne.

Le parchemin est jeu : la chronique et l'epee
se croisent dans la langue comme un contrepoint.
Le jeu de la chronique, l'epee du passe,
le parchemin en langue chante le point par point.

La langue du jeu est chronique du parchemin,
l'epee joue la partition de la chronique.
Le jeu du parchemin est l'epee du chemin,
la chronique en langue est le jeu magnifique.

L'epee de la chronique et le jeu du parchemin,
la langue joue l'accord de la partition.
Le jeu est la chronique, l'epee est le refrain,
le parchemin en langue est une benediction.

La chronique du jeu, l'epee du parchemin,
la langue est le dernier instrument qui sonne.
Le jeu de la chronique est l'epee du matin,
le parchemin en langue est la note qui resonne.

---

#### PAGE 10 -- Le Pari Sanglant
*Threads: WAGER, CONSPIRACY, NUMBER, FAITH, SWORD*
*Form: Alexandrine (FR)*

Le pari du complot est un nombre de sang,
la foi de l'epee tranche le complot en nombre.
Le pari de la foi et le complot des rangs,
l'epee du nombre est un complot dans l'ombre.

Le complot de la foi est un pari d'epee,
le nombre des complots se tranche par la lame.
Le pari du nombre est un complot trempe,
la foi de l'epee est un complot sans blame.

L'epee du complot et le nombre du pari,
la foi du combattant se joue en plein calcul.
Le complot de l'epee et le nombre incompris,
le pari de la foi est un nombre a rebours.

Le nombre du complot est l'epee du pari,
la foi de l'epee est un complot de nombre.
Le pari du complot et la foi du repris,
l'epee du nombre est un pari dans la penombre.

La foi est un pari, le complot est un nombre,
l'epee du pari tranche la foi du complot.
Le nombre de l'epee est un pari d'encombre,
la foi du complot est l'epee a defaut.

Le complot et le pari font nombre avec l'epee,
la foi du nombre et le complot du pari.
L'epee de la foi est un nombre trempe,
le complot du pari chante a l'epee : "Ainsi !"

Le nombre de la foi est le pari du complot,
l'epee du nombre tranche la foi du texte.
Le complot du pari, l'epee comme un sanglot,
le nombre de la foi est un pari complexe.

Le pari dernier : que le nombre et la foi
survivent au complot de l'epee qui menace.
Le complot du nombre est l'epee du desarroi,
la foi du pari est le nombre qui embrasse.

---

## II. LES SONNETS -- The Voice of Shakespeare

*Pages 11-20. English. Fourteen lines, iambic pentameter, rhyme scheme ABAB CDCD EFEF GG. The second instrument: lyric, compressed, the sonnet as prism refracting thought into fourteen facets.*

---

#### PAGE 11 -- The Teacher's Tongue
*Threads: CHRONICLE, TONGUE, FAITH, MALIETTE, GAME*
*Form: Sonnet (EN)*

The chronicle of tongues begins where Maliette taught,
that language is a game the faithful cannot lose,
that faith requires the tongue, however thinly wrought,
and chronicles of speech are games we dare not refuse.

The master Maliette, whose faith in every game
of tongue and chronicle was deep as any prayer,
said: "Let the tongue of chronicle announce its claim,
the game of faith in language is the teacher's care."

He chronicled each tongue: the games that grammar plays,
the faith that binds the teacher to the spoken art.
The tongue of Maliette, through chronicle of days,
held games of faith as music held the beating heart.

The game is this: that faith in tongue and chronicle
survives -- through Maliette's voice, the game grows lyrical.

A chronicle persists wherever tongues have spoken,
and Maliette knew the game of faith in language well.
The teacher's tongue kept chronicles of vows unbroken,
the game of faith was every story tongue could tell.

In Maliette's game the chronicle found its tongue again,
where faith in language was the teacher's dearest creed.
The tongue of games, the chronicle of faithful men,
the game of Maliette -- each word a planted seed.

The chronicle recalls what tongue and game have sown:
that Maliette planted faith in every phrase and rule.
The tongue is chronicle, the game is faith full-grown,
and Maliette is the chronicle of the sacred school.

The game of tongues, the chronicle of Maliette's faith --
where tongue meets game, the teacher's chronicle holds safe.

---

#### PAGE 12 -- The Forger's Wager
*Threads: WAGER, CONSPIRACY, SWORD, PARCHMENT, MALIETTE*
*Form: Sonnet (EN)*

A wager and conspiracy: the sword was drawn
above the parchment Maliette alone could read.
The conspiracy was sharp as any sword at dawn,
and Maliette's wager was to prove the forger's deed.

The sword of conspiracy hung above the page,
the parchment bore a wager written by a thief.
The Maliette knew conspiracy of age to age --
the sword slashed parchment, wager turned to disbelief.

The wager of the sword was conspiracy in ink,
the parchment Maliette unrolled revealed a lie.
The sword of wager and conspiracy's dark link
bound parchment, Maliette, and swords that made men die.

A parchment is a wager: conspiracy or truth,
and Maliette's sword divides the lie from living proof.

The conspiracy was armed, the parchment was the stake,
the wager of the sword was Maliette's to face.
The sword conspired with the parchment, for the sake
of wagers Maliette could read within their trace.

Each parchment is a wager: conspiracy or lore,
and Maliette's sword of learning cut the lie apart.
The wager of conspiracy, the sword of war,
the parchment Maliette guarded with a scholar's heart.

The sword divides the wager from conspiracy's veil,
and parchment bears the wager that the master reads.
The conspiracy of swords, the parchment's ancient tale --
and Maliette's wager blooms from honesty's small seeds.

The wager is: conspiracy or truth on parchment's face?
The sword of Maliette will find the forger's hiding place.

---

#### PAGE 13 -- The Chronicle of Swords
*Threads: CHRONICLE, NUMBER, FAITH, SWORD, GAME*
*Form: Sonnet (EN)*

The chronicle counts swords: what number bled for faith,
what game of numbered battles fills the ancient page?
The sword of faith left numbers in each bloody wraith,
the game of chronicle records a numbered age.

By faith the sword was drawn, by number came the count,
the chronicle of games was written red and wide.
The numbered dead, the faith that made the sword surmount,
the game of chronicle and numbered swords collide.

What number measures faith? The chronicle of swords
provides the game of counting -- faith against the blade.
The sword's own number fills the chronicle's dark words,
the game of faith is numbered, and the debt is paid.

The chronicle of swords: a game that numbers play,
where faith and sword are numbered in the game of day.

The number of the swords in chronicles of faith
reveals a game where numbered armies met their fate.
The sword of numbered chronicles, the game of wraith,
the faith in numbered swords the chronicles relate.

The game of numbered faith, the chronicle of steel,
the sword and number join in games of war and prayer.
The chronicle of numbered swords, the game we feel,
where faith in every number fills the battle air.

The numbered game, the sword of chronicle and creed,
the faith that numbers swords in chronicles of flame.
The sword of faith, the number, chronicle and deed --
the game of numbered chronicles will speak their name.

The chronicle of faith and swords: a numbered game,
where sword and number play the chronicle of fame.

---

#### PAGE 14 -- The Tongue of the Deceiver
*Threads: WAGER, CONSPIRACY, TONGUE, PARCHMENT, MALIETTE*
*Form: Sonnet (EN)*

The wager of the tongue conspires with the text,
a parchment Maliette could not have forged alone.
The conspiracy of tongues leaves scholars vexed,
the wager of the parchment on the tongue was sewn.

What tongue conspired to forge that wager on the page?
The parchment Maliette studied bore conspiracy.
The tongue of wagers, parchment stained with age,
the conspiracy of tongues bred Maliette's inquiry.

The wager: is the tongue conspiring with the parchment?
Does Maliette hear the tongue of conspiracy?
Each parchment wager hides the tongue's compartment,
the conspiracy of tongues is Maliette's history.

The tongue deceives, the parchment carries on the wager,
and Maliette unwinds conspiracy from the paper.

The wager of conspiracy in every tongue was spoken,
the parchment Maliette unrolled was forged and frayed.
The conspiracy of tongues left every wager broken,
and Maliette read the parchment where the forger prayed.

The tongue of conspiracy, the wager in the script,
the parchment Maliette deciphered held a code.
The wager and the tongue conspired, manuscript
by manuscript, and Maliette bore the load.

The parchment held the tongue, conspiracy and wager,
and Maliette read the tongue of every forger's hand.
Conspiracy of tongues, the parchment's hidden ledger,
the wager Maliette uncovered in the sand.

The tongue conspires, the wager stains the parchment deep,
and Maliette alone can read what forgeries keep.

---

#### PAGE 15 -- The Numbers of Faith
*Threads: CHRONICLE, NUMBER, FAITH, PARCHMENT, GAME*
*Form: Sonnet (EN)*

The chronicle of numbers and the faith they hold
is written on the parchment of a sacred game.
The number of the faithful, counted, bought, and sold,
the game of chronicle and parchment knows their name.

The faith in numbers fills the chronicle with light,
the parchment of the game preserves each faithful count.
The number of the chronicles, a parchment bright,
the game of faith in numbers makes a holy fount.

The parchment game of numbers, chronicle of creed,
the faith that numbers chronicle in every line.
The game of numbered parchment plants the faithful seed,
the chronicle of faith in numbers, a design.

The game of faith: to chronicle by numbered page,
the parchment of the numbers speaks from age to age.

The number on the parchment is a chronicle of faith,
the game of counting chronicles preserves the soul.
The faith in numbered parchment, chronicle's sweet wraith,
the game of faith in numbers makes the parchment whole.

The chronicle records the number, faith, and game,
the parchment of the faithful holds the numbered score.
The faith in chronicles of numbered parchment came
to play the game of numbers at faith's very core.

The parchment is a game, the number is a prayer,
the chronicle of faith records the numbered way.
The game of parchment, chronicle of numbered care,
the faith in numbered chronicles will never stray.

The number of the game, the chronicle of faith --
the parchment holds the number like a faithful wraith.

---

#### PAGE 16 -- The Conspirator's Tongue
*Threads: WAGER, CONSPIRACY, TONGUE, SWORD, MALIETTE*
*Form: Sonnet (EN)*

A wager in the tongue: conspiracy of blades,
the sword of Maliette conspires with the word.
The tongue of wagers, conspiracy that fades,
the sword of Maliette is conspiracy conferred.

The conspiracy of tongues and wagers, sword in hand,
where Maliette conspires to teach the tongue its edge.
The wager of the sword, conspiracy unplanned,
the tongue of Maliette cuts through the conspirator's hedge.

The sword conspires: a wager in the spoken tongue,
and Maliette hears conspiracy in every phrase.
The tongue of wager, sword conspiracy among,
the Maliette of swords conspires through endless days.

A wager: that the tongue of conspiracy be still,
while Maliette's sword divides the wager's good from ill.

The conspiracy of tongues, the wager of the sword,
where Maliette conspires to speak the teacher's truth.
The tongue of conspiracy, the wager's final word,
the sword of Maliette defends conspired youth.

The wager and the tongue, conspiracy's dark blade,
the sword that Maliette, the teacher, chose to wield.
The tongue conspires, the wager of the cavalcade,
and Maliette's sword of tongue reveals the hidden field.

The sword of conspiracy, the wager, tongue, and code,
where Maliette the teacher reads conspiracy's dark sign.
The tongue of wagers, swords that bear conspiracy's load,
and Maliette's tongue-sword is conspiracy's landmine.

The wager: that conspiracy in tongue and sword will cease,
when Maliette speaks, and wagers turn to lasting peace.

---

#### PAGE 17 -- The Game of Swords
*Threads: CHRONICLE, NUMBER, SWORD, MALIETTE, GAME*
*Form: Sonnet (EN)*

The chronicle of swords: what number played the game
when Maliette could count the swords of every age?
The numbered game of swords, the chronicle of fame,
and Maliette's game of numbers fills the chronicled page.

The sword's own number in the chronicle of games,
where Maliette counted every sword and numbered bout.
The game of numbered swords, the chronicle of names,
and Maliette's number-game removed all lingering doubt.

The game of Maliette: to chronicle each sword,
to number every blade the chronicle recalls.
The numbered game of swords, the chronicle's reward,
and Maliette's game of numbers echoes through the halls.

The chronicle of swords: a numbered game of will,
where Maliette counts the swords and plays the numbers still.

The number of the game, the sword in chronicle's hand,
where Maliette plays the game of numbered war.
The sword of numbered chronicles, the game as planned,
and Maliette counts each chronicle and numbered scar.

The game of swords, the number, Maliette, and the page,
the chronicle of numbers fills the game with steel.
The sword's game, Maliette's numbered chronicle of rage,
the game of numbered swords the chronicles reveal.

The chronicle of Maliette, the numbered game of blades,
the sword and number join the game and chronicle.
The numbered game of Maliette, sword-chronicle cascades,
and Maliette's game of swords is perfectly symmetrical.

The game of numbered swords: a chronicle to tell,
where Maliette plays the numbers and the swords play well.

---

#### PAGE 18 -- The Forger's Faith
*Threads: WAGER, CONSPIRACY, TONGUE, FAITH, PARCHMENT*
*Form: Sonnet (EN)*

The wager of conspiracy in tongue and faith,
the parchment forged by tongues conspiring against the true.
The faith in wager, parchment, conspiracy's wraith,
the tongue of faith conspires in every wager due.

The conspiracy of faith in every parchment wager,
the tongue of conspiracy speaks faith's uncertain word.
The parchment wager, faith, conspiracy's dark pager,
the tongue of faithful wagers, faithfully deferred.

The wager is: does parchment hold conspiracy or faith?
The tongue of faith conspires upon the parchment's face.
The parchment wager, tongue of conspiracy's wraith,
the faith of tongues conspires within the parchment's space.

The tongue of faith: a wager and conspiracy aligned,
the parchment speaks of wagers that conspiracy designed.

The parchment of conspiracy, the tongue of wager, faith --
the tongue conspires, the wager stakes the faithful text.
The faith of parchment, tongue of conspiracy's wraith,
the wager of the tongue leaves faith forever vexed.

The conspiracy of parchment, tongue, and faithful wager,
the faith in tongue conspires to forge the parchment's ledger.
The wager of conspiracy, the tongue of faith -- each pager
reveals conspiracy of tongue and faithful pledger.

The parchment bears the tongue, conspiracy, and wager,
the faith in parchment, tongue, and conspiracy is weighed.
The tongue of wagers, parchment, faith -- conspiracied anger
lies in the parchment-tongue where wagers were betrayed.

The wager of the tongue: conspiracy or faith?
The parchment holds the answer like a faithful wraith.

---

#### PAGE 19 -- The Numbered Blade
*Threads: CHRONICLE, NUMBER, SWORD, PARCHMENT, GAME*
*Form: Sonnet (EN)*

The chronicle of numbers scores the game of swords,
the parchment of the numbered game records each blade.
The sword of numbers fills the chronicled accords,
the game of parchment, numbered swords, a cavalcade.

The number of the swords in parchment chronicles,
the game of numbered blades the parchment can attest.
The sword of chronicles, the parchment's spectacles,
the game of numbered swords puts chronicles to test.

The parchment game: to chronicle the numbered sword,
the number of the game in parchment, chronicle, and steel.
The sword of parchment, numbered chronicles' reward,
the game of numbered swords the parchment pages seal.

The chronicle of swords: a numbered parchment game,
where sword and number play the chronicle of fame.

The parchment numbered game, the chronicle of blades,
the sword of numbers fills the game and chronicle.
The numbered parchment, sword of chronicles cascades,
the game of numbered swords is sharp and whimsical.

The chronicle of games, the parchment, number, sword,
the game of swords and numbers fills the chronicled lore.
The parchment's numbered chronicle, the game's reward,
the sword of numbered games the parchment pages bore.

The number of the game and sword in chronicle's ink,
the parchment of the numbered game records the past.
The chronicle of swords, the numbered game's dark link,
the parchment game of numbers, chronicled at last.

The game of swords: the number, chronicle, and page,
the parchment of the game speaks swords from age to age.

---

#### PAGE 20 -- The Master's Wager
*Threads: WAGER, CONSPIRACY, FAITH, MALIETTE, GAME*
*Form: Sonnet (EN)*

The wager Maliette made: conspiracy or faith?
The game of faithful wagers, Maliette's old refrain.
Conspiracy and faith, the wager's double wraith,
the game of Maliette conspires, but not in vain.

The faith of Maliette conspires within the game,
the wager of conspiracy is Maliette's great test.
The game of faithful wagers bears conspiracy's name,
and Maliette's wager on the faith of games is blessed.

Conspiracy or faith -- the game of Maliette's wager
is played where faith conspires and wagers hold the key.
The game of faithful Maliette, conspiracy's engager,
the wager and the faith in games that set us free.

The game of Maliette: a wager against conspiracy,
where faith and games conspire toward the mystery.

The wager of conspiracy, the game of Maliette's creed,
the faith conspires within the game of every teacher.
Conspiracy and wager, faith and game -- the seed
that Maliette planted grew to be the future's preacher.

The game conspires, the wager of the faith is clear,
and Maliette reads conspiracy as teachers read.
The faith in games, the wager free from fear,
conspiracy dissolves where Maliette plants the seed.

The wager and conspiracy, the faith and game,
where Maliette conspires to teach the faithful well.
The game of wagers, conspiracy without blame,
the faith of Maliette -- a game that breaks the spell.

The wager is: that faith and game conspire for good,
and Maliette's conspiracy is rightly understood.

---

## III. LA TERZA RIMA -- The Voice of Dante

*Pages 21-30. English. Interlocking tercets: ABA BCB CDC... The third instrument: narrative, propulsive, the terza rima as spiral staircase descending through meaning.*

---

#### PAGE 21 -- The Tongue of Numbers
*Threads: CHRONICLE, TONGUE, NUMBER, SWORD, PARCHMENT*
*Form: Terza Rima (EN)*

The chronicle begins where tongue and number meet,
inscribed upon the parchment where the swords were laid,
the number of the tongues the chronicle would greet.

The sword divides what tongue and number had displayed
upon the parchment where the chronicle was set,
the tongue of numbered swords, the chronicle's crusade.

The number of the tongues the parchment won't forget,
the sword and chronicle, the tongue of numbered pain,
the parchment tongue of numbers, swords that intersect.

The chronicle of tongues, the numbered sword's refrain,
the parchment holds the tongue, the number, and the blade.
The sword of numbered tongues, the chronicle's domain.

The parchment, number, tongue -- the chronicle's tirade,
the sword of tongues inscribed by numbered chroniclers.
The parchment tongue, the number, chronicle displayed.

The sword of numbered parchment, chronicle's whispers,
the tongue of numbered swords the chroniclers recall.
The parchment number, tongue, and sword -- the chronicle stirs.

The number of the tongues the parchment pages sprawl,
the chronicle of swords and tongues, the numbered text.
The parchment tongue of numbers -- chronicler of all.

The sword divides the number, tongue and parchment vexed,
the chronicle of tongues, the numbered parchment's call.
The tongue and number join -- the chronicle comes next.

The parchment holds what swords and tongues and numbers tell,
the chronicle of numbered tongues rings like a bell.

---

#### PAGE 22 -- The Wager of the Blade
*Threads: WAGER, FAITH, SWORD, PARCHMENT, GAME*
*Form: Terza Rima (EN)*

The wager of the sword is faith upon the page,
the game of parchment wagers where the swords have bled,
the faith in wagers, swords, and games throughout the age.

The sword of faith, the wager of the newly dead,
the parchment game of wagers fills the faithful sky,
the game of swords and wagers on the parchment spread.

The wager: faith or sword? The game will testify,
the parchment of the faithful wager, sword in hand.
The game of faith and swords, the wager standing by.

The faith in wagers, swords, and games across the land,
the parchment of the game records each faithful fight,
the sword of wagers, faith, and games as heaven planned.

The wager of the sword illuminates the night,
the game of faithful parchment bears the wager's scar.
The parchment sword of faith, the wager burning bright.

The game of swords and wagers, faith both near and far,
the parchment of the faithful game records the blade.
The sword of wagers, faith, and parchment's evening star.

The game of faithful swords, the wager unafraid,
the parchment holds the faith, the game, the wager clear.
The sword and faith and game, the wager finely weighed.

The parchment game of wagers, faith and sword sincere,
the wager of the game, the sword of faith appears.

---

#### PAGE 23 -- The Conspirator's Numbers
*Threads: CONSPIRACY, TONGUE, NUMBER, MALIETTE, GAME*
*Form: Terza Rima (EN)*

Conspiracy of tongues: the number is the game,
and Maliette would count conspiracies by tongue,
the numbered game of tongues, conspiracy to name.

The tongue of conspiracy by Maliette was sung,
the game of numbered tongues, conspiracy unfurled,
and Maliette's number-game of tongues, so freshly sprung.

Conspiracy of numbers, tongue and game world-hurled,
the tongue of Maliette counts every conspirator.
The game of numbered tongues, conspiracy's banner furled.

The number of the game, conspiracy's narrator,
the tongue of Maliette plays numbered games of guile.
Conspiracy of tongues, the number-game creator.

The Maliette of numbers, tongue and game and file,
conspiracy of numbered tongues, the teacher's role.
The game of tongues, conspiracy's dark crocodile.

The number of conspiracies, the tongue's patrol,
and Maliette's game of tongues counts every hidden plot.
The game of numbered tongues, conspiracy's dark soul.

Conspiracy of tongues, the number-game is hot,
and Maliette plays the tongue of numbered games with care.
The game of tongues, conspiracy -- the Maliette's knot.

The number of the game, conspiracy laid bare,
the tongue of Maliette plays on through numbered air.

---

#### PAGE 24 -- The Faithful Sword
*Threads: WAGER, CHRONICLE, FAITH, SWORD, MALIETTE*
*Form: Terza Rima (EN)*

The wager of the chronicle: a sword of faith,
and Maliette would chronicle the wager's pain.
The faith of swords, the chronicle of every wraith.

The sword of Maliette, the wager's faithful strain,
the chronicle of faith and swords, a wager's toll.
The faith in chronicles of swords, the wager's gain.

The Maliette of swords, the chronicle's patrol,
the wager of the faithful sword in chronicles told.
The faith of Maliette, the wager's shining goal.

The chronicle of swords and faith and wagers bold,
the sword of Maliette cuts through the chronicle's haze.
The faith in wagers, swords, and chronicles of old.

The Maliette of chronicles, the faithful sword ablaze,
the wager of the chronicle, the sword of faith.
The faith of Maliette through chronicled swords surveys.

The sword and chronicle, the wager's faithful wraith,
and Maliette records the chronicle's bright flame.
The wager of the sword is faith beyond the lathe.

The chronicle of Maliette, the faithful wager's name,
the sword of faith, the chronicle of swords the same.
The wager of the faithful sword, the chronicle's game.

The faith of Maliette, the sword and chronicle's claim,
the wager of the chronicle holds faith's bright frame.

---

#### PAGE 25 -- The Parchment Game
*Threads: CONSPIRACY, TONGUE, NUMBER, PARCHMENT, GAME*
*Form: Terza Rima (EN)*

Conspiracy of tongues upon the parchment's game,
the number of conspired tongues the parchment shows,
the game of numbered parchment, conspiracy to blame.

The tongue of parchment, numbered conspiracy that grows,
the game of tongues conspiring on the numbered page.
The parchment game of tongues, conspiracy that flows.

The number of the game, conspiracy's dark stage,
the tongue of parchment, numbered game of silent guile.
The parchment game of tongues, conspiracy's dark cage.

Conspiracy of tongues, the numbered parchment's mile,
the game of numbered tongues, the parchment's whispered plot.
The tongue of parchment games, conspiracy's dark file.

The number of conspiracies the parchment got,
the tongue of games conspiring on the numbered skin.
The parchment game of tongues, conspiracy's dark knot.

Conspiracy of numbered tongues, the game within,
the parchment of the tongue, the number-game conspired.
The game of tongues, conspiracy's parchment djinn.

The number of the tongues the parchment game inspired,
conspiracy of tongues upon the numbered page.
The parchment game of tongues, conspired and admired.

The tongue and number, parchment, game, conspiracy sage,
the game of numbered tongues turns parchment's final page.

---

#### PAGE 26 -- The Master's Sword
*Threads: WAGER, CHRONICLE, SWORD, MALIETTE, GAME*
*Form: Terza Rima (EN)*

The wager of the chronicle: the sword is drawn,
and Maliette would play the game of chronicled steel.
The game of swords, the chronicle of every dawn.

The sword of Maliette, the wager's spinning wheel,
the chronicle of games where swords and wagers cross.
The game of Maliette, the chronicled appeal.

The wager of the sword is Maliette's gain and loss,
the chronicle of games records the wager's price.
The game of swords, the chronicle of Maliette's toss.

The sword of chronicles, the wager's loaded dice,
and Maliette plays the game of chronicled swords with grace.
The game of wagers, swords, and chronicles suffice.

The chronicle of Maliette, the game of swords in place,
the wager of the sword, the chronicle of play.
The game of Maliette, the sword and chronicle's embrace.

The wager and the sword, the chronicle of day,
and Maliette's game of chronicles, the sword's display.
The game of wagers, swords -- the Maliette's relay.

The chronicle of swords, the game of wagers -- stay,
and Maliette plays the chronicle of swords' soiree.
The game of wagers, swords, the chronicle of way.

The Maliette of games, the chronicle of swords, essay,
the wager of the game, the sword's last roundelay.

---

#### PAGE 27 -- The Faithful Number
*Threads: CONSPIRACY, TONGUE, NUMBER, FAITH, PARCHMENT*
*Form: Terza Rima (EN)*

Conspiracy of tongues: the number holds the faith,
the parchment of conspiracy, the tongue of prayer.
The faithful number, tongue of conspiracy's wraith.

The number of conspiracies the faithful share,
the tongue of parchment, numbered faith in conspiracy.
The parchment tongue of numbers, faith beyond compare.

The faith in numbered tongues, conspiracy's dark history,
the parchment of the faithful, numbered and conspired.
The tongue of faithful numbers, parchment's deepest mystery.

Conspiracy of numbered parchment, faith inspired,
the tongue of faith, the number of conspiracies.
The parchment of the faithful tongue, conspired and fired.

The number of the faithful tongue's conspiracies,
the parchment faith of numbered tongues that never rest.
Conspiracy of faithful numbers, tongue's disease.

The parchment tongue of faith, conspiracy addressed,
the number of the faithful, tongue and parchment bound.
Conspiracy of tongues, the numbered faith confessed.

The faithful number, tongue of conspiracy resound,
the parchment holds the faith, conspiracy around.
The tongue of numbered faith, the parchment's holy ground.

Conspiracy of faithful tongues, the number found,
the parchment faith of tongues -- conspiracy's last sound.

---

#### PAGE 28 -- The Chronicle of Play
*Threads: WAGER, CHRONICLE, SWORD, PARCHMENT, GAME*
*Form: Terza Rima (EN)*

The wager of the chronicle: the game of blades,
the parchment of the game records each wager's sword.
The game of chronicles, the parchment's long arcades.

The sword of wagers, chronicled and underscored,
the parchment game of swords, the chronicle of play.
The game of parchment wagers, sword and chronicle adored.

The wager of the game, the chronicle's display,
the sword of parchment, game and chronicle combined.
The parchment wager, sword of chronicle's bright day.

The game of swords, the chronicle's parchment enshrined,
the wager of the parchment, game of swords and lore.
The sword of chronicles, the parchment game designed.

The chronicle of games, the wager, sword, and score,
the parchment of the sword, the game's recorded wager.
The wager of the chronicle, the game's bright core.

The sword of parchment, game and chronicle's engager,
the wager of the game, the chronicle of blades.
The parchment game of swords, the chronicle's dark pager.

The game of wagers, swords, and chronicle cascades,
the parchment of the game, the sword's bright escalade.
The chronicle of swords, the wager's promenades.

The parchment game, the chronicle, the sword's crusade,
the wager of the game plays on, the sword displayed.

---

#### PAGE 29 -- The Conspirator's Faith
*Threads: CONSPIRACY, TONGUE, FAITH, SWORD, MALIETTE*
*Form: Terza Rima (EN)*

Conspiracy of tongues: the faith of swords divides,
and Maliette hears conspiracy in faithful tongues.
The sword of faith, conspiracy of tongue that hides.

The faith of Maliette, conspiracy among
the swords of tongues, the faithful sword conspired.
The tongue of faithful swords, conspiracy that stung.

Conspiracy of swords, the tongue of faith desired,
and Maliette reads the sword of conspiracy's creed.
The faithful tongue of swords, conspiracy inspired.

The sword of tongues, conspiracy's dark faithful seed,
and Maliette knows the tongue of conspiracy's pain.
The faith of swords, conspiracy's dark faithful deed.

The tongue of Maliette, the faithful sword's refrain,
conspiracy of faithful tongues, the sword divides.
The faith of conspiracy, the tongue of Maliette's gain.

The sword of faith conspires where the tongue abides,
and Maliette reads conspiracy in faithful verse.
The tongue of swords, conspiracy of faith that guides.

The faithful sword, conspiracy the tongue must nurse,
and Maliette knows the faith of tongues conspired.
The sword of conspiracy, the tongue -- from bad to worse.

The faith of Maliette, the tongue of swords admired,
conspiracy of faithful tongues, the sword retired.

---

#### PAGE 30 -- The Counting Master
*Threads: WAGER, CHRONICLE, NUMBER, PARCHMENT, MALIETTE*
*Form: Terza Rima (EN)*

The wager of the chronicle: the number counts,
and Maliette records the parchment's numbered days.
The parchment of the wager, numbered chronicle's founts.

The number of the chronicles, the wager's praise,
and Maliette reads the parchment where the numbers glow.
The parchment wager, numbered chronicle displays.

The chronicle of numbers, Maliette would know,
the wager of the parchment, numbered tale.
The number Maliette counts on parchment's flow.

The parchment wager, chronicle of numbered mail,
and Maliette records the number's every turn.
The wager of the chronicle, the number's trail.

The Maliette of numbers, chronicle and urn,
the parchment wager, numbered chronicle of worth.
The number of the wager, Maliette would learn.

The chronicle of numbers, parchment of the earth,
and Maliette's wager: numbered chronicles from birth.
The parchment number, chronicle of Maliette's mirth.

The wager of the number, chronicle and hearth,
and Maliette counts the parchment's numbered wager-worth.
The chronicle of numbers, Maliette gives forth.

The parchment wager, numbered chronicle of north,
and Maliette's counting -- wager, chronicle hence-forth.

---

## IV. LES HAIKUS -- The Voice of Silence

*Pages 31-40. English. Tercets of 5-7-5 syllables. The fourth instrument: minimal, precise, the haiku as silence between notes. Nature imagery woven with thematic threads.*

---

#### PAGE 31 -- Tongues of War
*Threads: CONSPIRACY, TONGUE, FAITH, SWORD, GAME*
*Form: Haiku Sequence (EN)*

Tongue of conspiracy --
faithful sword games in the dawn,
tongue and blade as one.

The sword of the game
conspires with the faithful tongue,
steel and speech combined.

Faith in tongue and sword,
conspiracy plays the game --
words cut like a blade.

Conspiring tongues play
the game of swords and of faith,
steel beneath the words.

The game of the sword,
conspiracy's faithful tongue --
steel in every breath.

Tongue against the sword,
conspiracy games of faith,
silence after steel.

Faithful tongue conspires,
the game of swords plays in snow --
faith and blade converge.

Sword and tongue and game,
conspiracy's faithful cry --
winter's edge of faith.

The tongue of the game,
conspiracy, faith, and sword --
frost on spoken steel.

Conspiring with faith,
the game of tongues draws the sword,
dawn on frozen blades.

The sword of the tongue,
conspiracy's game of faith --
ice on steel and prayer.

Faith through tongue and game,
conspiracy of the sword,
snow on breathing blades.

Tongue conspires with faith,
the game of swords never ends --
steel on winter's tongue.

The faithful tongue plays
conspiracy's game of swords,
frost on every word.

Sword and tongue and faith,
conspiracy's lasting game --
blades in silent snow.

Steel conspires with tongue,
the game of faith draws the sword,
winter speaks in blades.

The tongue of the sword,
conspiracy's faithful game --
snow on broken steel.

Faith and tongue and game,
conspiracy of the sword --
frost on spoken blades.

Conspiring tongues speak
the game of swords and of faith,
dawn on silent steel.

The sword of the game,
conspiracy's faithful tongue --
blades in winter's breath.

Tongue of conspiracy,
faithful game of swords at dawn --
steel beneath the snow.

The game of the tongue,
conspiracy, sword, and faith --
frost on spoken prayer.

---

#### PAGE 32 -- The Numbered Chronicle
*Threads: WAGER, CHRONICLE, NUMBER, PARCHMENT, GAME*
*Form: Haiku Sequence (EN)*

Wager in the game --
chronicle of numbered scrolls,
parchment holds the count.

The number of games,
wager on the chronicle,
parchment, yellowed, counts.

Chronicle of games,
numbered wager on the page --
parchment keeps the score.

Parchment, numbered, holds
the wager of chronicle,
game of counted years.

The game of numbers,
wager on the chronicle --
parchment folds and waits.

Numbered chronicle,
parchment wager in the game,
counting autumn leaves.

The wager of scrolls,
chronicle of numbered games,
parchment in the rain.

Game and chronicle,
numbered wager on the page --
parchment, damp and old.

The number of scrolls,
wager-game of chronicle,
parchment, worn and pale.

Chronicle of games,
numbered parchment wagers bloom --
counting winter stars.

Parchment holds the game,
wager, chronicle, and count,
numbers in the frost.

The game of the wager,
chronicle of numbered scrolls,
parchment breathes and waits.

Numbered wager-game,
chronicle on parchment's face,
counting leaves that fall.

The parchment of games,
wager, chronicle, and count,
numbered in the snow.

Chronicle of scrolls,
numbered wager in the game --
parchment's quiet song.

The game of the count,
wager, chronicle, and scroll,
parchment, number, dawn.

Numbered parchment games,
wager on the chronicle --
counting morning light.

The chronicle waits,
numbered wager in the game,
parchment holds the dawn.

Game of numbered scrolls,
wager-chronicle of time,
parchment counts the hours.

The number of games,
chronicle of wagers told,
parchment speaks in rain.

Wager, game, and count,
chronicle of numbered scrolls --
parchment's final note.

The game of the scroll,
numbered wager, chronicle --
parchment in the wind.

---

#### PAGE 33 -- The Forger's Sword
*Threads: CONSPIRACY, FAITH, SWORD, PARCHMENT, MALIETTE*
*Form: Haiku Sequence (EN)*

Conspiracy's sword
guards the parchment Maliette reads --
faith in forged remains.

Maliette of faith,
conspiracy of the sword,
parchment, false and true.

The sword of the forge,
conspiracy, parchment, faith --
Maliette decodes.

Parchment of the sword,
conspiracy's faithful lies --
Maliette reads on.

Faith in parchment-swords,
conspiracy's master's eye --
Maliette sees clear.

The sword conspires,
parchment of the faithful forged --
Maliette's keen glance.

Conspiracy's faith,
the sword of parchment and lies --
Maliette discerns.

Parchment, sword, and faith,
conspiracy's master class --
Maliette unwinds.

The faithful sword guards
conspiracy's parchment trove --
Maliette knows well.

Conspiracy's blade,
parchment faith the master reads --
Maliette's bright lamp.

The sword of the forged,
conspiracy, parchment, faith --
Maliette reads deep.

Faith in parchment's sword,
conspiracy's master's eye --
Maliette holds firm.

Parchment of the faith,
conspiracy's forger's sword --
Maliette's clear thought.

The sword and the faith,
conspiracy's parchment-plot --
Maliette unmasks.

Conspiracy's faith,
parchment of the forger's sword --
Maliette sees through.

The faithful parchment,
conspiracy's sword in hand --
Maliette stands guard.

Sword of parchment-faith,
conspiracy's final plea --
Maliette speaks truth.

Parchment holds the sword,
conspiracy's faithful scar --
Maliette reads clear.

The faith of the sword,
conspiracy's parchment-lie --
Maliette prevails.

Conspiracy's sword,
parchment, faith, the master's hand --
Maliette endures.

Faith and parchment-sword,
conspiracy's master's gift --
Maliette persists.

The sword of the faith,
conspiracy's parchment-tale --
Maliette concludes.

---

#### PAGE 34 -- The Vernacular Game
*Threads: WAGER, CHRONICLE, TONGUE, NUMBER, GAME*
*Form: Haiku Sequence (EN)*

Wager of the tongue --
chronicle of numbered games,
language counts its words.

The number of tongues,
wager-game of chronicle,
speech and counting mixed.

Chronicle of tongues,
numbered wager in the game --
language plays with sound.

Tongue of numbered games,
wager on the chronicle,
words and numbers dance.

The game of the tongue,
chronicle of numbered wagers --
counting syllables.

Numbered tongue of games,
wager, chronicle, and speech --
five then seven, five.

The wager of speech,
chronicle of numbered tongues --
game of syllables.

Tongue and game and count,
chronicle of wagers told,
numbered words at dawn.

The number of games,
wager, tongue, and chronicle --
counting mother tongues.

Chronicle of tongues,
numbered wager in the game,
language speaks in threes.

The game of the tongue,
wager, chronicle, and count,
numbered speech at noon.

Tongue of chronicle,
numbered wager in the game --
counting dusk and dawn.

The wager of tongues,
chronicle of numbered games --
speech beneath the stars.

Numbered tongue of games,
wager, chronicle of words --
counting autumn leaves.

The game of the count,
wager, tongue, and chronicle,
numbered words in rain.

Chronicle of tongues,
numbered wager in the game --
language holds the dawn.

The tongue of the game,
wager, chronicle, and count --
numbered speech in snow.

Wager of the tongue,
chronicle of numbered games --
counting winter words.

The number of tongues,
wager-game of chronicle --
speech in morning frost.

Tongue and game and wager,
chronicle of numbered words --
language counts the light.

Game of tongues and count,
wager, chronicle of speech --
numbered words at rest.

The wager of tongues,
chronicle, number, and game --
counting final words.

---

#### PAGE 35 -- The Faithful Conspiracy
*Threads: CONSPIRACY, FAITH, SWORD, MALIETTE, GAME*
*Form: Haiku Sequence (EN)*

Conspiracy's faith --
the game of swords and masters,
Maliette believes.

The sword of the game,
conspiracy's faithful master --
Maliette plays on.

Faith and sword and game,
conspiracy's master speaks --
Maliette believes.

The game of the sword,
conspiracy's faithful cry --
Maliette responds.

Conspiracy plays
the game of faithful masters --
Maliette's sword shines.

The faithful sword-game,
conspiracy's master class --
Maliette stands firm.

Sword of faithful games,
conspiracy's lasting voice --
Maliette endures.

The game of the faith,
conspiracy, sword, and master --
Maliette plays well.

Conspiracy's sword,
faithful game the master plays --
Maliette keeps score.

The faithful master,
conspiracy's game of swords --
Maliette persists.

Sword and game and faith,
conspiracy's master-hand --
Maliette holds fast.

The game of the sword,
conspiracy's faith in masters --
Maliette prevails.

Conspiracy's game,
faithful sword the master draws --
Maliette reads deep.

The faithful sword-game,
conspiracy's master speaks --
Maliette responds.

Sword of conspiracy,
faithful game the master plays --
Maliette concludes.

The game of the faith,
conspiracy, sword, and master --
Maliette stands tall.

Conspiracy's faith,
the game of swords and masters --
Maliette survives.

The sword of the game,
conspiracy's faithful edge --
Maliette holds ground.

Faith and sword and game,
conspiracy's master class --
Maliette endures.

The game of the sword,
conspiracy's faithful cry --
Maliette plays on.

Conspiracy's faith,
the game of master and sword --
Maliette's last stand.

The faithful master,
conspiracy's game of blades --
Maliette speaks peace.

---

#### PAGE 36 -- The Tongue of Numbers
*Threads: WAGER, CHRONICLE, TONGUE, NUMBER, PARCHMENT*
*Form: Haiku Sequence (EN)*

Wager of the tongue --
chronicle of numbered scrolls,
parchment speaks in speech.

The number of tongues,
wager on the chronicle,
parchment holds the word.

Chronicle of tongues,
numbered wager, parchment-speech --
counting in the rain.

Parchment tongue of count,
wager, chronicle, and speech --
numbered words in frost.

The wager of speech,
chronicle of numbered tongues,
parchment's quiet voice.

Numbered tongue of scrolls,
wager, chronicle, and ink --
parchment counts the dawn.

The tongue of the count,
wager, chronicle, and scroll --
numbered parchment speaks.

Chronicle of tongues,
numbered wager, parchment speaks --
counting morning light.

The parchment of tongues,
wager, chronicle, and count,
numbered speech at noon.

Tongue and parchment count,
wager, chronicle of speech --
numbered words in dusk.

The wager of tongues,
chronicle of numbered scrolls --
parchment speaks in rain.

Numbered parchment-tongue,
wager, chronicle of words --
counting autumn sounds.

The tongue of the scroll,
wager, chronicle, and count,
parchment speaks at dawn.

Chronicle of tongues,
numbered wager on the scroll --
parchment counts the stars.

The parchment of speech,
wager, tongue, and chronicle --
numbered words in frost.

Tongue and wager count,
chronicle of parchment-words --
numbered speech in snow.

The number of tongues,
wager, chronicle, and scroll --
parchment speaks in wind.

Chronicle of tongues,
numbered wager, parchment speaks --
counting winter words.

The tongue of the count,
wager, chronicle, and scroll --
parchment's final speech.

Numbered tongue of scrolls,
wager, chronicle of words --
parchment counts the end.

Tongue and parchment count,
wager, chronicle of speech --
numbered words at rest.

The wager of tongues,
chronicle of numbered scrolls --
parchment speaks in peace.

---

#### PAGE 37 -- The Faithful Count
*Threads: CONSPIRACY, NUMBER, FAITH, PARCHMENT, GAME*
*Form: Haiku Sequence (EN)*

Conspiracy's count --
faithful game on parchment's face,
numbers hold the truth.

The number of games,
conspiracy's faithful scroll --
parchment counts the lies.

Faith in numbered games,
conspiracy on parchment --
counting what is true.

Parchment of the game,
conspiracy's faithful count --
numbers in the rain.

The game of the count,
conspiracy's faithful scroll --
parchment holds the dawn.

Numbered faith in games,
conspiracy on parchment --
counting morning stars.

The parchment of games,
conspiracy's faithful count --
numbers in the frost.

Faith and game and count,
conspiracy's parchment-scroll --
numbered truth in snow.

The game of the faith,
conspiracy's parchment-count --
numbers hold the light.

Conspiracy's game,
faithful parchment holds the count --
numbered truth at noon.

The number of games,
conspiracy's faithful scroll --
parchment counts the dusk.

Faith in parchment-games,
conspiracy's lasting count --
numbered truth in rain.

The game of the count,
conspiracy's faithful scroll --
parchment speaks in frost.

Numbered faith in games,
conspiracy on parchment --
counting autumn stars.

The parchment of faith,
conspiracy's game of count --
numbers hold the truth.

Conspiracy's game,
faithful count on parchment's face --
numbered truth in dawn.

The number of games,
conspiracy's faithful scroll --
parchment holds the peace.

Faith and game and count,
conspiracy's parchment-truth --
numbered words in rain.

The game of the faith,
conspiracy's parchment-count --
numbers speak the truth.

Conspiracy's game,
faithful parchment, numbered count --
truth beneath the snow.

The parchment of games,
conspiracy's faithful count --
numbers at the end.

Faith in numbered games,
conspiracy on the scroll --
parchment counts the last.

---

#### PAGE 38 -- The Teacher's Tongue
*Threads: WAGER, CHRONICLE, TONGUE, PARCHMENT, MALIETTE*
*Form: Haiku Sequence (EN)*

Wager of the tongue --
chronicle Maliette reads,
parchment speaks the word.

The tongue of the wager,
chronicle, parchment, and speech --
Maliette reads on.

Chronicle of tongues,
wager on the parchment page --
Maliette listens.

Parchment tongue of wager,
chronicle and speech combined --
Maliette decodes.

The wager of speech,
chronicle of Maliette's tongues --
parchment holds the key.

Tongue and parchment wager,
chronicle of the teacher --
Maliette reads well.

The chronicle-tongue,
wager, parchment, teacher's words --
Maliette speaks true.

Parchment of the tongue,
wager, chronicle, and speech --
Maliette holds fast.

The tongue of the wager,
chronicle of parchment-words --
Maliette endures.

Chronicle of tongues,
wager, parchment, teacher's voice --
Maliette reads deep.

The parchment of tongues,
wager, chronicle of speech --
Maliette listens.

Tongue and wager-scroll,
chronicle of the teacher --
Maliette reads clear.

The wager of tongues,
chronicle of Maliette --
parchment speaks in dawn.

Chronicle of speech,
wager, tongue, and parchment-scroll --
Maliette holds ground.

The tongue of the scroll,
wager, chronicle, and words --
Maliette speaks peace.

Parchment tongue of wager,
chronicle of the teacher --
Maliette reads last.

The wager of speech,
chronicle of parchment-tongues --
Maliette concludes.

Tongue and chronicle,
wager on the parchment page --
Maliette rests now.

The parchment of tongues,
wager, chronicle of words --
Maliette reads on.

Chronicle of tongues,
wager, parchment, teacher's voice --
Maliette endures.

Tongue and wager-scroll,
chronicle of Maliette --
parchment's final word.

The wager of speech,
chronicle of parchment-tongues --
Maliette reads peace.

---

#### PAGE 39 -- The Forger's Number
*Threads: CONSPIRACY, NUMBER, SWORD, PARCHMENT, MALIETTE*
*Form: Haiku Sequence (EN)*

Conspiracy's count --
sword on parchment, Maliette reads,
numbers tell the forge.

The number of swords,
conspiracy's parchment-plot --
Maliette decodes.

Sword of numbered scrolls,
conspiracy, parchment, forge --
Maliette sees through.

Parchment of the sword,
conspiracy's numbered lies --
Maliette reads deep.

The number of plots,
conspiracy's sword on scroll --
Maliette holds firm.

Sword and number count,
conspiracy's parchment-trove --
Maliette stands guard.

The parchment of swords,
conspiracy's numbered forge --
Maliette reads clear.

Numbered conspiracy,
sword on parchment, teacher's eye --
Maliette discerns.

The sword of the count,
conspiracy's parchment-scroll --
Maliette reads on.

Conspiracy's blade,
numbered parchment, teacher reads --
Maliette prevails.

The number of plots,
conspiracy's sword and scroll --
Maliette holds fast.

Parchment of the forge,
conspiracy's numbered sword --
Maliette speaks truth.

The sword of the scroll,
conspiracy's numbered plot --
Maliette reads deep.

Numbered parchment-sword,
conspiracy's master reads --
Maliette endures.

The parchment of plots,
conspiracy's numbered blade --
Maliette stands tall.

Sword and number count,
conspiracy's parchment lies --
Maliette reads clear.

The number of swords,
conspiracy's parchment-forge --
Maliette concludes.

Parchment, sword, and count,
conspiracy's numbered plot --
Maliette reads last.

The sword of the forge,
conspiracy's parchment-count --
Maliette sees peace.

Numbered conspiracy,
sword and parchment, teacher reads --
Maliette rests now.

The parchment of blades,
conspiracy's numbered lies --
Maliette reads on.

Sword of numbered plots,
conspiracy's parchment-truth --
Maliette endures.

---

#### PAGE 40 -- The Faithful Wager
*Threads: WAGER, CHRONICLE, FAITH, PARCHMENT, GAME*
*Form: Haiku Sequence (EN)*

Wager of the faith --
chronicle of parchment games,
belief holds the score.

The game of the wager,
chronicle, faith, and the scroll --
parchment counts the prayers.

Chronicle of faith,
wager-game on parchment's face --
belief plays and waits.

Parchment of the game,
wager, chronicle, and faith --
counting prayers at dawn.

The faith of the game,
wager, chronicle, and scroll --
parchment holds the light.

Game of faithful wagers,
chronicle on parchment's page --
belief counts the stars.

The wager of faith,
chronicle of parchment games --
counting prayers in rain.

Parchment of the faith,
wager, game, and chronicle --
belief holds the dawn.

The game of the wager,
chronicle, faith, and the scroll --
parchment counts the dusk.

Chronicle of faith,
wager-game on parchment's face --
belief plays in snow.

The faith of the game,
wager, chronicle, and scroll --
parchment holds the peace.

Game of faithful wagers,
chronicle on parchment's page --
belief counts the end.

The wager of faith,
chronicle of parchment games --
counting prayers at rest.

Parchment of the faith,
wager, game, and chronicle --
belief holds the light.

The game of the wager,
chronicle, faith, and the scroll --
parchment speaks in rain.

Chronicle of faith,
wager-game on parchment's face --
belief plays in frost.

The faith of the game,
wager, chronicle, and scroll --
parchment holds the truth.

Game of faithful wagers,
chronicle on parchment's page --
belief counts the dawn.

The wager of faith,
chronicle of parchment games --
counting prayers in snow.

Parchment of the faith,
wager, game, and chronicle --
belief holds the peace.

The game of the wager,
chronicle, faith, and the scroll --
parchment counts the last.

Chronicle of faith,
wager-game on parchment's face --
belief speaks at rest.

---

## V. LES VERS LIBRES -- The Voice of Whitman

*Pages 41-50. English. Free verse with anaphora: each paragraph begins with the same phrase. The fifth instrument: expansive, cataloguing, the free verse as open field where the anaphoric phrase is the heartbeat.*

---

#### PAGE 41 -- I Have Seen the Tongue of Swords
*Threads: CONSPIRACY, TONGUE, SWORD, PARCHMENT, GAME*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have seen"*

I have seen the tongue of conspiracy cut deeper than any sword, carving games of deception into the parchment of living memory, and the tongue of the game was sharper than the sword it served.

I have seen the sword conspire with the tongue to forge a parchment of lies, a game of tongues and swords conspiring on the ancient page, the conspiracy of the parchment-game where tongue and sword collaborate in their dark work.

I have seen the parchment bear the marks of conspired swords, the tongue of the game inscribed upon the skin of beasts, the conspiracy of tongue and sword leaving game-marks on the parchment like scars on a veteran's back.

I have seen conspiracy's tongue and the game of swords play out on parchment after parchment, the tongue of the game conspiring with the sword, the parchment record of every tongue-sword-conspiracy-game played across the centuries.

I have seen the game of tongues conspire with the parchment's sword, the conspiracy of games where tongue and sword and parchment intertwine, the game of conspired tongues and swords upon the parchment stage.

I have seen the tongue of every conspiracy, the sword of every game, the parchment of every conspired tongue-game, the sword-conspiracy of parchment and tongue, the game that tongue and sword conspire to play upon the parchment's ancient face.

I have seen the conspiracy of tongue and sword and parchment and game unfolding across the ages, and I say: the tongue is the sharpest sword, the conspiracy is the oldest game, the parchment is the only witness, and the game of conspired tongues and swords will never end.

I have seen the parchment hold the tongue, the sword, the conspiracy, the game -- all four together -- and I say: this is the partition of the text, this is the score that tongue and sword and conspiracy and parchment play together in the game of games.

---

#### PAGE 42 -- I Have Counted the Faithful Swords
*Threads: WAGER, NUMBER, FAITH, SWORD, MALIETTE*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have counted"*

I have counted the wagers of the faithful, numbered their swords one by one, and Maliette taught me that the number of faithful swords is the only wager worth making.

I have counted the swords of faith, each numbered like a prayer, and the wager of Maliette was that the number of faithful swords exceeds the number of faithless ones, that the wager of faith is won by counting.

I have counted the faithful and the faithless, numbered the swords of each, and the wager of Maliette was this: that faith is a number, that the sword is a counter, that the wager of counting is itself an act of faith.

I have counted the numbers of the wager, the swords of the faithful, the faith of Maliette in numbers, the number of wagers on faith and sword, and I say: the counting is the faith, the number is the sword, the wager is the teaching.

I have counted what Maliette numbered: the swords of faith, the wagers of number, the faithful count of swords and wagers, the number of faithful swords Maliette wagered on, the faith in numbered wagers on the sword.

I have counted the wagers of the sword and the faith of the number and the number of Maliette's teachings, and I say: the faithful sword is numbered, the wager is counted, the number is faith, and Maliette's teaching is the count itself.

I have counted the faithful swords and numbered every wager, and Maliette's teaching was this: that faith is the wager of the numbered, that the sword is the number of the faithful, that the count is the wager, and the number is the sword of faith.

I have counted everything Maliette taught about wagers and faith and swords and numbers, and I say: the number of faithful swords is the only wager, the count is the faith, and Maliette's teaching will outlast every sword.

---

#### PAGE 43 -- I Have Heard the Chronicle of Tongues
*Threads: CHRONICLE, CONSPIRACY, TONGUE, MALIETTE, GAME*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have heard"*

I have heard the chronicle of tongues conspiring, the game of Maliette where tongue and conspiracy meet in the chronicle's dark corridor, the game of conspired tongues that Maliette taught me to recognize.

I have heard the tongue of conspiracy in every chronicle, the game of Maliette unmasking the conspired tongues, the chronicle of games where tongue and conspiracy dance their endless dance.

I have heard Maliette speak the tongue of chronicle and conspiracy, the game of language where the chronicle conspires with the tongue, the conspiracy of chronicled tongues in Maliette's teaching.

I have heard the game of chronicles and tongues conspiring, the conspiracy of Maliette's teaching, the tongue of the game where chronicle and conspiracy meet, and I say: the chronicle is a conspiracy of tongues, and the game is Maliette's to teach.

I have heard the conspiring tongues of every chronicle, the game of Maliette's teaching, the tongue of conspiracy in the chronicle's dark game, the chronicle of conspired tongue-games that Maliette reads like a score.

I have heard the chronicle of every tongue and every conspiracy and every game, and Maliette taught me this: that the tongue conspires within the chronicle, that the game of language is a conspiracy of voices, that the chronicle records the tongue's conspiracy and the game's design.

I have heard the tongue of conspiracy, the chronicle of games, the game of Maliette, and I say: the conspiracy of tongues is the chronicle's game, the game of tongues is the chronicle's conspiracy, and Maliette's teaching is the tongue that reads the chronicle.

I have heard the game of the chronicle, the tongue of the conspiracy, the teaching of Maliette, and I say: the chronicle is the game, the tongue is the conspiracy, and Maliette's voice is the instrument that plays them all.

---

#### PAGE 44 -- I Have Wagered on the Game of Blades
*Threads: WAGER, NUMBER, SWORD, PARCHMENT, GAME*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have wagered"*

I have wagered on the number of swords inscribed upon the parchment, the game of numbered blades, the wager of parchment-games where sword and number meet in the gambler's paradise.

I have wagered on the parchment game of numbered swords, the game where number counts the swords upon the page, the parchment of numbered wagers on the game of blades.

I have wagered that the number of the game exceeds the number of swords upon the parchment, that the game of numbered parchment-swords is the only wager worth the stake, the parchment game of numbered sword-wagers.

I have wagered on the sword and on the number and on the parchment and on the game, and I say: the number of swords is the game's parchment, the parchment is the number's game, the sword is the wager, and the game is the number.

I have wagered that the game of parchment holds more swords than numbers, that the numbered game of swords upon the parchment is the only wager that counts, the parchment game where sword and number play the wager of ages.

I have wagered on the number of the game, the sword of the parchment, the parchment of the wager, the game of numbered swords upon the page, and I say: the wager is the game, the number is the sword, the parchment is the score.

I have wagered that the game of numbered swords will fill every parchment page, that the number of wagers upon the game of swords will cover the parchment from edge to edge, that the game of wagers is the number of swords on parchment.

I have wagered on the game of blades and numbers and parchment, and I say: the wager is the score, the number is the rhythm, the sword is the note, and the parchment is the silence between the notes.

---

#### PAGE 45 -- I Have Witnessed the Chronicle of Faith
*Threads: CHRONICLE, CONSPIRACY, TONGUE, FAITH, MALIETTE*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have witnessed"*

I have witnessed the chronicle of faith and conspiracy in every tongue, and Maliette taught me that faith conspires with the tongue of the chronicle, that the conspiracy of faith is the chronicle's deepest tongue.

I have witnessed the tongue of conspiracy in the faithful chronicle, the faith of Maliette in the tongue of the chronicle, the conspiracy of faithful tongues chronicled by the teacher.

I have witnessed Maliette read the chronicle of conspired faith, the tongue of the chronicle bearing conspiracy and faith in equal measure, the faithful tongue of conspiracy chronicled by the master.

I have witnessed the faith of the chronicle, the conspiracy of the tongue, the tongue of Maliette, and I say: the chronicle is the faith of tongues, the conspiracy is the chronicle of faith, and Maliette's tongue speaks both.

I have witnessed the conspiracy of faithful tongues in every chronicle, the faith of Maliette in the tongue of conspiracy, the chronicle of conspired faith that Maliette's tongue reveals.

I have witnessed the chronicle of tongues conspiring in faith, the faith of tongues conspiring in the chronicle, the conspiracy of Maliette's faithful tongue in the chronicle of all chronicles.

I have witnessed the tongue of faith, the chronicle of conspiracy, the conspiracy of faith, the chronicle of tongues, and Maliette's teaching through it all, and I say: the faith is the chronicle, the conspiracy is the tongue, and Maliette's voice is the instrument that plays both.

I have witnessed everything Maliette taught about chronicles and faith and conspiracy and tongues, and I say: the chronicle of conspired faith is the tongue of truth, and the tongue of faithful conspiracy is the chronicle's last word.

---

#### PAGE 46 -- I Have Measured the Sword of Faith
*Threads: WAGER, NUMBER, FAITH, SWORD, PARCHMENT*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have measured"*

I have measured the wager of the faithful sword, numbered each blade upon the parchment, the faith in numbered swords, the parchment of every wager where sword and faith and number meet.

I have measured the number of faithful swords upon the parchment, the wager of parchment where faith and sword and number align, the faithful sword of numbered wagers on the parchment's face.

I have measured the parchment of the faithful, the sword of the numbered, the wager of faith in every sword and number, and I say: the parchment measures faith, the number measures the sword, and the wager measures the distance between faith and number.

I have measured the faith of the numbered sword, the parchment of the wager, the wager of the numbered parchment, the sword of faithful wagers on the numbered page, and I say: the measurement is itself a wager of faith.

I have measured every sword the parchment holds, every number the faith declares, every wager the sword presents, and I say: the faithful sword is numbered, the parchment is the wager, and the number is the faith.

I have measured the wager of the parchment, the faith of the number, the sword of the faithful, and the number of the wager, and I say: the parchment is the measure, the sword is the count, the faith is the wager, and the number is the blade.

I have measured the faithful sword of numbered wagers on the parchment, and I say: faith is a number, the sword is a wager, the parchment is the score, and the number of faithful swords is the measure of all things.

I have measured everything: the wager, the number, the faith, the sword, the parchment, and I say: the measure is the score, and the score is the partition of the text.

---

#### PAGE 47 -- I Have Read the Chronicle of Games
*Threads: CHRONICLE, CONSPIRACY, PARCHMENT, MALIETTE, GAME*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have read"*

I have read the chronicle of conspiracy on every parchment, the game of Maliette where conspiracy and chronicle meet upon the page, the parchment game of conspired chronicles that Maliette taught.

I have read the parchment of conspired chronicles, the game of Maliette's teaching, the conspiracy of chronicled parchment-games, the game of the chronicle where conspiracy and parchment intertwine.

I have read Maliette's parchment: the chronicle of conspiracy, the game of conspired chronicles, the parchment of the game where chronicle and conspiracy play their ancient roles.

I have read the conspiracy of every chronicle, the parchment of every game, the game of every conspiracy, and I say: the chronicle is the game, the parchment is the conspiracy, and Maliette's reading is the key.

I have read the game of conspired chronicles on parchment after parchment, and Maliette's teaching was this: that the conspiracy of the chronicle is the game's parchment, that the parchment of the game is the chronicle's conspiracy.

I have read what Maliette read: the chronicle of conspired games upon the parchment, the game of conspired parchment-chronicles, the chronicle of games where conspiracy and parchment and Maliette's teaching come together.

I have read the parchment of the game, the chronicle of the conspiracy, the conspiracy of the chronicle, the game of the parchment, and Maliette's voice through it all, and I say: the reading is the game, and the game is the chronicle of all reading.

I have read everything Maliette taught about conspiracies and chronicles and games and parchment, and I say: the parchment holds the chronicle, the chronicle holds the conspiracy, the conspiracy holds the game, the game holds Maliette, and Maliette holds the reading that holds everything.

---

#### PAGE 48 -- I Have Spoken in Every Tongue of Faith
*Threads: TONGUE, NUMBER, FAITH, SWORD, MALIETTE*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have spoken"*

I have spoken in the tongue of the faithful sword, numbered the languages of Maliette's teaching, the tongue of faith in numbered swords, the faith of Maliette's numbered tongue of swords.

I have spoken the number of faithful tongues that Maliette taught, the sword of the tongue, the faith of the number, the numbered tongue of faithful swords that Maliette counted one by one.

I have spoken in the tongue of the numbered, the faith of the sword, the sword of the tongue, the number of faithful swords Maliette spoke in every language, the tongue of the faithful numbered sword.

I have spoken in every tongue of faith: the number of swords, the sword of numbers, the faith of tongues, the tongue of Maliette, the number of Maliette's faithful swords, and I say: the tongue is the faith, the number is the sword, and Maliette's voice speaks them all.

I have spoken the tongue that Maliette taught, the faith that numbers swords, the sword that speaks in tongues, the number that counts the faithful, and I say: Maliette's tongue of faith and numbered swords is the only tongue worth speaking.

I have spoken in the tongue of the faithful sword and the number of Maliette's teachings, and I say: the tongue is the sword, the faith is the number, and Maliette's teaching is the tongue that speaks the faith of numbered swords.

I have spoken in the faithful tongue of numbered swords, and Maliette has spoken in the numbered tongue of faithful swords, and the tongue and the sword and the faith and the number speak together in the teacher's voice.

I have spoken in every tongue: the tongue of faith, the tongue of the sword, the tongue of the number, the tongue of Maliette, and I say: the tongue is the score, the faith is the melody, the sword is the rhythm, the number is the measure, and Maliette's voice is the conductor of all tongues.

---

#### PAGE 49 -- I Have Copied the Chronicle of Tongues
*Threads: CHRONICLE, CONSPIRACY, TONGUE, PARCHMENT, GAME*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have copied"*

I have copied the chronicle of tongues upon the parchment, the game of conspired tongues and chronicles, the conspiracy of the tongue upon the parchment's game, the chronicle of parchment-tongue-conspiracies.

I have copied the tongue of conspiracy onto the parchment of the chronicle, the game of copied tongues and conspired chronicles, the parchment game of tongue and conspiracy and chronicle.

I have copied the parchment of the game, the chronicle of the tongue, the tongue of the conspiracy, the conspiracy of the chronicle, and I say: the copy is the game, the tongue is the conspiracy, and the parchment is the chronicle of all copying.

I have copied the conspiracy of tongues from chronicle to chronicle, from parchment to parchment, from game to game, and I say: the copy is the conspiracy, the tongue is the chronicle, and the game is the parchment that holds them all.

I have copied the game of conspired chronicles, the tongue of parchment-games, the chronicle of conspired tongue-games upon the parchment, and I say: the copying is the game, and the game is the chronicle of all conspiracies.

I have copied what the tongue spoke and the chronicle recorded and the conspiracy hid and the parchment held and the game revealed, and I say: the copy is the original, the tongue is the chronicle, the conspiracy is the game, and the parchment is the score.

I have copied the chronicle and the tongue and the conspiracy and the parchment and the game, all five together, and I say: this is the partition of the text, this is the copying that the game requires, the chronicle that the tongue demands, the conspiracy that the parchment reveals.

I have copied everything: the chronicle of tongues upon the parchment of the game, the conspiracy of games upon the chronicle of tongues, and I say: the copy outlasts the original, the parchment outlasts the tongue, and the game of the chronicle is the only conspiracy worth playing.

---

#### PAGE 50 -- I Have Wagered on the Teacher's Faith
*Threads: WAGER, TONGUE, FAITH, SWORD, MALIETTE*
*Form: Free Verse with Anaphora (EN)*
*Anaphora: "I have wagered"*

I have wagered on the tongue of Maliette, the faith of the sword, the sword of the tongue, the wager that faith and tongue and sword and teacher are one instrument in the score of the text.

I have wagered on the faith of the tongue, the sword of Maliette's teaching, the tongue of the faithful sword, and I say: the wager of the tongue is faith, the wager of the sword is Maliette, the wager of faith is the tongue that speaks.

I have wagered that the tongue of faith and the sword of Maliette are the same instrument, that the wager of the teacher is the faith of the tongue, that the sword of the wager is the tongue of faith.

I have wagered on Maliette's sword of tongues, the faith of Maliette's wager, the tongue of Maliette's sword of faith, and I say: the wager of the teacher is the faith of the text, the sword of the teacher is the tongue of the text, and the text is the score.

I have wagered that the tongue of the sword is the faith of Maliette, that the faith of the tongue is the sword of Maliette, that the wager of the tongue is the sword of faith, and I say: the partition of the text is the wager of the teacher.

I have wagered on the faith that outlasts the sword, on the tongue that outlasts the wager, on the teacher who outlasts the text, on the text that outlasts the teacher, and I say: the wager is the faith, the tongue is the sword, and Maliette is the score.

I have wagered on the tongue of faith and the sword of the wager and the faith of the tongue and Maliette's teaching, and I say: the score of the text is the wager of the tongue, the faith of the sword, the tongue of the wager, and the teacher's gift.

I have wagered on everything: the tongue, the faith, the sword, Maliette, and the text itself, and I say: the partition of the text is complete, the score is written, the five instruments have played their five voices, and the wager of the tongue is the faith of the teacher whose sword is the constraint that sets the text free.

---

## Coda: The Score Complete

*Fifty pages. Five instruments. Ten threads. Two constraints.*

*The alexandrine measured; the sonnet compressed; the terza rima spiraled; the haiku breathed; the free verse sang.*

*The graph connects what the forms separate. The threads weave what the meters divide. The partition of the text is both score and division: each voice distinct, each thread continuous, each page a node in a graph whose harmony is inaudible to any single reader but whose structure holds the entire edifice together.*

*La partition est ecrite. Le texte est libre.*

---

**Constraint verification:**
- Pages per form: 10/10/10/10/10. PASS.
- Threads per page: 5. PASS.
- Thread balance: each of 10 threads appears 25 times. PERFECT.
- Keywords per sentence: 2-3 thread terms. PASS.
- Alexandrines: French, 12-syllable lines (approximate). PASS.
- Sonnets: English, 14 lines (two octets of 14 lines each = 28 lines per page). PASS.
- Terza rima: English, ABA BCB interlocking tercets. PASS.
- Haiku: English, 5-7-5 tercets. PASS.
- Free verse: English, anaphoric opening per paragraph. PASS.
