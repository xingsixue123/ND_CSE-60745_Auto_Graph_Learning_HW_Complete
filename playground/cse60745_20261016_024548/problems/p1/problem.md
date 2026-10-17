# Problem p1 — Q1 Structural Encoding (20 pts) + Q2 Efficient Graph Transformer (20 pts)

**Problem id: `p1`.** Namespace every LaTeX label, every figure filename and every macro
you define with `p1:` / `fig_p1_` (rule R5 below).

These two questions are one problem because the notebook makes Q2 a subclass of Q1:
`class SparseSPDAttention(SPDAttention)` (cell 16), run as
`LapPETransformer(attention_cls=SparseSPDAttention)` (cell 18). Q2 inherits Q1's
parameters, Q1's `precompute` and Q1's absolute encoding. Answer them as one coherent
implementation.

---

## 1. Where this comes from

Assignment document: `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3(B).doc`

Ingested at `INGEST/pages/CSE 60745_Fall 2026_HW3(B)/` — **rendered page 2** (page 1 is
the cover page). Anchor text: `Q1: Structural Encoding in Graph Transformer (20 pts)`.

The document has **no figures**. Both rendered pages contain exactly one image, the Notre
Dame monogram in the running header; I read both page PNGs and confirmed it. Nothing in
this problem depends on an image, so there is no figure file you need to open. The text
channel and the page image agree verbatim.

### Assignment text, transcribed verbatim from rendered page 2

> \* This assignment contains 70 points. You are encouraged to finish independently. Any
> submitted work that it copied from any source or too similar to be an independent
> write-up will not be given credit. Please submit this homework (as a PDF or Word file
> including the cover page) to ND Canvas by **11:59pm on Monday, 10/26/2026**.
>
> In this assignment, you will practice the implementation of basic graph transformers.
> Please use Google Colab for experiments and **submit only your implemented code file**.
> Useful papers for this assignment are listed as follows:
>
> [1] Chen, Dexiong, Leslie O'Bray, and Karsten Borgwardt. "Structure-aware transformer for
> graph representation learning." In ICML 2022.
> [2] Ying, Chengxuan, Tianle Cai, Shengjie Luo, Shuxin Zheng, Guolin Ke, Di He, Yanming
> Shen, and Tie-Yan Liu. "Do transformers really perform badly for graph representation?."
> In NeurIPS 2021.
> [3] Shirzad, Hamed, Ameya Velingker, Balaji Venkatachalam, Danica J. Sutherland, and Ali
> Kemal Sinop. "Exphormer: Sparse transformers for graphs." In ICML 2023.
> [4] Rampášek, Ladislav, Michael Galkin, Vijay Prakash Dwivedi, Anh Tuan Luu, Guy Wolf,
> and Dominique Beaini. "Recipe for a general, powerful, scalable graph transformer." In
> NeurIPS 2022.
> [5] Wu, Qitian, Wentao Zhao, Chenxiao Yang, Hengrui Zhang, Fan Nie, Haitian Jiang, Yatao
> Bian, and Junchi Yan. "Sgformer: Simplifying and empowering transformers for large-graph
> representations." In NeurIPS 2023.
>
> **Q1: Structural Encoding in Graph Transformer (20 pts)**
> Complete LapPETransformer() and SPDAttention() to implement graph Laplacian absolute
> structural encoding and shortest path distance-based relative structural encoding in graph
> transformer. You may refer to the demo in Section 4 for implementation ideas.
>
> **Q2: Efficient Graph Transformer (20 pts)**
> Complete SparseSPDAttention() to implement attention mask for sparse graph attention. You
> only need to specify the node pairs used for attention in your implementation. It is
> encouraged to test different masking strategies.

(Q3 is on the same page and belongs to a different worker. Do not answer it.)

## 2. The real question is in the notebook

Second input file, **read it**:
`/home/xing/project/auto_hw_complete/input/task6_graph_transformer-1.ipynb`

It is also ingested as plain text at
`INGEST/pages/task6_graph_transformer-1/alltext.txt` (22 cells; the notebook has no
stored outputs and no embedded images, so that text is the complete notebook).

"The demo in Section 4" that Q1 points you at is notebook cells 10-11:
`CentralityTransformer` (absolute encoding) and `CNAttention` (relative encoding). Read
them; they are the template for both of your Q1 classes.

Below are the question cells **verbatim**. The TODO cells are the signatures you must
match exactly — the framework calls them by name.

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

---

## 3. A working environment is already built for you

There is no GPU on this machine (`nvidia-smi` fails). 32 CPUs, 125 GB RAM. Everything
below was built and smoke-tested by the master before you were spawned.

**Interpreter** (read-only to you, but you only need to run it — do not pip-install into it):

    /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/.venv-gt/bin/python

It has torch 2.14.1+cpu, torch_geometric 2.8.1, pandas, scipy, scikit-learn, numpy.

**Shared directory** (read-only to you):

    /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/shared/
        gt_framework.py       the notebook's framework code, extracted verbatim
        data/zinc/            the ZINC subset, already downloaded and processed
        data/task2/, data/task3/   the three LastFM CSVs, already downloaded

