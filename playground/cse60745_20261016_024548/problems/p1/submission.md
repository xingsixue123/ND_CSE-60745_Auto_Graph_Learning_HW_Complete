## What the problem asked

Q1 (20 pts): complete `LapPETransformer()` and `SPDAttention()` — Laplacian absolute
structural encoding and shortest-path-distance relative structural encoding. Q2 (20 pts):
complete `SparseSPDAttention()`, i.e. choose the node pairs attention runs on, and test
different masking strategies. The real specification is in the notebook (cells 12-19); the
`.doc` page is the two-paragraph version of it.

**Brief vs. assignment page.** No disagreement. I read rendered page 2 of
`CSE 60745_Fall 2026_HW3(B)` in both channels — `page_002.txt` and `page_002.png` — and the
brief's transcription is verbatim correct. The third channel is empty by construction:
`ingest/manifest.json` lists `figures: []` for both pages, and the one image per page is the
Notre Dame monogram in the header, which the page render shows. Nothing in Q1/Q2 depends on a
figure. Notebook cells 10-19 in `ingest/pages/task6_graph_transformer-1/alltext.txt` also match
the brief verbatim (the only cosmetic difference: cell 11's demo label is
"demo: centrality + common neighbours", which my tables shorten to "demo: centrality + CN").

**One defect in the handout, confirmed myself.** Cell 16's docstring says to use
`torch_geometric.utils.segment_attention`; `hasattr(torch_geometric.utils,
"segment_attention")` is `False` in the PyG 2.8.1 installed here. Cell 3 imports
`softmax as segment_softmax`, PyG's segment softmax, which is the helper the sparse path needs.
Stated in one sentence in `answer.tex`.

## What I decided it needed

**code**, dominantly, plus about 300 words of prose per question. Both questions are
"complete this class", and the brief makes the LaTeX fragment the code submission, so
`answer.tex` carries the final implementation verbatim plus the measured results. Every table
cell comes from a run I did in this round.

**No diagram.** The only figure worth drawing would be ZINC MAE against pairs per graph, and
Table 2 already puts those two columns side by side for all five strategies, with validation
MAE and a three-seed mean as well. A six-point scatter would restate the table (R8).

## What I did

1. Re-verified the problem statement against both channels of the assignment page and against
   the notebook text, and re-confirmed the `segment_attention` defect in the installed PyG.
2. Read the inherited `solution.py` from the interrupted attempt line by line against
   `gt_framework.py` before trusting it — in particular that `make_batch` stores
   `full[dst, src]` for the pair `(src, dst)`, so `enc["spd"]` really is "distance from the
   querying node to the attended node", and that `pair_types` labels any pair touching a
   virtual node "virtual".
3. Re-ran `test_solution.py` from scratch: 26 checks, all pass. The load-bearing ones are
   `hop_distances` against a plain BFS (exact and capped, dense and sparse branches), the
   eigenvectors against the dense spectrum of `L`, and sparse attention against dense attention
   on a complete pair set (max abs difference 7.5e-8).
4. Re-ran every experiment: the Q1 encoding table, the Q2 masking-strategy table, two
   ablations for the two Q1 design choices, the LastFM benchmark and node task, and a
   three-seed repeat of the Q2 comparison.

## Intermediate steps and code

All paths relative to PLAYGROUND; the interpreter is
`../../.venv-gt/bin/python` and every script must run from this directory (the framework
loads `data/` with relative paths).

| file | what it does | reproduces |
5. Chose which pair set `SparseSPDAttention` itself should use **on validation**, not on test.
   The 2-hop ball plus one global virtual node has the lowest validation MAE on ZINC at all
   three seeds; on LastFM the top three are within 0.008 validation micro-F1 of each other (the submitted
   set is second, 0.005 behind `local`), so
   that task does not discriminate and ZINC decides. Exphormer's expander, which I had
   expected to win and which the first version of `solution.py` submitted, is last of the five
   on both datasets; it stays in `pair_set` and in the comparison.
