# p2 — submission (round 3)

## Round-3 summary: I was wrong, the validator was right

Round 2 fixed all six round-1 defects, but my rewrite of the cold-start paragraph asserted a
**mechanism I never measured** — that an all-zero source row ties all 21 candidates, so cold
queries score at chance $1/21$. That is false, and I have now measured it false myself
(`tie_check.py`, log in `tie_check.log`):

| check | result |
|---|---|
| cold source rows actually all-zero | **216 / 216** — this part of my premise was right |
| cold queries with all 21 scores tied | **0 / 216** (median **20** distinct of 21; score spread 2.12–5.33) |
| tiebreak vector varies between runs | **No** — `evaluate_ranking` is never passed a seed, so it is byte-identical every run and contributes **zero** variance |
| reproduces the reported ×15 seed-0 cold value | **0.0880**, exact |
| is 0.0803 at chance? | **No** — chance is 0.0476; observed is +2.8 binomial sd above it (n=216) |

**Why it was wrong.** With $u = 0$, `_pair_features` still emits $|u-v| = |v|$ and
$\lVert u-v\rVert = \lVert v\rVert$, which vary by candidate. The hadamard/dot/cos features
do collapse to constants, but those two do not — so the predictor ranks cold queries on
candidate-only features (effectively a popularity prior), well above chance.

The validator also pointed out my claim was **self-disproving from my own data**: tied scores
plus a constant tiebreak would force *identical* cold hit@1 at every seed, yet mine differ
(0.0880 / 0.0972 / 0.0556). I should have caught that.

**What this changes and what it does not.** The cold-start *result* is untouched — 0.2824 and
0.3596 against a budget-matched baseline of 0.0803 is still the largest effect in the study.
What changed is the anchor: ratios are now **3.5× / 4.5× the measured token-matched control**
(gaps 7.5 / 10.3 cold-bucket sd), not "5.9× / 7.6× chance" (8.7 / 11.5 sd). Round 1 anchored
on the measured control and was correct; round 2 replaced a control-dependent truth with an
unmeasured falsehood. I have gone back to the measured anchor and added one *measured*
sentence about why the floor sits above chance.

| round-3 defect | status |
|---|---|
| false tie/chance mechanism (`answer.tex` cold-start ¶) | **fixed** — mechanism corrected and now measured; ratios/sd re-anchored on the control |
| "chance (1/21)" line in both figures | **removed** from `make_figs.py`; both PDFs regenerated and re-inspected |
| conclusion "from chance to 6–8× chance" | **fixed** → "by 3.5–4.5× over a budget-matched baseline" |
| "ranked at chance" in the density ¶ | **fixed** → "ranked on a popularity prior" |
| `float` unused | **removed** — and I checked the whole preamble the same way: `amssymb` and `caption` were also unused and are gone. Preamble is now 5 lines, each verified required by deleting it and failing to compile |
| `submission.md` preserved the wrong justification | **fixed** — this section replaces it |

---

## What the problem asked

Task 4 of HW2-Part(B) (notebook `input/graph_embedding-1.ipynb`, sections 7–8; slide deck
rendered pages 10–11, labelled **Optional**): build `H_train = G_train + artists +
user–artist edges`, implement a heterogeneous embedding method (metapath2vec recommended),
run at least two meta-path schemas, and report them in the *same* `comparison_table()` as
Task 3. Everything else is reused unchanged from Task 3.

**Brief vs. assignment page: no discrepancy.** R7 done across all three channels;
`page_011_fig_02.jpeg` (507×338) is the illustrative U–A–U cartoon — no data, nothing to
transcribe or redraw. The validator independently confirmed this reading.

## What I decided it needed

**code + diagram + plain.** Every number is measured; the "did it help, and for whom"
question is a per-degree question needing figures; the analysis is the point of an optional
extension.

## What I did

**Reuse.** `scaffold.py`/`impl.py` copied from p1, byte-identical (sha256 `041ff22b…` /
`908322aa…`). `hetero.py::MetaPathWalkEmbedding` subclasses p1's `WalkEmbedding` and
overrides `sample_walks` only, so `train_embedding`, `LinkPredictor` and `CountryClassifier`
are the same objects p1 measured. No bug found in p1's code; nothing changed.

