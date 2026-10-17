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
