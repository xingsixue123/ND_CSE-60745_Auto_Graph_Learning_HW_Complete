# p1 — validator checklist

## Round 1
Verdict: PASS

### What I verified independently (not by reading the worker's claims)

**Ground truth / R7 three channels.**
- Text: read `ingest/pages/Homework_2/page_001.txt` and `page_002.txt` in full.
- Render: cropped `page_001.png` / `page_002.png` into halves and upscaled 2x LANCZOS
  (`pg1_top.png`, `pg1_bot.png`, `pg2_top.png`, `pg2_bot.png`) and read all four, rather
  than reading the downscaled whole page.
- Figure channel: did **not** trust `manifest.json`. Re-derived with
  `pymupdf ... get_images(full=True)` over all 9 pages -> 0 images on every page.
  Pages 1/2 contain only 13 and 10 vector `drawings` (the gray section-header bars and
  the blank answer rules), and the renders confirm those carry no information.
  The worker's "figure channel is genuinely empty" claim is correct.
- Result: `problem.md`'s transcription of the setup and of Questions A-D is verbatim
  faithful to the assignment page. **No brief-vs-page discrepancy.**

**Question A.** (1) False, (2) True, (3) False. All three are the standard answers;
each carries one clause of justification, correctly weighted for 3 points.

**Question B.** Recomputed from scratch: L2 = 512 KB = 2^19 B; 2^19/2^7 = 4096 blocks;
4096/4 ways = 1024 = 2^10 sets. offset 7, index 10, tag 64-10-7 = 47, sum 64. Matches.
The answer explicitly disposes of the "each data word is 64-bit" distractor by appealing
to "Entries are Byte addressable" — the grader planted that sentence and the worker
addressed it rather than ignoring it.

**Question C.** Re-derived symbolically with sympy, independently of `verify.py`:
AMAT(16 B bus) = M/250 + 139/50; solving = 4 gives M = 305 CC = 152.5 ns. Cross-checked
a third way with the fully expanded closed form: M=305 -> AMAT exactly 4; M=306 -> 4.004
(> 4), so the bound is real and tight. Matches the answer.

**Question D.** Independently 1 + 0.05(10 + 0.4(50 + 0.2(305+30))) = 96/25 = 3.84 CC.
Matches. Answer is given in **CCs** as the blank demands (this is what the question's
hint warns about) with the ns equivalent as a parenthetical.

**Robustness finding that retires the worker's own stated doubt #2.** I tested the
alternative "no first-transfer credit" convention (8 additional transfers). It gives
M_max = 295 CC and P_L3 = 295 + 40 = 335 CC — *identical* P_L3 to the worker's
305 + 30 = 335. So **Question D's 3.84 CC is invariant to that convention**; only
Question C's 152.5 ns vs 147.5 ns pivots on it. And the statement's wording ("the
initial time required to access memory, which accounts for a single transfer ... plus
10 CCs for every additional transfer") unambiguously supports the worker's 7-additional
reading. Convention is correct and is stated explicitly in the answer.

**Code requirement (needs = plain + code).** Copied `verify.py` to my own dir and ran it.
It executes, and reproduces every number in the results table. It is genuinely
self-checking, not self-reporting: asserts tag+index+offset == 64, asserts the C bound by
back-substitution (`amat(305,16) == 4`), asserts tightness (`amat(306,16) > 4`), and
asserts power-of-two before each log. Exact `Fraction` arithmetic, no floats. No
fabricated numbers: every value in `answer.tex` traces to script output or to my own
independent recomputation.

**LaTeX / R5.** Compiled the fragment in a minimal wrapper: 3 pages, exit 0, second
pdflatex pass **zero warnings**, no undefined references, no overfull boxes reported.
No `\documentclass`, `\usepackage`, or `document` environment (checked with the Grep
tool after my first bash grep produced an unreliable escaping result). Both labels
namespaced — `p1:eq:amat`, `p1:eq:pl3` — and all five `\eqref`s resolve. No custom
macros, no `\includegraphics`, no absolute paths. Rendered all 3 pages to PNG and read
them, plus a 3x upscale of the Question A block: layout is clean, the booktabs table is
correct, both boxed results are legible, nothing clipped or overlapping.

**OUTPUT clean / R4.** `python3 framework/tools/lint_output.py output/hw_20260907_f8533b/p1`
-> `OUTPUT LINT OK`, exit 0. Contains only `answer.tex` and `preamble.txt`. All scratch
(crops, wrapper, `.aux`/`.log`, page renders) correctly confined to the playground.

**R3 downloads.** `downloads.md` present and correctly records `- (nothing installed)`
with a note on which preinstalled tools were used. Consistent with what I observed.

### Defects
None blocking, none major.

- [1.1] `\usepackage{amssymb}` in `preamble.txt` is unused | `OUTPUT/p1/preamble.txt` |
  severity: minor. Verified by recompiling with only amsmath + booktabs — exit 0. Harmless
  (the master de-duplicates preambles and amssymb is universally available); not worth a
  round trip.
- [1.2] In Question D the unit sits outside the box (`\boxed{3.84}` CCs) whereas Question C
  boxes the unit with the value | `answer.tex:134` | severity: minor. Cosmetic
  inconsistency only; the unit is unambiguous in the surrounding sentence.

### Resolved since last round
N/A — first round.

### Still outstanding
Nothing substantive. The two items above are cosmetic and I am not holding the
submission for them.