**Schemas.** `UAU`, `UUAU`, `UUUAU` — one per cyclic-rotation class (`UAUU` is a rotation of
`UUAU`), forming a one-parameter family indexed by forced-social-step fraction 0, 1/3, 1/2,
with DeepWalk as the 1 endpoint. Plus type-blind DeepWalk on H and my own rare-artist
variant (step into artist $\propto \deg(a)^{-1}$).

**Artist starts and dead ends.** The cycle is rotated to the start node's type, so artists
walk `A U A U…`. A walk stops whenever the required next type is absent — at the first step
(dropped, matching p1's `[]`) or mid-walk. Round 1 documented only the first-step case; that
was defect [1.2] and is now fully disclosed.

**The controls (the round-2 fix).** Task 3 walks 6,958 users; Task 4 walks all 15,466 nodes
of H. Round 1 equalised *walks*. But meta-path walks truncate, so walks ≠ tokens:

| config | walks | mean len | tokens | vs ×22 |
|---|---|---|---|---|
| DeepWalk ×10 | 69,580 | 40.0 | 2,783,200 | −54.5% |
| **DeepWalk ×15 (token-matched)** | 104,370 | 40.0 | **4,174,800** | −31.8% |
| DeepWalk ×22 (walk-matched) | 153,076 | 40.0 | 6,123,040 | — |
| metapath U-A-U | 152,930 | 40.0 | 6,117,200 | −0.1% |
| metapath U-U-A-U | 148,000 | 24.3 | 3,593,757 | −41.3% |
| **metapath U-U-U-A-U** | 148,000 | 27.5 | **4,068,117** | −33.6% |

So the ×22 control was fair to U-A-U but handed U-U-U-A-U's comparator ~50% more tokens.
DeepWalk ×15 emits 4,174,800 tokens, **+2.6%** vs U-U-U-A-U — a real match, with the residual
still favouring the control, so the comparison stays conservative in the same direction.

**The cold-start anchor (corrected in round 3).** The cold bucket is anchored on the
**measured token-matched control**, 0.0803. An earlier draft anchored it on chance $1/21$;
that was wrong — see the round-3 section at the top. The social-only floor is *above* chance
because the ranker falls back on candidate-only features. The two controls do give different
cold values (0.0494 vs 0.0803); I report the token-matched one as the reference because it is
the fair comparator, and I note the others explicitly.

## Intermediate steps and code

Paths relative to PLAYGROUND. Interpreter `../../venv/bin/python`; `data` symlinks the
shared read-only dataset.

| file | what it does | command |
|---|---|---|
| `scaffold.py`, `impl.py` | p1's code, byte-identical | imported |
| `hetero.py` | **the meta-path sampler** — the only new algorithm; shown in the answer | imported |
| `test_sampler.py` | type sequence, edge existence, rotation, `[]` cases, social-step fractions | `python test_sampler.py` |
| `run_hetero.py` | notebook §7 + §5 verbatim + §8 mine: 5 configs × seeds {0,1,2} | `python run_hetero.py` → `run_hetero.log`, `results_hetero.{csv,pkl}` |
| `control_budget.py` | **walk**-matched control, DeepWalk ×22 | `python control_budget.py` → `results_control.pkl` |
| **`control_tokens.py`** | **NEW (round 2): token-matched control, DeepWalk ×15** | `python control_tokens.py` → `control_tokens.log`, `results_tokens.pkl` |
| **`corpus_size.py`** | **NEW (round 2): measures walks/tokens/mean-length/%full for every config** | `python corpus_size.py` → `corpus_size.json` |
| **`tie_check.py`** | **NEW (round 3): tests whether a cold all-zero source row ties all 21 candidates — it does not** | `python tie_check.py` → `tie_check.log` |
| `cold_start_stats.py` | isolated-user artist coverage, U-A-U 2-hop reach | `python cold_start_stats.py` |
| `typeblind_steps.py` | social-step fraction of a type-blind walk on H (0.72%) | `python typeblind_steps.py` |
| `make_tables.py` | emits every table body and prose number from the pickles | `python make_tables.py > tables.tex` |
| `make_figs.py` | writes both vector PDFs into OUTPUT | `MPLCONFIGDIR=$PWD/.mplcache python make_figs.py` |
| `trace_numbers.py` | audit: every 4-dp number in `answer.tex` must appear in an artefact | `python trace_numbers.py` |

`run_hetero.py` was **not** re-run this round (its results are seed-fixed and unchanged);
only the new control was computed. Table 2's bolding is now *generated* by `make_tables.py`
rather than hand-typed, since changing the reference column changed several row maxima.

## Results

3-seed means over seeds {0,1,2}. Task 3 rows come from p1's pickles, not re-run.

| config | test H@1 | test MRR | test mi-F1 | test ma-F1 | cold H@1 |
|---|---|---|---|---|---|
| Task 3 DeepWalk ×10 | 0.6009 | 0.7207 | 0.7629 | 0.6833 | 0.0447 |
| Task 3 triadic (p1 best) | 0.6087 | 0.7248 | 0.7661 | **0.6974** | 0.0293 |
| **control ×15 (token-matched)** | 0.6118 | 0.7269 | 0.7601 | 0.6764 | 0.0803 |
| control ×22 (walk-matched) | **0.6179** | 0.7292 | 0.7624 | 0.6852 | 0.0494 |
| type-blind DeepWalk on H | 0.4534 | 0.6229 | 0.6804 | 0.3794 | 0.3889 |
| metapath U-A-U | 0.4133 | 0.5849 | 0.6489 | 0.3516 | **0.3596** |
| metapath U-U-A-U | 0.5525 | 0.6876 | 0.7632 | 0.5675 | 0.2994 |
| metapath U-U-U-A-U | 0.6163 | **0.7361** | **0.7887** | 0.6353 | 0.2824 |
| U-A-U rare-artist α=1 | 0.4261 | 0.5942 | 0.6857 | 0.4007 | 0.3657 |

Noise floor (mean within-config sd over all 14 rows): 0.0038 / 0.0029 / 0.0050 / 0.0032 /
0.0072 / 0.0134 / 0.0038 / 0.0060. Cold-bucket noise floor 0.0271.

Every claim in `answer.tex` and its source:

- **Aggregate LP null.** vs token-matched: $+0.0045$ H@1 ($+0.9$ sd), $+0.0093$ MRR
  ($+2.9$ sd). vs walk-matched: $-0.0016$ ($-0.3$ sd), $+0.0070$ ($+2.2$ sd).
  `make_tables.py` "THE CONTROLS" block.
- **Budget alone** (×10→×15): $+0.0109$ test H@1, $+0.0062$ MRR, $-0.0027$ micro-F1. Same block.
- **Cold start** (re-anchored, round 3). control $0.0803$ → U-A-U $0.3596$ ($4.48\times$,
  gap $0.2793$ = **10.3** cold-bucket sd) and → U-U-U-A-U $0.2824$ ($3.52\times$, gap
  $0.2022$ = **7.5** sd). `make_tables.py` COLD block.
- **Cold queries are not tied** — 0/216 fully tied, median 20 distinct of 21. `tie_check.py`.
- **Cold-start coverage.** 666 isolated users, **647 (97.1%)** with ≥1 artist, median 334
  artists; 216 cold test queries, **209 (96.8%)** covered. `cold_start_stats.py`.
- **U-A-U 2-hop reach** median **7,307 of 7,623** (~96%) vs social median **61** — 40 sampled
  users, `cold_start_stats.py`.
- **Type-blind walk takes 0.72% social steps** (224 of 31,122), yet beats U-A-U by $+0.0401$
  test H@1. `typeblind_steps.py`.
- **Country.** vs token-matched: micro $+0.0286$ (7.6 sd), macro $-0.0411$ (6.9 sd); vs
  walk-matched $+0.0263$ / $-0.0498$. `make_tables.py`.
- **Rare-artist** gains on all eight columns: $+0.0129$ H@1 (2.6 sd), $+0.0094$ MRR (2.9 sd),
  $+0.0368$ mi-F1 (9.8 sd), $+0.0491$ ma-F1 (8.2 sd). `make_tables.py`.
- **Corpus/token counts** — `corpus_size.py` → `corpus_size.json`; every figure in the
  answer's token list matches the JSON exactly (checked programmatically).
- **Degree-≥16 dilution** $0.6504 \to 0.3785$ — updated to the ×15 reference (was 0.6644
  against ×22; a stale number I caught while re-checking Table 2).

`trace_numbers.py`: **184 distinct 4-dp numbers, 183 verbatim in a generated artefact.** The
single exception is `0.0154` = 0.6163 − 0.6009, arithmetic on two Table 1 cells.

## Verification performed this round

- `make_tables.py` re-run; **all 21 generated table rows match `answer.tex`** by number
  sequence (script in the transcript, not `make_tables` itself).
- Corpus numbers in the prose checked programmatically against `corpus_size.json`: walks,
  tokens, mean lengths (24.3 / 27.5) and %full (32.2 / 43.7) all match.
- Control means recomputed from `results_tokens.pkl` independently of `make_tables.py`.
- `lint_output.py` → rc=0. Fresh 2-pass compile → **rc=0, 6 pages, no overfull/underfull
  boxes, 0 undefined references.**
- Both figures re-rendered to PNG and **looked at** after the round-3 regeneration: legend
  clear of all bars, error bars visible, axes labelled, values still matching Table 2, and
  neither PDF contains the string "chance" any more (checked by extracting figure text).
- R5: 0 forbidden macros; all labels `p2:`-namespaced; figures by bare filename.

## Deliverables

- `OUTPUT/answer.tex` — LaTeX fragment, 6 pages typeset.
- `OUTPUT/fig_p2_degree.pdf` — 0 raster / 126 vector, 6.00 × 2.95 in (chance line removed in round 3).
- `OUTPUT/fig_p2_social.pdf` — 0 raster / 72 vector, 6.00 × 3.05 in (chance line removed in round 3).
- `OUTPUT/preamble.txt` — **5** `\usepackage` lines; `enumitem`, `float`, `amssymb` and `caption` all removed as unused, each confirmed by deleting it and checking the compile fails only for the ones that are needed.

## How I absorbed the length constraint [1.6]

Net length is unchanged at 6 pages despite the added content. I got there by, in order:
(a) switching the four floats from `[H]` to `[htbp]` — `[H]` was stranding 360pt of
whitespace on pages 2–4; (b) tightening prose throughout without dropping any claim;
(c) shortening the four captions; (d) reducing figure heights (3.4→2.95 in, 3.6→3.05 in) by
reclaiming excess legend headroom rather than shrinking fonts — the width stays 6.0 in at
`0.86\textwidth`, so on-page font size is unchanged and legibility is preserved; and
(e) converting the corpus table to a compact prose list, which removes presentation but
**no information** (every token count is still stated, and is still machine-checked against
`corpus_size.json`). I did **not** cut the type-blind paragraph or row, per the validator's
explicit ruling.

## Where I am least confident

1. **The token match is +2.6%, not exact.** `num_walks` is an integer, so on the social graph
   I can hit 3,896,480 (×14, −4.2%) or 4,174,800 (×15, +2.6%) against U-U-U-A-U's 4,068,117.
   I chose ×15 because the residual then favours the *control*, keeping the null conservative.
   An exact match would need fractional walk counts or a truncated final walk.
2. **Token count is a proxy for "amount of training signal", not the thing itself.** Two
   corpora of equal token count but different walk-length distributions are not strictly
   equivalent for Skip-Gram — a length-24 walk yields fewer within-window pairs per token
   near its ends than a length-40 walk. So U-U-U-A-U may still be *slightly*
   under-resourced even at matched tokens. This pushes in the same (conservative) direction
   as the +2.6%, so it cannot manufacture the null; it could only be hiding a small positive.
   I did not measure context-pair counts, which would settle it.
3. **Three seeds**, inherited from p1 for comparability. Ample for the large effects (cold
   start 7.5–10.3 sd, country 6.9–7.6 sd), thin for the small one: the MRR edge is 2.9 sd and
   I call it "small" rather than a win.
4. **The cold bucket is 216 test queries** with a wide per-seed spread. The *effect* is far
   too large to be noise, but I would not defend any single cold value to 4 dp. Note the two
   controls disagree there (0.0494 vs 0.0803), and round 2 wrongly explained that away as
   tie-breaking noise. It is not: the tiebreak is constant, so that spread is genuine
   seed-to-seed variance in the learned embedding. I report the token-matched control as the
   reference and state the others rather than explaining the difference away.
5. **"Music taste is regional" is interpretation, not measurement.** I show micro-F1 rises and
   macro-F1 falls and offer a large-vs-small-class explanation; I did not measure per-country
   F1 against country size, which would test it directly.
6. **2-hop reach samples 40 users**, not all 7,624. The numbers (median 7,307 of 7,623) are
   too extreme for sampling error to matter, but it is a sample.
7. **Only α=1 tried** for rare-artist sampling, so "rare-artist helps" is established but
   "α=1 is optimal" is not.
