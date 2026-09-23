# p1 — Ex. 2.1 submission

## What the problem asked

Draw schedule diagrams for Round-Robin (q = 1), FIFO and SJF for the task set
(arrival, execution): T1(1,10), T2(2,4), T3(3,1), T4(4,6). Ties go to the smaller index.
5 pts per diagram, 15 total.

The assignment is a markdown file, `input/hw2_instruction.md`, not a PDF — ingest
recorded it as `kind: text_document`, so there are no page PNGs and no figure files for
it, and nothing is hidden in an image channel. I read the markdown itself as ground
truth. **Line 5 of `hw2_instruction.md` matches the brief's transcription verbatim**,
including "Time quantum for Round-Robin is 1 time unit", the tie rule and
"(5pts for each diagram)". No discrepancy between brief and source; no figure is
referenced by this question.

## What I decided it needed

**code + diagram.** The question says "Draw", so three Gantt charts are the deliverable
(15 of the 15 marks are explicitly attached to them). Code because the brief forbids
eyeballing and because the RR queue is genuinely error-prone by hand; every number in
`answer.tex` comes out of the simulator. Only a small "plain" component: the conventions
paragraph, which is needed because the task set is tie-heavy and the answer is not
well defined without them.

## What I did

Wrote a discrete-time simulator (`sim.py`) implementing the three policies exactly as the
conventions are stated in `answer.tex`, with the RR ready queue modelled explicitly:
at each instant the tasks arriving at that instant are appended first, then the task
preempted at the end of the previous quantum is appended. The simulator asserts the
invariants before printing anything: t = 0 idle, exactly one idle unit, makespan 22, and
each task receiving exactly its execution time of CPU. It dumps `schedules.json`.
`mkfig.py` reads that JSON (no hand-typed blocks) and emits three vector PDFs.

I also hand-computed all three schedules independently before running the code; the code
agreed with the hand computation in every cell, which is the cross-check I would
otherwise not have.

I rendered each figure PDF to PNG and looked at it. First version had the arrival
triangle for T2 visually colliding with T1's bar, so I reduced the bar height from 0.62
to 0.50 and re-checked. I then test-compiled the fragment inside a throwaway master
document in `build/` and looked at both rendered pages.

### Environment note the master may care about

`\begin{itemize}` **does not compile on this machine with pdflatex.** The default bullet
is `\textbullet` in TS1, which needs the bitmap font `tcrm1095`; mktexpk generates it but
cannot install it because `~/.TinyTeX/texmf-var` is read-only, and pdflatex then dies with
`Font tcrm1095 at 600 not found` and produces no PDF. Reproduced with a four-line minimal
document (`build/t4.tex`). I worked around it in my own fragment by using
`\begin{itemize}[label=$\bullet$,...]` from `enumitem` (a math-mode bullet from cmsy,
which is a real Type 1 font) — verified in `build/t5.tex` and in the full test compile.
If another problem's fragment uses a bare `itemize`, the master's compile will fail the
same way; the alternative fix is to set `TEXMFVAR` to a writable directory.

## Intermediate steps and code

All paths relative to PLAYGROUND.

| file | what it does |
|---|---|
| `notes.md` | the ground-truth check and the conventions I fixed before coding |
| `sim.py` | the simulator. `python3 sim.py` prints all three timelines and tables, asserts the invariants, writes `schedules.json` |
| `schedules.json` | machine-readable timelines, Gantt blocks and per-task stats |
| `mkfig.py` | `MPLCONFIGDIR=$PWD/.mplcache ~/miniconda3/envs/py311/bin/python mkfig.py <OUTPUT>` — reads `schedules.json`, writes the three PDFs |
| `srtf_check.py` | scratch; `python3 srtf_check.py` — exists only to verify the single sentence in `answer.tex` about the preemptive variant |
| `view_{rr,fifo,sjf}.png` | the rendered figures I inspected |
| `build/` | throwaway master document for the test compile, plus the minimal files that isolate the `itemize`/TS1 failure |

Reproduce every number in the answer with `python3 sim.py`. Reproduce the figures with
the `mkfig.py` line above. Reproduce the compile with
`cd build && pdflatex master.tex` (run twice).

## Results

All from `python3 sim.py`.

Timelines (task occupying the CPU over [t, t+1), t = 0 … 21):

