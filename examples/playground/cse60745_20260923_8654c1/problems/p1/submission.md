# p1 — submission (round 2)

## Response to validator round 1

All five defects fixed. None required re-running the sweep — every number was already in
the pickles, which is exactly why the omission was inexcusable rather than expensive.

- **[1.1 major] Country validation macro-F1 now reported.** The validator is right and
  the miss was mine: `make_tables.py` computed `cc_val_macro` and I dropped it from
  `ORDER`. I had been thinking of the four country numbers as "micro + macro on test,
  micro on val" and never noticed the fourth cell was missing. Table 1 now has all eight
  scalar columns. The validator's numbers reproduce exactly: spread **0.0411**, noise
  floor **0.0077**, ratio **5.35×**, triadic 0.6833 vs DeepWalk 0.6639 vs deg-corrected
  0.6421. It is the second-largest effect in the study and it corroborates the answer's
  central thesis, so I have promoted it into the analysis rather than just tabulating it:
  the "which differences are real" paragraph now leads on macro-F1 across both splits, and
  the "why triadic works" paragraph quotes the val gain (+0.0194, 2.5 sd) alongside the
  test gain (+0.0141, 2.3 sd). I also added the explanation for *why* macro-F1 is where
  triadic's advantage shows up: it is the metric that rewards the small countries, and a
  small country is a tight triangle-dense community.
- **[1.2 minor] The six `val_hit@1_deg*` columns are restored.** Rather than widen
  Table 1 to 14 columns I added **Table 3**: validation Hit@1 by degree bucket for all
  seven strategies — literally those columns — with bucket sizes in the caption, and
  re-captioned Table 1 to say it carries the scalar metrics with the per-degree columns
  given in full in Table 3. This also fixes the "3 of 7 strategies" complaint.
  It surfaced something worth saying, so I said it: triadic wins every *aggregate* column
  but only three of six degree buckets, and I now note that per-bucket cells are far
  noisier than the aggregates instead of letting the reader assume a clean sweep.
- **[1.3 minor] Arithmetic error fixed.** It was a genuine metric mismatch: Hit@1 gap vs
  MRR spread. Now "a gap of about 0.64, roughly **thirty-two** times the **0.0198**"
  (0.64 / 0.0198 = 32.3), both quantities in Hit@1.
- **[1.4 minor] Self-refuting cost claim rewritten.** I no longer claim triadic is "as
  cheap as DeepWalk". It now says sampling costs 1.9 s vs DeepWalk's 0.7 s *because* each
  step draws from a weighted table, and that this is negligible against the ~40 s of
  Skip-Gram training that follows — which is the defensible version of the point.
- **[1.5 minor] Validation-bias caveat added, and the argument re-based on test.** The
  three columns that are the selection criteria are marked `†` in Table 1 with the caption
  explaining why, and "Which differences are real" now opens by naming val H@1/val MRR/val
  micro-F1 as optimistic and rests the case on test (4.1×, 4.2×, 3.9×). One nuance I added
  because it matters for [1.1]: val **macro**-F1 is *not* the selection objective —
  `CountryClassifier` selects `C` on validation accuracy — so it is less compromised than
  the other val columns, and the unbiased test macro-F1 column agrees with it on both the
  winner and the ordering.
- **Informational note also fixed:** the `impl.py` comment that called the internal rank
  "pessimistic" now correctly says optimistic and notes it is only the `C`-selection
  criterion. Comment-only; I re-ran `deepwalk` afterwards and it is still bit-exact.

Re-verified after the edits: fragment compiles to 8 pages, **zero** overfull boxes, no
undefined references; `lint_output.py` passes; no `\documentclass`/`\usepackage`/`document`
env; all labels namespaced `p1:`. `trace_numbers.py` now finds 156 distinct 4-dp numbers,
152 traceable to artefacts; the 4 exceptions are prose differences I checked by hand
(0.0083 = 0.7207−0.7124; 0.0141 = 0.6974−0.6833; 0.0194 = 0.6833−0.6639; 0.2009 = the
control MRR 0.20087… rounded). Every generated table row in `tables.tex` — Tables 1, 2 and
3 — matches `answer.tex` exactly; the only generated rows not in the answer are Table 1b's
per-strategy standard deviations, condensed on purpose into the single noise-floor row.

