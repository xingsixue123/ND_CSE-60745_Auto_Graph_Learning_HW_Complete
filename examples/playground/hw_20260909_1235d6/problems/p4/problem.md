# Problem p4 — Ex 1.0 (30 pts: 10 pts per paper)

This is the second of the two heavy questions. The user's specification says of Ex 1.9 and
Ex 1.0:

> notice that many answers are just plain qa. so no need to compose long answer. but last 2
> ones (1.9,1.0) look big. need careful work, dl paper, read, compose answer and validation.

So: **actually download and read the papers.** Do not write from memory of the title.

## Where this lives in the assignment

    /home/xing/project/auto_hw_complete/input/hw_questions.md      (line 41, the last line)

Anchor text: `Ex. 1.0 (30pts) | Search for three papers on the topic of ‘OS History and Architecture’.`

Transcribed verbatim:

> Ex. 1.0 (30pts) | Search for three papers on the topic of ‘OS History and Architecture’.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper’s
> summarization and judgment. (10pts for each paper)

Note on the numbering: the question really is labelled **"Ex. 1.0"** in the source, even
though it comes after Ex 1.9 and is plainly the tenth question. It is almost certainly a typo
for Ex 1.10. **Keep the label exactly as `Ex. 1.0`** in your answer so it matches the
assignment the grader is holding. Do not renumber it.

The assignment's global instruction (line 1) applies:

> You can utilize Google search and read articles that help you to answer the questions. But
> you cannot just copy the answers, put the answers in your own way.

**Do not copy the papers' own abstracts.**

## The one thing that makes this question different from Ex 1.9

Ex 1.9 said *"pick three papers from the paper list"*. This question says *"**search for**
three papers"*. The contrast is the entire point of the question being asked twice: this one
wants papers you found yourself, **not** ones handed to you.

Therefore:

### Hard exclusion 1 — the three papers already used in Ex 1.9

Another worker has already answered Ex 1.9 and its answer is final. It used:

- **Paper 1-10** — Dijkstra, *The Structure of the "THE"-Multiprogramming System*, CACM 1968
- **Paper 1-2** — Ritchie & Thompson, *The UNIX Time-Sharing System*, CACM 1974
- **Paper 1-3** — Engler, Kaashoek & O'Toole, *Exokernel: An Operating System Architecture for
  Application-Level Resource Management*, SOSP 1995

You may **not** write about any of these three. Repeating one would mean the submission
answers 1.9 and 1.0 with the same content and loses marks on this question.

### Hard exclusion 2 — the whole supplied paper list

Do not use *any* of the eleven papers in the 'OS History and Architecture' group of
`/home/xing/project/auto_hw_complete/input/PaperList.xlsx` (exported for you at
`playground/hw_20260909_1235d6/ingest/csv/PaperList.csv`), because all eleven are "from the
paper list" and so belong to Ex 1.9's question, not yours. That group is papers **1-1 through
1-11** — note that the CSV's `Topics` column uses merged cells, so the label appears only on
row 1-1 and rows 1-2..1-11 look blank; I verified the extent of the group against the colour
banding in `ingest/pages/PaperList/page_001.png` and the topic order in `page_005.txt`. The
eleven are:

    1-1  The Nucleus of a Multiprogramming System            (Brinch Hansen 1970)
    1-2  The UNIX Time-Sharing System                        (Ritchie & Thompson 1974)   [used by 1.9]
    1-3  Exokernel                                           (Engler et al. 1995)        [used by 1.9]
    1-4  HYDRA: The Kernel of a Multiprocessor OS            (Wulf et al. 1974)
    1-5  The Performance of µ-Kernel-Based Systems           (Härtig et al. 1997)
    1-6  StarOS, a Multiprocessor OS for Task Forces         (Jones et al. 1979)
    1-7  Application Performance and Flexibility on Exokernel Systems (Kaashoek et al. 1997)
    1-8  On µ-Kernel Construction                            (Liedtke 1995)
    1-9  seL4: Formal Verification of an OS Kernel           (Klein et al. 2009)
    1-10 The Structure of the "THE"-Multiprogramming System  (Dijkstra 1968)             [used by 1.9]
    1-11 Unikernels: Library Operating Systems for the Cloud (Madhavapeddy et al. 2013)

All eleven are off-limits to you.

### What you should do instead

Actually search. You have unrestricted network access — use WebSearch/WebFetch to find papers
on OS history and architecture, and say in your answer, in one sentence, that these were found
by searching the literature (a grader for "search for three papers" wants to see that you did).

Good candidate territory, none of it on the list, all of it squarely "OS History and
Architecture" and all freely downloadable:

- **Corbató & Vyssotsky, "Introduction and Overview of the Multics System"** (AFIPS FJCC 1965) —
  the system THE and UNIX were both reacting to; multics.org hosts it.
- **Accetta et al., "Mach: A New Kernel Foundation for UNIX Development"** (USENIX Summer 1986) —
  the microkernel as an actual product path, and the origin of the memory-object/external-pager
  design that survives in macOS today.
