# p5 — Ex. 2.7 (22.5 pts): three "Scheduling" papers from the course paper list

**Problem id: `p5`.** Namespace every label and macro with `p5`.

## Where this lives in the assignment

The assignment text is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, a byte-for-byte copy of the markdown.
Read the markdown itself as ground truth for the question text.

The **paper list** is a separate spreadsheet, `input/PaperList.xlsx`, and it *does*
have rendered pages (6 of them) plus a CSV export. Details below.

Anchor text: `Ex. 2.7 | (22.5pts) Pick three papers from 'Scheduling' in the paper
list.`

## The question, transcribed verbatim

> Ex. 2.7 | (22.5pts) Pick three papers from ‘Scheduling’ in the paper list. Read,
> summarize, and critically judge them. Write at least 1/3 page for each paper’s
> summarization and judgment. (7.5pts for each paper)

The assignment's preamble also applies, and it matters here more than anywhere else:
*"You can utilize Google search and read articles that help you to answer the
questions. But you cannot just copy the answers, put the answers in your own way."*

## The paper list, and how to read it safely

Three channels, already extracted for you:

- CSV export (use this for the titles):
  `playground/hw_20260921_077701/ingest/csv/PaperList.csv`
- rendered page image (use this to confirm group membership):
  `playground/hw_20260921_077701/ingest/pages/PaperList/page_001.png`
- per-page text: `.../pages/PaperList/page_001.txt` (IDs) and `page_003.txt` (titles)

**Two traps, both already diagnosed — do not re-derive them, just do not fall into
them.** (1) The spreadsheet's `Topics` column uses merged cells, and CSV export
flattens them: the word `Scheduling` appears only on row `2-1`, and rows `2-2`…`2-7`
have an empty Topics cell. They are *still* in the Scheduling group. (2) The per-page
text of a spreadsheet extracts column-major, so IDs and titles come out as two separate
runs and must be zipped back together by position.

The Scheduling group is therefore exactly these seven, confirmed independently by the
`2-` ID prefix, by the merged-cell run in the CSV, and by the shared blue colour band
on `page_001.png`:

| ID | Title |
|---|---|
| 2-1 | Rate Monotonic vs. EDF: Judgment Day |
| 2-2 | Real-Time Dynamic Voltage Scaling for Low-Power Embedded Operating System |
| 2-3 | Lottery Scheduling: Flexible Proportional-Share Resource Management |
| 2-4 | Stride Scheduling: Deterministic Proportional-Share Resource Management |
| 2-5 | Arachne: Core-Aware Thread Management |
| 2-6 | Implementing Lottery Scheduling: Matching the Specializations in Traditional Schedulers |
| 2-7 | Microservices The Journey So Far and Challenges Ahead |

## Which three to write about

Write about **2-3, 2-4 and 2-1**, in that order:

1. **2-3** — C. A. Waldspurger and W. E. Weihl, *Lottery Scheduling: Flexible
   Proportional-Share Resource Management*, OSDI 1994.
2. **2-4** — C. A. Waldspurger and W. E. Weihl, *Stride Scheduling: Deterministic
   Proportional-Share Resource Management*, MIT/LCS/TM-528, 1995.
3. **2-1** — G. C. Buttazzo, *Rate Monotonic vs. EDF: Judgment Day*, Real-Time Systems
   29(1), 2005.

This trio is chosen deliberately: 2-4 is the same authors' own answer to 2-3's biggest
weakness (throughput error that decays only as O(√n) because the allocation is random),
so the two can be judged against each other rather than in isolation, and 2-1 is a
different tradition entirely (hard real-time, RM vs EDF) which stops the answer from
becoming one long essay about proportional share.

If a paper's full text genuinely cannot be obtained, you may substitute another paper
**from the seven above only**, and you must say in your submission report which one you
dropped and why. Do not silently substitute.

## What the deliverable is

**plain.** For each of the three papers, a *Summary* and a *Critical judgment*.

**You must actually read the papers.** You have unrestricted network access. Download
each PDF into your PLAYGROUND, read it with the Read tool (it reads PDFs directly, with
a `pages` argument) or with `pymupdf`, and record every download in
`PLAYGROUND/downloads.md` per rule R3. Do not write a critique from an abstract, a
Wikipedia article or your prior knowledge of the paper: a summary assembled from
memory reliably contains numbers that are not in the paper, and your validator will
open the paper and check. Known-good starting points (verify, do not assume):
Lottery Scheduling and Stride Scheduling are both freely available from MIT and from
the USENIX archive; the Buttazzo paper is widely mirrored — search for it.

**What a good critique looks like here.** The reference answer from the previous
assignment (which you cannot see) earned its marks by doing three things: quoting the
paper's own numbers and its own hedges; naming the specific place where the evidence
does not reach the claim; and saying what history did with the idea. Concretely, for
these three, the load-bearing material is in the evaluation sections — e.g. lottery
scheduling's fairness experiments and the 2:1 ratio it actually achieves, its own
admission about response-time variability, the compensation-ticket mechanism, and what
it says about currencies; stride scheduling's direct error comparison against lottery
and its hierarchical variant; Buttazzo's tabulated comparison of implementation
complexity and overhead and his arguments about behaviour during overload. Use the
paper's real figures, not remembered ones.

**Rule R9 applies with full force** (it is quoted in full below): before you criticise
a paper for not addressing something, read to the end of that discussion. Both
of these papers answer the obvious objections somewhere in the text, and a critique
that says "the authors never consider X" when section 5 considers X is a defect that
costs a validation round.

A short comparative paragraph across the three at the end is welcome if it earns its
place; it is not required.

## Citations

End your fragment with a small reference list (`p5`-namespaced labels, or plain
manual `[1] [2] [3]`-style items in an `enumerate`/`description` — do **not** use
`\bibliography`, there is no `.bib` in the assembled document). Give authors, title,
venue and year for each paper, in the style of the hw1 reference answer. Cite the
paper-list ID (2-3, 2-4, 2-1) alongside, since the question asks for papers *from the
list*.

## Length

Per rule R8 below: a 10-point paper summary-and-critique targets about 550 words. These
are worth 7.5 points each, so target roughly **400–450 words per paper** (summary plus
critical judgment together), and make sure each comfortably clears the assignment's
own "at least 1/3 page" floor. Three papers ≈ 1250–1400 words total. Substantially
over that, with no new substance, is a defect.

---

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
