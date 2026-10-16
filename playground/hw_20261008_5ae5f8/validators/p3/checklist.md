# p3 validator checklist — Ex. 3.3-3.8 (40 pts)

## Round 1
Verdict: PASS

### Defects
None blocking or major. Five minor/cosmetic observations recorded below; none
requires a resubmission.

- [1.1] Heading level: six `\section*` per exercise render at the same visual level
  as a master-emitted problem heading | OUTPUT/answer.tex:1,27,47,71,123,153 |
  severity: minor
  Confirmed by compiling with `\section*{Problem 3...}` prepended: the exercise
  headings are typographically indistinguishable from the problem heading. The
  brief says "it starts at the section level", so this is literally compliant, and
  the worker flagged it itself (submission.md "least confident" #4). One-line fix
  to `\subsection*` if the master emits its own heading. Not failing on it.
- [1.2] Inline TikZ sketch floated to the following page in my wrapper, leaving
  ~1/4 page of whitespace at the foot of the preceding page | answer.tex:89-117 |
  severity: minor
  Caused by my added heading shifting the text; layout-dependent and will differ
  under the master's real geometry. The non-floating choice is deliberate and
  well-argued (keeps the sketch adjacent to Ex. 3.6). Cosmetic.
- [1.3] Figure shows all three in-gap frames as R=0 | answer.tex:95-96 | severity: minor
  In a real sweep some in-gap frames would have been re-referenced and show R=1.
  A mixed gap would be marginally more instructive. The prose is accurate ("releases
  any page whose R is still clear"), so this is a simplification, not an error.
- [1.4] Stale line in scratch notes: notes.md "What this needs" says the sketch gets
  "a `p3:`-namespaced label"; the shipped figure correctly carries no label, as the
  same file's "Figure decision detail" section explains | notes.md | severity: minor
  Scratch-note inconsistency only. The deliverable is correct.
- [1.5] FILO is an interpretation, not a sourced definition | answer.tex:161-165 |
  severity: minor
  "first-in last-out" -> evict most recently loaded is the standard reading, and the
  answer hedges explicitly ("as the name is used here"). Correct handling of an
  under-specified term in the assignment.

### Checks performed and their results

Question fidelity
- Read the ground-truth source `input/os_hw_3_problems.md` directly. All six
  questions in problem.md are verbatim identical to the source, including its
  idiosyncratic grammar. No brief-vs-source discrepancy.
- R7 channels: `ingest/manifest.json` classifies the source `kind: text_document`
  with no `pages` array -> no `page_*.png` and no `page_*_fig_*.*` physically exist.
  Only the text channel exists. Verified it against the original input with diff:
  identical apart from the trailing newline, exactly as the worker reported.
  No figure is referenced by any of 3.3-3.8 (Ex. 3.1 is the only figure question in
  the assignment and is not p3's).
- All six sub-answers present, in order 3.3 -> 3.8, each headed with the exercise
  number and its points. Ex. 3.7's two explicitly marked sub-questions ("which
  instruction", "why back it up") are both answered under their own bold lead-ins.
  Ex. 3.8 covers all five algorithms at 73/68/59/67/73 words - the brief's 60-70
  per algorithm, evenly weighted for 2 pts each.

Technical correctness (checked independently against standard OS references)
- 3.3 full sequence present: victim selection, M-bit test + conditional write-back,
  PTE invalidation *and* TLB shootdown, read-in, PTE reinstall, instruction restart,
  plus the faulting process blocking. Ordering matches standard textbook treatment.
- 3.4 cost/availability argument correct; LRU hardware variants (per-access counter,
  move-to-front list, n x n bit matrix) correctly stated.
- 3.5 aging arithmetic correct (shift right, insert R at the high-order end); the
  finite-width limitation and the intra-tick tie are both correctly stated.
- 3.8 NRU class numbering 0..3 over (R,M) = (0,0),(0,1),(1,0),(1,1) with R cleared
  per tick and M left alone - correct. FIFO/Belady and LRU-as-stack-algorithm -
  correct. No fabricated numbers anywhere; "8 bits" is flagged as typical.
- Cross-answer consistency holds: NFU's counter is defined identically in 3.4, 3.5
  and 3.8 (add R per tick, clear R, evict smallest, lifetime frequency, never
  forgets). Later answers reference earlier ones in prose rather than redefining.

R9 - sources opened and read past the quotation, by me
- Chalmers EDA092 "4BSD UNIX Virtual Memory" (cached PDF in the worker's playground,
  re-extracted with pdftotext): all three quotes verbatim. The slides do go on to
  the pageout-daemon goal and the lotsfree mechanism, so the worker's
  "decouples scanning from eviction / pre-builds a free pool" framing is the
  source's own, not a gloss on a fragment. The "degenerates to FIFO" step is the
  worker's inference, correctly disclosed as such in submission.md; it is standard
  clock-algorithm reasoning and is sound.
- UW-Madison CS537 notes: fetched the live page myself. All four quotes verbatim.
  Context check - the page later says "The original 68000 did neither of these and
  so paging was not possible on the 68000"; the answer uses the 68000 only as the
  PC-already-advanced example, which is the source's own use, so no contradiction.

Numbers and claims
- Re-ran the worker's `wordcount.py` on the shipped answer.tex: reproduces its
  reported table exactly (1512 total, 1.10x).
- Wrote an independent counter using a different stripping method (math content
  counted as words rather than collapsed to one token): 1530 total vs 1380 target =
  1.11x; per question 1.12/1.13/1.15/1.16/1.08/1.06x. Every item is under the 1.25x
  R8 threshold and the two methods agree within ~1%. The worker's self-report is
  honest. Em-dash density 1 per 126 words, inside R8's 1-per-70 line.

LaTeX and compliance
- R5: no \documentclass, \usepackage, \begin{document} or \end{document}. Grep
  confirmed.
- Namespacing: zero \label, zero \ref, zero \includegraphics, zero \newcommand/\def
  /\newenvironment. The fragment presents no collision surface at all - the
  strongest possible form of the requirement.
- Compiled in my own master-like wrapper (documentclass + amsmath/amssymb/graphicx/
  geometry + the two preamble.txt lines + a problem-level heading): pdflatex exit 0,
  zero overfull, zero underfull, zero undefined references or warnings.
- preamble.txt declares exactly the two non-assumed packages actually used
  (tikz for the sketch, enumitem for the 3.3 list optional argument). Pure ASCII.

Figure
- Rendered all pages at 150 dpi and looked at every one; cropped the sketch from a
  600 dpi render and upscaled it.
- Legible at printed size, labels do not overlap or clip, legend present, vector
  (TikZ) not raster.
- Geometry verified by measurement, not by eye: compiled a minimal test of the exact
  sweep arc `(205:1.95) arc (205:245:1.95)`, which renders W -> S, i.e.
  COUNTERCLOCKWISE. Under counterclockwise motion the 120 deg hand leads and the
  30 deg hand trails, so "front hand: clears R" at 120 deg and "back hand: evicts if
  R=0" at 30 deg are correctly assigned, and the three open R=0 dots at 45/75/105
  deg lie strictly inside the gap (30,120) - precisely the frames the front hand has
  cleared and the back hand has not yet reached. The figure is semantically correct.

Hygiene
- `lint_output.py` -> OUTPUT LINT OK, exit 0. OUTPUT holds only answer.tex and
  preamble.txt; no logs, no scratch, no venv.
- downloads.md present and accurate (R3): records nothing installed, plus the one
  reference PDF the harness cached, with its path and the reason it was fetched.

### Resolved since last round
N/A - first round.

### Still outstanding
Nothing substantive. [1.1]-[1.5] are cosmetic and are noted for the master's
information, not as blockers.
