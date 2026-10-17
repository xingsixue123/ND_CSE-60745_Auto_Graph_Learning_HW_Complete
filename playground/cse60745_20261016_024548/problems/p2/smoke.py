import torch, time
torch.set_num_threads(4)
from hybrid_layer import HybridGTLayer, HybridGT
from gt_framework import *

# --- sanity 1: shapes and a forward/backward on one real ZINC batch ---
m = HybridGT()
graphs = ZINC_GRAPHS["train"][:8]
ensure_precomputed(graphs, [HybridGT.precompute])
b = make_batch(graphs, HybridGT.precompute)
print("batch keys:", sorted(b.keys()))
print("x", b["x"].shape, "edge_index", b["edge_index"].shape, "edge_attr", b["edge_attr"].shape,
      "unique bond ids", sorted(set(b["edge_attr"].tolist())), "virtual any?", bool(b["virtual"].any()))
out = m(b)
print("model out", out.shape, "finite", bool(torch.isfinite(out).all()))
out.sum().backward()
nog = [n for n, p in m.named_parameters() if p.grad is None]
print("params with no grad:", nog)
print("n params:", sum(p.numel() for p in m.parameters()))
