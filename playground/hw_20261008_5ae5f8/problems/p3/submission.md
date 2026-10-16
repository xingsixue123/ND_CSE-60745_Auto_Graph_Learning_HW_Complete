# p3 — submission

## What the problem asked

Six separately-marked short answers from an OS course, 40 pts total, all on demand
paging and page replacement:

- **Ex. 3.3** (5) what the OS must do when all frames are in use and a page must be
  brought in from disk;
- **Ex. 3.4** (5) why use NFU over LRU;
- **Ex. 3.5** (5) why use NFU-with-aging over NFU or LRU;
- **Ex. 3.6** (5) what purpose the two-handed clock algorithm serves;
- **Ex. 3.7** (10) why the instruction must be backed up after page-fault handling,
  and which instruction that is (two explicitly marked sub-questions);
- **Ex. 3.8** (10, 2 each) describe FIFO, FILO, NRU, LRU, NFU.

**Brief vs. source — no disagreement.** The source is
`input/os_hw_3_problems.md`, plain markdown. I diffed the ingest text against the
input file and they are byte-identical apart from a trailing newline:

    diff <(sed 's/[[:space:]]*$//' input/os_hw_3_problems.md) \
         <(grep -v '^===' ingest/pages/os_hw_3_problems/alltext.txt | sed 's/[[:space:]]*$//')

