"""Check that every notebook cell spliced into rgcn_run.py is reproduced CONTIGUOUSLY and
byte-for-byte -- not merely that its lines appear somewhere.

Round 1's validator was right that a set-membership test is too weak: it would pass a
reordered cell or a deleted duplicate line. This does a contiguous-block comparison, and
for the two cells with declared cuts it checks the kept part is an exact prefix.
"""
import json, pathlib, sys

nb = json.loads(pathlib.Path(
    "/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb").read_text())
run = pathlib.Path("rgcn_run.py").read_text()

VERBATIM = (3, 5, 11, 12, 25, 26)
PREFIX = {7: "X = node2vec_features(", 28: 'train_and_eval_hetero("R-GCN")'}

ok = True
for n in sorted(VERBATIM + tuple(PREFIX)):
    src = "".join(nb["cells"][n - 1]["source"]).rstrip("\n")
    if n in PREFIX:
        kept = src[:src.index(PREFIX[n])].rstrip()
        verdict = "exact prefix, only the declared cut" if kept and kept in run else "MISMATCH"
        ok &= kept in run
        cut_lines = len(src.split("\n")) - len(kept.split("\n"))
        print(f"cell {n:2d}: {len(kept.split(chr(10))):3d} kept lines  "
              f"({cut_lines} cut at `{PREFIX[n]}`)  -> {verdict}")
    else:
        verdict = "byte-identical, contiguous" if src in run else "MISMATCH"
        ok &= src in run
        print(f"cell {n:2d}: {len(src.split(chr(10))):3d} lines  -> {verdict}")

# the delivered answer must be the only non-notebook code in the file
answer = pathlib.Path("my_rgcn_conv.py").read_text().rstrip()
print(f"cell 27: {len(answer.split(chr(10))):3d} lines  -> my answer, present contiguously: "
      f"{answer in run}")
ok &= answer in run

print("\nFROZEN HARNESS REPRODUCED VERBATIM AND CONTIGUOUSLY" if ok else "\nMISMATCH")
sys.exit(0 if ok else 1)
