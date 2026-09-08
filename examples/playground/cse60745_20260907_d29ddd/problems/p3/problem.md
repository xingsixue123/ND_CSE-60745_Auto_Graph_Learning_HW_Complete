# p3 — Part B: Q5 Graph Measures (30 pts)

**Problem id: `p3`.** Namespace every LaTeX label, macro and figure filename with
`p3` (e.g. `\label{p3:tab:eig}`).

## Where this lives in the assignment

Rendered page **3** of
`playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_003.png`.
Anchor text: `Q5: Graph Measures (30 pts)`.

## Verbatim question text

> **Q5: Graph Measures (30 pts)**
> (Note: You may use NetworkX to facilitate your solutions.)
>
> Based on the created graph in Q3, generate eigenvector centrality, report top-10
> nodes with largest eigenvector centrality (10 pts). (You can use default
> parameters in NetworkX)
>
> Generate katz centrality, report top-10 nodes with largest katz centrality
> (10 pts). (You can use default parameters in NetworkX)
>
> Report average clustering coefficient of all nodes in the graph, report average
> Jaccard similarity of all connected node pairs in the graph (10 pts).

For context, Q3 (a different worker's problem, `p2`) reads:

> Create undirected graph using edge list file from graph.txt (attached in this
> assignment). Report node and edge numbers, number of connected components.

There is **no figure** attached to this question. The page contains only text.

## The data file

The assignment calls it `graph.txt`; the file actually attached is named
`graph-1.txt`. Absolute path:

    /home/xing/project/auto_hw_complete/input/graph-1.txt

**Read-only** — never write to `input/`.

Format: 26377 lines, each a **tab-separated pair of integer node ids**, one
undirected edge per line. Verified by the master: no self-loops, no duplicate
edges, no header, no comments.

### Pinned construction convention (use exactly this)

Build a **simple undirected** graph (`networkx.Graph`), one node per distinct id
in the file, one edge per line. Worker `p2` is building the same graph from the
same file for Q3/Q4 under this identical convention; your graph must be the same
object. The master's reference numbers: **26728 nodes, 26377 edges, 4104
connected components**. You do not have to report these (that is Q3's job) but
you should confirm you got the same graph, and state the graph you are working on
in one sentence so your answer stands alone.

## What to watch out for

- **Eigenvector centrality on a disconnected graph.** The graph has 4104
  components, one giant (13903 nodes) and many tiny ones.
  `nx.eigenvector_centrality` is a power iteration and **may fail to converge**
  (`PowerIterationFailedConvergence`) on such a graph with default `max_iter=100`.
  The question says "You can use default parameters in NetworkX". If the default
  call converges, use it and say so. If it does **not**, do not silently switch
  methods — state the failure, then use `nx.eigenvector_centrality_numpy` (exact,
  no convergence parameter) or raise `max_iter`, and say exactly what you did and
  why. Report which function produced the numbers you table.
  Note also: on a disconnected graph the principal eigenvector is supported on
  the component with the largest spectral radius, so most nodes may get
  centrality ~0 and the top-10 may all come from one small dense component. If
  that happens it is the correct answer to the question as asked — report it, and
  add one or two sentences interpreting it. Do **not** quietly restrict to the
  largest connected component instead; that answers a different question. (If you
  want to additionally show the LCC-restricted result as a remark, that is fine,
  but the headline answer must be the whole graph with default parameters.)
- **Katz centrality.** Same caution: `nx.katz_centrality` iterates and can fail
  to converge; `nx.katz_centrality_numpy` is the exact alternative. Defaults are
  `alpha=0.1, beta=1.0`. Note that Katz requires `alpha < 1/lambda_max`; check
  that the default alpha is admissible for this graph and say so. Report which
  function you used.
- **Average clustering coefficient**: `nx.average_clustering(G)` — the mean of
  the per-node local clustering coefficient over *all* nodes (nodes of degree < 2
  contribute 0 by convention). State that convention.
- **Average Jaccard similarity of all connected node pairs**: for every **edge**
  (u,v) in the graph, compute the Jaccard similarity of the neighbourhoods of u
  and v, then average over all 26377 edges. `nx.jaccard_coefficient(G, G.edges())`
  does exactly this. Note explicitly the convention question: NetworkX's Jaccard
  for an edge (u,v) uses the raw neighbour sets |N(u) ∩ N(v)| / |N(u) ∪ N(v)|,
  which *includes* u and v themselves in each other's neighbour sets — so an
  isolated edge (a degree-1/degree-1 pair) gets similarity 0. State the formula
  you used so the grader can see the convention. Report the average as a number
  to at least 4 significant figures.

## Deliverable

`answer.tex` — a LaTeX **fragment**: no `\documentclass`, no `\begin{document}`,
no `\usepackage`. Extra packages go one per line in `preamble.txt`.

Structure: a subsection per part. The two top-10 lists must be presented as
**tables** — rank, node id, centrality value (enough significant figures to
distinguish adjacent entries; use scientific notation if the values are tiny).
The clustering coefficient and average Jaccard similarity must each be stated as
a single clearly labelled number.

`needs` for this problem is `code` only — no figure is required. If you choose to
add one, it must be `fig_p3_*.pdf`, vector, referenced by bare filename.

Tooling: base `python3` has networkx 3.6.1, numpy, scipy is **absent** from base
but present in `/home/xing/miniconda3/envs/py311/bin/python` (which also has
matplotlib/pandas — check whether it has networkx). `eigenvector_centrality_numpy`
and `katz_centrality_numpy` need scipy for sparse eigensolvers, so you may need
the py311 interpreter or a venv built in your playground (record any venv in
`downloads.md`, rule R3). Some of these computations take a while on 26728 nodes
— that is expected; let them run rather than sampling.

This is a homework submission, not a lab notebook: **do not paste your script
into `answer.tex`**, and do not dump intermediate output. Method in a sentence or
two, then the numbers.
