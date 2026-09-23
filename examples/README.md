# Worked example — Operating Systems, Homework 2

The first run under R8 and R9, the two rules added to `specs.md` after the previous
assignment was hand-edited. It is also the most varied assignment so far: three
schedule diagrams to draw, a C program to compile and run, pseudo-code for four
system calls, and the paired paper questions again, this time on Scheduling.

## Where these files originally lived

| file, as it is here | where it was during the run |
|---|---|
| `specs.md` | `auto_hw_complete/specs.md` |
| `input/hw2_instruction.md` | `auto_hw_complete/input/hw2_instruction.md` |
| `input/hw1_example.md` | `auto_hw_complete/input/hw1_example.md` |
| `input/PaperList.xlsx` | `auto_hw_complete/input/PaperList.xlsx` |
| `output/hw_20260921_077701/` | `auto_hw_complete/output/hw_20260921_077701/` |
| `playground/hw_20260921_077701/` | `auto_hw_complete/playground/hw_20260921_077701/` |

Papers the workers downloaded are excluded, as before: third-party copyrighted
material, with each `downloads.md` recording the URL and how the file was verified.

## Did the rules work

R8 asks for the shortest answer that earns full marks and gives measured word
targets rather than an instruction to be brief. It also tells the validator to count
words and treat over-length as a major defect. That second half is the part that
mattered.

| | HW1 | HW2 |
|---|---|---|
| short-answer questions | 50–51 words per point | 38–42 |
| paper questions | 92–99 | 71–74 |
| whole assignment | 77 | **53** |

Every validator counted. The p3 validator wrote "212 words vs the 190 target —
within the +25% tolerance R8 sets ... Not a defect. Do not spend a round shortening
it", which is the behaviour the rule wanted: check the number, check the four named
kinds of padding, and do not burn a round on a 5% overshoot. The p5 validator folded
the 10-point target down to the 7.5-point questions itself, arriving at 1250–1400
words for three papers, then counted 449 / 468 / 523. The master validator tracked
per-paper counts across all three of its rounds and noted when one section grew from
477 to 482 words.

Paper questions still land about 30% above target. That looks like a floor rather
than a failure: each paper owes a summary and a critique, and the assignment sets
its own minimum of a third of a page.

R9 asks that a quotation be read past before an argument is built on it. Nothing in
this run tripped it, which is not evidence either way.

## The paired paper questions

Ex 2.7 takes three papers from the course list, Ex 2.8 requires three found by
search, and nothing in the assignment forbids answering both with the same papers.
The master sequenced them and wrote Ex 2.7's actual choices plus the whole course
list into Ex 2.8's brief as forbidden. The result is disjoint: Lottery, Stride and
Buttazzo against Liu and Layland, Lozi et al. and Kaffes et al.

The list again hid its own structure. `Scheduling` is papers 2-1 through 2-7, but
after CSV export the label sits only on row 2-1 and the six below it are blank. The
master derived the group from three independent signals: the `2-` ID prefix, the
contiguous run of blank cells ending where the next label resumes, and a shared
colour band in the rendered page that exists in no text channel at all.

## How the run went

| | |
|---|---|
| wall clock | 103 minutes |
| cost | $66.89 |
| p1, p2, p4, p5 | passed on validator round 1 |
| p3 | failed round 1, passed round 2 |
| p6 | failed round 1, passed round 2 |
| master validation | FAIL, then PASS with one minor, then PASS clean |

p3's defect is worth reading. Its fragment opened with `\subsection*` where both
siblings used `\section*`, so once assembled it would have read as a sub-part of the
previous exercise rather than as a question in its own right. The validator found it
by opening the two sibling deliverables and comparing, which is cross-problem work
that nothing asks a per-problem validator to do.

## An operational bug found here

The first launch was stopped with `fw despawn --master`, which reported success.
It killed only the pid in the pidfile; the nested bwrap and the agent under it
survived, ran for another hour and twenty minutes, and spawned a worker of its own
against a job directory that had already been deleted. It was eventually killed by
pid. `run.log` shows one `job created` and one `spawning master agent` and a
monotonic cost sequence, so the orphan did not contaminate this run's accounting,
but `despawn` needs to kill the process group rather than one pid.

## Reproducing it

```bash
cp examples/specs.md .
cp examples/input/* input/
framework/fw run
```
