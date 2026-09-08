# p3 — Q5 Graph Measures — working notes

## Verification of the brief against the assignment page (rule R7)

Rendered page 3 (`ingest/pages/CSE 60745_Fall 2026_HW1/page_003.png` + `page_003.txt`).

- Text channel (`page_003.txt`, lines 20-27) contains Q5 verbatim, matching the brief
  word for word.
- Page-image channel: read the PNG. Same three sub-questions, same point split
  (10/10/10). Header "Part B – Graph Essentials and Measures (70 pts)".
- Figure channel: **there is no `page_003_fig_*` file at all**. The only extracted
  figure in the whole ingest is `page_002_fig_01.jpeg`, which belongs to Q1/Q2 on
  page 2, not to Q5. So Q5 genuinely has no figure, exactly as the brief says.

Conclusion: brief and page agree. No discrepancy to report.

Note: the page footer says "Page 2 of 4" while this is rendered page index 3 (a cover
page offsets it). I cite the rendered index, per env.md.

## What this problem needs

**code only.** Every one of the three parts asks for a computed number or ranking:
top-10 eigenvector centrality, top-10 Katz centrality, average clustering
coefficient, average Jaccard similarity. No "plot"/"show"/"visualize"/"draw" verb
appears anywhere in Q5 (those verbs are in Q4, which is a different worker's
problem). So: no figure required. I will not invent one.

## Plan

1. Build `nx.Graph` from `input/graph-1.txt`, tab-separated int pairs, one edge per
   line. Confirm 26728 nodes / 26377 edges / 4104 components against the master's
   reference numbers.
2. Eigenvector centrality: call `nx.eigenvector_centrality(G)` with **defaults
   first**, in a try/except. Record honestly whether it converges. If
   `PowerIterationFailedConvergence`, fall back to `eigenvector_centrality_numpy`
   and say so explicitly in the answer.
3. Katz: same protocol with `nx.katz_centrality(G)` (defaults alpha=0.1, beta=1.0).
   Also compute lambda_max to check the admissibility condition alpha < 1/lambda_max.
4. `nx.average_clustering(G)` — state the degree<2 => 0 convention.
5. Jaccard over all 26377 edges via `nx.jaccard_coefficient(G, G.edges())`; state the
   formula |N(u) n N(v)| / |N(u) u N(v)| with raw neighbour sets.
6. Cross-check the headline numbers with an independent implementation (numpy/scipy
   eigensolve for eigenvector centrality, direct linear solve for Katz, hand-rolled
   set arithmetic for Jaccard and clustering) so nothing rests on a single call.

## Environment decision

scipy is absent from base python3 but `eigenvector_centrality_numpy` /
`katz_centrality_numpy` need it. Check `/home/xing/miniconda3/envs/py311/bin/python`
for networkx; if it lacks it, build a venv in the playground and record in
downloads.md.
