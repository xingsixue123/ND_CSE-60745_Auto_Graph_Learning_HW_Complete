# Problem p1 — CSE 60745 HW3 Part (A), Questions 1, 2, 3 and 5

**Problem id: `p1`. Namespace every LaTeX label, every macro, every `lstdefinestyle`
name and every figure filename with `p1`.**  Worth **24 of the assignment's 30 points**
(Q1 6 pts, Q2 6 pts, Q3 6 pts, Q5 6 pts).

Question 4 is *not* yours. It is being answered by a different worker. Do not implement
R-GCN, do not touch the heterogeneous graph, and do not mention Q4 in your answer.

---

## 1. Where this lives in the assignment

Two source documents, both read-only:

| what | absolute path |
|---|---|
| the question text | `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3-Part(A).docx` |
| the scaffolding you complete | `/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb` |

Ingested copies (rule R7 — read all three channels and reconcile them):

    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002.png   <- preamble + Q1
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002.txt
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002_fig_01.png   <- THE ONE FIGURE
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_003.png   <- Q2, Q3, Q4, Q5
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_003.txt
    ingest/pages/Practice3_pyg_basics/alltext.txt               <- all 32 notebook cells

Rendered page indices, not the printed footer: the footer on **rendered page 2** says
"Page 1 of 4" because the cover page offsets it. Cite rendered indices.

**There is exactly one embedded figure in the whole document: `page_002_fig_01.png`
(727x525, rendered page 2).** Go and read it at native resolution. It is a screenshot of
the `MyGCNConv` skeleton — `class MyGCNConv(MessagePassing)` with `# TODO Q1` and the
four stubs. I have cross-checked it against notebook cell 16 and the two agree
character for character, so nothing in it is new information — but read it anyway and
confirm that for yourself rather than taking my word for it.

The notebook is a `.ipynb`, so ingest produced only `alltext.txt` for it (there is no
`pages/Practice3_pyg_basics/*.png`; a notebook has no page images). Read the original
`.ipynb` directly if you want cell boundaries.

---

## 2. The question text, transcribed

### From the preamble, rendered page 2 (applies to every question)

> In this assignment, you will practice the basic usage of PyTorch-Geometric and use the
> framework to address over-smoothing problem in deep GNNs. Please refer to PyG
> documentation for more technical details and use Google Colab for experiments. For each
> question, you will be asked to complete a `MessagePassing()` subclass as shown in the
> example below, where you need to specify the required components and aggregation
> strategy in `__init__()`, define propagated message in `message()`, and implement
> aggregation and node updation in `forward()`. You also need to complete
> `reset_parameters()` for parameter initialization.

### Q1 — rendered page 2, anchor "Q1: GCN Implementation (6 pts)"

> **Q1: GCN Implementation (6 pts)**
> Complete MyGCNConv(). You can refer to \`degree\`, \`add_self_loops\` and
> \`remove_self_loops\` functions defined in PyG to assist adjacency matrix related
> computation.

Notebook cell 15 states the formula the grader expects:

> Kipf & Welling's graph convolution, in the form the paper actually propagates:
> $$H' = \hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H W + b, \qquad \hat{A} = A + I, \quad \hat{d}_i = \sum_j \hat{A}_{ij}$$
> Per node, that is a weighted sum over the **closed** neighbourhood:
> $$h_i' = \sum_{j \in N(i) \cup \{i\}} \frac{1}{\sqrt{\hat{d}_i \hat{d}_j}}\, W h_j \;+\; b$$
> **Implement `forward`, `reset_parameters` and `message`.**

### Q2 — rendered page 3, anchor "Q2: GAT Implementation (6 pts)"

> **Q2: GAT Implementation (6 pts)**
> Complete MyGATConv() in multi-head fashion. Use \` torch_geometric.utils.softmax\` for
> softmax computation.

Notebook cell 18:

> $$e_{ij} = \text{LeakyReLU}\!\left(\mathbf{a}^\top [W h_i \,\|\, W h_j]\right), \qquad \alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in N(i) \cup \{i\}} \exp(e_{ik})}, \qquad h_i' = \sum_{j} \alpha_{ij} W h_j$$
> with $K$ independent heads, concatenated in hidden layers and averaged at the output.
> **Implement `forward`, `reset_parameters` and `message`.**

Note the softmax denominator runs over $N(i) \cup \{i\}$ — self-loops are included, as in
the GAT paper. Cell 19's stub additionally says:

> `node_dim`: the axis of the tensors passed to propagate that indexes nodes. The
> default, -2, is right for a `[N, channels]` tensor. For multi-head attention, propagate
> carries a `[N, heads, channels]` tensor, please set `node_dim=0` in that case.
>
> `message(self, h_j, h_i, index, size_i)`: Normalise the attention scores with
> `torch_geometric.utils.softmax` (already imported as `softmax`). `index` is the target
> node of each edge and `size_i` the number of targets.

Keep that `message` signature. `__init__` is called by the harness as
`conv_cls(in_channels, out_channels)` only, so the head count is yours to choose and must
default inside `__init__`; `out_channels` is the dimension the layer must **return** (the
next layer is built with `in_channels = out_channels`), so if you concatenate `K` heads
each head must produce `out_channels // K` features. Say in your answer how you handled
the "concatenated in hidden layers and averaged at the output" instruction — the harness
builds every layer through the same class, so you cannot know from inside the layer
whether you are the output layer unless you make that a constructor default.