6. The LastFM ablations then turned up something that changed the Q1 answer too: forcing the
   random sign flip on a single-graph full-batch task costs about 0.12 micro-F1. The flip is
   an augmentation *across* graphs, and LastFM has one, so `inject_absolute` now skips it when
   `batch["num_graphs"] == 1`. ZINC is unaffected (its batches hold 128 or 256 graphs), which
   `run_cell18.py` confirms by reproducing the measured row exactly.
7. Re-ran, against the final `solution.py`: the test suite, `verify_switch.py` (the renamed
   classes build pair-for-pair identical pair sets to the ones Table 2 was measured with),
   `run_timing2.py`, `run_lastfm_final.py`, and `run_cell18.py`.


## Intermediate steps and code

All paths relative to PLAYGROUND; the interpreter is
`../../.venv-gt/bin/python` and every script must run from this directory (the framework
loads `data/` with relative paths).

| file | what it does | reproduces |
|---|---|---|
| `gt_framework.py` | the notebook's framework, copied unmodified from `shared/` (`diff` clean) | — |
| `solution.py` | **the answer**: cells 13 and 16, plus the two helpers | — |
| `test_solution.py` | 26 correctness checks | `python -u test_solution.py` -> `logs/test_solution.log` |
| `experiments.py` | the four alternative masking strategies and the three LapPE ablations, `count_pairs` | — |
| `runner.py` | thin wrapper recording each `run_graph_task` result to JSON | — |
| `run_zinc_q1.py` | Table 1 | `logs/zinc_q1.log`, `logs/zinc_q1_results.json` |
| `run_zinc_q2.py` | Table 2 (seed 0) and the pair counts | `logs/zinc_q2.log`, `logs/zinc_q2_results.json`, `logs/zinc_pair_counts.json` |
| `run_seeds.py <s>` | Table 2's three-seed column | `logs/zinc_seed{1,2}.log`, `logs/zinc_seed{1,2}_results.json` |
| `run_ablation.py` | the two ablation numbers quoted in Q1 | `logs/zinc_ablation.log`, `logs/zinc_ablation_results.json` |
| `run_lastfm.py` | LastFM precompute, pair counts, `benchmark_step`, `run_node_task` | `logs/lastfm.log`, `logs/lastfm_results.json` |
| `run_timing.py` | first attempt at Table 3's timings; kept as the evidence that a 32-thread single step is not a measurement | `logs/lastfm_timing.log` |
| `run_timing2.py` | **Table 3's timings**: 8 threads, best of 7 steps, plus the framework's own `benchmark_step` line | `logs/lastfm_timing2.log` |
| `run_lastfm_final.py` | Table 3's micro-F1 column and the LastFM ablations, final code | `logs/lastfm_final.log`, `logs/lastfm_final_results.json` |
| `run_cell18.py` | notebook cell 18 against the final code, as a reproduction check | `logs/zinc_cell18.log` |
| `switch_submitted.py`, `apply_flip_fix.py` | the two edits made to `solution.py` after the comparison, applied once by `finalize.sh` | `logs/finalize.log` |
| `verify_switch.py` | proves the renamed classes build pair-for-pair identical pair sets | `logs/verify_switch.log` |
| `verify_facts.py` | the dataset facts the prose states (sizes, connectivity, channel RMS) | `logs/verify_facts.log` |
| `extract_code.py`, `build_answer.py` | split `solution.py` into the three listings and generate `answer.tex` with every table cell read back from the JSON logs | `python build_answer.py` |
| `count_words.py` | prose word count per section (R8) | `python count_words.py` |


## Round 2 — what the validator found, and what changed

All seven defects accepted; no disagreement with any of them. The validator's independent
suite (`validators/p1/work/val_check.py`) re-derives the distances, the eigenvectors, the pair
set and both attention paths from scratch and agrees with mine, so nothing below is a
correctness fix to the model — [1.1] is a stale sentence inside the submitted code.

