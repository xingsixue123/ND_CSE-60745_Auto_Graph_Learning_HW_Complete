# p3 — Ex. 1.9 notes

## Ground-truth check of the brief

- `input/hw_questions.md` line 37 matches the brief's transcription **verbatim**. No discrepancy.
- Paper list group membership independently re-verified (I did not take the brief's word):
  1. `ingest/csv/PaperList.csv` — `OS History and Architecture` on row 1-1 only; rows 1-2..1-11
     blank; `Scheduling` reappears on 2-1. Contiguous run ⇒ merged cell spanning 1-1..1-11.
  2. `ingest/pages/PaperList/page_001.png` — the Paper ID column is colour-banded. 1-1 through
     1-11 are one green band; 2-1 begins a blue band. Independent of the CSV.
  3. `ingest/pages/PaperList/page_005.txt` — topic labels in order.
     Note a small correction to the brief: the brief says "five topic labels ... 1-,2-,3-,5-,4-".
     The extraction actually shows the order OS History / Scheduling / Memory Management /
     Storage and File Systems / Threads,Events,Concurrency,Synchronization, and `Distributed
     Systems` (group 6-) does not appear in that text channel at all. That is a column-major
     PDF-extraction artifact and is irrelevant to my question — group 1 membership is
     unaffected and is confirmed by channels 1 and 2 anyway.
- **Conclusion: 'OS History and Architecture' = papers 1-1 .. 1-11.** Same as the brief.

## What this problem needs

**plain** only. No code, no diagram.
Justification: the question is "read, summarize, and critically judge three papers". There is
no number to compute, nothing to plot, no figure to transcribe. The only "data gathering" is
downloading and reading the actual PDFs, which R7's figure rules do not apply to (they are
prose papers, not figure-bearing homework pages) — but I do read them, not summarize from
memory, per the brief's explicit instruction.

## Papers picked

- **1-10** Dijkstra, "The Structure of the THE-Multiprogramming System", CACM 1968
- **1-2**  Ritchie & Thompson, "The UNIX Time-Sharing System", CACM 1974
- **1-3**  Engler, Kaashoek & O'Toole, "Exokernel: An Operating System Architecture for
           Application-Level Resource Management", SOSP 1995

Rationale: they form a real line of descent — structure-by-layers (1968) →
structure-by-uniform-abstraction (1974) → abolish-the-abstraction (1995) — which makes the
"critically judge" half substantive rather than three disconnected book reports.

## Plan

1. Download all three PDFs into `papers/`. Record in `downloads.md`.
2. Extract text from each; read it properly (not the abstract — the body: mechanisms,
   evaluation, what they actually concluded).
3. Verify the bibliographic data (authors, venue, year, page numbers) against the PDF itself,
   not against the brief's reconstruction.
4. Write ~400-450 words per paper: summary + genuine criticism, plus a short comparative close.
5. `answer.tex` fragment, labels namespaced `p3:`.

## Anti-plagiarism discipline

The assignment forbids copying. I will not lift abstract sentences. Specific technical facts
(numbers, mechanism names) are quoted as facts with the paper's own figures cited; the prose
is mine.