### Q3 — rendered page 3, anchor "Q3: GIN Implementation (6 pts)"

> **Q3: GIN Implementation (6 pts)**
> Complete MyGINConv(). Feel free to design your own MLP architecture.

Notebook cell 21:

> $$h_i' = \text{MLP}\!\left((1 + \epsilon) \cdot h_i + \sum_{j \in N(i)} h_j\right)$$
> **Implement `forward`, `reset_parameters` and `message`.**
> Note that your MLP will contain a `BatchNorm1d` if you follow the GIN paper.

Cell 22's stub adds: "The MLP is yours to design. Whatever eps is, initialise it to 0."
and "nn.Sequential has no reset_parameters; its children do."

### Q5 — rendered page 3, anchor "Q5: Mitigate Over-Smoothing in Deep GNNs (6 pts)"

> **Q5: Mitigate Over-Smoothing in Deep GNNs (6 pts)**
> Stacking too many GNN layers will make all node embeddings drift towards each other and
> cause over-smoothing problem. Please look into the literature on over-smoothing and
> implement MyDeepConv() to design a GNN model that stays useful with an 8-hop receptive
> field. Note that 8-hop receptive field is not equal to 8-layer GNN.

Notebook cell 29:

> The first cell below trains your GCN from Q1 with 2 and with 8 layers on the same task.
> You will notice significant performance drop.
> **Your job:** design a layer, `MyDeepConv`, that stays useful with an 8-hop receptive
> field (**Not Necessarily 8 Layers!**). Feel free to look into the literature on
> over-smoothing and design your approach.

Cell 32 is `train_and_eval("MyDeepConv", MyDeepConv, n_layers=8)` prefixed with
`# Change n_layers based on your implementation`. So if your layer reaches 8 hops in
fewer than 8 stacked layers, change `n_layers` to match and **say what receptive field
your choice gives and why it is 8 hops**. The sentence "8-hop receptive field is not
equal to 8-layer GNN" appears in both the docx and the notebook; it is the hinge of the
question, and an answer that just stacks 8 of something has not engaged with it.

---

## 3. What you must deliver

`OUTPUT/answer.tex`, a LaTeX fragment with four `\section`s — Q1, Q2, Q3, Q5, in that
order. (Leave a gap for Q4; the master inserts it between Q3 and Q5.) Use
`\section*{...}` or `\section{...}` consistently; the master wraps your fragment and
will not renumber it.

For **each** of the four questions:

1. **The completed code**, as a listing. This question type explicitly asks you to
   complete named functions, so **the code listing IS the answer and is required** —
   this overrides the general "not a code listing unless the question explicitly asks"
   guidance you were given. Show the finished class (the four methods), not the stub,
   not a diff, and not your scratch experiments. Keep the comments you need to explain a
   non-obvious line and delete the rest.
2. **A short justification**: why that aggregation, why that normalisation, where the
   formula from the notebook maps onto your code. Roughly 120–180 words per question
   (see R8 below — these are 6-point questions). Do not re-derive the formula the
   notebook already gave you; explain the implementation decisions it does not fix.
3. **The measured result**: real val and test MRR and Hit@1 from an actual run.

