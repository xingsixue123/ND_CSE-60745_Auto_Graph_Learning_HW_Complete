# p3 — Q5: Graph Measures (30 pts) — submission

## What the problem asked

Three parts, all on the graph built in Q3 from `graph.txt` (attached as
`input/graph-1.txt`):

1. Eigenvector centrality; report the top-10 nodes. "You can use default
   parameters in NetworkX." (10 pts)
2. Katz centrality; report the top-10 nodes. Same note about defaults. (10 pts)
3. Average clustering coefficient over all nodes, and average Jaccard similarity
   of all connected node pairs. (10 pts)

**Brief vs. assignment page — no disagreement.** I checked all three channels of
rendered page 3 (rule R7):
- `page_003.txt` lines 20–27 contain Q5 word for word, matching `problem.md`.
- `page_003.png` read as an image: same three sub-questions, same 10/10/10 split.
- Figure channel: **no `page_003_fig_*` file exists**. The only extracted figure in
  the entire ingest is `page_002_fig_01.jpeg`, which belongs to Q1/Q2 on page 2.
  So Q5 genuinely has no figure, as the brief states.

(Minor, not a discrepancy: the page footer reads "Page 2 of 4" because a cover page
offsets the numbering. I cite rendered index 3 throughout, per env.md.)

## What I decided it needed

**`code` only.** Every part asks for a computed number or ranking. No verb in Q5 is
"plot"/"show"/"visualize"/"draw" — those appear in Q4, which belongs to another
worker. So no figure is required and I did not invent one.

## What I did

Built the graph under the pinned convention and confirmed it reproduces the
master's reference numbers exactly before computing anything.

For each of the two centralities I followed the protocol the brief demanded: call
the **default** NetworkX function first inside a `try/except
PowerIterationFailedConvergence` and record honestly what happened. **Both default
calls converged** — contrary to the brief's expectation — so both headline answers
are the default-parameter results, and no method substitution was needed.

I did not stop at that, though, because a converged call is not necessarily an
accurate one. I recomputed each quantity a second and third way (exact `*_numpy`
variants, plus my own `scipy` eigensolve / sparse linear solve / hand-rolled set
arithmetic) and compared. That is how I found the one genuinely interesting result
in this problem: **the default eigenvector call converges but is not accurate
enough to settle ranks 7 and 8.** NetworkX stops when the *total* $L^1$ change
drops below `n*tol` = 26728 x 1e-6 ≈ 2.67e-2, a loose absolute bound on a
unit-norm vector. The returned vector has residual 7.8e-3 and swaps nodes 9068 and
17902 relative to the exact eigenvector. I report the default answer as the
headline (that is what was asked) with the exact column beside it and an
explanation, rather than quietly reporting one and hiding the other.

For Katz I checked the admissibility condition alpha < 1/lambda_max explicitly, since
alpha=0.1 is close to the boundary here.

I also verified the graph is disconnected-but-dominated-by-the-giant-component
rather than assuming it: I computed the spectral radius of *every one* of the 4104
components to confirm which one carries the Perron vector.

## Intermediate steps and code

Paths relative to PLAYGROUND. Run everything with
`PYTHONPATH=scripts /home/xing/miniconda3/envs/py311/bin/python <script>`.

| script | what it does |
|---|---|
| `scripts/build_graph.py` | shared graph constructor + invariant checks. Run directly to print node/edge/component counts. |
| `scripts/q5a_eigenvector.py` | part (a): default call, numpy call, raised-`max_iter` call; top-10 for each. |
| `scripts/q5_spectrum.py` | lambda_max via `eigsh`, Katz admissibility check, per-component spectral radii. |
| `scripts/q5b_katz.py` | part (b): default call, numpy call, my own `spsolve` of (I-alpha A)x=beta*1. |
| `scripts/q5c_clustering_jaccard.py` | part (c): both quantities via NetworkX and via hand-rolled code, plus the endpoints-excluded Jaccard variant. |
| `scripts/q5a_verify.py` | networkx-version cross-check (runs under **both** interpreters, no scipy) + Rayleigh/residual diagnosis of the default vector. |
| `scripts/q5a_exact_check.py` | independent Perron vector via my own `eigsh`; emits the final table rows. |

JSON results land in `results/`. LaTeX test-compile harness in `build/`.

Which command reproduces which number:
- graph counts, lambda_max → `build_graph.py`, `q5_spectrum.py`
- eigenvector table (both columns) → `q5a_exact_check.py` ("FINAL TABLE ROWS")
- eigenvector residual/Rayleigh, ~0-centrality fractions, degree overlap → `q5a_verify.py`
- Katz table → `q5b_katz.py`
- clustering + Jaccard → `q5c_clustering_jaccard.py`

## Results

