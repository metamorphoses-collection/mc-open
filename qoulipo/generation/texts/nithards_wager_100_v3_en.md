# Nithard's Wager 100 v3 — Hard-Zone Edition (English)

Version 3 (2026-04-10): deliberate combinatorial design targeting d ≥ 0.30 at k=25 under `multilingual-e5-large-instruct`.

Three voices weave through this constrained text: **Nithard** the Carolingian chronicler, **Pascal** the mathematician of wagers, and the **Professor**, Porteur de Maliettes, who arrives from a later century carrying the apparatus of proofs.

Ten thematic threads are rotated through the 100 pages: **CHRONICLE, FAITH, TONGUE, WAGER, MALIETTE, NUMBER, PARCHMENT, SWORD, CIPHER, DREAM**. Each page activates exactly five of these threads, their keywords saturating every sentence. Pages are organized in five thematic clusters of twenty pages each; within a cluster, three threads are mandatory (the cluster core) and two rotate, producing planted within-cluster similarity and looser cross-cluster similarity. Target: a graph density above the Cazals hard-zone threshold at k=25 with the current multilingual embedder.

The thread matrix itself is deposited at `3_MIS/oulipo/designs/thread_matrix.json`; the predicted overlap distribution is at `predicted_density.json`. The pilot pages below are pages 1–10 of cluster 0, whose core threads are CHRONICLE, FAITH, and TONGUE.

---

## Cluster 0 — Chronicle, Faith, Tongue

### Page 1 — The chronicler takes up his quill
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, CIPHER*
*Voice: NITHARD*

I, Nithard, nephew of Charlemagne and son of a poet-abbot, begin this chronicle as a man takes up a wager with time. The quill in my hand is the quill of a chronicler who knows his chronicle will outlive him only if faith and tongue conspire to keep it alive. My faith is not the comfortable faith of a monk in a well-endowed abbey; it is the faith of a chronicler who has seen his Christian cousins cut each other to pieces at Fontenoy, and who writes in a tongue that is neither fully Latin nor fully the Romance tongue of the soldiers beneath the rain. The chronicle I undertake is a wager on the survival of a tongue that has never before carried a chronicle of this kind, and the wager is sealed by a cipher of faith that I place in the margin of every parchment.

The cipher is simple and it is not simple. In the margin of each chronicle page I mark a small cross where faith has steadied the tongue, and a circle where the tongue has betrayed the chronicle, and a vertical stroke where the wager of writing has nearly cost me the chronicle itself. Anyone reading this chronicle in a later century will, if they read it in the tongue it was written, recognise the cipher; anyone translating it into a purer tongue will lose the cipher and with it the private chronicle of my faith. This is the wager I make against time: that a tongue and a cipher together will carry the chronicle where faith alone could not.

I write this first chronicle page in the language my cousins the soldiers speak at the campfire, the Romance tongue in which the oaths of Strasbourg were sworn, and I ask the reader to trust that my faith and my chronicle and my tongue are all wagers on the same outcome. The cipher in the margin is the only proof I can leave.

---

### Page 2 — Pascal reads Nithard in the margin
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, CIPHER*
*Voice: PASCAL*

I, Pascal, reading Nithard's chronicle eight centuries after it was written, find in the margin a cipher that the chronicler's faith encoded into the tongue of his chronicle. The chronicler's wager was a wager on the tongue; my wager is a wager on faith itself, but the two wagers turn out to be the same wager encoded in different ciphers. Where Nithard writes his chronicle in the Romance tongue because the Latin tongue cannot carry the faith he feels, I write my wager in French because the Latin of the schoolmen cannot carry the faith I calculate. The chronicle of faith that moves between the two of us, across the centuries, is a single chronicle in two tongues, each tongue a cipher for the same wager.

