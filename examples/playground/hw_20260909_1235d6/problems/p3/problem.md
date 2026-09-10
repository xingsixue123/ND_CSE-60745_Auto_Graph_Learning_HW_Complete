# Problem p3 — Ex 1.9 (30 pts: 10 pts per paper)

This is one of the two heavy questions in the assignment. The user's specification says of
Ex 1.9 and Ex 1.0:

> notice that many answers are just plain qa. so no need to compose long answer. but last 2
> ones (1.9,1.0) look big. need careful work, dl paper, read, compose answer and validation.

So: **actually download and read the papers.** Do not write from memory of the title.

## Where this lives in the assignment

    /home/xing/project/auto_hw_complete/input/hw_questions.md      (line 37)

Anchor text: `Ex. 1.9 (30pts) | Pick three papers from ‘OS History and Architecture’ in the paper list.`

Transcribed verbatim:

> Ex. 1.9 (30pts) | Pick three papers from ‘OS History and Architecture’ in the paper list.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper’s
> summarization and judgment. (10pts for each paper)

The assignment's global instruction (line 1) applies:

> You can utilize Google search and read articles that help you to answer the questions. But
> you cannot just copy the answers, put the answers in your own way.

**Do not copy the papers' own abstracts.** A summary lifted from the abstract is exactly what
this instruction forbids, and it is trivially detectable.

## "The paper list" — which papers you may pick from

The paper list is `/home/xing/project/auto_hw_complete/input/PaperList.xlsx`. It is a
spreadsheet, and the ingest already exported it:

    /home/xing/project/auto_hw_complete/playground/hw_20260909_1235d6/ingest/csv/PaperList.csv

**There is a trap in that CSV and I have already resolved it for you.** The `Topics` column
uses merged cells: the label `OS History and Architecture` appears only on the row for paper
1-1, and rows 1-2 through 1-11 have a *blank* Topics cell. If you grep for rows whose Topics
column literally says "OS History and Architecture" you will find exactly one paper and
conclude, wrongly, that the topic has one entry.

I cross-checked this three ways before writing this brief:

1. the CSV blanks form one contiguous run from 1-2 to 1-11, then `Scheduling` appears on 2-1;
2. `ingest/pages/PaperList/page_001.png` colour-bands the Paper ID column — 1-1 through 1-11
   are one green band, and 2-1 starts a different colour;
3. `ingest/pages/PaperList/page_005.txt` lists the five topic labels in order, and their order
   matches the ID prefixes 1-, 2-, 3-, 5-, 4-.

**Conclusion: the 'OS History and Architecture' group is papers 1-1 through 1-11.** These are:

