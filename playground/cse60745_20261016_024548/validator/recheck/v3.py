import torch, numpy as np, math
from gt_framework import *
from solution import LapPETransformer, SPDAttention, SparseSPDAttention, pair_set
from hybrid_layer import HybridGTLayer, HybridGT

def np_(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)
print("plain GraphTransformer                :", f"{np_(GraphTransformer())/1000:.1f}k")
print("demo CentralityTransformer+CNAttention:", f"{np_(CentralityTransformer(attention_cls=CNAttention))/1000:.1f}k")
print("HybridGT (cell 22)                    :", f"{np_(HybridGT())/1000:.1f}k")

# ---- sparse vs dense equivalence on a complete pair set ----
torch.manual_seed(0)
g = ZINC_GRAPHS["train"][0]; n = g["n"]; ei = g["edge_index"]
dim, heads = 64, 4
dense = SPDAttention(dim, heads)
sparse = SparseSPDAttention(dim, heads)
sparse.load_state_dict(dense.state_dict(), strict=False)
with torch.no_grad():
    sparse.type_table.weight.zero_()          # no pair-type bias -> identical to dense
spd = torch.as_tensor(SPDAttention.precompute(ei, n)["spd"])
h = torch.randn(1, n, dim)
mask = torch.ones(1, n, dtype=torch.bool)
out_d = dense(h, {"spd": spd[None]}, mask)[0]
# complete pair set, no virtual node
full = torch.stack([torch.arange(n).repeat_interleave(n), torch.arange(n).repeat(n)])
src, dst = full
enc = {"spd": spd[dst, src], "pair_type": pair_types(full, ei, n)}
out_s = sparse(h[0], enc, full)
print("max |dense - sparse| on complete pair set:", f"{float((out_d-out_s).abs().max()):.3e}")

# ---- rows of sparse attention sum to 1 over each query's pairs ----
p = SparseSPDAttention.attention_pairs(ei, n)
print("submitted pair set on graph 0: P =", p.size(1), " max id =", int(p.max()), " n =", n)
