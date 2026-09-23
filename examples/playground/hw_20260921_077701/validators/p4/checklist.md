# p4 validator checklist — Ex. 2.5 (20 pts) + Ex. 2.6 (5 pts)

## Round 1
Verdict: PASS

### What I verified independently (not by reading the worker's claims)

**Ground truth (R7).** The assignment is `input/hw2_instruction.md`, plain markdown,
37 lines. Ingest produced exactly one artefact,
`ingest/pages/hw2_instruction/alltext.txt`; I ran `diff` against the input myself —
IDENTICAL. There are no page PNGs and no figure files because the document contains
no figure, so the text channel is the only channel that exists. Nothing in this
problem depends on a figure, so the R7 image/figure requirements are vacuous here
rather than skipped. I read line 26 (Ex. 2.5) and line 30 (Ex. 2.6) of the source
directly: **the brief's transcription is verbatim correct, hint included.** I also
read the whole file for any global instruction the brief might have dropped — the
only one is the preamble's "put the answers in your own way", which the brief
carries. No discrepancy between brief and source.

**The hint / the trap.** Ex. 2.5 says "write code to implement each system call, not
use these system calls in some code". All four floats are kernel-side implementations
operating on the process table and PCB (`\textsc{Current}`, `AllocatePCB`,
`FreePid`, `Sleep` on a wait channel, `Schedule`). There is no `pid = fork(); if
(pid==0) exec(...)` anywhere. The worker did not fall into the trap.

**Coverage against the brief's required elements — all four algorithms, item by item:**
- `fork`: `EAGAIN` on exhausted slot/pid (l.14–16); PCB field copy incl. uid/gid/cwd/
  root/umask/signal dispositions/limits (l.18–19); COW address space (l.21–23);
  per-descriptor refcount increment (l.24–27); link into `children` (l.20);
  **child's saved return register ← 0 (l.31) and parent returns child pid (l.34)**;
  ready queue (l.33). Complete.
- `exec`: `namei` + `ENOENT`/`EACCES` (l.49–52); **magic number selects loader**,
  `ENOEXEC` (l.53–56); argv/envp copied into kernel *before* teardown (l.57–58);
  teardown (l.61); map text/data/bss + fresh heap and stack (l.62–64); caught signals
  reset to default with ignored dispositions and blocked mask preserved (l.65–70);
  close-on-exec (l.71); set-uid (l.72–73); args pushed (l.74); PC ← entry (l.75–76);
  annotated that it does not return on success (l.77–78). Complete.
- `waitpid`: rescan loop; `ECHILD` when no child matches at all (l.103); on a ZOMBIE
  child — copy out status, accumulate child CPU time, unlink, `FreePCB`+`FreePid`
  labelled "the reaping step", return pid (l.93–100); `WNOHANG` → 0 (l.104); sleep on
  wait channel (l.106). Complete.
- `exit`: close all descriptors dropping refcounts (l.118–121); release address space
  and cwd/root/timers/locks (l.122–123); **re-parent children to `init` and wake
  `init` for any already zombie** (l.124–129); save status and accounting (l.130);
  mark ZOMBIE with PCB and pid retained (l.131–132); `SIGCHLD` + wakeup to parent
  (l.133–134); `Schedule`, never returns (l.135–136). Complete.

**Technical spot-checks I did not take on trust.** `c.pending signals ← ∅` and
`c.cputime ← 0` in fork are correct POSIX (pending signals are not inherited).
`Current.childcputime += c.cputime + c.childcputime` in waitpid correctly accumulates
the grandchild-inclusive total. The 2.6 claims that `SIGKILL` is discarded for a
zombie, that `ps` shows `Z` / `<defunct>`, that `init` adopts and reaps on parent
death, and that `SIG_IGN` on `SIGCHLD` prevents the leak are all correct.

**Inter-relation explanation (the part carrying the marks).** Present as its own
subsection, argued as two pairs bracketing a process's life rather than four bullets:
fork+exec are jointly necessary to run a new program, the split buys the descriptor
window (worked through with `ls > out`), exit+waitpid are a pair because the status
must outlive the process, and the pid stays reserved so "wait for process p" stays
unambiguous. Closes with the shell's cycle in one sentence, which is what the brief
asked for. This is the strongest part of the answer.

