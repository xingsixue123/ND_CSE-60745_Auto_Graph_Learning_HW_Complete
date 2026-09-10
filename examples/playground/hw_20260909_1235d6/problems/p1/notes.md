# p1 — notes

## Source verification (R7 / brief-vs-page reconciliation)

The assignment is **not a PDF**. It is `/home/xing/project/auto_hw_complete/input/hw_questions.md`,
41 lines. I read the file directly (the authoritative channel for a text source).

Cross-check on "are there figures I am missing":
`ingest/manifest.json` lists exactly one rendered document, `PaperList.xlsx` (6 pages).
Every page reports `n_images: 0` and `"figures": []`. `hw_questions.md` is not rendered at
all because it is already text. So there is no image channel to reconcile for this problem —
the three-channel rule is satisfied vacuously, and I am saying so rather than pretending I
looked at a page PNG.

Brief vs. source: **no disagreement.** Ex 1.1/1.2/1.3/1.4 in `problem.md` match lines
5 / 9 / 13 / 17 of `hw_questions.md` word for word.

The stray backslashes in Ex 1.4 (`\segmentation fault (core dumped)."`) are LaTeX-to-markdown
corruption of opening double quotes (`` `` `` → `\`). Confirmed by shape: every backslash sits
where an opening quote belongs and every closing quote survived. I render them as proper
quotation marks and do not reproduce the backslashes.

## What this problem needs

**plain** only. No code, no diagram, no computation. Nothing in Ex 1.1–1.4 asks for a number,
a plot, or anything to be drawn — they are four conceptual OS questions. So there is nothing
to compute and no figure to produce, and adding either would be padding.

## Constraints that shape the writing

1. Assignment line 1: "you cannot just copy the answers, put the answers in your own way."
   This is a grading requirement. Everything is written from scratch in my own prose; no text
   lifted from man pages, Wikipedia, or a textbook.
2. User spec: "just few sentences sufficient for answering question 1.1-1.8". Target ~3–6
   sentences per question. 1.2 and 1.4 are explicitly *list* questions, so those get a short
   labelled list plus a sentence each — still compact.

## Part checklist (what a grader ticks off)

- 1.1 — (a) role of the magic number, (b) where it is stored. Both must be visible.
- 1.2 — list the segments AND explain each. Include text, initialized data, BSS, heap,
  mmap region, stack. Say which grow and in which direction.
- 1.3 — (a) what a von Neumann machine is, (b) **how it relates to today's machines**.
  The second half is where the marks hide; do not answer only the first half.
- 1.4 — four parts: (a) what the message means, (b) possible reasons (several),
  (c) what "segmentation" means here, (d) what "core" means here.

## Output plan

`OUTPUT/answer.tex` — fragment, `\section*` + four `\subsection*{Ex. 1.N (5 pts)}`.
All labels namespaced `p1:`. `enumitem` in `preamble.txt` for compact lists (verified
installed per env.md). No figures, so no `fig_p1_*.pdf`.
