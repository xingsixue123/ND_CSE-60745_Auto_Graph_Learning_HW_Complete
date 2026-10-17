# Problem p2 — Q3 Hybrid Graph Transformer (30 pts)

**Problem id: `p2`.** Namespace every LaTeX label, every figure filename and every macro
you define with `p2:` / `fig_p2_` (rule R5 below).

---

## 1. Where this comes from

Assignment document: `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3(B).doc`

Ingested at `INGEST/pages/CSE 60745_Fall 2026_HW3(B)/` — **rendered page 2** (page 1 is
the cover page). Anchor text: `Q3: Hybrid Graph Transformer (30 pts)`.

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
> **Q3: Hybrid Graph Transformer (30 pts)**
> Complete HybridGTLayer() to implement a hybrid graph transformer composed of both
> MPNN-based local attention and transformer-based global attention. You can implement
> GraphGPS or design your own hybrid structures.

(Q1 and Q2 are on the same page and belong to a different worker. Do not answer them.)

Reference [4], Rampášek et al., "Recipe for a general, powerful, scalable graph
transformer" (NeurIPS 2022), is the GraphGPS paper the question names. If you build an
argument on what it says, read the surrounding passage, not just the sentence you quote
(rule R9 below).

## 2. The real question is in the notebook

Second input file, **read it**:
`/home/xing/project/auto_hw_complete/input/task6_graph_transformer-1.ipynb`

It is also ingested as plain text at
`INGEST/pages/task6_graph_transformer-1/alltext.txt` (22 cells; the notebook has no
stored outputs and no embedded images, so that text is the complete notebook).

Read cells 6-11 as well as the three below: cell 8 defines `Attention`,
`TransformerBlock`, `GraphTransformer` and `graph_mean_pool`; cell 9 defines
`run_graph_task`; cell 11 is the demo. They are the conventions your layer lives inside.

Below are the question cells **verbatim**. Cell 21 is the signature you must match
exactly, and cell 22 is the driver that will call it.

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
        data/task2/, data/task3/   the three LastFM CSVs (Q2 only; you will not need them)

**First thing to do — copy it into your own playground and work there:**

    cp -r /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/shared/gt_framework.py .
    cp -r /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/shared/data .

`gt_framework.py` loads the datasets at import time with relative paths (`data/zinc`,
`data/task2/...`), so run from a directory that has `data/` in it.

`gt_framework.py` is notebook cells 3, 5, 7, 8, 9 in full, plus the two demo classes of
cell 11 and `PAIR_TYPES`/`pair_types` from cell 16. It deliberately contains **no**
answer: the TODO cells are not in it. Write your classes in your own file:

    from gt_framework import *
    class HybridGTLayer(nn.Module): ...
    class HybridGT(nn.Module): ...        # cell 22, copied verbatim from the notebook

Do not edit `gt_framework.py`'s content in your own copy. If you think the given
framework is wrong, say so in `submission.md` rather than silently changing it.

**Measured timings** (so you can plan): the demo
`run_graph_task("demo", CentralityTransformer(attention_cls=CNAttention))` runs at
**4.5 s/epoch**, i.e. a full 30-epoch ZINC run takes about 2.5 minutes. Real experiments
are cheap here. Your worker round has a 2-hour budget.

### Things the master already checked, so you do not have to

1. **Dataset facts, measured.** ZINC: 10000/1000/1000 graphs, node counts 9 to 37, every
   graph connected, 23.2 nodes on average. Atom ids run 0..20 (`num_atom_types=21`).
   **Bond ids in the ZINC subset are {1, 2, 3}** — the docstring says `[0, 4)`, so size an
   edge-type embedding 4 and do not assume id 0 occurs. Max degree 4.
2. **Your layer is called by `HybridGT` (cell 22), not by `GraphTransformer`.** The node
   states arrive as `[num_nodes, dim]` for the whole batch with `batch` giving the graph
   id — they are **not** padded to `[B, N, dim]`. If your global branch uses dense
   attention you must densify yourself; `to_dense_batch` is imported by cell 3 and
   available from `gt_framework`, and `graph_mean_pool` is there too. Attention must stay
   **inside each graph** — a node must not attend to a different molecule's nodes. Getting
   this wrong still trains and still prints a plausible MAE, so check it explicitly.