**Numbers / computation.** There is nothing to compute in this problem and the worker
correctly declined to invent any. No numeric claim appears in `answer.tex`.

**Figure.** Optional per the brief (`fig_p4_lifecycle.pdf`). The worker declined and
gave a reason. Declining an explicitly optional deliverable is not a defect.

**LaTeX, compiled by me in my own wrapper** (`validators/p4/vbuild/`, my own
`wrap.tex` loading only geometry/amsmath/amssymb/algorithm/algpseudocode):
`pdflatex -halt-on-error` exit 0, 4 pages, `grep -c "Overfull\|Underfull" wrap.log`
→ **0**. This independently reproduces the worker's claim. Note `[H]` works without
my requesting `float`, confirming `algorithm.sty` pulls it in, so `preamble.txt`
(`algorithm` + `algpseudocode`) is sufficient and minimal.

**R5 compliance.** `grep -n "documentclass\|usepackage\|begin{document}\|end{document}"`
over `answer.tex` → no matches. No `\newcommand`/`\def`/`\renewcommand`, no
`\includegraphics`, no absolute path, no `\input`. All four labels namespaced:
`p4:alg:fork`, `p4:alg:exec`, `p4:alg:waitpid`, `p4:alg:exit`. Nothing can collide
with another problem.

**Figure/render legibility.** Rendered all 4 pages at 150 dpi and read them. Layout is
clean: no `\Comment` wraps onto the following line, no clipped text, the `\Statex`
continuation lines are correctly unnumbered. `pdftotext -f 3 -l 4` confirms `ls > out`
and `<defunct>` render as literal glyphs, not mangled.

**R8 length.** I counted the words myself with my own macro-stripping script rather
than trusting the worker's count, and got the same numbers: inter-relation explanation
**340** (target 300–350, in band), Ex. 2.6 **223** (target 190–220). 223 is 1.4% over,
far inside R8's "more than a quarter" defect threshold. Plus 58 words of notation
setup and a 37-word note under Algorithm 1; 658 words of prose total for 25 points.
Not bloated — I looked specifically for R8's four failure modes and found no
exhaustive enumeration, no closing sentence restating the opening, and no
"it is worth noting that".

**R9.** No quotation and no characterisation of what any source says or fails to say
appears anywhere in `answer.tex`. I grepped for quotation marks and citation-like
constructions; the only quoted strings are LaTeX typographic quotes around the phrase
"fork returns twice", which is the worker's own coinage, not a source. R9 does not
apply.

**R3 / R4.** `downloads.md` exists and reads `- (nothing installed)`, which matches —
nothing was installed and no venv exists in the playground.
`python3 framework/tools/lint_output.py <OUTPUT>` → `OUTPUT LINT OK`, exit 0. OUTPUT
contains only `answer.tex` and `preamble.txt`; all build artefacts are in
`playground/problems/p4/build/`, where they belong.

### Defects

- [1.1] The inter-relation section says `exec` "keeps exactly that [descriptor] table,
  less the close-on-exec entries, while discarding everything else"
  (`answer.tex:151-152`). This is looser than the worker's own Algorithm 2, which
  correctly preserves ignored signal dispositions, the blocked mask and the
  credentials (l.69–70, and set-uid is conditional at l.72). "Everything else" reads
  in context as the program image, which is the contrast being drawn, but a careful
  grader could read it as contradicting the algorithm two pages earlier. |
  `OUTPUT/answer.tex:151-152` | severity: minor
- [1.2] Ex. 2.6 is 223 words against the brief's 190–220 band
  (`answer.tex:177-198`). Three words over; well inside R8's tolerance. Not worth a
  round trip. | `OUTPUT/answer.tex:177-198` | severity: minor
- [1.3] Algorithm 2 marks the "point of no return" and says every error above it is
  reportable, but never says what happens if a step *below* it fails — in a real
  kernel the process is killed, since there is no caller left to return to. One
  `\Comment` would close it. The brief did not require it and nothing stated is
  wrong. | `OUTPUT/answer.tex:59-61` | severity: minor

### Resolved since last round
(first round — none)

### Still outstanding
[1.1], [1.2], [1.3] — all minor, all cosmetic or stylistic. Per the validator brief,
remaining objections that are all cosmetic do not justify a FAIL. Passed with these
noted; the master may apply them or not.
