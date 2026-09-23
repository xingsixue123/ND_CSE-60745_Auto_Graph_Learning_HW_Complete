# p1 — worker validator checklist

## Round 1
Verdict: PASS

### What I checked and how

**Ground truth (R7).** The assignment is `input/hw2_instruction.md`, a markdown file;
`ingest/manifest.json` records `kind: text_document`, so there is genuinely no PNG and no
figure channel — the text channel is the only channel, and there is nothing to reconcile
against. I read line 5 of the markdown directly. It matches the brief's transcription
**verbatim**, including "Time quantum for Round-Robin is 1 time unit", the smaller-index
tie rule and "(5pts for each diagram)". Ex. 2.1 is a single-part question; Ex. 2.2 on
line 9 is a different problem. No figure is referenced. The worker's ground-truth claim
in `notes.md` and `submission.md` is accurate.

**Numbers — recomputed independently, twice.** I hand-derived all three schedules and the
SRTF variant before running anything, then wrote my own RR simulator
(`rerun/indep.py`, a `deque` event loop structured differently from the worker's
`sim.py`), then re-ran the worker's `sim.py` from my own directory. All three agree
cell-for-cell:

    RR    -- T1 T2 T1 T3 T2 T4 T1 T2 T4 T1 T2 T4 T1 T4 T1 T4 T1 T4 T1 T1 T1
    FIFO  -- T1 T1 T1 T1 T1 T1 T1 T1 T1 T1 T2 T2 T2 T2 T3 T4 T4 T4 T4 T4 T4
    SJF   -- T1 T1 T1 T1 T1 T1 T1 T1 T1 T1 T3 T2 T2 T2 T2 T4 T4 T4 T4 T4 T4

Every C/T/W cell in Table 1 of `answer.tex` matches `sim.py` output and my own
derivation. Averages: RR 12.00/6.75, FIFO 13.50/8.25, SJF 12.75/7.50 — all confirmed by
arithmetic (48/4, 27/4, 54/4, 33/4, 51/4, 30/4). Invariants hold: busy = 21, exactly one
idle unit at t=0, makespan 22 for all three, per-task occupancy equals burst. No number
appears in `answer.tex` that does not come out of a script.

**SRTF sentence.** `srtf_check.py` gives
`-- T1 T2 T3 T2 T2 T2 T4 T4 T4 T4 T4 T4 T1 T1 T1 T1 T1 T1 T1 T1 T1`, which I reproduced by
hand. T2 does preempt T1 at t=2 and T3 does preempt T2 at t=3, so the single sentence in
`answer.tex` is correct and correctly scoped (T4 at t=4 does not preempt: burst 6 >
T2's remaining 3).

**RR convention — the worker's self-flagged risk.** I ran both conventions.
Arrivals-first gives the shipped schedule; preempted-first gives
`-- T1 T1 T2 T1 T3 T2 T4 ...` with C = 22/13/6/20. The two genuinely differ and no
invariant separates them. The worker used the convention the brief explicitly nominated
and states it in one line in `answer.tex` ("the arriving task is enqueued first and the
preempted task then joins the tail of the ready queue"), which is what the brief asked
for and is enough for a grader to reproduce the queue. Not a defect.

**Deliverable type.** Needed code + diagram; both present. Three vector PDFs, all
generated from `schedules.json` rather than hand-typed. I re-ran
`mkfig.py` into my own directory: the regenerated PDFs differ from the shipped ones in
**exactly 4 bytes each**, the `/CreationDate` timestamp. The figures are bit-reproducible
from the simulator output — no hand editing anywhere.

**Figures actually read.** Rendered all three to PNG at 170 dpi and looked at them, then
looked at them again at document scale in the test compile. Each is 432 x 169.2 pt =
6.0 in wide (inside the 3–6 in standard), one row per task plus a labelled "CPU idle"
row, integer ticks 0–22 covering the whole makespan, `[0,1)` drawn as a hatched idle band
rather than cropped, arrival instants marked with triangles and dotted drop-lines,
legend present, no title. `pdfimages -list` reports **0 embedded images** in all three —
genuinely vector, not a rasterized PNG. I checked each drawn bar against the timeline:
all 20 RR blocks, and the FIFO and SJF blocks, are in the right places. No overlapping or
clipped text; the arrival markers sit clear of the bars above them (triangle at row
centre +0.55, bar top edge at +0.25).

**LaTeX and R5.** `grep` for `documentclass|usepackage|begin{document}|end{document}` and
for absolute paths in `answer.tex` returns nothing. Every label is namespaced
(`p1:fig:rr`, `p1:fig:fifo`, `p1:fig:sjf`, `p1:tab:times`), every figure filename is
namespaced and referenced by bare filename. I built a minimal wrapper
(`compile/master.tex`) with the four `preamble.txt` packages and compiled with
`pdflatex -halt-on-error`: **exit 0, 2 pages, zero Overfull/Underfull/undefined
warnings**, and the 12-column table renders correctly. All four declared packages are
actually used (graphicx, booktabs, float, enumitem).

**The `itemize` environment note.** The worker claims a bare `\begin{itemize}` cannot
compile here. I reproduced it independently with a four-line document:
`!pdfTeX error: pdflatex (file tcrm1000): Font tcrm1000 at 600 not found`, no PDF
produced. The claim is true and the `enumitem` `label=$\bullet$` workaround is justified,
not a stylistic quirk. This is useful information for the master and the submission
report flags it.

**R8 length.** My own count of the prose in `answer.tex`, excluding the figure and table
environments, is **219 words** (the worker reported 246 — either count is comfortably
inside the band for a 15-point question with three sub-deliverables). No enumeration
padding, no self-summary, no "it is worth noting". 3 em-dashes in 219 words. Under
target, correctly so for a draw-this question.

**R9.** No external source is quoted or characterised anywhere in the answer, so R9 has
nothing to bite on.

**Housekeeping.** `python3 framework/tools/lint_output.py output/hw_20260921_077701/p1`
exits 0; OUTPUT contains only `answer.tex`, `preamble.txt` and the three `fig_p1_*.pdf`.
`downloads.md` exists and records `(nothing installed)` with a correct explanation of the
`MPLCONFIGDIR` cache redirect, which is not an install.

### Defects
None blocking or major.

Two cosmetic observations, recorded and **not** requiring a fix:

- [1.1] In Table 1 the `average` row leaves the three $C$ columns empty rather than
  printing `--`. A reader scanning the row could take a beat to see that 12.00 sits under
  $T$, not $C$. | `OUTPUT/answer.tex:51` | severity: minor
- [1.2] $T_3$'s one-unit bar carries no inline "T3" text in any of the three figures (the
  `e - s >= 2` guard in `mkfig.py:45` suppresses it), so the reader relies on the y-axis
  row label. The row labels are legible at document scale, so this is readable as shipped.
  | `mkfig.py:45` / all three figures | severity: minor

### Resolved since last round
n/a — first round.

### Still outstanding
Nothing substantive. Items 1.1 and 1.2 are cosmetic and do not justify another round.
