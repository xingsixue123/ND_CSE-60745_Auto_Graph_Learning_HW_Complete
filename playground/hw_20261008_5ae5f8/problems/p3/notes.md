# p3 notes — Ex. 3.3-3.8 (40 pts)

## R7 channel reconciliation

Source is `input/os_hw_3_problems.md`, a **plain markdown text file**, not a PDF.
`ingest/manifest.json` classifies it `kind: text_document` with no `pages` array,
no `page_*.png`, no `page_*_fig_*.*`. So only ONE channel physically exists
(`ingest/pages/os_hw_3_problems/alltext.txt`); there is no image channel and no
figure channel to read, because ingest produced none.

Verified by diff: the ingest text is byte-identical to `input/os_hw_3_problems.md`
except for a trailing newline. Command:

    diff <(sed 's/[[:space:]]*$//' input/os_hw_3_problems.md) \
         <(grep -v '^===' ingest/pages/os_hw_3_problems/alltext.txt | sed 's/[[:space:]]*$//')
    -> only difference: "\ No newline at end of file" on the last line.

Brief vs source: the six questions quoted in problem.md are **verbatim identical**
to the source, including the odd grammar ("In what purpose the two-handed clock
algorithm useful?", the trailing "?" on 3.8's imperative). No discrepancy to report.

None of 3.3-3.8 refers to a figure. Confirmed by reading the full source: the only
question in the whole assignment that mentions a figure is Ex. 3.1 ("Explain your
idea by drawing the memory map"), which is not mine.

## What this needs

**plain**, for all six. No computation, no data, no measurement anywhere in the six
questions -> no `code`. No question says plot/draw/show/visualize -> no `diagram`
is *required*.

One optional exception, explicitly sanctioned by the brief: a small TikZ sketch of
the two hands for 3.6. Decision: **include it**. 3.6's whole answer turns on the
*gap between the hands* being the test window, and a 2-inch circle with two hands
and a labelled gap carries that geometrically in a way a sentence cannot. Inline
TikZ (not a fig_p3_*.pdf), as the brief directs, with `\usepackage{tikz}` in
preamble.txt and a `p3:`-namespaced label. No diagrams on the other five.

## Length budget (R8) — hard target

| q | pts | target words |
|---|---|---|
| 3.3 | 5 | ~190 |
| 3.4 | 5 | ~190 |
| 3.5 | 5 | ~190 |
| 3.6 | 5 | ~190 |
| 3.7 | 10 (2 sub-parts) | ~290 |
| 3.8 | 10 (5 x 2) | ~330 (60-70 each) |
| **total** | **40** | **~1350** |

Ceiling before it is a major defect: 1350 * 1.25 = ~1690. Will measure with a
script that strips LaTeX, not by eye.

## Consistency contract across the six

Fixed definition of NFU, used identically in 3.4, 3.5 and 3.8:
  per-page software counter; at each clock tick the OS ADDS that page's R bit to
  the counter and CLEARS R; evict the smallest counter. Measures frequency over
  the page's whole lifetime; never forgets.
Aging (3.5 only) = same sampling, but SHIFT the counter right one bit first, then
  insert R at the HIGH-ORDER end. Weight of a reference halves per tick.
3.3 ends by restarting the faulting instruction -> hands off to 3.7.
3.4/3.5's cost argument cites LRU's per-reference cost, defined once in 3.8.

## Facts to verify rather than assert from memory

1. Two-handed clock rationale + BSD pagedaemon attribution.
2. VAX/CISC: hidden internal registers used to unwind partially-executed
   instructions; autoincrement as the canonical side-effect example.
3. Belady's anomaly: FIFO suffers it, LRU does not (stack algorithm).

## Verification results (done, with sources)

**(1) Two-handed clock — CONFIRMED.** Chalmers EDA092 "4BSD UNIX Virtual Memory"
slides (fetched, text extracted with pdftotext; copy under
`.claudecfg/.../tool-results/webfetch-*.pdf`):

  - "If a large main memory is used, the clock algorithm with one hand do not work
    very well because the time to scan all page frames is too large."
  - "The first clock hand is used to reset the reference bit, and the second clock
    hand releases pages with the referenced bit still reset. (they have not been
    referenced in the time span between the scan of the first and second clock
    hands)"
  - "The goal for the pageout daemon is to assure that there are a sufficient
    number of free frames available at all times." Woken every 250 ms; sweeps only
    far enough to restore `lotsfree` free frames; capped so it uses <10% of CPU.

  R9 check — I read past each quote. The slides do NOT stop at "two hands exist";
  they go on to give the free-frame-pool purpose and the lotsfree mechanism, which
  is exactly the second half of my 3.6 answer. So the "decouples scan rate from
  eviction rate / pre-builds a free pool" framing is the source's own framing, not
  my gloss. The one thing I infer rather than quote is the *degenerate-to-FIFO*
  consequence of a slow single hand; the slides state the premise (revolution too
  long) and I state the consequence. Flagged as an inference in submission.md.

**(2) Instruction restart — CONFIRMED.** UW-Madison CS537 notes
<https://pages.cs.wisc.edu/~solomon/cs537/html/paging2.html>:
  - restart so as to "re-try the offending instruction";
  - on the 68000 "the PC will be pointing at the word immediate following the part
    of the instruction that caused the fault", hence "How can the OS figure out
    where the instruction started, so that it can back the PC up to retry?";
  - autoincrement/autodecrement modes change index registers as a side effect and
    after a mid-instruction fault "it may be difficult to figure out which
    registers have been modified so that they can be restored";
  - hardware fix: designers "either they undo the effects of the instruction before
    faulting, or they dump enough information into registers somewhere that the OS
    can undo them."
  Corroborated independently by search hits describing the two standard approaches
  (instruction restart vs instruction continuation) and the 68010 saving ~100 bytes
  of internal state to resume mid-instruction.

**(3) Belady's anomaly** — FIFO suffers it; LRU is a stack algorithm and does not.
  Standard result (Belady/Nelson/Shedler 1969; Mattson et al. 1970). Asserted from
  textbook knowledge, not separately re-verified; it is the one claim in 3.8 I did
  not chase a source for, and it is not load-bearing for any other answer.

## Figure decision detail

Inline, non-floating `tikzpicture` inside `\begin{center}`, NOT a `figure` float and
NOT a separate `fig_p3_*.pdf`. Reasons: (a) the brief sanctions inline TikZ here;
(b) a float can drift pages away from Ex. 3.6 once the master assembles six
problems, and the sketch is only useful adjacent to the text; (c) with no float and
no cross-reference there is no `\label` at all, so there is nothing to collide with
another worker's labels. Referenced in prose as "the sketch", not by `\ref`.
