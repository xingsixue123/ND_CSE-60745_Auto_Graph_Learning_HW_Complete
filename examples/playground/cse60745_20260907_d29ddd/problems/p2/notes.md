# p2 notes — Q3 Graph Creation + Q4 Graph Essentials

## Channel reconciliation (rule R7)
Rendered page 3 of `ingest/pages/CSE 60745_Fall 2026_HW1/`.
- text (`page_003.txt`): matches `problem.md` verbatim question text.
- page image (`page_003.png`): text-only page, no figure region.
- figure files: **none exist** for page 003 (`ls` shows only `page_002_fig_01.jpeg`).
All three channels agree. No figure to transcribe. Brief and page do not disagree.

## What this problem needs
- **code** — every requested item is a computed number (node/edge/component counts,
  LCC counts, degree stats). Must actually run networkx, not estimate.
- **diagram** — two figures are explicitly demanded:
  - "Show visualization of the second largest connected component" -> fig_p2_cc2.pdf
  - "Plot degree distribution of the whole graph" -> fig_p2_degree_dist.pdf
- **plain** — short prose stating method + numbers. No code listing (brief forbids it).

## Construction convention (pinned by master, must match worker p3)
`nx.Graph()`, one node per distinct id in `input/graph-1.txt`, one edge per
tab-separated line. Undirected simple graph. No isolated nodes added.
Master's expected check: 26728 nodes / 26377 edges / 4104 components. Reproduce.

## Tooling
`/home/xing/miniconda3/envs/py311/bin/python` has networkx 3.3 + matplotlib 3.10.8.
Base `python3` has networkx 3.6.1 but no matplotlib.
=> No venv needed, nothing to install, `downloads.md` stays empty.
Cross-check the Q3/Q4 counts under BOTH networkx versions to rule out a version artifact.
Need `MPLCONFIGDIR` set to a writable playground dir.

## Plan
1. `analyze.py` — build graph, emit all counts to `results.json` + `results.txt`.
2. `crosscheck.py` — recompute counts with base python3 (nx 3.6.1) and with a
   pure-Python union-find that uses no networkx at all. Three independent agreements.
3. `figs.py` — produce the two vector PDFs, then render to PNG and LOOK at them.
4. Write `OUTPUT/answer.tex` fragment, namespaced `p2:`. Lint. Write submission.md.

## Tie-breaking note for the 2nd LCC
Master warns 3rd place is tied at 30 nodes. 2nd place (69) should be unique — verify
explicitly by printing the top component sizes, and state the selection rule used.
