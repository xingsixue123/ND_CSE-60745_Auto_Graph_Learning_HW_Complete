# p2 — Q4 R-GCN — worker validator checklist

## Round 1
Verdict: FAIL

### What I verified independently (not taken from the worker's own scripts)

- **Question text.** Read `page_003.txt`, `page_003.png` and `page_002_fig_01.png` at
  native resolution. Q4 is transcribed exactly in the brief; the figure is the
  `MyGCNConv` four-method skeleton, matching notebook cell 16. No channel disagreement.
- **The math.** Wrote my own brute-force reference (`recheck/val_reference.py`) from the
  cell-24 equation alone, loaded the *delivered* class out of `rgcn_run.py` by AST, and
  compared on a 9-node/3-relation graph with multi-edges and an all-isolated node:
  **max abs diff 1.19e-07**; isolated node exactly `W_0 h_i`; parameter count
  `(R+1)*in*out+out`; output invariant under duplicating every edge (confirms it is a
  true mean). The implementation is correct.
- **Harness fidelity.** The worker's `verify_fidelity.py` only tests line *membership in a
  set*, which would not catch reordering or a deleted duplicate line. I wrote a stricter
  contiguous-block diff (`recheck/my_fidelity.py`): cells 3, 5, 11, 12, 25, 26, 28 are
  **byte-identical** to the `.ipynb`, and cells 7 and 28 are exact prefixes with only the
  two declared cuts. Harness genuinely frozen.
- **Listing provenance.** `answer.tex` listing == `my_rgcn_conv.py` == cell 27 of
  `rgcn_run.py` == cell 27 of the completed notebook (only cell 27 differs from the
  original, 32 cells both sides).
