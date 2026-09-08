# p3 — notes

## Channel reconciliation (R7)
- **Text** `ingest/pages/Homework_2/page_004.txt`: full problem text present, matches brief verbatim.
- **Page render** `page_004.png`: read directly. Confirms layout AND the emphasis that
  text extraction drops — "1.1 ns **additional** cache access time if prediction fails"
  has *additional* in bold+underline. Text channel renders it as plain "additional".
- **Figures**: manifest.json reports `n_images = 0` and `figures: []` for page 4 (and for
  every page of this assignment). Channel 3 is legitimately empty — verified, not assumed.
  Nothing in this problem depends on an image.
- Brief and page **agree**; no discrepancy to report.

## Extra evidence found on page 1 (front matter)
The Problem 1 hint states the assignment's own convention explicitly:
> "for a cache miss, cache miss penalty (transfer time) is an additional cost on top of
> the hit time (access time). A cache miss happens after first attempting to access it."

This independently confirms AMAT = access_time + miss_rate x miss_penalty (penalty is a
delta, not a total), which is exactly how I build both AMATs. Also fixes the same "delta"
reading for the way-prediction 1.1 ns.

Front matter also requires: "Please clearly indicate which question an answer is for."
=> answer.tex needs an explicit subsection per question.

## What this needs
**plain + code.** A derivation is the deliverable (6 of 8 points are "provide your
calculation process"). "code" = verify the algebra/threshold numerically before writing
it down. No diagram (nothing to plot; the problem asks for two numbers and a threshold).

## The reading
Best case = prediction succeeds = 1 ns.
Worst case = prediction fails = 1 + 1.1 = 2.1 ns (because "additional" is a delta:
probe predicted way, miss the prediction, then do the normal associative lookup).
"Cache access" here = access/hit time, NOT including the 50 ns miss penalty, which the
assignment treats as a separate additive term. Will state this reading explicitly so the
grader sees it, and note the alternative in one clause.

Note the 4-way / 64 B / 256 KB geometry is unused numerically — it justifies the 1.1 ns
baseline and the direct-mapped comparison. Do not manufacture a set-count calculation.

## Plan
1. Baseline AMAT = 1.1 + 0.01*50.
2. AMAT_wp(a) = [a*1 + (1-a)*2.1] + 0.01*50  (miss rate & penalty unchanged).
3. Impose AMAT_wp <= 0.95 * AMAT_base, solve for a. Round the threshold UP.
4. Verify exactly with sympy (rational arithmetic, no float drift) + a numeric sweep.
5. Write answer.tex fragment, namespaced p3. Run lint_output.py.
</content>
</invoke>
