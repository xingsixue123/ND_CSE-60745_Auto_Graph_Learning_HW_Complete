"""
The round-3 submission claims two "machine checks" were added, but no such script
exists in the playground. Independently verify whether the two CLAIMS are true.

Claim 1: homophily denominator == stats_out.json E_und, 13/13 identical.
Claim 2: every h_edge in Table 1 and the two baked into fig_p1_subgraphs
         == homophily_out.json rounded to 2 d.p., 15/15 consistent.
"""
import json
import re

W = "/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/problems/p1"
O = "/home/xing/project/auto_hw_complete_graph/output/cse60745_20260921_2c609b/p1"

hom = json.load(open(f"{W}/homophily_out.json"))
stats = json.load(open(f"{W}/stats_out.json"))

# ---- normalise stats_out.json into {name: E_und} -------------------------
srows = stats if isinstance(stats, list) else stats.get("rows", stats)
if isinstance(srows, dict):
    srows = list(srows.values())
E_und = {}
for r in srows:
    if isinstance(r, dict) and "name" in r:
        E_und[r["name"]] = r.get("E_und")

ALIAS = {"Cora": "Cora (Planetoid)", "CiteSeer": "CiteSeer (Planetoid)",
         "PubMed": "PubMed (Planetoid)", "Cornell": "Cornell (WebKB)",
         "Texas": "Texas (WebKB)", "Wisconsin": "Wisconsin (WebKB)",
         "Actor": "Actor", "Chameleon": "chameleon (WikipediaNetwork)",
         "Squirrel": "squirrel (WikipediaNetwork)", "Coauthor CS": "Coauthor CS",
         "Coauthor Physics": "Coauthor Physics",
         "Amazon Computers": "Amazon Computers", "Amazon Photo": "Amazon Photo"}

print("CLAIM 1 -- homophily denominator vs stats_out.json E_und")
ok1 = bad1 = 0
for name, rec in hom.items():
    key = ALIAS.get(name, name)
    e = E_und.get(key)
    n = rec["n_entries"]
    good = (e == n)
    ok1 += good
    bad1 += not good
    print(f"  {name:20s} hom_denom={n:>10,d}  stats_E_und={str(e):>10s}  "
          f"{'ok' if good else 'MISMATCH'}")
print(f"  => {ok1}/{ok1+bad1} identical  (claim says 13/13)\n")

# ---- Claim 2: parse Table 1 h_edge out of answer.tex ---------------------
tex = open(f"{O}/answer.tex").read()
tbl = re.search(r"\\label\{p1:tab:nodecls\}(.*?)\\end\{tabular\}", tex, re.S).group(1)

parsed = {}
for line in tbl.splitlines():
    if "&" not in line:
        continue
    cells = [c.strip() for c in line.split("&")]
    if len(cells) < 9:
        continue
    ds = re.sub(r"\{|\}|\\rlap.*|\\multirow.*", "", cells[1]).strip()
    last = cells[-1].replace("\\\\", "").strip()
    last = re.sub(r"\\rlap\{.*?\}", "", last).strip()
    m = re.match(r"^([0-9]*\.[0-9]+)", last)
    if m and ds:
        parsed[ds.replace("{,}", ",")] = float(m.group(1))

print("CLAIM 2a -- Table 1 h_edge vs homophily_out.json (2 d.p.)")
ok2 = bad2 = 0
for ds, printed in parsed.items():
    rec = hom.get(ds)
    if rec is None:
        print(f"  {ds:20s} printed={printed}  (no homophily entry -- skipped)")
        continue
    exp = round(rec["h_incl_selfloops"], 2)
    good = abs(exp - printed) < 1e-9
    ok2 += good
    bad2 += not good
    print(f"  {ds:20s} printed={printed:.2f}  json={rec['h_incl_selfloops']:.4f}"
          f" -> {exp:.2f}  {'ok' if good else 'MISMATCH'}")
print(f"  => {ok2}/{ok2+bad2} consistent")

# ---- Claim 2b: the two values baked into the subgraphs figure ------------
print("\nCLAIM 2b -- values baked into fig_p1_subgraphs source")
try:
    fig = open(f"{W}/figs/fig_p1_subgraphs.tex").read()
    for nm, key in [("Cora", "Cora"), ("Texas", "Texas")]:
        found = re.findall(rf"{nm}[^0-9]{{0,40}}([01]\.[0-9]+)", fig)
        exp = round(hom[key]["h_incl_selfloops"], 2)
        print(f"  {nm:8s} in figure {found}  expected {exp:.2f}  "
              f"{'ok' if found and abs(float(found[0])-exp) < 1e-9 else 'CHECK'}")
except FileNotFoundError as e:
    print("  figure source not found:", e)
