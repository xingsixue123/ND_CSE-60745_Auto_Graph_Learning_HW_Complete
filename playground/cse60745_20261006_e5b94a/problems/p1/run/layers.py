"""Q1, Q2, Q3 and Q5 of CSE 60745 HW3-Part(A): the four MessagePassing subclasses.

Every reset_parameters() is safe to call twice: GNNLinkPredictor (notebook cell 11)
calls it again after construction, and __init__ already called it once.
"""

import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import (add_self_loops, degree, remove_self_loops,
                                   softmax)


# ------------------------------------------------------------------ Q1: GCN

class MyGCNConv(MessagePassing):
    """GCN: h_i' = sum_{j in N(i) u {i}} (d_i d_j)^{-1/2} W h_j + b."""

    def __init__(self, in_channels, out_channels):
        # "add": the 1/sqrt(d_i d_j) coefficient is the normaliser, so the reduction
        # must be a plain sum -- "mean" would divide by the degree a second time.
        super().__init__(aggr="add")
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.lin = nn.Linear(in_channels, out_channels, bias=False)
        self.bias = nn.Parameter(torch.empty(out_channels))
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.lin.reset_parameters()
        nn.init.zeros_(self.bias)

    def forward(self, x, edge_index):
        # Closed neighbourhood A_hat = A + I. Removing first makes d_hat correct even
        # if edge_index already carries self-loops.
        edge_index, _ = remove_self_loops(edge_index)
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        src, dst = edge_index[0], edge_index[1]            # message src -> dst
        deg_inv_sqrt = degree(dst, x.size(0), dtype=x.dtype).pow(-0.5)
        norm = deg_inv_sqrt[src] * deg_inv_sqrt[dst]       # [E]; d_hat >= 1 after loops

        out = self.propagate(edge_index, x=self.lin(x), norm=norm)
        return out + self.bias

    def message(self, x_j, norm):
        return norm.view(-1, 1) * x_j


# ------------------------------------------------------------------ Q2: GAT

class MyGATConv(MessagePassing):
    """GAT: alpha_ij = softmax over j of LeakyReLU(a . [W h_i || W h_j])."""

    def __init__(self, in_channels, out_channels, heads=8, concat=True,
                 negative_slope=0.2):
        # node_dim=0: propagate carries [N, heads, channels], so the node axis is 0,
        # not the default -2 (which would be the head axis here).
        super().__init__(aggr="add", node_dim=0)
        self.in_channels = in_channels
        self.out_channels = out_channels
        # Concatenated heads must together be out_channels wide, since the next layer
        # is built with in_channels = out_channels.
        if concat and out_channels % heads != 0:
            heads = 1
        self.heads = heads
        self.concat = concat
        self.head_channels = out_channels // heads if concat else out_channels
        self.negative_slope = negative_slope

        self.lin = nn.Linear(in_channels, heads * self.head_channels, bias=False)
        # a = [a_dst || a_src], split so the edge score is a sum of two node terms.
        self.att_src = nn.Parameter(torch.empty(1, heads, self.head_channels))
        self.att_dst = nn.Parameter(torch.empty(1, heads, self.head_channels))
        self.bias = nn.Parameter(torch.empty(out_channels))
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.lin.reset_parameters()
        nn.init.xavier_uniform_(self.att_src)
        nn.init.xavier_uniform_(self.att_dst)
        nn.init.zeros_(self.bias)

    def forward(self, x, edge_index):
        n = x.size(0)
        # The softmax denominator runs over N(i) u {i}, as in the GAT paper.
        edge_index, _ = remove_self_loops(edge_index)
        edge_index, _ = add_self_loops(edge_index, num_nodes=n)

        h = self.lin(x).view(n, self.heads, self.head_channels)
        out = self.propagate(edge_index, h=h)              # [N, heads, head_channels]
        out = out.flatten(1) if self.concat else out.mean(dim=1)
        return out + self.bias

    def message(self, h_j, h_i, index, size_i):
        # a^T [W h_i || W h_j] = a_dst . W h_i + a_src . W h_j.
        e = (h_i * self.att_dst).sum(-1) + (h_j * self.att_src).sum(-1)   # [E, heads]
        alpha = softmax(F.leaky_relu(e, self.negative_slope), index, num_nodes=size_i)
        return h_j * alpha.unsqueeze(-1)


# ------------------------------------------------------------------ Q3: GIN

class MyGINConv(MessagePassing):
    """GIN: h_i' = MLP((1 + eps) h_i + sum_{j in N(i)} h_j)."""

    def __init__(self, in_channels, out_channels):
        super().__init__(aggr="add")           # sum is the injective multiset aggregator
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.eps = nn.Parameter(torch.empty(1))
        self.mlp = nn.Sequential(
            nn.Linear(in_channels, out_channels),
            nn.BatchNorm1d(out_channels),
            nn.ReLU(),
            nn.Linear(out_channels, out_channels),
        )
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        for layer in self.mlp:                 # nn.Sequential has no reset_parameters
            if hasattr(layer, "reset_parameters"):
                layer.reset_parameters()
        nn.init.zeros_(self.eps)

    def forward(self, x, edge_index):
        # Open neighbourhood: (1 + eps) h_i is already the self term, so a self-loop
        # would count the node twice.
        edge_index, _ = remove_self_loops(edge_index)
        agg = self.propagate(edge_index, x=x)
        return self.mlp((1 + self.eps) * x + agg)

    def message(self, x_j):
        return x_j


# ------------------------------------------------- Q5: 8 hops, one message-passing layer

class MyDeepConv(MessagePassing):
    """APPNP-style decoupled propagation: transform once, then K personalised-PageRank
    steps. One layer reaches K hops, so K=8 gives an 8-hop receptive field at n_layers=1.
    """

    def __init__(self, in_channels, out_channels, K=8, alpha=0.3):
        super().__init__(aggr="add")
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.K = K            # propagation steps = hops: K=8 at n_layers=1 is 8 hops
        self.alpha = alpha    # teleport probability, chosen on validation MRR
        self.lin1 = nn.Linear(in_channels, out_channels)
        self.lin2 = nn.Linear(out_channels, out_channels)
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.lin1.reset_parameters()
        self.lin2.reset_parameters()

    def forward(self, x, edge_index):
        edge_index, _ = remove_self_loops(edge_index)
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))
        src, dst = edge_index[0], edge_index[1]
        deg_inv_sqrt = degree(dst, x.size(0), dtype=x.dtype).pow(-0.5)
        norm = deg_inv_sqrt[src] * deg_inv_sqrt[dst]

        # Prediction first: all the parameters live here, none in the propagation,
        # so the hop count K is free of parameters and cannot overfit with depth.
        h = self.lin2(F.relu(self.lin1(x)))

        # Z <- (1 - alpha) A_hat Z + alpha H, K times: personalised PageRank with
        # restart to H, so the node's own features are re-injected at every hop.
        z = h
        for _ in range(self.K):
            z = (1 - self.alpha) * self.propagate(edge_index, x=z, norm=norm) \
                + self.alpha * h
        return z

    def message(self, x_j, norm):
        return norm.view(-1, 1) * x_j
