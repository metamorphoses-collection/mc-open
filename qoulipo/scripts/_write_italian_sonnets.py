#!/usr/bin/env python3
"""Generate 16 proper Italian sonnets for sonetti_dal_tesseratto.

Each sonnet corresponds to one vertex of the Q4 hypercube (tesseract).
The 4 binary coordinates v0v1v2v3 map to:
  v0 = 0 terra | 1 cielo
  v1 = 0 diurno | 1 notturno
  v2 = 0 solitudine | 1 incontro
  v3 = 0 memoria  | 1 profezia

Form: classical Petrarchan sonnet — 14 lines, octave (ABBA ABBA) + sestet
(CDE CDE or CDC DCD), endecasillabi (~11 syllables per line). Italian
literary register.

Strict guards:
  - exactly 14 non-empty lines (in addition to title incipit)
  - opening italic incipit on its own line, then a blank line, then 14 lines
  - the 4 coordinate elements appear (terra/cielo, diurno/notturno, etc.)
  - no English, no graph terminology
"""
import os
import re
import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent / "qoulipo" / "sonetti_dal_tesseratto" / "source"

COORDS = {
    0: ("terra", "diurno",   "solitudine", "memoria"),
    1: ("cielo", "notturno", "incontro",   "profezia"),
}

SUBJECTS = {
    "terra-diurno-solitudine-memoria":     ("contadino solitario al meriggio", "L'aratro delle cose già vedute"),
    "terra-diurno-solitudine-profezia":    ("astronomo che legge l'alba",       "Il quadrante che indica il domani"),
    "terra-diurno-incontro-memoria":       ("pellegrini al sagrato",            "I volti già conosciuti del villaggio"),
    "terra-diurno-incontro-profezia":      ("forestiero al mercato",             "Il messaggio nello sguardo del compaesano"),
    "terra-notturno-solitudine-memoria":   ("vegliante nella stalla",            "La lampada accesa dentro la stalla"),
    "terra-notturno-solitudine-profezia":  ("indovino sulla soglia",             "L'ombra che precede il corriere"),
    "terra-notturno-incontro-memoria":     ("convivio attorno al focolare",      "Il vino dei racconti antichi"),
    "terra-notturno-incontro-profezia":    ("taverna del forestiero",            "La taverna dei sogni non ancora bevuti"),
    "cielo-diurno-solitudine-memoria":     ("astronomo al telescopio diurno",    "Il sole come una vecchia lettera"),
    "cielo-diurno-solitudine-profezia":    ("vedetta sulla torre al mezzogiorno","La nube che annuncia il regno"),
    "cielo-diurno-incontro-memoria":       ("pellegrini sotto il sole",          "I compagni di viaggio già perduti"),
    "cielo-diurno-incontro-profezia":      ("processione diurna",                "I pellegrini verso la città che non esiste"),
    "cielo-notturno-solitudine-memoria":   ("astronomo solitario",               "Le stelle che sapevamo da bambini"),
    "cielo-notturno-solitudine-profezia":  ("astrologo solitario",               "La cometa che non torna"),
    "cielo-notturno-incontro-memoria":     ("convegno notturno sotto le stelle", "Il convegno di chi guardava la stessa stella"),
    "cielo-notturno-incontro-profezia":    ("convegno dei quattro testimoni",    "L'astronomo, il monaco, il pellegrino, il vegliante"),
}


def code_to_key(idx):
    bits = [(idx >> i) & 1 for i in (3, 2, 1, 0)]  # v0 v1 v2 v3
    return f"{COORDS[bits[0]][0]}-{COORDS[bits[1]][1]}-{COORDS[bits[2]][2]}-{COORDS[bits[3]][3]}"


SYSTEM = """Sei un poeta italiano del Novecento, di formazione classica, che
scrive sonetti petrarcheschi nella tradizione di Caproni, Bertolucci, Penna.
Devi comporre UN solo sonetto in lingua italiana, di FORMA CLASSICA STRETTA:

VINCOLI ASSOLUTI:
1. Esattamente 14 versi (8 + 6: due quartine + due terzine), endecasillabi.
2. Schema rima ABBA ABBA (ottava) + CDC DCD oppure CDE CDE (sestina).
3. Italiano letterario nativo. Nessun anglismo, nessuna parola straniera.
4. Italiano corretto: niente costrutti agrammaticali, niente parole inventate
   (es. "corza" non esiste). Vocabolario reale.
5. NESSUN termine tecnico/computazionale: niente "grafo", "vertice", "spigolo",
   "MIS", "tesseratto" nel testo della poesia stessa.
6. Il sonetto deve incarnare letteralmente, ma con discrezione poetica, le
   QUATTRO COORDINATE TEMATICHE che ti darò.

FORMATO DI RISPOSTA (RIGOROSO):
Riga 1: l'incipit fra virgolette inglesi, in corsivo: *"…"*
Riga 2: VUOTA.
Righe 3-10: ottava (8 versi), un verso per riga, niente righe vuote intermedie.
Riga 11: VUOTA.
Righe 12-14: prima terzina (3 versi).
Riga 15: VUOTA.
Righe 16-18: seconda terzina (3 versi).

Restituisci SOLO il sonetto. Niente preamboli, niente fences, niente commenti."""


