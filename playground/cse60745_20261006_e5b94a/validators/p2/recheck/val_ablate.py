"""Decisive test of answer.tex's claim that the pooled-c_i gain comes from fixing the
averaging *within the listening relations*.

Four variants, same harness, same seeds:
  A per-relation  c_{i,r}=|N_r(i)| everywhere          (the delivered answer)
  B pooled        c_{i,r}=c_i      everywhere          (0.286 in the worker's log)
  C friend-pooled friend uses c_i, listening per-rel   <- isolates the friend change
  D listen-pooled listening uses c_i, friend per-rel   <- isolates the listening change
If the worker's stated mechanism is right, D recovers ~0.286 and C does not.
"""
import torch, torch.nn as nn, numpy as np
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import scatter
import rgcn_run as R

N = R.HETERO["num_nodes"]
def degs(g):
    d = torch.zeros(g["num_relations"], N)
    for r in range(g["num_relations"]):
        ei = g["edge_index"][:, g["edge_type"] == r]
        d[r] = torch.bincount(ei[1], minlength=N).float()
    return d
DEG = {id(R.HETERO): degs(R.HETERO), id(R.HETERO_TRAINVAL): degs(R.HETERO_TRAINVAL)}

MODE = {"pooled": None}
class Conv(MessagePassing):
    def __init__(self, i, o, nr):
        super().__init__(aggr="sum")
        self.num_relations = nr
        self.root = nn.Linear(i, o, bias=True)
        self.rel = nn.ModuleList([nn.Linear(i, o, bias=False) for _ in range(nr)])
        self.reset_parameters()
    def reset_parameters(self):
        super().reset_parameters(); self.root.reset_parameters()
        for l in self.rel: l.reset_parameters()
    def forward(self, x, edge_index, edge_type):
        out = self.root(x); n = x.size(-2)
        deg = DEG[self._gid]
        c_pool = deg.sum(0)
        for r in range(self.num_relations):
            ei = edge_index[:, edge_type == r]
            if ei.size(1) == 0: continue
            acc = self.propagate(ei, x=self.rel[r](x), size=(n, n))
            use_pool = MODE["pooled"] is not None and r in MODE["pooled"]
            c = (c_pool if use_pool else deg[r]).clamp(min=1).unsqueeze(1)
            out = out + acc / c
        return out
    def message(self, x_j): return x_j

# route the graph identity into the conv (the harness passes edge_index only)
_enc = R.RGCNLinkPredictor.encode
def encode(self, x, ei, et):
    gid = id(R.HETERO) if ei.size(1) == R.HETERO["edge_index"].size(1) else id(R.HETERO_TRAINVAL)
    for c in self.convs: c._gid = gid
    return _enc(self, x, ei, et)
R.RGCNLinkPredictor.encode = encode
R.MyRGCNConv = Conv
import sys; sys.modules["rgcn_run"].MyRGCNConv = Conv

for name, pooled in [("A per-relation", set()), ("B pooled-all", {0,1,2}),
                     ("C friend-pooled", {0}), ("D listen-pooled", {1,2})]:
    MODE["pooled"] = pooled
    vals = [R.train_and_eval_hetero(f"{name:16}", seed=s)["MRR"] for s in range(3)]
    print(f"  >> {name:16} val MRR mean {np.mean(vals):.4f}  {[round(v,4) for v in vals]}\n")
