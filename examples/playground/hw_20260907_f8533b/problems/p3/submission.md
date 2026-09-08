# p3 — submission

## What the problem asked

Problem 3 (8 points), rendered page 4 of `ingest/pages/Homework_2/`. An L1 instruction
cache: 4-way, 64 B blocks, 256 KB, **1.1 ns access time**, **1% miss rate**, **50 ns
additional miss penalty**. With way prediction: **1 ns access if the prediction succeeds**
(same as direct mapped), **1.1 ns *additional* access time if the prediction fails**,
other conditions unchanged.

- **Question A (2 pts)** — fill in the blank: best-case and worst-case cache access time, in ns.
- **Question B (6 pts)** — with the same miss rate, way prediction must reduce AMAT by at
  least 5%; find the minimum prediction accuracy, showing the calculation process.

**Brief vs. assignment page: no discrepancy.** I checked all three channels (R7):
- Text `page_004.txt` — full problem present, matches the brief verbatim.
- Render `page_004.png` — read directly; confirms the layout and, importantly, the
  **bold+underlined "additional"** on the misprediction bullet, an emphasis the text
  channel silently flattens to plain text. That emphasis is what fixes 1.1 ns as a
  *delta* rather than a replacement.
- Figures — `manifest.json` reports `n_images = 0` and `figures: []` for page 4 (and every
  page of this assignment). Channel 3 is legitimately empty; I verified that rather than
  assuming it. Nothing in this problem depends on an image.

**Extra corroboration found on page 1** (front matter, Problem 1 hint), which I used and
which supports the delta reading independently of the page-4 emphasis:
> "for a cache miss, cache miss penalty (transfer time) is an additional cost on top of
> the hit time (access time). A cache miss happens after first attempting to access it."

That is the assignment's own statement of `AMAT = access + miss_rate x penalty`, which is
exactly the formula I build both AMATs from. Page 1 also requires "clearly indicate which
question an answer is for", so `answer.tex` has an explicit subsection per question.

## What I decided it needed

**plain + code.** No diagram — the problem asks for two numbers and a threshold; there is
nothing to plot and the brief explicitly says no diagram is required. The deliverable is a
derivation (6 of the 8 points are "provide your calculation process"), so `answer.tex` is
prose + algebra. "code" here means I verified the algebra and the threshold numerically
before writing any number down; **no code appears in `answer.tex`**.

## What I did

Read "additional" as a delta in both places, so a failed prediction costs
`1 + 1.1 = 2.1` ns (probe the predicted way, miss, then do the ordinary associative
lookup) and the 50 ns penalty sits on top of the access time rather than replacing it.
Baseline `AMAT = 1.1 + 0.01x50 = 1.6` ns. Because the miss rate and penalty are unchanged
("assuming the same cache miss rate"), the miss term is identical on both sides and only
the access-time term differs, giving `AMAT_wp(a) = [a(1) + (1-a)(2.1)] + 0.5 = 2.6 - 1.1a`.
Imposing `AMAT_wp <= 0.95 x 1.6 = 1.52` and solving gives `a >= 54/55`.

I solved it in exact rationals with sympy (not floats, to avoid drift on a threshold that
sits at a repeating decimal), then cross-checked with an independent brute-force sweep over
`a` on a 1e-6 grid that does not use `sympy.solve` at all. Both agree. I also compiled the
fragment in a wrapper and read the rendered pages (cropped and upscaled 3x) to confirm the
math typesets legibly.

## Intermediate steps and code

Paths relative to PLAYGROUND:

- `notes.md` — channel reconciliation, the reading of "additional", and the plan.
- `verify.py` — **the only script producing results.** Exact sympy solve for the
  threshold, the equality check at `a_min`, the rounding-direction test, and the
  independent numeric sweep. Reproduce everything with `python3 verify.py`.
- `verify_out.txt` — captured output of that run (every number below is in it).
- `build/wrapper.tex`, `build/log2.txt` — compile-test of the fragment as the master will
  use it (`\input{answer.tex}`); clean second pass, no warnings.
