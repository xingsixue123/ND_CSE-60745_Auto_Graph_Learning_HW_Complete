# p1 — Ex. 2.1 (15 pts): schedule diagrams for Round-Robin, FIFO and SJF

**Problem id: `p1`.** Namespace every label, figure filename and macro with `p1`
(e.g. `\label{p1:fig:rr}`, `fig_p1_rr.pdf`).

## Where this lives in the assignment

The assignment is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest therefore produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, which is a byte-for-byte copy of the
markdown. There is no figure anywhere in this assignment; nothing is hidden in an
image channel. Read the markdown file itself as your ground truth and confirm the
transcription below against it. (`ingest/manifest.json` records it as
`kind: text_document`, which is why there are no renders.)

Anchor text: `Ex. 2.1 | (15pts) Draw schedule diagrams ...`

## The question, transcribed verbatim

> Ex. 2.1 | (15pts) Draw schedule diagrams of the following task set for Round-Robin,
> First-in-first-out (FIFO), and Shortest job first (SJF), respectively. The task set,
> (arrival time, execution time): T1(1, 10), T2(2, 4), T3(3, 1), T4(4, 6).  Time
> quantum for Round-Robin is 1 time unit. If there is a tie, schedule tasks with
> smaller index. For example, if T1 and T2 can be both scheduled, schedule T1 first.
> (5pts for each diagram).

The assignment's own preamble also applies: *"You can utilize Google search and read
articles that help you to answer the questions. But you cannot just copy the answers,
put the answers in your own way."*

## What the deliverable is

**code + diagram.** Specifically:

1. **Compute, do not eyeball.** Write a small simulator in your PLAYGROUND that
   implements all three policies over this task set and prints, for each, the
   per-time-unit occupancy of the CPU plus completion time, turnaround time and
   waiting time per task. Every number that appears in `answer.tex` must come out of
   that program. Keep the script; name it in your submission report.
2. **Three schedule diagrams**, one per policy, as vector PDFs in OUTPUT:
   `fig_p1_rr.pdf`, `fig_p1_fifo.pdf`, `fig_p1_sjf.pdf` (or one combined figure —
   your call, but each policy's diagram must be individually readable). A schedule
   diagram here means a Gantt chart: time on the horizontal axis with integer ticks
   covering the whole makespan, one labelled band or row per task, arrival instants
   marked, and the idle interval before the first arrival shown as idle rather than
   silently cropped. Follow the diagram standards in your context file — 3–6 in wide,
   legible fonts, no title, vector PDF.
3. A short table of completion / turnaround / waiting times per policy is worth
   including (it is cheap and it is what a grader checks the diagram against), but
   keep the prose minimal: this question asks you to *draw*, and the marks are 5 per
   diagram.

## Conventions you must state and defend

The task set is deliberately tie-heavy, so the answer is only well defined once the
conventions are fixed. Decide each of these, state it in one line in `answer.tex`, and
make the simulator implement exactly what you state:

- **t = 0 to t = 1 is idle** — nothing has arrived yet. Say so on the diagrams.
- **SJF**: the classical "shortest job first" is **non-preemptive** — once a task is
  dispatched it runs to completion, and the scheduler picks the shortest *total*
  execution time among the tasks that have arrived. Use that as the answer. You may
  add at most one sentence noting that the preemptive variant (SRTF) gives a different
  schedule; do not draw a fourth diagram for it.
- **FIFO**: non-preemptive, dispatch in order of arrival.
- **Round-Robin, q = 1**: at an instant where a task arrives *and* the running task is
  preempted, say explicitly whether the arriving task or the preempted task goes into
  the ready queue first (the usual convention, and the one the smaller-index tie rule
  is consistent with, is that the arriving task is enqueued first). State the
  convention; a grader has to be able to reproduce your queue.
- The stated tie rule — *smaller index wins* — applies to SJF's equal-burst case and to
  any ambiguity in queue ordering.

Sanity check the simulator before you trust it: total busy time must be
10 + 4 + 1 + 6 = 21 units, and with one idle unit at the start every policy must finish
at t = 22.

## Length

This is a diagram question. The written part should be short: conventions, the three
figures, the timing table, and one or two sentences of comparison at most. See R8
below.

---

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