The cipher of my wager is arithmetic: if faith wins, the gain is infinite; if faith loses, the stake is finite; therefore any rational chronicle of the wager must favour faith. Nithard's cipher is narrative: if the chronicle survives, the Romance tongue wins its wager against Latin; if the chronicle burns, the tongue loses nothing because no faith had been placed in it. The two ciphers meet in the margin of Nithard's chronicle, where faith in a tongue and faith in a wager are copied onto the same vellum by two chroniclers separated by a silence the length of eight centuries.

I have spent the whole of a winter in the library reading Nithard's chronicle in the original tongue, decoding his cipher, and transposing the cipher into the algebra of my wager. The result is a table of correspondences: each mark in Nithard's margin maps to a fragment of my *Pensées*, each fragment of my *Pensées* maps back to a chronicler's act of faith in the tongue of his chronicle. The wager, in the end, is whether any chronicle can be written in a tongue whose cipher a later chronicler will still be able to read. Faith says yes; the chronicle says perhaps; the cipher says: try.

---

### Page 3 — The Professor opens the maliette
*Threads: CHRONICLE, FAITH, TONGUE, MALIETTE, NUMBER*
*Voice: PROFESSOR*

I am the Professor, the Porteur de Maliettes, and in the maliette I carry from seminar to seminar there lies the chronicle of Nithard and the table of numbers that Pascal transposed from Nithard's cipher. The maliette is a small leather case that I keep on the floor beside the lectern, and when I open it I do not open it all at once: I draw out the chronicle first, then the tongue in which it was written, then the faith that encoded the chronicle, then the numbered table that Pascal drew up in the margin. Each item in the maliette corresponds to a numbered page of the chronicle, and each number corresponds to a fragment of a faith that has survived because a chronicler took the wager of writing it in the only tongue that could carry it.

The numbers I teach the students are not the numbers of the tax-rolls or the numbers of the census: they are the numbers of a chronicle, the numbered pages on which a tongue and a faith jointly enact the passage of time. I say to the students: the chronicle is not a record of events. The chronicle is a numbered table of faith's refusals and the tongue's acceptances. The number seven recurs in Nithard's chronicle with a regularity that the chronicler himself perhaps did not notice, but that Pascal noticed in the eighteenth century and that I have numbered in the maliette for the students to see. Seven folios, seven cross-marks in the margin, seven pages on which the tongue veers from Latin to Romance, seven chronicles within the chronicle.

I close the maliette. The students are watching. One of them asks me whether the numbers in the chronicle prove the faith of the chronicler or only the arithmetic of the mathematician who read him. I say: the numbers prove neither. The numbers carry the chronicle in a maliette across the centuries, and the faith lives in the tongue in which the numbers were first copied down. That is the whole of what the maliette contains, and it is enough.

---

### Page 4 — Nithard on the Romance tongue
*Threads: CHRONICLE, FAITH, TONGUE, MALIETTE, DREAM*
*Voice: NITHARD*

I, Nithard, dreamt last night of a maliette in which my chronicle was kept, though the maliette belonged to no reader I could name. In the dream the maliette was leather and iron, and inside it lay a copy of my chronicle in a tongue I could not fully read — it had the cadence of my Romance tongue but it carried inflections that felt strange, and the faith that moved between its sentences was a faith that had passed through centuries I could not see. I woke before I could read the dream's chronicle to the end, and when I woke I knew I had been dreaming of a reader yet unborn who would carry my chronicle in a maliette to a place I could not follow.

The Romance tongue in which I write this chronicle is not a noble tongue. It is the tongue of the soldiers, the tongue of the women at the well, the tongue of the Strasbourg oaths that my cousins swore to each other in the year before Fontenoy. My faith in this tongue is the faith of a chronicler who has no other tongue in which to tell the chronicle of his dreams. The Latin tongue would have given my chronicle the authority of the schoolmen, but the Latin tongue could not have given my chronicle the authority of a dream — and my chronicle, I now realise, is partly a chronicle of dreams as much as it is a chronicle of battles and treaties and oaths.