The six questions quoted in `problem.md` are verbatim identical to the source,
including its idiosyncratic grammar ("In what purpose the two-handed clock algorithm
useful?") and the trailing "?" on 3.8's imperative. Nothing to report.

**R7 / figures.** The source is a text file, not a PDF: `ingest/manifest.json` gives
it `kind: text_document` with no `pages` array, so ingest produced no `page_*.png`
and no `page_*_fig_*.*` for it. Only the text channel physically exists, and I
verified it against the original input file rather than trusting it alone. I also
read the whole source, not just my six questions, to confirm that the only question
in the entire assignment referring to a figure is **Ex. 3.1** ("Explain your idea by
drawing the memory map"), which is not mine. None of 3.3–3.8 refers to a figure, so
there was nothing to go and look at. This matches the brief.

## What I decided it needed

**plain**, for all six. Nothing in the six questions asks for a number, a count, a
distribution or a measurement, so there is no `code` component; stating a computed
value here would be inventing one. Nothing says plot/draw/show/visualize, so no
diagram is *required*.

I added **one optional diagram**, which the brief explicitly sanctions for 3.6: a
small inline TikZ sketch of the clock face. It earns its place because 3.6's whole
answer turns on the *gap between the hands* being the test window, and that is a
geometric fact that a 2.4-inch circle carries better than a sentence. No diagrams on
the other five, as instructed.

Decision detail: the sketch is a **non-floating** `tikzpicture` inside
`\begin{center}`, not a `figure` float and not a separate `fig_p3_*.pdf`. A float
would be free to drift pages away from Ex. 3.6 once the master assembles the whole
assignment, and the sketch is only useful next to that text. Because it does not
float and is never cross-referenced, it carries **no `\label` at all** — so there is
nothing that could collide with another worker's labels. The fragment defines zero
labels, zero `\ref`s and zero `\includegraphics` (verified by grep), which is the
strongest possible form of the namespacing requirement.

## What I did

Wrote the six answers as prose, holding one fixed definition of each mechanism
across all six so the document says one thing rather than six. The contract I held
to (recorded in `notes.md` before writing):

- **NFU**, used identically in 3.4, 3.5 and 3.8: a per-page *software* counter; each
  clock tick the OS **adds** that page's R bit to the counter and **clears** R; evict
  the smallest counter; it measures frequency over the page's whole lifetime and
  never forgets.
- **Aging** (3.5 only): same sampling, but **shift the counter right one bit first,
  then insert R at the high-order end**, so a reference's weight halves per tick.
- 3.3 ends by restarting the faulting instruction, handing off to 3.7; 3.6's
  free-frame pool is the thing 3.3 refers to for moving write-back off the fault
  path; 3.4 and 3.5 cite LRU's per-reference cost, which 3.8 defines once.

Rather than assert the two load-bearing historical/architectural claims from memory,
I checked them against primary sources (details under **Results**).

I then compiled the fragment inside a wrapper that mimics the master (documentclass +
amsmath/amssymb/graphicx/geometry + my `preamble.txt` lines + `\input{answer}`),
rendered it, and **looked at every page and at the figure cropped and upscaled 4x**.
That caught two real figure defects, which I fixed: the legend sat on top of the
dashed ring, and the text "R=0, evictable" overlapped a frame dot. I also merged an
orphaned bold lead-in ("Why it has to be backed up.") into the paragraph that follows
it so it cannot be stranded alone at a page break.

## Intermediate steps and code

Paths relative to PLAYGROUND.

| path | what it does |
|---|---|
| `notes.md` | plan, the R7 channel reconciliation, the cross-answer consistency contract, verification results with quoted sources, figure-design decision |
| `wordcount.py` | the R8 check. Strips comments, the whole `tikzpicture`, math and control words from `answer.tex`, then counts prose words per `\section*` block against the brief's per-question targets. Run: `python3 wordcount.py <OUTPUT>/answer.tex` |
| `build/wrapper.tex` | master-like wrapper: `\documentclass`, the four assumed packages, `\input{preamble_lines}`, `\input{answer}` |
| `build/compile.log` | pdflatex transcript (exit 0, zero overfull/underfull/undefined) |
| `build/fig_crop.png` | the 3.6 figure cropped from the compiled PDF and rendered at 4x, which is what I actually inspected |
| `downloads.md` | nothing installed; records the one reference PDF the harness cached during a WebFetch |

Reproduce the compile and the inspection:

    cd build && cp <OUTPUT>/answer.tex answer.tex \
      && cp <OUTPUT>/preamble.txt preamble_lines.tex \
      && pdflatex -interaction=nonstopmode -halt-on-error wrapper.tex

## Results

No answer contains a computed numeric result — this problem has none to compute, and
I have not stated any number that is not a definition (e.g. "8 bits" as the typical
aging counter width, which is stated as typical, not measured).

The two claims I verified rather than asserted:

1. **Two-handed clock (Ex. 3.6)** — confirmed against the Chalmers EDA092 slides
   *"4BSD UNIX Virtual Memory"*
   (`https://www.cse.chalmers.se/edu/year/2012/course/EDA092/SLIDES/8-bsd_virtual_memory.pdf`,
   text read with `pdftotext`):
   - *"If a large main memory is used, the clock algorithm with one hand do not work
     very well because the time to scan all page frames is too large."*
   - *"The first clock hand is used to reset the reference bit, and the second clock
     hand releases pages with the referenced bit still reset. (they have not been
     referenced in the time span between the scan of the first and second clock
     hands)"*
   - *"The goal for the pageout daemon is to assure that there are a sufficient
     number of free frames available at all times"* — woken every 250 ms, sweeps only
     far enough to restore `lotsfree` free frames.

   **R9 check:** I read past each quote. The slides do not stop at "two hands exist";
   they go on to give the free-frame-pool purpose and the `lotsfree` mechanism, which
   is the second half of my answer. So the "decouples scanning from eviction / builds
   a free pool in advance" framing is the source's own, not my gloss on a fragment.

2. **Instruction restart (Ex. 3.7)** — confirmed against UW-Madison CS537 notes
   (`https://pages.cs.wisc.edu/~solomon/cs537/html/paging2.html`): restart so as to
   *"re-try the offending instruction"*; on the 68000 *"the PC will be pointing at the
   word immediate following the part of the instruction that caused the fault"*, hence
   *"How can the OS figure out where the instruction started, so that it can back the
   PC up to retry?"*; autoincrement/autodecrement modes change index registers as a
   side effect and after a mid-instruction fault *"it may be difficult to figure out
   which registers have been modified so that they can be restored"*; and designers
   *"either ... undo the effects of the instruction before faulting, or they dump
   enough information into registers somewhere that the OS can undo them."*

**Length (R8), measured not eyeballed** — `python3 wordcount.py <OUTPUT>/answer.tex`:

| ex | words | target | ratio |
|---|---|---|---|
| 3.3 | 211 | 190 | 1.11x |
| 3.4 | 210 | 190 | 1.11x |
| 3.5 | 215 | 190 | 1.13x |
| 3.6 | 221 | 190 | 1.16x |
| 3.7 | 313 | 290 | 1.08x |
| 3.8 | 342 | 330 | 1.04x |
| **total** | **1512** | **1380** | **1.10x** |

Every question is under the 1.25x defect threshold. First draft came in at 1586
with 3.6 at 1.31x (an R8 defect); I trimmed all six. Em-dash density is one per
126 words, well inside R8's one-per-70 warning line.

**Checks run:** `lint_output.py` → `OUTPUT LINT OK`. `pdflatex` → exit 0, 3 pages,
zero overfull/underfull/undefined. Fragment contains no `\documentclass`,
`\begin{document}`, `\end{document}` or `\usepackage` (R5, grep-verified). Macros used
are `\text` (amsmath), `\times` (base), tikz's `\draw/\node/\foreach`, and
`enumerate`'s optional argument (enumitem) — both non-standard packages are declared
in `preamble.txt`.

## Deliverables

- `OUTPUT/answer.tex` — the fragment: six `\section*` answers in order 3.3 → 3.8,
  each headed with the exercise number, its points and a short descriptor, plus the
  inline TikZ sketch inside Ex. 3.6.
- `OUTPUT/preamble.txt` — `\usepackage{tikz}` (the 3.6 sketch) and
  `\usepackage{enumitem}` (the compact numbered list in 3.3).
- No `fig_p3_*.pdf`: the only diagram is inline TikZ, by the brief's own direction.

## Where I am least confident

1. **The "degenerates to FIFO" step in 3.6 is my inference, not a quote.** The
   Chalmers source states the *premise* (on large memory a single hand's revolution
   takes too long) but does not spell out the consequence I draw from it — that the
   hand then finds R=1 almost everywhere, clears bits and sweeps on, so the victim is
   effectively chosen by position in the frame list. This is standard textbook
   reasoning about the clock algorithm and I believe it is right, but it is the one
   sentence in 3.6 that rests on me rather than on the source. The same goes for the
   symmetric "driving it faster makes the choice near-random" clause.

2. **"FILO" is not a standard algorithm name** and the assignment supplies no
   definition beyond expanding it to "first-in last-out". I read that as: first in,
   last out ⇒ the most recently loaded page is evicted first ⇒ a stack discipline, and
   I say so explicitly ("as the name is used here") before arguing it is a poor
   policy. If the course intended something else by the name, that paragraph is aimed
   at the wrong target. This is the single most likely place for a mismatch with the
   marker's expectation, and it is worth 2 points.

3. **Belady's anomaly is the one claim in 3.8 I did not chase a source for.** FIFO
   suffers it; LRU is a stack algorithm and does not (Belady/Nelson/Shedler 1969;
   Mattson et al. 1970). I am confident, but it is asserted from textbook knowledge
   rather than re-verified, unlike the 3.6 and 3.7 claims.

4. **Heading level.** I used `\section*` per exercise, reading the brief's "it starts
   at the section level" plus "each under its own heading" literally, and unnumbered
   so nothing conflicts with another problem's numbering. If the master emits its own
   problem-level heading, six sections may sit one level lower than its siblings. That
   is a one-line change to `\subsection*` if the validator prefers it.

5. **Word counts are from my own stripper.** `wordcount.py` counts `$...$` as a single
   token and drops the figure entirely, so its numbers are a reasonable proxy for
   prose length but not identical to what another counter would produce. The margin
   to the 1.25x threshold is comfortable enough that I do not think the method
   changes the verdict, but the exact figures depend on it.