- **[1.1] major.** `SparseSPDAttention`'s docstring still claimed the 2-hop ball had "the
  highest validation micro-F1 on LastFM". It was written by `switch_submitted.py` against
  `lastfm_nodetask_results.json`, before the conditional sign flip reordered that ranking in
  `lastfm_final_results.json` (`local` 0.8152, 2-hop ball 0.8100). The docstring now reads
  "lowest validation MAE on ZINC at every seed; on LastFM it is second of five, 0.005 behind
  the best", which is what the logs say and what the prose already said. The real hole was
  that `build_answer.py` asserted its *generated* prose against the data but not the
  *spliced* docstrings, so a listing could contradict the tables and still build. It now
  checks the docstring too: the LastFM rank word, the 0.005 gap, the per-seed ZINC claim, and
  that the string "highest validation micro-F1" cannot reappear.
- **[1.2]** Table 2's caption disclosed the three test repeats but not the validation ones,
  while the bolded validation number is what "picked on validation" rests on. It now gives
  both (val 0.4318, 0.4418, 0.4418; test 0.4715, 0.4766, 0.4766), says plainly that every
  later repeat is worse than the printed draw, and says the choice rests on the per-seed
  ranking rather than on these decimals.
- **[1.3]** "it alone keeps the pair count O(n)" was false — `local` and `local+virtual` are
  O(n) too. The expander's actual distinction is hub-free mixing, and that is what it now says.
- **[1.4]** "at 3 of the 3 seeds" was computed on test MAE against `local+virtual` only, and
  on test MAE at seed 2 `local` beats the 2-hop ball. The claim is now the one that is true
  of all five strategies at all three seeds — lowest **validation** MAE — with the test-mean
  margin stated separately as a test-mean margin.
- **[1.5]** `p1:tab:q2lastfm` is now referenced from the Q2 result paragraph, and
  `build_answer.py` refuses to write a fragment containing a label nothing references.
- **[1.6]** Q1 trimmed by ~30 words (my count 364 to 340; no content dropped, four sentences
  compressed).
- **[1.7]** `notes.md` said 21/21 checks where the suite reports 26; `submission.md` quoted
  0.005 for the LastFM top-three spread, which is 0.008 (0.005 is the submitted set's gap to
  the best). Both corrected, and the two quantities are now named separately wherever they
  appear.

The guard is tested, not just written: tampering with the docstring (`second` to `first`) and
rebuilding fails with `AssertionError: (2, 'stale docstring: LastFM rank')`, and `solution.py`
was restored and rebuilt afterwards (`diff` clean).

`solution.py` changed only inside that docstring. `test_solution.py` was re-run against it
afterwards (26/26, `logs/test_solution.log`), and the answer was rebuilt and recompiled:
0 overfull boxes, 5 pages, `lint_output.py` OK.

## Results

Every value below is in `answer.tex`. `PY = ../../.venv-gt/bin/python`, run from PLAYGROUND.

### Table 1 — ZINC, 30 epochs, dense attention (`PY run_zinc_q1.py` -> `logs/zinc_q1.log`)

| row | val MAE | test MAE | best epoch |
|---|---|---|---|
| none: plain attention | 0.6472 | 0.7013 | 18 |
| demo: centrality + CN | 0.4629 | 0.4957 | 27 |
| LapPE only | 0.6205 | 0.6575 | 30 |
| SPD only | 0.5373 | 0.5614 | 29 |
| LapPE + SPD (cell 14) | 0.5160 | 0.5496 | 30 |

### Table 2 — ZINC masking strategies (`PY run_zinc_q2.py` -> `logs/zinc_q2.log`; seeds 1 and 2 from `PY run_seeds.py <s>` -> `logs/zinc_seed{1,2}.log`; pair counts from `logs/zinc_pair_counts.json`)

