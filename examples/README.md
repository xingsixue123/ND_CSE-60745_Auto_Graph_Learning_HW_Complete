# Worked example — Operating Systems, Homework 1

The third test of the pipeline, and the first where the answers cannot be checked by
recomputation. Eight short-answer questions, then two thirty-point questions that
require finding real research papers, reading them, and criticising them.

That changes what validation means. In the earlier runs a validator could re-run a
worker's script and diff the numbers. Here there is nothing to recompute: the only way
to know whether a critique is sound is to read the source papers and check every claim
against them.

## Where these files originally lived

Moved here after the run so `input/`, `output/` and `playground/` are empty for the
next assignment:

| file, as it is here | where it was during the run |
|---|---|
| `specs.md` | `auto_hw_complete/specs.md` |
| `input/hw_questions.md` | `auto_hw_complete/input/hw_questions.md` |
| `input/PaperList.xlsx` | `auto_hw_complete/input/PaperList.xlsx` |
| `output/hw_20260909_1235d6/` | `auto_hw_complete/output/hw_20260909_1235d6/` |
| `playground/hw_20260909_1235d6/` | `auto_hw_complete/playground/hw_20260909_1235d6/` |

The papers the workers downloaded are **not** here — they are third-party copyrighted
material (ACM, USENIX) and `.gitignore` excludes them. Each worker's `downloads.md`
records the exact URL it fetched and how it verified the file was the genuine paper, so
the run is reproducible without redistributing them.

## What made this assignment different

**The assignment is Markdown, not a PDF**, and it arrived beside a spreadsheet and, at
first, 289 pages of lecture slides. That exposed three gaps, all fixed before the run:
`ingest.py` classified the actual assignment as a data file while treating the slides
as documents; it would have rendered all 289 slide pages at 200 dpi; and a spreadsheet
converted to PDF extracts column-major, so every row came apart. Assignments are now
files directly in `input/` (subdirectories are supporting material, never pre-rendered),
`.md`/`.txt` are first-class assignment formats, and spreadsheets are also exported to
CSV.

**The paper list hides its own structure.** `PaperList.xlsx` uses merged cells for the
`Topics` column, so after CSV export the label `OS History and Architecture` appears
only on the row for paper 1-1 and rows 1-2 … 1-11 are blank. Ex. 1.9 asks for three
papers *from that topic*; a literal search finds one, and the question looks
unanswerable. Four agents independently worked out that the group is 1-1 … 1-11, each
citing two channels: the CSV blanks form one contiguous run that ends where `Scheduling`
resumes at 2-1, and the rendered page colour-bands the Paper ID column in matching
groups. The colour banding exists only in the image channel — it is not in the text at
all. `env.md` warns about merged cells generally; the specific grouping was not given
to anyone.

**Ex. 1.9 and Ex. 1.0 must not overlap.** One says pick three papers from the list, the
other says search for three on the same topic. Nothing forbids answering both with the
same papers, but doing so would be wrong. The master neither merged them into one
sixty-point worker nor let them run blind: it sequenced Ex. 1.0 *after* Ex. 1.9 and, once
Ex. 1.9 had passed, wrote its three actual choices plus all eleven list papers into Ex.
1.0's brief as forbidden. The brief's timestamp is 69 seconds after Ex. 1.9's validator
returned. It also added an exclusion nobody asked for — Ritchie's "The Evolution of the
Unix Time-sharing System", on the grounds that although it is not literally on the list
it is close enough to Paper 1-2 to read as the same submission twice.

The result: Ex. 1.9 took THE (1968), UNIX (1974) and Exokernel (1995); Ex. 1.0 found
Multics (1965), Mach (1986) and the Multikernel (2009). Disjoint, and between them they
trace a coherent line through OS architecture.

## The defect worth reading

`playground/.../validators/p4/checklist.md`, round 1 — the only blocking defect of the
run, and the third time across three assignments that the failure was **reading a value
off a figure**.

The worker wrote that Barrelfish's unmap cost starts "at roughly 5.5k cycles at two
cores, merely with a gentler slope than Linux's", concluding that the multikernel
"reduced the constant; it did not remove the scaling term". The validator re-rendered
page 13 of the Multikernel paper at 300 dpi, cropped the x ∈ [2,8] region, and read the
curves against the legend: at two cores Barrelfish costs ~10.3k, Linux ~5.2k, Windows
~5.8k. The 5.5k figure was *Linux's*. Tracing it back, the worker's own `notes.md`
recorded "(Barrelfish ~5.5k, Linux ~5k, Windows ~10k)" — Barrelfish and Windows swapped
at the left edge of the plot — and the error propagated verbatim into the answer.

It reversed the criticism. Corrected, Barrelfish grows 1.7× over 2→32 cores where Linux
grows 5.7×: the multikernel did not reduce the constant, it roughly doubled it and
bought a much flatter slope. The validator pointed out that the paper concedes exactly
this two sentences later in text the answer already quoted — so as written, the paragraph
contradicted itself. It also said which neighbouring claim was sound and should be kept.

Text, formulas, tables and code have not produced a substantive error in any run.
Reading a number off a chart has produced two of the three blocking defects.

## How the run went

| | |
|---|---|
| wall clock | 82 minutes |
| cost | $51.44 |
| Ex. 1.1–1.8 (two workers) | passed on validator round 1 |
| Ex. 1.9 | passed on round 1 |
| Ex. 1.0 | failed round 1 on the figure misread, passed round 2 |
| master validation | three rounds, all PASS |

Roughly twice the cost of the earlier runs, almost entirely in the paper questions: six
papers to fetch and read, and a validator that had to read them too. The master
validator alone cost $7.69 on its first round against $2.76 and $1.39 in the previous
two assignments.

**Three master rounds, all passing, is worth noticing.** A `PASS` describes the document
as submitted, so the master must re-validate anything it edits afterwards — a rule added
after the first assignment. Here it passed with six minor defects, fixed five,
re-submitted, passed with one new minor defect, fixed it, re-submitted, and passed
cleanly. It converged because the defect count fell to zero, not because anything
stopped it: with a slightly pickier validator the same loop would have run to the
five-round cap.

## Reproducing it

```bash
cp examples/specs.md .
cp examples/input/* input/
framework/fw run
```
