"""For each corpus folder: extract MIS solution, build MIS sequence, generate summary,
compute embedding distance via e5-large-instruct (same pipeline as paper natural-text path)."""
import os, json, sys, time, csv, re
from pathlib import Path
import numpy as np

os.environ.setdefault("ANTHROPIC_API_KEY", "<REDACTED:set ANTHROPIC_API_KEY env var>")
import anthropic
client = anthropic.Anthropic()
ROOT = Path(__file__).resolve().parent.parent

def solve_mis_with_solution(N, edges_idx):
    from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, PULP_CBC_CMD, value as lpv
    prob = LpProblem("mis", LpMaximize)
    x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(N)]
    prob += sum(x)
    for a,b in edges_idx:
        prob += x[a] + x[b] <= 1
    prob.solve(PULP_CBC_CMD(msg=0))
    return [i for i in range(N) if lpv(x[i]) > 0.5]

def load_graph(path):
    d = json.loads(Path(path).read_text())
    inner = d.get("graph") if isinstance(d.get("graph"), dict) else d
    raw_nodes, raw_edges = inner.get("nodes"), inner.get("edges")
    if isinstance(raw_nodes[0], dict):
        nodes = [str(n.get("id", i)) for i,n in enumerate(raw_nodes)]
    else:
        nodes = [str(n) for n in raw_nodes]
    name_to_idx = {n:i for i,n in enumerate(nodes)}
    edges = []
    for e in raw_edges:
        a, b = (str(e.get("source")), str(e.get("target"))) if isinstance(e, dict) else (str(e[0]), str(e[1]))
        if a in name_to_idx and b in name_to_idx:
            edges.append((name_to_idx[a], name_to_idx[b]))
    return nodes, edges

def map_nodes_to_files(nodes, src_dir):
    files = sorted(src_dir.glob("*.txt"))
    if not files: return {}
    file_stems = {f.stem: f for f in files}
    if all(n in file_stems for n in nodes):
        return {n: file_stems[n] for n in nodes}
    if all(n.isdigit() for n in nodes):
        try: return {n: files[int(n)] for n in nodes if int(n) < len(files)}
        except: pass
    mapping = {}
    for n in nodes:
        m = re.search(r'(\d+)', n)
        if m:
            num = int(m.group(1))
            for digits in (3, 2, 1):
                cand = f"page_{num:0{digits}d}"
                if cand in file_stems: mapping[n] = file_stems[cand]; break
            if n not in mapping and num < len(files):
                mapping[n] = files[num]
            elif n not in mapping and num-1 < len(files) and num-1 >= 0:
                mapping[n] = files[num-1]
    if len(mapping) >= 0.8 * len(nodes): return mapping
    if len(nodes) <= len(files):
        return {n: files[i] for i, n in enumerate(nodes)}
    return mapping

def get_summary(client, text, lang, target_words):
    sys_p = f"""Produce a concise summary of the following text in {lang}, of approximately {target_words} words. Capture themes, key narrative beats, characteristic voice. Coherent passage, not bullets. Return ONLY the summary."""
    try:
        r = client.messages.create(model="claude-sonnet-4-5", max_tokens=4096, system=sys_p,
                                    messages=[{"role":"user","content":text}])
        if r.content: return r.content[0].text.strip()
    except Exception as e:
        print(f"    summary err: {e}")
    return None

