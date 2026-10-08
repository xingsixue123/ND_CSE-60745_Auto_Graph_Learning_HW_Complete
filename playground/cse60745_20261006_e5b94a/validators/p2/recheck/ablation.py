"""Round-1 defect [1.1]: WHY does the pooled c_i help?

My answer.tex claimed it was smoothing inside the two listening relations. Test that
directly: (i) measure the per-relation rescaling pooling actually applies, (ii) ablate
which relations are pooled, 4 variants x 3 seeds through the same frozen harness.
"""
import json, statistics as st, torch
from torch import nn
from torch_geometric.nn import MessagePassing
import rgcn_run as R


class FlexRGCNConv(MessagePassing):
    """Same layer, but each relation's denominator is selectable:
    per-relation |N_r(i)| (the delivered choice) or pooled c_i = sum_r |N_r(i)|."""
    POOLED = frozenset()                       # class-level knob, set per variant

    def __init__(self, in_channels, out_channels, num_relations):
        super().__init__(aggr="add")           # "add" + explicit divisor
        self.num_relations = num_relations
        self.root = nn.Linear(in_channels, out_channels, bias=True)
        self.rel = nn.ModuleList([nn.Linear(in_channels, out_channels, bias=False)
                                  for _ in range(num_relations)])
        self._deg_cache = {}
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.root.reset_parameters()
        for lin in self.rel:
            lin.reset_parameters()

    def _degrees(self, edge_index, edge_type, n):
        key = (id(edge_index), n)
        if key not in self._deg_cache:
            d = [torch.zeros(n).index_add_(
                     0, edge_index[1][edge_type == r],
                     torch.ones(int((edge_type == r).sum())))
                 for r in range(self.num_relations)]
            self._deg_cache[key] = (d, torch.stack(d).sum(0))
        return self._deg_cache[key]

    def forward(self, x, edge_index, edge_type):
        n = x.size(self.node_dim)
        deg, c = self._degrees(edge_index, edge_type, n)
        out = self.root(x)
        for r in range(self.num_relations):
            ei_r = edge_index[:, edge_type == r]
            if ei_r.size(1) == 0:
                continue
            agg = self.propagate(ei_r, x=self.rel[r](x), size=(n, n))
            denom = (c if r in self.POOLED else deg[r]).clamp(min=1).unsqueeze(1)
            out = out + agg / denom
        return out

    def message(self, x_j):
        return x_j


# ---- control: variant A must reproduce the DELIVERED layer bit-for-bit -------------
torch.manual_seed(0)
mine = R.MyRGCNConv(64, 8, 3).eval()
flex = FlexRGCNConv(64, 8, 3).eval()
FlexRGCNConv.POOLED = frozenset()
with torch.no_grad():
    flex.root.load_state_dict(mine.root.state_dict())
    for r in range(3):
        flex.rel[r].load_state_dict(mine.rel[r].state_dict())
    a = mine(R.X_HETERO, R.HETERO["edge_index"], R.HETERO["edge_type"])
    b = flex(R.X_HETERO, R.HETERO["edge_index"], R.HETERO["edge_type"])
print(f"control: |variant A - delivered layer| max = {float((a - b).abs().max()):.3e}  "
      f"(must be ~0)")

# ---- (i) what rescaling does pooling actually apply? ------------------------------
g, N = R.HETERO, R.HETERO["num_nodes"]
deg = [torch.zeros(N).index_add_(0, g["edge_index"][1][g["edge_type"] == r],
                                 torch.ones(int((g["edge_type"] == r).sum())))
       for r in range(3)]
c = torch.stack(deg).sum(0)
print("\nrescaling applied by pooling, |N_r(i)| / c_i :")
for r, name in enumerate(["friend", "listens", "listened_by"]):
    m = deg[r] > 0
    ratio = (deg[r][m] / c[m])
    print(f"  relation {r} {name:12} mean {float(ratio.mean()):.4f}  "
          f"median {float(ratio.median()):.4f}  "
          f"(= down-weighting by {1/float(ratio.mean()):.1f}x)  over {int(m.sum())} nodes")

# ---- (ii) ablation ----------------------------------------------------------------
VARIANTS = [("A per-relation (delivered)", frozenset()),
            ("B pooled everywhere",        frozenset({0, 1, 2})),
            ("C friend pooled only",       frozenset({0})),
            ("D listening pooled only",    frozenset({1, 2}))]
_orig = R.MyRGCNConv
R.MyRGCNConv = FlexRGCNConv
results = {}
try:
    for name, pooled in VARIANTS:
        FlexRGCNConv.POOLED = pooled
        runs = [R.train_and_eval_hetero(name[:14], seed=s) for s in range(3)]
        results[name] = runs
        print(f"  -> {name:28} val MRR mean {st.mean([r['MRR'] for r in runs]):.4f}  "
              f"test MRR mean {st.mean([r['test_MRR'] for r in runs]):.4f}")
finally:
    R.MyRGCNConv = _orig
    FlexRGCNConv.POOLED = frozenset()

print("\nSUMMARY  (3 seeds each, same frozen harness)")
print(f"{'variant':30} {'val MRR':>9} {'test MRR':>9}")
for name, _ in VARIANTS:
    r = results[name]
    print(f"{name:30} {st.mean([x['MRR'] for x in r]):9.4f} "
          f"{st.mean([x['test_MRR'] for x in r]):9.4f}")
print("ABLATION_JSON " + json.dumps({k: v for k, v in results.items()}))
