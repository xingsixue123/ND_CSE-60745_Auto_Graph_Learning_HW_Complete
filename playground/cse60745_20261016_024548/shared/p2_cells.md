
#### notebook cell 20 (markdown) — verbatim

```markdown
---

## Question 3 — Hybrid graph transformer

Message passing sees the graph's edges but only a node's neighbourhood; attention sees every
node but not the edges. A hybrid layer, as in GraphGPS, combines a local message-passing
branch with a global attention branch.

Implement `HybridGTLayer` from scratch: its parameters, how the two branches are built and
how they are combined. It must accept `__init__(dim, heads)` and
`forward(x, edge_index, edge_attr, batch)`, returning new node states of the same shape.

- `x` : `[num_nodes, dim]`, the node states of all graphs in the batch, concatenated
- `edge_index` : `[2, E]`
- `edge_attr` : `[E]`, bond type ids in `[0, 4)`
- `batch` : `[num_nodes]`, the graph id of every node
```

#### notebook cell 21 (code) — verbatim

```python
class HybridGTLayer(nn.Module):
    # TODO Q3: implement the whole module.

    def __init__(self, dim, heads):
        super().__init__()
        raise NotImplementedError

    def forward(self, x, edge_index, edge_attr, batch):
        """x          : [num_nodes, dim], node states of all graphs in the batch
        edge_index : [2, E]
        edge_attr  : [E], bond type ids in [0, 4)
        batch      : [num_nodes], graph id of every node
        Returns new node states [num_nodes, dim]."""
        raise NotImplementedError
```

#### notebook cell 22 (code) — verbatim

```python
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


run_graph_task("hybrid GT", HybridGT())
```