Thank you for the node2vec unit test — that retires my §5 worry, and I have removed it
from the confidence list below rather than leaving a doubt you disproved.

---

# p1 — submission

## What the problem asked

Task 3 of HW2-Part(B) (notebook sections 1–6): implement the four TODOs of
`input/graph_embedding-1.ipynb` — `sample_walks`, `train_embedding`, `LinkPredictor`,
`CountryClassifier` — reproduce DeepWalk and node2vec, add at least one sampling strategy
of my own, run everything through the provided `run_experiment` / `comparison_table`
machinery on the LastFM-Asia graph, report link-prediction Hit@1/MRR (val+test), the
per-source-degree breakdown, and country-classification micro/macro-F1, then analyse which
strategy helps which task and why. `LinkPredictor` and `CountryClassifier` must be held
fixed while the embedding varies. Task 4 (heterogeneous, sections 7–8) is out of scope.

**Brief vs. assignment page: no discrepancy found.** I read the slide deck rendered
pages 8 and 9 through all three channels — `page_008.txt` / `page_009.txt`,
`page_008.png` / `page_009.png`, and the native-resolution figure files
`page_008_fig_02.jpeg`, `page_009_fig_02/03/04.jpeg`. The master's claim that those
figures are illustrative recaps only is correct: `page_009_fig_03.jpeg` is a toy
"Walk 1 … Walk 5" table of A–G node sequences and `page_009_fig_04.jpeg` is a 7×6
heatmap standing in for an embedding matrix. **Neither contains data or parameter values.**
The only thing the slide adds over the notebook is a mention of struct2vec and the
suggestion to "first re-implement DeepWalk/Node2Vec, and then test your own ideas".
The notebook is authoritative for everything that matters and I worked from it.

## What I decided it needed

**code + diagram + plain**, all three.

- *code*, mandatory: the deliverable is a table of measured numbers. Nothing is estimated.
- *diagram*: the per-degree breakdown is the question's own framing, and the
  "is one embedding best for both tasks" question is a two-axis scatter. Two vector PDFs.
- *plain*: the analysis carries a large share of the marks.

I also decided, after seeing the seed-0 results, that a **three-seed repeat of the whole
protocol** was necessary. The seven strategies span only ~0.013 test MRR, so without a
noise floor any claim of a "winner" would have been unfalsifiable. This turned out to be
the most important methodological decision in the problem — see Results.

## What I did

Copied the notebook's scaffolding verbatim into `scaffold.py` (sections 1, 2, 5) and
`run_all.py` (`run_experiment`, which needs module-level globals), and wrote the four
TODOs in `impl.py`. A strategy is a set of constructor kwargs; the walk budget
(10 walks × length 40 from each of the 6,958 non-isolated nodes = 69,580 walks) and every
Skip-Gram hyper-parameter are **identical across all seven strategies**, so the transition
rule is the only thing that varies. Both downstream models are the same code for every
run, as the notebook demands.

Seven strategies: DeepWalk (uniform), node2vec at (p=1,q=0.5), (p=1,q=2), (p=q=0.25) via
O(1) rejection sampling, and three of my own — RWR (teleport to `start` w.p. 0.15),
degree-corrected (P(x) ∝ deg(x)^-1), and triadic (P(x) ∝ 1 + |N(cur) ∩ N(x)|).

Word2Vec uses `workers=1` and `sample=0`. `workers=1` because gensim's multi-threaded
training is nondeterministic and I wanted the run to be bit-exactly reproducible by the
validator; it costs ~40 s per strategy, which was affordable. `sample=0` because gensim's
default frequent-token subsampling would itself down-weight hubs and thereby
half-implement the degree-corrected strategy, confounding that specific comparison.

## Intermediate steps and code

All paths relative to PLAYGROUND (`problems/p1/`). Interpreter is
`../../venv/bin/python` throughout; `data` is a symlink to the read-only shared dataset.

