"""Q3: HybridGTLayer, plus notebook cell 22's HybridGT copied verbatim.

The HybridGTLayer source below is what appears in answer.tex.
"""
from gt_framework import *   # torch, nn, F, math, to_dense_batch, graph_mean_pool, ...


class HybridGTLayer(nn.Module):
    """One GraphGPS-style hybrid layer: a local message-passing branch and a
    global self-attention branch, run in parallel on the same input and summed.
    """

    def __init__(self, dim, heads, num_bond_types=4):
        super().__init__()
        self.dim, self.heads = dim, heads
        # local branch: GINE message passing
        self.bond = nn.Embedding(num_bond_types, dim)
        self.eps = nn.Parameter(torch.zeros(1))
        self.mpnn = nn.Sequential(nn.Linear(dim, 2 * dim), nn.ReLU(),
                                  nn.Linear(2 * dim, dim))
        # global branch: multi-head self attention inside each graph
        self.qkv = nn.Linear(dim, 3 * dim)
        self.proj = nn.Linear(dim, dim)
        # fusion
        self.norm_local = nn.LayerNorm(dim)
        self.norm_global = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(nn.Linear(dim, 2 * dim), nn.ReLU(),
                                 nn.Linear(2 * dim, dim))
        self.norm_ffn = nn.LayerNorm(dim)

    def local_branch(self, x, edge_index, edge_attr):
        """GINE: every message carries its bond type, neighbours are summed."""
        src, dst = edge_index
        msg = F.relu(x[src] + self.bond(edge_attr))        # [E, dim]
        agg = torch.zeros_like(x).index_add_(0, dst, msg)  # [num_nodes, dim]
        return self.mpnn((1 + self.eps) * x + agg)

    def global_branch(self, x, batch):
        """Self attention; the padding mask keeps it inside a single graph."""
        h, mask = to_dense_batch(x, batch)          # [B, N, dim], [B, N]
        B, N, D = h.shape
        qkv = self.qkv(h).view(B, N, 3, self.heads, D // self.heads)
        q, k, v = qkv.permute(2, 0, 3, 1, 4)        # each [B, heads, N, D/heads]
        scores = q @ k.transpose(-1, -2) / math.sqrt(D // self.heads)
        scores = scores.masked_fill(~mask[:, None, None, :], float("-inf"))
        weights = torch.softmax(scores, dim=-1).nan_to_num(0.0)
        out = (weights @ v).transpose(1, 2).reshape(B, N, D)
        return self.proj(out)[mask]                 # back to [num_nodes, dim]

    def forward(self, x, edge_index, edge_attr, batch):
        """x          : [num_nodes, dim], node states of the whole batch
        edge_index : [2, E]
        edge_attr  : [E], bond type ids in [0, 4)
        batch      : [num_nodes], graph id of every node
        Returns new node states [num_nodes, dim]."""
        local = self.local_branch(x, edge_index, edge_attr)
        glob = self.global_branch(x, batch)
        h = self.norm_local(x + local) + self.norm_global(x + glob)
        return self.norm_ffn(h + self.ffn(h))


class HybridGT(nn.Module):
    """Stack of HybridGTLayer. Absolute encoding: degree centrality, as in the demo."""

    def __init__(self, dim=64, heads=4, layers=4, num_atom_types=21, max_degree=64):
        super().__init__()
        self.max_degree = max_degree
        self.atom = nn.Embedding(num_atom_types, dim)
        self.degree_table = nn.Embedding(max_degree + 1, dim)
        self.layers = nn.ModuleList([HybridGTLayer(dim, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Sequential(nn.Linear(dim, dim), nn.ReLU(), nn.Linear(dim, 1))

    precompute = staticmethod(CentralityTransformer.precompute)

    def forward(self, batch):
        h = self.atom(batch["x"]) + self.degree_table(batch["deg"].clamp(max=self.max_degree))
        for layer in self.layers:
            h = layer(h, batch["edge_index"], batch["edge_attr"], batch["batch"])
        return self.head(graph_mean_pool(self.norm(h), batch["batch"], ~batch["virtual"]))
