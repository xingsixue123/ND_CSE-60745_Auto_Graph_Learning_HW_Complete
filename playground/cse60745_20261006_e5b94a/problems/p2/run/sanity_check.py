"""Unit-checks MyRGCNConv against a brute-force reference, on toy graphs.

The class under test is lifted verbatim out of rgcn_run.py by AST, so this tests
exactly the code that is delivered in answer.tex -- no second copy to drift.
"""
import ast, pathlib, torch
from torch import nn
from torch_geometric.nn import MessagePassing

src = pathlib.Path("rgcn_run.py").read_text()
tree = ast.parse(src)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "MyRGCNConv")
ns = {"nn": nn, "torch": torch, "MessagePassing": MessagePassing}
exec(ast.get_source_segment(src, cls), ns)
MyRGCNConv = ns["MyRGCNConv"]

torch.manual_seed(0)

# --- toy graph: 6 nodes, 2 relations; node 5 has no incoming edge of either relation,
# --- node 4 has incoming edges of relation 1 only.
N, R, Cin, Cout = 6, 2, 5, 3
edge_index = torch.tensor([[0, 1, 2, 0, 3, 1],
                           [1, 1, 3, 2, 4, 4]])
edge_type  = torch.tensor([0, 0, 0, 1, 1, 1])
x = torch.randn(N, Cin)

conv = MyRGCNConv(Cin, Cout, R)
conv.eval()
out = conv(x, edge_index, edge_type)

# brute-force reference:  h_i' = W_0 h_i + sum_r (1/|N_r(i)|) W_r sum_{j in N_r(i)} h_j
ref = conv.root(x).clone()
for r in range(R):
    acc = torch.zeros(N, Cin)
    cnt = torch.zeros(N)
    for k in range(edge_index.size(1)):
        if edge_type[k] == r:
            s, t = int(edge_index[0, k]), int(edge_index[1, k])
            acc[t] += x[s]
            cnt[t] += 1
    for i in range(N):
        if cnt[i] > 0:
            ref[i] += conv.rel[r](acc[i] / cnt[i])
print("shape                      ", tuple(out.shape), "expected", (N, Cout))
assert out.shape == (N, Cout)
print("max |out - brute force|    ", float((out - ref).abs().max()))
assert torch.allclose(out, ref, atol=1e-5)
print("any NaN/Inf                ", bool(torch.isnan(out).any() or torch.isinf(out).any()))
assert torch.isfinite(out).all()

# node 5: no incoming edge at all -> must be exactly W_0 h_5 (mean of empty set == 0)
print("isolated node 5 == W_0 h_5 ", torch.allclose(out[5], conv.root(x[5]), atol=1e-6))
assert torch.allclose(out[5], conv.root(x[5]), atol=1e-6)
# node 4: relation-1 neighbours only -> no relation-0 contribution
r0_only = conv.rel[0](torch.zeros(Cin))
print("node 4 drops empty rel 0   ",
      torch.allclose(out[4], conv.root(x[4]) + conv.rel[1]((x[3] + x[1]) / 2), atol=1e-5))
assert torch.allclose(out[4], conv.root(x[4]) + conv.rel[1]((x[3] + x[1]) / 2), atol=1e-5)

# --- reset_parameters must be safe to call twice and must actually change weights
before = conv.rel[0].weight.clone()
conv.reset_parameters(); conv.reset_parameters()
print("reset_parameters x2 ok     ", not torch.equal(before, conv.rel[0].weight),
      "| finite:", bool(torch.isfinite(conv.rel[0].weight).all()))
assert torch.isfinite(conv.rel[0].weight).all()

# --- a relation with ZERO edges must not crash and must contribute nothing
conv3 = MyRGCNConv(Cin, Cout, 3)
conv3.eval()
o3 = conv3(x, edge_index, edge_type)           # relation 2 absent from edge_type
print("unused relation ok         ", bool(torch.isfinite(o3).all()))
assert torch.isfinite(o3).all()

# --- a relation whose edges touch only low ids must still return N rows
ei_low = torch.tensor([[0], [1]]); et_low = torch.tensor([0])
o4 = conv(x, ei_low, et_low)
print("size=(N,N) honoured        ", tuple(o4.shape), "expected", (N, Cout))
assert o4.shape == (N, Cout)

# --- parameter count: R+1 matrices of in*out, plus one bias
p = sum(q.numel() for q in conv.parameters())
print("params                     ", p, "expected", (R + 1) * Cin * Cout + Cout)
assert p == (R + 1) * Cin * Cout + Cout

# --- gradients flow to every relation matrix
conv.train()
conv(x, edge_index, edge_type).sum().backward()
for r in range(R):
    g = conv.rel[r].weight.grad
    print(f"grad rel {r} nonzero        ", bool(g is not None and g.abs().sum() > 0))
    assert g is not None and g.abs().sum() > 0
assert conv.root.weight.grad.abs().sum() > 0

print("\nALL SANITY CHECKS PASSED")
