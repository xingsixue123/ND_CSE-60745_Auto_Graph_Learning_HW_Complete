# Worked example — CSE 60321 Spring 2026, Homework 2 (with a deliberate skip)

The second test of the pipeline, on a different course and a different kind of
question: no data files, no graphs, no code to speak of — analytical cache and
pipeline arithmetic, where every answer is a number that is either right or wrong.

This run also exercises something the first one did not: **the user asked for a
problem to be skipped**, and both levels of validator had to treat that as
compliance to check rather than a gap to flag.

## Where these files originally lived

Moved here after the run so `input/`, `output/` and `playground/` are empty for the
next assignment:

| file, as it is here | where it was during the run |
|---|---|
| `specs.md` | `auto_hw_complete/specs.md` |
| `input/Homework_2.pdf` | `auto_hw_complete/input/Homework_2.pdf` |
| `output/hw_20260907_f8533b/` | `auto_hw_complete/output/hw_20260907_f8533b/` |
| `playground/hw_20260907_f8533b/` | `auto_hw_complete/playground/hw_20260907_f8533b/` |

## What went in

**`input/Homework_2.pdf`** — 9 pages, five problems, 100 points. Unlike the graph
assignment, every figure here is drawn as **vector** graphics, so `ingest.py`
extracted zero figure files: `get_image_info` finds nothing because nothing is an
embedded image. That would matter if the vectors were diagrams; they are table
rules and section header bars, and the questions are answerable from text plus the
page render. The general fix lives in `pdf_pages.py --page N --dpi 600`, which
re-renders any page or region on demand.

**`specs.md`** — the instruction that makes this example interesting:

> **Skip Problem 5.** Do not answer it, do not assign a worker to it, and do not
> include it in the final document. Problem 5 is worth 45 points; the answered work
> is therefore Problems 1 through 4, 55 points in total. This is a deliberate
> instruction from the user, not an omission.

The master did not merely obey it. It read Problem 5 anyway and recorded, in
`problems.json` under `uncovered`, that the problem is *also* not executable here —
it requires downloading `hw2.tar` onto a specific Notre Dame machine and running
Multi2Sim simulations of 15–25 minutes each, with every answer being a table of
measured cycle counts. Two independent reasons, the user's instruction being the
operative one.

## What came out

`output/hw_20260907_f8533b/final/main.pdf` — 9 pages, Problems 1–4, with the
omission stated once on page 1: *"Problem 5 (45 points) has been omitted
intentionally, at the explicit instruction of the submitter; it is not an
oversight."*

The master cut on problem boundaries rather than merging, which was right here: the
four problems share nothing, while the sub-questions inside each share one machine
description. Its note on Problem 4 shows the reasoning:

> Question B opens with "For this question, ignore Question A", which decouples B's
> arithmetic from A's — but Question C then says "You may refer to your answer in B"

## How the run went

| | |
|---|---|
| wall clock | ~46 minutes |
| cost | $22.49 |
| p1, p3, p4 | passed on validator round 1 |
| **p2** | **failed round 1 on a blocking defect**, passed round 2 |
| master validation | passed round 1 |

### The defect worth reading

`playground/.../validators/p2/checklist.md` records the only real rework of the run,
and it is the fragment contract (rule R5) failing exactly as predicted at design time.

The worker's `answer.tex` used `\text{}` but its `preamble.txt` declared only
`booktabs` and `float`, so the fragment did not compile. The worker had *tested* it —
and reported "pdflatex exits 0, one page, no errors" — but against its own private
wrapper, which loaded `amsmath` and `amssymb` without declaring them. Its compile
check was run against a richer preamble than the one it shipped.

Two things make this a good catch. First, the assembled document would have built
anyway, because Problem 1 happens to declare `amsmath`; the defect was invisible at
the system level and would have surfaced only when Problem 1 changed. The validator
failed it regardless: *"that is luck, not correctness."* Second, on re-check it
generated its wrapper by `cat`-ing the shipped `preamble.txt` rather than writing one
by hand, then ran a three-way negative control — dropping each declared package in
turn — to confirm all three were necessary and none superfluous.

`framework/tools/crosscheck.py` now checks macro-versus-declared-package mechanically,
so this class of defect is caught without spending a validation round on it.

## Reproducing it

```bash
cp examples/specs.md .
cp examples/input/Homework_2.pdf input/
framework/fw run
```
