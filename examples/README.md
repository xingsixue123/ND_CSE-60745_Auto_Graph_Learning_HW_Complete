# Worked example — CSE 60745 Fall 2026, Homework 1

One complete run of the pipeline, kept as a reference: what went in, what came
out, and how little had to be said to get there.

The whole input was **a Word document, a data file, and a three-line spec.**

## Where these files originally lived

They were moved here after the run finished, so that `input/` and `output/` are
empty and ready for the next assignment. Their original locations:

| file, as it is here | where it was during the run |
|---|---|
| `specs.md` | `auto_hw_complete/specs.md` |
| `input/CSE 60745_Fall 2026_HW1.doc` | `auto_hw_complete/input/CSE 60745_Fall 2026_HW1.doc` |
| `input/graph-1.txt` | `auto_hw_complete/input/graph-1.txt` |
| `output/cse60745_20260907_d29ddd/` | `auto_hw_complete/output/cse60745_20260907_d29ddd/` |

The matching scratch space — every worker's scripts and notes, both validators'
checklists, the ingest renders, the run log — is **not** here. It stayed at
`auto_hw_complete/playground/cse60745_20260907_d29ddd/`, because it is the
trajectory rather than the deliverable.

## What went in

**`input/CSE 60745_Fall 2026_HW1.doc`** — a legacy Word file, 3 pages, five
questions worth 100 points. Two things about it matter:

- it is `.doc`, not `.pdf`, so it has to go through LibreOffice before anything
  can read it;
- **Q1's graph exists only as an embedded image.** "Create the following
  undirected graph" is unanswerable from extracted text — the text channel has a
  blank gap where the figure is. This is why `ingest.py` pulls figures out at
  native resolution and why `rules.md` R7 requires all three channels.

**`input/graph-1.txt`** — 26,377 whitespace-separated undirected edges over
26,728 nodes, in 4,104 connected components. Used by Q3, Q4 and Q5.

**`specs.md`** — the entire human-written specification, reproduced in full:

```
inputdir: `/home/xing/project/auto_hw_complete/input`, contains hw doc and graph data

outputdir: `/home/xing/project/auto_hw_complete/output`
```

That is all of it. No problem list, no hints about the figure, no instructions
about which questions belong together. Everything else — that there are five
questions, that Q2 depends on the graph built in Q1, that Q4(b) needs a figure
and Q5 does not — the master worked out by reading the assignment.

## What came out

`output/cse60745_20260907_d29ddd/`:

```
final/                     the deliverable
  main.pdf                 10 pages, cover page + all five questions
  main.tex preamble.tex    assembled source, recompilable
  p1.tex p2.tex p3.tex     the three fragments as assembled
  fig_*.pdf                four vector figures
p1/ p2/ p3/                each worker's own deliverable, before assembly
```

The master cut the assignment into three problems rather than five, on
dependency rather than numbering:

| id | questions | pts | why grouped this way |
|---|---|---|---|
| p1 | Q1 + Q2 | 30 | Q2 modifies the graph Q1 builds. Split, two workers would transcribe the figure independently and could disagree. |
| p2 | Q3 + Q4 | 40 | Q4 is explicitly "based on the graph created in Q3". |
| p3 | Q5 | 30 | Q5 also builds on Q3's graph, but inherits only a deterministic edge-list file, so there is nothing to diverge about. Kept separate so one worker did not carry 70 points and seven deliverables. |

To stop p2 and p3 disagreeing about the shared graph, the master pinned the same
reference counts (26,728 / 26,377 / 4,104) into both briefs.

## How the run went

| | |
|---|---|
| wall clock | ~80 minutes |
| cost | $19.95 |
| p1, p2, p3 | each passed its validator on **round 1** |
| master validation | round 1 PASS with three minor defects; master fixed all three; round 2 confirmed the fixes and checked the resulting page reflow for regressions |

The Q1 transcription is the part worth looking at. The drawing has vertices 5, 4
and 8 nearly collinear, with the single edge (5,8) drawn straight across the disc
of vertex 4 — so it *looks* like two edges (5,4) and (4,8). Read by eye, that
misreading is very hard to avoid; it inflates three vertex degrees and corrupts
Q1 and Q2 together. The worker resolved it by measurement rather than by
looking, confirmed the result is 3-regular (it is the Petersen graph), and then
**redrew the edge (5,8) with a slight bow** in its own figure so a grader can see
it passes behind vertex 4 rather than terminating there.

## Reproducing it

```bash
cp examples/specs.md .
cp examples/input/* input/
framework/fw run
```

The job id is a hash of the input filenames, `specs.md` and the date, so a rerun
on a different day lands in a different directory and will not overwrite this one.