def main():
    from sentence_transformers import SentenceTransformer
    print("Loading e5-large-instruct...")
    model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")
    PREFIX = "Instruct: Retrieve semantically similar passages.\nQuery: "
    rows = []
    for kind in ("qoulipo", "natural"):
        for folder in sorted((ROOT / "corpus" / kind).iterdir()):
            if not folder.is_dir() or folder.name.startswith("_"): continue
            mp = folder / "metadata.json"
            if not mp.exists(): continue
            m = json.loads(mp.read_text())
            graph_file = m.get("canonical_graph_file")
            if not graph_file: continue
            gpath = (folder / graph_file)
            if not gpath.exists():
                gpath = gpath.resolve()
                if not gpath.exists(): continue
            print(f"\n[{folder.name}]", flush=True)
            try:
                nodes, edges = load_graph(gpath)
            except Exception as e:
                print(f"  graph err: {e}"); continue
            N = len(nodes)
            mis_idx = solve_mis_with_solution(N, edges)
            mis_pages = [nodes[i] for i in mis_idx]
            src = folder / "source"
            if not src.exists():
                if "components_of" in m: print("  component folder; skip"); continue
                continue
            mapping = map_nodes_to_files(nodes, src)
            if len(mapping) < 0.5 * N:
                print(f"  ⚠ poor mapping ({len(mapping)}/{N}); skip"); continue
            print(f"  mapped {len(mapping)}/{N}; MIS size {len(mis_pages)}")
            mis_texts = [mapping[n].read_text(encoding="utf-8") for n in mis_pages if n in mapping]
            full_files = sorted(src.glob("*.txt"))
            full_texts = [f.read_text(encoding="utf-8") for f in full_files]
            mis_seq = "\n\n---\n\n".join(mis_texts)
            full_text = "\n\n---\n\n".join(full_texts)
            mis_w, full_w = len(mis_seq.split()), len(full_text.split())
            print(f"  MIS={mis_w}w full={full_w}w")
            if mis_w == 0:
                print("  empty; skip"); continue
            lang_map = {"EN":"English","FR":"French","IT":"Italian","LA":"Latin","HE+IT":"English"}
            lang = lang_map.get(m.get("lang","EN"),"English")
            target = max(200, mis_w)
            full_sum = " ".join(full_text.split()[:30000]) if full_w > 30000 else full_text
            summary = get_summary(client, full_sum, lang, target) or "[summary failed]"
            try:
                embs = model.encode([PREFIX+mis_seq, PREFIX+summary, PREFIX+full_sum],
                                     normalize_embeddings=True, show_progress_bar=False, batch_size=2)
                cms = float(np.dot(embs[0], embs[1]))
                cmf = float(np.dot(embs[0], embs[2]))
                csf = float(np.dot(embs[1], embs[2]))
                print(f"  cos(MIS,sum)={cms:.3f} cos(MIS,full)={cmf:.3f} cos(sum,full)={csf:.3f}")
            except Exception as e:
                cms = cmf = csf = None
                print(f"  embed err: {e}")
            interp = ("MIS and summary highly aligned" if cms and cms > 0.92 else
                      "MIS diverges from summary" if cms and cms < 0.78 else "intermediate")
            analysis = {"folder": folder.name, "corpus_kind": kind, "title": m.get("title", folder.name),
                "lang": m.get("lang",""), "N": N, "MIS_size": len(mis_pages),
                "MIS_pages": mis_pages, "MIS_words": mis_w, "full_words": full_w,
                "summary_words": len(summary.split()),
                "cos_mis_summary": cms, "cos_mis_full": cmf, "cos_summary_full": csf,
                "interpretation": interp,
                "mis_sequence_preview": mis_seq[:500] + ("..." if len(mis_seq)>500 else ""),
                "summary": summary}
            (folder / "mis_analysis.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False)+"\n")
            rows.append({"folder": folder.name, "corpus_kind": kind, "title": m.get("title",""),
                "lang": m.get("lang",""), "N": N, "MIS_size": len(mis_pages),
                "MIS_words": mis_w, "full_words": full_w, "summary_words": len(summary.split()),
                "cos_mis_summary": cms, "cos_mis_full": cmf, "cos_summary_full": csf,
                "MIS_pages": ",".join(mis_pages)})
    out = ROOT / "corpus" / "mis_analysis_all.csv"
    if rows:
        with out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows: w.writerow(r)
        print(f"\n✓ {out} ({len(rows)} rows)")

if __name__ == "__main__":
    main()