Plus, once:

4. **One results table** collecting GraphSAGE (the demo, as control), GCN (2 layers),
   GAT, GIN, GCN at 8 layers, and MyDeepConv at an 8-hop receptive field — val MRR,
   val Hit@1, test MRR, test Hit@1. Put it in the Q5 section or in a short closing
   paragraph, whichever reads better; it is one table, not one per question.
5. **One figure, `fig_p1_depth.pdf`** (required): test MRR as a function of
   receptive-field depth for `MyGCNConv` against `MyDeepConv` — e.g. depths 2, 4, 6, 8.
   This is the evidence for the Q5 claim; without it the claim "stays useful" is an
   assertion. One figure only. 3–6 inches wide, axes labelled, legend, vector PDF,
   no title (the master writes the caption). Look at it after you make it.

`OUTPUT/preamble.txt` — one `\usepackage{...}` per line. You will need at least
`listings` and `xcolor`; `booktabs` for the table; `graphicx` and `float` for the
figure. All of these are installed (see `env.md`); `tlmgr install` does not work, so do
not reach for anything outside that list.

**Namespacing (rule R5) — this is the single most common way this pipeline breaks.**
Everything you define gets a `p1` in its name:
`\label{p1:tab:results}`, `\label{p1:fig:depth}`, `\lstdefinestyle{p1pystyle}` — and the
figure file is `fig_p1_depth.pdf`, referenced by **bare filename**, never an absolute
path. (A LaTeX control sequence cannot contain a digit, so if you define a macro,
namespace it in words: `\newcommand{\pOneCode}{...}`, not `\p1code`. Better still,
define no macros.)

**The completed notebook is NOT a deliverable** (rule R4 forbids it in OUTPUT). Keep it
in your PLAYGROUND; your validator will want to run it.

---

## 4. How to run it — environment, already verified by the master

Do **not** use Google Colab (the assignment says to; we are overriding that and running
locally). Do **not** use `~/miniconda3/envs/py311` — its pandas is broken on this machine
(`numpy.dtype size changed` ABI mismatch); I checked. Base `python3` has torch and numpy
but no pandas.

This exact recipe was run by the master and works. Use it:

    cd <your PLAYGROUND>
    python3 -m venv --system-site-packages .venv
    PIP_CACHE_DIR=$PWD/.pipcache ./.venv/bin/pip install torch_geometric gensim pandas scikit-learn scipy

`--system-site-packages` matters: it reuses the already-installed `torch 2.13.0+cpu`
instead of downloading a ~200 MB wheel. The resolved versions are numpy 2.5.2,
scipy 1.18.1, pandas 3.0.6, scikit-learn 1.9.1, torch_geometric 2.8.0.post1,
gensim 4.4.0. I smoke-tested `gensim.models.Word2Vec` and the notebook's
`load_social()` / `evaluate_ranking()` under pandas 3.0.6 — both fine.

Record the install in `PLAYGROUND/downloads.md` (rule R3), one line per item, including
the data files the notebook downloads.

The notebook's setup cell fetches 7 files from
`https://raw.githubusercontent.com/antman9914/CSE60745-Practice/main/`. Reachable;
1.4 s total. You only need `data/task1/*` — `data/task3/*` belongs to Q4, which is not
yours.

Measured facts you can check your run against:

    nodes 7624 | G_train 19464 undirected edges, 666 isolated nodes
    G_trainval 23635 undirected edges
    train 19464 queries / 116784 pairs | val 4171 queries / 87591 pairs | test same

This machine has 32 cores, 125 GB RAM and torch sees 16 threads. Nothing here is
expensive: a 3M-edge `propagate` at 64 channels benchmarks at 0.08 s forward. node2vec
(cell 7, Python walk loop, ~76k walks) is the slowest single step and is still minutes,
not hours. **You therefore have no excuse to cut `epochs` or `patience` for speed.**

### Rules of engagement with the notebook

- **Run the GraphSAGE demo (cell 14) end to end first**, before writing any of your own
  layers, "so that a failure later is yours and not the framework's" (cell 13). Report
  its numbers as the control row in your table.
- `MySAGEConv` (cell 9) is a complete worked example of exactly the pattern all four of
  your layers follow. Read it before writing anything.
