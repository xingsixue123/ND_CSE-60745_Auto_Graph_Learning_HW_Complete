# p1 — Ex. 3.1 (10 pts) — submission

## What the problem asked

> Ex. 3.1 | (10pts) The CPU (most of them) assumes that programs are running from
> address 0 and the address space of the programs are contiguous. MMU enable the CPU
> make such an assumption. Consider a memory management for a system that only allows
> one application program to be loaded in the main memory and run. This means that at
> any given time, only the OS and one application program are loaded in the main
> memory. If we want to support the CPU's assumption without an MMU, how would you
> load the program and OS in the main memory? Explain your idea by drawing the memory
> map.

**Brief vs. assignment page: no disagreement.** The source is a plain markdown file,
not a PDF. `ingest/manifest.json` records it as `kind: "text_document"` with no `pages`
array, so ingest produced no page PNGs and no extracted figure files — the three R7
channels collapse to the single text channel here, and there is nothing else to
cross-check against. I verified the ingest copy is byte-identical to the original:

    diff input/os_hw_3_problems.md ingest/pages/os_hw_3_problems/alltext.txt   # identical

and read the brief's transcription against that text word by word, including the curly
apostrophe in "CPU's". It matches exactly. **There is no figure in the assignment**;
the memory map is one I draw.

## What I decided it needed

