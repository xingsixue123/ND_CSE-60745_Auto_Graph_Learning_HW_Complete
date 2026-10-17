## What the problem asked

Q3 of *CSE 60745 (Fall 2026) – HW3-Part(B)*, 30 points, on rendered page 2 of the `.doc`:

> **Q3: Hybrid Graph Transformer (30 pts)**
> Complete HybridGTLayer() to implement a hybrid graph transformer composed of both
> MPNN-based local attention and transformer-based global attention. You can implement
> GraphGPS or design your own hybrid structures.

**The brief and the assignment page agree.** I read `page_002.txt`, `page_002.png` and the
notebook text, and reconciled them (R7). The `.doc` has no figures: `ingest/manifest.json`
lists `"figures": []` for both pages and `n_images: 1`, which is the Notre Dame monogram in
the running header — I looked at both page PNGs and confirmed that is the only image. So
there is no figure channel to read for this problem, and nothing in my answer rests on one.

The operative specification is the notebook, `task6_graph_transformer-1.ipynb`: cell 20
(what a hybrid layer is), cell 21 (the signature `__init__(dim, heads)` /
`forward(x, edge_index, edge_attr, batch)`), cell 22 (`HybridGT`, the driver that calls it).
Cell 22 as given in the brief is byte-identical to cell 22 of the notebook; I checked this
programmatically rather than by eye, and my `HybridGT` is that text verbatim.

## What I decided it needed

**code + plain + a diagram.**

- *code*, because the question is "complete `HybridGTLayer()`" and cell 22 runs it on ZINC.
  Every number in the answer comes from a run I did.
- *plain*, because the marks for a 30-point design question are in **how the two branches
  are combined and why**, which is an argument, not a number.
- *diagram*: optional by the brief. I made one, because the parallel-sum structure (two
  branches reading the same input, two residuals, one sum) is the whole point of the answer
  and is much faster to read as a block diagram than as prose. It is drawn in TikZ and
  compiled to a standalone PDF, so the master only needs `graphicx`.

## What I did

**Design.** GraphGPS, with the two substitutions named in the answer. Local branch: GINE
written from scratch with `index_add_` (no PyG `MessagePassing`), bond type embedded into
the message. Global branch: the framework's own multi-head attention algebra, applied to
`to_dense_batch(x, batch)` so attention cannot cross a molecule boundary. Combination:
each branch gets a residual and a LayerNorm, the two are summed, and a residual MLP
follows — GraphGPS Eqs. (9)–(11) from Appendix D.1 of the paper, with LayerNorm for
BatchNorm and dropout at zero.

**I read the GraphGPS paper rather than quoting it from memory** (R9). The two quotations
in the answer are from the downloaded PDF: "the edge features are only passed to the MPNN
layer" is in §3.3 under *Update function*, and "these layers could irreparably fail to keep
some information in the early stage" is in §3.3 under *Preventing early smoothing*. I read
past both. The second is the paper's argument against the GraphTrans-style MPNN-then-
Transformer stack, and the paragraph continues by noting the analogous 2-stage strategy
succeeded in computer vision but is not expected to transfer to graphs; I use it for exactly
the claim it makes (against stacking) and I tested the stacked alternative myself rather
than taking the paper's word for it. The precise per-branch residual/norm/dropout equations
I follow are Eqs. (6)–(11) in Appendix D.1, not the simplified Eqs. (1)–(4) of §3.3.

**Correctness checks before any training** (`check_isolation.py`, all pass, output in
`logs_checks.txt`). The brief flags that a global branch leaking across molecules "still
trains and still prints a plausible MAE", so I tested it rather than reading the code:

1. perturbing graph 0's node states changes graph 0's output and leaves every other graph
   bit-identical (max delta 0.0);
2. a graph run alone gives bit-identical output to the same graph inside a batch of 6;
3. attention puts exactly 0.0 mass on padding and every real row sums to 1.0;
4. the local branch matches an explicit per-edge reference loop (max delta 0.0);
5. the local branch actually uses the edges (output changes when they are removed);
6. `sum(deg) == E` and `batch["deg"]` matches a recomputed degree (invariant check);
7. the ablation harness `AblationGT(HybridGTLayer)` is parameter-for-parameter and
   output-for-output identical to plain `HybridGT()` after `_reset`, so an ablation row
   differs from the hybrid row only by the branch it removes.

