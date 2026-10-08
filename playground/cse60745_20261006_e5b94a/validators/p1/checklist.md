# Validator checklist — problem p1 (HW3-Part(A) Q1, Q2, Q3, Q5)

## Round 1
Verdict: PASS

### What I verified independently (not taken from submission.md)

**Ground truth (R7).** Read `page_002.txt` / `page_003.txt`, `page_002.png` /
`page_003.png`, and `page_002_fig_01.png` at native resolution. The brief's
transcription of Q1/Q2/Q3/Q5 is faithful to the page. The document's one embedded
figure is a screenshot of the `MyGCNConv` stub and matches notebook cell 15; it
carries no information not already in the notebook. No brief-vs-page conflict.

**Harness not tampered with.** Diffed `run/common.py` against notebook cells 2, 4, 6,
8, 10, 11: `evaluate_ranking`, `GNNLinkPredictor` and `train_and_eval` are verbatim.
The only deviations are the two the file documents (task3 download dropped, node2vec X
cached). Diffed `Practice3_pyg_basics_completed.ipynb` against the shipped notebook:
exactly cells 15, 18, 21, 30 (the four stubs) and 31 (`n_layers`, the sanctioned
change) differ; all 32 cells present.

**Listings == code that was run.** Extracted the four `lstlisting` blocks from
`answer.tex` and diffed each against the corresponding class in `run/layers.py`:
all four IDENTICAL. The same four classes are byte-identical to the completed
notebook's cells.

**Layer correctness.** Copied `test_layers.py` into my own dir and re-ran it:
`MyGCNConv` vs `GCNConv` 0.0, hand-computed 4-node graph 2.4e-7, `MyGATConv` vs
`GATConv` (8 heads) 0.0, `MyGINConv` vs `GINConv` 0.0 with the difference under an
injected self-loop confined to exactly the self-loop nodes, `MyDeepConv` vs `APPNP`
0.0, `reset_parameters()` safe twice. ALL CHECKS PASSED.

**Numbers.** Re-ran `run_all.py` from my own copy against the cached X. Five of the
six table rows reproduce to 4 d.p. (GraphSAGE 0.6281, GCN-2 0.7379, GAT 0.6365,
GIN 0.4417, GCN-8 0.3919). MyDeepConv came out test MRR 0.7510 / Hit@1 0.6461 against
the reported 0.7492 / 0.6421 — float-scatter non-determinism interacting with
early-stopping epoch choice (132 vs 134), consistent with the worker's own
`robustness.json` repeat spread. Re-ran `gin_probe.py`: 0.868 / 0.632 and
22.90x / 2.07x, exactly as quoted.

**Independent recomputation.** Wrote my own probe measuring the Q3 degree-coupling
claim *after* training rather than at initialisation: GIN norm ratio 22.6x vs GCN
2.35x at the early-stopping checkpoint, so the operator-bias claim survives training.
(The log-log correlation gap narrows, 0.776 vs 0.744 — the answer only claims the
initialisation numbers and labels them as such, so it is not overstating.)
Recomputed the 3-seed means from `sweep_seeds.json`: GCN 0.7244 -> 0.3972 is a 45.2%
drop, matching the "45%" in the text.

**Notebook actually runs.** Executed `Practice3_pyg_basics_completed.ipynb` end to end
in a clean directory with a fresh node2vec draw (Q4 cells 23-27 skipped, as designed):
exit 0, "NOTEBOOK RAN TO COMPLETION". GraphSAGE 0.6331, GCN 0.7400, GAT 0.6365,
GIN 0.4448, GCN-8 0.3916, MyDeepConv (K=8, n_layers=1) 0.7515. Same ordering as the
reported table on independent features, which is the claim the answer makes.

**Citations (R9) — opened both sources myself.** Downloaded arXiv 1810.05997 (APPNP).
Both quoted fragments are verbatim and in context: "...is independent of the random
walk's starting (root) node x. This global property is therefore unsuitable for
describing the root node's neighborhood", immediately preceding the paper's own
personalized-PageRank proposal — which is the fix the worker implements, so the
argument survives its context. "the original paper uses alpha = 0.1 with K = 10" is
verbatim from its experimental setup. For Li, Han & Wu, read `run/logs/li2018.txt`
around Theorem 1 and the Co-Training/Self-Training sections: the convergence claim and
the "proportional to the square root of the vertex degree" phrasing are the paper's
own, and the remedy really is co-training with ParWalks plus self-training on a
shallow GCN. The answer states that remedy rather than asserting the authors left the
problem unaddressed. R9 satisfied.

