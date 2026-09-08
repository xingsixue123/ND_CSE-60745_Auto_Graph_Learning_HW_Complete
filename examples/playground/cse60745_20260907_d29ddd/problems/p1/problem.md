# p1 — Part A: Graph Creation and Modification (30 pts)

**Problem id: `p1`.** Namespace every LaTeX label, every macro and every figure
filename with `p1` (e.g. `\label{p1:fig:q1}`, `fig_p1_q1_graph.pdf`).

## Where this lives in the assignment

Rendered page **2** of `playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_002.png`.
Anchor text: `Part A – Graph Creation and Modification (30 pts)`.

## Verbatim question text

> Part A – Graph Creation and Modification (30 pts)
>
> In this part, you will learn "Graph Creation and Modification".
>
> Note: You may use NetworkX, a python library for studying graphs and answering
> below questions. The NetworkX Tutorial can help you start working with NetworkX.
>
> **Q1: Graph Creation (15 pts)**
>
> Create the following undirected graph and show visualization of this graph.
> (Note: You may read NetworkX tutorial to facilitate your solutions.)
>
> *[a figure follows here — see below]*
>
> **Q2: Graph Modification (15 pts)**
>
> Based on graph created in Q1, remove node 1, edge (0, 4) and edge (0, 5). List
> remaining components and visualize remaining graph. (Note: You may use NetworkX
> to facilitate your solutions.)

## THE GRAPH IS ONLY IN A FIGURE — you must read the image

Q1 says "create the **following** graph". The graph is an embedded image; it does
**not** appear in the extracted text at all. The figure file is:

    /home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_002_fig_01.jpeg

(428x588 px, native resolution). Read that file. If labels are too small, crop
and upscale it 4x with PIL and read it again. Do **not** answer from the
whole-page PNG — it is downscaled and the node labels are unreadable there.

### Master's own reading of the figure (verify it, do not just trust it)

The master extracted the node-disc centres programmatically and then measured, for
each node, the angular directions in which line segments depart from it, at ring
radii r = 24, 32, 42, 55 px. A departure whose measured angle is *constant* in r
points at a true neighbour; an angle that *drifts* with r belongs to a straight
line passing near, but not through, that node's centre. Detected node centres
(x, y in figure pixels):

    0:(78.5,43.0)   8:(290.5,91.0)   4:(211.0,121.0)  6:(372.5,196.5)  5:(74.5,212.5)
    1:(194.5,261.0) 3:(340.5,322.0)  9:(244.5,368.5)  7:(96.5,482.0)   2:(234.5,530.5)

Resulting edge list (15 edges):

    (0,1) (0,4) (0,5)
    (1,2) (1,6)
    (2,3) (2,7)
    (3,4) (3,8)
    (4,9)
    (5,7) (5,8)
    (6,8) (6,9)
    (7,9)

**Two traps the master hit, which you should re-check rather than rediscover:**

1. **There is NO edge (4,5) and NO edge (4,8).** Nodes 5, 4, 8 are very nearly
   collinear, so the single straight edge **(5,8)** is drawn passing *through the
   drawn disc of node 4*. It looks exactly like "5–4 and 4–8". The measurement
   that settles it: the departure angle at node 5 drifts 325.5°→328.5° as r goes
   24→55 (converging on the 5→8 bearing of 330.6°, not the 5→4 bearing of 326.2°),
   and symmetrically at node 8 it drifts 156.0°→153.0° (converging on 8→5 = 150.6°,
   not 8→4 = 159.3°). Node 4 shows only three *constant-angle* departures.
2. **There is NO edge (0,6) and NO edge (0,9).** 0–4–6 are nearly collinear and so
   are 0–1–9; the true edges are the short ones, (0,4) and (0,1). Node 6 has no
   departure toward 0, and node 9 has no departure toward 0 or 1.

**Consistency checks that corroborate this reading — cite them in your answer if
useful, and re-derive them yourself:**

- Every one of the 10 nodes has degree exactly 3. The graph is 3-regular on 10
  nodes with 15 edges. A hand-drawn homework figure landing on a perfectly
  3-regular graph by accident is very unlikely; this is almost certainly a
  `networkx.random_regular_graph(3, 10)` layout.
- Q2 independently corroborates two of the edges: it instructs you to *remove*
  edge (0,4) and edge (0,5), which only makes sense if (0,4) and (0,5) are edges.
  They are, in the reading above. (Note this is also the reason a reading with an
  edge (4,5) would still be self-consistent — hence the careful measurement in
  trap 1.)

You are responsible for confirming this. Look at the figure yourself, at native
resolution and upscaled. If your reading differs from the master's, say so
explicitly in your notes and explain which channel you trusted and why.

## Q2 — expected shape of the answer

Remove node 1 (and with it its incident edges (0,1), (1,2), (1,6)), then remove
edge (0,4) and edge (0,5). Node 0 then has degree 0. "List remaining components"
means: enumerate the connected components of the resulting graph, giving the node
set of each (and, helpfully, its size). Then visualize the remaining graph.

Verify this by computation; do not copy a claimed answer.

## Deliverable

`answer.tex` — a LaTeX **fragment** (no `\documentclass`, no `\begin{document}`,
no `\usepackage`; extra packages go one per line in `preamble.txt`). It must:

- present Q1 and Q2 as two clearly headed subsections;
- for Q1: state how the graph was constructed (the node set and the explicit edge
  list, formatted readably — a table or an inline list, not a code dump) and
  include the **visualization** as a figure;
- for Q2: state which elements were removed, list the remaining connected
  components explicitly (node sets), and include the **visualization** of the
  remaining graph;
- report node/edge counts before and after.

Figures: produce `fig_p1_*.pdf` (vector PDF) via matplotlib and reference them by
**bare filename** only. Use `/home/xing/miniconda3/envs/py311/bin/python` — the
base `python3` has networkx but **no matplotlib**; the py311 env has matplotlib
3.10.8 + numpy + scipy but you must check whether it has networkx, and if not,
either build a venv in your playground (record it in `downloads.md`, rule R3) or
compute the graph facts with base `python3` and only draw with py311.

Use a **fixed layout seed** so the two figures (Q1 and Q2) place shared nodes in
the same positions — this makes the modification visually obvious and is worth
doing. Label every node with its number.

This is a homework submission, not a lab notebook: **do not paste your Python
script into `answer.tex`.** State the construction, the results, and show the
figures. A short snippet is acceptable only if it genuinely helps the grader; a
full script dump is a defect.