In the maliette of my dream the chronicle had been copied by a hand I did not know, and the copy had been folded into a maliette I did not own, and the faith in the margin was the faith of someone whose tongue I could not fully hear. But the faith was the same faith, and the chronicle was the same chronicle, and the dream tells me the maliette will travel further than the chronicler who first wrote the chronicle in the Romance tongue of his faith. The chronicle will sleep in maliettes for centuries. The dream tells me this. I believe the dream.

---

### Page 5 — Pascal's table
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, CIPHER*
*Voice: PASCAL*

My table is a table of the wager. In one column I have written the gain if the wager on faith is won, and in another column I have written the loss if the wager is lost, and in a third column I have written the cipher by which Nithard's chronicle encoded the same wager eight centuries before my table was drawn. The three columns do not have the same tongue: the gain is written in algebra, the loss is written in the Romance tongue of Nithard's chronicle, and the cipher is written in a mixed tongue that belongs neither to the algebra of the wager nor to the Romance tongue of the chronicle. This mixed tongue is the tongue of my own faith, which has to negotiate between the algebra and the chronicle if it is to carry the wager to any conclusion.

The cipher in the margin of Nithard's chronicle resembles the ciphers I have used in my correspondence with Fermat, and for a long winter I believed that the two ciphers were the same. They are not. Nithard's cipher is a cipher of faith: it marks where the chronicler's tongue trembled and where his faith steadied it, and it does not carry any number except the number of the chronicle page on which the cipher appears. My cipher is a cipher of the wager: it carries a number that signifies the odds of faith against the odds of unfaith, and the number does not mark any tongue except the tongue of arithmetic. But both ciphers live in margins, and both ciphers encode a wager, and both chroniclers — Nithard in his Romance tongue and I in my French — wagered their chronicles on the survival of a faith carried by a tongue.

The table I have drawn is therefore a table of correspondences between two ciphers of one wager, and when I place it beside Nithard's chronicle I can read the chronicle as the prehistory of my wager and the wager as the afterlife of the chronicle. The faith that moves between them is a single faith in two tongues, and the cipher that encodes the faith is a single cipher written twice.

---

### Page 6 — The Professor on dreams and ciphers
*Threads: CHRONICLE, FAITH, TONGUE, CIPHER, DREAM*
*Voice: PROFESSOR*

The chronicle that Nithard wrote in the Romance tongue is, among other things, a chronicle of dreams — and I, the Professor, Porteur de Maliettes, want to put that fact in front of my students this morning. The cipher in the margin of Nithard's chronicle marks the passages where the chronicler recorded a dream. Pascal did not notice this; Pascal read the cipher as a cipher of faith only, because Pascal was interested in the wager and not in the dream. I read the cipher as a cipher of dreams, because a dream in a chronicle is a place where the chronicler's tongue admits that it cannot tell the whole chronicle without borrowing from another tongue — the tongue of sleep, the tongue of vision, the tongue in which chronicles are written before anyone has the Romance tongue in which to copy them onto the parchment.

The cipher in the margin of Nithard's chronicle therefore has two layers. One layer is Pascal's layer: the cipher marks a wager of faith against unfaith, and each mark encodes a judgement the chronicler made about whether his tongue had or had not carried the faith of the passage. The other layer is the layer of dreams: the cipher marks a passage in which the chronicler admitted that his chronicle had crossed over, for a sentence or a paragraph, into the tongue of a dream he could not fully remember on waking. The two layers coexist in the margin without contradicting each other, because the chronicler's faith was a faith that included the authority of dreams, and the chronicler's tongue was a tongue that could carry the cipher of both layers.

I show the students how the cipher layers onto the chronicle. I open the maliette and I draw out the folio with the clearest examples, and I let the students see how a single mark in the margin can mean both 'faith here' and 'dream here' and still not mean two contradictory things. The chronicle of Nithard is a chronicle in which the tongue of faith and the tongue of dreams meet, and the cipher in the margin is the sign that they meet.

