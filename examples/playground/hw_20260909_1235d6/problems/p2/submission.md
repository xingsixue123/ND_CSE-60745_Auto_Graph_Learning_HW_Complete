# p2 — submission

## What the problem asked

Four short-answer OS concept questions, 5 pts each, from
`/home/xing/project/auto_hw_complete/input/hw_questions.md` (lines 21, 25, 29, 33):

- **Ex. 1.5** — Why can't a compiler know where/how its binary will be loaded? And what
  assumptions about where/how does it make instead? (Two halves; half the marks are in
  the second.)
- **Ex. 1.6** — What happens on a double-click, or a typed command? All the steps in the
  OS until the application appears on screen.
- **Ex. 1.7** — Finding the physical address from a virtual address under contiguous
  memory allocation.
- **Ex. 1.8** — What is the round-robin scheduler?

**Brief vs. source: no disagreement.** I read `hw_questions.md` in full myself. The
master's transcription of all four questions is verbatim correct.

On the figure question (R7): the assignment is a **markdown file, not a PDF**, so the
three-channel reconciliation has nothing to apply to for my questions. I did not take the
brief's word that there are no figures — I checked `ingest/manifest.json` directly. It
contains exactly one entry, `PaperList.xlsx`, rendered to 6 pages, and every page reports
`n_images: 0` and `"figures": []`. (Those pages do report nonzero `n_vector_drawings`,
51/19/51/19/13/8, but that is spreadsheet cell ruling, and `PaperList.xlsx` belongs to
Ex. 1.9 anyway, not to me.) There is no figure content anywhere in my problem.

Also noted, and deliberately **not** acted on because it is outside my range: line 17
(Ex. 1.4) has mangled opening quotes (`\segmentation fault (core dumped)."`) and the final
exercise is numbered `Ex. 1.0` where `Ex. 1.10` was clearly meant. Those belong to other
workers; I mention them only so the master sees they were spotted.

## What I decided it needed

**plain** — prose only. No code, no diagram.

Every one of the four asks for conceptual explanation. None uses "plot", "draw", "show"
or "illustrate"; none asks for a number, count, distribution or ranking. The single piece
of arithmetic is the worked base/limit example in Ex. 1.7 ($14000 + 346 = 14346$), which
exists to *demonstrate the translation procedure* — writing a script to add two integers
would have been theatre rather than verification, so I did it inline where a grader can
check it by eye. I want to be explicit about this rather than let it look like a skipped
step: **no code was run to produce any number in this answer, because no question asked
for a computed one.**

Two further constraints I treated as binding:
- Line 1 of the assignment says "you cannot just copy the answers, put the answers in
  your own way" — a **grading requirement**, so the prose is written from understanding,
  not lifted phrasing.
- The user spec says "just few sentences sufficient for answering question 1.1-1.8", so I
  held to ~3–6 sentences each, with Ex. 1.6 as a one-line-per-step numbered list since it
  explicitly asks for "all the steps".

## What I did

Wrote the four answers directly, one `\subsection*` each, keeping the assignment's exact
numbering. I worked from the coverage checklist in `notes.md` so that each half-mark item
a grader would tick is actually present: both halves of 1.5 (the *why not* and the
*assumptions*, plus the compile-/load-/execution-time binding trichotomy); the full
fork → exec → magic-number → address-space → dynamic-linker → PCB → dispatch → draw chain
in 1.6, ending on the observation that double-click and typed command differ *only* in how
the argument vector is assembled (which is the point of the question being asked twice);
the explicit **check-then-add** ordering plus a worked example and a trap case in 1.7; and
definition, mechanism, quantum trade-off, virtue and vice in 1.8.

Then I compile-tested the fragment and read the rendered pages back at 200 dpi.

## Intermediate steps and code

No result-producing scripts — there are no computed results. What exists in PLAYGROUND:

- `notes.md` — source verification, the plain/code/diagram decision and its reasoning,
  and the per-question grader coverage checklist I wrote against.
- `build/test.tex` — a throwaway wrapper (`\documentclass` + `amsmath` + `enumitem`) that
  `\input`s the real `answer.tex` from OUTPUT, to prove the fragment compiles in the
  shape the master will use it. Reproduce with:
  `cd build && pdflatex -interaction=nonstopmode -halt-on-error test.tex`
- `build/` also holds the render/crop artifacts (`hi-2.png`, `crop_eq.png`, `c1a.png`,
  `c1b.png`, `c2b.png`) I used to actually look at the output. All scratch; none of it is
  in OUTPUT.

