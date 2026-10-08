"""Validator's OWN brute-force reference for the R-GCN formula, written from the
notebook's equation alone, then compared against the delivered MyRGCNConv source
(loaded by AST out of rgcn_run.py so it is the exact delivered text)."""
import ast, pathlib, torch, torch.nn as nn
from torch_geometric.nn import MessagePassing

src = pathlib.Path("rgcn_run.py").read_text()
tree = ast.parse(src)
cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "MyRGCNConv")
ns = {"MessagePassing": MessagePassing, "nn": nn, "torch": torch}
exec(compile(ast.Module(body=[cls], type_ignores=[]), "<delivered>", "exec"), ns)
MyRGCNConv = ns["MyRGCNConv"]

def reference(layer, x, edge_index, edge_type, R):
    """h_i' = W_0 h_i + sum_r sum_{j in N_r(i)} (1/c_{i,r}) W_r h_j, c_{i,r}=|N_r(i)|.
    Pure python loops, no PyG. N_r(i) = sources j with edge j->i of type r."""
    N = x.size(0)
    W0, b0 = layer.root.weight, layer.root.bias
    out = x @ W0.T + b0
    for r in range(R):
        Wr = layer.rel[r].weight
        for i in range(N):
            nbrs = [int(edge_index[0, e]) for e in range(edge_index.size(1))
                    if int(edge_index[1, e]) == i and int(edge_type[e]) == r]
            if not nbrs:            # |N_r(i)| = 0 -> the term must vanish, not NaN
                continue
            acc = torch.zeros(x.size(1))
            for j in nbrs:
                acc = acc + x[j]
            out[i] = out[i] + (Wr @ (acc / len(nbrs)))
    return out

torch.manual_seed(7)
N, C, O, R = 9, 5, 4, 3
x = torch.randn(N, C)
# deliberately include: multi-edges, a node with 0 in-degree in every relation (node 8),
# a relation with no edges at all for some targets, and self-referencing structure
ei = torch.tensor([[0,1,2,3,4,0,1,2,5,6,7,3,4,5,0],
                   [1,2,3,4,0,2,3,4,6,7,5,1,2,0,3]])
et = torch.tensor([0,0,0,0,0,1,1,1,1,1,1,2,2,2,2])

layer = MyRGCNConv(C, O, R)
layer.eval()
with torch.no_grad():
    got = layer(x, ei, et)
    ref = reference(layer, x, ei, et, R)
d = (got - ref).abs().max().item()
print(f"shape {tuple(got.shape)} expected {(N,O)}")
print(f"max |delivered - validator reference| = {d:.3e}")
print("NaN/Inf present:", bool(torch.isnan(got).any() or torch.isinf(got).any()))

# node 8 has no incoming edge of any relation -> must be exactly W_0 h_8
w0 = x[8] @ layer.root.weight.T + layer.root.bias
print("isolated node 8 == W_0 h_8:", torch.allclose(got[8], w0, atol=1e-6))

# parameter count: (R+1)*C*O + O   (one bias, on the root only)
want = (R+1)*C*O + O
print(f"params {sum(p.numel() for p in layer.parameters())} expected {want}")

# the per-relation mean really is a MEAN: scale one relation's edges by duplication
print("\n-- duplication test (mean must be invariant to duplicating every edge) --")
ei2 = torch.cat([ei, ei], 1); et2 = torch.cat([et, et])
with torch.no_grad():
    got2 = layer(x, ei2, et2)
print("mean-invariance under edge duplication:", torch.allclose(got, got2, atol=1e-5),
      f"(max diff {(got-got2).abs().max().item():.3e})")

print("\nREFERENCE AGREEMENT:", "PASS" if d < 1e-5 else "FAIL")