**First thing to do — copy it into your own playground and work there:**

    cp -r /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/shared/gt_framework.py .
    cp -r /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/shared/data .

`gt_framework.py` loads the datasets at import time with relative paths (`data/zinc`,
`data/task2/...`), so run from a directory that has `data/` in it.

`gt_framework.py` is notebook cells 3, 5, 7, 8, 9 in full, plus the two demo classes of
cell 11 and `PAIR_TYPES`/`pair_types` from cell 16. It deliberately contains **no**
answer: the TODO cells are not in it. Write your classes in your own file:

    from gt_framework import *
    class LapPETransformer(GraphTransformer): ...

Do not edit `gt_framework.py`'s content in your own copy. If you think the given
framework is wrong, say so in `submission.md` rather than silently changing it.

**Measured timings** (so you can plan): the demo
`run_graph_task("demo", CentralityTransformer(attention_cls=CNAttention))` runs at
**4.5 s/epoch**, i.e. a full 30-epoch ZINC run takes about 2.5 minutes. Real experiments
are cheap here. Your worker round has a 2-hour budget.

### Traps the master already hit, so you do not have to

1. **`torch_geometric.utils.segment_attention` does not exist.** The Q2 docstring in cell
   16 says "You may use torch_geometric.utils.segment_attention for sparse attention
   computation, which is already imported in the code". It is not, and PyG 2.8.1 has no
   such function (`hasattr(torch_geometric.utils, "segment_attention")` is `False`). What
   cell 3 *actually* imports is
   `from torch_geometric.utils import ... softmax as segment_softmax ...`, i.e. PyG's
   **segment softmax** — `segment_softmax(src, index, num_nodes=...)` softmaxes `src`
   within each group given by `index`. That is the helper to use for the sparse attention
   in Q2. Note this discrepancy in your answer in one sentence; it is a defect in the
   handout, not in your code.
2. **Dataset facts, measured.** ZINC: 10000/1000/1000 graphs, node counts 9 to 37, every
   graph connected, atom ids 0..20, bond ids {1,2,3}, max degree 4. LastFM: one connected
   component, 7624 nodes, 27806 undirected edges, 18 classes, max degree 216.
   `LAP_K = 8` and the smallest ZINC graph has 9 nodes, so exactly 8 non-trivial
   eigenvectors exist in the worst case — tight, but it fits. Write the code so it still
   works if `n <= LAP_K` (pad with zeros) rather than crashing.
3. **LastFM is where the costs bite.** `SPDAttention.precompute` must return a
   `[7624, 7624]` pair-level tensor for LastFM — the framework indexes the full matrix in
   `make_batch` even in sparse mode. All-pairs BFS in a Python loop over 7624 sources is
   slow; a hop-by-hop frontier expansion with sparse matrices, capped at `max_dist + 1`,
   is the sane way (distances beyond `max_dist` all share one bias anyway, and
   unreachable pairs use index `max_dist + 1`). Likewise the Laplacian eigenvectors for a
   7624-node graph want `scipy.sparse.linalg.eigsh`, not a dense `eigh`.
4. **`benchmark_step("full: ...", lastfm_model(SPDAttention))`** builds a dense
   `[1, 7624, 7624]` score tensor per head and may take minutes or fail with a memory
   error on CPU. That is the point of the comparison, and `benchmark_step` already catches
   `RuntimeError` and prints `FAILED: ...`. Report whatever it actually does — do not
   quietly drop the full-attention row from your table. The `peak GPU memory` column will
   print `n/a on CPU`; say so rather than inventing a memory number.
5. **`_reset(model)`** re-seeds and calls `reset_parameters()` on every submodule that has
   it. `nn.Embedding` and `nn.Linear` do; a raw `nn.Parameter` you add yourself does not,
   so it keeps whatever you initialised it with. Not a bug, just know it.

## 4. What you must deliver

`OUTPUT/answer.tex`, a LaTeX **fragment** (no `\documentclass`, no `\begin{document}`,
no `\usepackage` — those go in `OUTPUT/preamble.txt`). It starts at `\section{...}`.

The course asks for "your implemented code file", and this pipeline delivers a PDF, so
your fragment **is** the code submission: the grader has to be able to read your actual
implementation in it. Structure it as:

1. `\section{Q1: Structural Encoding in Graph Transformer}`
   - a short statement of what you implemented and the two design choices that matter
     (which eigenvectors, how they are injected and whether you handle sign ambiguity;
     how SPD is computed and how the bias enters the score);
   - the **final** code of `LapPETransformer` and `SPDAttention`, verbatim as you ran it,
     in a `lstlisting` (or `verbatim`) environment;
   - the measured result of cell 14, with the demo and plain-`Attention` baselines next to
     it so the numbers mean something.
2. `\section{Q2: Efficient Graph Transformer}`
   - which pairs you attend to and why (name the strategy: Exphormer-style
     neighbours + expander + global/virtual node, k-hop, BFS ball, whatever you chose);
   - the final code of `SparseSPDAttention`;
   - **the comparison the question asks for**: at least two masking strategies, their ZINC
     MAE and their pair counts, plus the LastFM `benchmark_step` full-vs-sparse row and the
     `run_node_task` micro-F1.

