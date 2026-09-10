# p2 — notes and plan

## Source verification (R7)

The assignment is `/home/xing/project/auto_hw_complete/input/hw_questions.md`, a plain
markdown file — not a PDF. There is no page render for it, so the three-channel PDF
procedure does not apply. I verified the "no figures" claim myself rather than taking
the brief's word for it:

- `ingest/manifest.json` has exactly one entry, `PaperList.xlsx` (role: assignment),
  rendered to 6 pages. Every page reports `n_images: 0` and `"figures": []`.
  The nonzero `n_vector_drawings` (51/19/51/19/13/8) are spreadsheet cell borders, not
  content figures. `PaperList.xlsx` is the paper list for Ex. 1.9 — not my problem.
- `hw_questions.md` itself: read in full (41 lines). My questions are lines 21, 25, 29, 33.

Brief vs. source: the brief's transcription of Ex. 1.5–1.8 is **verbatim correct**. No
discrepancy to report. (Note for context: lines 17 and 37/41 of the source have OCR-ish
artifacts — `\segmentation fault (core dumped)."` uses backslash-quotes for open quotes,
and the last exercise is numbered `Ex. 1.0` where `Ex. 1.10` was surely meant — but both
are outside my range and belong to other workers.)

## What this problem needs

**plain** only. No code, no diagram.

Reasoning: all four questions ask for conceptual explanation. None says "plot", "draw",
"show" or "illustrate"; none asks for a computed number, count, distribution or ranking.
The one numeric content is the worked base/limit example in Ex. 1.7, which is a
two-operation arithmetic demonstration (14000 + 346) whose purpose is to demonstrate the
translation procedure — inventing a script to add two integers would be theatre, not
verification. I do the arithmetic inline and it is checkable by eye.

## Plan

- One `\subsection*{Ex. 1.N (5 pts)}` per question, numbering exactly as the assignment.
- Length target 3–6 sentences each (user spec: "just few sentences"). Ex. 1.6 as a
  compact numbered list, one line per step, since it asks to "describe all the steps".
- Grading requirement from line 1 of the assignment: "put the answers in your own way".
  So: no copied textbook phrasing. Write from understanding.
- Namespace every label `p2:`.
- Packages needed: `amsmath` (for the aligned translation rule / `\text`) and `enumitem`
  (compact `enumerate` for 1.6). Both confirmed installed per env.md. -> `preamble.txt`.

## Coverage checklist (what a grader ticks)

- 1.5 — BOTH halves. (a) why not: compile-once/run-many, memory state unknown at compile
  time, loader picks the hole, plus ASLR / shared libs / demand paging make it vary
  run-to-run. (b) assumptions: logical address space starting at 0, contiguous; binding
  deferred to load time (relocating loader) or execution time (base register / MMU);
  this is what makes relocatable and position-independent code possible; name the
  compile-time / load-time / execution-time binding trichotomy.
- 1.6 — full chain: event -> resolve to path+argv -> fork -> exec -> permission check,
  header read, MAGIC NUMBER validated -> old address space torn down, new one built
  (text/data/BSS/heap/stack) by mmap -> dynamic linker maps + relocates shared libs ->
  PCB set up, ready queue -> dispatch -> entry point, demand paging -> connects to
  window system/terminal and draws -> shell wait()s, GUI launcher usually does not.
  Must state that double-click vs typed command differ ONLY in how argv is assembled.
- 1.7 — check-then-add order stated explicitly; limit register trap; physical = base +
  virtual; worked example base=14000 limit=3000: VA 346 -> PA 14346; VA 3200 -> trap.
- 1.8 — preemptive FCFS + fixed quantum q, circular ready queue, timer interrupt moves
  runner to tail; quantum tradeoff (large -> FCFS, small -> switch overhead dominates);
  virtue (fairness, bounded response, no starvation, ~1/n of CPU in slices <= q);
  vice (poor average turnaround, ignores priority and job length).
