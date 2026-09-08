# Validator checklist — p3 (Q5: Graph Measures, 30 pts)

## Round 1
Verdict: PASS

### Method used to audit
Did **not** re-run the worker's scripts as primary evidence. Wrote an independent
recomputation from scratch (`indep_check.py` in this dir): own file parser, own
`nx.Graph` build, own power iteration on a self-built sparse matrix, own
`spsolve` of $(I-\alpha A)x=\beta\mathbf{1}$, own set-arithmetic clustering and
Jaccard. Ran it under **both** interpreters (py311/nx 3.3/scipy and base/nx 3.6.1).

### Question fidelity (R7)
- `page_003.txt` and `page_003.png` both read. Q5 text matches `problem.md`
  verbatim; 10/10/10 split confirmed.
- Figure channel: listed the whole ingest dir — the only extracted figure is
  `page_002_fig_01.jpeg` (belongs to Q1/Q2). **No `page_003_fig_*` exists**, so
  Q5 genuinely has no figure. Worker's `needs = code only` is correct; the
  plot/visualize verbs on page 3 belong to Q4, a different worker's problem.
- All four deliverables present: eigenvector top-10 table, Katz top-10 table,
  average clustering (single number), average Jaccard (single number).

### Numbers independently reproduced (all exact matches)
- Graph: 26728 nodes / 26377 edges / 4104 components; LCC 13903 n / 16695 e;
  2nd = 69. Invariants: 26377 lines = 26377 distinct undirected pairs (no
  duplicates), 0 self-loops, degree sum 52754 = 2|E|.
- $\lambda_{\max}=8.762217269069$, $1/\lambda_{\max}=0.114126364286$;
  $\alpha=0.1$ admissible. Per-component radii: giant 8.7622, next 3.6331 —
  matches the answer's "at most 3.63 for every other component".
- Eigenvector **default** call converges (no exception) — worker's claim that it
  converged, contra the brief's expectation, is correct. All 10 default values
  match to the printed 6 dp.
- Eigenvector **exact** column matches `_numpy` and my own power iteration
  (agreement 1.7e-14). Ranks 7/8 really do swap (17902 above 9068 exactly).
- Default-vector diagnostics: Rayleigh 8.7620165, inf-residual 7.845e-03 — as
  stated. 12908 nodes (48.29%) below 1e-12 — as stated.
- Katz: all 10 values match; default vs exact 1.336e-05, numpy vs my spsolve
  1.943e-16; min unnormalised entry 1.111111 > 0.
- Clustering 0.10053915193944186 -> 0.100539; 13942 nodes deg<2 (52.16%);
  1926 triangles; mean over deg>=2 = 0.210168. All confirmed.
- Jaccard 0.04130422456498827 -> 0.041304 over exactly 26377 pairs; 21167 zero
  edges (80.25%); max 2/3; endpoints-excluded variant 0.084305. All confirmed.

### Interpretive claims spot-checked (all correct)
- NetworkX stop rule is literally `sum(abs(x[n]-xlast[n]) for n in x) < nnodes*tol`
  — the answer's $n\cdot\texttt{tol}\approx2.67\times10^{-2}$ explanation is
  accurate, not hand-waving. Defaults verified from the signatures
  (ev: max_iter=100, tol=1e-6; katz: alpha=0.1, beta=1.0, max_iter=1000, tol=1e-6).
  Both normalise to unit $L^2$ (verified norm = 1.0).
- "6 of 10 also in top-10 by degree": overlap is exactly 6
  {2884, 9068, 14618, 16485, 17902, 22777}. Correct.
- "Node 9068 is the entry still furthest from its limit": it is the argmax of
  |default - exact| (0.008484). Correct.
- "max_iter=1e5, tol=1e-10 reproduces the exact column to 9.3e-7": measured
  9.268915742016715e-07. Correct.
- "Bit-identical under nx 3.3 and 3.6.1": verified — both default top-10 lists
  identical across the two versions.

### Compliance
- R5: no `\documentclass` / `\usepackage` / `document` env. Both labels
  namespaced (`p3:tab:eig`, `p3:tab:katz`). No figures, no absolute paths.
- Compiles in a minimal wrapper with exactly the declared preamble
  (booktabs, float, amsmath): exit 0, **zero** overfull/underfull, no undefined
  refs, 3 pages. Rendered all 3 pages to PNG and read them — tables legible,
  well-formed, nothing clipped or overflowing.
- R4: `lint_output.py` -> `OUTPUT LINT OK` (exit 0). OUTPUT holds only
  `answer.tex` + `preamble.txt`.
- R3: `downloads.md` present, records `(nothing installed)` with rationale;
  no venv or download was in fact made.

### Defects
- [1.1] `\label{p3:tab:eig}` (answer.tex:37) and `\label{p3:tab:katz}`
  (answer.tex:100) sit inside `table` environments that have **no** `\caption`,
  so the label binds to the subsection counter rather than a table counter.
  Verified: `\ref{p3:tab:eig}` renders as "1.1", not a table number. |
  `OUTPUT/answer.tex:37,100` | severity: **minor** (cosmetic — the labels are
  correctly namespaced so there is no collision risk, nothing in the fragment
  or elsewhere references them, and it compiles clean; it self-corrects if the
  master adds captions).

### Judgement calls reviewed, not counted as defects
- **Headline eigenvector column.** Worker flagged this as its least-confident
  call. Its choice (default column is the headline, exact shown alongside with
  an explanation) is what the question ("you can use default parameters") and
  the brief ("if the default call converges, use it and say so") both direct.
  The 7/8 discrepancy is disclosed rather than hidden, so a grader with either
  reference solution can follow it. Correct call; no change requested.
  Side effect: the "exact" column is non-monotonic at ranks 7/8, but the Remark
  paragraph explains exactly why, so it will not read as an arithmetic error.
- **Jaccard convention.** Raw-neighbour-set definition, as the brief pinned;
  the formula is written out in the answer and the alternative value (0.084305)
  is given as an explicit contrast. The ambiguity is surfaced to the grader
  rather than buried. Acceptable.
- Significant figures suffice to separate every adjacent pair in both tables
  (tightest: Katz ranks 7/8, 0.068771 vs 0.066834).

### Resolved since last round
(n/a — first round)

### Still outstanding
- [1.1] minor, cosmetic. Not worth another round on its own.