- **Numbers.** Re-ran `rgcn_run.py` myself: val MRR 0.2221 / test 0.2133, epoch 11
  (worker's run 1: 0.2291 / 0.2229, epoch 13) — consistent given the documented
  `Word2Vec(workers=4)` cross-process nondeterminism. Recomputed the five-run mean/sd
  from the raw logs: 0.190±0.020 val, 0.182±0.023 test — both as claimed. Regenerated
  `answer.tex` via `gen_answer.py` into a scratch dir: **byte-identical** to the
  delivered file, so no number is hand-transcribed.
- **Chance baseline.** Confirmed from the CSVs that every query has exactly 21 candidates
  and 1 positive, so H_21/21 = 0.173589 is the right closed form for 0.174.
- **PyG claim.** `count.clamp(min=1)` confirmed verbatim at
  `torch_geometric/utils/_scatter.py:62`.
- **R9.** Opened `refs/rgcn_1703.06103.pdf` myself. All three quotations verbatim and
  correctly scoped: Eq. (2) offers `c_{i,r}=|N_i^r|` as an example ("such as"); §5.2
  link prediction found the pooled `c_i` "to work best"; §2.2 is titled "Regularization"
  and introduces the two decompositions as regularisers. I also found that §5.1 /
  supplementary **did** use `c_{i,r}=|N_i^r|` for entity classification — the worker's
  careful scoping of the pooled constant to *link prediction* is accurate.
- **Compliance.** `lint_output.py` OK. No `\documentclass`/`\usepackage`/`document`.
  Every defined name namespaced (`p2:sec:rgcn`, `pTwoPyStyle`, `pTwoKw/Cmt/Str/Rule`);
  no digits in control sequences; no macros; no absolute paths; no figures. Compiles in a
  5-section wrapper with 0 errors and no overfull/underfull boxes; I rendered both pages
  and read them — listing and table are legible.
- **R3.** `downloads.md` covers everything present in the playground (.venv, .pipcache,
  refs, run/data).
- **R8.** My own count: 266 prose words (worker says 268). R8 allows "up to 290 if it has
  several sub-parts"; this answer has several. Within target — not a defect.

### Defects

- [1.1] **`answer.tex` states a mechanism its own data contradicts.** Lines 118–121:
  *"Averaging within the two ≈400-degree listening relations smooths the users flat;
  pooling, as the paper's own link-prediction experiments do (c_{i,r}=c_i=Σ_r|N_r(i)|),
  reaches validation MRR 0.286."* The semicolon asserts that pooling helps by fixing the
  within-listening-relation averaging. It does not. Two measurements:
  (a) `recheck/val_mechanism.py` — switching to pooled `c_i` scales each relation's term
  by `|N_r(i)|/c_i`: **listens 1.0000, listened_by 0.9785** (i.e. unchanged), but
  **friend 0.0451, a 22x down-weighting**. Pooling barely touches the listening terms.
  (b) `recheck/val_ablate.py`, 4 variants x 3 seeds through the same harness —
  `A per-relation 0.1895` (control, reproduces the delivered 0.190),
  `B pooled-all 0.2957`, `C friend-pooled-only 0.3294`, `D listening-pooled-only 0.2388`.
  Pooling **only** the friend relation recovers and exceeds the whole gain; pooling only
  the listening relations captures little of it. The cause is the down-weighting of the
  sparse friend relation relative to the dense ones, not smoothing inside the listening
  relations — the stated mechanism in fact predicts the opposite sign, since under
  pooling the (allegedly flat) listening terms dominate *more*.
  Fix: either drop the causal clause and report the pooled result as a bare measured
  aside, or state the mechanism the data supports.
  | `OUTPUT/answer.tex` lines 118–121 | severity: **major**

- [1.2] Same sentence, secondary: "the two ≈400-degree listening relations smooths **the
  users** flat" — relation 1 (`listens`, mean degree 384.4) aggregates into *artists*,
  not users; only relation 2 (404.6) averages into users. Loose even before 1.1.
  | `OUTPUT/answer.tex` line 119 | severity: minor

- [1.3] The headline table reports val 0.2291 / test 0.2229, which is the **maximum** of
  the worker's five runs (others: 0.1698, 0.1810, 0.1824, 0.1888). I accept this is not
  cherry-picking — `submission.md` declares the "report run 1" rule, log mtimes confirm
  `rgcn_run_1.log` was chronologically first, the 0.190±0.020 spread is printed
  immediately below the table, and my own independent run landed at 0.2221. Noting only
  because a grader reads the table first and it sits ~2sd above the mean.
  | `OUTPUT/answer.tex` lines 99–108 | severity: minor

- [1.4] `submission.md` claims "crosscheck.py passes with 0 label collisions". In my run
  `crosscheck.py` printed "skipping p2 -- not finished (running)", so p2's labels were
  not actually examined by it. I verified by hand that the single label is namespaced, so
  there is no real collision risk; the claim is just not currently demonstrable.
  | `submission.md`, Deliverables | severity: minor

### Resolved since last round
(none — first round)

### Still outstanding
[1.1] major, [1.2] [1.3] [1.4] minor.

Everything else — correctness of the layer, fidelity of the harness, provenance of every
number, R5/R7/R9 compliance, LaTeX, lint — passes. [1.1] is the only item that must
change before this ships: it is a wrong technical explanation presented as the answer's
diagnosis, and it is disprovable with one ablation.

---

## Round 2
Verdict: PASS

### Re-verified from scratch (not taken from the worker's scripts or its round-1 state)

- **Harness still frozen.** Re-ran my own contiguous-block diff: cells 3, 5, 11, 12, 25,
  26 byte-identical to the `.ipynb`; cells 7 and 28 exact prefixes with only the two
  declared cuts. Listing in `answer.tex` == `my_rgcn_conv.py` == cell 27 of
  `rgcn_run.py`. The layer source is unchanged from round 1, so the round-1 correctness
  proof (my brute-force reference, 1.19e-07) still stands.
- **Provenance of the new numbers.** Regenerated `answer.tex` with `gen_answer.py` into a
  scratch dir: **byte-identical** to the delivered file. Its stdout shows 0.305 / 0.325 /
  the scale factors / 22.1x are *pulled from* `run/ablation.log`, not hardcoded. Each
  traces: B 0.3053 -> "0.305", C 0.3253 -> "0.325", listens 1.0000 / listened_by 0.9785
  -> "x1.00, x0.98", friend 0.0451 -> "by 22".
- **The leak claim, checked my own way.** Read `lp_graph_obs.csv` and the three split
  CSVs directly, with none of the worker's code: 19,464 distinct observed undirected
  edges; **train 19,464/19,464 positives (100.0%) are observed edges; val 0/4,171; test
  0/4,171.** The clause "whose edges *are* the training positives" is exact, and there is
  no val/test contamination.
- **The ablation is a genuine like-for-like test.** Read `ablation.py`: variant A loads
  the delivered layer's weights into the flexible layer and asserts the forward output is
  bit-identical (log shows 0.000e+00), and only the denominator varies across A/B/C/D;
  the harness is monkeypatched and restored in a `finally`. Its ordering (A 0.1809 <
  D 0.2465 < B 0.3053 < C 0.3253) matches my own independently-written round-1 ablation
  (A 0.1895 < D 0.2388 < B 0.2957 < C 0.3294). Same conclusion from two separate
  implementations.
- **Compliance.** `lint_output.py` OK. Recompiled in the 5-section wrapper: 0 errors,
  **0 overfull/underfull boxes**; rendered both pages and read them — the rewritten
  closing paragraph is legible and sets cleanly. R5 clean: no forbidden constructs, only
  `p2:sec:rgcn` / `pTwoPyStyle` / `pTwoKw,Cmt,Str,Rule` defined, no absolute paths, no
  figures. R3: `downloads.md` unchanged and still complete — the six new files are local
  scripts and logs, no new installs.
- **R8.** My count: 286 prose words (worker reports 287). R8 allows up to 290 for an
  answer with several sub-parts, which this has. Within target.

### Resolved since last round

- **[1.1] major — RESOLVED.** The answer no longer claims pooling helps by smoothing the
  listening relations. It now states the mechanism the data supports: pooling barely
  changes the dense relations (x1.00, x0.98) and helps by dividing the sparse `friend`
  term by 22, with variant C (0.325) quoted. The worker reproduced the finding itself
  with an exact control rather than taking my word for it, and went further by measuring
  *why* down-weighting `friend` helps — the leak — which I then confirmed independently.
- **[1.2] minor — RESOLVED.** The loose "smooths *the users* flat" premise is gone; no
  claim about which node type each listening relation smooths now appears.
- **[1.4] minor — RESOLVED.** `submission.md` now states what `crosscheck.py` actually
  reports for an in-flight problem.
- **[1.3] minor — WITHDRAWN.** The worker kept the run-1 table and gave its reasoning:
  the "report run 1" rule was fixed before any value was seen, and switching to the
  median after seeing run 1 come out high would be a post-hoc rule change. I accept that
  — it is the better practice of the two, the 0.190+/-0.020 spread sits in the sentence
  immediately below the table, and my own independent run (0.2221) landed near the
  reported value. Withdrawing rather than carrying it forward.
- **Unrequested improvement:** `verify_fidelity.py` now does a contiguous-block
  comparison instead of set membership, closing the weakness I noted in round 1.

### Still outstanding

Nothing substantive. Cosmetic nits, recorded but not worth another round:

- 0.305 and 0.325 are 3-seed means quoted to three significant figures with no spread,
  while the underlying seeds span 0.287-0.324 and 0.315-0.333. The qualitative claim
  (C > B >> A) is robust across two independent implementations, so this is presentation
  only.
- `run/leak_check.py`'s docstring says "Not asserted in answer.tex" but `answer.tex` does
  assert it in one clause — stale docstring in a playground script, not the deliverable.
- `submission.md` still says "before calling the two decompositions *optional*
  regularisers"; `answer.tex` now says just "regularisers". Stale prose in the notes.
- 286 words sits at the top of the R8 band.

PASS.
