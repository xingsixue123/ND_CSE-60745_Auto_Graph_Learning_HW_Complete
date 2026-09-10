# Problem p2 — Ex 1.5 through Ex 1.8 (20 pts total, 5 pts each)

## Where this lives in the assignment

The assignment is a plain markdown file, not a PDF:

    /home/xing/project/auto_hw_complete/input/hw_questions.md

It is 41 lines long and contains **no figures at all** (confirmed against
`ingest/manifest.json`: the only rendered document is `PaperList.xlsx`, and every one of its
six pages reports `n_images: 0` and `"figures": []`). There is no image you need to look at
for this problem. Read `hw_questions.md` yourself to confirm the wording — do not rely solely
on my transcription below.

Anchor text: `Ex. 1.5 (5pts) | When a compiler generates the binary code for a source program`
(line 21 of the file). Your four questions run from line 21 to line 33.

The assignment's global instruction, at line 1, is:

> Instructions: Finish the following exercise questions. You can utilize Google search and
> read articles that help you to answer the questions. But you cannot just copy the answers,
> put the answers in your own way. The total is 100 pts.

**"Put the answers in your own way" is a grading requirement.** Write prose in your own words.

## The questions, transcribed verbatim

> Ex. 1.5 (5pts) | When a compiler generates the binary code for a source program written in a
> high-level programming language, it does not know where and how the binary code will be
> loaded by the operating system. Why not? In order to generate a binary code, the compiler,
> however, must make certain assumptions on where and how the binary code will be loaded in the
> main program by the operating system. What are the reasonable assumptions that are made by
> most of compilers in terms of where and how?

> Ex. 1.6 (5pts) | What happens when we double-click a program icon? Or type a command at the
> prompt? Describe all the steps happening in OS until we see the application on the screen.

> Ex. 1.7 (5pts) | Finding the physical address from a virtual address in a contiguous memory
> allocation scheme.

> Ex. 1.8 (5pts) | What is the round-robin scheduler?

## What the deliverable is

Plain prose. No diagrams required. No code required.

**Length: keep it short.** The user's specification for this assignment says explicitly:

> just few sentences sufficient for answering question 1.1-1.8

Aim for roughly 3–6 sentences per question. Ex 1.6 is a "describe all the steps" question, so
a compact numbered list of steps is appropriate there and will read better than a paragraph —
but keep each step to one line. Do not turn any of these into an essay.

Guidance on the parts a grader will be ticking off:

- **1.5** has two halves. *Why not*: the compiler emits one object/executable that must run on
  many machines under many memory conditions; it cannot know what else will be resident, how
  much memory the machine has, where the loader will find a free hole, or (with ASLR / shared
  libraries / demand paging) even where the OS will choose to put it on this particular run.
  *What it assumes instead*: essentially that it is generating code into a **logical address
  space that starts at 0** and is **contiguous**, with the run-time binding of logical to
  physical addresses left to the hardware (relocation register / MMU) or to a relocating
  loader. Mention that this is exactly what makes relocatable code and position-independent
  code possible, and note the compile-time / load-time / execution-time binding distinction.
  Answer BOTH halves — half the marks are in "what are the reasonable assumptions".

- **1.6** wants the whole chain, end to end. Something like: shell or GUI file manager receives
  the event and resolves the command to a path; `fork()` (or equivalent) creates a new process;
  `exec()` on the executable; the kernel checks permissions and reads the header, validates the
  **magic number**, and works out the format; the old address space is torn down and a new one
  built — text, data, BSS, heap, stack — usually by memory-mapping the file rather than reading
  it in; the dynamic linker/loader is invoked to map and relocate shared libraries; the PCB is
  set up and the process is put on the ready queue; the scheduler dispatches it; it starts at
  its entry point, faulting pages in on demand; it connects to the window system / terminal and
  draws; the parent (a shell) typically `wait()`s, while a GUI launcher usually does not. Note
  in one clause that the double-click and the typed command differ only in *how* the command
  line is assembled — from then on the path is identical. That observation is the point of the
  question being asked as two questions.

- **1.7** is the one question here that benefits from being concrete. Contiguous allocation
  means each process gets one contiguous block, so translation is a single add with a bounds
  check: the MMU compares the virtual (logical) address against the **limit register** and
  traps if `virtual >= limit`, otherwise `physical = base + virtual` using the **relocation
  (base) register**. Give a short worked numerical example (e.g. base = 14000, limit = 3000,
  virtual address 346 → physical 14346; virtual address 3200 → addressing trap), because a
  question phrased as "finding the physical address" is asking you to demonstrate the
  procedure, not just name it. State the check-then-add order explicitly. You may typeset the
  formula with `amsmath`; a tiny two-line worked example is enough, and do NOT draw a figure.

- **1.8** wants the definition and the mechanism: preemptive FCFS with a fixed **time quantum**,
  ready queue treated circularly, a timer interrupt preempts the running process and moves it to
  the tail. Say what the quantum trades off — too large degenerates to FCFS, too small and
  context-switch overhead dominates — and name its virtue (fairness / bounded response time,
  no starvation, each of n processes gets ~1/n of CPU in slices of at most q) and its vice
  (poor average turnaround time; it ignores priority and job length).

## LaTeX / output rules

Write your answer as a LaTeX **fragment** into `answer.tex` in your OUTPUT dir. It will be
`\input{}` into a master document, so:

- No `\documentclass`, no `\begin{document}`, no `\usepackage` in `answer.tex`.
  Any extra package goes one `\usepackage{...}` per line in `preamble.txt`.
- Start at `\section*{...}` / `\subsection*{...}` level.
- **Namespace every label with `p2:`** — e.g. `\label{p2:eq:reloc}`. Unnamespaced labels
  collide with the other workers' fragments and break the master compile.
- One `\subsection*{Ex. 1.5 (5 pts)}` (etc.) per question so a grader can find each answer.
- Keep the question numbering exactly as the assignment has it: Ex. 1.5 … Ex. 1.8.