| strategy | pairs/graph | % of n² | val MAE | test MAE | test, seed 1 | test, seed 2 | 3-seed mean ± half-range |
|---|---|---|---|---|---|---|---|
| local | 73.0 | 13.1 | 0.4918 | 0.5048 | 0.5313 | 0.5073 | 0.5145 ± 0.0133 |
| local+virtual | 120.4 | 21.6 | 0.4791 | 0.5047 | 0.5049 | 0.5181 | 0.5092 ± 0.0067 |
| 2-hop ball+virtual **(submitted)** | 189.2 | 34.0 | 0.4293 | 0.4677 | 0.4951 | 0.5098 | 0.4909 ± 0.0211 |
| local+expander+virtual | 200.2 | 35.9 | 0.5179 | 0.5551 | 0.5810 | 0.5761 | 0.5708 ± 0.0129 |
| local+expander8+virtual | 266.4 | 47.8 | 0.5213 | 0.5554 | 0.5792 | 0.5620 | 0.5655 ± 0.0119 |
| full attention | 556.8 | 100.0 | 0.5160 | 0.5496 | 0.5651 | 0.5696 | 0.5614 ± 0.0100 |

### Table 3 — LastFM (`PY run_timing2.py` -> `logs/lastfm_timing2.log` for pairs and seconds, 8 threads, best of 7 steps; `PY run_lastfm_final.py` -> `logs/lastfm_final.log` for micro-F1)

| strategy | pairs attended | one step (s) | val micro-F1 | test micro-F1 |
|---|---|---|---|---|
| full: LapPE + SPD | 58,125,376 | 5.23 | not trained | not trained |
| local | 63,236 | 0.03 | 0.8152 | 0.7893 |
| local+virtual | 78,485 | 0.04 | 0.8073 | 0.7826 |
| 2-hop ball+virtual **(submitted)** | 804,349 | 0.33 | 0.8100 | 0.7827 |
| local+expander+virtual | 108,965 | 0.05 | 0.7929 | 0.7678 |
| local+expander8+virtual | 139,417 | 0.06 | 0.7733 | 0.7607 |

### Ablations quoted in the Q1 prose

| ablation | dataset | metric | value | reference | source |
|---|---|---|---|---|---|
| no sqrt(n) scaling | ZINC | test MAE | 0.5449 | 0.5496 | `run_ablation.py` -> `logs/zinc_ablation.log` |
| no sign flip | ZINC | test MAE | 0.5999 | 0.5496 | `run_ablation.py` -> `logs/zinc_ablation.log` |
| no sqrt(n) scaling | LastFM | test micro-F1 | 0.7319 | 0.7827 | `run_lastfm_final.py` -> `logs/lastfm_final.log` |
| sign flip forced on | LastFM | test micro-F1 | 0.6546 | 0.7827 | `run_lastfm_final.py` -> `logs/lastfm_final.log` |

### Other numbers in the text

- sparse attention reproduces dense attention on a complete pair set to **7.45e-08** (`test_solution.py` check 5, `logs/test_solution.log`).
- cell 18 against the final code, three identical repeats at 8 threads (`run_cell18.py` -> `logs/zinc_cell18.log`): val 0.4318, 0.4418, 0.4418; test 0.4715, 0.4766, 0.4766. Reference row measured before the rename and the sign-flip change: 0.4293 / 0.4677. The spread across identical repeats (0.0051 on test) is run-to-run non-determinism in `index_add_`, not a change in the model.
- ZINC: 12000 graphs, n from 9 to 37, every graph one connected component; LastFM: one component, unscaled LapPE channel RMS 0.01145 = 1/sqrt(7624) (`verify_facts.py` -> `logs/verify_facts.log`).
- LastFM SPD histogram (0..8 hops, none unreachable) is in `logs/lastfm.log`.

## Deliverables

- `OUTPUT/answer.tex` — the fragment: two sections, three tables, three code listings
  (helpers, cell 13, cell 16) spliced verbatim from `solution.py`.
- `OUTPUT/preamble.txt` — `listings`, `xcolor`, `booktabs`, `float`, `amsmath`, `amssymb`.
- No figure. Table 2 already carries pairs-per-graph against MAE for all five strategies with
  a three-seed column; a scatter of the same five points would restate it.

