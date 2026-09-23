# p6 — Ex. 2.8 (22.5 pts): three scheduling papers you find yourself

**Problem id: `p6`.** Namespace every label and macro with `p6`.

## Where this lives in the assignment

The assignment text is a **plain markdown file**, not a PDF or a Word document:

    /home/xing/project/auto_hw_complete/input/hw2_instruction.md

Ingest produced **no page PNGs and no figure files** for it — only
`ingest/pages/hw2_instruction/alltext.txt`, a byte-for-byte copy of the markdown.
There is no figure anywhere in this assignment. Read the markdown as ground truth.

Anchor text: `Ex. 2.8 | (22.5pts) Search for three papers on the topic of 'Scheduling'.`

## The question, transcribed verbatim

> Ex. 2.8 | (22.5pts) Search for three papers on the topic of ‘Scheduling’. Read,
> summarize, and critically judge them. Write at least 1/3 page for each paper’s
> summarization and judgment. (7.5pts for each paper)

The assignment's preamble also applies, and it matters here more than anywhere else:
*"You can utilize Google search and read articles that help you to answer the
questions. But you cannot just copy the answers, put the answers in your own way."*

## The one constraint the question does not spell out

This exercise sits directly after Ex. 2.7, which asks for three papers **from the
course paper list**. Ex. 2.8 is the "go and find your own" counterpart, so your three
papers must **not** be on that list. The list's Scheduling group is exactly:

| ID | Title |
|---|---|
| 2-1 | Rate Monotonic vs. EDF: Judgment Day |
| 2-2 | Real-Time Dynamic Voltage Scaling for Low-Power Embedded Operating System |
| 2-3 | Lottery Scheduling: Flexible Proportional-Share Resource Management |
| 2-4 | Stride Scheduling: Deterministic Proportional-Share Resource Management |
| 2-5 | Arachne: Core-Aware Thread Management |
| 2-6 | Implementing Lottery Scheduling: Matching the Specializations in Traditional Schedulers |
| 2-7 | Microservices The Journey So Far and Challenges Ahead |

None of those seven. The full list is at
`playground/hw_20260921_077701/ingest/csv/PaperList.csv` if you want to check anything
else you are considering — note that its `Topics` column comes from merged cells, so
only row `2-1` carries the word `Scheduling`; rows `2-2`…`2-7` are in the same group
with a blank cell. The colour banding on
`.../ingest/pages/PaperList/page_001.png` confirms the group boundaries independently.

Also: do not pick a paper that is merely *adjacent* to one on the list (a second
lottery-scheduling paper, say) — the point of this exercise is coverage the list does
not already give you.

## What the deliverable is

**plain.** For each of the three papers: a *Summary* and a *Critical judgment*, plus a
one-line statement at the top of the section of **how you found them** (the question
says "search for", and saying which search and why these three is cheap and shows the
selection was deliberate).

**You must actually read the papers.** You have unrestricted network access. Download
each PDF into your PLAYGROUND, read it with the Read tool (it reads PDFs directly, with
a `pages` argument) or with `pymupdf`, and record every download in
`PLAYGROUND/downloads.md` per rule R3. Do not write a critique from an abstract, a blog
post, or prior knowledge: a summary assembled from memory reliably contains numbers
that are not in the paper, and your validator will open the paper and check every one
of them. **Pick papers whose full text you can actually obtain for free** — if the PDF
is paywalled, pick a different paper rather than working from the abstract.

### Choosing the three

Choose them yourself; the following is a pool of strong, freely available, genuinely
scheduling-focused candidates that are *not* on the course list, offered so you do not
burn time searching. Verify availability before committing.

- J. Liu and J. Layland, *Scheduling Algorithms for Multiprogramming in a Hard-Real-Time
  Environment*, JACM 1973 — the origin of rate-monotonic and EDF.
- J.-P. Lozi et al., *The Linux Scheduler: a Decade of Wasted Cores*, EuroSys 2016 —
  four bugs in CFS's load balancer, with a measurement methodology.
- A. Verma et al., *Large-scale cluster management at Google with Borg*, EuroSys 2015.
- A. Ghodsi et al., *Dominant Resource Fairness: Fair Allocation of Multiple Resource
  Types*, NSDI 2011.
- B. Hindman et al., *Mesos: A Platform for Fine-Grained Resource Sharing in the Data
  Center*, NSDI 2011.
- A. Ousterhout et al., *Shenango: Achieving High CPU Efficiency for Latency-sensitive
  Datacenter Workloads*, NSDI 2019; or K. Kaffes et al., *Shinjuku: Preemptive
  Scheduling for μsecond-scale Tail Latency*, NSDI 2019.
- T. E. Anderson et al., *Scheduler Activations* is **on the list** (4-8) — do not use
  it.

Prefer a spread — e.g. one classical/theoretical, one OS-kernel, one datacenter — over
three papers making the same argument. Aim for papers with real evaluation sections,
because a critique needs something to bite on.

### What a good critique looks like

The reference answer from the previous assignment earned its marks by quoting the
paper's own numbers and its own hedges, naming the specific place where the evidence
does not reach the claim, and saying what history did with the idea. Use the paper's
real figures, not remembered ones, and quote sparingly and exactly.

**Rule R9 applies with full force** (quoted in full below). Before writing that an
author "never addresses" or "leaves open" something, read to the end of that
discussion — papers of this calibre usually have a limitations or discussion section
that anticipates the obvious objection, and a critique aimed at an objection the paper
already answers is a defect that costs a validation round. The stronger move is to
quote what the paper says about its own limitation and then say why that answer is
insufficient.

## Citations

End your fragment with a small reference list (`p6`-namespaced labels, or plain manual
`[1] [2] [3]` items in an `enumerate`/`description` — do **not** use `\bibliography`,
there is no `.bib` in the assembled document). Authors, title, venue, year; include a
DOI or URL where you have one, since these are papers you found rather than papers the
course supplied.

## Length

Per rule R8 below: a 10-point paper summary-and-critique targets about 550 words. These
are worth 7.5 points each, so target roughly **400–450 words per paper** (summary plus
critical judgment together), and make sure each comfortably clears the assignment's own
"at least 1/3 page" floor. Three papers ≈ 1250–1400 words total plus the one-line note
on how you searched. Substantially over that, with no new substance, is a defect.

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