| file | what it does | command |
|---|---|---|
| `scaffold.py` | notebook sections 1/2/5 copied verbatim (download loop removed, data is on disk) | imported |
| `impl.py` | **the four TODOs** — this is the code shown in the answer | imported |
| `run_all.py` | `run_experiment` verbatim + the 7 strategies at seed 0 | `../../venv/bin/python run_all.py` → `run_all.log`, `results_comparison.csv`, `results_full.pkl` |
| `seed_study.py` | re-runs all 7 strategies at seeds 1 and 2 | `../../venv/bin/python seed_study.py` → `seed_study.log`, `results_seeds.csv`, `results_seeds.pkl` |
| `control_random.py` | sanity control: same pipeline on a random Gaussian Z | `../../venv/bin/python control_random.py` |
| `check_claims.py` | recomputes every per-bucket number quoted in the analysis, seed-averaged | `../../venv/bin/python check_claims.py` |
| `make_tables.py` | emits the LaTeX table bodies from the pickles | `../../venv/bin/python make_tables.py > tables.tex` |
| `make_figs.py` | writes both vector PDFs straight into OUTPUT | `MPLCONFIGDIR=$PWD/.mplcache ../../venv/bin/python make_figs.py` |
| `trace_numbers.py` | audit: asserts every `0.NNNN` in `answer.tex` appears in a generated artefact | `../../venv/bin/python trace_numbers.py` |

**Reproducibility, verified not assumed.** I re-ran the full 7-strategy sweep and
`control_random.py` from scratch after finishing the write-up; both reproduced their
earlier numbers **bit-exactly** (e.g. DeepWalk val Hit@1 0.6039 / MRR 0.7226, test 0.6023
/ 0.7214; control test Hit@1 0.06713018460800767). This is what `workers=1` bought.

