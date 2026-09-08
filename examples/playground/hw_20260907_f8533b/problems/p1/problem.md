# Problem id: `p1`

**Course:** CSE 60321 -- Advanced Computer Architecture -- Spring 2026
**Assignment:** Homework 2
**This problem:** Problem 1, 21 points (Questions A, B, C, D)
**Location in the assignment:** rendered pages **1 and 2** of
`playground/hw_20260907_f8533b/ingest/pages/Homework_2/` (`page_001.png`,
`page_002.png`, and the matching `.txt`). The problem header and Question A are at
the bottom of rendered page 1; Questions B, C and D are on rendered page 2.
**Anchor text:** `Problem 1: (21 points)` / "One possible organization of the memory
hierarchy on an Intel Xeon chip is:"

**Figures:** none. The ingest manifest reports `n_images = 0` for every page of this
assignment and the page renders confirm it — the only graphics are ruled tables and
the black/gray section-header bars. Nothing in this problem depends on an image. (Note
that the Read tool downscales `page_001.png`; if you want to check the setup bullets
against the render, crop the region and upscale it rather than reading the whole page.)

**Namespacing (mandatory):** every LaTeX label, every figure filename and every macro
you define must carry the `p1` prefix — `\label{p1:eq:amat}`, `fig_p1_*.pdf`. Unnamespaced
labels collide with the other problems and break the master document's compile.

---

## Assignment-wide unit convention (stated on rendered page 1, applies here)

> Unit clarification: for all problems in this homework,
> 1TB = 2^10 GB, 1GB = 2^10 MB, 1MB = 2^10 KB, 1KB = 2^10 Bytes, 1 Byte = 8 bits;
> 1 ns = 10^-9 s, 1 ms = 10^-3 s; 1 GHz = 10^9 Hz, 1 Hz = 1 s^-1.

---

## Shared setup (transcribed verbatim — applies to all four questions)

> One possible organization of the memory hierarchy on an Intel Xeon chip is:
>
> - A 64KB L1 instruction cache.
>   - The L1 instruction cache contains only instruction encodings.
> - A 64KB L1 data cache.
>   - The L1 data cache contains only data words.
> - A 512KB unified L2 cache.
>   - The L2 cache can contain both data and instruction encodings.
> - An 8 MB unified L3 cache.
>   - The L3 cache can contain both data and instruction encodings.
>
> Suppose this chip has the clock frequency at 2.0 GHz, and for its cache system,
> assume that:
>
> - All caches use the block size of 128 Bytes.
> - The hit time for either L1 cache is 1 clock cycle (CC); the hit time for L2 cache
>   is 10 CCs.
> - The time required to find data (i.e., hit time) in the L3 cache is 50 CCs.
> - If data is not found in the L3 cache, the processor must look for data in main
>   memory.
>   - The processor-to-memory bus can accommodate 16 Bytes of memory at a time.
>   - The L3 miss penalty is the initial time required to access memory, which
>     accounts for a single transfer (equal to the bus bandwidth, in this case 16
>     Bytes), plus 10 CCs for every additional transfer (also 16 Bytes here).
>
> Hint: for a cache miss, cache miss penalty (transfer time) is an additional cost on
> top of the hit time (access time). A cache miss happens after first attempting to
> access it.

**Read that last hint carefully — it fixes the AMAT convention this problem wants.**
It says the penalty is charged *on top of* the hit time, i.e. the hierarchy is modelled as

    AMAT = HitTime_L1 + MissRate_L1 x Penalty_L1
    Penalty_L1 = HitTime_L2 + MissRate_L2 x Penalty_L2
    Penalty_L2 = HitTime_L3 + MissRate_L3 x Penalty_L3
    Penalty_L3 = (main memory access)

and *not* a model in which a lower level's hit time replaces the level above it. State
the convention you use explicitly before you use it; a grader awarding the 10 points for
Question C is marking the derivation, not just the final number.

Also note the wording of the bus model: the "initial time required to access memory"
**already covers the first 16-Byte transfer**, and only the *additional* transfers cost
10 CCs each. So for a 128-Byte block over a 16-Byte bus there are 128/16 = 8 transfers,
of which 7 are additional. Do not double-count the first transfer.

---

## Question A (3 points) — transcribed verbatim

