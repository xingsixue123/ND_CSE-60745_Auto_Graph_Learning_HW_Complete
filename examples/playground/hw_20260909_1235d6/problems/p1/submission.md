# p1 — submission

## What the problem asked

Four conceptual OS questions, 5 pts each, 20 pts total:

- **Ex. 1.1** — the role of the magic number for binary executables, and where it is stored.
- **Ex. 1.2** — list all segments that make up an address space and explain each.
- **Ex. 1.3** — what von Neumann machines are, and how they relate to computers we use today.
- **Ex. 1.4** — what "segmentation fault (core dumped)" means, possible reasons for it, what
  "segmentation" means in this context, and what "core" means in this context.

**Source and brief-vs-page reconciliation.** The assignment is *not* a PDF — it is
`/home/xing/project/auto_hw_complete/input/hw_questions.md`, 41 lines of plain markdown, which I
read directly (the authoritative channel for a text source). My four questions are on lines
5, 9, 13 and 17. **The brief's transcription matches the source word for word; no
disagreement to report.**

On R7 (three channels): there is no image channel for this problem, and I want to be explicit
rather than claim a check I did not make. `ingest/manifest.json` lists exactly one rendered
document, `PaperList.xlsx` (6 pages), and every one of those pages reports `n_images: 0` and
`"figures": []`. `hw_questions.md` is not rendered at all because it is already text. So there
is no figure anywhere in this assignment, nothing for my questions to refer to, and no
transcription-from-a-drawing step. The three-channel rule is satisfied vacuously.

I accepted the brief's reading that the stray backslashes in Ex 1.4 (`\segmentation fault
(core dumped)."`) are LaTeX-to-markdown corruption of opening double quotes, not content. The
evidence is positional: every backslash sits exactly where an opening quote belongs, and every
*closing* quote survived intact — consistent with `` `` ``→`\` mangling. I render them as
proper quotation marks and do not reproduce the backslashes.

## What I decided it needed

**plain only.** No code, no diagram, no computation.

Nothing in Ex 1.1–1.4 asks for a number, a count, a ranking, a plot, or anything to be drawn
or illustrated. They are four definition/explanation questions. There is consequently **no
computed value anywhere in `answer.tex`**, and no figure. Adding either would be padding, and
the user's spec explicitly asks for brevity.

## What I did

Wrote the four answers from my own knowledge, in my own prose. The assignment's global
instruction (line 1) makes "put the answers in your own way" a *grading requirement*, so I
deliberately wrote nothing that is lifted from a man page, Wikipedia or a textbook.

I worked from an explicit part-checklist rather than writing free-form, because these
questions each bundle several sub-questions and the marks sit in the parts, not in the volume:

- 1.1 → role **and** storage location, with concrete magic numbers (ELF `0x7F 'E' 'L' 'F'`,
  `#!` = `0x23 0x21`, PE `MZ`, Java `0xCAFEBABE`) and the point that sitting at offset 0 in the
  header is what makes the check cheap on the exec path.
- 1.2 → all six regions (text, `.data`, BSS, heap, mmap region, stack), one sentence each,
  stating which grow and in which direction, and closing on the heap/stack gap — which sets up
  1.4.
- 1.3 → both halves. What the machine *is* (stored-program, single memory for code and data,
  fetch–decode–execute, the von Neumann bottleneck) **and** how today's machines relate: still
  von Neumann at the programmer-visible level, with split L1 caches, pipelining, OoO and
  multicore layered underneath to hide the bottleneck. The brief warned that the "how are they
  related" half is where the marks hide; I gave it a full paragraph.
