
#### notebook cell 12 (markdown) — verbatim

```markdown
---

## Question 1 — Absolute and relative structural encodings

A transformer treats its input as a set: without help it cannot see the graph at all.
Structural encodings put the graph back in, in two ways — **absolute** encodings describe each
node on its own and are added to its input, **relative** encodings describe each node pair and
bias the attention between them. Following the demo, implement one of each.

- **`LapPETransformer` — Laplacian positional encoding (absolute).** Use the eigenvectors of
  the symmetric normalised Laplacian $L = I - D^{-1/2} A D^{-1/2}$ as node positions: row $i$
  of the `LAP_K` eigenvectors with the smallest non-trivial eigenvalues is the encoding of
  node $i$.
- **`SPDAttention` — shortest-path distance (relative).** Use the hop distance between two
  nodes as in Graphormer: every distance gets one learnable scalar per head, added to the
  attention score.

$$\text{score}_{ij} = \frac{q_i^\top k_j}{\sqrt{d}} + b_{\,\mathrm{SPD}(i,j)}$$
```

#### notebook cell 13 (code) — verbatim

```python
# TODO Q1: implement precompute and inject_absolute of LapPETransformer, and precompute and
# forward of SPDAttention.


class LapPETransformer(GraphTransformer):
    """Absolute encoding: Laplacian eigenvectors, added to the input once.

    Constructed like the demo's CentralityTransformer, e.g.
    LapPETransformer(attention_cls=SPDAttention). All arguments go to GraphTransformer:
      attention_cls  : attention class used in every block (Attention, CNAttention, SPDAttention, ...)
      dim            : size of the node states (default 64)
      heads          : number of attention heads (default 4)
      layers         : number of transformer blocks (default 4)
      out_dim        : size of the prediction (1 for ZINC)
      num_atom_types : size of the atom-type embedding (21 for ZINC, 0 for no node features)
      graph_level    : True to predict one value per graph, False for one per node

    Inherited attributes you can use: self.dim, self.attention_cls.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Linear map from the LAP_K eigenvector entries of a node to a node vector of size dim.
        self.lap_proj = nn.Linear(LAP_K, self.dim)

    @staticmethod
    def precompute(edge_index, num_nodes):
        """Raw absolute encoding of one graph, computed once and cached by the framework.

        edge_index : long [2, E], every undirected edge listed in both directions
        num_nodes  : int, number of nodes of this graph
        Returns a dict of node-level tensors, e.g. {"lap": float tensor [num_nodes, LAP_K]}.
        The key is your choice: inject_absolute reads the batched tensor back as batch[key].
        """
        raise NotImplementedError

    def inject_absolute(self, h, batch):
        """Add the absolute encoding to the input node states, once, before the first block.

        h     : [num_nodes, dim], the atom embeddings of all graphs in the batch, concatenated
        batch : dict; batch["lap"] (or your key) is [num_nodes, LAP_K], the precompute output
                of all graphs concatenated in the same node order as h. batch["batch"] gives the
                graph id of every node. self.training tells whether the model is training.
        Returns [num_nodes, dim].
        """
        raise NotImplementedError


class SPDAttention(Attention):
    """Relative encoding: shortest-path distance, one learnable bias per head.

    Constructed by GraphTransformer as attention_cls(dim, heads), once per block.
      dim      : size of the node states
      heads    : number of attention heads; each head has size dim // heads
      max_dist : distances larger than this share one bias

    Inherited from Attention: self.heads, self.qkv (nn.Linear(dim, 3 * dim), producing queries,
    keys and values) and self.out (nn.Linear(dim, dim), the output projection).
    Attention.forward and CNAttention.forward show the full computation.
    """

    def __init__(self, dim, heads, max_dist=8):
        super().__init__(dim, heads)
        self.max_dist = max_dist
        # one bias per head for each distance 0..max_dist, plus one for unreachable pairs
        self.spd_table = nn.Embedding(max_dist + 2, heads)

    @staticmethod
    def precompute(edge_index, num_nodes):
        """Raw relative encoding of one graph, computed once and cached by the framework.

        edge_index : long [2, E], every undirected edge listed in both directions
        num_nodes  : int, number of nodes of this graph
        Returns a dict of pair-level tensors, e.g. {"spd": long tensor [num_nodes, num_nodes]}
        where entry [i, j] is the hop distance from i to j. The key is your choice: forward
        reads the batched tensor back as enc[key].
        """
        raise NotImplementedError

    def forward(self, h, enc, mask):
        """Multi-head attention among the nodes of each graph, with the SPD bias.

        h    : [B, N, dim], node states of the B graphs in the batch, padded to N nodes
        enc  : dict; enc["spd"] (or your key) is [B, N, N], your precompute output padded with
               0 outside each graph; entry [b, i, j] concerns node i attending to node j
        mask : [B, N] bool, True for real nodes and False for padding
        Returns [B, N, dim].
        """
        raise NotImplementedError
```

