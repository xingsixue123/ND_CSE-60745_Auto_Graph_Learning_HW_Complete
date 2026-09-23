# p1 notes

## Ground truth check
Read `/home/xing/project/auto_hw_complete/input/hw2_instruction.md` directly (it is a
markdown file; ingest produced no PNG/figure channels — `manifest.json` says
`kind: text_document`). Line 5 of the markdown is Ex. 2.1 and it matches the brief's
transcription **verbatim**, word for word, including "(5pts for each diagram)".
No figure is referenced by this question, so there is nothing in an image channel to read.

## What this needs
**code + diagram** (no real "plain" derivation beyond stating conventions).
- code: a simulator for RR(q=1), FIFO, SJF-nonpreemptive over
  T1(1,10) T2(2,4) T3(3,1) T4(4,6); must emit per-time-unit CPU occupancy and
  completion/turnaround/waiting per task.
- diagram: three Gantt charts, vector PDF, `fig_p1_{rr,fifo,sjf}.pdf`.

## Conventions fixed before coding
- Time axis starts at 0; [0,1) is idle (first arrival is at t=1). Drawn as an idle band.
- A task arriving at time a is runnable at instant a.
- FIFO: non-preemptive, dispatch in arrival order.
- SJF: non-preemptive, pick smallest *total* execution time among arrived-and-unfinished;
  tie -> smaller index.
- RR q=1: at an instant where a task arrives *and* the running task is preempted, the
  **arriving task is enqueued first**, then the preempted task goes to the tail.
- Tie in queue construction -> smaller index first.

## Sanity invariants
- busy time = 10+4+1+6 = 21; 1 idle unit at the front; every policy ends at t = 22.
- sum over the occupancy timeline of each task's units = its execution time.

## Plan
1. `sim.py` — simulator, prints timelines + tables, asserts the invariants. JSON dump.
2. `mkfig.py` — matplotlib (py311 env) -> three vector PDFs straight into OUTPUT.
3. Render each PDF to PNG and *look* at it.
4. Write `answer.tex` (short: conventions, 3 figures, one timing table, 1-2 sentences).