```
RR    -- T1 T2 T1 T3 T2 T4 T1 T2 T4 T1 T2 T4 T1 T4 T1 T4 T1 T4 T1 T1 T1
FIFO  -- T1 T1 T1 T1 T1 T1 T1 T1 T1 T1 T2 T2 T2 T2 T3 T4 T4 T4 T4 T4 T4
SJF   -- T1 T1 T1 T1 T1 T1 T1 T1 T1 T1 T3 T2 T2 T2 T2 T4 T4 T4 T4 T4 T4
```

As blocks (what the figures draw):

- RR: idle[0,1), then unit slices T1,T2,T1,T3,T2,T4,T1,T2,T4,T1,T2,T4,T1,T4,T1,T4,T1,T4, then T1[19,22).
- FIFO: idle[0,1), T1[1,11), T2[11,15), T3[15,16), T4[16,22).
- SJF: idle[0,1), T1[1,11), T3[11,12), T2[12,16), T4[16,22).

Completion / turnaround / waiting (the table in `answer.tex`):

| task | RR C/T/W | FIFO C/T/W | SJF C/T/W |
|---|---|---|---|
| T1 | 22 / 21 / 11 | 11 / 10 / 0 | 11 / 10 / 0 |
| T2 | 12 / 10 / 6 | 15 / 13 / 9 | 16 / 14 / 10 |
| T3 | 5 / 2 / 1 | 16 / 13 / 12 | 12 / 9 / 8 |
| T4 | 19 / 15 / 9 | 22 / 18 / 12 | 22 / 18 / 12 |
| avg | 12.00 / 6.75 | 13.50 / 8.25 | 12.75 / 7.50 |

Invariants that passed inside `sim.py` (assertions, not eyeballed): busy time
10+4+1+6 = 21; exactly one idle unit, at t = 0; makespan 22 for all three; no task runs
before its arrival; each task's occupancy count equals its execution time.

The one sentence about SRTF comes from `srtf_check.py`, which gives
`-- T1 T2 T3 T2 T2 T2 T4 T4 T4 T4 T4 T4 T1 T1 T1 T1 T1 T1 T1 T1 T1`, i.e. T2 preempts T1
at t = 2 and T3 preempts T2 at t = 3. (T4 at t = 4 does *not* preempt: its burst of 6
exceeds T2's remaining 3, which is why the sentence names only T2 and T3.)

Prose length: 246 words excluding the table and figure environments — under the R8
target band for a multi-part question, as a diagram question should be.

## Deliverables

- `OUTPUT/answer.tex`
- `OUTPUT/fig_p1_rr.pdf`, `OUTPUT/fig_p1_fifo.pdf`, `OUTPUT/fig_p1_sjf.pdf`
- `OUTPUT/preamble.txt` (graphicx, booktabs, float, enumitem)

`python3 framework/tools/lint_output.py <OUTPUT>` exits 0.
All labels namespaced: `p1:fig:rr`, `p1:fig:fifo`, `p1:fig:sjf`, `p1:tab:times`.
Figures referenced by bare filename.

## Where I am least confident

1. **The RR enqueue convention.** The schedule is only unique once you fix what happens
   at t = 2, 3, 4, where an arrival coincides with a quantum expiry. I enqueue the
   arriving task first, which is what the brief nominates and what the smaller-index tie
   rule is consistent with, and I state it explicitly in `answer.tex`. The opposite
   convention (preempted task first) gives a genuinely different diagram — T1 would run
   at t = 2 rather than T2. If the course used the other convention my RR diagram is
   wrong in a way no invariant catches, because the makespan and the busy time are
   identical either way. This is the single riskiest thing in the submission.
2. **Whether T3 should be labelled inside its bar.** Its block is one unit wide in every
   policy, so the inline "T3" text is suppressed and the reader relies on the row label
   on the y-axis. I judged that legible; a grader might want the text.
3. **The two-page layout.** `[H]` forces each figure in place, so figure 1 sits alone on
   page 1 with white space below it. Correct but not pretty. I left it because the
   master controls the surrounding document and may well reflow it.
4. **SJF direction.** I used non-preemptive SJF as the brief instructs. The course
   material is not visible to me, so if this course teaches "SJF" as preemptive, the SJF
   diagram would need to be the SRTF schedule that I only mention in one sentence.