- 1.4 → all four parts, each under its own bold run-in heading so a grader can tick them off:
  meaning (MMU fault → `SIGSEGV` → default action kills and dumps core; the message is the
  *shell* reporting the child's death), seven possible reasons, then the etymology of
  "segmentation" (segmented memory, base/limit/rights, hardware trapping an out-of-bounds
  reference — name outlived the mechanism, since we page now) and of "core" (magnetic-core
  memory; the dump is the process's memory image plus register state at the fault instant).

Length is ~3–6 sentences per question as the spec asked, with 1.2 and 1.4 using compact lists
because those two questions explicitly say "list".

I then test-compiled the fragment inside a throwaway master document and looked at the
rendered pages.

## Intermediate steps and code

No code produced any *result* — there are no computed values in this answer. The only scripts
are build/verification scaffolding:

- `notes.md` — the plan and the part-checklist, written before drafting.
- `build/master.tex` — throwaway wrapper (`\documentclass` + `geometry` + `amsmath,amssymb` +
  `enumitem` + `\input{answer.tex}`) used only to prove the fragment compiles. Not a
  deliverable.
- Reproduce the compile:
  `cd build && pdflatex -interaction=nonstopmode master.tex` → exit 0, 2 pages, no warnings.
- Reproduce the visual check: `pdftoppm -r 110 -png master.pdf pg` → `pg-1.png`, `pg-2.png`.
- Reproduce the lint:
  `python3 framework/tools/lint_output.py output/hw_20260909_1235d6/p1` → `OUTPUT LINT OK`.

## Results

**There are no computed values in `answer.tex`** — this is a prose-only problem, so there is
nothing in the answer that came out of a program. The factual claims (magic-number byte
patterns, segment layout, signal name) are standard OS knowledge, not measurements.

The only empirical results I generated are about the build:

| Claim | How verified |
|---|---|
| Fragment compiles inside a master document | `pdflatex master.tex`, exit 0 |
| 2 pages, no LaTeX warnings, no undefined refs | `pdfinfo master.pdf`; `master.log` grep for warning/undefined/overfull returns nothing but the benign rerun notice |
| Output dir is clean per R4 | `lint_output.py` → `OUTPUT LINT OK`, exit 0 |
| Renders legibly, bullets present | read `build/pg-1.png` and `build/pg-2.png` |

**One real finding worth flagging to the validator and to the master.** My first compile
*failed*, and the cause is an environment defect, not a mistake in my LaTeX:

    !pdfTeX error: pdflatex (file tcrm1095): Font tcrm1095 at 600 not found

`\textbullet` lives in the TS1 encoding, and TS1 Computer Modern is not shipped as Type1 on
this box — pdfTeX falls back to generating a pk bitmap with METAFONT, which fails because
`~/.TinyTeX/texmf-var` is mounted read-only. I bisected it to a three-line minimal case:

    \documentclass[11pt]{article}\begin{document}\begin{itemize}\item one\end{itemize}\end{document}

**Plain `itemize` does not compile on this machine.** So does a bare `\textbullet`. This is not
specific to `enumitem` — `enumitem` was innocent.

I fixed it in the least invasive way available: `label=$\bullet$`, which draws the bullet from
`cmsy` (a real Type1 font that is present) instead of TS1. It is visually identical and it is
confined to my own two lists. I deliberately did **not** put `\usepackage{lmodern}` or
`\usepackage[T1]{fontenc}` in `preamble.txt`, even though both also fix it (I verified both
do), because either would silently restyle the *entire* merged document for every other
problem — not my call to make from inside one fragment.

**This will bite any other worker who used a plain `itemize`,** and it will surface as a master
compile failure rather than as their bug. Worth passing upstream.

## Deliverables

- `/home/xing/project/auto_hw_complete/output/hw_20260909_1235d6/p1/answer.tex` — the fragment.
  One `\section*{Exercise 1.1 -- 1.4}` and four `\subsection*{Ex. 1.N (5 pts)} ...` in the
  assignment's own numbering. All four labels namespaced: `p1:sec:main`, `p1:sec:magic`,
  `p1:sec:segments`, `p1:sec:vonneumann`, `p1:sec:segfault`. No `\documentclass`,
  `\begin{document}` or `\usepackage` (R5 checked, and the linter agrees).
- `/home/xing/project/auto_hw_complete/output/hw_20260909_1235d6/p1/preamble.txt` — one line,
  `\usepackage{enumitem}`.
- No figures (none needed).

## Where I am least confident

1. **Whether `enumitem` is worth requiring at all.** I use it only for `nosep` and
   `leftmargin`, i.e. purely cosmetic compactness. If the master would rather not carry the
   dependency, the two lists degrade fine to plain `itemize` — *provided* the `label=$\bullet$`
   option survives, which it would not, and then the TS1 bug above returns. If a reviewer wants
   `enumitem` dropped, the right substitution is `description`, not bare `itemize`. Flagging
   because the obvious simplification is the one that breaks the build.

2. **Ex. 1.2, "list *all* segments" — where to draw the boundary.** I listed six: text, `.data`,
   BSS, heap, memory-mapped region, stack. The classic textbook answer is four or five (often
   folding `.data`/BSS together, and often omitting the mmap region entirely). I included the
   mmap region because on any real Unix it is where shared libraries actually live, and the
   brief asked for it. I did *not* list `.rodata` separately, kernel-reserved space, the
   `vdso`/`vvar` pages, or the argv/environ block above the stack — all genuinely part of a
   real address space. If the grader is working from a specific textbook figure, my list may be
   longer than expected. I judged over-inclusion to be the safer error for a "list all"
   question, but it is a judgement call.

3. **Ex. 1.3 "how are they related" is inherently interpretive.** My framing — von Neumann at
   the architectural/programming-model level, Harvard-ish and heavily parallel underneath — is
   the standard one, but a grader wanting a more historical answer (EDVAC, the 1945 draft
   report, Turing/ENIAC lineage) would find my answer light on names and dates. I gave no
   dates and named no machines. That is a deliberate cut for length, not an oversight, but it
   is the answer most exposed to a different marking scheme.

4. **Ex. 1.4 reason list is not exhaustive and cannot be.** I gave seven common causes. I left
   out several real ones — misaligned access on architectures that trap it, `alloca` overflow,
   jumping through a corrupted function pointer, mmap'd file truncated under the mapping
   (`SIGBUS` on Linux, so arguably correctly excluded). If the grader expects a specific
   canonical list, mine may not overlap exactly.

5. **Unverifiable by construction: the prose is mine, but I cannot *prove* originality.** The
   requirement is "put the answers in your own way." I wrote everything from scratch and copied
   no source, but on standard material like this, correct answers converge on similar phrasing
   and I have no way to demonstrate the negative. If the validator wants a specific passage
   reworded to be more clearly distinct, that is a cheap fix.