> Write "True" for correct statements, and "False" for wrong statements.
>
> _______ (1) This chip will be faster if we remove L2 and L3 caches and keep L1 cache
> the same.
>
> _______ (2) Typically, building a certain amount of L1 cache into the chip is more
> expensive than building the same amount of L3 cache.
>
> _______ (3) To execute a program correctly on this chip, all instructions of this
> program must be loaded into L1 instruction cache prior to execution.

**Deliverable:** True/False for each of (1), (2), (3), each with a one-sentence
justification. The question only demands the verdict, but a bare "False" three times is
weak homework; one short clause of reasoning per item is the right weight for 3 points.
Do not pad these into paragraphs.

## Question B (6 points) — transcribed verbatim

> Consider the L2 cache. It is 4-way set associative. Physical addresses are 64 bits
> long. Each data word is 64-bit. Entries are Byte addressable. **How many bits of a
> 64-bit physical address comprise the tag, index and offset?** Please provide your
> calculation process.

**Deliverable:** the three bit-counts *and* the calculation process (the question asks
for it explicitly — 6 points is mostly for the derivation). Show the number of sets you
get and how. Note "Entries are Byte addressable": the block offset must address individual
bytes within the block, so the "each data word is 64-bit" sentence does **not** shrink the
offset — say so in one clause rather than silently ignoring it, since a grader put it there
on purpose. Sanity-check that your three counts sum to 64.

## Question C (10 points) — transcribed verbatim

> Assuming the local miss rates of 5%, 40%, and 20% for the L1, L2, and L3 caches,
> respectively. **To have an average memory access time of no higher than 4 CCs,
> determine the maximum initial main memory access time (in nanosecond).** Please
> provide your calculation process.
>
> Hint: to simplify calculation, you may use CCs for time and convert to nanoseconds
> at the last step.

**Deliverable:** the maximum initial main memory access time **in nanoseconds**, with the
full derivation. This is the heaviest question in the problem (10 of 21 points), so lay the
algebra out step by step from the AMAT expression down to the bound.

Watch three things: (a) the quantity being solved for is the *initial* memory access time,
which is only one component of the L3 miss penalty — the additional-transfer cost has to be
subtracted off; (b) the rates given are *local* miss rates, which is exactly what the nested
AMAT expression above consumes, so no conversion to global rates is needed; (c) the final
conversion uses the 2.0 GHz clock, so 1 CC = 0.5 ns.

## Question D (2 points) — transcribed verbatim

> Assuming the same local miss rates in Question C. **Fill in the blank:**
>
> If the bus bandwidth increases to 32 Bytes, the average memory access time will be
> _______ CCs.
>
> Hint: be careful about the unit of time this question asks for.

**Deliverable:** a single number, the AMAT, **in CCs** (the blank's unit is printed as CCs
— that is what the hint is warning about, since Question C just made you convert to ns).
Show the one or two lines of arithmetic that produce it.

This question continues Question C: "the same local miss rates" means 5%/40%/20%, and the
initial main memory access time to use is the maximum value you determined in Question C
(that is the only value of it in play). Only the bus width changes, which changes the number
of transfers for the same 128-Byte block and therefore the additional-transfer cost. State
which initial memory access time you are carrying forward so the grader can follow.

---

## What to produce

- `OUTPUT/p1/answer.tex` — a LaTeX **fragment**: no `\documentclass`, no
  `\begin{document}`, no `\usepackage`. It starts at the section level. Extra packages
  go one per line in `OUTPUT/p1/preamble.txt` as literal `\usepackage{...}` lines.
- Structure it as a section for Problem 1 with a clearly labelled subsection per
  question (A, B, C, D), so a grader can match answers to questions — the assignment's
  own front matter demands this: *"Please clearly indicate which question an answer is
  for in your submission."*
- **`needs`: plain + code.** "code" here means you should verify your arithmetic with
  python in your playground before you write it down — the Question C bound and the
  Question D AMAT are easy to slip a factor on. **Do not put code in `answer.tex`.**
  This is a homework submission, not a lab notebook: show the mathematical derivation a
  grader needs to award the marks, and nothing else. No code listings, no
  console output, no record of your exploration.
- No diagram is required for this problem. A small table is a reasonable way to present
  the Question A True/False verdicts or the Question B bit split, but it is optional.
