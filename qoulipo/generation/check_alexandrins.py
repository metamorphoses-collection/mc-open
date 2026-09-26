"""Syllable check on the alexandrines of La Partition du Texte (pages 1-10).

Approach:
  - Extract the alexandrine verses from pages 1-10
  - Count syllables with a simple French metrical counter:
      * tokenize by word; count vowel groups within each word
      * apply elision: word-final mute -e disappears before a vowel
      * apply verse-end rule: final mute -e / -es / -ent does not count
      * treat 'oi', 'ou', 'eu', 'au', 'ai', 'ei', 'ey' as single syllables
        (synérèse); diphthong 'io', 'ia', 'ua', 'ui' kept as one syllable
        unless they fall on stressed positions (we don't model that — we
        will under-count diérèses, so the counter is slightly conservative)
  - Calibrate against known Racine alexandrines (12 expected) before scoring
  - Output: histogram of syllable counts + list of non-12 verses
"""
import re
import sys
from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parent
MD = ROOT / "texts/partition_du_texte.md"
OUT = ROOT / "alexandrins_syllable_check.json"

# =============================================================================
# French syllable counter
# =============================================================================
VOWELS = "aeiouyàâäéèêëîïôöùûüÿAEIOUYÀÂÄÉÈÊËÎÏÔÖÙÛÜŸ"

