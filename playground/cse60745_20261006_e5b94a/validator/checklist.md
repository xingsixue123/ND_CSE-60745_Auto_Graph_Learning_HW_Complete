# Master validator checklist — job cse60745_20261006_e5b94a
Assignment: CSE 60745 (Fall 2026) HW3-Part(A): GNNs Hands-on Practice, 30 pts, Q1–Q5 @ 6 pts.

## Round 1 — 2026-10-06
Verdict: **FAIL** (one major defect; everything substantive I could test checked out)

### What I did, and where I looked

**Assignment enumerated independently (R7, all three channels).**
`ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/` — `alltext.txt` + `page_001..003.png` +
the one embedded figure `page_002_fig_01.png` read at native 727x525. The figure is a
screenshot of the `MyGCNConv` stub and fixes the four required method signatures
(`__init__(in_channels, out_channels)`, `reset_parameters`, `forward(x, edge_index)`,
`message(x_j)`); text and page image agree and carry nothing the figure does not.
My own question list, derived from the pages and *not* from `problems.json`:
Q1 GCN, Q2 GAT, Q3 GIN, Q4 R-GCN, Q5 deep/over-smoothing — 5 x 6 = 30 pts.
All five are answered in `final/main.pdf`, in order, each under its own `\section*`
heading with the assignment's own wording and point value. Cover page reproduced
(rendered page 1). Points covered: 30/30. **Coverage: no gap.**

