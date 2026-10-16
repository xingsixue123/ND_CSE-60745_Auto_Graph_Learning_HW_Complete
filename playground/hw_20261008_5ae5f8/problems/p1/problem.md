# p1 — Ex. 3.1 (10 pts)

**Your problem id is `p1`. Every LaTeX label, every figure filename and every macro
you define must be namespaced with it** (`\label{p1:fig:map}`, `fig_p1_memmap.pdf`).

## Where this comes from

The assignment is a plain markdown file:
`/home/xing/project/auto_hw_complete/input/os_hw_3_problems.md`

It is a text document — ingest produced no page images and no figure files for it
(`ingest/pages/os_hw_3_problems/alltext.txt` is the whole thing), because there is
nothing in it but text. **There is no figure to read for this question.** The
diagram in the deliverable is one *you* draw, not one you extract.

Anchor text: `Ex. 3.1 | (10pts) The CPU (most of them) assumes that programs are
running from address 0`

## The question, transcribed verbatim

> Ex. 3.1 | (10pts) The CPU (most of them) assumes that programs are running from
> address 0 and the address space of the programs are contiguous. MMU enable the CPU
> make such an assumption. Consider a memory management for a system that only allows
> one application program to be loaded in the main memory and run. This means that at
> any given time, only the OS and one application program are loaded in the main
> memory. If we want to support the CPU's assumption without an MMU, how would you
> load the program and OS in the main memory? Explain your idea by drawing the memory
> map.

## My reading (separate from the transcription above — check it, don't just adopt it)

The constraint set is: no MMU, so no address translation at all — every address the
CPU emits goes straight to the memory bus; exactly one application resident at a
time, plus the OS. The program must believe it starts at physical address 0 and
occupies a contiguous block. The question is where the OS can live such that the
application still owns address 0.

The expected shape of the answer is a layout decision plus the memory map that
realises it, and the interesting part is what has to live at the very bottom of
memory on a real machine (the interrupt/trap vector table, which the hardware fetches
from fixed low addresses) and how you reconcile that with giving address 0 to the
user program. Say what you decide about that rather than ignoring it. Also address
what happens at the boundary — with no MMU there is no hardware protection, so say
what, if anything, stops the application from writing over the OS (a base/limit or
fence register is hardware, not an MMU; whether you allow yourself one is a design
choice you should state).

If you think the sensible answer is "OS at the high end of physical memory, program
loaded at 0 upward", say so and defend it. If you think it is something else, say
that instead. What matters is that the map and the prose agree and that the CPU's
two assumptions (starts at 0, contiguous) are visibly satisfied by the picture.

## Deliverable

- `answer.tex` — a LaTeX **fragment** (no `\documentclass`, no `\begin{document}`,
  no `\usepackage`), starting at a section/subsection heading for `Ex. 3.1`.
- **A memory map figure is required** — the question says "Explain your idea by
  drawing the memory map", so an answer without a drawing loses marks. Draw it with
  TikZ inline in `answer.tex` (preferred: no external file to ship, and `tikz` is
  already installed) or as `fig_p1_memmap.pdf` referenced by **bare filename**.
  Label the boundaries with addresses (0, the top of the program's region, the
  bottom and top of the OS region, and the physical top of memory). Make it legible
  at print size.
- `preamble.txt` — one `\usepackage{...}` per line for anything beyond
  amsmath/amssymb/graphicx/geometry. If you use TikZ, put `\usepackage{tikz}` there.

Write it to your OUTPUT directory. Nothing else may go there (no code, no logs, no
`.aux`).
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