#### notebook cell 14 (code) — verbatim

```python
run_graph_task("LapPE + SPD", LapPETransformer(attention_cls=SPDAttention))
```

#### notebook cell 15 (markdown) — verbatim

```markdown
---

## Question 2 — Efficient graph transformer

Full attention compares every node with every other node: $N^2$ pairs per graph. On ZINC
that is a few hundred pairs; on LastFM it is 58 million.

An efficient graph transformer lets each node attend to a **chosen set of pairs** only. Build it
on your Q1 solution: `SparseSPDAttention` subclasses your `SPDAttention`, so its parameters and
its `precompute` (the shortest-path distances) are inherited, and runs inside your
`LapPETransformer` unchanged. Two things are new:

- `attention_pairs` chooses which pairs attend to each other in one graph. Node ids from
  `num_nodes` upwards are **virtual nodes**: extra tokens with a learnable start state that are
  not part of the graph and are left out of the prediction.
- `forward` computes attention on those pairs only. Node states are no longer padded per
  graph: `h` is `[num_nodes, dim]` for the whole batch, and the shortest-path distance of every
  pair arrives as `enc["spd"]`, one value per pair. The framework also labels every pair as a
  self loop, a graph edge, a pair with a virtual node, or another pair, in `enc["pair_type"]`
  (indices into `PAIR_TYPES`).

You may reproduce Exphormer or develop your own efficient graph transformer.
```

#### notebook cell 16 (code) — verbatim

```python
PAIR_TYPES = ("self", "edge", "virtual", "other")     # labels the framework gives attention pairs


def pair_types(pairs, edge_index, num_nodes):
    """Label every pair: a virtual node at either end, a self loop, a graph edge, or other."""
    src, dst = pairs
    total = max(num_nodes, int(pairs.max()) + 1 if pairs.numel() else 0)   # ids that can occur
    is_edge = torch.isin(src * total + dst, edge_index[0] * total + edge_index[1])
    t = torch.full_like(src, PAIR_TYPES.index("other"))
    t[is_edge] = PAIR_TYPES.index("edge")
    t[src == dst] = PAIR_TYPES.index("self")
    t[(src >= num_nodes) | (dst >= num_nodes)] = PAIR_TYPES.index("virtual")
    return t


class SparseSPDAttention(SPDAttention):
    """Your Q1 attention, restricted to a chosen set of node pairs."""

    @staticmethod
    def attention_pairs(edge_index, num_nodes):
        """Choose which node pairs attend to each other in one graph.

        Returns a long tensor [2, P]: column (j, i) means node i attends to node j.
        Ids 0..num_nodes-1 are the graph's nodes; ids num_nodes, num_nodes+1, ... are
        virtual nodes.
        """
        # TODO Q2: implement attention_pairs and forward.
        raise NotImplementedError

    def forward(self, h, enc, pairs):
        """h     : [num_nodes, dim], node states of all graphs in the batch
        enc   : dict of per-pair features, each [P]: enc["spd"] from your precompute
                (0 for pairs with a virtual node) and enc["pair_type"] for type of node pairs.
        pairs : [2, P], the attention pairs of the whole batch, with global node ids
        Returns [num_nodes, dim].
        
        Note: You may use torch_geometric.utils.segment_attention for sparse attention computation, 
        which is already imported in the code.
        """
        raise NotImplementedError
```

#### notebook cell 17 (markdown) — verbatim

```markdown
First ZINC, for accuracy. Then LastFM: one training step of full attention and of your
pairs, side by side, and finally your model trained for country classification.
```

#### notebook cell 18 (code) — verbatim

```python
run_graph_task("sparse: LapPE + SPD", LapPETransformer(attention_cls=SparseSPDAttention))
```

#### notebook cell 19 (code) — verbatim

```python
def lastfm_model(attention_cls):
    return LapPETransformer(attention_cls=attention_cls, dim=32, heads=2, layers=2,
                            out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


benchmark_step("full: LapPE + SPD", lastfm_model(SPDAttention))
benchmark_step("sparse: LapPE + SPD", lastfm_model(SparseSPDAttention))
run_node_task("sparse: LapPE + SPD", lastfm_model(SparseSPDAttention))
```
