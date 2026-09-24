# p2 validator checklist — Task 4, Heterogeneous Graph Embedding

## Round 1
Verdict: FAIL

Scope note: the worker's round-1 run completed (`rc=0`) but was never audited; its
`submission.md` carries a self-audit. I took none of that on trust. Every number below
was recomputed by me, through my own code path, in `VALIDATOR_DIR`.

### What I verified independently (all clean)

**Source (R7), done myself.** Read `page_010.txt` / `page_011.txt`, the whole-page render
`page_011.png`, and the embedded figure `page_011_fig_02.jpeg` at native resolution
(507x338). The figure is six blue user nodes U1-U6, four orange artist nodes A1-A4, and a
purple "U-A-U Meta-path" arrow U1 -> A1 -> U2. It is illustrative: no data, no parameters,
nothing to transcribe or redraw. `page_011_fig_01.png` is the Notre Dame slide template.
I also diffed the master's brief against notebook cells 14/16/18 — quoted word for word.
No discrepancy between brief and page. The worker's account of all this is accurate.

**Numbers (`indep_check.py`).** Loaded `results_hetero.pkl`, `results_control.pkl`,
`../p1/results_full.pkl`, `../p1/results_seeds.pkl` and rebuilt both tables without
importing `make_tables.py`:
- Table 1: all 13 rows x 8 columns match `answer.tex` to 4 dp. Noise-floor row matches.
- Table 1 bolding: recomputed the argmax of every column. All 8 correct
  (test H@1 -> control 0.6179; val/test MRR, val/test mi-F1, val H@1 -> U-U-U-A-U;
  val/test ma-F1 -> triadic).
- Table 2: all 6 rows x 8 cells match; all 12 bolded cells are the true row maxima.
  Bucket index and `n_queries` (216/266/469/842/939/1439, sum 4171) are identical across
  all 39 runs, so the positional `.iloc[i]` lookups cannot be misaligned.
- Headline deltas all reproduce: -0.0016 / +0.0070 test (U-U-U-A-U vs control),
  +0.0170 / +0.0085 / -0.0004 (budget alone), +0.0154 (vs x10), +0.0263 / -0.0498
  (country), cold 0.0494 -> 0.3596 (7.28x, 11.0 sd) and -> 0.2824 (5.72x, 8.3 sd).

**Reuse of p1.** `sha256` of `scaffold.py` / `impl.py` identical to p1's. I checked the
one thing that could have invalidated this: p1's `impl.py` mtime (16:50) is *later* than
p1's `results_full.pkl` (16:35) and `results_seeds.pkl` (16:19). Per p1's own validator
record that edit was comment-only (the "pessimistic"/"optimistic" tie comment at
`impl.py:202`) and p1 re-ran `deepwalk` bit-exact afterwards. Comparison is valid.
`scaffold.py` also matches notebook cells 5 and 11 verbatim.

