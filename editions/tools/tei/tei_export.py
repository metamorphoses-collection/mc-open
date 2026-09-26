"""TEI P5 export for the MC Editions (Bavarius, Capilupi, Ross), generated from each edition's live edition.json.

One generator for all editions, so every export follows the same model:
  teiHeader   bibliographic description of the source and of our copy, editorial and encoding conventions,
              responsibility (including machine-assisted steps), licence.
  facsimile   one <surface> per page (IIIF canvas + image), one <zone> per verse from the line boxes.
  text        <group> of two <text>s: the Latin (diplomatic) and the English translation, line for line;
              every English line points to its Latin verse with @corresp.
Latin verses are <l> with @n, @facs (zone), @met (scansion pattern where scanned); the printed Virgil source tags are
<note type="source"> in the margin, each resolved locus a <ref> to its CTS URN. Printed side-notes are
<note type="printed" place="margin">; annotator marks <note type="annotation" resp="#annotator">; corrections made
in the 2026 text passes <note type="editorial" resp="#editor">. Pages are named by the collation (<pb n>).

Usage: python3 tei_export.py [bavarius capilupi ross] -> out/<edition>.tei.xml
"""
import os
import json, re, sys, datetime
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

H = Path(__file__).parent
SITE = Path(os.environ.get("MC_EDITIONS", Path(__file__).resolve().parents[2]))   # the editions/ folder
TODAY = datetime.date.today().isoformat()

META = {
    "bavarius": dict(
        author="Aegidius Bavarius", title_la="Musa Catholica", place="Antverpiae", date="1622",
        mcid="MC-C-113", lang_note="Latin verse (Virgilian cento) with Latin prose and side-notes",
        subject="A Catholic catechism in dialogue composed as a Virgilian cento."),
    "capilupi": dict(
        author="Lelio Capilupi", title_la="Centones ex Virgilio", place="Romae", printer="Valerio Dorico",
        date="c. 1555", when="1555", mcid="MC-C-145", collation="[iv] 64 [4]; A² B–I⁴ K²",
        editor_hist="Antonio Possevino",
        provenance="E. J. Kenney (booklabel; pencil note 'Not in Adams').",
        subject="Twelve Virgilian centos, with prose prefaces, printed side-notes and the exchange with Benedetto Egio."),
    "ross": dict(
        author="Alexander Ross", title_la="Virgilii Evangelisantis Christiados libri XIII", place="Roterodami",
        printer="Arnold Leers", date="1653", mcid="MC-C-133",
        collation="Preliminaries [1]–[28] (A1v and A2v blank), pp. 1–439.",
        subject="The gospel narrative in thirteen books composed of lines and half-lines of Virgil, with Ross's printed notes."),
}

def x(s):
    return escape(str(s if s is not None else ""))

def attr(s):
    return quoteattr(str(s))

def slug(s):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", str(s)).strip("-") or "x"

def data(ed, name):
    """edition file: repository layout (editions/<ed>/<name>) or site layout (<ed>/data/<name>)"""
    for q in (SITE / ed / name, SITE / ed / "data" / name):
        if q.exists():
            return q
    return SITE / ed / name

def canvases(ed):
    """vflat -> (canvas id, image url) from the IIIF manifest."""
    out = {}
    try:
        M = json.load(open(data(ed, "manifest.json")))
    except FileNotFoundError:
        return out
    for c in M.get("items", []):
        m = re.search(r"/canvas/(\d+)$", c["id"])
        if not m:
            continue
        try:
            body = c["items"][0]["items"][0]["body"]
            out[int(m.group(1))] = (c["id"], body.get("id"))
        except (KeyError, IndexError):
            out[int(m.group(1))] = (c["id"], None)
    return out

