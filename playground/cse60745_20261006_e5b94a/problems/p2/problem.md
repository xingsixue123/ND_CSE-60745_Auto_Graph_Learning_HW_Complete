# Problem p2 — CSE 60745 HW3 Part (A), Question 4 (R-GCN)

**Problem id: `p2`. Namespace every LaTeX label, every macro, every `lstdefinestyle`
name and every figure filename with `p2`.**  Worth **6 of the assignment's 30 points**.

Questions 1, 2, 3 and 5 are *not* yours; another worker has them. Do not implement GCN,
GAT, GIN or a deep layer, and do not mention them in your answer.

---

## 1. Where this lives in the assignment

Two source documents, both read-only:

| what | absolute path |
|---|---|
| the question text | `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3-Part(A).docx` |
| the scaffolding you complete | `/home/xing/project/auto_hw_complete/input/Practice3_pyg_basics.ipynb` |

Ingested copies (rule R7 — read all three channels and reconcile them):

    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_003.png   <- YOUR QUESTION
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_003.txt
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002.png   <- the shared preamble
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002.txt
    ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_002_fig_01.png   <- THE ONE FIGURE
    ingest/pages/Practice3_pyg_basics/alltext.txt               <- all 32 notebook cells

Rendered page indices, not the printed footer: the footer on **rendered page 3** says
"Page 2 of 4" because the cover page offsets it. Cite rendered indices.

**Cell numbering convention in this brief.** When I say "cell N" I mean the 1-indexed
numbering printed in `ingest/pages/Practice3_pyg_basics/alltext.txt`
(`===== cell 1 (markdown) =====`, ... through cell 32). The raw `.ipynb`'s `cells` array
is 0-indexed, so brief "cell N" is `nb["cells"][N-1]`. The p1 worker flagged this
ambiguity, so it is spelled out here.

**There is exactly one embedded figure in the whole document: `page_002_fig_01.png`
(727x525, rendered page 2) — not on your page, but it governs your answer's shape.** Go
and read it at native resolution. It is a screenshot of the `MyGCNConv` skeleton, shown
in the preamble as the template every question follows: `__init__`, `reset_parameters`,
`forward`, `message`, each `raise NotImplementedError`. I have cross-checked it against
notebook cell 16 and the two agree character for character — but read it yourself rather
than taking my word for it. Your `MyRGCNConv` (cell 27) is the same skeleton with
`num_relations` added to `__init__` and `edge_type` added to `forward`.

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

### Q4 — rendered page 3, anchor "Q4: R-GCN Implementation (6 pts)"

