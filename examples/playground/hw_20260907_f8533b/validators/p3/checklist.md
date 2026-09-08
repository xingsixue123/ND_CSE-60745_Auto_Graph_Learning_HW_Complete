# p3 — worker validator checklist

## Round 1
Verdict: PASS

### What I checked (independently, not by trusting the submission)

**1. Question fidelity (R7, all three channels).**
- Text `ingest/pages/Homework_2/page_004.txt` — read in full. Matches the brief's
  transcription verbatim: 4-way, 64 B block, 256 KB, 1.1 ns access, 1% miss rate, 50 ns
  additional miss penalty; way-predicting 1 ns on success, 1.1 ns additional on failure.
  Question A = fill in best/worst case cache access; Question B = min prediction accuracy
  for >=5% AMAT reduction, with process.
- Render `page_004.png` — read directly. Confirms the bold+underlined **additional** on
  the misprediction bullet, which the text channel flattens. Confirms there is nothing
  else on the page (no hidden sub-part, no figure).
- Figures — `manifest.json` checked myself: `n_images: 0`, `figures: []` for page 4 (and
  every page, all 9). Channel 3 legitimately empty. The worker's claim is true.
- Cross-check on page 1: the Problem 1 hint the worker cites is real and verbatim —
  "for a cache miss, cache miss penalty (transfer time) is an additional cost on top of
  the hit time (access time)". It does support the additive AMAT model. Page 1 also
  requires "clearly indicate which question an answer is for"; `answer.tex` has an
  explicit `\subsection*` per question. No brief/page discrepancy.

**2. Numbers — re-run and independently recomputed.**
- Copied `verify.py` into `validators/p3/rerun/` and ran it. Output is byte-identical to
  the worker's `verify_out.txt` (`diff` clean). Not a stale capture.
- Recomputed from scratch in `fractions.Fraction`, not reusing the worker's model or
  sympy: baseline AMAT = 11/10 + (1/100)(50) = 8/5 = 1.6 ns; the 5% target = 38/25 =
  1.52 ns; threshold a = (2.6 - 1.52)/1.1 = 54/55 = 0.98181818... Agrees.
- Independent exact-rational brute-force over a 1e-6 grid: smallest qualifying
  a = 981819/1000000 = 0.981819, consistent with 54/55 to 1e-6.
- Rounding claim verified: a=0.9818 -> AMAT 1.52002 ns (violates); a=0.9819 -> 1.51991 ns
  (satisfies). So rounding *up* to 98.19% is correct, and the answer says so.
- Perfect-predictor remark verified: a=1 -> 1.5 ns, (1.6-1.5)/1.6 = 6.25% reduction.
  This is a real ceiling and it is why the required accuracy is so high — the answer is
  tight but not wrong.
- Every number appearing in `answer.tex` (1, 2.1, 1.6, 1.52, 2.6-1.1a, 54/55, 98.19%,
  1.52002, 1.51991, 1.5, 6.25%) traces to a computed line. Nothing fabricated.

**3. Did it do the required kind of work?** `needs: plain + code`, no diagram. The
derivation is present and complete (4 steps + a check), the numerics were actually run,
and no code or console output leaked into `answer.tex`. Correct: no figure is required —
the problem asks for two numbers and a threshold, there is nothing to plot.

**4. LaTeX compliance and compile.** Copied `answer.tex` into my own `build/` and
compiled it inside a minimal wrapper (`\input{answer.tex}`, article + amsmath + amssymb +
geometry). Two clean passes, exit 0, no warnings, no undefined references, no overfull
boxes reported. `grep`: no `\documentclass`, no `\usepackage`, no `document` environment,
no `\newcommand`, no `\includegraphics`, no absolute paths (R5 satisfied). All 7 labels
namespaced: `p3:eq:{amat,cases,base,wp,target,solve,amin}` — no collision risk.

**5. Typeset output is legible.** Rendered the wrapper PDF to PNG at 130 dpi and again at
260 dpi with a 1.6x upscaled crop of Steps 2-3, and read them. The align blocks, the
fraction chain 1.08/1.1 = 108/110 = 54/55, and the repeating-decimal overlines all set
correctly. Nothing clipped or overlapping.

**6. Hygiene.** `python3 framework/tools/lint_output.py output/.../p3` -> `OUTPUT LINT OK`,
exit 0. OUTPUT contains exactly `answer.tex` and `preamble.txt` (R4). `downloads.md`
exists and records `(nothing installed)`; I confirmed there is no venv, no `site-packages`
and no downloaded artifact anywhere in the worker playground, so the record is accurate (R3).

### Defects
None blocking or major.

- [1.1] `notes.md` lines 47-48 contain a leaked tool-call artifact (`</content>`,
  `</invoke>`) appended after the plan. | `problems/p3/notes.md:47-48` | severity: minor.
  Playground-only, so no R4 violation and no effect on the deliverable; noted for tidiness.
- [1.2] `preamble.txt` requests `amssymb`, but nothing in `answer.tex` needs it (`\le`,
  `\times`, `\approx`, `\overline` are all base/amsmath). | `OUTPUT/preamble.txt:2` |
  severity: minor. Harmless — the master de-duplicates preambles and the package is
  installed on this machine.

### Judgement calls I examined and accepted
- **"Worst case" = 2.1 ns rather than 52.1 ns (misprediction that also misses).** I
  considered rejecting this. I accept it: the blank asks what "a cache access takes", the
  two bullets under "with way-predicting enabled" are exactly the two access times, the
  assignment's own page-1 hint separates access time from miss penalty as additive terms,
  and Question A's two values are precisely the inputs Question B's access-time term
  needs — A is the setup for B. The worker states the reading explicitly in `answer.tex`
  so a grader can see it, and flags the alternative in `submission.md`. Defensible and on
  the record; not a defect.
- **1.1 ns misprediction cost is a delta (2.1 ns total), not a replacement.** Forced: as a
  replacement it would never beat the 1.1 ns baseline and Question B would be
  unanswerable. Independently supported by the bold+underline in the render and the page-1
  hint. Confirmed.
- **Miss term identical on both sides.** Matches "assuming the same cache miss rate" and
  the standard AMAT formula. A pedantic model (way prediction always fails on a miss)
  is not what this question is asking for.

### Resolved since last round
n/a — first round.

### Still outstanding
[1.1] and [1.2], both minor and both non-blocking. Not worth another round.
