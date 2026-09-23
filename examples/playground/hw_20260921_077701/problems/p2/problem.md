# p2 — Ex. 2.2 (5 pts) + Ex. 2.3 (5 pts): process creation, and a fork()/exec() program

**Problem id: `p2`.** Namespace every label, figure filename and macro with `p2`
(e.g. `\label{p2:lst:forkexec}`).

## Where this lives in the assignment

The assignment is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest therefore produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, a byte-for-byte copy of the markdown.
There is no figure anywhere in this assignment; nothing is hidden in an image channel.
Read the markdown file itself as your ground truth and check the transcription below
against it.

Anchor text: `Ex. 2.2 | (5pts) The following shows three different ways a process can be
created.` and `Ex. 2.3 | (5pts) Write a small program ...`

## The questions, transcribed verbatim

> Ex. 2.2 | (5pts) The following shows three different ways a process can be created.
>
> A human user explicitly commands the OS to run a program by double-clicking the
> program icon or typing a command.
> A currently running process creates a sub-process (also known as a child process)
> prompted by an external event (a human user's request, an event caused by another
> process).
> A currently running process creates a child process explicitly executing an
> instruction such as fork().
> The third case, in which a currently running process creates a new process, in
> general covers the first two cases. Explain why.

(In the source markdown the three cases are consecutive list lines; they are cases 1,
2 and 3 in order.)

> Ex. 2.3 | (5pts) Write a small program that uses fork() and exec() to run the ls
> command.

The assignment's preamble also applies: *"You can utilize Google search and read
articles that help you to answer the questions. But you cannot just copy the answers,
put the answers in your own way."*

## What the deliverable is

**Ex. 2.2 — plain.** An explanation, not a list of facts about fork. The argument the
grader is looking for: in case 1 the human does not create anything — the click or the
keystroke is delivered to a process that is *already running* (the desktop shell /
window manager, or the command shell), and that process is what forks. Case 2 is the
same mechanism with the trigger coming from software rather than a human. So all three
collapse onto case 3, and the only thing that varies is what caused the already-running
process to decide to fork. Worth including, briefly: there is exactly one process on a
Unix system that is *not* created this way — the initial process (`init`/`systemd`, pid 1)
hand-built by the kernel at boot — and everything else descends from it, which is what
makes "a running process creates a process" the general case rather than one case among
three. Do not pad this with a general tutorial on fork's copy-on-write semantics.

**Ex. 2.3 — code, actually run.** Write a small C program using `fork()` and one of the
`exec` family to run `ls`, compile it with `gcc` (available on the machine; if it is
not, say so in your report rather than pretending) and **run it**. The program must:

- call `fork()`, check the return value for all three cases (`-1` error, `0` child,
  `> 0` parent);
- in the child, `execvp("ls", ...)` (or `execlp`) and handle the case where exec
  returns, which means it failed — `perror` + `_exit`;
- in the parent, `waitpid()` for the child and report its exit status.

Put the real source in `answer.tex` as a listing (this question explicitly asks for a
program, so a code listing is required here — it is not a code dump), and quote the
actual output you saw, trimmed to a couple of lines. Keep the source in your PLAYGROUND
and name the file and the compile/run command in your submission report.

Use `lstlisting` (package `listings`) or `verbatim` for the code. If you use `listings`,
put `\usepackage{listings}` and any colour package in `OUTPUT/preamble.txt`, and define
any style with a `p2`-namespaced name (e.g. `\lstdefinestyle{p2cstyle}{...}`) inside
`answer.tex` — remember `answer.tex` may not contain `\usepackage`.

## Length

Two 5-point questions. Target roughly 190 words of prose for 2.2, and for 2.3 the
listing plus a few sentences of explanation of what each branch does. See R8 below.

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