> **Q4: R-GCN Implementation (6 pts)**
> Complete MyRGCNConv(). Please implement the basic version of R-GCN. Edge type labels
> are provided in \`edge_type\`.

Notebook cell 24 gives the formula and the graph:

> Every layer so far has treated all edges alike. Combining the social graph with
> Practice 2's user–artist graph gives a graph with three relation types:
>
> | relation | from | to | count (directed) |
> |---|---|---|---|
> | `friend` | user | user | 38,928 |
> | `listens` | user | artist | 3,014,361 |
> | `listened_by` | artist | user | 3,014,361 |
>
> The `friend` relation is `G_train`, not the full graph — the same 70% of edges
> everything else here is allowed to see.
>
> **Input features.** Users and artists now share one index space, so the node2vec
> features of section 3 (users only) no longer fit. The second cell below replaces them
> with a metapath2vec embedding of all 15,466 nodes, `X_HETERO`, trained on the
> `listens` / `listened_by` edges along the meta-path `U-A-U`.
>
> R-GCN gives each relation its own weight matrix:
> $$h_i' = W_0 h_i + \sum_{r \in R} \sum_{j \in N_r(i)} \frac{1}{c_{i,r}} W_r h_j$$
>
> **Implement `__init__`, `reset_parameters`, `forward` and `message`.**

Note that for Q4 the notebook asks for **all four** methods including `__init__`
(elsewhere it asks for three) — and the docx preamble asks for all four everywhere.
Implement all four.

**"The basic version of R-GCN"** is the phrase to honour. Schlichtkrull et al. (ESWC
2018) give the equation above and then two parameter-reduction schemes on top of it —
basis decomposition and block-diagonal decomposition. The question asks for the one
*without* either: one full `[in_channels, out_channels]` weight matrix per relation,
plus the separate self-connection $W_0$. Do not implement basis or block decomposition;
if you want to mention them, one clause is enough, and rule R9 applies to how you
characterise the paper.

$c_{i,r}$ is a problem-specific normalisation constant; the paper's default choice is
$|N_r(i)|$, i.e. mean aggregation within each relation. State which you used and why,
and note what happens when $|N_r(i)| = 0$.

---

## 3. What you must deliver

`OUTPUT/answer.tex`, a LaTeX fragment with one `\section` for Q4. The master inserts it
between Q3 and Q5 of the assembled document, so do not number the section yourself in a
way that assumes it is first or last, and do not write "as we saw above".

The section must contain:

1. **The completed code**, as a listing. This question explicitly asks you to complete
   named functions, so **the code listing IS the answer and is required** — this
   overrides the general "not a code listing unless the question explicitly asks"
   guidance you were given. Show the finished `MyRGCNConv` (all four methods), not the
   stub, not a diff, not your scratch experiments.
2. **A short justification**: how the per-relation weight matrices and the self-loop
   term map onto the formula, what you chose for $c_{i,r}$, what `aggr` you used and
   why, and how you got `edge_type` through `MessagePassing` (the obvious route is one
   `propagate` call per relation on the edge subset; if you instead pass `edge_type`
   into a single `propagate`, say how you indexed the weights). Roughly 150–190 words —
   this is a 6-point question. See R8 below.
3. **The measured result**: real val and test MRR and Hit@1 from an actual run of
   `train_and_eval_hetero("R-GCN")` (cell 28), plus the epoch it selected. A small
   table or an inline sentence, your choice; one table at most.

**No figure is required for this question** and you should not invent one. If you
believe a figure genuinely earns its place, it must be `fig_p2_<name>.pdf`, referenced
by bare filename, and you must justify it in `submission.md`.

`OUTPUT/preamble.txt` — one `\usepackage{...}` per line. You will need at least
`listings` and `xcolor`, plus `booktabs` if you use a table. All are installed (see
`env.md`); `tlmgr install` does not work, so do not reach for anything outside the
list there.

**Namespacing (rule R5) — this is the single most common way this pipeline breaks.**
Everything you define gets a `p2` in its name: `\label{p2:tab:rgcn}`,
`\lstdefinestyle{p2pystyle}`. A LaTeX control sequence cannot contain a digit, so if you
define a macro, namespace it in words: `\newcommand{\pTwoCode}{...}`, not `\p2code`.
Better still, define no macros.

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
`https://raw.githubusercontent.com/antman9914/CSE60745-Practice/main/`. All reachable,
1.4 s total; `data/task3/user_artist.csv.gz` is 7.9 MB / 3,014,361 rows.

Measured facts you can check your run against:

    nodes 7624 | G_train 19464 undirected edges (38928 directed), 666 isolated nodes
    G_trainval 23635 undirected edges
    train 19464 queries / 116784 pairs | val 4171 queries / 87591 pairs | test same
    user_artist.csv.gz 3014361 rows, columns ['user', 'artist']
    hetero: 15466 nodes = 7624 users + 7842 artists; artist_id_offset 7624

This machine has 32 cores, 125 GB RAM and torch sees 16 threads. **Your graph is big
(6,067,650 directed edges) but it is not slow**: I benchmarked a 3,014,361-edge
`MessagePassing.propagate` at 64 channels on this machine at **0.08 s forward, 0.12 s
backward**. So a 50-epoch `train_and_eval_hetero` run is minutes, not hours. You
therefore have no excuse to cut `epochs`, `patience` or the edge set for speed.

### Which cells you need

