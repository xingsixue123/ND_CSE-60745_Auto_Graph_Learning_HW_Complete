# Problem id: `p4`

**Course:** CSE 60321 -- Advanced Computer Architecture -- Spring 2026
**Assignment:** Homework 2
**This problem:** Problem 4, 16 points (Questions A, B, C)
**Location in the assignment:** rendered page **5** of
`playground/hw_20260907_f8533b/ingest/pages/Homework_2/` (`page_005.png`, `page_005.txt`).
The whole problem fits on that one page.
**Anchor text:** `Problem 4: (16 points)` / "Consider applying critical-word first and
early restart techniques to reduce miss penalty in a system with L1 and L2 caches."

**Figures:** none. The ingest manifest reports `n_images = 0` for every page of this
assignment. This problem is entirely prose. Note that the Read tool downscales
`page_005.png` badly — the numeric constants in Questions A and B have already been
verified for you by cropping and 2x-upscaling that page, and the transcriptions below
are the reconciled result. If you want to re-check them, crop and upscale rather than
reading the whole page.

**Namespacing (mandatory):** every LaTeX label, every figure filename and every macro
you define must carry the `p4` prefix — `\label{p4:eq:er}`, `fig_p4_*.pdf`.
Unnamespaced labels collide with the other problems and break the master document's compile.

---

## Shared setup (transcribed verbatim — applies to all three questions)

> Consider applying critical-word first and early restart techniques to reduce miss
> penalty in a system with L1 and L2 caches. Originally, in a cache miss scenario, the
> processor continues only when the entire block with the critical word is loaded into
> the cache.
>
> In this problem, a word is 8 Bytes wide.

That first sentence defines the **baseline** ("originally") that both Question A's case
(1) and Question B's "original case" refer to: the processor waits for the *whole block*.
The three schemes the problem contrasts are:

- **neither** — wait for the entire block to arrive;
- **early restart only** — words arrive in normal order, but the processor resumes as
  soon as the *requested* word has arrived;
- **both (critical-word first + early restart)** — memory sends the requested word
  first, so the processor resumes after that one transfer.

`a word is 8 Bytes wide` is what converts each block size into a word count.

---

## Question A (8 points) — transcribed verbatim

> First, we have an L2 cache with 1MB capacity and 64-Byte block size. With
> critical-word first, it takes 110 CCs to get the first word from memory. Otherwise,
> the time to receive the first word from memory is 90 CCs, and each additional word
> from the main memory requires 10 CCs. Further assume that the probability of
> referencing the first word in a block of L2 cache is 30% while the rest ones are
> referenced with equal probability.
>
> **How many CCs would it take on average to service an L2 cache miss for 1) with
> neither critical-word first nor early restart, 2) with early restart only, and 3)
> with both critical-word first and early restart?** Please provide your calculation
> process.

**Deliverable:** three average times in CCs — one per scheme — with the calculation
process (asked for explicitly; at 8 points this is the largest question in the problem
and the derivation carries the credit).

Things to get right:

- Work out the number of words per block first, from the 64-Byte block and the 8-Byte
  word. The 1MB capacity is not needed numerically.
- The reference-probability distribution is **not** uniform: the first word has
  probability 30%, and the remaining words share the other 70% equally. Compute that
  per-word probability explicitly rather than assuming 1/n.
- Note the two different first-word latencies. Critical-word first costs **110** CCs to
  deliver the requested word; without it, the first word of the block arrives at **90**
  CCs and each further word costs 10 CCs. Critical-word first is *slower per transfer*
  here — that asymmetry is the point of the question, not a typo.
- For case (1) the processor waits for the whole block, so the answer does not depend on
  which word was requested — the distribution is irrelevant and the "average" is just
  that fixed time. Say so in a clause; it is the kind of observation a grader is looking
  for.
- For case (2) the wait depends on the position of the requested word, so this is a
  genuine expectation over the distribution. Show the weighted sum.
- For case (3), think about what the block-position distribution does to the answer once
  the critical word is always delivered first.

## Question B (4 points) — transcribed verbatim

