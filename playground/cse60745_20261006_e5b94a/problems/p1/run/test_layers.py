"""Correctness checks: each of my layers against PyG's own reference implementation,
with the parameters copied across, plus a hand-computed GCN check on a 4-node graph."""
import math
import torch
from torch import nn
from torch_geometric.nn import GCNConv, GATConv, GINConv, APPNP
from torch_geometric.utils import to_undirected, coalesce, remove_self_loops

from layers import MyGCNConv, MyGATConv, MyGINConv, MyDeepConv

torch.manual_seed(0)
N, F_IN, F_OUT = 60, 16, 24
e = torch.randint(0, N, (2, 300))
EI = coalesce(to_undirected(e), num_nodes=N)
# deliberately include a pre-existing self-loop: forward() must not double-count it
EI = coalesce(torch.cat([EI, torch.tensor([[3], [3]])], 1), num_nodes=N)
XT = torch.randn(N, F_IN)

ok = True
def check(name, a, b, tol=1e-5):
    global ok
    d = (a - b).abs().max().item()
    print(f"{name:52} max|diff| = {d:.3e}  {'OK' if d < tol else 'FAIL'}")
    ok &= d < tol

# ---------------------------------------------------------------- Q1 vs GCNConv
mine = MyGCNConv(F_IN, F_OUT)
ref = GCNConv(F_IN, F_OUT, add_self_loops=True, normalize=True, bias=True)
with torch.no_grad():
    ref.lin.weight.copy_(mine.lin.weight)
    ref.bias.copy_(mine.bias + 0.3); mine.bias.copy_(ref.bias)
check("Q1 MyGCNConv vs torch_geometric.nn.GCNConv", mine(XT, EI), ref(XT, EI))

# hand-computed GCN on a path 0-1-2 plus isolated node 3
ei_s = torch.tensor([[0, 1, 1, 2], [1, 0, 2, 1]])
xs = torch.eye(4)[:, :1] * 0 + torch.tensor([[1.], [2.], [4.], [8.]])
m = MyGCNConv(1, 1)
with torch.no_grad():
    m.lin.weight.fill_(1.0); m.bias.zero_()
got = m(xs, ei_s).flatten()
dh = torch.tensor([2., 3., 2., 1.])            # closed-neighbourhood degrees
want = torch.tensor([
    1/math.sqrt(dh[0]*dh[0])*1 + 1/math.sqrt(dh[0]*dh[1])*2,
    1/math.sqrt(dh[1]*dh[0])*1 + 1/math.sqrt(dh[1]*dh[1])*2 + 1/math.sqrt(dh[1]*dh[2])*4,
    1/math.sqrt(dh[2]*dh[1])*2 + 1/math.sqrt(dh[2]*dh[2])*4,
    1/math.sqrt(dh[3]*dh[3])*8,                # isolated node: d_hat = 1, no NaN
])
check("Q1 MyGCNConv vs hand-computed 4-node graph", got, want)

# ---------------------------------------------------------------- Q2 vs GATConv
H = 8
mine = MyGATConv(F_IN, F_OUT, heads=H)
ref = GATConv(F_IN, F_OUT // H, heads=H, concat=True, negative_slope=0.2,
              dropout=0.0, add_self_loops=True, bias=True)
with torch.no_grad():
    ref.lin.weight.copy_(mine.lin.weight)
    ref.att_src.copy_(mine.att_src); ref.att_dst.copy_(mine.att_dst)
    ref.bias.copy_(mine.bias)
check("Q2 MyGATConv vs torch_geometric.nn.GATConv (8 heads)", mine(XT, EI), ref(XT, EI))
print(f"{'Q2 output width == out_channels':52} {mine(XT, EI).shape[1]} == {F_OUT}")
ok &= mine(XT, EI).shape[1] == F_OUT
avg = MyGATConv(F_IN, F_OUT, heads=H, concat=False)
ok &= avg(XT, EI).shape[1] == F_OUT
print(f"{'Q2 concat=False (head-averaging) width':52} {avg(XT, EI).shape[1]} == {F_OUT}")

# ---------------------------------------------------------------- Q3 vs GINConv
# PyG's GINConv does not strip self-loops, so on the loop-free graph the two must agree
# exactly; on the graph with the injected loop at node 3 they must differ at node 3 only,
# where mine is the one matching the notebook's open-neighbourhood sum.
EI_NOLOOP, _ = remove_self_loops(EI)
mine = MyGINConv(F_IN, F_OUT).eval()           # eval(): BatchNorm uses running stats
ref = GINConv(mine.mlp, eps=0.0, train_eps=True).eval()
check("Q3 MyGINConv vs GINConv (loop-free graph)", mine(XT, EI_NOLOOP), ref(XT, EI_NOLOOP))
differ = ((mine(XT, EI) - ref(XT, EI)).abs().max(1).values > 1e-6).nonzero().flatten()
loops = sorted(set(EI[0][EI[0] == EI[1]].tolist()))     # every node carrying a self-loop
print(f"{'Q3 self-loop stripped: rows differing from GINConv':52} "
      f"{differ.tolist()} == self-loop nodes {loops}")
ok &= differ.tolist() == loops
print(f"{'Q3 eps initialised to':52} {float(mine.eps.detach())}")
ok &= float(mine.eps.detach()) == 0.0

# ------------------------------------------------------- Q5 propagation vs APPNP
mine = MyDeepConv(F_IN, F_OUT, K=8, alpha=0.1).eval()
with torch.no_grad():
    h = mine.lin2(torch.relu(mine.lin1(XT)))
ref = APPNP(K=8, alpha=0.1, dropout=0.0)
check("Q5 MyDeepConv propagation vs torch_geometric.nn.APPNP", mine(XT, EI), ref(h, EI))

# ------------------------------------- reset_parameters must be callable twice
for cls in (MyGCNConv, MyGATConv, MyGINConv, MyDeepConv):
    c = cls(F_IN, F_OUT)
    c.reset_parameters(); c.reset_parameters()
    out = c.eval()(XT, EI)
    assert out.shape == (N, F_OUT) and torch.isfinite(out).all()
print(f"{'reset_parameters() twice + output shape [N, out]':52} OK (all four layers)")

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
