"""Validator's own, STRICTER fidelity check: compare each spliced block in rgcn_run.py
against the original notebook cell as a contiguous, ordered block (not a line set)."""
import json, pathlib, re, difflib

nb = json.loads(pathlib.Path(
    "/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb").read_text())
run = pathlib.Path("rgcn_run.py").read_text()

# split rgcn_run.py on the generated cell markers
marks = list(re.finditer(r"^# ===== cell (\d+)(.*?) =====(.*)$", run, re.M))
print("blocks found:", [(int(m.group(1)), m.group(2).strip(), m.group(3).strip()) for m in marks])

blocks = {}
for i, m in enumerate(marks):
    end = marks[i+1].start() if i+1 < len(marks) else len(run)
    body = run[m.end():end]
    # strip the trailing __main__ guard from the last block
    body = re.split(r'^if __name__ == "__main__":', body, flags=re.M)[0]
    blocks[int(m.group(1))] = body.strip("\n")

bad = 0
for n in (3, 5, 7, 11, 12, 25, 26, 28):
    orig = "".join(nb["cells"][n-1]["source"]).rstrip("\n")
    got = blocks[n]
    if orig == got:
        print(f"cell {n:2d}: IDENTICAL ({len(orig.splitlines())} lines)")
        continue
    # allowed: got is a strict prefix of orig (the two declared cuts)
    if orig.startswith(got) or orig.rstrip().startswith(got.rstrip()):
        cut = orig[len(got):].strip()
        print(f"cell {n:2d}: PREFIX-ONLY, tail cut = {cut!r}")
        continue
    bad += 1
    print(f"cell {n:2d}: *** DIFFERS ***")
    for l in difflib.unified_diff(orig.splitlines(), got.splitlines(),
                                  "notebook", "rgcn_run.py", lineterm="", n=1):
        print("   ", l)

# cell 27 must equal the delivered answer source AND the answer.tex listing
ans = pathlib.Path("my_rgcn_conv.py").read_text().rstrip("\n")
print("\ncell 27 block == my_rgcn_conv.py :", blocks[27] == ans)

tex = pathlib.Path("/home/xing/project/auto_hw_complete/output/cse60745_20261006_e5b94a/p2/answer.tex").read_text()
listing = re.search(r"\\begin\{lstlisting\}\[[^\]]*\]\n(.*?)\\end\{lstlisting\}", tex, re.S).group(1).rstrip("\n")
print("answer.tex listing == my_rgcn_conv.py :", listing == ans)
if listing != ans:
    for l in difflib.unified_diff(ans.splitlines(), listing.splitlines(),
                                  "my_rgcn_conv.py", "answer.tex", lineterm="", n=1):
        print("   ", l)
print("\nVERDICT:", "ALL BLOCKS FAITHFUL" if bad == 0 else f"{bad} BLOCK(S) ALTERED")
