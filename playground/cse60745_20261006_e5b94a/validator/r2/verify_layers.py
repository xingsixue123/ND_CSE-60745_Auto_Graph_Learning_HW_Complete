import sys, torch, torch.nn as nn, torch.nn.functional as F
sys.path.insert(0,'.')
from extracted_layers import MyGCNConv, MyGATConv, MyGINConv, MyRGCNConv, MyDeepConv
from torch_geometric.nn import GCNConv, GATConv, GINConv, RGCNConv, APPNP

torch.manual_seed(0)
N, C_IN, C_OUT, E = 60, 16, 32, 400
x = torch.randn(N, C_IN)
ei = torch.randint(0, N, (2, E))
ei = ei[:, ei[0] != ei[1]]                      # no self loops in the raw graph
et = torch.randint(0, 3, (ei.size(1),))

def rep(name, a, b):
    d = (a-b).abs().max().item()
    print(f"{name:28s} max|diff| = {d:.3e}   {'OK' if d < 1e-5 else '*** MISMATCH ***'}")
    return d

# ---------- Q1 GCN ----------
m = MyGCNConv(C_IN, C_OUT); r = GCNConv(C_IN, C_OUT, add_self_loops=True, normalize=True)
with torch.no_grad():
    r.lin.weight.copy_(m.lin.weight); r.bias.copy_(m.bias)
rep("Q1 MyGCNConv vs GCNConv", m(x, ei), r(x, ei))

# GCN with self-loops already present in edge_index (idempotence claim)
ei_sl = torch.cat([ei, torch.arange(N).repeat(2,1)], 1)
rep("Q1 self-loop idempotence", m(x, ei), m(x, ei_sl))

# ---------- Q2 GAT ----------
H = 8
m = MyGATConv(C_IN, C_OUT, heads=H)
r = GATConv(C_IN, C_OUT // H, heads=H, concat=True, add_self_loops=True,
            negative_slope=0.2, bias=True)
with torch.no_grad():
    r.lin.weight.copy_(m.lin.weight)
    r.att_src.copy_(m.att_src); r.att_dst.copy_(m.att_dst)
    r.bias.copy_(m.bias)
rep("Q2 MyGATConv vs GATConv", m(x, ei), r(x, ei))
o = m(x, ei); print(f"   GAT output shape {tuple(o.shape)} (expect ({N}, {C_OUT})), heads={m.heads}, head_ch={m.head_channels}")

# ---------- Q3 GIN ----------
m = MyGINConv(C_IN, C_OUT); m.eval()
r = GINConv(m.mlp, train_eps=True); r.eval()
with torch.no_grad(): r.eps.copy_(m.eps)
rep("Q3 MyGINConv vs GINConv", m(x, ei), r(x, ei))

# ---------- Q4 R-GCN ----------
m = MyRGCNConv(C_IN, C_OUT, 3)
r = RGCNConv(C_IN, C_OUT, num_relations=3, aggr='mean', num_bases=None,
             num_blocks=None, root_weight=True, bias=True)
with torch.no_grad():
    for k in range(3): r.weight[k].copy_(m.rel[k].weight.t())
    r.root.copy_(m.root.weight.t()); r.bias.copy_(m.root.bias)
rep("Q4 MyRGCNConv vs RGCNConv", m(x, ei, et), r(x, ei, et))

# ---------- Q5 DeepConv ----------
m = MyDeepConv(C_IN, C_OUT, K=8, alpha=0.3)
app = APPNP(K=8, alpha=0.3, add_self_loops=True, normalize=True)
h = m.lin2(F.relu(m.lin1(x)))
rep("Q5 MyDeepConv vs APPNP", m(x, ei), app(h, ei))
print("   MyDeepConv params:", sum(p.numel() for p in MyDeepConv(64,64).parameters()))
print("   GCN 2-layer params:", sum(sum(p.numel() for p in MyGCNConv(64,64).parameters()) for _ in range(2)))
print("   GCN 8-layer params:", sum(sum(p.numel() for p in MyGCNConv(64,64).parameters()) for _ in range(8)))
