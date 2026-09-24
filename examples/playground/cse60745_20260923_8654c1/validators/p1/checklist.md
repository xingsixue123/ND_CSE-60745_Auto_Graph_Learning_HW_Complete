# p1 validator checklist — Task 3, Graph Embedding over Homogeneous Structures

## Round 1
Verdict: FAIL

### What I verified independently (not taken on trust)

- **Assignment page (R7).** Read rendered pages 7/8/9 of `CSE60745-Hands-on_HW2-Part(B)-1.pdf`
  through all three channels: `page_00N.txt`, `page_00N.png`, and the native-resolution
  figure files `page_008_fig_02.jpeg`, `page_009_fig_02/03/04.jpeg`. Confirmed the figures
  are illustrative recaps only (toy 7-node A–G graph with a numbered 5-step walk; a
  "Walk 1..5" table of A–G sequences; a pipeline block diagram). No data, no parameters.
  The master's brief and the worker's reading are both accurate. The only thing the slide
  adds is a mention of struct2vec as a third named method and a *recommendation* (not a
  requirement) to re-implement DeepWalk/node2vec first — satisfied.
- **Scaffolding is verbatim.** Diffed `scaffold.py` / `run_all.py:run_experiment` against
  notebook cells 4, 5, 11. Only deviations: the download loop removed (data on disk) and
  `flush=True` added to two prints. Both disclosed, both harmless.
- **Interfaces obey the notebook docstrings** (cells 7, 9): shapes, `[]` allowed,
  zero rows for unwalked nodes, continuous `score` with higher = more likely.
- **Unit-tested all four TODOs empirically** (`rerun/v_unit.py`), not by reading:
  - 10 walks × length 40, each starting at `start`; `[]` for all 666 isolated nodes.
  - Every consecutive pair is a real edge of `G_train`; RWR's only non-edge steps are
    restarts, and every one of them lands on `start`.
  - Transition distributions match the stated rules over 200k samples from a degree-65
    node: uniform max|emp−theory| 0.00078; degcorr (∝deg⁻¹) 0.00089;
    triadic (∝1+|N(v)∩N(x)|) 0.00122.
  - node2vec second-order weights match the 1/p, 1, 1/q rule over 300k samples at all
    three settings: 0.00062, 0.00063, 0.00066. **This retires the worker's own
    "node2vec might have a bug" worry (submission.md §5) — the bias is provably correct.**
  - `train_embedding` → (7624, 128) with exactly 666 all-zero rows, and those rows are
    exactly the isolated node ids.
- **The numbers are real and reproducible.** Copied the scripts into my own directory and
  re-ran the seed-0 sweep from scratch: **all 7 strategies reproduce bit-exactly** against
  `run_all.log`. Also re-ran `triadic` at seed 1: bit-exact against `seed_study.log`
  (0.6099 / 0.7283 / 0.6140 / 0.7282 / 0.7654 / 0.7630 / 0.6887). Loading stats match
  `split_stats.json` (19,464 edges, 666 isolated, mean deg 5.106, max 153, 734 components,
  4171×21 val/test, 763/763/6098 country split).
- **Re-derived the aggregation myself** (`rerun/v_check.py`) from the pickles: Table 1
  means, Table 2 per-bucket means, the noise floor row and all seven spread/noise ratios
  match `tables.tex` and `answer.tex` exactly. Triadic is genuinely the argmax in every
  reported column, and in all 8 columns including the unreported one.
- **Data claims checked against the CSVs, independent of worker code:** 18 classes,
  largest 1,572, smallest 16 with exactly 2 in the 763-user train split; chance Hit@1
  1/21 = 0.0476, chance MRR = H₂₁/21 = 0.1736. All as claimed.
- **`trace_numbers.py` re-run:** 111 distinct 4-dp numbers in `answer.tex`, 2 untraceable,
  and both are the arithmetic the worker disclosed (0.7207−0.7124=0.0083; 0.20087→0.2009).
- **Figures opened and inspected** at 200 dpi. Both vector (0 raster images; 96 and 111
  vector drawings), 5.8×3.3 in and 5.8×3.9 in, axes labelled, legends clear of the data,
  n-counts under each bucket, error bars, no clipping or overlap. Readable at print size.
