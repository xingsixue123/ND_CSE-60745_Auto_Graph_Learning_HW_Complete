"""(a) is the harness reproducible at a fixed seed?  (b) does single-threading fix it?
(c) what does the paper's own link-prediction normalisation c_i = sum_r |N_i^r| give?
(d) how collapsed are the scores at the end of training?
"""
import json, torch, torch.nn.functional as F
from torch import nn
from torch_geometric.nn import MessagePassing
import rgcn_run as R

print("torch threads:", torch.get_num_threads())
print("\n-- (a) two identical seed-0 runs, default threading --")
a1 = R.train_and_eval_hetero("run A", seed=0)
a2 = R.train_and_eval_hetero("run B", seed=0)
print("   identical:", a1["MRR"] == a2["MRR"] and a1["epoch"] == a2["epoch"])

print("\n-- (b) the same, with torch.set_num_threads(1) --")
torch.set_num_threads(1)
b1 = R.train_and_eval_hetero("1-thread A", seed=0)
b2 = R.train_and_eval_hetero("1-thread B", seed=0)
print("   identical:", b1["MRR"] == b2["MRR"] and b1["epoch"] == b2["epoch"])
torch.set_num_threads(16)

# --- (c) c_{i,r} = c_i = sum_r |N_i^r|, the constant the R-GCN paper's section 5.2 says
#         worked best for *link prediction*. Same layer, aggr="add" + one shared divisor.
class AcrossRelConv(MessagePassing):
    def __init__(self, in_channels, out_channels, num_relations):
        super().__init__(aggr="add")
        self.num_relations = num_relations
        self.root = nn.Linear(in_channels, out_channels, bias=True)
        self.rel = nn.ModuleList([nn.Linear(in_channels, out_channels, bias=False)
                                  for _ in range(num_relations)])
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.root.reset_parameters()
        for lin in self.rel:
            lin.reset_parameters()

    def forward(self, x, edge_index, edge_type):
        n = x.size(self.node_dim)
        acc = torch.zeros(n, self.root.out_features)
        for r in range(self.num_relations):
            ei_r = edge_index[:, edge_type == r]
            if ei_r.size(1) == 0:
                continue
            acc = acc + self.propagate(ei_r, x=self.rel[r](x), size=(n, n))
        c = torch.zeros(n).index_add_(0, edge_index[1], torch.ones(edge_index.size(1)))
        return self.root(x) + acc / c.clamp(min=1).unsqueeze(1)

    def message(self, x_j):
        return x_j

print("\n-- (c) paper's link-prediction normalisation c_i = sum_r |N_i^r| --")
_orig = R.MyRGCNConv
R.MyRGCNConv = AcrossRelConv
try:
    c_runs = [R.train_and_eval_hetero(f"c_i seed{s}", seed=s) for s in range(3)]
finally:
    R.MyRGCNConv = _orig
import statistics as st
print("   val MRR mean", round(st.mean([r['MRR'] for r in c_runs]), 4),
      "| test MRR mean", round(st.mean([r['test_MRR'] for r in c_runs]), 4))

# --- (d) how collapsed are the scores?
print("\n-- (d) score spread, my layer, seed 0, after 22 epochs (the harness's horizon) --")
torch.manual_seed(0)
model = R.RGCNLinkPredictor(3)
opt = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
g = R.HETERO
for epoch in range(1, 23):
    model.train(); opt.zero_grad()
    z = model.encode(R.X_HETERO, g["edge_index"], g["edge_type"])
    loss = F.binary_cross_entropy_with_logits(model.score(z, R.PAIRS["train"]), R.LABELS["train"])
    loss.backward(); opt.step()
model.eval()
with torch.no_grad():
    z = model.encode(R.X_HETERO, g["edge_index"], g["edge_type"])
    s = model.score(z, R.PAIRS["val"])
print(f"   final train loss {float(loss):.5f}   ln2 = {torch.log(torch.tensor(2.0)).item():.5f}")
print(f"   val score   mean {float(s.mean()):+.3e}  sd {float(s.std()):.3e}  "
      f"max|.| {float(s.abs().max()):.3e}")
print(f"   embedding   mean row norm {float(z.norm(dim=1).mean()):.3e}")
