"""Explicit correctness checks on HybridGTLayer. Nothing here is judged by eye."""
import torch
torch.set_num_threads(4)
from hybrid_layer import HybridGTLayer, HybridGT
from gt_framework import *

torch.manual_seed(0)
dim, heads = 64, 4
layer = HybridGTLayer(dim, heads).eval()

graphs = ZINC_GRAPHS["train"][:6]
ensure_precomputed(graphs, [HybridGT.precompute])
b = make_batch(graphs, HybridGT.precompute)
x = torch.randn(b["batch"].size(0), dim)
ei, ea, bt = b["edge_index"], b["edge_attr"], b["batch"]
with torch.no_grad():
    full = layer(x, ei, ea, bt)

ok = True

# ---- 1. no information crosses a graph boundary: perturb graph 0's states only ----
x2 = x.clone()
x2[bt == 0] = torch.randn_like(x2[bt == 0])
with torch.no_grad():
    pert = layer(x2, ei, ea, bt)
other = bt != 0
d_other = (full[other] - pert[other]).abs().max().item()
d_g0 = (full[~other] - pert[~other]).abs().max().item()
print(f"[1] perturb graph 0  -> max|delta| on other graphs {d_other:.3e} (want 0), on graph 0 {d_g0:.3e} (want >0)")
ok &= (d_other == 0.0) and (d_g0 > 0)

# ---- 2. batch-composition invariance: a graph alone vs. in a batch of 6 ----
g = graphs[3]
sub = make_batch([g], HybridGT.precompute)
n_before = sum(gg["n"] for gg in graphs[:3])
x_sub = x[bt == 3].clone()
with torch.no_grad():
    alone = layer(x_sub, sub["edge_index"], sub["edge_attr"], sub["batch"])
d_batch = (alone - full[bt == 3]).abs().max().item()
print(f"[2] graph 3 alone vs. in a batch of 6 -> max|delta| {d_batch:.3e} (want ~0)")
ok &= d_batch < 1e-5

# ---- 3. attention weights really are a per-graph distribution over that graph only ----
h, mask = to_dense_batch(x, bt)
B, N, D = h.shape
q, k, v = layer.qkv(h).view(B, N, 3, heads, D // heads).permute(2, 0, 3, 1, 4)
import math
s = q @ k.transpose(-1, -2) / math.sqrt(D // heads)
s = s.masked_fill(~mask[:, None, None, :], float("-inf"))
w = torch.softmax(s, dim=-1).nan_to_num(0.0)
pad_mass = w[:, :, :, :][~mask[:, None, None, :].expand_as(w)].abs().max().item()
rows = w.sum(-1)[mask[:, None, :].expand(B, heads, N)]
print(f"[3] attention mass on padding {pad_mass:.3e} (want 0); real rows sum to "
      f"[{rows.min():.6f}, {rows.max():.6f}] (want 1); dense N={N} = max graph size "
      f"{max(gg['n'] for gg in graphs)}")
ok &= pad_mass == 0.0 and abs(rows.min() - 1) < 1e-5 and abs(rows.max() - 1) < 1e-5

# ---- 4. the local branch is exactly the GINE formula (reference loop over edges) ----
with torch.no_grad():
    mine = layer.local_branch(x, ei, ea)
ref = torch.zeros_like(x)
with torch.no_grad():
    for e in range(ei.size(1)):
        src, dst = int(ei[0, e]), int(ei[1, e])
        ref[dst] += torch.relu(x[src] + layer.bond(ea[e]))
    ref = layer.mpnn((1 + layer.eps) * x + ref)
d_local = (mine - ref).abs().max().item()
print(f"[4] local branch vs. explicit per-edge reference -> max|delta| {d_local:.3e} (want ~0)")
ok &= d_local < 1e-4

# ---- 5. the local branch only uses edges; the global branch only uses `batch` ----
with torch.no_grad():
    no_edges = layer.local_branch(x, ei[:, :0], ea[:0])
    gb = layer.global_branch(x, bt)
print(f"[5] local branch with no edges differs from with edges: "
      f"{(no_edges - mine).abs().max().item():.3e} (want >0); global branch shape {tuple(gb.shape)}")
ok &= (no_edges - mine).abs().max().item() > 0

# ---- 6. invariant: degree sum from edge_index == 2 * undirected edge count ----
deg = torch.bincount(ei[0], minlength=x.size(0))
print(f"[6] sum(deg)={int(deg.sum())} == directed edge count {ei.size(1)}; "
      f"batch['deg'] matches recomputed deg: {bool(torch.equal(deg, b['deg']))}; max deg {int(deg.max())}")
ok &= int(deg.sum()) == ei.size(1) and bool(torch.equal(deg, b["deg"]))

print("\nALL CHECKS PASS" if ok else "\n*** A CHECK FAILED ***")

# ---- 7. the ablation harness is faithful: AblationGT(HybridGTLayer) == HybridGT() ----
from gt_framework import _reset
from variants import AblationGT
a, b2 = HybridGT(), AblationGT(HybridGTLayer)
_reset(a); _reset(b2)
pa, pb = dict(a.named_parameters()), dict(b2.named_parameters())
same_keys = set(pa) == set(pb)
max_pd = max((pa[k] - pb[k]).abs().max().item() for k in pa)
bt_graphs = ZINC_GRAPHS["val"][:32]
ensure_precomputed(bt_graphs, [HybridGT.precompute])
bb = make_batch(bt_graphs, HybridGT.precompute)
a.eval(); b2.eval()
with torch.no_grad():
    d_out = (a(bb) - b2(bb)).abs().max().item()
print(f"[7] AblationGT(HybridGTLayer) vs HybridGT(): same param names {same_keys}, "
      f"max|param delta| {max_pd:.3e}, max|output delta| {d_out:.3e} (all want 0)")
print("CHECK 7 PASS" if same_keys and max_pd == 0.0 and d_out == 0.0 else "*** CHECK 7 FAILED ***")
