"""Ablation variants of HybridGTLayer, used only for the experiments in the report.
Each one changes exactly one thing; everything else is inherited from HybridGTLayer.
"""
from hybrid_layer import HybridGTLayer, HybridGT
from gt_framework import *


class LocalOnlyLayer(HybridGTLayer):
    """Global attention branch removed: message passing only."""
    def forward(self, x, edge_index, edge_attr, batch):
        h = self.norm_local(x + self.local_branch(x, edge_index, edge_attr))
        return self.norm_ffn(h + self.ffn(h))


class GlobalOnlyLayer(HybridGTLayer):
    """Message-passing branch removed: global attention only."""
    def forward(self, x, edge_index, edge_attr, batch):
        h = self.norm_global(x + self.global_branch(x, batch))
        return self.norm_ffn(h + self.ffn(h))


class SequentialLayer(HybridGTLayer):
    """Same two branches, stacked instead of summed: attention reads the MPNN output."""
    def forward(self, x, edge_index, edge_attr, batch):
        h = self.norm_local(x + self.local_branch(x, edge_index, edge_attr))
        h = self.norm_global(h + self.global_branch(h, batch))
        return self.norm_ffn(h + self.ffn(h))


class GatedLayer(HybridGTLayer):
    """Same two branches, combined by a learned per-node, per-channel gate."""
    def __init__(self, dim, heads, num_bond_types=4):
        super().__init__(dim, heads, num_bond_types)
        self.gate = nn.Linear(2 * dim, dim)

    def forward(self, x, edge_index, edge_attr, batch):
        h_local = self.norm_local(x + self.local_branch(x, edge_index, edge_attr))
        h_global = self.norm_global(x + self.global_branch(x, batch))
        g = torch.sigmoid(self.gate(torch.cat([h_local, h_global], dim=-1)))
        h = g * h_local + (1 - g) * h_global
        return self.norm_ffn(h + self.ffn(h))


class AblationGT(HybridGT):
    """Cell 22's HybridGT with its layer class swapped. The submodule registration
    order (atom, degree_table, layers, norm, head) is unchanged, so _reset gives the
    shared parameters exactly the same seeded initialisation as HybridGT()."""
    def __init__(self, layer_cls, dim=64, heads=4, layers=4, **kw):
        super().__init__(dim=dim, heads=heads, layers=layers, **kw)
        self.layers = nn.ModuleList([layer_cls(dim, heads) for _ in range(layers)])
