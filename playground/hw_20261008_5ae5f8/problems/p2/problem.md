# p2 — Ex. 3.2 (10 pts)

**Your problem id is `p2`. Namespace every label, figure filename and macro with it**
(`\label{p2:...}`, `fig_p2_*.pdf`).

## Where this comes from

`/home/xing/project/auto_hw_complete/input/os_hw_3_problems.md` — a plain markdown
file. Ingest produced no page images and no figure files for it because it is text
only. **This question refers to no figure**; there is nothing to go and look at.

Anchor text: `Ex. 3.2 | (10 pts) Memory hierarchy is given by the speed of memory
devices and the size of the devices along the hierarchy.`

## The question, transcribed verbatim

> Ex. 3.2 | (10 pts) Memory hierarchy is given by the speed of memory devices and the
> size of the devices along the hierarchy. What if we build a giant memory device
> made of the fastest materials available that is as big as some terabytes? Would
> that eliminate the need for having intermediate memory devices as in memory
> hierarchy? Why or why not?

## My reading (check it, don't just adopt it)

This is a yes/no question with a required justification, and the grader wants the
justification, not the verdict. Commit to an answer in the first sentence and then
support it.

The substance available to you: cost per bit is the reason the hierarchy exists in
the first place, but it is not the only reason and an answer that stops there is a
5-point answer, not a 10-point one. The physical arguments are the stronger half —
access time is bounded below by signal propagation across the array, so a device's
latency grows with its physical size no matter what it is built from; a terabyte of
the fastest material is therefore *not* as fast as a kilobyte of it. Address
decoding, fan-out, wire delay dominating gate delay at scale, and power/heat density
all push the same way. The conclusion that follows is that the hierarchy is not a
workaround for expensive fast memory that would evaporate if the memory were cheap —
it is a response to a size/speed trade-off that is intrinsic to the device, so you
would end up building a hierarchy *inside* the giant device (which is, in effect,
what caches already are).

You do not need every argument above. Pick the ones that carry the conclusion — R8
below is explicit that enumerating six mechanisms where three suffice is a defect.

## Deliverable

- `answer.tex` — LaTeX **fragment** (no `\documentclass`, no `\begin{document}`, no
  `\usepackage`), starting at a section/subsection heading for `Ex. 3.2`.
- `needs: plain`. No figure is required. Do not invent one to pad the answer; if a
  small diagram genuinely helps your argument you may add one, namespaced as above.
- `preamble.txt` only if you need a package beyond
  amsmath/amssymb/graphicx/geometry.

Target length: this is a 10-point question with no sub-parts. Roughly 300–380 words.
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