def header(ed, E, m):
    S = E.get("summary", {})
    title = S.get("title") or f"{m['author']}, {m['title_la']}"
    imprint = f"<pubPlace>{x(m['place'])}</pubPlace>"
    if m.get("printer"):
        imprint += f"<publisher>{x(m['printer'])}</publisher>"
    imprint += f"<date{(' when=' + attr(m['when'])) if m.get('when') else ''}>{x(m['date'])}</date>"
    coll = m.get("collation") or S.get("collation") or ""
    ann = S.get("annotator")
    ann_desc = (ann.get("characterization") if isinstance(ann, dict) else "") or ""
    return f"""<teiHeader>
  <fileDesc>
   <titleStmt>
    <title type="main">{x(m['title_la'])}</title>
    <title type="sub">A digital edition with English translation (MC Editions)</title>
    <author>{x(m['author'])}</author>
    <editor xml:id="editor">MC Editions, Metamorphoses of Civilization</editor>
    <respStmt><resp>Transcription, apparatus, translation and encoding</resp><name>Metamorphoses of Civilization (MC Editions)</name></respStmt>
    <respStmt xml:id="machine"><resp>Machine-assisted steps: independent vision readings of the page images, handwritten-text recognition, draft translations and blind refereeing by large language models; every correction verified against the page images and recorded</resp><name>MC Editions pipeline</name></respStmt>
   </titleStmt>
   <editionStmt><edition>Digital edition, TEI export generated {TODAY} from the published edition data</edition></editionStmt>
   <publicationStmt>
    <publisher>Metamorphoses of Civilization</publisher>
    <pubPlace>https://metamorphoses-collection.org/editions/{ed}/</pubPlace>
    <date when="{TODAY}">{TODAY}</date>
    <availability>
     <licence target="https://creativecommons.org/licenses/by/4.0/">Text, apparatus and translation: CC BY 4.0.</licence>
     <licence target="https://creativecommons.org/publicdomain/zero/1.0/">Page images of the collection copy: CC0.</licence>
    </availability>
   </publicationStmt>
   <sourceDesc>
    <biblStruct>
     <monogr>
      <author>{x(m['author'])}</author>
      <title>{x(m['title_la'])}</title>
      {('<editor>' + x(m['editor_hist']) + '</editor>') if m.get('editor_hist') else ''}
      <imprint>{imprint}</imprint>
      {('<extent>' + x(coll) + '</extent>') if coll else ''}
     </monogr>
    </biblStruct>
    <msDesc>
     <msIdentifier><institution>Metamorphoses of Civilization collection</institution><idno type="MC-ID">{x(m['mcid'])}</idno></msIdentifier>
     <msContents><summary>{x(m['subject'])}</summary></msContents>
     {('<history><provenance>' + x(m['provenance']) + '</provenance></history>') if m.get('provenance') else ''}
    </msDesc>
   </sourceDesc>
  </fileDesc>
  <encodingDesc>
   <editorialDecl>
    <p>Diplomatic transcription of the collection copy: spelling, u/v and i/j, ligatures (æ, œ), abbreviations (q;, tildes) and accents are kept as printed; long s is transcribed s. Printer's misprints are kept as printed and noted. Pages are named by the collation of the copy. The English translation faces the Latin line by line; English may carry a word across a line break where the sense of the pair is kept.</p>
    <p>Text establishment: two independent machine readings of every line from the page images, compared letter by letter; every divergence adjudicated against the image; corrections logged in editorial notes (type="editorial").</p>
   </editorialDecl>
   <refsDecl><p>Verses are identified by page (collation name) and line number; each Latin verse has an xml:id, which the English line cites in @corresp.</p></refsDecl>
   <classDecl><taxonomy xml:id="notes"><category xml:id="source"><catDesc>Printed marginal source tag naming the Virgilian model, resolved to a CTS URN.</catDesc></category></taxonomy></classDecl>
  </encodingDesc>
  <profileDesc>
   <langUsage><language ident="la">Latin</language><language ident="en">English</language></langUsage>
   {('<handNotes><handNote xml:id="annotator">' + x(ann_desc) + '</handNote></handNotes>') if ann_desc else ''}
  </profileDesc>
 </teiHeader>"""

def lid(ed, p, l, k):
    n = l.get("n")
    return f"{ed}-{p['vflat']}-{n if n is not None else 'u' + str(k)}"

