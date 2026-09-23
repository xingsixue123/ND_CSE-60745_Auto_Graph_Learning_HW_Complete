# p3 — Ex. 2.4 (5 pts): why a thread context switch is much cheaper than a process one

**Problem id: `p3`.** Namespace every label and macro with `p3`.

## Where this lives in the assignment

The assignment is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, a byte-for-byte copy of the markdown.
There is no figure anywhere in this assignment. Read the markdown file itself as your
ground truth and check the transcription below against it.

Anchor text: `Ex. 2.4 | (5pts) The amount of time that takes to make a context-switch
between threads versus that of between processes is much shorter.`

## The question, transcribed verbatim

> Ex. 2.4 | (5pts) The amount of time that takes to make a context-switch between
> threads versus that of between processes is much shorter. Explain why.

Read it precisely: it is about switching between two threads **of the same process**
versus switching between two processes. Say so explicitly, because a switch between
threads of *different* processes costs the same as a process switch, and naming that
boundary is part of showing you understand the reason.

The assignment's preamble also applies: *"You can utilize Google search and read
articles that help you to answer the questions. But you cannot just copy the answers,
put the answers in your own way."*

## What the deliverable is

**plain.** A causal explanation, not a list of differences between threads and
processes. The chain a grader wants: threads of one process share the address space,
so the switch does not change the memory map — no page-table / `CR3` (or `TTBR`) swap,
no TLB flush and no cache pollution from a new working set, and none of the *indirect*
cost of refilling TLB and cache afterwards, which is the larger half of the bill. What
must still be saved and restored is the small per-thread state: the register file
(including PC and stack pointer) and the kernel stack / thread control block. Also
relevant and worth a clause each: the open-file table, signal dispositions and other
per-process kernel state do not have to be swapped; and a user-level thread switch can
avoid the kernel trap altogether.

Do not turn this into a table of "threads vs processes" or a treatise on ASIDs/PCIDs —
one clause noting that tagged TLBs soften, but do not remove, the flush cost is the
right weight. You do not need to cite measured numbers; if you do quote a figure from
a source, cite it properly and make sure the source actually says it.

## Length

A 5-point short answer: about 190 words. See R8 below — this is exactly the kind of
question that comes out at twice the length it needs.

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