You do **not** need section 3's node2vec (cell 7) or the `X` matrix at all — your
features come from `metapath2vec_features` (cell 26), which is independent of it. You
do need:

  - cell 3 (setup / downloads), cell 5 (`load_social`), cell 7 **only** for the
    `neighbour_table` helper, which cell 26 reuses — you can run cell 7's function
    definitions without executing `X = node2vec_features(...)` at the bottom;
  - cell 11 (`evaluate_ranking`), cell 12 (`GNNLinkPredictor.score` is reused by
    `RGCNLinkPredictor`);
  - cells 25, 26, 27, 28.

If you skip the `X = node2vec_features(...)` line, say so in `submission.md` — it is a
legitimate saving (it is Q1–Q3's input, not yours) but your validator will otherwise
notice a cell that did not run and treat it as a defect.

### Rules of engagement with the notebook

- `MySAGEConv` (cell 9) is a complete worked example of exactly the pattern your layer
  follows. Read it before writing anything. Running the GraphSAGE demo (cell 14) first
  is cheap insurance that the framework works before you blame your own code — but it
  needs `X`, so if you skipped node2vec, use the R-GCN run itself as your smoke test and
  say so.
- `RGCNLinkPredictor` and `train_and_eval_hetero` (cell 28) are the fixed harness, the
  heterogeneous counterpart of section 5's "Please only modify the code in this section
  if necessary". Treat them as frozen. If you believe something must change, do not
  quietly change it — say so explicitly in `submission.md` and in the answer, with the
  reason.
- Cell 28 constructs `MyRGCNConv(dims[i], dims[i+1], num_relations)` and then calls
  `conv.reset_parameters()` a second time for every conv. Your `reset_parameters` must
  be safe to call twice and must work whether or not `__init__` already called it. Keep
  the `super().reset_parameters()` call and delete the `raise NotImplementedError`.
- `forward(self, x, edge_index, edge_type)` — keep that signature; the harness calls it
  positionally.
- Numbers must be real. Run it, keep the console output in your playground, and make it
  clear in `submission.md` which command reproduces each number.

---

## 5. Where I expect this to go wrong

Flagging these so you spend your rounds on substance rather than rediscovering them:

- **`message(self, x_j)` and per-relation weights.** The stub's `message` takes only
  `x_j`. The clean way to honour both the stub and the formula is to apply $W_r$ to the
  features *before* propagating that relation's edge subset — valid because $W_r$ is
  linear and $c_{i,r}$ does not depend on $j$, so
  $\sum_j \frac{1}{c_{i,r}} W_r h_j = W_r\big(\frac{1}{c_{i,r}}\sum_j h_j\big)$, and the
  second form is also much cheaper when $W_r$ shrinks the width. Either order is
  defensible; pick one, implement it, and say which and why.
- **Relation 0 is already bidirectional.** `friend` comes from `EI_TRAIN`, which
  `load_social` has already passed through `to_undirected`, so both directions are
  present (38,928 directed = 2 x 19,464). `listens` and `listened_by` are separate
  relations precisely so that direction is modelled, so do **not** symmetrise them.
- **Zero-degree normalisation.** Most of the 15,466 nodes have $|N_r(i)| = 0$ for at
  least one relation (173 users have no artist; 666 users have no friend edge). Dividing
  by $|N_r(i)|$ must be guarded — `clamp(min=1)` on the degree, or `aggr="mean"`, which
  PyG already defines as 0 for an empty neighbourhood. Say which you used. An
  unguarded division gives NaNs that silently poison every metric.
- **`num_nodes`.** The hetero graph has 15,466 nodes but relation 0's edge subset only
  mentions users. If you call `propagate` per relation, pass the full node count
  (`size=(N, N)` or an `x` of the full height) or PyG will infer a smaller graph from
  the edge subset and your output tensors will not line up between relations.
- **Memory.** Messages for the two big relations are `[3014361, C]`. At C = 64 that is
  1.5 GB each — fine on 125 GB, but transform-before-propagate (above) keeps it smaller
  on the second layer. Do not subsample the graph to avoid this.
- **R8 length.** One 6-point question. The code listing is necessary and does not count
  against you; the prose does. Do not write a tutorial on relational GNNs.

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