---

### Page 7 — Nithard before Fontenoy
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, SWORD*
*Voice: NITHARD*

The dawn of Fontenoy, June 841: I am writing this chronicle by memory, long after the sword has rested and the blood has dried, and I can still hear the sound of the wager that was placed that morning on the fate of an empire. The sword of my cousin Lothair met the sword of my cousin Louis and my cousin Charles, and the chronicle of what the swords did is a chronicle that I set down in the Romance tongue of the soldiers rather than in the Latin tongue of the clerks, because the Latin tongue cannot carry the weight of what the swords did. My faith that morning was a soldier's faith: that the wager of steel against steel would resolve a chronicle that had refused to resolve itself by word or by oath for seven long years.

The Romance tongue in which I now write this chronicle is the tongue in which the wager was placed. My cousin Louis swore his oath to his men in the Romance tongue; my cousin Charles swore his oath to Louis's men in a tongue I shall call Teudisca, and the chronicle of the oaths — the Strasbourg oaths, that I copied into my chronicle in their exact tongues — is a chronicle of how the faith of each brother was translated into the sword of each brother's men. The wager was not merely a wager between three brothers; it was a wager between two tongues that each carried a different chronicle of the same faith.

I remember that morning: the rain and the mud, and the priest moving between the ranks with the consecrated bread, and the sword at my belt heavier than the chronicle of all the years that had led to this field. The wager of steel was placed. The sword did its chronicle-work. At the end of the day the Romance tongue had the chronicle of a victory, and the Latin tongue of the clerks had the chronicle of a disaster, and my chronicle in the Romance tongue is the only chronicle that tried to carry both faiths at once. The sword was the cipher of the wager, and the wager decided the chronicle, and the chronicle decided the tongue in which the chronicle would be remembered.

---

### Page 8 — Pascal on the sword in the margin
*Threads: CHRONICLE, FAITH, TONGUE, PARCHMENT, SWORD*
*Voice: PASCAL*

In the margin of Nithard's chronicle of Fontenoy there is a small sword drawn beside a passage where the chronicler's tongue broke. The sword in the margin is a cipher of the sword in the field. I have seen the parchment in the library of Saint-Germain and I can testify that the sword is drawn in a hand that is not the chronicler's hand — it is a later hand, perhaps a copyist's hand, perhaps the hand of a reader who wanted to mark where the chronicle of the sword had overwhelmed the chronicler's tongue. The parchment is old enough that the ink of the sword is darker than the ink of the chronicle's letters, and the parchment has been folded at that page more often than at any other, so that the sword in the margin is half-worn by centuries of hands and faith.

My chronicle of this chronicle — for a mathematician too can write a chronicle, and a faith can be carried by a table of correspondences as well as by a parchment — is that the sword in the margin encodes a wager that the chronicler could not place. Nithard could not place the wager of steel because Nithard was the nephew of the emperor who had died and the son of a poet-abbot who had died, and Nithard's faith in the Romance tongue did not give him the standing to declare the wager of the sword won or lost. The copyist who drew the sword in the margin was placing the wager that Nithard could not place. The sword was drawn in the later ink because the later reader had the faith Nithard lacked.

The parchment is what survived. The chronicle is what the parchment carried. The sword in the margin is the cipher of the wager that was placed not by the chronicler but by a reader who understood that the chronicle of the sword needed a witness the chronicler could not be.

---

### Page 9 — The Professor and the dream of the chronicle
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, DREAM*
*Voice: PROFESSOR*

My students ask me whether the chronicle of Nithard is a chronicle of facts or a chronicle of dreams, and I tell them that the question is the wrong question. The chronicle of Nithard is a chronicle of the places where a faith in a tongue was tested by a wager against time. Some of those places are places where facts happened — the battle of Fontenoy, the oaths of Strasbourg, the death of this emperor or that brother — and some of them are places where dreams happened, and a dream in a chronicle is as much a fact as a battle, provided the chronicler had the faith to write the dream down in the tongue of the chronicle.