def normalize(text):
    """Strip diacritics-equivalent variants, lowercase, remove punctuation."""
    text = text.lower()
    # Replace special apostrophes
    text = text.replace("’", "'").replace("‘", "'")
    # Remove punctuation but keep apostrophes and hyphens
    text = re.sub(r"[.,;:!?\"«»\(\)\[\]…—–]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

def apply_elisions(text):
    """Word-final mute -e elides before a word-initial vowel/h."""
    # Replace "e " followed by vowel (or 'h' followed by vowel) with " "
    # Handle apostrophes: l', d', n', s', j', m', t', c', qu', jusqu', presqu', lorsqu', puisqu', quoiqu'
    text = re.sub(r"\b(l|d|n|s|j|m|t|c|qu|jusqu|presqu|lorsqu|puisqu|quoiqu)'", r"\1' ", text)
    # Word-final 'e' before vowel: 'le ami' → 'l ami' (count one syllable less)
    # We approximate: replace 'e[s]? ' followed by vowel with ' '
    text = re.sub(r"e\s+([" + VOWELS + r"])", r" \1", text)
    text = re.sub(r"es\s+([" + VOWELS + r"])", r" \1", text)
    # 'ent ' followed by vowel: counts (it's not always silent) — leave alone
    return text

def drop_verse_final_mute(text):
    """At end of verse, final mute -e (or -es, -ent for 3p plural) doesn't count."""
    text = re.sub(r"e\s*$", "", text)
    text = re.sub(r"es\s*$", "", text)
    # 'ent' at end of verse only counts as 1 if preceded by a consonant + e
    # We approximate: drop final -ent
    text = re.sub(r"ent\s*$", "", text)
    return text

def count_vowel_groups(text):
    """Count contiguous vowel groups in normalized text."""
    return len(re.findall(r"[" + VOWELS + r"]+", text))

def syllables(verse):
    s = normalize(verse)
    s = apply_elisions(s)
    s = drop_verse_final_mute(s)
    return count_vowel_groups(s)

# =============================================================================
# Calibration on known Racine alexandrines
# =============================================================================
RACINE = [
    # Phèdre, Acte I, scène 3
    ("Je le vis, je rougis, je pâlis à sa vue", 12),
    ("Un trouble s'éleva dans mon âme éperdue", 12),
    # Britannicus
    ("Captive, toujours triste, importune à moi-même", 12),
    # Andromaque
    ("Je t'aimais inconstant, qu'aurais-je fait fidèle?", 12),
    # Bérénice
    ("Dans l'Orient désert quel devint mon ennui!", 12),
]
print("=== Calibration on Racine (expected: 12) ===")
for v, exp in RACINE:
    got = syllables(v)
    flag = "OK " if got == exp else f"OFF({got-exp:+d})"
    print(f"  {flag}  count={got}  {v}")

# =============================================================================
# Extract alexandrine verses from pages 1-10
# =============================================================================
text = MD.read_text()
lines = text.splitlines()

verses = []  # list of (page, line)
current_page = None
in_alexandrine_zone = False
in_page_body = False
for i, raw in enumerate(lines):
    line = raw.strip()
    # Detect entry to alexandrine section
    if line.startswith("## I. LES ALEXANDRINS"):
        in_alexandrine_zone = True
        continue
    if line.startswith("## II."):
        in_alexandrine_zone = False
        break
    if not in_alexandrine_zone: continue
    # Detect page header
    m = re.match(r"^####\s+PAGE\s+(\d+)", line)
    if m:
        current_page = int(m.group(1))
        in_page_body = False
        continue
    # Skip form line and italic notes
    if line.startswith("*Form:") or line.startswith("---"):
        continue
    # Verses are non-empty lines that aren't headers/comments
    if not line: continue
    if line.startswith("#"): continue
    if line.startswith(">"): continue
    if line.startswith("*"): continue
    if line.startswith("|"): continue
    # This should be a verse
    verses.append((current_page, line))

print(f"\n=== Extracted {len(verses)} alexandrine verses from pages 1-10 ===")
print("First few:")
for p, v in verses[:6]:
    print(f"  P{p}:  {v}")

# =============================================================================
# Count syllables on every verse
# =============================================================================
results = []
for page, verse in verses:
    n = syllables(verse)
    results.append(dict(page=page, verse=verse, syllables=n, deviation=n-12))

dist = Counter(r["syllables"] for r in results)
print(f"\n=== Syllable distribution across {len(results)} verses ===")
for s in sorted(dist):
    bar = "#" * dist[s]
    flag = "  ← target" if s == 12 else ""
    print(f"  {s:3d} syllables : {dist[s]:3d}  {bar}{flag}")

n_exact = dist[12]
n_off1 = dist[11] + dist[13]
n_off2plus = sum(c for k, c in dist.items() if abs(k - 12) >= 2)
total = sum(dist.values())
print(f"\n  Exact 12 syllables:  {n_exact}/{total}  ({100*n_exact/total:.1f}%)")
print(f"  Off by ±1:           {n_off1}/{total}  ({100*n_off1/total:.1f}%)")
print(f"  Off by ±2 or more:   {n_off2plus}/{total}  ({100*n_off2plus/total:.1f}%)")

# =============================================================================
# Per-page breakdown
# =============================================================================
print(f"\n=== Per-page breakdown ===")
for page in sorted(set(r["page"] for r in results if r["page"])):
    page_verses = [r for r in results if r["page"] == page]
    n_pg = len(page_verses)
    n12 = sum(1 for r in page_verses if r["syllables"] == 12)
    avg = sum(r["syllables"] for r in page_verses) / n_pg
    print(f"  Page {page:2d}: {n12:2d}/{n_pg:2d} at 12  (avg {avg:.2f})")

# =============================================================================
# Deviant verses
# =============================================================================
print(f"\n=== Deviant verses ({total - n_exact} total) ===")
for r in results:
    if r["syllables"] != 12:
        sign = "+" if r["deviation"] > 0 else "−"
        print(f"  P{r['page']:2d}  [{r['syllables']:2d}={sign}{abs(r['deviation'])}]  {r['verse']}")

# =============================================================================
# Save JSON
# =============================================================================
summary = dict(
    total_verses=total,
    distribution=dict(dist),
    exact_12=n_exact,
    off_by_1=n_off1,
    off_by_2_or_more=n_off2plus,
    pct_exact=100*n_exact/total if total else 0,
    per_page=[
        dict(
            page=page,
            n_verses=len([r for r in results if r["page"] == page]),
            n_exact=sum(1 for r in results if r["page"] == page and r["syllables"] == 12),
            mean_syllables=sum(r["syllables"] for r in results if r["page"] == page) / len([r for r in results if r["page"] == page])
        )
        for page in sorted(set(r["page"] for r in results if r["page"]))
    ],
    verses=results,
)
json.dump(summary, open(OUT, "w"), indent=2, ensure_ascii=False)
print(f"\n  -> {OUT}")
