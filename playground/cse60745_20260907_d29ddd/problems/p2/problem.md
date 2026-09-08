# p2 — Part B: Q3 Graph Creation + Q4 Graph Essentials (40 pts)

**Problem id: `p2`.** Namespace every LaTeX label, macro and figure filename with
`p2` (e.g. `\label{p2:fig:deg}`, `fig_p2_degree_dist.pdf`).

## Where this lives in the assignment

Rendered page **3** of
`playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_003.png`.
Anchor text: `Q3: Graph Creation (10 pts)`.

## Verbatim question text

> Part B – Graph Essentials and Measures (70 pts)
>
> In this part, you will create a graph and compute related graph essentials and
> measures.
>
> Note: You may use NetworkX, a python library for studying graphs and answering
> below questions.
>
> **Q3: Graph Creation (10 pts)**
> (Note: You may use NetworkX to facilitate your solutions.)
>
> Create undirected graph using edge list file from graph.txt (attached in this
> assignment). Report node and edge numbers, number of connected components.
>
> **Q4: Graph Essentials (30 pts)**
> (Note: You may use NetworkX to facilitate your solutions.)
>
> Based on the created graph in Q3, get the largest connected component, report
> node and edge number of this component (10 pts).
>
> Show visualization of the second largest connected component (10 pts).
>
> Plot degree distribution of the whole graph (10 pts).

*(Q5, on the same page, is a different worker's problem — ignore it.)*

There is **no figure** attached to this question. The page contains only text.

## The data file

The assignment calls it `graph.txt`; the file actually attached to this
assignment is named `graph-1.txt`. Absolute path:

    /home/xing/project/auto_hw_complete/input/graph-1.txt

It is **read-only**. Never write to `input/`.

Format: 26377 lines, each a **tab-separated pair of integer node ids**, one
undirected edge per line. Verified by the master: no self-loops, no duplicate
edges (in either orientation), no header line, no comments.

### Pinned construction convention (use exactly this)

Build a **simple undirected** graph (`networkx.Graph`), one node per distinct id
appearing in the file, one edge per line. Do not add isolated nodes, do not
symmetrize twice, do not treat it as directed. Another worker (`p3`) is building
the same graph from the same file for Q5, under this same convention, so your
Q3 counts must agree with theirs. The master's own check of this construction
gives **26728 nodes, 26377 edges, 4104 connected components** — reproduce it
yourself and report your own computed numbers; if you disagree with the master,
say so and show why.

## Q4 specifics

- **Largest connected component**: report its node count and its edge count (the
  number of edges in the induced subgraph, not the whole graph's edge count).
- **Second largest connected component**: visualize it. ⚠️ **There is a size tie
  here** — the master observed component sizes 13903, 69, 30, 30, 29, 26, ... so
  the second largest (69 nodes) is unique, but the *third* place is tied at 30.
  Verify the ordering yourself. State plainly which component you visualized and
  how you selected it (e.g. `sorted(nx.connected_components(G), key=len,
  reverse=True)[1]`), and note its node and edge count so the grader can see it
  is the right one. If you find a tie at second place, say how you broke it.
  A 69-node component is small enough to draw legibly; choose a layout
  (spring/kamada-kawai) with a fixed seed, keep node markers small, and consider
  omitting node labels if they make the picture unreadable — say which you did.
- **Degree distribution of the whole graph**: plot it. A bar/scatter plot of
  P(k) or of the raw count N(k) versus degree k. Because this is a sparse graph
  with a heavy tail, a **log-log** plot is the informative one; a linear plot
  alone will look like a single spike. Producing both (linear inset or two
  panels) is fine, but at minimum make the plot readable and label both axes
  including units/meaning. Also report the min/max/mean degree in the text so
  the plot is anchored by numbers.

## Deliverable

`answer.tex` — a LaTeX **fragment**: no `\documentclass`, no `\begin{document}`,
no `\usepackage`. Extra packages go one per line in `preamble.txt`.

Structure it as subsections for Q3 and for the three parts of Q4. Report every
requested number explicitly in the prose or in a small table — a grader must be
able to find "number of nodes", "number of edges", "number of connected
components", "LCC node count", "LCC edge count" without hunting.

Figures: `fig_p2_*.pdf`, vector PDF from matplotlib, referenced by **bare
filename** (never an absolute path). Place each figure near the text that refers
to it and give it a caption.

Tooling: base `python3` has networkx 3.6.1 but **no matplotlib**.
`/home/xing/miniconda3/envs/py311/bin/python` has matplotlib 3.10.8, numpy,
scipy, pandas — check whether it also has networkx. If you need a venv, build it
inside your playground and record it in `downloads.md` (rule R3).

This is a homework submission, not a lab notebook: **do not paste your script
into `answer.tex`**, and do not include intermediate/debugging output. State the
method briefly, give the numbers, show the figures.
