# p3 — Ex. 3.3, 3.4, 3.5, 3.6, 3.7, 3.8 (40 pts total)

**Your problem id is `p3`. Namespace every label, figure filename and macro with it**
(`\label{p3:alg:clock}`, `fig_p3_clock.pdf`). You are writing six answers into one
fragment; `\label{eq:aging}` would collide with another worker's and break the
master's compile.

## Where this comes from

`/home/xing/project/auto_hw_complete/input/os_hw_3_problems.md` — plain markdown.
Ingest produced no page images and no figure files for it because it is text only.
**None of these six questions refers to a figure**; there is nothing to go and look
at. Any diagram you draw is your own.

Anchor text: from `Ex. 3.3 | (5 pts) What does OS have to do when all page frames are
being used` through `Ex. 3.8 | (10 pts, 2pts for each algorithm) Describe page
replacement algorithms including FIFO, First-in Last-out (FILO), NRU, LRU, NFU?`

## Why these six are one problem and not six

They share objects. Ex. 3.8 supplies the definitions of FIFO, NRU, LRU and NFU that
Ex. 3.4, 3.5 and 3.6 then argue about; Ex. 3.3 is the question that page replacement
is the answer to; Ex. 3.7 is the other half of the same page-fault service routine
Ex. 3.3 describes. One worker writes them so that the document says one thing about
what NFU's counter does, not two. **Keep them as six separate, clearly headed
answers** — the grader marks them separately — but make them consistent, and let the
later ones lean on the earlier ones instead of redefining terms (e.g. 3.4 may say
"NFU as defined in 3.8" rather than restating it).

## The questions, transcribed verbatim

> Ex. 3.3 | (5 pts) What does OS have to do when all page frames are being used and
> there is at least one page to be brought in from hard disk to the main memory?

> Ex. 3.4 | (5 pts) Why would you use NFU over LRU?

> Ex. 3.5 | (5 pts) Why would you use NFU with aging over NFU or LRU?

> Ex. 3.6 | (5 pts) In what purpose the two-handed clock algorithm useful?

> Ex. 3.7 | (10 pts) Why do you have to back up the instruction after page fault
> handling? And which instruction is that?

> Ex. 3.8 | (10 pts, 2pts for each algorithm) Describe page replacement algorithms
> including FIFO, First-in Last-out (FILO), NRU, LRU, NFU?

## My reading (check it, don't just adopt it)

Points to get right, because these are the places this topic is usually answered
loosely:

- **3.3** is asking for the whole sequence, not just the words "page replacement":
  select a victim frame with a replacement policy, and — the part that is usually
  dropped — check the victim's dirty/modified bit and write it back to the swap area
  only if dirty, invalidate the old mapping (and the TLB entry for it), then read the
  new page in and update the page table. Mentioning that the faulting process blocks
  over the disk I/O is fair. 5 points, so keep it tight.
- **3.4** NFU over LRU: the honest answer is cost. True LRU needs either a hardware
  counter/timestamp written on *every* memory reference or a list reordered on every
  reference — infeasible in software, expensive in hardware. NFU needs only the
  reference bit most MMUs already provide, sampled periodically on a clock tick, so
  it is implementable in software at bounded cost. Say what is given up, too.
- **3.5** NFU-with-aging over plain NFU *and* over LRU: plain NFU never forgets — a
  page referenced heavily during program start-up keeps a high count forever and is
  retained long after it has gone cold, and ties between pages that were all hot once
  cannot be broken. Aging fixes this by shifting the counter right before adding the
  reference bit at the high-order end, so old references decay exponentially and the
  counter approximates recency, not lifetime frequency. Worth noting the limit: the
  counter has finite width (e.g. 8 bits), so it cannot distinguish references older
  than that many ticks, and it cannot distinguish two references within the same
  tick — it is an approximation of LRU, not LRU.
- **3.6** two-handed clock: the point is that it decouples *how often pages are
  scanned* from *how fast pages are evicted*. The front hand clears the reference
  bit; the trailing hand evicts pages whose bit is still clear. The gap between the
  hands sets how long a page has to prove it was referenced. It was introduced for
  machines where a plain one-handed clock either spun too slowly to find free frames
  in time (BSD/VAX is the standard reference) or, with little memory pressure,
  scanned so rarely that reference bits stayed set and the algorithm degenerated to
  FIFO. The useful framing is: it lets the system pre-build a pool of free frames and
  tune replacement aggressiveness independently of memory pressure.
- **3.7** has two parts and both are marked. *Which instruction*: the one that was
  executing when the fault was taken — the faulting instruction itself, which must be
  re-executed from its start, not resumed mid-way. *Why back it up*: the PC saved by
  the trap may already have advanced past (part of) it, and more importantly a CISC
  instruction may have been partially executed before the fault and have side effects
  already committed — auto-increment/auto-decrement addressing modes that have
  already updated a register, a multi-word block move partially done. Simply resuming
  would skip the memory access; restarting without undoing those side effects would
  apply them twice. So the handler must restore the PC to the instruction's first
  byte and undo partially applied effects — which is why machines either keep enough
  state in hidden registers to unwind, or are designed so instructions are
  restartable. 10 points: answer both halves explicitly.