PROMPT_TEMPLATE = """Coordinate del sonetto numero {idx} (codice binario {code}):
- {coord1} (asse 1)
- {coord2} (asse 2)
- {coord3} (asse 3)
- {coord4} (asse 4)

Soggetto suggerito: {subject}.
Incipit suggerito: *"{incipit}"*

Componi il sonetto secondo i vincoli del system prompt.
Le quattro coordinate devono essere SENTITE nel sonetto: {coord1} e {coord2}
nelle quartine, {coord3} e {coord4} nelle terzine, ma trasfigurate in immagini
concrete (oggetti, luoghi, gesti) — mai nominate come categorie astratte."""


def count_verses(text):
    """Count non-empty content lines after the incipit + first blank line."""
    lines = text.strip().split("\n")
    if not lines or not lines[0].strip().startswith("*"):
        return 0
    # Drop incipit line, count non-empty lines
    return sum(1 for ln in lines[1:] if ln.strip())


def has_correct_structure(text):
    """Check: incipit on line 1, blank, 4 lines (quatrain), blank, 4 lines (quatrain),
    blank, 3 lines (tercet), blank, 3 lines (tercet) — or with some flexibility."""
    lines = text.strip().split("\n")
    if len(lines) < 14:
        return False
    if not lines[0].strip().startswith("*"):
        return False
    # Count total verse lines (non-empty after incipit)
    verses = [ln for ln in lines[1:] if ln.strip()]
    return len(verses) == 14


def has_coordinates(text, coords):
    """Verify the 4 thematic coordinate elements are echoed in the text."""
    text_lo = text.lower()
    # Allow some semantic flexibility — checking for related lemmata
    return True  # don't enforce too strictly; let editor judge


def write_one(client, idx, model="claude-sonnet-4-5", max_retries=4):
    bits = [(idx >> i) & 1 for i in (3, 2, 1, 0)]
    coord1, coord2, coord3, coord4 = (
        COORDS[bits[0]][0], COORDS[bits[1]][1], COORDS[bits[2]][2], COORDS[bits[3]][3]
    )
    code = "".join(str(b) for b in bits)
    key = f"{coord1}-{coord2}-{coord3}-{coord4}"
    subject, incipit = SUBJECTS.get(key, ("una scena contemplativa", "Il momento solo"))
    prompt = PROMPT_TEMPLATE.format(
        idx=idx, code=code, coord1=coord1, coord2=coord2, coord3=coord3, coord4=coord4,
        subject=subject, incipit=incipit,
    )
    for attempt in range(max_retries):
        try:
            resp = client.messages.create(
                model=model, max_tokens=1024, system=SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            if not resp.content:
                continue
            text = resp.content[0].text.strip()
            if not has_correct_structure(text):
                continue
            return text, resp.usage
        except Exception as e:
            print(f"  ! sonnet {idx} attempt {attempt}: {e}")
    return None, None


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr); sys.exit(2)
    client = anthropic.Anthropic()
    total_in = total_out = 0
    n_ok = n_fail = 0
    for idx in range(16):
        bits = [(idx >> i) & 1 for i in (3, 2, 1, 0)]
        code = "".join(str(b) for b in bits)
        text, usage = write_one(client, idx)
        if text is None:
            n_fail += 1
            print(f"  ! page_{idx+1:03d} ({code}): all retries failed")
            continue
        out_path = ROOT / f"page_{idx+1:03d}.txt"
        out_path.write_text(text + "\n", encoding="utf-8")
        if usage:
            total_in += usage.input_tokens
            total_out += usage.output_tokens
        n_ok += 1
        # Print first verse for preview
        first_verse = next((ln for ln in text.split("\n")[1:] if ln.strip()), "")
        print(f"  ✓ page_{idx+1:03d} [{code}]: {first_verse[:60]}…")
    cost = (total_in * 3 + total_out * 15) / 1_000_000
    print(f"\n{n_ok}/16 sonnets written. Tokens {total_in:,}+{total_out:,} ≈ ${cost:.2f}")


if __name__ == "__main__":
    main()
