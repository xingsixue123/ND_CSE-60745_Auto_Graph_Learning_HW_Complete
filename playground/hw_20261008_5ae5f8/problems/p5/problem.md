# p5 — Ex. 3.10 (20 pts)

**Your problem id is `p5`. Namespace every label, figure filename and macro with it**
(`\label{p5:...}`, `fig_p5_*.pdf`).

## Where this comes from

`/home/xing/project/auto_hw_complete/input/os_hw_3_problems.md` — plain markdown.
Ingest produced no page images and no figure files for it because it is text only.
**This question refers to no figure.**

Anchor text: `Ex. 3.10 | (20pts) Search for three papers on the topic of 'Memory
Management'.`

## The question, transcribed verbatim

> Ex. 3.10 | (20pts) Search for three papers on the topic of 'Memory Management'.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper's
> summarization and judgment.

## What distinguishes this from Ex. 3.9 — read this carefully

Ex. 3.9 (answered by another worker, already accepted) asked the student to pick three
papers **from the course paper list**. Ex. 3.10 asks them to **search** for three. The
two questions are only different if the papers are different, so:

**You must NOT use any of these three, which Ex. 3.9 already covers:**

1. Denning, "The Working Set Model for Program Behavior", CACM 11(5):323–333, 1968.
2. Rashid, Tevanian, Young, Golub, Baron, Black, Bolosky, Chew, "Machine-Independent
   Virtual Memory Management for Paged Uniprocessor and Multiprocessor Architectures",
   ASPLOS II, 1987.
3. Navarro, Iyer, Druschel, Cox, "Practical, Transparent Operating System Support for
   Superpages", OSDI '02.

**You must also NOT use any other paper on the course list's Memory Management topic**,
since those are what Ex. 3.9 draws from. The full set to avoid is papers 3-1 … 3-7:

| ID | Title (as the course spreadsheet prints it) |
|----|---------------------------------------------|
| 3-1 | The Working Set Model for Program Behavior |
| 3-2 | WSCLoca - A Simple and Effective Algorithm for Virtual Memory Management (sic: "WSCLOCK") |
| 3-3 | The Multics Virtual Memory: Concepts and Design |
| 3-4 | Practical, transparent operating system support for superpages |
| 3-5 | Implementing Global Memory Management in a Workstation Cluster |
| 3-6 | Machine-Independent Virtual Memory Management for Paged Uniprocessor and Multiprocessor Architectures |
| 3-7 | Virtual Memory Management in the VAX/VMS Operating System |

The course spreadsheet is at
`/home/xing/project/auto_hw_complete/playground/hw_20261008_5ae5f8/ingest/csv/PaperList.csv`
if you want to check the rest of it; note that its topic column uses merged cells, so
the literal string "Memory Management" appears only on row 3-1 — the topic actually
spans rows 3-1 through 3-7, which the `3-` ID prefix confirms independently.

## What to pick instead

Search properly; you have unrestricted outbound network access. Pick three real,
findable papers on memory management that you can obtain and read **in full** — do not
summarise from an abstract, and do not cite a paper you could not open. Say in one
clause per paper why you chose it.

Choosing three papers that are recent, or that cover ground the 1968–2002 list does
not, makes for a better answer than three more classics, but this is your call and the
marks are for the summary and the critique, not for the taste of the selection. Give a
full, correct citation for each (authors, exact title, venue, year) **verified against
the paper itself or its publisher page**, not reconstructed from memory.

## Deliverable

- `answer.tex` — LaTeX **fragment** (no `\documentclass`, no `\begin{document}`, no
  `\usepackage`), starting at a heading for `Ex. 3.10`, with one clearly headed
  sub-block per paper: full citation, then summary, then critique.
- `needs: plain`. No figures.
- `preamble.txt` only for packages beyond amsmath/amssymb/graphicx/geometry.

## Length

The assignment sets a floor ("at least 1/3 page" per paper, roughly 150–200 words);
R8 below sets the ceiling. Budget **about 400–450 words per paper**, roughly 60/40
between summary and critique, for a total of about 1,200–1,350 words. The critique is
what earns the marks above a pass — do not let it collapse into two sentences.

**R9 below is the rule most likely to catch you out.** Before you write that a paper
"does not address" or "never considers" something, read to the end of that discussion
in the paper. Authors routinely raise a limitation and answer it in the next
paragraph, and a critique aimed at a gap the paper actually fills is the single
easiest defect for a marker to find.
## Rules for workers

**Master: copy this whole section verbatim into every `problem.md` you write.**
Workers and worker validators never see this file; the brief is the only channel
that reaches both of them.

These are not style preferences. They are defects. A worker that breaks one has
not finished, and a validator that passes one has not done its job.

### R8 — Answer the question asked, at the length it deserves

Write the shortest answer that earns full marks, then stop. Concrete targets,
measured from a previous assignment after a careful human edit:

| question | target |
|---|---|
| a 5-point short answer | about 190 words; up to 290 if it has several sub-parts |
| a 10-point paper summary and critique | about 550 words |

Left alone, an answer comes out **1.5 to 2 times** these lengths. That is the
failure mode to watch for in yourself. The excess is never new substance; it is
always one of these four:

- **exhaustive enumeration** — four examples where the question needs one, six
  hardware mechanisms where three carry the argument;
- **summarising your own answer** — a closing sentence that restates the opening
  one. If a paragraph begins "so the model is X" and ends "the model is therefore
  X", delete the ending;
- **explaining the significance of your own answer** — the question asked *where*
  the magic number is stored, not why that location is efficient;
- **stating what you are about to do** — "the three binding times are worth
  naming", "it is worth noting that".

Em-dashes are a symptom rather than a cause, but they mark the places to look:
one every 70 words means the sentences are being extended rather than ended.

**Validator: count the words.** Compare against the target above and against what
the problem is worth. Over target by more than a quarter, with no sub-part that
justifies it, is a defect to be reported and fixed, at severity major. Do not pass
an answer because it is correct if it is also twice as long as it needs to be.

### R9 — Read past the quotation

When you quote or cite a source, read the sentences that follow the quote before
you build an argument on it. Stop at the quote and you will write a criticism the
source already answers, or attribute to an author a claim they did not make.

Both of these happened in a previous assignment and both were findable with one
grep by the person marking it:

- A paper was criticised for raising a security problem and leaving it there. The
  next sentence of the paper proposed two countermeasures. (The real criticism was
  available and stronger: one countermeasure reintroduced the central authority the
  design existed to remove, and the other was justified only "on a system that
  assumes no malicious processes".)
- A paper's closing section was described as claiming a system succeeded because
  it had no predefined objectives. It says nothing of the sort; it says the authors
  were grateful never to have had to satisfy someone else's requirements. The
  critique was aimed at an invented claim.

So: quote the source, then say what the source does next with it. Never assert that
an author "leaves the problem there", "never asks", or "does not address" something
without having read to the end of that discussion.

**Validator: for every quotation and every characterisation of what a source says
or fails to say, open the source and read the surrounding passage yourself.** A
quotation that is verbatim can still be used to support a claim the source
contradicts two sentences later. Confirming the words exist is not the check;
confirming the argument survives the context is.
