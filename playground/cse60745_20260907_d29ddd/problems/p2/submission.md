# p2 submission — Q3 Graph Creation + Q4 Graph Essentials

## What the problem asked

**Q3 (10 pts):** build an undirected graph from the edge list `graph.txt` and report
node count, edge count, number of connected components.

**Q4 (30 pts):** (a) get the largest connected component, report its node and edge
number; (b) show a visualization of the second largest connected component; (c) plot
the degree distribution of the whole graph.

**Brief vs. assignment page: no disagreement.** I read rendered page 3 through all
three channels. `page_003.txt` matches the brief's verbatim quote word for word.
`page_003.png` shows a text-only page. There are **no** `page_003_fig_*` files in the
ingest directory (only `page_002_fig_01.jpeg` exists), confirming the brief's claim
that this question has no attached figure. Nothing on the page needed transcription
from an image.

One naming point, already flagged by the master and confirmed: the assignment says
`graph.txt`, the attached file is `input/graph-1.txt`. Same file; I used it read-only.

## What I decided it needed

**code + diagram + a little plain prose.**
- *code*: every requested item is a computed number. Nothing here is estimated.
- *diagram*: two figures are explicitly demanded by the verbs "Show visualization"
  and "Plot".
- *plain*: brief statement of method and interpretation. Per the brief I did **not**
  paste any script into `answer.tex`.

## What I did

Built the graph under the master's pinned convention: `networkx.Graph`, one node per
distinct id, one edge per tab-separated line, no isolated nodes added, not
symmetrised twice, not directed. I first verified the file itself has **0 self-loops
and 0 duplicate undirected edges**, so 26,377 lines give exactly 26,377 distinct
edges.

Because every downstream number depends on this one construction, I verified it
**three independent ways** rather than trusting a single run (`crosscheck.py`):

1. networkx 3.3 (py311 interpreter),
2. networkx 3.6.1 (base `python3`) — rules out a library-version artifact,
3. a **pure-Python union-find** with plain dicts that never imports networkx —
   rules out a networkx bug or a misuse of its API.

All three agree on all eleven reported quantities. I also checked three global
invariants, all of which hold: degree sum $=2m$ (52,754 $=2\times 26{,}377$); the
component sizes sum to the node count; and the induced edge counts of the components
sum to the total edge count. My numbers reproduce the master's expected
26,728 / 26,377 / 4,104 exactly, so there is nothing to dispute.

For Q4(b) I selected the component by `sorted(nx.connected_components(G), key=len,
reverse=True)[1]` and explicitly counted ties at that size. **Second place is not
tied** — exactly one component has 69 nodes — so no tie-breaking was needed. The tie
the master warned about is at *third* place (two components of 30 nodes) and does not
affect this question. I state this in the answer.

For the drawing I rendered the component both with and without node labels and
*looked at both PNGs* before choosing. The labelled variant
(`cc2_labelled_variant.pdf`, playground only) has overlapping and marker-occluded
labels in the dense core, so the delivered figure omits labels; the answer says so
and says why. Layout is Kamada–Kawai, which is deterministic for a given graph, so no
RNG seed is needed for reproducibility.

## Intermediate steps and code

All paths relative to PLAYGROUND. Run with
`/home/xing/miniconda3/envs/py311/bin/python` (needs `MPLCONFIGDIR=$PWD/.mplconfig`
for the figure script).

| File | What it does |
|---|---|
| `analyze.py` | Builds the graph and computes every reported number. Writes `results.json` + `results.txt`. Also checks the file for self-loops/duplicates and asserts the three global invariants. |
| `crosscheck.py` | Recomputes all counts via networkx *and* via a no-networkx union-find, and diffs both against `results.json`. Prints a table and exits non-zero on any mismatch. |
| `figs.py` | Produces the two vector PDFs into OUTPUT, plus the labelled CC2 variant into the playground for the readability comparison. |
| `notes.md` | Channel reconciliation, plan, tooling decision. |
| `compiletest/` | Wrapper document proving `answer.tex` compiles as a fragment. |

Reproduce everything:

```
/home/xing/miniconda3/envs/py311/bin/python analyze.py     # all numbers
python3 crosscheck.py                                      # -> "ALL THREE CHANNELS AGREE", exit 0
MPLCONFIGDIR=$PWD/.mplconfig /home/xing/miniconda3/envs/py311/bin/python figs.py
```

