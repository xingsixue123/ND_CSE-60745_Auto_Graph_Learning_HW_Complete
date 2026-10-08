"""Two independent checks that MyRGCNConv is correct on the REAL graph.

1. Numerical equivalence with torch_geometric.nn.RGCNConv (aggr="mean", no basis
   decomposition) with weights copied across, on the full 6,067,650-edge graph.
2. Train PyG's own RGCNConv through the SAME frozen harness and compare metrics.
   If the official layer lands in the same place, the low MRR is the task's, not mine.
"""
import json, time, torch, torch.nn.functional as F
from torch import nn
from torch_geometric.nn import RGCNConv
import rgcn_run as R

torch.manual_seed(0)
N = R.HETERO["num_nodes"]
ei, et = R.HETERO["edge_index"], R.HETERO["edge_type"]
Cin, Cout = 64, 8

mine = R.MyRGCNConv(Cin, Cout, 3).eval()
ref = RGCNConv(Cin, Cout, 3, aggr="mean", num_bases=None, num_blocks=None).eval()
print("PyG RGCNConv aggr:", ref.aggr, "| num_bases:", ref.num_bases, "| root is None:", ref.root is None)

with torch.no_grad():
    for r in range(3):
        ref.weight[r].copy_(mine.rel[r].weight.t())      # nn.Linear is [out, in]
    ref.root.copy_(mine.root.weight.t())
    ref.bias.copy_(mine.root.bias)
    a = mine(R.X_HETERO, ei, et)
    b = ref(R.X_HETERO, ei, et)
d = (a - b).abs()
print(f"max |mine - PyG RGCNConv| = {float(d.max()):.3e}   "
      f"(rel to |out| max {float(b.abs().max()):.3f})   allclose: {torch.allclose(a, b, atol=1e-4)}")
assert torch.allclose(a, b, atol=1e-4), "MyRGCNConv disagrees with PyG's RGCNConv"

# ---- 2. PyG's RGCNConv through the frozen harness --------------------------------
class PyGShim(RGCNConv):
    def __init__(self, i, o, nr):
        super().__init__(i, o, nr, aggr="mean")

_orig = R.MyRGCNConv
R.MyRGCNConv = PyGShim
try:
    print("\n-- torch_geometric.nn.RGCNConv through train_and_eval_hetero --")
    pyg_best = R.train_and_eval_hetero("PyG RGCNConv")
finally:
    R.MyRGCNConv = _orig
print("PYG_RESULT_JSON " + json.dumps(pyg_best))

# ---- 3. repeat MY layer 5x with different torch seeds, to size the run-to-run noise
print("\n-- MyRGCNConv, five seeds --")
rows = []
for s in range(5):
    b = R.train_and_eval_hetero(f"R-GCN seed{s}", seed=s)
    rows.append(b)
import statistics as st
for k in ("MRR", "hit@1", "test_MRR", "test_hit@1"):
    v = [r[k] for r in rows]
    print(f"  {k:12} mean {st.mean(v):.4f}  sd {st.pstdev(v):.4f}  min {min(v):.4f}  max {max(v):.4f}")
print("SEEDS_JSON " + json.dumps(rows))