- Section 5 (cells 11, 12 — `evaluate_ranking`, `GNNLinkPredictor`, `train_and_eval`) is
  the fixed harness: "Please only modify the code in this section if necessary." Treat
  it as frozen. The one sanctioned change is `n_layers` for Q5 (cell 32 tells you to).
  If you believe something else in it must change, do not quietly change it — say so
  explicitly in `submission.md` and in the answer, with the reason.
- `train_and_eval` constructs layers as `conv_cls(in_dim, out_dim)` and then calls
  `conv.reset_parameters()` a second time (cell 12 does this for every conv after
  construction). Your `reset_parameters` must therefore be safe to call twice and must
  work whether or not `__init__` already called it. Keep the `super().reset_parameters()`
  call and delete the `raise NotImplementedError`.
- Keep the given `message` signatures (`message(self, x_j)`, and for GAT
  `message(self, h_j, h_i, index, size_i)`). If a layer genuinely needs another argument
  you may add it, but pass it through `propagate`, do not route it around
  `MessagePassing`.
- `X` has 666 all-zero rows (users with no training edge). That is expected, not a bug.
- Numbers must be real. Run it, keep the console output in your playground, and make it
  clear in `submission.md` which command reproduces each number.

### Q5 specifically

Read actual over-smoothing papers before you design. The candidates a grader will
recognise: Li, Han & Wu (AAAI 2018) on GCN as Laplacian smoothing; Xu et al.
(ICML 2018) jumping knowledge; Chen et al. (ICML 2020) GCNII with initial residual and
identity mapping; Klicpera/Gasteiger et al. (ICLR 2019) APPNP / personalised PageRank;
Rong et al. (ICLR 2020) DropEdge; Zhao & Akoglu (ICLR 2020) PairNorm; Oono & Suzuki
(ICLR 2020) on exponential loss of expressive power. You do not need all of them — pick
the mechanism you actually implement and cite that.

**Rule R9 below applies with force here.** If you cite a paper, read past the sentence
you are quoting. Do not say a method "does not address" something without having read to
the end of that discussion, and do not attribute to an author a claim they did not make.
Cite only what you actually used; two or three citations, correctly characterised, beat
six name-drops. Give author, title, venue and year in a short bibliography at the end of
your Q5 section (hand-written `\begin{thebibliography}` or a simple list — do **not**
add a `.bib` file or a `\bibliography` command; `OUTPUT` may not contain one, and the
master compiles with `latexmk` without bibtex).

Note the structural point the question is making: an 8-hop receptive field can be
reached by something other than 8 message-passing layers (decoupled propagation, a
k-hop operator in one layer, jumping knowledge over a shallower stack, personalised
PageRank propagation...). Whatever you choose, state the hop count your design reaches
and justify it arithmetically, and set `n_layers` in cell 32 accordingly.

---

## 5. Where I expect this to go wrong

Flagging these so you spend your rounds on substance rather than rediscovering them:

- **GCN normalisation.** `aggr` must be `"add"`, not `"mean"` — the $1/\sqrt{\hat d_i \hat d_j}$
  coefficient already does the normalising, and `"mean"` would divide twice. The closed
  neighbourhood means you add self-loops before computing $\hat d$. If the incoming
  `edge_index` might already contain self-loops, `remove_self_loops` then `add_self_loops`
  is the safe order — that is why the question names all three helpers.
- **Isolated nodes.** 666 nodes have no training edge. After `add_self_loops`,
  $\hat d_i = 1$ for them, so there is no division by zero in GCN — but in GIN and in any
  layer where you normalise by degree without self-loops, guard it.
- **GAT `node_dim=0`.** The stub tells you to set it when propagating `[N, heads, C]`.
  Forgetting it produces silently wrong indexing rather than an error.
- **GIN + BatchNorm.** The harness calls `model.train()` / `model.eval()`, so BatchNorm
  is fine, but it is full-batch over 7624 nodes — mention it if it affects your design.
- **`out_channels` is a contract.** Whatever a layer returns must have width
  `out_channels`, because the next layer is constructed with that as its input width and
  the scorer takes a dot product of two node vectors.
- **R8 length.** Four questions, 24 points. The code listings are necessary and do not
  count against you; the prose does. Do not write a tutorial on GCNs.

---

## 6. Rules for workers — copied verbatim from the course notes

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
