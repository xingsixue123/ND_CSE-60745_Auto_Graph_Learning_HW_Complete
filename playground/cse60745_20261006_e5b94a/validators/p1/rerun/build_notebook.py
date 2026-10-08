"""Write the completed notebook: fill the Q1/Q2/Q3/Q5 stubs with the bodies from
layers.py and set n_layers for Q5. Every other cell is left byte-identical, including
Q4's, which belongs to a different problem."""
import json, re
from pathlib import Path

SRC = Path("/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb")
DST = Path(__file__).resolve().parent.parent / "Practice3_pyg_basics_completed.ipynb"

src = Path("layers.py").read_text()

def body(cls):
    """The source of one class in layers.py, without the trailing blank lines."""
    m = re.search(rf"^class {cls}\(MessagePassing\):.*?(?=\n# ---|\Z)", src,
                  re.S | re.M)
    return m.group(0).rstrip() + "\n"

nb = json.loads(SRC.read_text())
fills = {15: "MyGCNConv", 18: "MyGATConv", 21: "MyGINConv", 30: "MyDeepConv"}
for idx, cls in fills.items():
    assert nb["cells"][idx]["cell_type"] == "code"
    assert cls in "".join(nb["cells"][idx]["source"]), (idx, cls)
    nb["cells"][idx]["source"] = body(cls).splitlines(keepends=True)
    nb["cells"][idx]["outputs"] = []
    nb["cells"][idx]["execution_count"] = None

# cell 31: "Change n_layers based on your implementation" -- 8 hops is 1 layer of K=8
assert "n_layers=8" in "".join(nb["cells"][31]["source"])
nb["cells"][31]["source"] = [
    "# MyDeepConv reaches K hops in ONE layer, so an 8-hop receptive field is K=8,\n",
    "# n_layers=1 -- not 8 stacked layers.\n",
    'train_and_eval("MyDeepConv", MyDeepConv, n_layers=1)\n',
]
DST.write_text(json.dumps(nb, indent=1) + "\n")
print("wrote", DST)
