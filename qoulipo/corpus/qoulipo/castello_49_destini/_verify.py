#!/usr/bin/env python3
"""Verify word counts, required-token inclusion, and adjacency for castello_49_destini pages."""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")

plan = json.load(open(os.path.join(HERE, "_plan.json"), encoding="utf-8"))
tokens = plan["tokens"]  # key "r,c" -> {name,type}
page_tokens = plan["page_tokens"]  # key "p" -> {i,j,token_keys}

# Build a list of all distinct names
all_names = sorted({tokens[k]["name"] for k in tokens}, key=len, reverse=True)

def count_words(text):
    # Skip the roman numeral header line
    lines = text.strip().split("\n")
    body = "\n".join(l for l in lines if not re.match(r"^[IVXLCDM]+\.\s*$", l.strip()))
    words = re.findall(r"\b[\w'’]+\b", body, flags=re.UNICODE)
    return len(words)

def strip_article(name):
    """Strip leading Italian article from token name to get matchable core."""
    parts = name.split(" ", 1)
    articles = {"il","la","lo","gli","le","i","l'","un","una","uno"}
    # Handle l' (elided)
    if name.startswith("l'"):
        return name[2:]
    if parts[0].lower() in articles and len(parts) > 1:
        return parts[1]
    return name

def find_tokens(text, names):
    """Match token by its article-stripped core (case sensitive)."""
    found = set()
    for name in names:
        core = strip_article(name)
        if core in text:
            found.add(name)
    return found

report = {"pages": {}, "violations": []}
total_violations = 0
strict_mode = "--strict" in sys.argv

for p in range(1, 50):
    fn = os.path.join(SRC, f"page_{p:02d}.txt")
    if not os.path.exists(fn):
        report["pages"][p] = {"status": "MISSING"}
        continue
    text = open(fn, encoding="utf-8").read()
    wc = count_words(text)
    req = {tokens[k]["name"] for k in page_tokens[str(p)]["token_keys"]}
    found = find_tokens(text, all_names)
    missing = req - found
    extra = found - req
    status = "OK"
    if wc < 350 or wc > 390: status = "WORDCOUNT"
    if missing: status = "MISSING_TOKENS"
    if extra: status = "EXTRA_TOKENS"
    report["pages"][p] = {
        "wc": wc,
        "status": status,
        "required": sorted(req),
        "found": sorted(found),
        "missing": sorted(missing),
        "extra": sorted(extra),
    }
    if status != "OK":
        print(f"p={p:2d} wc={wc:3d} status={status} missing={sorted(missing)} extra={sorted(extra)}")
        total_violations += 1

# Adjacency check across all pairs of existing pages
def cheb(p,q):
    ip=(p-1)%7; jp=(p-1)//7
    iq=(q-1)%7; jq=(q-1)//7
    return max(abs(ip-iq),abs(jp-jq))

existing = [p for p in range(1,50) if "wc" in report["pages"].get(p,{})]
adj_viol = 0
for i,p in enumerate(existing):
    for q in existing[i+1:]:
        d = cheb(p,q)
        fp = set(report["pages"][p]["found"])
        fq = set(report["pages"][q]["found"])
        shared = fp & fq
        if d <= 2 and not shared:
            print(f"ADJ-MISS p={p} q={q} d={d}")
            adj_viol += 1
        elif d > 2 and shared:
            print(f"ADJ-FALSE p={p} q={q} d={d} shares {sorted(shared)}")
            adj_viol += 1

print(f"--- pages checked: {len(existing)} ---")
print(f"page-level violations: {total_violations}")
print(f"adjacency violations : {adj_viol}")
if total_violations == 0 and adj_viol == 0 and len(existing) == 49:
    print("OVERALL: PASS")
else:
    print("OVERALL: FAIL" if (total_violations+adj_viol) else "OVERALL: INCOMPLETE")

with open(os.path.join(HERE,"_verify_report.json"),"w") as f:
    json.dump(report,f,indent=2,ensure_ascii=False)