- **plain** — the design decision and its justification carry most of the marks.
- **diagram** — **required**. "Explain your idea by drawing the memory map." Drawn with
  TikZ inline in `answer.tex` (the brief's preferred option), so nothing external ships.
- **code** — **none, deliberately**. There is nothing to compute: no data, no counts, no
  numbers derived from anything. The hex addresses in the figure are an illustrative
  instance I chose (64 MiB of RAM, OS in the top 8 MiB), not a computed result. Their
  internal consistency is the only arithmetic involved and I checked it by hand (below).

## What I did

Reasoned the constraint through and committed to a layout. Without an MMU there is no
translation stage, so the address the CPU emits *is* the physical address; the program is
linked to start at 0 over a contiguous range, so physical 0 and the bytes above it must
belong to the application. Address 0 has one owner, so the OS goes at the **high end of
RAM**, growing down from the physical top, and the application is loaded verbatim at 0,
growing up (text, data+bss, heap ↑, gap, stack ↓). The program owns all of `[0, F)` where
`F` is the bottom of the OS, so both CPU assumptions are satisfied by construction and
the loader does no relocation at all.

I then addressed the two things the brief asked me not to dodge:

1. **The trap/interrupt vector table.** Most CPUs fetch vectors from fixed *low*
   addresses, which collides with giving 0 to the program. I require a CPU with a
   **vector base register** (68010 VBR, ARM VBAR, RISC-V `mtvec`) and set it to `F`, so
   the table lives inside the OS region. That register is read only when an exception is
   dispatched and does nothing to ordinary loads and stores, so it is not an MMU. I also
   state plainly the case where this fails: a CPU that hard-wires its vectors at 0 cannot
   honour the assumption, the vectors keep the low addresses, and the program must be
   relocated at load time. The reset vector is called out as the one address that cannot
   move in principle (served from boot ROM).
2. **The boundary.** No MMU means no per-access permission check, so I allow myself one
   **fence (limit) register** holding `F` and say so explicitly as a design choice. I
   draw the line the brief asked about: a comparison adds nothing to the address, so it
   is not translation, whereas a *base* register that is added to every address is where
   an MMU begins.

Hardware claims I asserted and checked against what I know of each architecture before
writing them: 68000 vector table `0x000`–`0x3FF` (256 × 4 B = 1 KiB); x86 real-mode IVT
`0x00000`–`0x003FF` (256 × 4 B); ARM low vectors at 0; VBR introduced on the 68010;
VBAR on ARM; `mtvec` on RISC-V. These are stated as architecture facts, not quoted from
any source in the assignment, so R9 has nothing to bite on — there is no source text in
this problem beyond the one-paragraph question itself, which I quote in full above.

## Intermediate steps and code

No computation was required, so there is no result-producing script. The files below are
build/verification scaffolding only, all inside PLAYGROUND:

- `notes.md` — the plan and the design decision, written before drafting.
- `build/answer.tex` — working copy of the fragment (identical to the delivered one).
- `build/main.tex` — test wrapper. Reproduce the compile with:
  `cd build && pdflatex -interaction=nonstopmode main.tex` (run twice for `\ref`).
- `build/libtest.tex` — one-off check that `\usetikzlibrary{decorations.pathreplacing}`
  loads from the document body rather than a preamble (it does; exit 0). This matters
  because R5 restricts `preamble.txt` to `\usepackage{...}` lines, so the library has to
  be pulled in from inside the fragment.
- `build/qg-1.png`, `build/qg-2.png` — 150 dpi renders of the final draft. **I looked at
  both.** The first render (`build/pg-1.png`, kept for comparison) had the words "vector
  table" overprinted by the thick fence rule; I grew that band from 0.7 cm to 1.0 cm and
  re-rendered to confirm the fix.
- `verify/master.tex` — final check that the **delivered** `answer.tex` compiles with
  *only* amsmath/amssymb/graphicx/geometry plus the two lines in the delivered
  `preamble.txt`, i.e. that the fragment declares everything it needs. Reproduce:
  `cd verify && pdflatex -interaction=nonstopmode master.tex` (twice). Exit 0, 2 pages,
  no overfull boxes, no undefined references.
- `downloads.md` — `- (nothing installed)`. Nothing was downloaded or installed.

## Results

No claim in `answer.tex` is a computed value. The only numbers are the illustrative
addresses in the figure, which I chose and verified for internal consistency by hand:

| quantity | value in figure | check |
|---|---|---|
| RAM size | 64 MiB = `0x0400_0000` | — (chosen) |
| physical top byte | `0x03FF_FFFF` | `0x0400_0000 − 1` ✓ |
| OS size | 8 MiB = `0x0080_0000` | — (chosen) |
| `F` = bottom of OS | `0x0380_0000` | `0x0400_0000 − 0x0080_0000` ✓ |
| top of program region | `0x037F_FFFF` | `F − 1` ✓ |
| program region | `[0x0000_0000, 0x0380_0000)` | contiguous, contains 0 ✓ |

Prose length: **353 words** excluding the figure and its caption (measured by
`build/`-side script shown in the transcript; re-measurable by stripping the `figure`
environment and counting). R8's table gives ~190 words for a 5-pointer and ~550 for a
10-point paper summary; this is a 10-point design question whose answer is carried partly
by a required figure, so I targeted ~320 and landed at 353. The first draft was 422 and
I cut it. There are no em-dashes in the prose (the only `---` in the file is the one in
the section heading; the rest are comment separators inside the TikZ source).

## Deliverables

- `OUTPUT/answer.tex` — the fragment. `\section*` heading, four short paragraphs, TikZ
  memory map inline. No `\documentclass`, `\usepackage`, or `document` environment
  (checked by grep). Single label `\label{p1:fig:memmap}`, namespaced.
- `OUTPUT/preamble.txt` — `\usepackage{tikz}` and `\usepackage{float}` (for `[H]`).
- No figure files: the map is inline TikZ, so there is no `fig_p1_*.pdf` to ship.
- `python3 framework/tools/lint_output.py <OUTPUT>` → `OUTPUT LINT OK`, exit 0.

## Where I am least confident

1. **The caption.** The shared "Diagram standards" say a figure should carry *no* caption
   because the master adds one. That rule is written for shipped `fig_*.pdf` files the
   master `\includegraphics` itself; my map is inline TikZ, which the master cannot
   caption, and the prose references it by number. So I wrote a caption and a label. If
   the validator reads the rule as absolute, deleting `\caption{...}` and rewording
   "(Figure~\ref{p1:fig:memmap})" to "below" is a two-line change. I flag it rather than
   leave it silently decided.
2. **`\usetikzlibrary` in the body.** `preamble.txt` may only contain `\usepackage` lines,
   so the brace decoration library is loaded from inside `answer.tex`, just above the
   float. I tested that this works (`build/libtest.tex`, exit 0) and the delivered
   fragment compiles clean, but it is unusual placement and depends on the master not
   doing something exotic with the fragment. If that is judged too fragile, the two
   braces can be replaced with plain ticked lines and the dependency disappears entirely.
3. **`\section*` vs `\section`.** I used starred so the master's numbering does not
   produce "1 Ex. 3.1". If the master wants numbered sections this is a one-character fix.
4. **How hard to lean on the vector base register.** This is the part of the answer with
   real room for disagreement. I treat VBR/VBAR/`mtvec` as "not an MMU" because it does no
   translation of ordinary accesses. A grader could instead expect the simpler textbook
   answer — OS high, program at 0, vectors ignored entirely — or could want the vectors
   left at 0 with the program starting just above them. I argue for the first and name
   the second as the fallback when the hardware forces it; I do not think the third
   satisfies the question, since it breaks the "starts at 0" assumption outright. The
   grader's model answer may simply not go into this at all, in which case my answer is
   a superset rather than a mismatch.
5. **Length.** 353 words is above the ~320 I set myself. I believe each paragraph earns
   its place (constraint, layout, vectors, protection — the last two were explicitly
   demanded by the brief), but if the validator counts against a stricter 10-point target
   the vector paragraph is where I would cut, specifically the three-architecture list.
