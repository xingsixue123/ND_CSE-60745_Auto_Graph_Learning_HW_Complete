# p3 — worker validator checklist

## Round 1
Verdict: FAIL

### What I verified independently (all passed)
- **Ground truth (R7).** Assignment is `input/hw2_instruction.md`, a markdown file; no
  PNGs/figure files exist for it (`ingest/pages/hw2_instruction/` holds only
  `alltext.txt`). `diff input/hw2_instruction.md
  playground/.../ingest/pages/hw2_instruction/alltext.txt` → identical. Line 22 reads
  exactly the text in the brief. Brief transcription confirmed correct; Ex. 2.4 refers
  to no figure, so nothing had to be transcribed from an image.
- **Question actually answered.** "Explain why" → causal explanation delivered. Every
  link the brief names is present: same-process scoping; shared address space → no
  `CR3`/`TTBR` reload → no TLB invalidation; indirect cost (cold TLB, displaced cache)
  as the larger half; tagged-TLB caveat held to one sentence; what is still saved
  (register file incl. PC/SP, kernel stack/TCB); per-process state (open-file table,
  signal dispositions) not swapped; user-level switch skips the kernel trap.
- **Technical correctness.** No error found. Notably it avoids the common wrong claim
  that caches are *flushed* on a process switch — it correctly says they are polluted
  /displaced. Causality `CR3` reload → TLB invalidation is right, and the PCID/ASID
  qualification is correctly stated as softening not removing.
- **Deliverable type.** plain; no code result and no figure required. Correct call —
  nothing in the question asks for a computation or a drawing. No fabricated numbers:
  `answer.tex` contains no numeric result at all.
- **R5 fragment check.** No `\documentclass`, `\usepackage`, `\begin{document}`,
  `\end{document}`. No `\label{}` and no `\includegraphics` at all, so no namespacing
  collision is possible.
- **Compile.** Copied nothing; `\input` the fragment into my own minimal wrapper
  (`validators/p3/vbuild/wrap.tex`, article + geometry only):
  `pdflatex -interaction=nonstopmode -halt-on-error wrap.tex` → exit 0, 1 page, zero
  overfull/underfull/undefined. Rendered `pdftoppm -png -r 110` and read it back: clean
  three-paragraph page, no broken markup.
- **R8 length.** My own count of the body (macros and braces stripped, heading
  excluded) = **212 words**, matching the worker's claim exactly. Target 190, defect
  threshold 237.5 (+25%). 212 is +11.6% — under threshold, **not** a defect. Em-dash
  density 1 per 212 words, fine.
- **R4 OUTPUT clean.** `python3 framework/tools/lint_output.py
  output/hw_20260921_077701/p3` → `OUTPUT LINT OK`, exit 0. OUTPUT holds exactly
  `answer.tex`; all scratch (`build/test.tex`, `test.pdf`, `render-1.png`) stayed in
  PLAYGROUND.
- **R3 downloads.** `PLAYGROUND/downloads.md` records `- (nothing installed)`; nothing
  in the playground contradicts it (no venv, no downloaded assets).
- **R9.** `answer.tex` quotes no source and characterises no author's claim, so there
  is no quotation surface to check. Confirmed by reading the fragment in full.

### Defects
- [1.1] Wrong sectioning level. `OUTPUT/answer.tex:1` opens with `\subsection*{...}`.
  R5 says the fragment "starts at the section level", and both sibling problems do:
  `output/hw_20260921_077701/p1/answer.tex:1` and `p2/answer.tex:1` both use
  `\section*{...}`. When the master `\input`s all three in order, p3's answer will be
  typeset as a subsection and will read as if it were a sub-part of Ex. 2.2 rather than
  a question in its own right. | `OUTPUT/answer.tex` line 1 | severity: major
  Fix: change `\subsection*` to `\section*` on line 1. Nothing else in the file depends
  on it.

### Non-defects I considered and am not raising
- 212 words vs the 190 target — within the +25% tolerance R8 sets; the prose has no
  restatement, no "it is worth noting", no padding paragraph. Not a defect. Do not
  spend a round shortening it.
- "the register saving is the smaller half of its bill" — an unsourced qualitative
  claim, flagged by the worker itself. It is standard and correct, the brief explicitly
  says measured numbers are not needed, and the answer commits to no figure. Fine.
- Omission of FPU/SIMD state and scheduler bookkeeping — a deliberate choice the brief
  supports ("do not turn this into a table"). Fine.

### Resolved since last round
- (none — first round)

### Still outstanding
- [1.1] `\subsection*` → `\section*` in `OUTPUT/answer.tex:1`.

## Round 2
Verdict: PASS

### Defects
- (none)

### Resolved since last round
- **[1.1] major — wrong sectioning level. RESOLVED.** `OUTPUT/answer.tex:1` is now
  `\section*{Ex.~2.4 (5 pts) --- ...}`. Verified independently, not taken on the
  worker's word:
  - the string `subsection` no longer appears anywhere in the file;
  - `head -1` across all three siblings now agrees — `p1`, `p2` and `p3` all open with
    `\section*{...}`, so the assembled document will typeset Ex. 2.4 at the same level
    as Ex. 2.1 and Ex. 2.2 instead of nesting it under Ex. 2.2;
  - the fix really was one token and no prose was smuggled in with it: file size went
    1402 → 1399 bytes, exactly the three characters of `sub`, and lines 3–21 are
    character-identical to the round-1 text I recorded;
  - recompiled my own wrapper (`validators/p3/vbuild/wrap.tex`): exit 0, 1 page, zero
    overfull/underfull/undefined/warning lines; re-rendered at 110 dpi and read the
    page back — heading now sets at section weight over two lines, body unchanged and
    clean.

### Re-verified after the fix (no regressions)
- **R5.** No `\documentclass`, `\usepackage`, `\begin{document}`, `\end{document}`.
  No `\label` and no `\includegraphics` at all → no namespacing collision possible.
  No absolute paths in the fragment.
- **R8 length.** Body still **212 words** by my own count (macros/braces stripped,
  heading excluded) — unchanged, as I required. Target 190, threshold 237.5. Fine.
- **R4 OUTPUT clean.** `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT holds
  exactly `answer.tex` (1399 bytes). All round-2 scratch (`assembled.tex/.pdf/.log/
  .aux`, `p3only.tex`, `fixed-1.png`) correctly stayed in PLAYGROUND/build.
- **R3 downloads.** `downloads.md` still records `- (nothing installed)`; playground
  contains no venv, no clone, no downloaded asset. Consistent.
- **R7 / content.** Ground truth re-confirmed in round 1 against
  `input/hw2_instruction.md:22`; question text unchanged, no figure involved. The
  causal chain the brief asks for is intact and technically correct.

### Still outstanding
- (nothing)

### Noted, not defects — for the master's information
- The answer's "the register saving is the smaller half of a process switch's bill" is
  a qualitative, unsourced claim. It is standard and correct, and the brief explicitly
  says measured numbers are not required. No action.
- 212 words vs the 190 target (+11.6%) is inside R8's tolerance. Deliberately left
  alone; shortening it would cost a link in the chain.
