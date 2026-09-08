# Problem id: `p3`

**Course:** CSE 60321 -- Advanced Computer Architecture -- Spring 2026
**Assignment:** Homework 2
**This problem:** Problem 3, 8 points (Questions A, B)
**Location in the assignment:** rendered page **4** of
`playground/hw_20260907_f8533b/ingest/pages/Homework_2/` (`page_004.png`, `page_004.txt`).
The whole problem fits on that one page.
**Anchor text:** `Problem 3: (8 points)` / "We are trying to deploy the way-prediction
technique on an L1 instruction cache."

**Figures:** none. The ingest manifest reports `n_images = 0` for every page of this
assignment, and the render of page 4 confirms it — this problem is entirely prose and
bullet lists. Nothing here depends on an image.

**Namespacing (mandatory):** every LaTeX label, every figure filename and every macro
you define must carry the `p3` prefix — `\label{p3:eq:amat}`, `fig_p3_*.pdf`.
Unnamespaced labels collide with the other problems and break the master document's compile.

---

## Shared setup (transcribed verbatim — applies to both questions)

> We are trying to deploy the way-prediction technique on an L1 instruction cache. The
> configurations of this cache are:
>
> - 4-way set associative.
> - 64 Bytes block size.
> - 256 KB cache size.
> - 1.1 ns cache access time.
> - 1% cache miss rate.
> - 50 ns additional cache miss penalty if missing.
>
> With way-predicting enabled, this cache has:
>
> - 1 ns cache access time if prediction succeeds, which is the same as a direct mapped
>   cache.
> - 1.1 ns **additional** cache access time if prediction fails.
> - Other conditions remain the same.

Two notes on reading this setup, both verified against the page render:

- The word **additional** is bold-and-underlined in the original on the "1.1 ns
  additional cache access time if prediction fails" bullet. The emphasis is the
  assignment telling you it is a *delta*, not a replacement: a failed prediction costs
  the successful-prediction time **plus** 1.1 ns, because the way-predicting cache
  probes the predicted way first and only then falls back to the normal associative
  lookup.
- Likewise "50 ns **additional** cache miss penalty" is a cost on top of the access
  time, not a total. Note also that the 4-way, 64-Byte-block, 256 KB geometry is not
  needed numerically by either question — it is there to justify the 1.1 ns baseline
  and the direct-mapped comparison. Do not manufacture a set-count calculation nobody
  asked for.

---

## Question A (2 points) — transcribed verbatim

> **Fill in the blank:**
>
> For this way-predicting enabled cache, for the best case, a cache access takes
> _______ ns; for the worst case, it takes _______ ns.

**Deliverable:** two numbers, in ns.

The question asks what a **cache access** takes, and the two bullets under "With
way-predicting enabled" are precisely the two cache-access times in play (prediction
succeeds vs. prediction fails). Answer on those terms and say in one clause how you read
"worst case", so the reading is on the record for the grader. Keep it to a line or two —
it is a 2-point fill-in, and whatever you settle on here is the pair of access times
Question B's AMAT expression must be built from, so the two answers have to agree.

## Question B (6 points) — transcribed verbatim

> Assuming the same cache miss rate with way-predicting. The way-predicting cache
> reduces the AMAT by at least 5%. **What is the minimum prediction accuracy?** Please
> provide your calculation process.

**Deliverable:** the minimum prediction accuracy (give it as a percentage) with the full
calculation process — the question asks for the process explicitly, and this is 6 of the
problem's 8 points, so the derivation carries most of the credit.

The shape of the work: compute the baseline AMAT of the original cache (1.1 ns access,
1% miss rate, 50 ns additional miss penalty); write the way-predicting AMAT as a function
of the prediction accuracy `a`, using the best-case and worst-case access times from
Question A weighted by `a` and `1 - a`; then impose that it be at most 95% of the
baseline and solve for `a`.

Points to be careful about: "Assuming the same cache miss rate" means the 1% and the
50 ns penalty term are unchanged between the two configurations, so only the access-time
part differs. "Reduces the AMAT by **at least** 5%" is an inequality — the answer is the
threshold value of `a`, and you should state the direction (accuracy must be *at least*
that). Keep enough decimal places to be meaningful and say how you rounded; note that
rounding a threshold *down* would violate the constraint, so round up.

---

## What to produce

- `OUTPUT/p3/answer.tex` — a LaTeX **fragment**: no `\documentclass`, no
  `\begin{document}`, no `\usepackage`. It starts at the section level. Extra packages
  go one per line in `OUTPUT/p3/preamble.txt` as literal `\usepackage{...}` lines.
- Structure it as a section for Problem 3 with a clearly labelled subsection per
  question (A, B) — the assignment's front matter requires it: *"Please clearly indicate
  which question an answer is for in your submission."*
- **`needs`: plain + code.** "code" means verify the algebra and the final threshold
  numerically in your playground before writing it down. **Do not put code in
  `answer.tex`.** This is a homework submission, not a lab notebook: show the
  derivation a grader needs to award the 6 points, and nothing else — no listings, no
  console output, no exploration.
- No diagram is required for this problem.
