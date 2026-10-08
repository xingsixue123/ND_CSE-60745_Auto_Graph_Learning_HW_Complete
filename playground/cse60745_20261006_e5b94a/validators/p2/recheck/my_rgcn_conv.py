class MyRGCNConv(MessagePassing):
    """R-GCN: one weight matrix per relation, plus a self-connection."""

    def __init__(self, in_channels, out_channels, num_relations):
        # aggr="mean" IS the 1/c_{i,r} of the formula, taking
        # c_{i,r} = |N_r(i)|: the example Schlichtkrull et al.'s Eq. (2)
        # itself offers. PyG's mean is 0, not NaN, when |N_r(i)| = 0, so
        # no empty neighbourhood needs a special case.
        super().__init__(aggr="mean")
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_relations = num_relations
        self.root = nn.Linear(in_channels, out_channels, bias=True)  # W_0
        # W_r: one full [in, out] matrix per relation. Basic R-GCN, so
        # neither basis nor block-diagonal decomposition.
        self.rel = nn.ModuleList([
            nn.Linear(in_channels, out_channels, bias=False)
            for _ in range(num_relations)])
        self.reset_parameters()

    def reset_parameters(self):
        # Safe to call twice, and the harness does call it twice.
        super().reset_parameters()
        self.root.reset_parameters()
        for lin in self.rel:
            lin.reset_parameters()

    def forward(self, x, edge_index, edge_type):
        out = self.root(x)                             # W_0 h_i
        n = x.size(self.node_dim)
        for r in range(self.num_relations):
            ei_r = edge_index[:, edge_type == r]       # relation r only
            if ei_r.size(1) == 0:
                continue
            # c_{i,r} does not depend on j and W_r is linear, so
            # sum_j (1/c_{i,r}) W_r h_j == W_r (mean_j h_j): transform
            # first, propagate second. size=(n, n) keeps the result at the
            # full node count where relation r touches only some nodes.
            out = out + self.propagate(ei_r, x=self.rel[r](x), size=(n, n))
        return out

    def message(self, x_j):
        return x_j