3. **`run_graph_task` calls `_prepare`, which calls `precompute_fns(model)`**, which reads
   `model.attention_cls` via `getattr(..., None)`. `HybridGT` does not define
   `attention_cls`, so the pair-level and sparse paths are skipped and only
   `HybridGT.precompute` (the degree table, aliased from `CentralityTransformer`) runs.
   `batch["virtual"]` exists and is all-`False`. Nothing for you to do here; just know why
   `batch` has the keys it has.
4. **`_reset(model)`** re-seeds and calls `reset_parameters()` on every submodule that has
   it. `nn.Embedding`, `nn.Linear`, `nn.LayerNorm` and PyG's `MessagePassing` layers do; a
   raw `nn.Parameter` you add yourself does not, so it keeps whatever you initialised it
   with. Not a bug, just know it.
5. **Baselines you can reproduce cheaply**, so your 30-point answer has something to be
   measured against: `run_graph_task("plain", GraphTransformer())` (no structural
   information at all) and `run_graph_task("demo", CentralityTransformer(attention_cls=CNAttention))`
   (cell 11's demo). Both run from `gt_framework` with no new code.

## 4. What you must deliver

`OUTPUT/answer.tex`, a LaTeX **fragment** (no `\documentclass`, no `\begin{document}`,
no `\usepackage` — those go in `OUTPUT/preamble.txt`). It starts at `\section{...}`.

The course asks for "your implemented code file", and this pipeline delivers a PDF, so
your fragment **is** the code submission: the grader has to be able to read your actual
implementation in it. Structure it as `\section{Q3: Hybrid Graph Transformer}` containing:

- **the design**, stated compactly: what the local branch is (which MPNN, how bond types
  enter it), what the global branch is, and — the part the question is really asking about
  — **how the two are combined** (parallel sum as in GraphGPS, gated, sequential, ...) and
  why you chose that. If you follow GraphGPS, say which parts you kept and which you
  simplified; if you designed your own, say what it does differently and why.
- **the final code** of `HybridGTLayer`, verbatim as you ran it, in a `lstlisting` (or
  `verbatim`) environment. Include `HybridGT` only if you changed it.
- **the measured result** of cell 22, in a small table against at least two baselines from
  item 5 above, so a 30-point answer is evidence rather than assertion.
- An ablation is a cheap way to earn the "how are they combined" marks on evidence rather
  than assertion: the same layer with the local branch removed, and with the global branch
  removed, is two more 2.5-minute runs. Worth doing.

**Every number you print must come from a run you actually did.** Put the scripts in your
PLAYGROUND and the raw console output in a log file there, and say in `submission.md`
which log backs which table row. A number you did not measure is a fabrication and the
validator will go looking for it.

Do not paste debugging output, per-epoch training curves, or exploratory code into
`answer.tex`. Final implementation + result table + the reasoning a grader needs.

**On length (rule R8 below).** R8's word targets are written for prose answers. Here the
code listing is the deliverable and is not counted against it, but your *prose* is: this
is a 30-point question with one deliverable, so aim for **about 400 words** of prose,
excluding the code listing, table contents and captions. That is enough to state the
design, justify the combination rule and read the results. Padding it out with a recap of
what message passing is, or a closing paragraph that restates the opening one, is a defect.

A figure is optional. If one genuinely helps (e.g. a block diagram of the layer, or the
ablation as a bar chart), produce it as `fig_p2_<name>.pdf` in your OUTPUT and reference it
by bare filename. matplotlib is **not** in `.venv-gt`; it is in
`/home/xing/miniconda3/envs/py311/bin/python`, or you can draw it with TikZ, or you can
skip the figure — a clean table is worth as much here.

## 5. Scope boundary

Q1 (`LapPETransformer`, `SPDAttention`) and Q2 (`SparseSPDAttention`) are another worker's
problem. Do not implement them, do not mention them in your answer, and do not define
those classes in anything you deliver. Your absolute encoding is the demo's degree
centrality, which `HybridGT` already provides.

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
