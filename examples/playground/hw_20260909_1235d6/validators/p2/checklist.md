# Validator checklist — p2 (Ex. 1.5–1.8)

## Round 1
Verdict: PASS

### What I verified independently (not taken from the submission)

**Source fidelity.** Read `input/hw_questions.md` myself. The brief's transcription of
Ex. 1.5 (line 21), 1.6 (line 25), 1.7 (line 29), 1.8 (line 33) is verbatim correct.
No brief-vs-source discrepancy. All four questions are in scope and all are answered.

**Sub-part coverage.** Every question decomposed and checked:
- 1.5 has two halves ("Why not?" + "What are the reasonable assumptions ... where and
  how?"). Both answered; the *assumptions* half (logical space starting at 0,
  contiguous, binding deferred) is present and is where half the marks sit.
- 1.6 asks two cases (double-click / typed command) plus "all the steps". Both cases
  covered, 11-step chain, plus the observation that the two differ only in how argv is
  assembled.
- 1.7 and 1.8 answered.

**R7 / figures.** Did not take the worker's word. Parsed `ingest/manifest.json` myself:
two entries only — `hw_questions.md` (kind `text_document`, `rendered: None`) and
`PaperList.xlsx` (6 pages, every page `n_images: 0`, `figures: []`). There is genuinely
no figure content in this problem, so the three-channel reconciliation has nothing to
apply to. The worker's reasoning here is correct, not an evasion.

**plain/code/diagram decision.** Agreed: no question says plot/draw/show/illustrate, and
none asks for a computed number, count, distribution or ranking. The only arithmetic is
the illustrative base/limit example. Not writing a script to compute `14000 + 346` is the
right call, and the worker was explicit about it rather than letting it look like a
skipped step.

**Numbers.** Re-derived by hand: base 14000, limit 3000; VA 346 < 3000 → PA 14346 (correct);
VA 3200 ≥ 3000 → trap (correct per the stated rule). No fabricated values — there are no
computed values to fabricate.

**Technical accuracy** (checked claim by claim, adversarially):
- 1.5: compile-once/run-many, ASLR, demand paging, assume origin 0 + contiguous,
  compile-/load-/execution-time binding trichotomy — all correct.
- 1.6: fork(COW) → exec → permission check → magic number selects format → address space
  rebuilt → mmap'd segments → `ld.so` (PT_INTERP) runs before `main()` and relocates →
  PCB/ready queue → dispatch → demand paging → window system. Chain is correct and in the
  right order. Shell `wait()`s, GUI launcher does not — correct.
- 1.7: check-then-add ordering stated explicitly; privileged loading of base/limit;
  process confined to `[0, limit)`. Correct.
- 1.8: preemptive FCFS + quantum, circular ready queue, ~1/n of CPU, wait ≤ (n−1)q,
  quantum trade-off both directions, no starvation, avg turnaround worse than SJF.
  All correct; matches the standard result without reading as lifted phrasing.

**Compile.** Copied `answer.tex` into my own dir and built it two ways:
- 1in-geometry wrapper: exit 0 both passes, 2 pages, `grep` for
  warning/overfull/underfull returns nothing. Confirms the worker's claim.
- Strict wrapper using *only* the two lines of `preamble.txt`: exit 0. Confirms
  `preamble.txt` declares exactly the packages the fragment needs (amsmath for
  `cases`/`align*`/`\text`, enumitem for the optioned `enumerate`) — nothing silently
  missing.

**R5 compliance.** `grep` for `documentclass|usepackage|begin{document}|end{document}`
in `answer.tex` → no matches. Exactly one label, `p2:eq:reloc`, correctly namespaced.
No `\includegraphics`, no absolute paths.

**R4 / lint.** `python3 framework/tools/lint_output.py output/hw_20260909_1235d6/p2` →
`OUTPUT LINT OK`, exit 0. OUTPUT contains only `answer.tex` and `preamble.txt`.

**R3 / downloads.** `downloads.md` records `(nothing installed)`; the playground confirms
it — no venv, no fetched packages, only `build/` render artifacts.

**Visual.** Rendered to PNG at 150 dpi and read both pages back. All four `\subsection*`
headings present with the assignment's exact numbering; the `cases` equation, the
`align*` worked example and the 11-item list all set correctly and are legible.

**Honesty spot-check.** The submission reports that its first compile hard-failed on
`\texttt{\$PATH}` via a missing TS1 typewriter font. I reproduced it: exit 1,
`mktexpk ... tctt1000`. The war story is true and the fix (drop the sigil rather than
push `\usepackage[T1]{fontenc}` into the shared master preamble) is the right call —
changing font encoding for the whole assembled document to fix one character would have
been an inappropriate side effect on other workers' fragments.

### Defects
- [1.1] Compiled against the default `article` text width (no `geometry`), the fragment
  produces one Overfull \hbox, 7.19pt, at `answer.tex` lines 58--60 (the
  `\texttt{main()}` list item). At 1in margins there are zero overfull boxes, so whether
  this ever appears depends on the master's page geometry, which is not knowable from
  here. | `OUTPUT/answer.tex:58-60` | severity: minor
- [1.2] `\label{p2:eq:reloc}` is defined but never `\ref`'d, so Ex. 1.7 carries a
  numbered equation nothing points at. Correctly namespaced, so it cannot collide; purely
  cosmetic. Worker self-flagged this. | `OUTPUT/answer.tex:77` | severity: minor
- [1.3] Notational infelicity in equation (1): the second branch reads
  `physical = addressing trap to the OS`, i.e. an address is equated to a control-flow
  event. Unambiguous to any grader, but strictly a type mismatch. | `OUTPUT/answer.tex:81`
  | severity: minor

None of these is blocking. Per my mandate, when the remaining objections are all
cosmetic the correct action is to pass and note them.

### Considered and explicitly NOT raised as defects
- **Length.** The worker's own top-listed worry was overshooting "just few sentences".
  I checked this rather than reflexively agreeing: the whole fragment is 2 rendered pages
  for four 5-point questions — roughly half a page each. Ex. 1.6's own wording is
  "Describe **all** the steps", which licenses the 11-item list, and Ex. 1.5 genuinely has
  two halves plus the binding trichotomy. Cutting to three sentences would drop ticked
  items. Current length is appropriate; no change wanted.
- **Ex. 1.7 read generously.** The question is a sentence fragment, not a question.
  Reading "finding" as "demonstrate the procedure" and supplying rule + bounds check +
  worked example + trap case is the interpretation that maximises marks. Correct call.
- **No code run.** Correct for this problem; running a script to add two integers would
  be theatre, and the worker said so up front instead of hiding it.

### Resolved since last round
(none — first round)

### Still outstanding
[1.1], [1.2], [1.3] — all minor, all optional. Passing regardless.