> For this question, ignore Question A. The following paragraph is a brief analysis
> regarding L1 cache. **Fill in the blank with the most appropriate integers:**
>
> Next, we have an L1 cache with 32 KB capacity and 32-Byte block size. To simplify the
> question, we only use the average L2 cache access time, i.e., we ignore how different
> situations of L2 cache access may affect L1 cache access. With critical-word first, it
> takes 27 CCs to get the first word from L2 cache. Otherwise, the time to receive the
> first word from L2 cache is **_______** CCs, and each additional word from the main
> memory requires 4 CCs. Further assume that the probability of referencing every word
> in a block of L1 cache is the same. Then, applying both critical-word first and early
> restart can reduce **_______%** of average time for the original case without either
> critical-word first or early restart to service an L1 cache miss; applying only early
> restart can reduce 20% of average time for the original case to service an L1 cache
> miss.

**Deliverable:** the two blanks, both integers. Show the working — 4 points for two
numbers means the method is being marked.

Read the structure of this one carefully, because it runs *backwards* compared to
Question A. The paragraph hands you a known result — "applying only early restart can
reduce **20%**" — and that known 20% is what pins down the first blank. So: express both
the original (whole-block) time and the early-restart-only average as functions of the
unknown first-word latency, set the reduction between them equal to 20%, and solve. Then
use the value you recover to compute the second blank from the critical-word-first time
of 27 CCs.

Note the differences from Question A: this is L1, the block is 32 Bytes (so recompute the
word count), the per-additional-word cost is 4 CCs, and here the reference probability
**is** uniform across the words of the block. "Ignore Question A" means do not carry any
of A's numbers over — but the *definitions* of the three schemes from the shared setup
still apply. Both blanks should come out as clean integers; if they do not, re-check the
setup rather than rounding.

## Question C (4 points) — transcribed verbatim

> **Would critical-word first and early restart be more important for L1 or L2 cache?
> Why? What factors would contribute to their relative importance?** You may refer to
> your observations while solving Questions A and B.
>
> Hint: the solution is not fixed as long as it makes sense, but there must be at least
> one reason, and your answer and reason(s) must be consistent.

**Deliverable:** a clear verdict (L1 or L2 — commit to one), at least one reason, and a
short discussion of the factors that drive the relative importance.

**This question is why A, B and C are one worker.** Read the hint literally: the grader is
marking internal consistency, not a fixed answer. You have just computed, in Question A,
the percentage saving these techniques buy at L2, and in Question B, the percentage saving
they buy at L1. Put those two numbers side by side and let the verdict follow from them —
an answer grounded in your own computed percentages is worth far more than a recital of
textbook generalities, and it is exactly what "you may refer to your observations while
solving Questions A and B" is inviting. Compute the L2 percentage saving explicitly if you
did not already; Question B hands you the L1 one directly.

For the "what factors" part, name the structural quantities that make the saving large or
small — things like the number of words per block, how the fixed first-word latency
compares to the per-word transfer cost, the penalty the critical-word-first mechanism
itself adds, and how the reference distribution is shaped. Whatever you argue, the verdict
and the numbers must not contradict each other; that is the one thing the hint says will
be checked.

---

## What to produce

- `OUTPUT/p4/answer.tex` — a LaTeX **fragment**: no `\documentclass`, no
  `\begin{document}`, no `\usepackage`. It starts at the section level. Extra packages
  go one per line in `OUTPUT/p4/preamble.txt` as literal `\usepackage{...}` lines.
- Structure it as a section for Problem 4 with a clearly labelled subsection per
  question (A, B, C) — the assignment's front matter requires it: *"Please clearly
  indicate which question an answer is for in your submission."*
- A small table summarising the three schemes in Question A is a good way to present
  those results, and it makes the Question C comparison easy to point at. Optional.
- **`needs`: plain + code.** "code" means verify the expectation arithmetic and the
  Question B back-solve numerically in your playground before writing them down — the
  weighted sum in A(2) and the inverse solve in B are both easy to slip. **Do not put
  code in `answer.tex`.** This is a homework submission, not a lab notebook: show the
  derivation a grader needs and nothing else.
- No diagram is required for this problem.