| ID | Title |
|----|-------|
| 1-1  | The Nucleus of a Multiprogramming System  (Brinch Hansen, CACM 1970) |
| 1-2  | The UNIX Time-Sharing System  (Ritchie & Thompson, CACM 1974 / SOSP 1973) |
| 1-3  | Exokernel: An Operating System Architecture for Application-Level Resource Management  (Engler, Kaashoek, O'Toole, SOSP 1995) |
| 1-4  | HYDRA: The Kernel of a Multiprocessor Operating System  (Wulf et al., CACM 1974) |
| 1-5  | The Performance of µ-Kernel-Based Systems  (Härtig et al., SOSP 1997) — note the CSV renders "µ" as "p" |
| 1-6  | StarOS, a Multiprocessor Operating System for the Support of Task Forces  (Jones et al., SOSP 1979) — the CSV has an OCR-style corruption, "Nlultiprocessor" |
| 1-7  | Application Performance and Flexibility on Exokernel Systems  (Kaashoek et al., SOSP 1997) — CSV corrupts "Flexibility" to "Hexibility" |
| 1-8  | On µ-Kernel Construction  (Liedtke, SOSP 1995) |
| 1-9  | seL4: Formal Verification of an OS Kernel  (Klein et al., SOSP 2009) — CSV has "Veri cation", a dropped ligature |
| 1-10 | The Structure of the "THE"-Multiprogramming System  (Dijkstra, CACM 1968) |
| 1-11 | Unikernels: Library Operating Systems for the Cloud  (Madhavapeddy et al., ASPLOS 2013) |

(The parenthetical venues/authors are my reconstruction to help you find the PDFs — verify
each against the paper you actually download, and cite what the paper actually says.)

## Which three to pick

Your choice, but pick three that let you say something interesting *in relation to each
other*, and prefer ones whose PDFs are reliably reachable. A strong, well-spaced set is:

- **1-10** Dijkstra, "THE" (1968) — layered structure, the origin of the semaphore-and-levels
  discipline;
- **1-2** Ritchie & Thompson, UNIX (1974) — the counter-argument: small, uniform abstractions,
  everything-is-a-file, built by two people;
- **1-3** Engler et al., Exokernel (1995) — the modern reaction against fixed abstractions.

That trio gives you a real arc (structure-by-layers → structure-by-abstraction →
abolish-the-abstraction) which makes the "critically judge" half much easier to write well.
You may substitute — 1-8 (Liedtke) and 1-5 (Härtig) pair naturally with 1-3, and 1-9 (seL4) is
a good modern endpoint — but **whatever you pick, state the Paper IDs explicitly in your
answer text** (e.g. "Paper 1-10"). The master needs to read them out of your fragment in order
to brief the next worker, and the grader needs to see you picked from the list.

You have unrestricted network access. Download the PDFs into your own playground directory
(NOT into OUTPUT — see the output rules below), and record every download in
`downloads.md` in your playground, one line each:

    - <name> | <how it was installed> | <path> | <why>

Most of these are freely available (ACM open DL for the classics, MIT PDOS for the exokernel
papers, Dijkstra's archive at UT Austin for THE). If a PDF is genuinely unreachable, pick a
different paper from the eleven rather than writing about one you could not read — and say in
your playground notes which one you swapped and why.

## What "at least 1/3 page for each paper's summarization and judgment" means

Roughly 20–25 lines of set text per paper, i.e. about 300–400 words each, ~1000 words total.
That is the floor, and you should clear it comfortably rather than land exactly on it, but do
not pad — three tight, well-observed 400-word treatments score better than three bloated ones.

**Both halves are required for the 10 pts.** Do not write three summaries and one paragraph of
generic praise at the end. For each paper give:

- **Summary** — the problem the paper is attacking, its central idea/mechanism, how it was
  built and evaluated, and what it actually concluded. Be specific: name the mechanisms
  (semaphores and the five levels; `fork`/`exec`, the i-node, the shell as an ordinary user
  program; secure bindings, software TLB, downloadable packet filters). Concrete detail is the
  evidence that you read it.
- **Critical judgment** — this is where marks are won or lost, and it must be genuine
  criticism, not a compliment. Useful angles: what was the evaluation actually able to show,
  and what did it not measure? What did the authors assume about hardware or workload that
  stopped being true? Which claims did history vindicate and which did it quietly refute? What
  did the paper cost in complexity for what it bought? Where is the argument rhetorical rather
  than measured?

  Some concrete hooks, if useful: THE is a design paper with essentially no performance data
  and a hierarchy that proved too rigid to nest arbitrarily, but its proof-oriented layering
  is the ancestor of everything from seL4 to modern verification; UNIX is famously honest that
  its elegance came from having no resources and no committee, but the paper undersells
  security and says almost nothing about multiprocessing, and "everything is a file" leaks
  badly at sockets and `ioctl`; Exokernel's evaluation is largely microbenchmarks against a
  research OS on 1990s hardware, and its own successor line (library OSes) only became
  practical twenty years later as unikernels and hardware virtualization — so the idea was
  right and the deployment argument was wrong.

Compare the papers to each other at least in passing. A short closing paragraph that puts the
three in a line of descent is cheap to write and reads as understanding rather than
book-reporting.

Cite each paper properly (authors, title, venue, year) at its heading or in a short reference
list at the end of your fragment. Use plain `\textbf`/`\emph` formatting or a
`thebibliography`-free manual list — do **not** introduce BibTeX, since the master compiles
the assembled document in one pass and a `.bib` file is not allowed in OUTPUT.

## What the deliverable is

Plain prose, no diagrams, no code. Three papers, each with a summary and a critical judgment.

## LaTeX / output rules

Write your answer as a LaTeX **fragment** into `answer.tex` in your OUTPUT dir:

- No `\documentclass`, no `\begin{document}`, no `\usepackage` in `answer.tex`.
  Any extra package goes one `\usepackage{...}` per line in `preamble.txt`.
- Start at `\section*{...}` / `\subsection*{...}` level. Suggested shape: one
  `\section*{Ex. 1.9 ...}`, then one `\subsection*{Paper 1-10: The Structure of the
  "THE"-Multiprogramming System}` per paper, each containing a summary and a judgment.
  Note: `"THE"` in LaTeX needs proper quotes — write ``\textit{``THE''}`` style quotes, not
  the ASCII `"` character, or it will render as `,,THE''`.
- **Namespace every label with `p3:`** — e.g. `\label{p3:sec:the}`.
- Downloaded PDFs, notes and scratch files stay in your PLAYGROUND. OUTPUT may contain only
  `answer.tex`, optionally `preamble.txt`, and `fig_p3_*.pdf` figures (you need none).
  Do not copy the papers you downloaded into OUTPUT.
