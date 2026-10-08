"""Execute the completed notebook's cells in order, in one namespace, exactly as a
notebook would. Cells 23-27 are Q4's (a different problem) and are skipped."""
import json, sys
from pathlib import Path

nb = json.loads(Path(sys.argv[1]).read_text())
SKIP = set(range(23, 28))               # Q4: load_hetero / metapath2vec / MyRGCNConv
ns = {"__name__": "__main__"}
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code" or i in SKIP:
        continue
    src = "".join(c["source"])
    print(f"\n----- cell[{i}] -----", flush=True)
    exec(compile(src, f"cell[{i}]", "exec"), ns)
print("\nNOTEBOOK RAN TO COMPLETION (Q4 cells 23-27 skipped)")
