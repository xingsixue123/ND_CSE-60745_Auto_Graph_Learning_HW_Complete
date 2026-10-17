# Worker validator checklist — p1 (Q1 structural encoding + Q2 efficient graph transformer)

## Round 1
Verdict: FAIL

### What I verified myself (not taken from the worker)
- **R7, assignment page.** Read `ingest/pages/CSE 60745_Fall 2026_HW3(B)/page_002.txt` and
  `page_002.png`, plus `ingest/manifest.json` (`figures: []`, `n_images: 1` = the ND monogram in
  the header, visible in the page render). The brief's transcription of Q1/Q2 is verbatim
  correct; nothing in this problem depends on a figure, so the third channel is empty by
  construction. Notebook cells 12-19 in `ingest/pages/task6_graph_transformer-1/alltext.txt`
  match the brief. Q3 belongs to another worker and does not appear in `answer.tex`.
- **Handout defect.** `hasattr(torch_geometric.utils, "segment_attention")` is `False` in the
  installed PyG 2.8.1; `softmax(src, index, ptr, num_nodes, dim)` is present. The answer's
  one-sentence note is accurate.
- **Framework untouched.** `diff problems/p1/gt_framework.py shared/gt_framework.py` -> identical.
- **Worker's suite re-run in my own directory**: 26 checks, all PASS.
- **My own independent suite** (`validators/p1/work/val_check.py`, log
  `validators/p1/logs/val_check.log`), written without reusing the worker's helpers:
  - `hop_distances` vs `scipy.sparse.csgraph.shortest_path` on 30 random ZINC graphs (max abs
    diff 0), on a hand-built disconnected graph with an isolated node, at caps 1/3/8, and on 12
    random LastFM sources (0 mismatches); unreachable pairs stay -1 under a cap.
  - `laplacian_eigvecs`: Rayleigh quotients equal dense eigenvalues 1..8 (<=1.1e-07),
    orthonormal columns, orthogonal to the trivial eigenvector D^{1/2}1, zero padding when
    n-1 < LAP_K.
  - `SparseSPDAttention.attention_pairs` is set-equal to {(i,j): d(i,j) <= 2} plus the virtual
    node, on 20 ZINC graphs.
  - Sparse `forward` vs a hand-built dense reference on the **real** (non-complete) pair set:
    max abs diff 1.19e-07. Dense `forward` vs a hand-built reference: 0.0.
  - `enc["spd"]` equals `D[querier, attended]` for every pair of a 4-graph batch.
  - Pair counts: 189.1828/graph, n^2 = 556.8356, LastFM 804,349 -- the table's 189 / 557 / 34%
    and 804,349 / 1.384%.
- **Table provenance.** Every cell of Tables 1-3 and every number in the prose traces to
  `logs/*.json` / `logs/lastfm_timing2.log`; `build_answer.py` reads them back rather than
  typing them. The three code listings are byte-verbatim from `solution.py` (checked with
  `extract_code.blocks`). Arithmetic spot-checked: 3-seed means and half-ranges, 0.0119 /
  0.0184 / 0.0799 / 0.0503 / 0.1281 / 0.0508, 16x, 1.384%.
- **LaTeX.** No `\documentclass`/`\usepackage`/document environment. All labels
  (`p1:tab:q1`, `p1:tab:q2`, `p1:tab:q2lastfm`) and all style/colour names (`p1py`, `p1kw`,
  `p1cm`, `p1st`) namespaced. Compiles in a minimal wrapper holding exactly `preamble.txt`:
  6 pages, 0 overfull boxes. Rendered to PNG and read -- listings legible at \scriptsize.
- **`lint_output.py` OK.** `downloads.md` records "(nothing installed)", consistent with the
  playground (prebuilt `.venv-gt` + copied `shared/data`).
- **My own reproduction runs** (`validators/p1/logs/val_rerun.log`, delivered `solution.py`,
  8 threads): cell 18 repeat 1 val 0.4451 / test 0.4792, repeat 2 val 0.4418 / test 0.4766;
  `local+virtual` val 0.4770 / test 0.4941; `local` val 0.4862 / test 0.5036. The Q2 ranking
  holds under my runs.