`trace_numbers.py` reports 111 distinct 4-decimal numbers in `answer.tex`, of which 109
appear verbatim in a generated artefact. The 2 that do not are arithmetic on quoted
values and were checked by hand: `0.0083` = 0.7207 − 0.7124 (RWR's deficit) and `0.2009`
= the control MRR 0.20087… rounded.

**No number in `answer.tex` was typed by hand** — Tables 1 and 2 were generated by
`make_tables.py` and pasted; the prose numbers were all checked against `check_claims.py`.

Loading sanity check (printed by `run_all.py`, matches `split_stats.json` exactly):
19,464 edges, 666 isolated users, mean degree 5.106, max degree 153, 734 components,
train 19,464×6, val/test 4,171×21, 18 country classes, users split 763/763/6,098.

## Results

Everything below is measured. Table 1 of the answer is the mean over seeds {0,1,2}; the
raw per-seed rows are in `results_comparison.csv` (seed 0) and `results_seeds.csv`.

Comparison table (mean of 3 seeds) — from `make_tables.py`:

| strategy | val H@1† | val MRR† | test H@1 | test MRR | val mi-F1† | val ma-F1 | test mi-F1 | test ma-F1 |
|---|---|---|---|---|---|---|---|---|
| DeepWalk | 0.6040 | 0.7227 | 0.6009 | 0.7207 | 0.7641 | 0.6639 | 0.7629 | 0.6833 |
| node2vec p=1,q=0.5 | 0.5995 | 0.7202 | 0.5959 | 0.7184 | 0.7636 | 0.6621 | 0.7621 | 0.6825 |
| node2vec p=1,q=2 | 0.6027 | 0.7210 | 0.6011 | 0.7196 | 0.7619 | 0.6467 | 0.7607 | 0.6802 |
| node2vec p=q=0.25 | 0.6039 | 0.7217 | 0.6061 | 0.7228 | 0.7610 | 0.6581 | 0.7628 | 0.6796 |
| RWR r=0.15 | 0.5870 | 0.7119 | 0.5889 | 0.7124 | 0.7637 | 0.6521 | 0.7620 | 0.6733 |
| deg-corrected α=1 | 0.6003 | 0.7144 | 0.5990 | 0.7121 | 0.7575 | 0.6421 | 0.7607 | 0.6781 |
| **triadic** | **0.6066** | **0.7247** | **0.6087** | **0.7248** | **0.7645** | **0.6833** | **0.7661** | **0.6974** |
| *noise floor (mean sd)* | 0.0028 | 0.0021 | 0.0048 | 0.0031 | 0.0055 | 0.0077 | 0.0032 | 0.0062 |
| *spread / noise* | 7.0× | 6.0× | 4.1× | 4.2× | 1.3× | 5.4× | 1.7× | 3.9× |

† = measured on the split `fit` selects `C` on, therefore optimistic. The argument rests
on the test columns. (val ma-F1 is not itself the selection objective — `C` is chosen on
validation accuracy — so it is less compromised than the other three.)

Key claims and where each comes from:

- **Triadic wins all eight columns.** `make_tables.py` bolding, 3-seed means.
- **Spread / noise ratios** (last row of the answer's Table 1): 7.0×, 6.0×, 4.1×, 4.2×,
  1.3×, 5.4×, 1.7×, 3.9× — `make_tables.py` "inline numbers" block. The 1.3×/1.7× on
  country micro-F1 is why I state that micro-F1 cannot distinguish the strategies; the
  5.4× on val macro-F1 and 3.9× on test macro-F1 are why the macro columns can.
- **Table 3** (`val_hit@1_deg*`, all 7 strategies, 3-seed means) — `make_tables.py`
  "TABLE 3" block. Bucket sizes 213/261/524/842/973/1358 from the val breakdown.
- **Per-degree breakdown** (answer Table 2), 3-seed means, `check_claims.py`. Triadic −
  DeepWalk test Hit@1 per bucket: −0.0154, +0.0038, +0.0057, +0.0036, +0.0121, +0.0125.
  RWR − DeepWalk: 0.0000, +0.0113, −0.0086, −0.0151, −0.0053, −0.0218.
  deg-corrected − DeepWalk: −0.0247, +0.0013, −0.0199, −0.0067, +0.0099, +0.0019.
- **Random-Z control** (`control_random.py`): test Hit@1 0.0671, MRR 0.2009, country test
  micro-F1 0.1340. Chance is 0.0476 / 0.1736; majority-class rate 0.2062.
- **Cold bucket across all 21 runs** ranges 0.0139–0.1065; DeepWalk's own three seeds give
  0.0833 / 0.0231 / 0.0278 (`check_claims.py`). This is what licenses calling it noise.
- **Class imbalance**: 18 classes, largest 1,572 users, smallest 16 (only 2 in the
  763-user training split) — computed from `data/task2/node_country.csv` joined with
  `data/task3/country_split.csv`.
- **Sampling times** quoted in the conclusion (0.7 s DeepWalk, 1.3 s node2vec, 1.9 s
  triadic for the whole 69,580-walk corpus) are from `run_all.log`.

## Deliverables

- `OUTPUT/answer.tex` — LaTeX fragment, starts at `\section`, no `\documentclass` /
  `\usepackage` / `document` env. All 9 labels namespaced `p1:`.
- `OUTPUT/fig_p1_degree.pdf` — grouped bar chart, test Hit@1 by source-degree bucket for
  DeepWalk / triadic / RWR with seed error bars. Vector (0 raster images, 96 vector
  drawings), 5.8 × 3.3 in.
- `OUTPUT/fig_p1_tradeoff.pdf` — the two tasks on two axes, one point per strategy with
  ±1 sd error bars. Vector, 5.8 × 3.9 in.
- `OUTPUT/preamble.txt` — 9 `\usepackage` lines.

`lint_output.py` passes. I compiled the fragment inside a wrapper (`tex_test/`, in the
playground): 8 pages, exit 0, zero overfull boxes, no undefined references. I rendered
and looked at both figures and fixed three legibility defects found that way (n-labels
hidden behind bars, a colliding "random" annotation, and a legend sitting on top of two
data points in the trade-off plot).

**Environment note worth passing on:** a plain `\begin{itemize}` **fails to compile in
this TinyTeX** — the default bullet requests the TS1 font `tcrm1095`, which is not
installed, and pdflatex dies at shipout with no PDF produced. I found this by bisection
and worked around it with `\begin{itemize}[label=$\bullet$]` (enumitem), which is local to
my fragment and cannot affect other problems. For the same reason I replaced my global
`\lstset` with a namespaced `\lstdefinestyle{p1code}` so my listing style cannot leak into
another problem's listings in the merged document.

**One process note, in the interest of not hiding anything:** partway through verification
I ran `run_all.py deepwalk` to confirm reproducibility, and because `run_all.py` wrote its
artefacts unconditionally, that filtered run truncated `results_full.pkl` to a single row.
No reported number was affected (the re-run was bit-identical), but I fixed `run_all.py`
so a filtered run refuses to write, regenerated the full sweep, and regenerated every
table and figure from the restored pickle before finalising.

## Where I am least confident

1. **The listings are lightly condensed.** `impl.py` is authoritative. In the answer's
   TODO 1 listing I wrote `self.params["p"]` where the real code is
   `self.params.get("p", 1.0)`, and I dropped two `if not nbrs: break` guards that are
   unreachable (isolated nodes return `[]` before that point). The helper bodies
   `_nbr_lists` and `_weighted_tables` are described in comments rather than listed, to
   keep the listing to the length the brief asked for. Nothing algorithmic is hidden.
2. **`triadic` wins, but the per-metric margins are modest.** Test MRR 0.7248 vs
   DeepWalk 0.7207 is +0.0041 against a mean within-strategy sd of 0.0031 — only ~1.3 sd
   on that single metric. My confidence comes from it winning *all eight* columns
   simultaneously and from the macro-F1 gaps (+0.0194 val at 2.5 sd, +0.0141 test at
   2.3 sd), not from any one number. Three seeds is a small sample; five or ten would be
   better and I did not run them (each full sweep is ~12 min). I would still not defend
   "triadic is best" as strongly as I would defend "RWR and degree-corrected are worse
   than DeepWalk" or "micro-F1 cannot tell these apart" — those have more margin.
   Adding the val macro-F1 column strengthened this claim rather than weakening it, which
   is worth noting: the evidence I had dropped was evidence *for* my own conclusion.
3. **Model selection happens inside `fit` per strategy.** The `C` grid search is the same
   code everywhere, but a different `C` may be selected for different embeddings. I read
   this as what `fit(..., pairs_val, y_val)` is for, and it keeps the *predictor* fixed in
   the sense the notebook means. A stricter reading — freeze `C` once and reuse it — would
   be defensible and I did not test whether it changes the ranking.
4. **The cold-start interpretation is an inference, not a direct measurement.** I argue
   the 666 isolated users get zero rows and therefore chance-level scores; I verified the
   zero rows directly (`train_embedding` produces exactly 666 all-zero rows) and verified
   that the bucket matches the random-Z control, but I did not ablate the
   destination-side features to prove that is the only signal left.
5. ~~**`node2vec` might have an implementation bug.**~~ **Retired.** The validator
   unit-tested the sampler empirically: the second-order 1/p, 1, 1/q weights match theory
   to <0.0007 over 300k samples at all three (p,q) settings, and the first-order rules
   (uniform, degree-corrected, triadic) match to <0.0013 over 200k samples. The bias is
   provably correct, so "node2vec buys nothing here" is a finding about this graph, not a
   bug. I am leaving the entry visible rather than deleting it, since the round-1 answer
   was written under that doubt.
6. **A process failure worth recording, not just the technical ones.** The round-1 defect
   [1.1] was not a hard judgement call — the number was sitting in my own
   `make_tables.py`, computed and then dropped, and it turned out to be the second-
   strongest result in the study. I checked that every number I *printed* was correct and
   traceable, and never checked that every number the brief *asked for* was printed. The
   `trace_numbers.py` audit I built enforces soundness in one direction only; a
   completeness check against the brief's list of required metrics would have caught it.