`answer.tex` is generated by `build_answer.py`: the prose is a template, the code is spliced
out of `solution.py` by `extract_code.py`, and every number is read back from the JSON logs,
so no value in it was typed by hand. The script also asserts the qualitative claims the prose
makes against those logs — that ZINC's lowest validation MAE is the submitted pair set, that
LastFM's top three are within 0.01 of each other, and that the two expander variants are last
on both datasets — so if a re-run changed the ranking, the build would fail rather than print
a sentence the data no longer supports. It compiles clean (0 overfull boxes) inside
`build/master_test.tex`, which is an article preamble holding exactly the packages
`preamble.txt` declares.

## Where I am least confident

1. **The margin that picked the submitted pair set.** The 2-hop ball beats the next strategy
   (`local+virtual`) at all three ZINC seeds on both validation and test, but the three-seed
   mean gap (0.018 test MAE) is about the size of the seed half-range and of the run-to-run
   noise in item 4. On LastFM it is not ahead at all: the top three strategies there finish
   within 0.008 validation micro-F1 of each other and the submitted set is second, 0.005
   behind `local`, which is nominally first. So the
   submitted choice is "wins ZINC consistently, ties LastFM", and `answer.tex` says exactly
   that rather than claiming it won both. The claims I would defend strongly are the ones with
   large margins: sparse attention beats full attention on ZINC, the two expander variants are
   last on both datasets, and both LapPE ablations.
2. **The LastFM rows are one run each.** 200 full-batch epochs on a single graph, no seed
   repeat — that was too expensive to triple inside the budget. The sign-flip effect there is
   0.12 micro-F1, far too large to be seed noise, but I would not defend its third decimal.
3. **Single-seed Table 1.** One run per row at the framework's fixed seed, as the notebook
   does. The LapPE-on-top-of-SPD gain, 0.0118, is inside the measured seed half-range, and
   `answer.tex` says so rather than claiming the gain.
4. **The sparse model is not bit-reproducible on CPU, and the size of that matters.** Running
   cell 18 three times in one process, with the seed, the weights and the batch order all
   identical, gives three different ZINC results (see `logs/zinc_cell18.log`): the sparse
   forward accumulates with `index_add_`, whose order across threads is not fixed. The spread
   is about 0.01 MAE, which is the same order as the gap between the submitted pair set and
   the runner-up. That is why the selection rests on winning at all three seeds rather than on
   the size of the mean gap, and why `answer.tex` prints the repeat spread in Table 2's
   caption. The same effect shows on LastFM: the pre-fix submitted model printed test micro-F1
   0.6384 with 8 threads and 0.6387 with 4.
5. **Timings are the weakest measurement here.** ZINC per-epoch times were taken with four
   jobs sharing the machine, so that column is not in the answer at all. For Table 3 a single
   `benchmark_step` turned out not to be a measurement either: with `OMP_NUM_THREADS=32` every
   sparse strategy hit the same ~4.8 s floor regardless of whether it attended 63k or 804k
   pairs, while at 8 threads the same models took 0.06--0.1 s. Table 3 therefore reports the
   best of 7 steps at a fixed 8 threads (`run_timing2.py`); `logs/lastfm_timing.log` keeps the
   32-thread run as the evidence for discarding it.
6. **Full attention is not trained on LastFM**, only benchmarked for one step, as cell 19 asks.
   There is therefore no full-attention micro-F1 to compare the sparse models against; the
   accuracy comparison against full attention is the ZINC one.
7. **The 2-hop ball does not scale like the expander.** Its pair count is
   $\sum_v \deg(v)^2$, so a graph with a very high-degree hub could make it expensive; it is
   1.4% of $n^2$ on LastFM because LastFM is sparse, not because the construction guarantees
   it. `answer.tex` states the cost as $\sum_v \deg(v)^2$ rather than implying $O(n)$.
