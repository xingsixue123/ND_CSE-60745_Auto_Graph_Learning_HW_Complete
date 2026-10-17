import torch
from gt_framework import *
from hybrid_layer import HybridGTLayer, HybridGT
import torch.nn as nn
def np_(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)
print("plain      :", np_(GraphTransformer()))
print("demo       :", np_(CentralityTransformer(attention_cls=CNAttention)))
print("HybridGT   :", np_(HybridGT()))

# ablations as described: global branch removed / local branch removed
class LocalOnly(HybridGTLayer):
    def forward(self, x, edge_index, edge_attr, batch):
        local = self.local_branch(x, edge_index, edge_attr)
        h = self.norm_local(x + local)
        return self.norm_ffn(h + self.ffn(h))
class GlobalOnly(HybridGTLayer):
    def forward(self, x, edge_index, edge_attr, batch):
        glob = self.global_branch(x, batch)
        h = self.norm_global(x + glob)
        return self.norm_ffn(h + self.ffn(h))
def count_used(cls):
    import copy
    class GT(HybridGT):
        def __init__(s, **kw):
            super().__init__(**kw)
            s.layers = nn.ModuleList([cls(64,4) for _ in range(4)])
    m = GT()
    g = ZINC_GRAPHS["train"][:4]
    ensure_precomputed(g, [HybridGT.precompute])
    b = make_batch(g, HybridGT.precompute)
    m(b).sum().backward()
    return sum(p.numel() for p in m.parameters() if p.grad is not None and p.grad.abs().sum()>=0 and p.requires_grad and p.grad is not None)
print("local-only (params receiving grad) :", count_used(LocalOnly))
print("global-only(params receiving grad) :", count_used(GlobalOnly))
