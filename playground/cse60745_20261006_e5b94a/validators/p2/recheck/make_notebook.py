"""Write Practice3_pyg_basics_p2_completed.ipynb: the original notebook with cell 27
(nb['cells'][26], MyRGCNConv) replaced by the completed layer from rgcn_run.py.
Nothing else is touched -- the harness cells stay frozen.
"""
import ast, json, pathlib

SRC_NB = pathlib.Path("/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb")
OUT_NB = pathlib.Path("../Practice3_pyg_basics_p2_completed.ipynb")

run_src = pathlib.Path("rgcn_run.py").read_text()
tree = ast.parse(run_src)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "MyRGCNConv")
answer = ast.get_source_segment(run_src, cls)

nb = json.loads(SRC_NB.read_text())
cell = nb["cells"][26]                      # brief's "cell 27" is 1-indexed
assert cell["cell_type"] == "code"
assert "class MyRGCNConv" in "".join(cell["source"]), "cell 27 is not the R-GCN stub"
assert "raise NotImplementedError" in "".join(cell["source"])

cell["source"] = [l + "\n" for l in answer.split("\n")]
cell["source"][-1] = cell["source"][-1].rstrip("\n")
cell["outputs"] = []
cell["execution_count"] = None

OUT_NB.write_text(json.dumps(nb, indent=1) + "\n")
print(f"wrote {OUT_NB.resolve()}  ({len(nb['cells'])} cells, replaced cells[26])")