Nothing was installed; `downloads.md` records `(nothing installed)`.

## Results

There are no computed values in `answer.tex`. The only numbers are the illustrative
worked example in Ex. 1.7, chosen (per the brief's suggestion) as base $=14000$,
limit $=3000$:

- virtual $346$: $346 < 3000$, so physical $= 14000 + 346 = 14346$ — arithmetic verified
  by inspection.
- virtual $3200$: $3200 \ge 3000$, so it traps. Correct by the stated rule.

Verification results that *are* real:

- **Compile:** clean. `test.pdf`, 2 pages, exit 0, **no warnings and no over/underfull
  boxes** (`grep -i "warning\|overfull\|underfull\|error" test.log` returns nothing after
  the label-rerun warning is resolved by the second pass).
- **Lint:** `python3 framework/tools/lint_output.py output/hw_20260909_1235d6/p2` →
  `OUTPUT LINT OK`, exit 0.
- **R5 check:** `grep` for `documentclass|usepackage|begin{document}|end{document}` in
  `answer.tex` returns nothing. The one label is `p2:eq:reloc`, namespaced.
- **Visual:** rendered all pages at 200 dpi, cropped and upscaled 1.5x LANCZOS, and read
  all four sections back. The `cases` equation, the worked example, and the numbered list
  all set correctly and legibly.

**One real problem I hit and fixed, worth flagging.** The first compile *failed outright*
(`Font tctt1095 at 600 not found`, no PDF produced). Cause: I had written
`\texttt{\$PATH}`, and in current LaTeX `\$` inside a typewriter font resolves to the TS1
text-companion glyph, whose font is not present as Type1 in this TinyTeX and cannot be
generated because `~/.TinyTeX` is read-only (per env.md). I bisected it to that exact
token by probing each `\texttt{...}` in isolation. I fixed it by dropping the sigil —
"the directories listed in `PATH`" — rather than by adding `\usepackage[T1]{fontenc}` to
`preamble.txt`, because `preamble.txt` is merged into the *master* document and silently
changing the whole assignment's font encoding to fix my one character would be an
inappropriate side effect on the other workers' fragments. Flagging this because any other
worker who writes a `$` inside `\texttt` will hit the identical hard failure.

## Deliverables

- `OUTPUT/answer.tex` — the fragment; four `\subsection*`s, Ex. 1.5 through Ex. 1.8.
- `OUTPUT/preamble.txt` — `\usepackage{amsmath}` and `\usepackage{enumitem}`.
- No figures (none required).

## Where I am least confident

1. **Length calibration is a genuine judgement call and I may have overshot.** The spec
   says "just few sentences", but the brief also demands specific content that is hard to
   fit in three sentences — 1.5 has two halves plus the binding trichotomy, and 1.6 says
   "describe *all* the steps". Ex. 1.5 ran to two substantial paragraphs and Ex. 1.6 to
   eleven list items. I judged that the brief's explicit coverage list outranks brevity
   since that is where the marks are, but if the validator reads "few sentences" strictly,
   1.5 and 1.6 are the two to cut, and they can be cut without losing a ticked item.
2. **Ex. 1.7 is a one-line question and I chose to interpret it generously.** "Finding the
   physical address from a virtual address in a contiguous memory allocation scheme" is
   not phrased as a question at all. I read it as "demonstrate the procedure" and gave the
   rule, the bounds check and a worked example. If it was meant as a bare "state the
   formula", my answer is longer than needed — but I think erring toward demonstrating is
   right for a question phrased as "*finding*".
3. **Step granularity in 1.6 is arguable.** Where exactly one step ends and the next
   begins (e.g. I split "build the address space" from "do it via mmap") is a
   presentation choice, not a fact. A grader with a different step list would still find
   every mechanism present, but the count would differ.
4. **The ordering claim in 1.6 step 7 is the mechanism I'd most want a second eye on.**
   I say the dynamic linker runs *before* `main()` and performs relocations, which is
   correct for ELF/`ld.so`, but I stated it in general terms across ELF/PE/Mach-O, whose
   details differ. The general shape holds; the specifics vary by platform.
5. **`\label{p2:eq:reloc}` is defined but never `\ref`'d.** Harmless, and the brief
   suggested that exact label, so I kept it — but it does mean Ex. 1.7 carries a numbered
   equation that nothing points at. Trivially removable if the master would rather it be
   unnumbered.