- `build/crop1_bottom.png`, `build/crop2_top.png` — upscaled crops I actually read to
  check the typeset math.

## Results

Every computed value in `answer.tex`, all from `python3 verify.py` (`verify_out.txt`):

| Claim in answer.tex | Value | Source |
|---|---|---|
| Best-case access | **1 ns** | given directly |
| Worst-case access | **2.1 ns** = 1 + 1.1 | `verify.py` Question A block |
| Baseline AMAT | **1.6 ns** = 1.1 + 0.01x50 | `AMAT_base = 8/5` |
| Way-predicting AMAT | **2.6 - 1.1a ns** | `AMAT_wp(a) = 13/5 - 11a/10` |
| 5%-reduction target | **1.52 ns** = 0.95 x 1.6 | `target = 38/25` |
| **Minimum accuracy** | **a = 54/55 = 98.1818...% ~ 98.19%** | `a_min (exact) = 54/55` |
| Check at `a_min` | AMAT = **1.52 ns**, exactly a **5.000000000%** reduction | `MATCH` line |
| 98.18% (rounded down) | AMAT = **1.52002 ns** > 1.52 -> **violates** | rounding block, `False` |
| 98.19% (rounded up) | AMAT = **1.51991 ns** <= 1.52 -> satisfies | rounding block, `True` |
| Perfect predictor `a=1` | AMAT = **1.5 ns**, a **6.25%** reduction | 2.6 - 1.1; (1.6-1.5)/1.6 |
| Numeric sweep | smallest grid `a` = **0.981819**, agrees with 54/55 to 1e-6 | sweep block |

The rounding point is a real computed finding, not a stylistic remark: because this is a
lower bound, rounding the threshold *down* to 98.18% genuinely breaks the constraint
(1.52002 > 1.52), so the answer is stated as the exact fraction 54/55 with the decimal
rounded **up** to 98.19%.

## Deliverables

In OUTPUT (`output/hw_20260907_f8533b/p3/`):
- `answer.tex` — LaTeX fragment. Section for Problem 3, `\subsection*` per question.
  No `\documentclass` / `\usepackage` / `document` environment (grep-verified). All 7
  labels namespaced `p3:eq:*` (grep-verified). No figures, so no `\includegraphics`.
- `preamble.txt` — `\usepackage{amsmath}`, `\usepackage{amssymb}`.

`python3 framework/tools/lint_output.py output/hw_20260907_f8533b/p3` -> **OUTPUT LINT OK**
(exit 0). `downloads.md` records `(nothing installed)` — no venv, no pip, no downloads.

## Where I am least confident

1. **The reading of "worst case" in Question A** is the one genuine judgement call, and
   Question B depends on it. I read it as the worst *cache-access* (hit-time) outcome =
   2.1 ns. The alternative reading is worst case over *everything*, i.e. a misprediction
   that also misses: `1 + 1.1 + 50 = 52.1` ns. I rejected it because the blank asks what
   "a cache access takes", the two bullets under "with way-predicting enabled" are exactly
   the two access times, and the assignment's own page-1 hint separates access time from
   miss penalty as additive terms. I stated this reading explicitly in `answer.tex` so a
   grader can see it. **Note this choice does not change Question B**: the AMAT formula
   needs the access-time component, so 2.1 ns is the right input there regardless — if a
   grader wanted 52.1 ns in A, B's 98.19% still stands.
2. **The additive interpretation of the 1.1 ns misprediction penalty** (2.1 ns total, not
   1.1 ns total). If it were instead read as "a failed prediction costs 1.1 ns total",
   way prediction could never beat the 1.1 ns baseline access time and the question would
   be unanswerable — so the additive reading is forced. The bold+underline in the render
   and the page-1 hint both support it. I am confident here, but flagging it since it is
   the single assumption the whole numeric answer rests on.
3. Everything downstream of those two readings is exact rational arithmetic, double-checked
   two independent ways, so I have no numerical concerns about 54/55 itself.
