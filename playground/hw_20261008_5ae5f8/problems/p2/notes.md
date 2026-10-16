# p2 — Ex. 3.2 (10 pts) — working notes

## Source verification (R7)

The source for this problem is `input/os_hw_3_problems.md`, a **plain markdown text
file**, not a PDF. R7's three channels therefore collapse to one:

  1. text  — `ingest/pages/os_hw_3_problems/alltext.txt`
  2. page image — DOES NOT EXIST (manifest: `kind: text_document`, no `pages` array,
     no `png`). Nothing was rendered because there is nothing to render.
  3. figure files — DO NOT EXIST, for the same reason.

The only PDF in the ingest bundle is `pdf/PaperList.pdf` (from `PaperList.xlsx`),
which belongs to Ex. 3.9, not to this problem. Every one of its 6 pages reports
`n_images: 0` and `figures: []`.

Instead of a cross-channel reconciliation I did a stronger check: byte-level diff of
the ingest text against the original input file.

    diff ingest/pages/os_hw_3_problems/alltext.txt input/os_hw_3_problems.md
    -> identical, no output

And the brief's "transcribed verbatim" block was compared against line 5 of the input
(`grep -n "Ex. 3.2" ... | cat -A`). It matches word for word. **No discrepancy
between brief and source.** This question refers to no figure, consistent with the
brief.

## What the problem needs

`plain`. It is a yes/no question with a required justification. No figure is asked
for ("why or why not", not "show"/"draw"/"plot"), and the brief says `needs: plain`.

One deviation from pure prose: I want two concrete magnitudes in the answer (the
physical footprint of a terabyte of SRAM-class cells, and the speed-of-light floor on
crossing it). Rule: *do not state a number you did not compute.* So those go through
a script — `calc_size_latency.py` — even though the problem does not demand code.
They are supporting figures inside a plain answer, not the deliverable.

## Plan for the argument

Verdict first: **no**, it would not eliminate the hierarchy.

Three arguments, chosen because each independently carries the conclusion. (R8: three,
not six. Rejected candidates listed at the bottom.)

A. **Capacity itself buys latency, independent of material.** Access time has a floor
   set by how far a signal must travel: address in across the decoder, data back out.
   A square array's linear dimension goes as sqrt(capacity), so latency grows with
   size even when every cell is identical and instantaneous. Also word/bit lines get
   longer -> RC delay grows super-linearly in length, and sense amps resolve more
   slowly against larger bit-line capacitance. So "a terabyte of the fastest material"
   is strictly slower than "a kilobyte of the fastest material". The premise of the
   question -- that material choice alone sets speed -- is what fails.

B. **This is already observable, inside one technology.** L1, L2 and L3 on a modern
   CPU are all SRAM: same material, same process, same die. Their latencies still
   span roughly 4 / 14 / 40+ cycles. Nothing but size differs. So the hierarchy
   demonstrably is not an artifact of mixing cheap slow materials with expensive fast
   ones -- it reappears when the material is held constant. This is the empirical
   half of A and it is the strongest single point available.

C. **Power and heat.** Fast cells are the power-hungry ones (6T SRAM, static leakage
   on every cell, no low-power idle state like a DRAM capacitor). A terabyte of them
   cannot be powered or cooled as one block; spreading it out to cool it re-pays the
   propagation delay from A.

Then the conclusion that actually answers the question: because small-and-near is
forced to be faster than large-and-far, the best thing to do with the giant device is
to put a small fast array in front of it -- i.e. you would build a hierarchy *inside*
it. That is what a cache is. Cost would stop being the motive; physics would still
supply one.

Cost per bit gets one clause, acknowledged as real but not decisive, because the
question stipulates we built the thing anyway.

## Deliberately NOT included (R8)

- persistence / non-volatility as a separate reason the bottom of the hierarchy
  exists. True, but the question says "intermediate" devices, so it is off-target.
- address-decoder fan-out and banking as a 4th named mechanism -- it is really a
  restatement of A, so it is folded into A as a half-sentence.
- locality of reference as a 5th argument. It explains why a hierarchy *works well*
  rather than why one is *needed*; one clause in the conclusion is enough.
- cost of wafer area, yield, defect tolerance.

## Length budget

Target 300-380 words (brief). Aim ~340. Count with `wc -w` on prose stripped of
LaTeX markup before submitting.

---

# Round 1 continuation (2026-10-08 12:46)

