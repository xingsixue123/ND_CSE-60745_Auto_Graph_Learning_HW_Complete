# p5 — worker validator checklist

## Round 1
Verdict: PASS

### What I checked and how

**Ground truth (R7 / brief-vs-source).** The assignment is markdown, not a PDF, so the
three-channel rule degenerates to reading the source. `input/hw2_instruction.md` line 34
matches the brief's transcription of Ex. 2.7 verbatim. Scheduling group 2-1…2-7 confirmed
from `ingest/csv/PaperList.csv` (merged-cell run: `Scheduling` on 2-1, blanks through 2-7,
next label `Memory Management` on 3-1). No brief/source discrepancy.

**Papers are genuine.** Re-extracted all three PDFs myself (`mypapers/*.flow.txt`) rather
than trusting the worker's text dumps. Title blocks match the cited venues, including
`Real-Time Systems, 29, 5-26, 2005` against reference [3].

**Independent quote/number verification.** Wrote my own harness (`vcheck.py`, 37 checks)
rather than only re-running the worker's. 36/37 hit verbatim. The one miss (`19.64`) is
the `pdftotext` artifact the worker documented: Computer Modern's math decimal point
extracts as `:`. Fig. 12's caption reads `= 20:13, = 19:64` / `= 20:00, = 0:01`, and the
sibling values (`1:05`, `0:24`) make the reading unambiguous. All four Fig. 12 numbers in
`answer.tex` are correct. The worker's own `verify_quotes.py` also reproduces: 60/60, exit 0.

Spot-verified in full surrounding context, not just as substrings:
- Lottery: 25378/12619, 13.42:1, 19.08:1 over three minutes, 17.19/43.19/132.20 s under the
  8:3:1 allocation, 1.01:1 → 1.00:1 currency insulation, 2.7%/0.8%/1.7%, Mach 3.0 on a
  25MHz DECStation 5000/125 with a 100 ms quantum, coefficient of variation √((1−p)/np).
- Stride: absolute error 50 for 101 clients at 100:1:…:1, hierarchical 4.5, 2409.18/802.89
  → 3.001:1, Linux 1.1.50, "fewer than 300 lines", range 1–194 quanta.
- Buttazzo: 256 priority levels and the adjacent-deadline remap, O(1) FIFO insertion,
  ln 2 ≈ 0.69, T̄i = Ti·U with the U=1.25 example, C=(2,3,1,1)/T=(5,9,20,30) with a 1.5-unit
  overrun making τ2 (not τ4) miss, jitters 0,2,8 vs 1,2,3.

**R9 — read past the quotation.** This is where I expected to find the defect, and did not.
Checked every characterisation of what a source does or fails to do:
- "the authors honestly note the run-to-run standard deviation was as large as the effect" —
  the paper says exactly that, and the worker did *not* stop at the flattering
  "does not pose any challenging problems" quote.
- The setuid/ACL criticism is correctly narrowed: the paper's next sentence is "A complete
  lottery scheduling system should protect currencies by using access control lists…", so
  the worker's "proposed but left as what a complete system should provide" is the accurate
  reading, and the naive "they ignore inflation" criticism was correctly avoided.
- The 1.7% speedup is indeed attributed to cache/TLB locality in footnote 9, as claimed.
- Buttazzo's jitter disclaimer ("does not prove that EDF always introduces less jitter")
  immediately follows the 0,2,8 vs 1,2,3 example — the worker quotes the disclaimer rather
  than criticising the overreach it already hedges.
- "grants that RM confines an overrun to tasks of lower priority while EDF confines it
  nowhere" matches §5.2 verbatim in substance.

**Absence claims (the R9 danger zone) — all three hold.**
- Buttazzo/multiprocessors: `multiprocessor`, `multi-core`, `parallel` all occur 0 times in
  the full text. Claim verified.
- Stride prototype implements neither transfers nor currencies: the paper says it outright —
  "We did not implement support for higher-level abstractions such as ticket transfers and
  currencies." Correctly framed as the paper's own admission.
- Stride never measured against a lottery kernel: §6 mentions lottery nowhere; every lottery
  comparison after §6 is in §7 Related Work. The head-to-head really is simulation only, and
  the paper's own "hierarchical stride scheduler *simulations*" wording corroborates it.

**The worker's pushback on the brief is correct.** The brief told it to use lottery's "own
admission about response-time variability". §2.2 states σ²=(1−p)/p² neutrally and follows it
with "reasonable fairness can be achieved over subsecond time intervals" — no admission of
cost. Declining to attribute it was the right call, not a dodge.

**Strongest critique survives context.** The milliseconds-to-seconds (§1) vs time-scale-of-
minutes (§7) vs three-minute-average (Fig. 4) tension is real: all three passages read as
characterised, and the convergence hedge is the authors' own reply to the 13.42:1 outlier.

**Deliverable mechanics.** No `\documentclass`/`\usepackage`/`document` env. No labels, refs,
`\includegraphics`, absolute paths, or `\bibliography` at all, so no namespace collision is
possible. `lint_output.py` exits 0; OUTPUT holds `answer.tex` only. Compiles in a minimal
wrapper to 3 pages with no errors and no over/underfull boxes — so each paper clears the
"at least 1/3 page" floor. `downloads.md` records all three PDFs with URLs plus the dead
links tried.

**R8 length.** My count: 449 / 468 / 523 (the last includes the 35-word closing comparative)
= 1440 body words excluding references. Target 1250–1400. 2.9% over the ceiling, far inside
the "more than a quarter over" defect threshold. Em-dashes: 4 in ~1440 words.

### Defects
None blocking or major.

### Minor observations (noted, not blocking)
- [1.1] `answer.tex` L81: "CFS and its EEVDF successor both schedule by picking the
  minimum-virtual-time task". Exact for CFS; EEVDF actually selects the *eligible* task with
  the earliest *virtual deadline*. The point being made (stride's rule survives in Linux's
  lineage) is carried by CFS alone, so the argument is unaffected. | severity: minor
- [1.2] `answer.tex` L82-83: "no production kernel ever shipped the lottery" is an
  unprovable negative existential. Worker self-flagged it. "no mainstream kernel adopted it"
  would be safer. | severity: minor
- [1.3] `submission.md` justifies the multiprocessor absence claim partly by saying
  Buttazzo's "task model in §1 is explicitly uniprocessor"; the word `uniprocessor` does not
  appear in the paper. The claim in `answer.tex` is nonetheless true (verified by exhaustive
  search) — this is loose wording in the notes, not in the deliverable. | severity: minor

### Resolved since last round
N/A — first round.

### Still outstanding
Nothing substantive. Items 1.1–1.3 are cosmetic/precision nits in non-load-bearing
history-and-context sentences; none affects a graded claim about any of the three papers.