**Every implementation re-verified numerically, from the PDF's own source.**
I extracted all five `lstlisting` blocks out of `final/p1a.tex`, `final/p2.tex`,
`final/p1b.tex` (so I tested the code a grader actually reads, not the worker's
`layers.py`) into `validator/r1/extracted_layers.py` and ran them against PyG's
reference layers with parameters copied across (`validator/r1/verify_layers.py`,
run under the p1 worker's venv):

| layer | reference | max abs diff |
|---|---|---|
| `MyGCNConv` | `GCNConv` | 0.0 |
| `MyGCNConv` (self-loops already in edge_index) | itself | 0.0 (idempotent, as claimed) |
| `MyGATConv` (heads=8, concat) | `GATConv` | 0.0 |
| `MyGINConv` | `GINConv(train_eps=True)` | 0.0 |
| `MyRGCNConv` | `RGCNConv(aggr='mean', num_bases=None)` | 4.8e-07 |
| `MyDeepConv` | `APPNP(K=8, alpha=0.3)` | 0.0 |

Parameter counts reproduced independently: MyDeepConv 8,320 = 2-layer GCN 8,320 =
8-layer GCN 33,280 / 4, exactly as Q5 claims. Requirement compliance: Q2 uses
`torch_geometric.utils.softmax` and is multi-head (K=8, `node_dim=0`); Q4 is the basic
R-GCN (one full `[in,out]` matrix per relation + `W_0`, no basis/block decomposition);
Q5 reaches 8 hops at `n_layers=1`, which is the point the assignment's own note makes.

**Every reported number recomputed or traced to a log.**
- Table 1 (all 24 cells) matches `problems/p1/run/logs/results.json` to the digit.
- Figure 1 / the depth claims recomputed from `logs/sweep_seeds.json`: GCN
  0.724 -> 0.397 is a 45.2% drop; MyDeepConv means are 0.725, 0.725, 0.726, 0.725.
  **The master's one edit to the worker's text (0.726 -> 0.725 at 4 hops) is correct** —
  the true mean is 0.72549. The master also added the two missing `\caption`s; the
  worker had shipped `\label`s inside caption-less float environments.
- Q3's degree/norm numbers: I re-ran `run/gin_probe.py` myself — +0.868 / +0.632 and
  22.90x / 2.07x, against the 0.87 / 0.63 / 22.9x / 2.1x printed. Correct.
- Q5's alpha plateau: `logs/tune_alpha.json` gives val MRR 0.733–0.737 over
  alpha in [0.25, 0.5] and 0.699 at 0.2. Correct. (alpha=0.4 is nominally 7e-5 higher
  than 0.3 on val; the answer calls it a plateau and alpha=0.3 won the earlier
  (alpha, dropout) grid in `tune_deep.json`, so the claim stands. Withdrawn, not a defect.)
- Q4: val 0.2291 / 0.0782, test 0.2229 / 0.0714 match `rgcn_run.log` epoch 13.
  The five-draw spread 0.190+-0.020 / 0.182+-0.023 is the population sd of
  `rgcn_run_1..5.log`. PyG parity 0.208 and 4e-7 match `check_vs_pyg.log`.
  Pooling 0.305 / friend-only 0.325 / x1.00, x0.98, /22 match `ablation.log`.
  Chance MRR over 21 candidates: H_21/21 = 0.1736 -> 0.174, confirmed by hand.
  Loss settling at ln 2: `diagnose.log` shows 0.6932–0.6937. All correct.

**Every quotation and characterisation opened at source (R9).**
- Li, Han & Wu (AAAI 2018), arXiv 1801.07606: "proportional to the square root of the
  vertex degree" is the paper's *own* wording immediately before Theorem 1. Their
  remedies are co-training with a random-walk model + self-training (secs. "Co-Train a
  GCN with a Random Walk Model", "GCN Self-Training"), and their Conclusions defer
  "new convolutional filters which are compatible with deep architectures" to future
  work — so "does not make deep propagation safe" is accurate, not a straw man.
- APPNP (ICLR 2019), arXiv 1810.05997, fetched by me: both quotes are verbatim
  (p. 3: "...is independent of the random walk's starting (root) node x. This global
  property is therefore unsuitable for describing the root node's neighborhood."), and
  the next paragraph is exactly the teleport fix the answer attributes to it.
  alpha=0.1 with K=10 confirmed (sec. 4).
- Schlichtkrull et al. (arXiv 1703.06103v4), read from the p2 worker's copy: Eq. (2)'s
  text does offer "c_{i,r} = |N^r_i|" as the example; the link-prediction section does
  say "we found a normalization constant defined as c_{i,r} = c_i = sum_r |N^r_i| ... to
  work best". Both characterisations accurate.

**The PDF itself (both channels).** `final/main.pdf`, 8 pages, letter, rendered at
200 dpi and read page by page plus full text extraction. Rebuilt from
`final/*.tex` in my own dir: clean `latexmk` exit, 8 pages, **zero Overfull hboxes**.
Figure 1 present and legible at printed size (axis labels, legend and the two
annotated endpoints all readable); it shows what the text says it shows. All equations
typeset, no raw source, no missing-file boxes, no duplicated or orphaned sections,
headers/footers correct, `Page n of 8` resolves. `lint_output.py` passes on both
`p1/` and `p2/`; `final/` holds only tex, the figure and the PDF.

### Defects

- **[D1.1] Q4's prose is ~50% over the R8 length target for a single-part question.**
  `output/.../final/p2.tex` (rendered PDF page 5–6). ~340 prose words excluding code
  and the results tabular. Q4 is one 6-point question with no sub-parts — "Complete
  MyRGCNConv(). Please implement the basic version of R-GCN." — so the R8 target scales
  to ~228 words, and even the 290-word several-sub-parts ceiling does not apply.
  The excess sits in the closing diagnostic paragraph (143 words). Load-bearing part:
  the near-chance MRR needs the "the layer is not the cause" verification, or a grader
  will read 0.223 as a bug. Not load-bearing: the counterfactual normalisation ablation
  from "The normalisation is the lever:" to the end (54 words — 0.305, x1.00/x0.98,
  /22, 0.325) is an extra experiment the question never asked for, and the +-spread
  sentence can lose its second clause.
  **Resolution:** cut ~80–110 words from that paragraph, keeping the chance baseline
  and the PyG-parity check, to land at ~240–260 words. Severity: **major**.

- **[D1.2] Schlichtkrull et al. is leaned on three times in Q4 but is absent from the
  References.** `final/p2.tex` lines 30, 72, 76 — including "their Eq. (2)" and "the
  paper's link-prediction experiments" — yet `final/p1b.tex` is the only file with a
  `thebibliography`, and it lists only Li et al. and Gasteiger et al. A reader cannot
  resolve "their Eq. (2)". **Resolution:** add a `\bibitem{p2:rgcn}` for Schlichtkrull,
  Kipf, Bloem, van den Berg, Titov, Welling, "Modeling Relational Data with Graph
  Convolutional Networks", ESWC 2018 (arXiv:1703.06103), and `\cite` it at the first
  mention. The bibliography is in `p1b.tex`, which the master orders *after* `p2.tex`,
  so this is a master-level assembly fix. Severity: **minor**.

- **[D1.3] The document opens with an orphaned, miscounting paragraph.** Rendered PDF
  page 2, above the Q1 heading (`final/p1a.tex`): "All four layers were run with the
  notebook's own `train_and_eval` harness...". It is true of worker p1's four layers,
  but it is the first sentence of a five-question submission and Q4's R-GCN — which the
  master interleaves at Q4 — runs under `train_and_eval_hetero`. It also carries no
  heading. **Resolution:** reword to name the layers it covers (Q1, Q2, Q3, Q5) or move
  it under a short "Setup" heading. Severity: **minor**.

- **[D1.4] The gensim non-determinism caveat is stated twice.** `final/p2.tex` ("Cell
  26's features come from gensim's `Word2Vec` at `workers=4`, not reproducible across
  processes") and `final/p1b.tex` ("node2vec is rebuilt by `gensim.models.Word2Vec`
  with `workers=4`, which is not deterministic"). These are two *different* feature
  matrices written by two workers, so neither is wrong, but in one assembled document
  it reads as repeated boilerplate. **Resolution:** optional — shorten the Q4 instance
  to a clause. Severity: **minor**.

### Checked and found clean (so the master does not re-litigate these)
- Coverage of all five questions and all four required methods in each layer.
- Numerical correctness of all five layers (table above).
- Every number in Table 1, Figure 1, and the Q3/Q4/Q5 prose.
- Every quotation and every characterisation of a cited paper (R9).
- Compile cleanliness, pagination, figure legibility, label namespacing
  (`p1:`, `p0:` — no collisions), `lint_output.py`, `downloads.md` completeness.
- Q1/Q2/Q3 lengths (158 / 197 / 213 words) — within target.
- Q5 length (407 words) — over the 6-pt single-part target, but Q5 genuinely demands
  four things (literature, implementation, 8-hop-vs-8-layer argument, evidence it
  "stays useful"), so the several-sub-parts ceiling scales to ~348 and 407 is 17% over,
  under the quarter threshold. **Not** reported as a defect.

### Resolved since last round
- n/a (first round).

### Still outstanding
- n/a (first round).

---

## Round 2 — 2026-10-06
Verdict: **PASS**

### What changed, and how I checked it
I diffed the round-2 `final/*.tex` against my own round-1 snapshot, and separately
diffed the *rendered* PDF text (`r1/final_pages/alltext.txt` vs `r2/pages/alltext.txt`).
The rendered diff contains the four fixes, the pagination reflow they cause, and the
citation renumbering — **and nothing else**. No number, no sentence and no line of code
elsewhere in the document moved.

### Resolved since last round

- **[D1.1] fixed.** Q4 prose is now **258 words** (was ~347), measured the same way as in
  round 1 (code and the results tabular excluded). Against the ~228-word R8 target for a
  single-part 6-point question that is 13% over — inside the quarter threshold. The cut
  is exactly the non-load-bearing material I named: the counterfactual normalisation
  ablation ("The normalisation is the lever:" to the end, with 0.305 / x1.00 / x0.98 /
  /22 / 0.325), the `ln 2` loss clause and "so read the table with that spread". The
  load-bearing content survives: the 0.174 chance baseline, the five-draw spread, and
  the PyG-parity check that stops a grader reading 0.223 as a bug. The trimmed paragraph
  reads coherently (rendered page 6) and every surviving number was already verified in
  round 1.
- **[D1.2] fixed.** `\bibitem{p2:rgcn}` added and `\cite{p2:rgcn}` placed at the first
  mention in `p2.tex`. The forward reference across the `p2 -> p1b` input order resolves
  cleanly: **0 undefined citations** in the rebuild, and the PDF renders
  "Schlichtkrull et al. [1]". The master put the new entry *first*, so the References
  are now in citation order ([1] Schlichtkrull, [2] Li, [3] Gasteiger). I checked the
  entry against the paper's own title page: title and all six authors, in order, match
  exactly; ESWC 2018 is the correct venue.
- **[D1.3] fixed.** The opening paragraph now reads "Q1--Q3 and Q5 use
  `train_and_eval` on the social graph; Q4 uses `train_and_eval_hetero` on the
  three-relation graph" — which is exactly right against notebook cells 11 and 27, and
  no longer miscounts in a five-question document.
- **[D1.4] fixed.** Q5's caveat now back-references Q4 ("node2vec carries the same
  `workers=4` nondeterminism noted in Q4") instead of restating it. Q4 precedes Q5, so
  the reference resolves in reading order.

### Regression checks (nothing broke)
- The five `lstlisting` blocks re-extracted from the round-2 `.tex` files are
  **byte-identical** to round 1. I re-ran the PyG comparison anyway: `MyGCNConv` 0.0,
  self-loop idempotence 0.0, `MyGATConv` 0.0, `MyGINConv` 0.0, `MyRGCNConv` 4.8e-07,
  `MyDeepConv` vs `APPNP` 0.0; parameter counts 8,320 / 8,320 / 33,280 unchanged.
- Rebuilt from the shipped sources: clean `latexmk` exit, 8 pages, **0 Overfull hboxes,
  0 undefined references or citations**. `pdftotext` of my rebuild is **identical** to
  `pdftotext` of the shipped `main.pdf`, so the delivered PDF is in sync with the `.tex`.
- Figure 1 still present, referenced by bare filename, unchanged and legible (page 7).
  Table 1 unchanged and correct. Cover page unchanged.
- `lint_output.py` passes on `p1/` and `p2/`; `final/` holds only tex, the figure and
  the PDF.
- Lengths: Q1 158, Q2 197, Q3 213, Q4 258, Q5 405. Q5 is unchanged and remains **not**
  a defect for the reason given in round 1 (four genuine sub-parts -> ~348 scaled
  ceiling; 405 is 16% over, under the quarter threshold). I am not re-litigating a
  defect I declined to raise.

### Still outstanding
None. All four round-1 defects are fixed and verified.

### Noted, not blocking
- `fancyhdr` emits "\headheight is too small (14.0pt)" on every page. Purely cosmetic —
  the underlined header wants ~1pt more — and all eight page renders show no overlap or
  clipping. Not raised as a defect in either round.

### Where I looked and found nothing
Coverage (5/5 questions, 30/30 points, all four required methods per layer); numerical
correctness of all five layers against PyG; every number in Table 1, Figure 1 and the
Q1–Q5 prose; every quotation and characterisation of all three cited papers; compile
cleanliness, pagination, figure legibility, label namespacing, citation resolution, lint
and output hygiene. **Passing with no substantive defects remaining.**
