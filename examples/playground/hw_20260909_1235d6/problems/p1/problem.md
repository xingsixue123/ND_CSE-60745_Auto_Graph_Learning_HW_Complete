# Problem p1 — Ex 1.1 through Ex 1.4 (20 pts total, 5 pts each)

## Where this lives in the assignment

The assignment is a plain markdown file, not a PDF:

    /home/xing/project/auto_hw_complete/input/hw_questions.md

It is 41 lines long and contains **no figures at all** (confirmed against
`ingest/manifest.json`: the only rendered document is `PaperList.xlsx`, and every one of its
six pages reports `n_images: 0` and `"figures": []`). So there is no image you need to look
at for this problem. Read `hw_questions.md` yourself to confirm the wording — do not rely
solely on my transcription below.

Anchor text: `Ex. 1.1 (5pts) | What is the role of the magic number for binary executable files?`
(line 5 of the file). Your four questions run from line 5 to line 17.

The assignment's global instruction, at line 1, is:

> Instructions: Finish the following exercise questions. You can utilize Google search and
> read articles that help you to answer the questions. But you cannot just copy the answers,
> put the answers in your own way. The total is 100 pts.

**"Put the answers in your own way" is a grading requirement.** Write prose in your own
words. Do not paste text from man pages, Wikipedia or a textbook.

## The questions, transcribed verbatim

> Ex. 1.1 (5pts) | What is the role of the magic number for binary executable files? Where is
> it stored?

> Ex. 1.2 (5pts) | List all segments that consist of an address space and explain each segment.

> Ex. 1.3 (5pts) | What are von-Neumann machines, and how are they related to the computers we
> use today?

> Ex. 1.4 (5pts) | Anyone who programmed in Unix environment using C or C++ (or other languages
> as well) surely experienced the famous error message \segmentation fault (core dumped)."
> Explain what this error message mean and list possible reason for this error. What does
> \segmentation" mean in this context? What does \core" mean in this context?

### Transcription note on Ex 1.4 — read this

The stray backslashes in Ex 1.4 are corruption, not content. The source was written in LaTeX,
where an opening double quote is typed as two backticks; the conversion to markdown mangled
them. The intended text is:

- `\segmentation fault (core dumped)."`  →  “segmentation fault (core dumped).”
- `\segmentation"`  →  “segmentation”
- `\core"`  →  “core”

**Do not reproduce the backslashes in your answer.** Use proper quotation marks.

## What the deliverable is

Plain prose. No code, no diagrams, no computation.

**Length: keep it short.** The user's specification for this assignment says explicitly:

> just few sentences sufficient for answering question 1.1-1.8

So aim for roughly 3–6 sentences per question — enough to hit every part the question asks
for, and then stop. A 5-pt question does not want an essay. Where a question has several
distinct parts, make sure each part is visibly answered; that is what a grader ticks off:

- **1.1** has two parts: the *role* of the magic number, and *where it is stored*. Answer both.
  (Mention concrete examples — the ELF magic `0x7F 'E' 'L' 'F'`, `#!` for scripts, `MZ` for
  PE — and the fact that it sits in the first bytes of the file header, which is what makes
  it cheap for the kernel's exec path to check.)
- **1.2** asks you to *list* the segments and *explain each*. A short labelled list is the
  right shape here: text/code, initialized data, BSS, heap, stack, and it is worth noting the
  memory-mapped region for shared libraries. One sentence of explanation each, and say which
  grow and in which direction.
- **1.3** has two parts: what a von Neumann machine *is* (stored-program, one memory for both
  instructions and data, the fetch–decode–execute cycle, the von Neumann bottleneck), and how
  today's machines *relate* to it — i.e. still von Neumann at the programming-model level, but
  with Harvard-split L1 caches, pipelines and multiple cores layered on top. Do not answer only
  the first half; the "how are they related" half is where the marks hide.
- **1.4** has four parts: what the message means, possible reasons (list several — null
  dereference, use-after-free, stack overflow from runaway recursion, writing to a string
  literal / read-only page, wild pointer, buffer overrun past a mapping), what "segmentation"
  means here, and what "core" means here. The etymology is worth one clause each: "segmentation"
  from segmented memory / the hardware's memory-protection unit signalling an access outside a
  valid segment, and "core" from magnetic-core memory, the dump being an image of the process's
  memory at the moment it died.

## LaTeX / output rules

Write your answer as a LaTeX **fragment** into `answer.tex` in your OUTPUT dir. It will be
`\input{}` into a master document, so:

- No `\documentclass`, no `\begin{document}`, no `\usepackage` in `answer.tex`.
  Any extra package goes one `\usepackage{...}` per line in `preamble.txt`.
- Start at `\section*{...}` / `\subsection*{...}` level.
- **Namespace every label with `p1:`** — e.g. `\label{p1:sec:magic}`. Unnamespaced labels
  collide with the other workers' fragments and break the master compile.
- Structure it so a grader can find each answer: one `\subsection*{Ex. 1.1 (5 pts)}` (etc.)
  per question, restating the question briefly or not at all, then the answer.
- Keep the question numbering exactly as the assignment has it: Ex. 1.1, Ex. 1.2, Ex. 1.3,
  Ex. 1.4.