**Experiments.** Seven configurations at 30 epochs (the framework's `EPOCHS_ZINC`): seeds
0–2 for the two baselines and the global-only ablation, where the gaps are 20–40 noise
widths and three runs settle them, and seeds 0–5 for the four configurations whose
differences are small (`hybrid`, `local-only`, `sequential`, `gated`). Plus 100-epoch runs
of the three that matter, and the three-run reproducibility probe in `logs_det/`. In total 39 training runs here, plus 7 archived in `logs_r1/`. The seed is varied by setting
`gt_framework.RANDOM_SEED` before the call — `_reset()` and `run_graph_task()` both read that
global at call time — not by editing `gt_framework.py`, which I did not modify.

I ran repeats because the effect I most needed to report is a *negative* one — removing the
global branch costs nothing measurable — and a single-run negative result is worth nothing
without a noise floor. Measuring that floor (point 1 below) turned out to matter more than
I expected: repeating one configuration unchanged moves test MAE about as much as changing
the seed does.

## Intermediate steps and code

All paths relative to PLAYGROUND. The interpreter for every one of them is
`../../.venv-gt/bin/python`.

| file | what it does |
|---|---|
| `hybrid_layer.py` | the deliverable: final `HybridGTLayer`, plus `HybridGT` (cell 22, verbatim). The listing in `answer.tex` is cut out of this file by `make_answer.py`, so it cannot drift from the code that ran. |
| `variants.py` | the four ablation layers (`LocalOnlyLayer`, `GlobalOnlyLayer`, `SequentialLayer`, `GatedLayer`) and `AblationGT`, which swaps `HybridGT`'s layer class. Nothing here is part of the answer. |
| `run_exp.py` | runs one configuration: `run_exp.py <name> <seed> <epochs>`. Prints a `### result` line. |
| `check_isolation.py` | the seven correctness checks above. Output: `logs_checks.txt`. |
| `graph_stats.py` | ZINC diameter, 4-hop coverage and degree distribution. Output: `logs_graph_stats.txt`. |
| `collect.py` | aggregates every `### result` line in `logs/` into the per-configuration mean and sd. |
| `answer_head.tex`, `OUT_preamble.txt` | the hand-written design prose and the package list that `make_answer.py` and `finalize.sh` copy into OUTPUT. |
| `wordcount.py` | counts prose words in a LaTeX fragment with listings, tables, figures and math stripped (rule R8). |
| `make_answer.py` | writes `OUTPUT/answer.tex`: design prose from `answer_head.tex`, the listing from `hybrid_layer.py`, the table from `logs/`. No number is typed by hand. |
| `fig/layer.tex` | the TikZ block diagram; `pdflatex` there produces `fig/layer.pdf`, copied to `OUTPUT/fig_p2_layer.pdf`. |
| `finalize.sh` | regenerates `answer.tex`, copies the figure and preamble into OUTPUT, test-compiles, counts words, lints. |
| `logs/` | raw console output, one file per `<experiment>_s<seed>_e<epochs>`. |
| `logs_r1/` | the first round of runs, before I reformatted the source to fit the listing width. Kept for comparison. |
| `logs_det/` | the reproducibility probe described below. |
| `smoke.py`, `smoke_variants.py` | first-run shape/gradient checks; superseded by `check_isolation.py`. |
| `refs/` | the downloaded GraphGPS PDF and the text extracted from it (recorded in `downloads.md`). |

**Reproducing any row of the table:** `cd` to PLAYGROUND and run
`OMP_NUM_THREADS=4 NTHREADS=4 ../../.venv-gt/bin/python run_exp.py <name> <seed> 30`,
with `<name>` one of `hybrid`, `local-only`, `global-only`, `sequential`, `gated`,
`baseline-plain`, `baseline-demo`. Then `python collect.py`.

## Results

Every number below is a `### result` line in `logs/`. Reproduce with
`run_exp.py <name> <seed> <epochs>`; aggregate with `collect.py`.

**ZINC test MAE, 30 epochs** (mean over runs ± sd; the epoch is chosen on val MAE by
`run_graph_task`). Log files are `logs/<name>_s<seed>_e30.log`.

| row in `answer.tex` | experiment | val MAE | test MAE | runs | active params |
|---|---|---|---|---|---|
| plain graph transformer | `baseline-plain` | 0.649 ± 0.004 | 0.693 ± 0.002 | 3 | 139,585 |
| demo: centrality + CN bias | `baseline-demo` | 0.469 ± 0.015 | 0.495 ± 0.018 | 3 | 143,889 |
| **hybrid GT (cell 22)** | `hybrid` | 0.350 ± 0.007 | **0.364 ± 0.008** | 6 | 211,589 |
| ablation: global branch removed | `local-only` | 0.353 ± 0.008 | 0.367 ± 0.007 | 6 | 144,517 |
| ablation: local branch removed | `global-only` | 0.533 ± 0.003 | 0.573 ± 0.003 | 3 | 143,745 |
| instead: sequential | `sequential` | 0.347 ± 0.006 | 0.359 ± 0.007 | 6 | 211,589 |
| instead: learned gate | `gated` | 0.340 ± 0.009 | 0.355 ± 0.005 | 6 | 244,613 |

**100 epochs, one run each** (`logs/<name>_s0_e100.log`), quoted in the answer's prose:

| experiment | val MAE | test MAE | best epoch |
|---|---|---|---|
| `local-only` | 0.2567 | 0.2514 | 98 |
| `hybrid` | 0.2804 | 0.2830 | 94 |
| `global-only` | 0.5172 | 0.5590 | 51 |

**Noise floor, 0.0087 test MAE** (`logs_det/`): three runs of `local-only seed 0 epochs 30`,
*identical configuration and seed*, two at 4 torch threads and one at 1 — test MAE 0.3702,
0.3615, 0.3620. Every comparative sentence in `answer.tex` is checked against this number by
an assertion in `make_answer.py`, which refuses to write the file if a claim stops holding.

**Facts about ZINC quoted in the answer** (`logs_graph_stats.txt`, from `graph_stats.py`):
mean diameter 12.5 over the 1000 test graphs; 51.8% of node pairs within 4 hops; node degree
takes 4 distinct values over 277,864 nodes, with 50.6% of nodes at degree 2. The claim "half
of all atoms share one value" is that 50.6%.

**Not hand-copied.** `make_answer.py` cuts the listing out of `hybrid_layer.py` and builds
the table from `logs/`, so the code in `answer.tex` is the code that ran and the table is
the logs. `./finalize.sh` regenerates everything, test-compiles and lints.

## Deliverables

| path | |
|---|---|
| `OUTPUT/answer.tex` | the fragment: design, the `HybridGTLayer` listing, Table 1, the reading. 475 prose words excluding listing, table and captions. Starts at `\section`; no `\documentclass`, `\usepackage` or `document` environment. |
| `OUTPUT/fig_p2_layer.pdf` | the layer block diagram, TikZ compiled standalone, 382×338 pt (5.3 in wide). Referenced by bare filename. |
| `OUTPUT/preamble.txt` | `graphicx`, `booktabs`, `listings`, `xcolor`, `amsmath`, `float`. |

Labels and files are namespaced: `p2:fig:layer`, `p2:tab:zinc`, `fig_p2_layer.pdf`, and the
listing style is `p2python`. Nothing from Q1 or Q2 is defined or mentioned.

## Where I am least confident

**1. A single run is not reproducible on this machine, even at a fixed seed.** I ran
`local-only seed 0 epochs 30` three times unchanged (`logs_det/`): test MAE 0.3702, 0.3615,
0.3620. `_reset` pins the seed, so this is float reduction order shifting with how many
threads torch actually gets, not a seeding bug — two of the three were at 4 threads and one
at 1, and even the two at 4 threads disagree. The spread, 0.0087, is as large as the
seed-to-seed sd, so I treat it as the noise floor for every comparison and ran 6 seeds on
the four configurations whose differences are small. **A validator re-running a row should
expect to land within ~0.009 of the table, not on the digit.** This also means my round-1
numbers (`logs_r1/`) do not match `logs/` exactly, and I cannot cleanly separate that from
the source reflow described in point 5.

**2. The gate is the softest number in the table.** It beats the plain sum by 0.0093 test
MAE against a 0.0087 noise floor — about one noise width, 6 runs each — and it carries 16%
more parameters, so the comparison is not capacity-matched. The answer says exactly that
and keeps the plain GraphGPS sum as the submitted layer. Reading it as "gating beats summing
in general" would be over-claiming, and so would dropping it.

**3. The 100-epoch result is one run per configuration.** local-only 0.2514 against the
hybrid's 0.2830 is a 0.032 gap, well past the noise floor, which is why I was willing to
say the gap opens the other way. But it is n=1, and I did not have time to repeat it.
It is the claim I would check first.

**4. The negative result is about this setting, not about hybrids.** "The global branch does
not pay for itself" holds at `dim=64`, 4 layers, with degree centrality as the only absolute
encoding — the configuration cell 22 fixes. GraphGPS's published ZINC numbers use RWSE and a
far longer schedule. I measured the two facts my explanation rests on (diameter 12.5 and
51.8% 4-hop coverage, so it is not a range problem; degree takes four values with 50.6% of
atoms sharing one, so it is an identity problem), but I did not test the fix: adding a
Laplacian or random-walk encoding is Q1's territory and out of scope here.

**5. The ablations are not capacity-matched, and the source was reflowed once.**
`local-only` and `global-only` carry ~144k trainable parameters against the hybrid's ~212k;
I report the active count per row so this is visible but ran no width-matched control. For
the direction the result points — the *larger* model being no better — this cuts the
harmless way. Separately, I reflowed `hybrid_layer.py` to fit the listing width before the
final sweep (e.g. splitting the `qkv` view/permute into two statements). The operations are
unchanged and everything in `answer.tex` comes from `logs/`, i.e. from the final source;
`logs_r1/` holds the earlier numbers for comparison.

**6. One thing I checked because I nearly got it wrong.** My first draft explained the
global branch's uselessness by saying ZINC molecules are small enough that four rounds of
message passing already cover them. I measured it instead of asserting it, and it is false:
mean diameter is 12.5 and four rounds reach 51.8% of pairs. The explanation in the answer is
the one that survived the measurement.
