# p4 — Ex. 3.9 (20 pts)

**Your problem id is `p4`. Namespace every label, figure filename and macro with it**
(`\label{p4:...}`, `fig_p4_*.pdf`).

## Where this comes from

Two documents.

1. The question text:
   `/home/xing/project/auto_hw_complete/input/os_hw_3_problems.md`
   Plain markdown; ingest produced no page images or figure files for it because it
   is text only. Anchor text: `Ex. 3.9 | (20pts) Pick three papers from 'Memory
   Management' in the paper list.`

2. The paper list: `/home/xing/project/auto_hw_complete/input/PaperList.xlsx`,
   normalised by ingest into
   - **`/home/xing/project/auto_hw_complete/playground/hw_20261008_5ae5f8/ingest/csv/PaperList.csv`
     — use this one.**
   - rendered pages: `.../ingest/pages/PaperList/page_003.png` (the titles) and
     `page_005.png` (the topic column). Rendered page indices 3 and 5.

   **I have already read all three channels and resolved the list for you**, because
   two of them are actively misleading here and you should not have to rediscover it:
   - The spreadsheet has the topic name in a *merged* cell spanning seven rows. The
     CSV export flattens merged cells, so `Memory Management` literally appears only
     on the row for paper 3-1 and rows 3-2 … 3-7 have an empty topic cell. Counting
     rows whose topic cell says `Memory Management` gives one paper. The correct
     count is seven. `page_005.png` shows the merge visually and the `3-` ID prefix
     is a third, independent encoding of the same grouping; all three agree.
   - `page_003.txt` (the PDF text channel) extracts the spreadsheet **column-major**
     and dumps the title of paper 3-6 out of order at the very bottom of the page.
     Reading that file alone makes the Memory Management block look like six papers.
     Trust the CSV for titles.

## The question, transcribed verbatim

> Ex. 3.9 | (20pts) Pick three papers from 'Memory Management' in the paper list.
> Read, summarize, and critically judge them. Write at least 1/3 page for each
> paper's summarization and judgment.

## The seven candidates (topic 'Memory Management', IDs 3-1 … 3-7)

Titles exactly as the spreadsheet gives them, with two transcription problems in the
source flagged:

| ID | Title as printed in the paper list |
|----|------------------------------------|
| 3-1 | The Working Set Model for Program Behavior |
| 3-2 | WSCLoca - A Simple and Effective Algorithm for  Virtual Memory Management |
| 3-3 | The Multics Virtual Memory: Concepts and Design |
| 3-4 | Practical, transparent operating system support for superpages |
| 3-5 | Implementing Global Memory Management in a Workstation Cluster |
| 3-6 | Machine-Independent Virtual Memory Management for Paged Uniprocessor and Multiprocessor Architect |
| 3-7 | Virtual Memory Management in the VAX/VMS Operating System |

- 3-2: `WSCLoca` is a typo in the source spreadsheet for **WSCLOCK**. Search for
  "WSCLOCK virtual memory management".
- 3-6: the title is truncated in the spreadsheet; the real one ends
  "...Multiprocessor **Architectures**".

**Pick three of these seven.** The choice is yours — pick ones you can actually
obtain and read in full, and say in the answer which three you picked and (one
clause is enough) why. Do not pick a paper you can only find an abstract for.

You have unrestricted outbound network access: fetch the papers. Verify each one's
real authors, venue and year yourself from the paper or its publisher page and cite
them correctly — do not reproduce a citation from memory, and do not cite the
spreadsheet's truncated/typo'd titles as if they were the real ones.

## Deliverable

- `answer.tex` — LaTeX **fragment** (no `\documentclass`, no `\begin{document}`, no
  `\usepackage`), starting at a heading for `Ex. 3.9`, with one clearly headed
  sub-block per paper giving the full citation, then the summary, then the critique.
- `needs: plain`. No figures.
- `preamble.txt` only for packages beyond amsmath/amssymb/graphicx/geometry.

## Length — the binding constraint on this question

The assignment sets a **floor**: "at least 1/3 page for each paper's summarization and
judgment". R8 below sets the ceiling, and names 550 words as the target for a 10-point
paper summary-and-critique. This question is 20 points for three papers, so budget
**about 400–450 words per paper** — comfortably over the one-third-page floor (a
third of a page is roughly 150–200 words) and under the R8 ceiling. Total roughly
1,200–1,350 words. Split each paper's words roughly 60/40 between summary and
critique; the critique is the part that distinguishes a good answer, so do not let it
shrink to two sentences.

**R9 below is the rule most likely to catch you out on this question.** A critique of
a classic paper that says the author "never considers X" is wrong surprisingly often,
because the author considered X in the section after the one you read. Read to the end
of the relevant discussion before you assert an omission, and prefer a criticism you
can anchor to what the paper actually does with the problem it raises.
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