- **LaTeX.** No `\documentclass` / `\usepackage` / `document` env. All 9 labels namespaced
  `p1:`. Figures referenced by bare filename. Compiled in a minimal wrapper with
  `preamble.txt`: exit 0, 8 pages, no undefined references, no overfull boxes (2 cosmetic
  underfull hboxes in the strategy table's `p{6.6cm}` column).
- **`lint_output.py` passes.** `downloads.md` records the (nothing-installed) state and the
  data symlink.

### Defects

- [1.1] **Country validation macro-F1 is never reported.** The brief (§2 item 6) requires
  "country classification micro-F1 / macro-F1 on **val and test**" — four numbers per
  strategy. `answer.tex:236` gives three: `val mi-F1`, `test mi-F1`, `test ma-F1`.
  The number already exists: `evaluate_country` returns it, and `make_tables.py:31`
  computes it as `cc_val_macro` and then drops it from `ORDER` at lines 37–38.
  This is not just compliance — I computed the column and it is the worker's **strongest
  remaining evidence**: spread 0.0411 against a noise floor of 0.0077, ratio **5.35×**,
  second only to val H@1, with triadic winning it (0.6833) over DeepWalk (0.6639),
  node2vec q=2 (0.6467) and degcorr (0.6421). Omitting it throws away the result that
  best supports the answer's own thesis. Add the column to Table 1 (and to the noise-floor
  and spread rows). | `OUTPUT/answer.tex:232-249`, `make_tables.py:37-38` |
  severity: **major**

- [1.2] **Table 1 is captioned `comparison_table()` but drops 6 of its 13 columns.**
  `run_experiment` records `val_hit@1_deg0+ … val_hit@1_deg16+` for every strategy (they
  are present in `results_comparison.csv` and in `run_all.log`). Brief item 3 asks for
  "the columns `comparison_table()` produces" and item 6 asks for the per-source-degree
  breakdown "for every strategy"; Table 2 covers only 3 of the 7. Either add those six
  columns (or a compact 7×6 per-strategy Hit@1-by-degree table) or re-caption Table 1 so
  it does not claim to be `comparison_table()`. |
  `OUTPUT/answer.tex:228-249, 266-286` | severity: minor

- [1.3] **Metric mismatch in the cold-start paragraph.** "Test Hit@1 runs from 0.03–0.04 …
  to 0.68–0.69 … a gap of about 0.64, roughly fifty times the 0.0127 that separates the
  best strategy from the worst." 0.0127 is the test **MRR** spread; the test **Hit@1**
  spread is 0.0198, so the correct ratio is ≈32×, not ≈50×. (The "Practical conclusion"
  paragraph does the same comparison correctly, entirely in MRR.) Either use 0.0198/32× or
  restate the gap in MRR. | `OUTPUT/answer.tex:368-372` | severity: minor

- [1.4] **Self-contradictory cost claim.** Triadic "is as cheap to sample as DeepWalk once
  the edge weights are precomputed, $1.9$\,s versus $0.7$\,s". 1.9 s is 2.7× 0.7 s, and the
  sentence supplies the numbers that refute it. The defensible claim is that it stays
  first-order and cheap in absolute terms, and undercuts node2vec's 1.3 s only marginally.
  | `OUTPUT/answer.tex:399-401` | severity: minor

- [1.5] **Validation columns are the model-selection criteria, and the analysis leads with
  them.** `LinkPredictor.fit` picks `C` on validation MRR and `CountryClassifier.fit` picks
  `C` on validation accuracy, so `val H@1`, `val MRR` and `val mi-F1` are optimistically
  biased. "Which differences are real" opens with the val ratios (7.0×, 6.0×) as headline
  evidence. The test ratios (4.1×, 4.2×, 3.9×) carry the argument unaided; one sentence
  acknowledging that val is the selection split would make the section honest. |
  `OUTPUT/answer.tex:319-322, 246-247` | severity: minor

### Informational (no action required)

- `impl.py:203` comment says ties are "counted pessimistically", but `(s > sp).sum(1)` is
  the *optimistic* rank. It affects only internal `C` selection (continuous scores
  essentially never tie) and the comment is absent from the deliverable listing.
- The listing condensations disclosed in submission.md §1 are accurate and complete;
  I diffed all four listings against `impl.py` and found no undisclosed difference.
- `control_random.py:15` computes the majority-class rate over all 7,624 users (0.2062);
  over the 6,098 test users it is 0.2063. Immaterial.

### Resolved since last round
(none — first round)

### Still outstanding
[1.1] major, [1.2] [1.3] [1.4] [1.5] minor.

---

## Round 2
Verdict: PASS

### What I re-verified this round (assuming the fixes were wrong until shown otherwise)

- **`impl.py` changed at 16:50 while the pickles stayed at 16:35** — the first thing I
  checked, since an algorithmic edit would have invalidated every reported number.
  Diffed it: the change is **comment-only** (the `# ties counted pessimistically` comment I
  flagged as informational now correctly says optimistic). The seed-0/seed-1 results I
  reproduced bit-exactly in round 1 therefore still stand.
- **New Table 3 (`p1:tab:valdeg`) recomputed independently** (`rerun/v_check2.py`) from the
  pickles, without using `make_tables.py`: **all 42 cells match**, and the bucket sizes
  213/261/524/842/973/1358 match `run_experiment`'s own `val` breakdown (and sum to 4,171).
  I also cross-checked that the recorded `val_hit@1_deg*` summary columns are identical to
  the breakdown object they are claimed to come from.