- **Baumann et al., "The Multikernel: A New OS Architecture for Scalable Multicore Systems"**
  (SOSP 2009) — treat the machine as a distributed system; Barrelfish.
- **Barham et al., "Xen and the Art of Virtualization"** (SOSP 2003) — paravirtualization; the
  architecture that actually reshaped deployment.
- **Pike et al., "Plan 9 from Bell Labs"** — the "second system" from the UNIX authors,
  per-process namespaces, 9P.
- **Hunt & Larus, "Singularity: Rethinking the Software Stack"** (OSR 2007) — software isolation
  via a safe language instead of hardware protection.
- **Swift et al., "Improving the Reliability of Commodity Operating Systems"** (Nooks, SOSP 2003).
- **Lampson, "Hints for Computer System Design"** (SOSP 1983) — if you want one that is
  reflective rather than a system description.

Pick any three. As with Ex 1.9, a set with an *argument* running through it beats three
unrelated picks — **Multics (1965) → Mach (1986) → Multikernel (2009)** gives you a clean
historical span (the maximal system → the attempt to decompose it → the abandonment of shared
memory as the organising assumption), and none of the three overlaps Ex 1.9's trio. Xen
substitutes well for the third if you would rather end on the architecture that actually won
commercially.

One thing to avoid: **do not pick Ritchie's "The Evolution of the Unix Time-sharing System"**.
It is not literally on the list, but it is close enough to Ex 1.9's Paper 1-2 that it reads as
double-dipping.

Download the PDFs into your own playground directory (NOT into OUTPUT), and record every
download in `downloads.md` in your playground, one line per item:

    - <name> | <how it was installed> | <path> | <why>

If a PDF turns out to be paywalled or unreachable, swap to a different paper rather than
writing about one you could not read, and note the swap in your playground notes.

## What "at least 1/3 page for each paper's summarization and judgment" means

Roughly 20–25 lines of set text per paper, i.e. about 300–400 words each, ~1000 words total.
That is the floor; clear it comfortably but do not pad.

**Both halves are required for the 10 pts.** For each paper give:

- **Summary** — the problem it attacks, the central mechanism, how it was built and evaluated,
  what it concluded. Be specific and name mechanisms (segments and dynamic linking and rings;
  tasks, threads, ports, messages and memory objects; CPU drivers, monitors, replicated state
  and explicit message passing; hypercalls and the split device driver model). Concrete detail
  is the evidence that you read the paper.
- **Critical judgment** — genuine criticism, not praise. What did the evaluation actually
  demonstrate and what did it quietly not measure? What hardware or workload assumption has
  since expired? Which claims did history vindicate, and which did it refute? What complexity
  was paid for what benefit? Where does the paper argue rhetorically instead of measuring?

Compare the three to each other in a short closing paragraph.

Cite each paper properly (authors, title, venue, year) in a short reference list at the end.
Use a manual list — do **not** introduce BibTeX or a `.bib` file, since the master compiles the
assembled document and a `.bib` is not permitted in OUTPUT.

## Match the house style of Ex 1.9

Your fragment sits immediately after Ex 1.9's in the same document, so a mismatch in structure
is visible on the page. Ex 1.9's fragment is laid out as:

    \section*{Ex.\ 1.9 --- ...}
      short intro paragraph naming the three papers and why they were chosen together
    \subsection*{Paper 1-10 --- Dijkstra, ``...''}
      \textbf{Summary.} ...
      \textbf{Critical judgment.} ...
    \subsection*{...}   (x3)
    \subsection*{The Three Together}
    \subsection*{References}   (an enumerate with [{[1-10]}] style custom labels)

Use the same shape: `\section*{Ex.\ 1.0 --- ...}`, an intro naming your three and why, one
`\subsection*` per paper with bold `Summary.` / `Critical judgment.` run-in headings, a short
comparative subsection, and a References subsection. Your papers have no list IDs, so number
your references `[1] [2] [3]` and title your per-paper subsections with author and short title
(e.g. `\subsection*{Paper 2 --- Accetta et al., ``Mach''}`).

Use LaTeX quotes (`` and '') rather than the ASCII `"` character throughout, or quotes render
backwards.

## What the deliverable is

Plain prose, no diagrams, no code. Three papers, each with a summary and a critical judgment.

## LaTeX / output rules

Write your answer as a LaTeX **fragment** into `answer.tex` in your OUTPUT dir:

- No `\documentclass`, no `\begin{document}`, no `\usepackage` in `answer.tex`.
  Any extra package goes one `\usepackage{...}` per line in `preamble.txt`.
- Start at `\section*{...}` level.
- **Namespace every label with `p4:`** — e.g. `\label{p4:sec:mach}`. Ex 1.9's worker used the
  `p3:` prefix, so a bare `\label{sec:refs}` from you would collide and break the compile.
- Downloaded PDFs, notes and scratch files stay in your PLAYGROUND. OUTPUT may contain only
  `answer.tex` and optionally `preamble.txt`. Do not copy downloaded papers into OUTPUT.