**Sampler (`my_sampler_check.py`, written from the spec, not from the worker's test).**
On the real `H_train`, 200 probe nodes per schema (150 users + 50 artists):
- 0 non-edges and 0 type violations for `UAU` / `UUAU` / `UUUAU`, from both user and
  artist starts — the rotation for artist starts is correct.
- Social-step fractions 0.0000 / 0.3335 / 0.5079 vs designed 0 / 1/3 / 1/2.
- Users with no artist give `[]` under `UAU`; socially isolated users give `[]` under
  `UUAU`. Correct.
- Total corpus over all 15,466 nodes: 152,930 / 148,000 / 148,000 — exactly the counts in
  `run_hetero.log`.
- Rare-artist alpha=1: empirical sampling distribution vs 1/deg(a) on a 625-artist node,
  max probability error 4.2e-4. The weighting is exactly what is claimed.

**Independent corroboration of the cold-start coverage claim.** The type-blind run made
154,470 walks = 15,447 x 10, i.e. 19 nodes of H are isolated. 666 socially isolated users
minus 647 with >=1 artist = 19. Two unrelated artefacts agree.

**Structural facts.** Re-ran `cold_start_stats.py` and `typeblind_steps.py`: 666 isolated,
647 (97.1%), median 334 artists; 173 with no artist; artists/user median 400 max 944 (an
independent match to the notebook's own table); artist popularity median 205; test 216
cold sources, 209 covered (96.8%); U-A-U 2-hop reach median 7,307 of 7,623 vs social 61;
type-blind social-step share 0.72% (224 of 31,122). All match the answer.

**Figures.** Rendered both to PNG at 150 dpi and looked at them. `fig_p2_degree`: 6.0x3.4
in, 0 rasters / 126 vector drawings, legend clear of the bars, error bars visible, both
axes labelled, n= labels legible, bar heights match Table 2. `fig_p2_social`: 6.0x3.6 in,
0 rasters / 72 vector, four x positions labelled with both the fraction and the schema,
values match Tables 1 and 2. Both readable at printed size. Generated from the pickles.

**LaTeX / layout.** 0 occurrences of `documentclass` / `usepackage` / `document` env.
All 10 `\label`s plus `label=p2:lst:sampler` namespaced `p2:`; both figures referenced by
bare filename. Compiled in my own wrapper (`texcheck/wrap.tex`): rc=0, 6 pages, 0
overfull/underfull boxes, no undefined references or LaTeX warnings.
`lint_output.py` -> rc=0, `OUTPUT LINT OK`. `downloads.md` correctly records
"nothing installed" plus the inherited shared resources (R3 satisfied).
Reproducibility claim checked: `repro_check.log` reproduces U-U-U-A-U seed 0 bit-exactly
and correctly refused to write artefacts on a filtered run.

### Defects

- [1.1] **The budget-matched control is matched by walk *count*, not by corpus size, and
  the two schemas that carry the headline conclusion fall 34-41% short.** |
  `answer.tex:117-124` (§Protocol) and `answer.tex:214-221` (§Analysis, first paragraph) |
  severity: **major**

  Measured exactly over all start nodes (`validators/p2/corpus_size.py`):

  | config | walks | tokens | % of walks reaching length 40 | tokens vs control |
  |---|---|---|---|---|
  | control DeepWalk x22 (G) | 153,076 | 6,123,040 | 100.0% | — |
  | metapath U-A-U | 152,930 | 6,117,200 | 100.0% | -0.1% |
  | metapath U-U-A-U | 148,000 | 3,593,757 | 32.2% | **-41.3%** |
  | metapath U-U-U-A-U | 148,000 | 4,068,117 | 43.7% | **-33.6%** |

  The answer equates walks with corpus ("$\approx$152,930 walks, a $2.2\times$ larger
  Skip-Gram corpus"; "matching the Task-4 corpus to within $0.1\%$"). That holds for
  U-A-U, rare-artist and type-blind. It is wrong by a third for **U-U-U-A-U — the one row
  the control exists to adjudicate**. In tokens the Task-4/Task-3 ratio for U-U-U-A-U is
  1.46x, not the stated 2.2x.

  The worker's own `run_hetero.log` already contains the evidence and it was not noticed:
  Skip-Gram time falls from ~111 s (U-A-U, 6.12M tokens) to 65 s and 72 s for U-U-A-U and
  U-U-U-A-U — ratios 0.59 and 0.65, matching the token ratios 0.587 and 0.665 almost
  exactly. gensim time tracks tokens, not walks.

  Consequence: the headline "-0.0016, i.e. nothing" is measured against a control handed
  ~50% more training tokens, so the aggregate null is conservative in a direction the
  reader is not told about. Fix by disclosing the token counts, restricting the "within
  0.1%" claim to the configs it actually covers, and qualifying the aggregate-null
  sentence. **No re-run is required** — everything needed is already measured.
  (For Figure~\ref{p2:fig:social} the truncation works *against* the rising blue trend, so
  that conclusion is safe; say so rather than leaving it unaddressed.)

- [1.2] **The sampler's mid-walk truncation is undocumented.** | `answer.tex:46-50`
  (§"Artist start nodes") and `hetero.py` docstring lines 22-25 | severity: **major**

  Both describe only the *first-step* failure: "a walk that cannot take its first step
  ... is dropped". In fact a walk also dead-ends at any point where the next required
  type is absent — overwhelmingly when an A->U step lands on one of the 666 socially
  isolated users and the schema then demands U->U. Measured mean walk lengths are 24.3
  (U-U-A-U) and 27.5 (U-U-U-A-U) against the stated 40, with only 32.2% / 43.7% of walks
  running to full length. The behaviour itself is a correct implementation choice
  (standard metapath2vec terminates on a dead end) — this is a disclosure defect, not a
  correctness one — but it is the mechanism behind [1.1] and a material property of the
  method being reported.

- [1.3] `answer.tex:118` says "every Task 4 run walks from all 15,466 nodes of $H$
  ($\approx$152,930 walks)". U-U-A-U and U-U-U-A-U start from 14,800 nodes and make
  148,000 walks, because the 666 socially isolated users cannot start those schemas —
  which the answer itself states at line 47. The two statements sit at odds. |
  severity: minor

- [1.4] `answer.tex:58` says rare-artist sampling lowers median visited-artist popularity
  "from $613$ to $205$". The worker's measurement was 204.5; rounding it up to 205 makes
  it land exactly on the quoted dataset median of 205, which overstates how clean the
  coincidence is. My own probe gives 632 -> 205.0, so the claim is substantively right;
  cosmetic only. | severity: minor

- [1.5] `\label{p2:fig:degree}` (`answer.tex:199`) is defined but never `\ref`'d, and
  `\usepackage{enumitem}` in `preamble.txt` is unused (the answer deliberately avoids list
  environments). Both harmless. | severity: minor

- [1.6] **Length.** 6 pages (page 6 ~45% full) against the brief's "2-4 pages is right".
  The worker disclosed this and asked to be overruled. **Ruling: keep the type-blind
  paragraph and row** — it is the strongest evidence for the metapath2vec argument and I
  would rather have it than 0.6 of a page. But the fixes for [1.1]/[1.2] must be absorbed
  by tightening §Method and §Protocol prose: **net length must not increase.** |
  severity: minor

### Resolved since last round

(First round — nothing to resolve.)

### Still outstanding

[1.1] through [1.6]. [1.1] and [1.2] are the two that require substantive edits; they are
the same underlying finding seen from the method side and the protocol side, and neither
requires re-running anything. No reported measurement is wrong.

---

## Round 2
Verdict: FAIL

The worker went past the minimum on [1.1]: rather than merely disclosing the token gap,
it ran a genuinely token-matched control (DeepWalk x15, 3 seeds) and re-anchored the
comparison on it. That was the right call and it is correctly executed. All six round-1
defects are fixed and I verified each one. One **new** defect was introduced in the
round-2 rewrite, and it is a measurably false claim, so this does not pass yet.

### Re-verified this round (independent recomputation, not the worker's scripts)

- **Corpus measurement.** `corpus_size.json` matches my round-1 `corpus_size.py` exactly
  on every field: 6,123,040 / 6,117,200 / 3,593,757 / 4,068,117 tokens; mean lengths
  24.282 / 27.487; 32.225% / 43.723% full. Independent agreement.
- **New x15 control is real and reproduces.** `control_tokens.log` present; I recomputed
  all 8 columns straight from `results_tokens.pkl`: 0.6110 / 0.7267 / 0.6118 / 0.7269 /
  0.7650 / 0.6678 / 0.7601 / 0.6764. Matches Table 1 row exactly. 6,958 x 15 = 104,370
  walks = 4,174,800 tokens, +2.62% over U-U-U-A-U's 4,068,117 — the +2.6% claim and the
  "residual favours the control" framing are both correct.
- **Table 1**: all 14 rows x 8 columns match. New 14-row noise floor
  (0.0038/0.0029/0.0050/0.0032/0.0072/0.0134/0.0038/0.0060) matches. All 8 bolded cells
  are the true argmax.
- **Table 2**: all 6 rows x 8 cells match against the new x15 reference column
  (0.0803/0.2210, 0.4361/0.5642, 0.5814/0.6900, 0.6690/0.7734, 0.6887/0.7940,
  0.6504/0.7739). All 12 bolded cells correct — including the subtle split in the 8–15
  row (U-U-U-A-U 0.6894 > x15 0.6887 on H@1, but x15 0.7940 > 0.7932 on MRR). Generating
  the bolding rather than hand-typing it was the right response to changing the reference.
- **Full-precision arithmetic**, all confirmed to the 4th decimal: +0.0045 H@1 (0.90 sd),
  +0.0093 MRR (2.89 sd), +0.0286 micro-F1 (7.59 sd), -0.0411 macro-F1 (6.88 sd);
  budget x10->x15 +0.0109 / +0.0062 / -0.0027; rare-artist +0.0368 (9.8 sd) / +0.0491
  (8.2 sd); MRR-vs-x22 re-stated as 2.2 sd (was 2.1) — correctly updated for the new
  noise floor. The stale 0.6644 -> 0.6504 fix in the degree->16 dilution sentence is
  correct and was caught by the worker, not by me.
- **Figures** re-rendered and looked at: 6.0x2.95 and 6.0x3.05 in, 0 rasters /
  127 and 73 vector drawings. Still legible after the height reduction — legend clear of
  the bars, error bars visible, both axes labelled, no collisions. Endpoints track the new
  x15 reference (0.6118 / 0.0803).
- **Compile / compliance**: rc=0, **6 pages** (length held per [1.6]), 0 overfull/underfull,
  0 undefined references. 0 forbidden macros; all 11 labels `p2:`-namespaced; bare
  filenames. `lint_output.py` rc=0. `downloads.md` still accurate.

### Defects

- [2.1] **The "cold start scores exactly chance because ties are broken at random" claim
  is false, and I measured it.** | `answer.tex:245-250`, echoed at `:267`, `:318`, and
  drawn as the "chance (1/21)" reference line in *both* figures | severity: **major**

  The answer asserts: "Each query ranks $21$ candidates and the scaffolding breaks ties at
  random, so an all-zero row scores exactly **chance, $1/21 = 0.0476$** --- and chance is
  what all three social-only configurations measure ... the spread between them is
  tie-breaking noise." Three separate claims, all wrong
  (`validators/p2/chance_probe.py`):

  1. **There are no ties.** I trained DeepWalk x15 seed 0 and inspected the real scores of
     all 216 cold-source test queries: **0 of 216** have tied candidate scores. Median 20
     distinct scores out of 21; within-query score spread 2.12 to 5.33 (median 3.68). The
     source row is indeed all-zero (666 such rows), but `_pair_features` still emits
     $|u-v| = |v|$ (128 dims) and $\|u-v\| = \|v\|$, which vary by *candidate*. The
     predictor therefore produces a real, deterministic ranking keyed on candidate-only
     features. My run reproduces the worker's x15 seed-0 cold value exactly (0.0880), so
     this is the same quantity, not a different measurement.
  2. **Tie-breaking cannot be the source of the spread.** `evaluate_ranking`
     (`scaffold.py:72-77`) seeds its tiebreak with `np.random.default_rng(RANDOM_SEED)`
     and `evaluate_link_prediction` never passes a seed — so the tiebreak vector is
     *byte-identical in every run ever performed*. It contributes exactly zero variance.
     The seed-to-seed cold spread comes from the embedding changing the candidate-only
     features. (This is also self-disproving from the worker's own data: if the scores
     were tied, identical tiebreaks would force identical cold hit@1 across seeds. The
     measured values differ — 0.0880/0.0972/0.0556 and 0.0602/0.0694/0.0185.)
  3. **x15 is not at chance.** Under the binomial model the "chance" framing implies
     ($p=1/21$, $n=216$, 3-seed mean, sd 0.0084), the measured 0.0803 sits **+3.9 sd above
     chance**. x10 (-0.3 sd) and x22 (+0.2 sd) are consistent with chance; x15 is not.
     Cold-bucket MRR tells the same story: 0.2210 against a chance MRR of
     $H_{21}/21 = 0.1736$, i.e. 1.27x chance.

  **What survives:** the cold-start result itself is untouched — 0.2824/0.3596 against a
  social-only baseline anywhere in 0.045–0.080 is a 3.5x–8x effect on any anchor. What
  does not survive is the asserted mechanism and the exactness. The derived figures
  "$5.9\times$ and $7.6\times$ chance" and "gaps of $8.7$ and $11.5$ times the $0.0271$
  mean seed spread" are computed against a baseline justified by a false argument.

  **Fix (no re-running required):** drop the ties/chance mechanism. Either (a) keep
  $1/21$ as a plotted floor but state that the social-only configs measure 0.9x–1.7x it
  rather than "exactly" it, and note that x15 sits measurably above chance; or (b) revert
  to anchoring on the measured token-matched control (0.0803), giving 4.5x and 3.5x, and
  state the control disagreement as a range rather than explaining it away. Either way,
  recompute the multipliers and sd-gaps, and correct `:267` ("ranked at chance"), `:318`
  ("from chance to $6$--$8\times$ chance") and the figure reference-line labels to match.
  Note round 1's version — anchoring on the measured control — was not wrong; it was
  control-dependent. This replaced a control-dependent truth with an unmeasured falsehood.

- [2.2] `\usepackage{float}` (`preamble.txt:7`) is now unused: all four floats moved to
  `[htbp]` and `[H]` appears 0 times in `answer.tex`. Same class as the `enumitem` item
  fixed this round, in a new place. | severity: minor

- [2.3] `submission.md:86-90` repeats the [2.1] reasoning ("both are chance-level
  tie-breaking noise, which is exactly why I re-anchored that claim to $1/21$"), as does
  "Where I am least confident" item 4. These should be corrected alongside the answer so
  the process record does not preserve the wrong justification. | severity: minor

### Resolved since last round

- [1.1] **major — fixed at the root, and verified.** Not merely disclosed: a token-matched
  DeepWalk x15 control was run and measured, token counts for all configs are stated in
  §Protocol, the "within 0.1%" claim is now correctly restricted to U-A-U, and the
  token-matched control is the reference column of Table 2 and both figures. The headline
  is now reported against *both* controls (+0.0045 / -0.0016), which is a stronger null
  than either alone. All numbers verified against `results_tokens.pkl`.
- [1.2] **major — fixed and verified.** §"Start nodes, and dead ends" now documents
  first-step *and* mid-walk termination, names the mechanism (A->U landing on one of the
  666 isolated users), and gives the measured mean lengths 24.3 / 27.5 and %full
  32.2 / 43.7 — all matching my own measurement.
- [1.3] **fixed.** Exact per-schema walk and start counts now stated (152,930 from 15,293;
  148,000 from 14,800). Verified.
- [1.4] **fixed.** Now reports 204.5 and notes it lands at the dataset median 205.
- [1.5] **fixed.** `p2:fig:degree` is now `\ref`'d; `enumitem` removed. (See [2.2].)
- [1.6] **met.** Still 6 pages despite a new control row, the token disclosure and the
  truncation disclosure. Achieved by `[H]`->`[htbp]`, prose tightening and reclaiming
  legend headroom — not by shrinking fonts (width stays 6.0 in at 0.86\textwidth) and not
  by cutting the type-blind paragraph, per my ruling. Legibility re-checked and intact.

### Still outstanding

[2.1] is the only substantive item; [2.2] and [2.3] are one-line cleanups that ride along
with it. No re-running is required — the fix is confined to the cold-start paragraph, two
sentences elsewhere, and the two figure labels.

---

## Round 3
Verdict: PASS

All three round-2 defects are resolved. The worker did the right thing on [2.1]: rather
than taking my word for it, it wrote its own probe (`tie_check.py`), reproduced my
measurement independently, and corrected the claim to match what the data actually says.

### Verified this round

**[2.1] fixed, and fixed for the right reason.** `tie_check.py` / `tie_check.log`
reproduce my `chance_probe.py` numbers exactly: 216/216 source rows all-zero, **0/216**
fully tied, median 20 distinct of 21, spread 2.117/3.676/5.328, cold hit@1 0.0880,
MRR 0.2274 vs chance MRR 0.1736, tiebreak vector byte-identical across calls. The worker
also surfaced a detail I had not reported — **124/216 queries have *partial* ties** (min
14 distinct) — and the answer now says "fully tied", which is the precise claim.
The rewritten paragraph (`answer.tex:243-257`) states the correct mechanism ($u=0$ makes
$|u-v|\to|v|$ and $\lVert u-v\rVert\to\lVert v\rVert$, so ranking runs on candidate-only
features) and calls the floor "a weak popularity prior, not chance".
Re-anchored on the measured token-matched control, verified by me at full precision:
$0.3596/0.0803 = 4.480 \to 4.5\times$, $0.2824/0.0803 = 3.519 \to 3.5\times$;
gaps $0.2793/0.027127 = 10.30$ and $0.2022/0.027127 = 7.45 \to 10.3$ and $7.5$ sd.
All follow-through done: `:267` now "ranked on a popularity prior"; the Conclusion now
"by $3.5$--$4.5\times$ over a budget-matched baseline"; the "chance (1/21)" reference line
is gone from both figures (confirmed by extracting the figure text — neither PDF contains
the string, and the vector-drawing counts drop back to 126/72).

**[2.2] fixed.** `float` removed; `[H]` appears 0 times. The worker went further and also
dropped `caption` and `amssymb`, leaving 5 packages. I checked this is safe rather than
assuming: no amssymb-only macros appear in the fragment, and my wrapper compile with only
p2's 5 packages plus `geometry` is clean. That is a real improvement to the merged master
preamble.

**[2.3] fixed.** `submission.md` now opens with the retraction, records the measurement,
and explicitly withdraws the old "Where I am least confident" item 4.

### Nothing regressed

Mechanically re-checked `answer.tex` against the raw pickles: **all 112 Table 1 cells
match**, all 8 bolded cells are the true argmax, the noise-floor row matches, and **all 48
Table 2 cells plus all 12 bolded cells match** — including the 8–15 row where H@1 and MRR
bold different columns. Result pickles are untouched since rounds 1–2 (17:30 / 17:36 /
18:14), so no configuration was silently re-run.
Compile rc=0, **6 pages** (length still held), 0 overfull/underfull, 0 undefined
references, no warnings. `lint_output.py` rc=0. R5: 0 forbidden macros, all 10 `\label`s
plus the listing label `p2:`-namespaced, both figures by bare filename, `p2:fig:degree`
still referenced. `downloads.md` accurate. Both figures re-rendered and inspected: vector,
legible, values tracking the tables.

### Defects

None. Nothing substantive remains.

### Resolved since last round

- [2.1] **major — fixed and independently re-measured by the worker.** The false
  tie/chance mechanism is gone from the answer, the conclusion, the density paragraph and
  both figures; the cold-start multipliers and sd-gaps are re-anchored on the measured
  token-matched control and verified correct at full precision.
- [2.2] **fixed.** Unused `float` removed (along with `caption` and `amssymb`); compile
  verified clean on the reduced preamble.
- [2.3] **fixed.** The process record no longer preserves the wrong justification.

### Still outstanding

Nothing. Across three rounds every reported number has been reproduced from the raw
pickles through an independent code path, the sampler has been verified against the
specification on the real graph, the corpus measurement has been confirmed twice, and the
one false mechanistic claim has been measured false and corrected.