## Results

Every computed value in `answer.tex`, and where it came from. All from
`results.json` (via `analyze.py`), all confirmed by `crosscheck.py`.

| Claim in answer.tex | Value |
|---|---|
| Q3 number of nodes | **26,728** |
| Q3 number of edges | **26,377** |
| Q3 number of connected components | **4,104** |
| self-loops / duplicate edges in file | 0 / 0 |
| independent cycles, whole graph ($m-n+c$) | 3,753 (vs 22,624 edges if it were a forest) |
| Q4(a) LCC nodes | **13,903** |
| Q4(a) LCC edges (induced) | **16,695** |
| LCC share of nodes / edges | 52.0% / 63.3% |
| Q4(b) 2nd-largest CC nodes / edges | **69 / 80** |
| top-10 component sizes | 13903, 69, 30, 30, 29, 26, 23, 21, 21, 20 |
| ties at 2nd place / at 3rd place | 1 (unique) / 2 (tied at 30) |
| CC2 diameter, max degree, independent cycles | 17, 7, 12 |
| CC2 degree histogram (supports "hubs of degree 7 and 6") | {1:19, 2:29, 3:7, 4:11, 5:1, 6:1, 7:1} |
| Q4(c) min / max / mean / median degree | **1 / 59 / 1.974 / 1** |
| $N(1)$, $N(2)$ | 13,942 (52.2%), 7,423 (27.8%) |
| fraction with degree $\le 2$ | 79.93% ("four fifths") |
| distinct degree values | 37 |
| node of maximum degree | node 22777, degree 59 |
| top degrees each realised once | $N(36)=N(38)=N(40)=N(51)=N(57)=N(59)=1$ |

## Deliverables

In OUTPUT:
- `answer.tex` — fragment; no `\documentclass`/`\usepackage`/`document` env (checked
  by grep). All labels namespaced `p2:`; figures referenced by bare filename.
- `fig_p2_cc2.pdf` — Q4(b), second largest connected component.
- `fig_p2_degree_dist.pdf` — Q4(c), two-panel degree distribution (linear + log–log).
- `preamble.txt` — `graphicx`, `booktabs`, `amsmath`.

`python3 framework/tools/lint_output.py <OUTPUT>` → **OUTPUT LINT OK**, exit 0.
The fragment compiles cleanly in a wrapper (`compiletest/`): exit 0, zero `!` errors,
all references resolved on the second pass, no overfull/underfull boxes. I rendered
all three pages to PNG and looked at them; both figures are legible at printed size.

Nothing was installed; `downloads.md` records "(nothing installed)".

## Where I am least confident

1. **The "roughly power-law-like" characterisation** in Q4(c) is a qualitative
   reading of the log–log plot, not a fitted claim. I deliberately did **not** fit an
   exponent or run a Kolmogorov–Smirnov / `powerlaw` test, because the question only
   asks to *plot* the distribution. If the grader wants a fitted $\gamma$, that is
   absent. I worded it as "approximately linearly ... roughly power-law-like" rather
   than asserting a power law, which I think is the honest level of claim, but it is
   the one sentence in the answer that is interpretive rather than computed.

2. **Choice of $P(k)$ vs $N(k)$ and no binning.** I plot the raw un-binned
   distribution on both panels. For a heavy tail, logarithmic binning or a CCDF is
   arguably the better presentation and would make the tail less ragged. I judged the
   raw plot more faithful to what was asked ("plot degree distribution"), but a
   grader preferring a CCDF would see the tail scatter as a weakness.

3. **The interpretation sentences about the CC2 drawing** ("two hubs", "long chain to
   the upper right") describe the specific rendering. The hub degrees are computed
   (exactly one node each of degree 7 and 6, verified), but "upper right" is read off
   the layout and would move if the layout algorithm or matplotlib version changed.
   The topological facts (69 nodes, 80 edges, diameter 17, 12 cycles) are layout-
   independent and are the load-bearing claims.

4. **Everything rests on the pinned construction convention.** If that convention is
   wrong (e.g. if the grader intended isolated nodes from some node list, or a
   directed reading), every number changes. I verified the convention is
   self-consistent and reproduces the master's counts three independent ways, but I
   cannot verify the *intent* from the assignment text, which just says "create
   undirected graph using edge list file". I consider this low risk — my Q3 counts
   are pinned to agree with worker p3's for Q5.