The wager that Nithard placed when he wrote the chronicle in the Romance tongue rather than the Latin tongue of the clerks was a wager that a dream could be chronicled as reliably as a battle, provided the chronicler's faith was equal to the task. My own wager, teaching this chronicle eight centuries later, is that a dream in a chronicle is the only kind of fact that survives without distortion, because a dream is already a translation before it reaches the tongue of the chronicler, and a translation that has already happened cannot be further corrupted by a second translation into the reader's tongue.

I tell the students the following paradox: the battles in Nithard's chronicle have all been mistranslated at least once in the centuries since they were fought, because every tongue that carried the chronicle had to translate the battles into its own idiom. But the dreams in Nithard's chronicle have remained exact, because a dream has already been translated by the chronicler's sleep and nothing the reader does can translate it further. The wager of the chronicle is therefore a wager that the dreams will be remembered more reliably than the facts — and the chronicle of Nithard, read carefully, is the proof of the wager.

---

### Page 10 — Nithard sends the maliette forward
*Threads: CHRONICLE, FAITH, TONGUE, WAGER, MALIETTE*
*Voice: NITHARD*

I, Nithard, imagine a maliette into which I shall place this chronicle when my chronicle is done, and I send the maliette forward in time the only way a chronicler can send anything forward: by writing the chronicle in a tongue that the faith of later readers will keep alive. The maliette I imagine is not the leather case that holds my parchment in the scriptorium of Saint-Riquier; it is the shape of a wager made against the silence of all the centuries that will pass between the writing of the chronicle and the reading of it. The maliette is a faith carried by a tongue, and the chronicle is the weight that the maliette will carry, and the wager is that the weight will not be too heavy for the tongue to bear.

I send the maliette forward to a reader who will speak a tongue I do not recognise but whose faith I will recognise when I hear them reading the chronicle. I send it forward to a Pascal who will draw a table of correspondences between my chronicle and his own wager, and to a Professor who will open the maliette in front of his students in a lecture-room I cannot imagine, and to a copyist who will draw a small sword in the margin of the page on which my chronicle of Fontenoy nearly broke under the weight of the chronicle. The maliette goes forward to all of them at once, because the maliette is a wager that carries all of them as its cargo.

My faith is that the maliette will arrive. My chronicle is the only ticket the maliette carries. My tongue is the only visa the maliette requires. The wager is between me and the silence, and the silence has no language of its own, and the chronicle in its Romance tongue will therefore beat the silence by the length of a faith that a tongue alone can carry. I close the parchment. The maliette is sealed. The chronicle sends itself forward.

---

*Pages 11–20 and beyond: to be written in a subsequent burst after pilot-graph validation of pages 1–10.*

---

## Cluster 1 — Wager, Maliette, Number (pilot pages 21-25 for cross-cluster gap measurement)

### Page 21 — Pascal tabulates the maliette
*Threads: WAGER, MALIETTE, NUMBER, CIPHER, DREAM*
*Voice: PASCAL*

I, Pascal, number the contents of a maliette that came into my hands last winter, and the number is not the number I expected. The maliette is a small leather case, the kind a travelling wager-taker might carry to the fairs, and inside it I have counted forty-two folios, each one numbered in the hand of a different scribe. The wager I am entering into, by opening this maliette at all, is a wager against my own arithmetic: that the numbers on the folios will turn out to obey a cipher I can break, and that the cipher, once broken, will reveal a dream that the compilers of the maliette did not know they were compiling. The number forty-two, I notice at once, is the same number of wagers that I have already placed in the margins of my own work, and this coincidence of numbers is the first cipher the maliette presents.

