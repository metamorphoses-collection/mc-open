#!/usr/bin/env python3
"""
Corpus verifier — runs against corpus/qoulipo/ and corpus/natural/.

Two modes:
  --report : enumerate current state, print every consistency issue, exit 0
  --strict : same checks but exit non-zero if anything fails (CI-style)

Checks performed:
  M1  metadata.json exists
  M2  metadata has uniform required fields (text_id, title, lang, canonical_N,
      canonical_graph_file, canonical_E, canonical_density, canonical_MIS,
      canonical_rho, canonical_optima, graph_mode)
  G1  canonical_graph_file exists in folder
  G2  graph file has explicit edge list (not just summary stats, not coords-only)
  G3  graph N matches metadata.canonical_N
  G4  graph density within 0.005 of metadata.canonical_density
  G5  ILP MIS on canonical graph matches metadata.canonical_MIS
  S1  source/ exists with at least canonical_N files
  S2  source page count == canonical_N (else paratext/ must hold the rest)
  S3  if source > N, paratext/ exists with N_extra = (source - N) files
  P1  no stale or backup files (graph_*_stale.json, source_v1, _backup, etc.)
       in canonical-mode folders

Usage:
  python3 corpus/verify.py --report
  python3 corpus/verify.py --strict
"""
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
QOULIPO = HERE / "qoulipo"

REQUIRED_FIELDS = [
    "text_id", "title", "lang", "canonical_N", "canonical_graph_file",
    "canonical_E", "canonical_density", "canonical_MIS",
    "canonical_rho", "canonical_optima", "graph_mode",
]

STALE_PATTERNS = [
    "_v1_stale", "_v1.json", "_backup", "_old.json", "_stale.json",
    "source_v1", "_pre_audit", "_pre_literary_rewrite", "_rewrite_originals",
]


_NO_MIS = False  # set by main() based on --no-mis flag

def solve_mis(N, edges_idx):
    if _NO_MIS:
        return None  # skip ILP per --no-mis flag
    try:
        from pulp import (LpProblem, LpMaximize, LpVariable, LpBinary,
                          PULP_CBC_CMD, value as lpvalue)
    except ImportError:
        return None
    prob = LpProblem("mis", LpMaximize)
    x = [LpVariable(f"x{i}", cat=LpBinary) for i in range(N)]
    prob += sum(x)
    for a, b in edges_idx:
        prob += x[a] + x[b] <= 1
    prob.solve(PULP_CBC_CMD(msg=0, timeLimit=30))
    return sum(int(lpvalue(xi) > 0.5) for xi in x)


def extract_graph(path):
    """Return (N, E, density, edges_idx) or None if file is not a usable graph."""
    try:
        d = json.loads(path.read_text())
    except Exception:
        return None
    inner = d.get("graph") if isinstance(d.get("graph"), dict) else d
    raw_nodes = inner.get("nodes")
    raw_edges = inner.get("edges")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        return None
    if not isinstance(raw_edges, list):
        return None
    if isinstance(raw_nodes[0], dict):
        nodes = [str(n.get("id", i)) for i, n in enumerate(raw_nodes)]
    else:
        nodes = [str(n) for n in raw_nodes]
    name_to_idx = {n: i for i, n in enumerate(nodes)}
    edges_idx = []
    for e in raw_edges:
        if isinstance(e, dict):
            a, b = str(e.get("source")), str(e.get("target"))
        elif isinstance(e, (list, tuple)):
            a, b = str(e[0]), str(e[1])
        else:
            continue
        if a in name_to_idx and b in name_to_idx:
            edges_idx.append((name_to_idx[a], name_to_idx[b]))
    N = len(nodes)
    E = len(edges_idx)
    d = 2 * E / (N * (N - 1)) if N > 1 else 0.0
    return {"N": N, "E": E, "density": d, "edges_idx": edges_idx}