- **3.8** five algorithms, 2 points each, so five short paragraphs of roughly equal
  weight. FIFO: evict the oldest-loaded page; cheap, ignores usage, suffers Belady's
  anomaly — naming Belady is worth the words. FILO ("first-in last-out"): as the
  assignment names it, evict the most recently loaded page, i.e. a stack discipline;
  it is in the list as a foil — note that it is a poor policy because it throws away
  the page most likely to be in the current working set, and say so. NRU: classify
  pages into four classes by the (referenced, modified) bit pair, evict at random
  from the lowest non-empty class, with the reference bit cleared periodically. LRU:
  evict the page unreferenced for longest; good, provably a stack algorithm (no
  Belady's anomaly), but costly to implement exactly. NFU: per-page counter
  incremented on each clock tick by the reference bit, evict the lowest counter;
  approximates LFU and has the never-forgetting flaw that aging fixes.

Keep the whole thing consistent: whatever you say NFU's counter does in 3.8 is what
3.4 and 3.5 must assume.

## Deliverable

- `answer.tex` — LaTeX **fragment** (no `\documentclass`, no `\begin{document}`, no
  `\usepackage`). Six clearly separated answers, in the order 3.3, 3.4, 3.5, 3.6,
  3.7, 3.8, each under its own heading naming the exercise and its points.
- `needs: plain`. No figure is required by any of these six. A small TikZ sketch of
  the two clock hands for 3.6 is allowed if it earns its space — if you draw one,
  `\usepackage{tikz}` goes in `preamble.txt` and the label is `p3:`-namespaced.
  Do not add diagrams to the other five.
- `preamble.txt` only for packages beyond amsmath/amssymb/graphicx/geometry.

**Length — read R8 below carefully, it binds hardest here.** Per-question targets:
3.3, 3.4, 3.5, 3.6 are 5-pointers at about 190 words each; 3.7 is a 10-pointer with
two explicit sub-questions, about 290 words; 3.8 is 10 points split five ways, so
about 60–70 words per algorithm, roughly 330 total. That is about 1,350 words for the
whole fragment. Coming in at 2,500 is the failure mode, and it will be counted.
## Rules for workers

**Master: copy this whole section verbatim into every `problem.md` you write.**
Workers and worker validators never see this file; the brief is the only channel
that reaches both of them.

These are not style preferences. They are defects. A worker that breaks one has
not finished, and a validator that passes one has not done its job.

### R8 — Answer the question asked, at the length it deserves

Write the shortest answer that earns full marks, then stop. Concrete targets,
measured from a previous assignment after a careful human edit:

| question | target |
|---|---|
| a 5-point short answer | about 190 words; up to 290 if it has several sub-parts |
| a 10-point paper summary and critique | about 550 words |

Left alone, an answer comes out **1.5 to 2 times** these lengths. That is the
failure mode to watch for in yourself. The excess is never new substance; it is
always one of these four:

- **exhaustive enumeration** — four examples where the question needs one, six
  hardware mechanisms where three carry the argument;
- **summarising your own answer** — a closing sentence that restates the opening
  one. If a paragraph begins "so the model is X" and ends "the model is therefore
  X", delete the ending;
- **explaining the significance of your own answer** — the question asked *where*
  the magic number is stored, not why that location is efficient;
- **stating what you are about to do** — "the three binding times are worth
  naming", "it is worth noting that".

Em-dashes are a symptom rather than a cause, but they mark the places to look:
one every 70 words means the sentences are being extended rather than ended.

**Validator: count the words.** Compare against the target above and against what
the problem is worth. Over target by more than a quarter, with no sub-part that
justifies it, is a defect to be reported and fixed, at severity major. Do not pass
an answer because it is correct if it is also twice as long as it needs to be.

### R9 — Read past the quotation

When you quote or cite a source, read the sentences that follow the quote before
you build an argument on it. Stop at the quote and you will write a criticism the
source already answers, or attribute to an author a claim they did not make.

Both of these happened in a previous assignment and both were findable with one
grep by the person marking it:

- A paper was criticised for raising a security problem and leaving it there. The
  next sentence of the paper proposed two countermeasures. (The real criticism was
  available and stronger: one countermeasure reintroduced the central authority the
  design existed to remove, and the other was justified only "on a system that
  assumes no malicious processes".)
- A paper's closing section was described as claiming a system succeeded because
  it had no predefined objectives. It says nothing of the sort; it says the authors
  were grateful never to have had to satisfy someone else's requirements. The
  critique was aimed at an invented claim.

So: quote the source, then say what the source does next with it. Never assert that
an author "leaves the problem there", "never asks", or "does not address" something
without having read to the end of that discussion.

**Validator: for every quotation and every characterisation of what a source says
or fails to say, open the source and read the surrounding passage yourself.** A
quotation that is verbatim can still be used to support a claim the source
contradicts two sentences later. Confirming the words exist is not the check;
confirming the argument survives the context is.