### Defects
- [1.1] **The delivered answer contains a false claim that contradicts its own prose.** In the
  "Implementation (notebook cell 16)" listing, the `SparseSPDAttention` docstring says the 2-hop
  ball "had the lowest validation MAE on ZINC **and the highest validation micro-F1 on LastFM**".
  Measured LastFM validation micro-F1 (`logs/lastfm_final_results.json`): `local` 0.8152,
  `local+virtual` 0.8073, **2-hop ball 0.8100** -- second, not highest. The answer's own Q2 prose
  two pages earlier says "the submitted set second of five", and `submission.md` says "`local` is
  nominally first". The docstring was written by `switch_submitted.py` against the *pre*
  sign-flip-fix `logs/lastfm_nodetask_results.json` (where the 2-hop ball was 0.6815, genuinely
  highest) and was never updated after `run_lastfm_final.py` reordered the ranking.
  | `OUTPUT/answer.tex`, `SparseSPDAttention` docstring (and `solution.py` line ~160, the source
  it is spliced from) | severity: **major**
  Fix: restate the LastFM half truthfully (e.g. "and was within 0.008 validation micro-F1 of the
  best on LastFM"), and extend `build_answer.py`'s consistency asserts (lines 254-262) to cover
  claims made inside the spliced docstrings, not only the generated prose.
- [1.2] **Table 2's bolded submitted row has never been reproduced.** The printed val 0.4293 /
  test 0.4677 comes from `run_zinc_q2.py`. Six later runs of the same configuration all land
  worse: the worker's own `logs/zinc_cell18.log` (val 0.4318/0.4418/0.4418, test
  0.4715/0.4766/0.4766, and `logs/rerun_checks.log` says "largest difference 0.012413 --
  DIFFERENT, investigate") and my two repeats (val 0.4451/0.4418, test 0.4792/0.4766). The
  caption discloses the three *test* repeats, which keeps the table honest, but the val column --
  the number on which "picked on validation" is said to rest -- is printed as 0.4293 with no
  indication that nothing since has matched it, and it is the single most favourable draw in the
  table. | `OUTPUT/answer.tex`, Table 2, row "2-hop ball + virtual" | severity: minor
  Fix: either print the row from the reproducible set, or add the val repeats to the caption
  alongside the test ones. (The conclusion is unaffected: my reruns put `local+virtual` at 0.4941
  and `local` at 0.5036 test, both clearly behind.)
- [1.3] **"The expander ... alone keeps the pair count $O(n)$ while mixing in $O(\log n)$ hops"**
  is not true as written: `local` and `local+virtual` are also $O(n)$ pairs on bounded-degree
  molecules, and `local+virtual` mixes in 2 hops through the global token, better than
  $O(\log n)$. The expander's actual distinction over a virtual node is that it spreads the
  mixing across many edges instead of one bottleneck token.
  | `OUTPUT/answer.tex`, Q2 opening paragraph | severity: minor
- [1.4] **"Two hops wins again, at 3 of the 3 seeds and by 0.0184 on the mean"** mixes two
  metrics in one clause. The "3 of 3" counter is computed against `local+virtual` only
  (`build_answer.py:265-268`); on *test* MAE at seed 2, `local` (0.5073) beats the 2-hop ball
  (0.5098). The claim is true on *validation* MAE -- the selection metric -- against all four
  alternatives at all three seeds. Say which metric.
  | `OUTPUT/answer.tex`, Q2 results paragraph | severity: minor
- [1.5] `\label{p1:tab:q2lastfm}` is defined but never `\ref`'d; the LastFM sentence ("LastFM
  shows the cost instead: ...") should point at Table~\ref{p1:tab:q2lastfm}.
  | `OUTPUT/answer.tex` | severity: minor
- [1.6] **Prose length, R8.** My count with listings, table bodies and captions excluded: Q1 385
  words, Q2 362, total 747 against the brief's ~300 per question. Q1 is 28% over, just past R8's
  quarter threshold; Q2 is 21% over. No padding of the four kinds R8 names -- the overage sits in
  the single sentence carrying four ablation numbers. Trimming ~30 words from Q1 clears it.
  Separately, Table 2's caption is ~145 words, which is a paragraph doing caption duty.
  | `OUTPUT/answer.tex` | severity: minor
- [1.7] **`submission.md` is internally inconsistent** (traceability document, not the graded
  deliverable): claims "26 checks" while `notes.md` says "21/21 checks pass"; claims the LastFM
  top three are "within 0.005 validation micro-F1" when the measured spread is 0.0079
  (`answer.tex` correctly says 0.008).
  | `PLAYGROUND/submission.md`, `PLAYGROUND/notes.md` | severity: minor

### Resolved since last round
(first round)

### Still outstanding
[1.1] through [1.7]. Only [1.1] is substantive; it is a one-line edit plus an assert.

## Round 2
Verdict: PASS

### How I checked, rather than taking the worker's word
- **`solution.py` changed only inside a docstring.** Parsed both revisions with `ast`, stripped
  every docstring, dumped the trees: identical. So round 1's numerical verification carries
  over unchanged. I re-ran both suites against the *delivered* file anyway: the worker's
  `test_solution.py` -> 26/26 (`validators/p1/logs/r2_test_solution.log`) and my own
  independent suite -> 31/31, ALL OK (`validators/p1/logs/r2_val_check.log`).
- **`answer.tex` regenerates byte-identically.** Copied `build_answer.py`, `extract_code.py`,
  `solution.py` and `logs/` into `validators/p1/regen/`, repointed `OUT` at my own directory and
  ran it: the output is byte-for-byte the delivered `answer.tex` and `preamble.txt`. Nothing in
  the fragment was typed by hand, and every assert in the generator passes against the logs.
- **Recompiled** in a minimal wrapper holding exactly `preamble.txt`: 5 pages (was 6),
  0 overfull/underfull boxes, 0 undefined references. Rendered to PNG and read every page.
  `lint_output.py` OK. R5 clean; all three labels and all four style/colour names namespaced.

### Resolved since last round
- **[1.1] (was major) — resolved, and guarded.** The docstring now reads "has the lowest
  validation MAE on ZINC at every seed; on LastFM it is second of five, 0.005 behind the best."
  I checked both halves against the logs myself: the 2-hop ball has the lowest validation MAE of
  the five at seed 0 (0.42935), seed 1 (0.46792) and seed 2 (0.46252), and is below full
  attention at all three; on LastFM it ranks 2 of 5 with a gap of 0.005242 to `local`, which
  prints as 0.005. `build_answer.py:271-277` now asserts the rank word, the gap and the per-seed
  claim against the logs and forbids the string "highest validation micro-F1". I tested the
  guard rather than reading it: reverting the docstring to the round-1 text and rebuilding dies
  with `AssertionError` at line 272.
- **[1.2] — resolved.** Table 2's caption now gives the validation repeats as well as the test
  ones (0.4318/0.4418/0.4418 and 0.4715/0.4766/0.4766), states that every later repeat is worse
  than the printed draw, and says the choice rests on the per-seed ranking rather than the
  decimals. That ranking is in fact stable: even my worst reproduction (val 0.4451) sits well
  below `local+virtual` at 0.4791.
- **[1.3] — resolved.** The false exclusivity ("it alone keeps the pair count O(n)") is gone;
  the expander is now distinguished by hub-free mixing at O(n) pairs, which is correct.
- **[1.4] — resolved.** The claim is now "lowest validation MAE of the five at every seed", with
  the 0.0184 margin stated separately as a test-mean margin to the runner-up. Both verified.
- **[1.5] — resolved**, and `build_answer.py:314` now refuses to emit a label nothing references.
- **[1.6] — resolved.** My recount (listings, table bodies and captions excluded): Q1 359 (was
  385), Q2 372 (was 362), total 731. Both sections are inside R8's quarter threshold. Q2 sits on
  the line, and its growth is the metric precision [1.3] and [1.4] asked for, so I am not asking
  for another trim.
- **[1.7] — resolved.** `notes.md` says 26/26; `submission.md` says 0.008 for the LastFM
  top-three spread and names the 0.005 gap separately.

### Still outstanding
Nothing substantive. Two cosmetic notes, recorded and deliberately not blocked on:
- `answer.tex` calls $D^{1/2}\mathbf{1}$ "the constant eigenvector". It is the trivial/null
  eigenvector of the symmetric Laplacian and is constant only on a regular graph (ZINC degrees
  run 1-4). The code drops the right column -- I verified the returned vectors are orthogonal to
  $D^{1/2}\mathbf{1}$ -- so this is a misplaced adjective, not an error.
- `submission.md` rounds the LapPE-on-SPD gain to 0.0118 where `answer.tex` prints 0.0119; the
  true value is 0.011853, so the deliverable has it right and the scratch document does not.