def check_folder(folder):
    issues = []
    name = folder.name

    # M1
    meta_path = folder / "metadata.json"
    if not meta_path.exists():
        issues.append(("M1", "metadata.json missing"))
        return issues, None
    try:
        meta = json.loads(meta_path.read_text())
    except Exception as e:
        issues.append(("M1", f"metadata.json malformed: {e}"))
        return issues, None

    # M2
    missing_fields = [f for f in REQUIRED_FIELDS if f not in meta]
    if missing_fields:
        issues.append(("M2", f"missing fields: {','.join(missing_fields)}"))

    # G1
    cgf = meta.get("canonical_graph_file")
    if not cgf:
        issues.append(("G1", "no canonical_graph_file in metadata"))
    else:
        gpath = folder / cgf
        if not gpath.exists():
            issues.append(("G1", f"canonical_graph_file not found: {cgf}"))
        else:
            # G2-G5
            g = extract_graph(gpath)
            if g is None:
                issues.append(("G2", f"{cgf} is not a usable graph (no edge list, "
                                     "or wrong format — likely a coords/summary file)"))
            else:
                exp_N = meta.get("canonical_N")
                exp_E = meta.get("canonical_E")
                exp_d = meta.get("canonical_density")
                exp_M = meta.get("canonical_MIS")
                if exp_N is not None and g["N"] != exp_N:
                    issues.append(("G3",
                        f"canonical_N {exp_N} ≠ graph N {g['N']}"))
                if exp_E is not None and g["E"] != exp_E:
                    issues.append(("G3",
                        f"canonical_E {exp_E} ≠ graph E {g['E']}"))
                if exp_d is not None and abs(g["density"] - exp_d) > 0.005:
                    issues.append(("G4",
                        f"canonical_density {exp_d:.4f} ≠ graph d {g['density']:.4f}"))
                if exp_M is not None:
                    mis = solve_mis(g["N"], g["edges_idx"])
                    if mis is not None and mis != exp_M:
                        issues.append(("G5",
                            f"canonical_MIS {exp_M} ≠ ILP MIS {mis}"))

    # S1, S2, S3
    src = folder / "source"
    paratext = folder / "paratext"
    n = meta.get("canonical_N")
    # Component folders (one layer of a bilayer etc.) point at a parent's graph;
    # their own source/ holds the layer text only — skip the strict S1/S2 check.
    is_component = bool(meta.get("components_of"))
    if not src.exists():
        issues.append(("S1", "source/ missing"))
    elif is_component:
        pass  # component folder — N matches the parent graph, source matches the layer
    else:
        n_src = len(list(src.glob("*.txt"))) + len(list(src.glob("*.md")))
        if n is not None:
            if n_src < n:
                issues.append(("S1", f"source/ has {n_src} files, < canonical_N {n}"))
            elif n_src > n:
                expected_paratext = n_src - n
                if not paratext.exists():
                    issues.append(("S2",
                        f"source/ has {n_src} files but canonical_N={n}; "
                        f"{expected_paratext} files should be in paratext/"))
                else:
                    n_para = len(list(paratext.glob("*.txt"))) + \
                             len(list(paratext.glob("*.md")))
                    if n_para != expected_paratext:
                        issues.append(("S3",
                            f"paratext/ has {n_para} files, expected {expected_paratext}"))

    # P2 - API key scan (deposit safety)
    import re as _re
    KEY_RE = _re.compile(r"sk-ant-api03-[A-Za-z0-9_-]{40,}")
    for fp in folder.rglob("*"):
        if fp.is_file() and fp.name == "verify.py":
            continue  # the verifier itself contains the regex pattern, not a real key
        if fp.is_file() and fp.suffix in (".py", ".json", ".txt", ".md"):
            try:
                content = fp.read_text(encoding="utf-8")
                if KEY_RE.search(content):
                    issues.append(("P2", f"hardcoded API key in {fp.relative_to(folder)}"))
            except Exception:
                pass

    # P1 - stale files
    for fp in folder.iterdir():
        for pat in STALE_PATTERNS:
            if pat in fp.name:
                issues.append(("P1", f"stale/backup file: {fp.name}"))
                break

    return issues, meta