**LaTeX / compliance.** No `\documentclass`, `\usepackage`, `document` env,
`\bibliography`, `.bib` or absolute path in `answer.tex` (R5). Every defined name is
namespaced: `p1kw`, `p1str`, `p1cmt`, `p1pystyle`, `p1:fig:depth`, `p1:tab:results`,
`p1:li2018`, `p1:appnp`; figure referenced as bare `fig_p1_depth.pdf`. Compiled the
fragment in a minimal wrapper: `latexmk -pdf` exit 0, 5 pages, no errors, no undefined
references, no overfull/underfull boxes. Rendered all 5 pages and read them.
`lint_output.py` -> OUTPUT LINT OK. `downloads.md` covers the venv, every pip package,
both redirected caches, the data files and the cached features (R3). No Q4 content
leaked into the answer.

**Figure.** Opened `fig_p1_depth.pdf`: 5.4 x 3.5 in, zero raster images, 34 vector
drawings, TrueType embedded, axes labelled ("Receptive field (hops)" / "Test MRR"),
two-entry legend, no title, data matches `sweep_seeds.json` means. Legible at print
size.

**Length (R8).** Prose only, listings/table/bibliography excluded: Q1 168, Q2 211,
Q3 223, Q5 427 (of which ~110 belongs to the once-only table/figure/caveat), preamble
61, total 1113 words for 24 points. Each section carries sub-parts the brief demanded
(Q2's concat-vs-average discussion, Q5's mechanism + hop arithmetic + figure reading +
reproducibility caveat). Within tolerance; not a defect. Em-dashes 14, i.e. one per
~80 words, under the R8 warning threshold.

### Defects
- [1.1] The shaded min-max band in `fig_p1_depth.pdf` is never defined — not in the
  figure (no legend entry, no annotation) and not in the surrounding prose, which only
  says the line is a "mean over three seeds". A grader sees an unexplained envelope. |
  `OUTPUT/fig_p1_depth.pdf`, `run/make_fig.py:34-36` | severity: minor
- [1.2] `answer.tex:306` quotes the MyDeepConv depth sweep as
  "$0.725, 0.726, 0.726, 0.725$ at $2, 4, 6, 8$ hops". The 4-hop 3-seed mean in
  `run/logs/sweep_seeds.json` is 0.72549, i.e. 0.725 to three decimals; 0.726 comes
  from rounding twice (to 0.7255, then up). Off by 0.0005; does not touch the "flat in
  depth" claim. | `OUTPUT/answer.tex:306` | severity: minor
- [1.3] `\label{p1:fig:depth}` (`answer.tex:300`) and `\label{p1:tab:results}`
  (`answer.tex:327`) sit inside `figure`/`table` environments that have no `\caption`,
  so they bind to the enclosing counter rather than to a float number. Nothing `\ref`s
  them, so nothing breaks as shipped — but if the master adds its caption *after* the
  label the resulting reference will point at the wrong number. Safer to drop the
  labels or note that a caption must precede them. | `OUTPUT/answer.tex:300,327` |
  severity: minor
- [1.4] `run/tune_deep.py:16` constructs `MyDeepConv.__init__(..., dropout=d)`, but the
  shipped `run/layers.py` `MyDeepConv.__init__(self, in_channels, out_channels, K=8,
  alpha=0.3)` has no `dropout` parameter (it was removed after tuning). Re-running the
  script now raises `TypeError: unexpected keyword argument 'dropout'`, so the 9-point
  (alpha, dropout) grid that `submission.md` cites as the basis for alpha=0.3 cannot be
  reproduced. No number in `answer.tex` depends on it, and `logs/tune_deep.json`'s
  alpha=0.3/dropout=0.0 row (val 0.73768, epoch 134) matches the shipped model's
  val 0.73757 at epoch 134, which confirms the removal was numerically a no-op. |
  `run/tune_deep.py:16` | severity: minor
- [1.5] `submission.md` claims the completed notebook was executed end to end, but
  `nbcheck/` holds only the downloaded data — no console log of that run was kept,
  unlike every other claim, which has a log. I executed it myself and it does pass, so
  this is an evidence gap rather than a false claim. | `nbcheck/` | severity: minor

### Resolved since last round
(first round — nothing to resolve)

### Still outstanding
[1.1]–[1.5], all minor. None of them changes a reported number, a claim's truth value,
or the final compile. Passing with them noted, per the standing instruction not to
withhold a pass for cosmetic objections.