def facsimile(ed, E):
    C = canvases(ed); out = ["<facsimile>"]
    for p in E["pages"]:
        vf = p["vflat"]; cid, img = C.get(vf, (None, None))
        W = p.get("tw") or p.get("w"); Hh = p.get("th") or p.get("h")
        dims = f' ulx="0" uly="0" lrx="{W}" lry="{Hh}"' if W and Hh else ""
        out.append(f' <surface xml:id="s-{ed}-{vf}" n={attr(p.get("physical",""))}{dims}' + (f' sameAs={attr(cid)}' if cid else "") + ">")
        if img:
            out.append(f"  <graphic url={attr(img)}/>")
        if W and Hh:
            for k, l in enumerate(p.get("lines", [])):
                b = l.get("bbox")
                if b:
                    out.append(f'  <zone xml:id="z-{lid(ed,p,l,k)}" ulx="{round(b[0]*W)}" uly="{round(b[1]*Hh)}" lrx="{round(b[2]*W)}" lry="{round(b[3]*Hh)}"/>')
        out.append(" </surface>")
    out.append("</facsimile>")
    return "\n".join(out)

def div_key(ed, p):
    if ed == "ross":
        return ("book", p.get("liber")) if p.get("liber") else ("section", p.get("section") or p.get("kind"))
    return ("cento", p.get("cento")) if p.get("cento") else ("section", p.get("section") or p.get("kind") or "front")

def urn(loc):
    return loc.get("cts_urn") or loc.get("urn")

def source_notes(l):
    out = []
    for side, key in (("L", "tag_l"), ("R", "tag_r")):
        refs = [lo for lo in (l.get("loci") or []) if lo.get("side", "L") == side and urn(lo)]
        printed = l.get(key)
        if not printed and not refs:
            continue
        place = "margin-left" if side == "L" else "margin-right"
        inner = x(printed) if printed else ""
        inner += "".join(f'<ref target={attr(urn(r))}/>' for r in refs)
        resp = "" if printed else ' resp="#editor" subtype="identified"'
        out.append(f'<note type="source" place="{place}"{resp}>{inner}</note>')
    return "".join(out)

def latin(ed, E):
    out = ['<text xml:lang="la" xml:id="la"><body>']; cur = None; fresh = False
    for p in E["pages"]:
        k = div_key(ed, p)
        if k != cur:
            if cur is not None:
                out.append("</div>")
            out.append(f'<div type="{k[0]}" n={attr(k[1] or "")}>'); cur = k; fresh = True
        pa = f' n={attr(p.get("physical",""))} facs="#s-{ed}-{p["vflat"]}"'
        out.append(f"<pb{pa}/>")
        if p.get("printed_as"):
            out.append(f'<note type="editorial" resp="#editor">Page numeral printed as {x(p["printed_as"])}.</note>')
        if p.get("printed_page_error") and p.get("sequence"):
            out.append(f'<note type="editorial" resp="#editor">Misprinted numeral: the printer set {x(p.get("printed"))}; this is page {x(p["sequence"])}.</note>')
        if p.get("heading"):   # TEI allows <head> only at the start of a division
            out.append(f"<head>{x(p['heading'])}</head>" if fresh else f'<ab type="heading">{x(p["heading"])}</ab>')
        fresh = False
        prose = p.get("prose") or []
        paras = p.get("paragraphs") if ed == "capilupi" else []
        for q in prose:
            la = q.get("la") if isinstance(q, dict) else q
            if la:
                out.append(f"<p>{x(la)}</p>")
        if ed == "capilupi" and p.get("paragraphs_en"):
            for q in paras or []:
                out.append(f"<p>{x(q)}</p>")
        lines = p.get("lines", [])
        if lines:
            out.append("<lg>")
            for kk, l in enumerate(lines):
                i = lid(ed, p, l, kk)
                a = f' xml:id="{i}"' + (f' n="{l["n"]}"' if l.get("n") is not None else "")
                if l.get("bbox"):
                    a += f' facs="#z-{i}"'
                sc = l.get("scansion") or {}
                if isinstance(sc, dict) and sc.get("pattern"):
                    a += f' met={attr(sc["pattern"])}'
                notes = source_notes(l)
                ed_notes = []
                for key in ("latin_pass", "reading_note", "note"):
                    v = l.get(key)
                    if isinstance(v, str) and v.strip():
                        ed_notes.append(f'<note type="editorial" resp="#editor">{x(v)}</note>')
                for mk in l.get("marks") or []:
                    ed_notes.append(f'<note type="annotation" resp="#annotator">{x(mk.get("text",""))}' + (f' ({x(mk.get("medium"))})' if mk.get("medium") else "") + "</note>")
                out.append(f"<l{a}>{x((l.get('orig') or '').strip())}{notes}{''.join(ed_notes)}</l>")
            out.append("</lg>")
        for j, mg in enumerate(p.get("marginalia") or []):
            tgt = ""
            bl = mg.get("beside_lines") or mg.get("at_lines")
            if bl:
                first = bl[0] if isinstance(bl, list) else bl
                tgt = f' target="#{ed}-{p["vflat"]}-{first}"'
            n = f' n={attr(mg["mark"])}' if mg.get("mark") else ""
            out.append(f'<note type="printed" place="margin"{n}{tgt} xml:id="{ed}-{p["vflat"]}-note{j+1}">{x(mg.get("text",""))}</note>')
        for mk in p.get("page_marks") or []:
            out.append(f'<note type="annotation" resp="#annotator">{x(mk.get("text",""))}</note>')
    if cur is not None:
        out.append("</div>")
    out.append("</body></text>")
    return "\n".join(out)