Graph (confirms the master's reference): **26728 nodes, 26377 edges, 4104
components**, largest component 13903 nodes / 16695 edges, second largest 69.
No self-loops; 26377 lines == 26377 distinct edges (no duplicates); degree sum
52754 == 2|E|.

**Spectral radius** (`q5_spectrum.py`): lambda_max = **8.762217269069**,
1/lambda_max = **0.114126364286**. Default Katz alpha=0.1 < 0.114126, so **admissible**.
Giant component has the largest spectral radius (8.7622; next largest component
radius is 3.633), confirmed by scanning all 4104 components.

**(a) Eigenvector centrality** — `nx.eigenvector_centrality(G)`, defaults,
**converged** (no exception). Bit-identical under networkx 3.3 and 3.6.1.

| rank | node | deg | default | exact (`_numpy`) |
|---|---|---|---|---|
| 1 | 16485 | 57 | 0.491844 | 0.492371 |
| 2 | 22777 | 59 | 0.419863 | 0.422581 |
| 3 | 14618 | 38 | 0.177656 | 0.177494 |
| 4 | 21928 | 17 | 0.139183 | 0.139695 |
| 5 | 2884 | 29 | 0.133813 | 0.133861 |
| 6 | 1197 | 18 | 0.133186 | 0.133738 |
| 7 | 9068 | 51 | 0.111138 | 0.102654 |
| 8 | 17902 | 32 | 0.109219 | 0.109103 |
| 9 | 1324 | 20 | 0.100115 | 0.100053 |
| 10 | 25747 | 19 | 0.094368 | 0.094399 |

Top-10 **sets** are identical; ranks 7/8 are swapped between the two columns.
Default vector: Rayleigh quotient 8.7620165 (vs true 8.7622173), inf-residual
7.845e-03, L1 residual 2.212e-01. Power iteration at `max_iter=1e5, tol=1e-10`
reproduces the exact column to 9.269e-07. My own `eigsh` Perron vector matches
`eigenvector_centrality_numpy` to **1.235e-15** with residual 1.554e-14.
Supporting stats: 12908 nodes (48.29%) below 1e-12; all top-10 in the giant
component; overlap with top-10-by-degree is 6/10.

**(b) Katz centrality** — `nx.katz_centrality(G)`, defaults (alpha=0.1, beta=1.0),
**converged**.

| rank | node | deg | katz (default) | exact |
|---|---|---|---|---|
| 1 | 16485 | 57 | 0.211609 | 0.211622 |
| 2 | 22777 | 59 | 0.175512 | 0.175524 |
| 3 | 9068 | 51 | 0.109482 | 0.109484 |
| 4 | 14618 | 38 | 0.099380 | 0.099385 |
| 5 | 2884 | 29 | 0.074102 | 0.074105 |
| 6 | 17902 | 32 | 0.070590 | 0.070592 |
| 7 | 17546 | 40 | 0.068771 | 0.068771 |
| 8 | 21928 | 17 | 0.066834 | 0.066838 |
| 9 | 1197 | 18 | 0.061642 | 0.061645 |
| 10 | 9740 | 27 | 0.060545 | 0.060545 |

Ordering identical across all three methods. max|default - numpy| = 1.336e-05;
max|numpy - my spsolve| = 1.943e-16. All entries of the unnormalised solution are
positive (min 1.111111), consistent with alpha being admissible.

**(c)** `nx.average_clustering(G)` = **0.1005391519394419**, reported as
**0.100539**. Hand-rolled recomputation agrees to 0.0 (py311) / 1.9e-16 (base).
Supporting: 13942 of 26728 nodes (52.16%) have degree < 2 and contribute 0; 1926
triangles total; mean over the 12786 nodes of degree >= 2 is 0.210168.

Average Jaccard over all 26377 edges = **0.0413042245649883**, reported as
**0.041304**. `nx.jaccard_coefficient` and my hand-rolled version agree to 0.0
(py311) / 6.4e-16 (base). Exactly 26377 pairs scored. 21167 edges (80.25%) score
0; max is 0.666667; no edge scores 1. Endpoints-excluded variant would be
0.0843047818 — stated in the answer as a contrast, clearly not the reported value.

## Deliverables

- `OUTPUT/answer.tex` — LaTeX fragment, 3 subsections, two booktabs tables.
  No `\documentclass`/`\usepackage`/`document` env (checked by grep). Both labels
  namespaced: `p3:tab:eig`, `p3:tab:katz`.
- `OUTPUT/preamble.txt` — `booktabs`, `float`, `amsmath`.
- No figures (not required; see "What I decided it needed").

Verified: compiles standalone with exactly that preamble via `pdflatex`, exit 0,
**zero** overfull/underfull/undefined warnings, 3 pages. I rendered all pages to
PNG and looked at them. `framework/tools/lint_output.py` → `OUTPUT LINT OK`.
Nothing installed; `downloads.md` records `(nothing installed)` with rationale.

## Where I am least confident

1. **Which eigenvector column should be the headline.** The question says "you can
   use default parameters", the default call converged, and the brief said to use
   it in that case — so I made the default column the answer. But the default
   column is *demonstrably* slightly wrong (ranks 7/8). A grader with a reference
   solution computed via `_numpy` would see 17902 before 9068. I show both columns
   and explain, so either expectation is satisfied, but if the validator thinks the
   exact column should be the headline instead, that is a one-line reorder and a
   defensible different call. This is the single judgement call in this problem.
2. **The Jaccard convention.** I used NetworkX's raw-neighbour-set definition, as
   the brief pinned, and stated the formula explicitly. "All connected node pairs"
   is unambiguous (= all edges) and I verified exactly 26377 pairs were scored. But
   if the course intended common-neighbour sets excluding the endpoints, the answer
   is 0.084305 instead. I state both, with the reported one clearly marked.
3. **networkx version.** All numbers were reproduced under 3.3 and 3.6.1 and were
   bit-identical for the pure-Python routines, so I do not think version drift is a
   risk. The scipy-backed `_numpy` variants were only run under py311 (base python3
   has no scipy), but I cross-checked those against my own eigensolve/spsolve
   rather than trusting a single routine.
4. Everything else (graph counts, lambda_max, clustering, Jaccard) is confirmed by at
   least two independent implementations and by global invariants (degree sum =
   2|E|, pair count = |E|, per-component spectral radii reconciling with the global
   lambda_max), so I consider those solid.