The wager at the heart of the maliette is not a wager about money. It is a wager about whether a dream, once numbered and cataloged and placed inside a maliette, retains the quality of a dream or becomes instead a mere entry in a ledger. I have spent the winter numbering the folios of the maliette — forty-two of them, each folio numbered with a cipher I did not at first understand — and I have discovered that the numbers themselves encode a second wager: the wager that a dream can survive its own numbering, that a cipher can be broken without killing the dream it encodes, that a maliette can carry numbers without reducing its contents to arithmetic. The wager is a wager on the integrity of the dream against the discipline of the number.

I place the folios back into the maliette in the order the numbers require and I close the lid. The wager is still open. The number on the lid is forty-two, and the cipher of the number is a cipher I have begun to understand but have not yet broken. The dream, I suspect, will not survive my breaking of the cipher — but the maliette will, and the number on the maliette will, and the wager that was placed when the maliette was first sealed will outlast both the dream and the breaking of its cipher.

---

### Page 22 — The Professor and the numbered folios
*Threads: WAGER, MALIETTE, NUMBER, PARCHMENT, CIPHER*
*Voice: PROFESSOR*

The maliette that Pascal numbered is now in my possession, the Professor's, and in front of my students I count the folios again. There are still forty-two, each folio numbered in a distinct hand, each number carrying the cipher of a wager that was placed by a different chronicler. The parchment of each folio is of different ages — some from the twelfth century, some from the sixteenth, one that I believe to be thirteenth-century — and the wager that unites them is a wager that the numbers will hold across the centuries even when the parchment itself is fragile. I pick up folio seventeen — the parchment is brittle, the cipher in the upper corner is a single numeral and a small cross — and I read the wager it encodes.

The wager of folio seventeen is a wager about whether a cipher on a parchment can be decoded by someone who does not know the tongue the cipher was written in. The chronicler who placed this wager was confident, because the cipher is simple and the parchment is sturdy and the number is memorable. But the decoder of the wager — me, the Professor, standing here eight centuries later with my maliette of folios — has no knowledge of the tongue in which the cipher was originally keyed, and my decoding of it is an approximation, a guess, a reading that takes the cipher on trust rather than on proof. The wager was not lost, because I have recovered something; the wager was not won, because what I have recovered is not what the chronicler placed. The parchment holds. The number holds. The cipher, however, has degraded.

I hand folio seventeen to a student and ask her to copy the number onto a fresh parchment. She does so, and I number the copy and place the copy in the maliette beside the original. The wager is now placed on two parchments, two numbers, two ciphers. The maliette now contains forty-three folios. The number has increased by one. The wager continues.

---

### Page 23 — Nithard dreams of a ledger
*Threads: WAGER, MALIETTE, NUMBER, CHRONICLE, DREAM*
*Voice: NITHARD*

I dreamt last night that my chronicle had become a ledger, and the ledger was kept inside a maliette, and the maliette was being numbered by a hand I did not recognize. In the dream every entry in my chronicle — every battle, every oath, every treaty — had been reduced to a number in the ledger, and the numbers were organized in columns of wagers won and wagers lost, and the maliette was being carried from one counting-house to another by a bearer who did not know the tongue in which my chronicle had originally been written. The dream unsettled me because the ledger was a kind of chronicle, but a chronicle drained of its tongue and its faith, and I woke before the dream could tell me who the bearer was.

The dream suggests that my chronicle will one day be read as a ledger, and I do not know whether this is a loss or a gain for the chronicle. A ledger is a precise chronicle — each number verifiable, each wager accounted for, each entry reducible to an exchange — and my chronicle has moments of such precision. But a ledger is also a chronicle without dreams, a chronicle without the faith in a tongue that makes a chronicle worth writing, and my chronicle has very many dreams that no ledger could accommodate. The dream I had last night is one of those dreams. It does not belong in any ledger. It belongs in a chronicle whose maliette travels through the centuries carried by a bearer who can read the chronicle's tongue.