def english(ed, E):
    out = ['<text xml:lang="en" xml:id="en" type="translation"><body>']; cur = None
    for p in E["pages"]:
        k = div_key(ed, p)
        if k != cur:
            if cur is not None:
                out.append("</div>")
            out.append(f'<div type="{k[0]}" n={attr(k[1] or "")}>'); cur = k
        out.append(f'<pb n={attr(p.get("physical",""))} corresp="#s-{ed}-{p["vflat"]}"/>')
        for q in p.get("prose") or []:
            if isinstance(q, dict) and q.get("en"):
                out.append(f"<p>{x(q['en'])}</p>")
        if ed == "capilupi":
            for q in p.get("paragraphs_en") or []:
                if q:
                    out.append(f"<p>{x(q)}</p>")
        lines = p.get("lines", [])
        if lines:
            out.append("<lg>")
            for kk, l in enumerate(lines):
                i = lid(ed, p, l, kk)
                out.append(f'<l corresp="#{i}"' + (f' n="{l["n"]}"' if l.get("n") is not None else "") + f">{x((l.get('en') or '').strip())}</l>")
            out.append("</lg>")
        for j, mg in enumerate(p.get("marginalia") or []):
            if mg.get("text_en"):
                out.append(f'<note type="printed" place="margin" corresp="#{ed}-{p["vflat"]}-note{j+1}">{x(mg["text_en"])}</note>')
    if cur is not None:
        out.append("</div>")
    out.append("</body></text>")
    return "\n".join(out)

def export(ed):
    E = json.load(open(data(ed, "edition.json"))); m = META[ed]
    doc = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n'
           f'<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="mc-{ed}">\n'
           + header(ed, E, m) + "\n" + facsimile(ed, E) + "\n<text><group>\n" + latin(ed, E) + "\n" + english(ed, E) + "\n</group></text>\n</TEI>\n")
    out = Path(os.environ.get("TEI_OUT", H / "out")); out.mkdir(exist_ok=True)
    f = out / f"{ed}.tei.xml"; f.write_text(doc)
    return f, doc.count("<l "), doc.count("<zone ")

if __name__ == "__main__":
    for ed in (sys.argv[1:] or ["bavarius", "capilupi", "ross"]):
        f, nl, nz = export(ed)
        print(ed, f, "lines(la+en)", nl, "zones", nz, round(f.stat().st_size / 1e6, 1), "MB")