The master restarted this worker with `fw spawn-worker p2 --force` after the run was
interrupted at ~03:02 (its process was killed while p2's validator was pending). The
playground was left intact, so round 1 re-entered on top of an already-written
`answer.tex`. `state.json` shows `p2: rounds 0`, and no p2 validator report exists in
`logs/` -- the validator never ran. So there is **no validator feedback to respond
to**; this is a first submission, not a revision.

I did not adopt the inherited draft on trust. What I re-verified from scratch:

- **Source.** `diff ingest/pages/os_hw_3_problems/alltext.txt input/os_hw_3_problems.md`
  -> identical. Brief's verbatim block matches line 5 of the input word for word.
- **Every number**, re-derived in SI units in a throwaway script sharing no code with
  `calc_size_latency.py`: area 168000 mm^2, side 409.88 mm, 2.3767 wafers,
  round trip 2.7344 ns, 10.94 cycles @ 4 GHz. All match what the answer quotes.
- **Both external figures**, by web search: the 0.021 um^2 HD SRAM cell is the
  published TSMC N5 number (and the densest production cell reported); ~32 Mib/mm^2
  is the same source's derived usable-cache density, which is the constant
  `crosscheck_area.py` leans on; L1/L2/L3 at ~4/14/40 cycles sits mid-range of
  published measurements (L1 4-5, L2 12-15, L3 40-50).

Two prose defects found in my own audit and fixed:

1. Thesis sentence read "at terabyte scale the two cannot be chosen independently".
   Muddy, and arguably false as written -- material and size plainly *can* be chosen
   independently. The actual claim is that size is the dominant term at this scale.
   Now: "at terabyte scale it is size that dominates."
2. "That time is bounded below by the array's linear dimension" bounded a *time* by a
   *length* -- a dimensional category error sitting inside the physics argument, and
   the first thing a hostile reader would pick at. Now: "bounded below by the time
   needed to cross the array, whose linear dimension grows as sqrt(C)...".

Net effect on length: 364 -> 368 words, still inside the 300-380 target. Source was
then rewrapped to 84 cols; `pdftotext` diff confirms the rendered page is byte
identical before and after the rewrap, so the rewrap touched source only.

---

# Round 2 (2026-10-08) — responding to validator FAIL

Validator raised two minor defects. I checked both myself before editing; **both are
real and I accepted both.** Neither changed a number or the conclusion.

## [1.1] "fastest cell" mislabelled the high-density cell — FIXED in the deliverable

The answer read "Take the fastest cell actually manufacturable, a high-density 6T SRAM
bit at 0.021 um^2". The HD cell is the *densest*, not the *fastest*. Confirmed from
the very source I had already cited in round 1: that search result states N5 offers
"a high-performance cell at 0.025 um^2 and a high-density cell at 0.021 um^2". So the
sentence was false, and it sat at the hinge of a question whose premise is literally
"the fastest materials available".

I took the validator's recommended **relabel** rather than switching to 0.025 um^2,
for a substantive reason, not just to save a re-run: the argument needs a **lower
bound** on physical size. The densest cell gives the smallest array and hence the
smallest crossing time, so quoting it concedes the maximum ground to the question's
premise. Switching to the HP cell would have made the answer *stronger* numerically
(2.0e5 mm^2, 447 mm, 2.98 ns, ~12 cycles — computed, see below) and therefore a weaker
piece of reasoning.

New text makes the lower-bound logic explicit instead of leaving it implicit:

    Take the densest cell in production, a 6T SRAM bit at 0.021 um^2; the faster
    high-performance variant is larger at 0.025 um^2, so this keeps the bound
    conservative.

All seven verified numbers are preserved untouched.

**Length.** The fix added ~13 words and pushed me to 382 by my own tokeniser (over the
380 ceiling). I cut the clause "and no choice of material moves that floor" from the
end of that paragraph: the new HP-variant sentence now carries that point concretely,
so the clause had become an abstract restatement of what preceded it — the R8
"summarising your own answer" pattern. Back to 374 (mine) / ~369 (validator's count,
which runs ~5 lower).

The same conflation was also sitting in the `SRAM_BITCELL_UM2` comment block in
`calc_size_latency.py`. Corrected there too, so the error does not survive anywhere in
the playground. Verified comment-only: `diff` of the script's full output before and
after is empty.

## [1.2] Cross-check sold as independent when it is circular — FIXED in playground docs

The validator is right and I verified the circularity arithmetically rather than
taking its word. Invert both routes to an effective per-bit area:

    bottom-up : 0.021 / 0.70        = 0.0300 um^2/bit
    top-down  : 1e6 / (32 * 2^20)   = 0.0298 um^2/bit   ratio 1.0066

Same cell, same ~30% overhead — WikiChip derives the ~32 Mib/mm^2 density from the
0.021 um^2 cell by assuming exactly that overhead, which is my own 70% constant. The
0.7% residual is 1 MiB vs 1e6 rounding. So it was never corroboration.

`crosscheck_area.py` rewritten to say so in its own docstring, and to print the
inversion above so the circularity is visible in the output rather than buried. What
the check legitimately establishes is narrower and is now stated as such: that my 70%
constant matches the industry convention.

**No delivered number is affected.** `answer.tex` quotes the cells-only 1.68e5 mm^2,
which is just (bits x cell area) and carries no efficiency assumption at all. That was
already the right choice; what was wrong was the claim made *about* the check.