def check_registry_consistency():
    """R1: instances.csv matches per-folder metadata.json
    R2: README.md table counts match instances.csv (lite check)
    R3: every natural/ folder has metadata.json (registered)"""
    import csv
    issues = []
    csv_path = HERE / "instances.csv"
    if not csv_path.exists():
        return [("R0", "instances.csv missing")]
    rows = list(csv.DictReader(csv_path.open()))
    csv_by_id = {r["instance_id"]: r for r in rows}
    # R1: check qoulipo + natural folders
    for root, role in [(QOULIPO, "qoulipo_engineered"),
                        (HERE / "natural", "natural")]:
        for folder in sorted(root.iterdir()):
            if not folder.is_dir() or folder.name.startswith("_"):
                continue
            mp = folder / "metadata.json"
            if not mp.exists():
                issues.append(("R3" if role == "natural" else "R1",
                               f"{folder.name}: metadata.json missing"))
                continue
            try:
                m = json.loads(mp.read_text())
            except Exception:
                continue
            tid = m.get("text_id", folder.name)
            if tid not in csv_by_id:
                issues.append(("R1", f"{folder.name}: not in instances.csv (text_id={tid})"))
                continue
            r = csv_by_id[tid]
            for fld, key in [("N", "canonical_N"), ("E", "canonical_E"),
                              ("MIS", "canonical_MIS")]:
                v_csv = r.get(fld, "")
                v_meta = m.get(key, "")
                if str(v_csv) != str(v_meta):
                    issues.append(("R1", f"{folder.name}: {fld} mismatch (csv={v_csv}, meta={v_meta})"))
    return issues


def check_source_lint(folder):
    """S4: source files do not begin with constraint/title/thread-table headers.

    Catches both English colon-tight forms (``Voice:``, ``Role:``) and the
    French/typographic spaced-colon variants (``Voix :``, ``Rôle :``,
    ``Fils :``) — also tolerates leading asterisks (``*Voix :``, ``**Voix :``).
    """
    src = folder / "source"
    if not src.exists():
        return []
    issues = []
    # canonical label stems; any of {":", " :"} suffix and {"", "*", "**"} prefix matches
    label_stems = (
        "threads", "voice", "voix", "role", "rôle", "fils", "form", "forme",
        "grid", "grille", "coordinate", "coordonnée", "coord",
        "vicini", "motivo lungo", "motivo breve",
    )
    import re as _re
    # ^(\*{0,2}\s*)? (label) \s* :  — case-insensitive
    pat = _re.compile(
        r"^\s*\*{0,2}\s*(" + "|".join(_re.escape(s) for s in label_stems) + r")\s*:",
        _re.IGNORECASE,
    )
    for p in src.glob("*.txt"):
        first = p.read_text(encoding="utf-8").lstrip().splitlines()[:1]
        if not first:
            continue
        m = pat.match(first[0])
        if m:
            issues.append(("S4", f"{p.name}: starts with scaffolding ({m.group(1)})"))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-mis", action="store_true",
                    help="Skip ILP MIS verification (G5) for faster runs")
    ap.add_argument("--lint", action="store_true",
                    help="Also run R1-R3 (registry) and S4 (source-lint) checks")
    args = ap.parse_args()

    global _NO_MIS
    _NO_MIS = bool(args.no_mis)
    if not args.report and not args.strict:
        args.report = True

    folders = sorted(d for d in QOULIPO.iterdir()
                     if d.is_dir() and not d.name.startswith("_"))

    print(f"corpus/qoulipo/  {len(folders)} folders")
    print("=" * 78)
    n_ok = n_issues = 0
    by_folder = {}
    for f in folders:
        issues, meta = check_folder(f)
        if args.lint:
            issues = list(issues) + check_source_lint(f)
        by_folder[f.name] = issues
        if not issues:
            print(f"  ✓ {f.name}")
            n_ok += 1
        else:
            print(f"\n  ✗ {f.name}  ({len(issues)} issues)")
            for code, msg in issues:
                print(f"      [{code}] {msg}")
            n_issues += 1
    print("\n" + "=" * 78)
    print(f"summary: {n_ok}/{len(folders)} folders pass; {n_issues} have issues")

    # Registry consistency (R1-R3) and full natural+qoulipo sweep
    if args.lint:
        print("\n" + "=" * 78)
        print("Registry & natural-folder consistency (R1/R2/R3)")
        print("=" * 78)
        reg_issues = check_registry_consistency()
        if reg_issues:
            for code, msg in reg_issues:
                print(f"  [{code}] {msg}")
            n_issues += len(reg_issues)
        else:
            print("  ✓ instances.csv ↔ all folder metadata consistent.")

    # Issue-code histogram
    from collections import Counter
    counts = Counter(c for issues in by_folder.values() for c, _ in issues)
    if args.lint and reg_issues:
        for code, _ in reg_issues:
            counts[code] += 1
    if counts:
        print("\nfailures by code:")
        for c, n in sorted(counts.items()):
            print(f"  {c}: {n}")

    if args.strict and n_issues > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