**Every number you print must come from a run you actually did.** Put the scripts in your
PLAYGROUND and the raw console output in a log file there, and say in `submission.md`
which log backs which table row. A number you did not measure is a fabrication and the
validator will go looking for it.

Do not paste debugging output, training curves per epoch, or exploratory code into
`answer.tex`. Final implementation + result tables + the reasoning a grader needs.

**On length (rule R8 below).** R8's word targets are written for prose answers. Here the
code listings are the deliverable and are not counted against it, but your *prose* is: aim
for **about 300 words per question** (so ~600 words of prose total), excluding code
listings, table contents and captions. That is enough to state the design, justify it and
read the results. Padding it out with a recap of what transformers are, or a closing
paragraph that restates the opening one, is a defect.

A figure is optional. If one genuinely helps (e.g. ZINC MAE against number of attended
pairs across your masking strategies), produce it as `fig_p1_<name>.pdf` in your OUTPUT
and reference it by bare filename. matplotlib is **not** in `.venv-gt`; it is in
`/home/xing/miniconda3/envs/py311/bin/python`, or you can pgfplots it, or you can skip the
figure — a clean table is worth as much here.

## 5. Scope boundary

Q3 (`HybridGTLayer`) is another worker's problem. Do not implement it, do not mention it
in your answer, and do not define a `HybridGTLayer` in anything you deliver.

---

## Rules for workers

**Master: copy this whole section verbatim into every `problem.md` you write.**
Workers and worker validators never see this file; the brief is the only channel
that reaches both of them.

These are not style preferences. They are defects. A worker that breaks one has
not finished, and a validator that passes one has not done its job.

### R8 — Answer the question asked, at the length it deserves

Write the shortest answer that earns full marks, then stop. Concrete targets,
measured from a previous assignment after a careful human edit:

| question | target |
|---|---|
| a 5-point short answer | about 190 words; up to 290 if it has several sub-parts |
| a 10-point paper summary and critique | about 550 words |

Left alone, an answer comes out **1.5 to 2 times** these lengths. That is the
failure mode to watch for in yourself. The excess is never new substance; it is
always one of these four:

- **exhaustive enumeration** — four examples where the question needs one, six
  hardware mechanisms where three carry the argument;
- **summarising your own answer** — a closing sentence that restates the opening
  one. If a paragraph begins "so the model is X" and ends "the model is therefore
  X", delete the ending;
- **explaining the significance of your own answer** — the question asked *where*
  the magic number is stored, not why that location is efficient;
- **stating what you are about to do** — "the three binding times are worth
  naming", "it is worth noting that".

Em-dashes are a symptom rather than a cause, but they mark the places to look:
one every 70 words means the sentences are being extended rather than ended.

**Validator: count the words.** Compare against the target above and against what
the problem is worth. Over target by more than a quarter, with no sub-part that
justifies it, is a defect to be reported and fixed, at severity major. Do not pass
an answer because it is correct if it is also twice as long as it needs to be.

### R9 — Read past the quotation

When you quote or cite a source, read the sentences that follow the quote before
you build an argument on it. Stop at the quote and you will write a criticism the
source already answers, or attribute to an author a claim they did not make.

Both of these happened in a previous assignment and both were findable with one
grep by the person marking it:

- A paper was criticised for raising a security problem and leaving it there. The
  next sentence of the paper proposed two countermeasures. (The real criticism was
  available and stronger: one countermeasure reintroduced the central authority the
  design existed to remove, and the other was justified only "on a system that
  assumes no malicious processes".)
- A paper's closing section was described as claiming a system succeeded because
  it had no predefined objectives. It says nothing of the sort; it says the authors
  were grateful never to have had to satisfy someone else's requirements. The
  critique was aimed at an invented claim.

So: quote the source, then say what the source does next with it. Never assert that
an author "leaves the problem there", "never asks", or "does not address" something
without having read to the end of that discussion.

**Validator: for every quotation and every characterisation of what a source says
or fails to say, open the source and read the surrounding passage yourself.** A
quotation that is verbatim can still be used to support a claim the source
contradicts two sentences later. Confirming the words exist is not the check;
confirming the argument survives the context is.

---

## 6. Note from the master: this run was restarted

An earlier attempt at this problem was launched and then stopped by the harness about 15
minutes in, for a scheduling reason that had nothing to do with the quality of the work.
Your playground therefore already contains files from that attempt — at the time it was
stopped there were `notes.md`, `solution.py`, `test_solution.py`, `experiments.py` and
`run_zinc.py`, plus a copy of `gt_framework.py` and `data/`.

Those files are yours to reuse, but **nobody has checked them**: no validator saw them, no
result was recorded, and the run was cut off while the first ZINC experiment was starting.
Read them before you trust a line of them, and re-run every experiment yourself — any
number left in a log file from that attempt is a number from an interrupted run and must
not appear in your answer unless you reproduced it.

If reading them costs you more than starting clean, start clean. Nothing in them is
required.