I write the dream down in my chronicle this morning, and I mark it in the margin with a small cipher so that a later reader will know that this passage of the chronicle is a dream. The maliette of the chronicle is slightly heavier this morning for the weight of the dream that has been added to it, and the number of folios in the maliette has increased by one, and the wager of the chronicle continues.

---

### Page 24 — Pascal on the cipher of the dream
*Threads: WAGER, NUMBER, CIPHER, DREAM, PARCHMENT*
*Voice: PASCAL*

A dream is a cipher placed on a parchment that the dreamer did not consent to sign. I write this proposition at the head of a new table that I have begun to draw up, a table in which the wager of every dream I have catalogued is numbered and the cipher of the wager is transcribed in a column beside the number. There are already thirty-six dreams in the table, each one a small wager placed by the dreamer against the interpretation of some later reader, and the cipher of each dream is a cipher I have tried to break by arithmetic alone, without recourse to the tongue in which the dream was originally dreamt. The parchment on which I write this table is a cheap parchment; the dreams in the table are not.

The number of dreams in my table is thirty-six, but the cipher of each dream is different, so the table has thirty-six ciphers and one wager. The single wager is the wager that any cipher, however private, can be broken by enough arithmetic applied with enough discipline. My arithmetic is disciplined — I have been practising it all my life — but the ciphers are resisting. I suspect that the ciphers are resisting not because my arithmetic is inadequate but because a cipher placed on a parchment without the dreamer's consent cannot be broken by arithmetic at all. It can only be broken by a second dream in which the cipher is decoded by a dreamer who has dreamt the same dream.

I place the parchment of the table inside the maliette that Nithard sent forward and that I have inherited. The cipher of the table is now the cipher of a wager placed against my own arithmetic. I close the maliette. The number of folios in the maliette is forty-three. The wager continues. The dreams remain unbroken, and the ciphers that encoded them remain intact, and the parchment that carries the table of dreams is now a cipher in its own right, waiting for a dreamer yet unborn to break the cipher by dreaming the same dream I dreamt when I first drew up the table.

---

### Page 25 — The Professor on hidden numbers
*Threads: WAGER, MALIETTE, NUMBER, CIPHER, SWORD*
*Voice: PROFESSOR*

In the maliette there are numbers that refer to other numbers. I show the students a folio on which the chronicler has written a number that turns out, after decoding, to be a cipher pointing to another number on a different folio. The cipher is a sword-cipher — a system used by Carolingian scribes to hide numerical information from the clerks of rival courts — and the wager placed by the chronicler was a wager that the sword-cipher would survive long enough for the intended reader to decode the hidden number. The intended reader, I tell the students, was very possibly me, or someone very like me, teaching this chronicle eight centuries later with a maliette full of numbered folios.

The sword-cipher works as follows: each number in the chronicle is encoded by a small drawing of a sword whose blade-length, hilt-type, and pommel-shape together encode three digits. A short blade is 0, a long blade is 9; a plain hilt is 0, an ornate hilt is 9; a round pommel is 0, a squared pommel is 9. The three digits concatenated give the hidden number, and the hidden number points to a folio elsewhere in the maliette. The wager placed by the chronicler is that a later reader will count the blades, hilts, and pommels correctly and will recover the hidden number before the parchment containing the sword crumbles to dust.

I pick up the folio I want the students to see. It contains a single sword drawn in the lower margin. I count its blade-length and I count its hilt-type and I count its pommel-shape, and the number I recover is forty-two. The number forty-two, the students understand, is the number of folios Pascal first counted in this maliette when it came into his hands in the seventeenth century. The wager is therefore won: the chronicler's sword-cipher has survived long enough for this class of students to decode it. The maliette contains, by my count, forty-three folios now, but the number the cipher encodes is forty-two, and the discrepancy is a new wager I shall place before the next class.