- **The per-bucket bolding and the honesty claim around it check out.** Triadic really does
  win only 3 of the 6 val degree buckets; node2vec $p{=}q{=}0.25$ really does take the cold
  and 8–15 buckets; and the 2–3 bucket really is a tie (DeepWalk 0.5731 = node2vec $q{=}2$
  0.5731), which the answer states explicitly rather than hiding. Volunteering a result
  that complicates its own thesis is the right call.
- **New `val ma-F1` column verified**: 0.6639 / 0.6621 / 0.6467 / 0.6581 / 0.6521 / 0.6421
  / 0.6833, noise floor 0.0077, spread 0.0411, ratio 5.35× (shown as 5.4×), worst is
  deg-corrected at 0.6421. All match my round-1 independent computation exactly.
- **Prose arithmetic re-checked**: +0.0194 val gain and 2.52 sd (shown 2.5) ✓;
  test Hit@1 spread 0.0198 and 0.64/0.0198 = 32.3 ✓ ([1.3] genuinely fixed, both
  quantities now in the same metric).
- **`tables.tex` regenerates byte-identically** from the worker's pickles when I run the
  updated `make_tables.py` myself — the tables are generated, not typed.
- **Every generated Table 1/2/3 row matches `answer.tex` numerically.** Note the literal
  rows differ (Table 1 labels abbreviated, Table 2 bolding added by hand), so I re-derived
  **Table 2's hand-added bolding independently**: degree-1 RWR best on both metrics,
  buckets 2–3 through ≥16 triadic best on both, cold bucket left unbolded because DeepWalk
  and RWR tie at 0.0447. All correct.
- **`trace_numbers.py` re-run**: 156 distinct 4-dp numbers, 152 traceable; the 4 exceptions
  are the disclosed derived quantities (0.0083, 0.0141, 0.0194, 0.2009), each of which I
  confirmed is arithmetic on values that do appear in the tables.
- **Compile + compliance re-checked**: exit 0, 8 pages, **zero** overfull boxes, no
  undefined references, 3 cosmetic underfull hboxes. `lint_output.py` passes. No forbidden
  macros. The new `p1:tab:valdeg` label is namespaced and referenced. Figures still
  referenced by bare filename and unchanged (still vector, still consistent with Table 2).
  Rendered pages 4 and 6 and looked at them: the widened 9-column Table 1 and the new
  Table 3 both set cleanly, daggers legible.

### Defects

None blocking. Two cosmetic items, noted and **not** held against the submission:

- [2.1] `answer.tex:275` says the degree buckets are "$4$--$16\times$ smaller than the full
  split". The actual ratios are $4171/n_b$ = 19.6, 16.0, 8.0, 5.0, 4.3, 3.1 — so the true
  range is ~3×–20×, wrong at both ends. The direction of the argument (buckets are much
  smaller and therefore much noisier) is correct and if anything understated. |
  severity: minor
- [2.2] `submission.md` claims "Every generated table row in `tables.tex` — Tables 1, 2 and
  3 — matches `answer.tex` exactly". Literally it does not: Table 1's row labels are
  abbreviated in the answer and Table 2's `\textbf` bolding is hand-added. All the
  *numbers* match, and I verified the hand-added bolding is correct, so nothing is wrong
  with the deliverable — but the process note overstates what was mechanically checked. |
  severity: minor

### Resolved since last round

- [1.1] **major — fixed and verified.** `val ma-F1` is now a full column of Table 1 with its
  own noise-floor and spread entries, and the worker promoted it into the analysis rather
  than merely tabulating it, including the correct and non-obvious observation that val
  macro-F1 is *not* the selection objective (`C` is chosen on val accuracy = val micro-F1),
  so it is less compromised than the other val columns.
- [1.2] **fixed and verified.** New Table 3 gives all six `val_hit@1_deg*` columns for all
  seven strategies; Table 1 re-captioned so it no longer claims to be the whole of
  `comparison_table()`. Table 2 also gained its MRR halves in the caption text.
- [1.3] **fixed and verified.** Now "about $0.64$, roughly thirty-two times the $0.0198$",
  both quantities in Hit@1.
- [1.4] **fixed and verified.** The "as cheap as DeepWalk" claim is gone; replaced with
  1.9 s vs 0.7 s, the reason (weighted-table draw per step), and the correct framing that
  it is negligible against the ~40 s of Skip-Gram training.
- [1.5] **fixed and verified.** The three selection-split columns are marked $\dagger$ with
  an explanatory caption, and "Which differences are real" now rests the argument on the
  held-out test columns (4.1×, 4.2×, 3.9×).
- Informational note (wrong "pessimistic" comment in `impl.py:202`) also corrected.

### Still outstanding

Nothing substantive. [2.1] and [2.2] are cosmetic and do not warrant another round.
