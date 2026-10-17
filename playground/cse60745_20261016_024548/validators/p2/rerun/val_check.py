"""Independent validator checks: model-level graph isolation, permutation invariance,
GINE direction, and an edge-count invariant. Written without reusing the worker's checks."""
import math, torch
torch.set_num_threads(2)
from hybrid_layer import HybridGTLayer, HybridGT
from gt_framework import *
from gt_framework import _reset

torch.manual_seed(123)
m = HybridGT(); _reset(m); m.eval()

G = ZINC_GRAPHS["test"][:12]
ensure_precomputed(G, [HybridGT.precompute])
b = make_batch(G, HybridGT.precompute)
with torch.no_grad():
    pred_batched = m(b).view(-1)

# A: each graph alone must give the same prediction as inside the batch of 12.
solo = []
for g in G:
    bb = make_batch([g], HybridGT.precompute)
    with torch.no_grad():
        solo.append(m(bb).view(-1).item())
solo = torch.tensor(solo)
dA = (solo - pred_batched).abs().max().item()
print(f"[A] solo vs batched prediction, max|delta| = {dA:.3e}  (want ~0; >1e-4 means attention leaks across molecules)")

# B: reorder the graphs in the batch; predictions must follow, unchanged.
perm = [7,0,11,3,5,1,9,2,8,4,10,6]
bp = make_batch([G[i] for i in perm], HybridGT.precompute)
with torch.no_grad():
    pred_perm = m(bp).view(-1)
dB = (pred_perm - pred_batched[perm]).abs().max().item()
print(f"[B] permuted batch, max|delta| = {dB:.3e}  (want ~0)")

# C: GINE direction + formula, recomputed from scratch with a dense adjacency.
layer = m.layers[0]
x = torch.randn(b["batch"].size(0), 64)
ei, ea = b["edge_index"], b["edge_attr"]
n = x.size(0)
with torch.no_grad():
    got = layer.local_branch(x, ei, ea)
    # dense reference: A[dst, src] = 1 ; message relu(x_src + e)
    agg = torch.zeros_like(x)
    for e in range(ei.size(1)):
        s, d = int(ei[0, e]), int(ei[1, e])
        agg[d] += torch.relu(x[s] + layer.bond.weight[int(ea[e])])
    want = layer.mpnn((1 + layer.eps) * x + agg)
print(f"[C] GINE vs dense reference, max|delta| = {(got-want).abs().max().item():.3e} (want ~0)")

# D: is edge_index symmetric (so src/dst convention cannot matter)?
E = set(map(tuple, ei.t().tolist()))
sym = all((d, s) in E for s, d in E)
# and is edge_attr symmetric too?
attr = {}
asym_attr = 0
for (s, d), a in zip(ei.t().tolist(), ea.tolist()):
    attr[(s, d)] = a
for (s, d), a in attr.items():
    if attr.get((d, s)) != a:
        asym_attr += 1
print(f"[D] edge_index symmetric: {sym}; edges with asymmetric bond type: {asym_attr}; |E_dir|={ei.size(1)}")

# E: bond ids present in the whole ZINC train split
ids = set()
for g in ZINC_GRAPHS["train"]:
    ids |= set(g["edge_attr"].tolist())
print(f"[E] bond ids over ZINC train = {sorted(ids)}  (embedding sized 4)")

# F: does the global branch output depend on `batch` grouping? merge two graphs into one id
bt = b["batch"].clone()
with torch.no_grad():
    g_ok = layer.global_branch(x, bt)
    bt2 = bt.clone(); bt2[bt2 == 1] = 0   # pretend graphs 0 and 1 are one molecule
    bt2[bt2 > 1] -= 1
    g_merged = layer.global_branch(x, bt2)
sel = (bt == 0) | (bt == 1)
print(f"[F] merging graphs 0,1 changes their outputs by {(g_ok[sel]-g_merged[sel]).abs().max().item():.3e} "
      f"(want >0: proves the mask is actually doing the separating) and leaves the rest at "
      f"{(g_ok[~sel]-g_merged[~sel]).abs().max().item():.3e} (want 0)")
