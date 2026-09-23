# Validator checklist — p2 (Ex. 2.2 + Ex. 2.3)

## Round 1
Verdict: PASS

### Checks performed (all independently re-run, not taken from the submission)

**Ground truth (R7).** Read `input/hw2_instruction.md` directly. The Ex. 2.2 and
Ex. 2.3 text in the brief is verbatim, including the three case lines and the
preamble instruction. Confirmed `ingest/pages/hw2_instruction/` contains exactly
one file (`alltext.txt`) and that it is byte-identical to the input markdown
(`diff` → identical). `find` for PNG/figure files under ingest returns hits only
for `PaperList/` (a different document, not p2). So the three-channel rule
genuinely collapses to one channel here and no figure content was missed. The
worker's "no discrepancy" claim is accurate.

**Did it answer the actual question?** Ex. 2.2 asks *why* case 3 covers cases 1
and 2. The answer makes the required argument: cases 1 and 2 name the *trigger*,
not the *creator*; the click/keystroke is an input event delivered to an
already-running process (desktop shell / window manager / command shell) which is
what calls `fork()`; case 2 is the same mechanism with a software trigger; plus
the structural closer that pid 1 is the only process not created this way.
Ex. 2.3 asks for a program using `fork()` and `exec()` to run `ls` — delivered as
a listing plus explanation. Both sub-parts present.

**Are the numbers real?** Re-compiled and re-ran the worker's program myself in
`recheck/` (copied `forkexec.c`; `diff` against the worker's copy → identical):
- `gcc -Wall -Wextra -o forkexec forkexec.c` → exit 0, `compile.log` is 0 bytes
  (zero warnings, as claimed).
- `gcc --version` → `gcc (Debian 12.2.0-14+deb12u1) 12.2.0`. Matches the answer.
- Normal run in a 2-file dir reproduced the exact structure: `total 8`, a 1-byte
  and a 2-byte file, then `parent: child 105 exited with status 0`.
- Failure branch `PATH=/nonexistent-dir ../forkexec` reproduced exactly:
  `execvp: No such file or directory` / `parent: child 115 exited with status 127`.
- `which ls` → `/usr/bin/ls`; `/bin` is a symlink to `usr/bin`. The answer's
  `/usr/bin/ls` is correct (the worker's noted self-correction was the right call).
- The pids 100/107 in the quoted output differ from my 105/115, but pids are
  inherently per-run and the low values confirm a PID namespace, so 100/107 are
  plausible genuine captures rather than invented. Structure and exit statuses
  (0, 127) reproduce exactly. Disclosed honestly by the worker.
- Audited every numeric literal in `answer.tex`: 100/107 (captures), 12.2 (gcc),
  127 (`_exit`), 16/21/37 (the `Sep 21 16:37` timestamps in the captured `ls`
  output), 2.2/2.3 (exercise numbers), 50/60 (xcolor blend percentages). No
  unsourced number.

**Byte-identity of quoted material.** Script-extracted both `lstlisting` blocks
from `answer.tex`: block 1 is byte-identical to `forkexec.c`, block 2 is
byte-identical to `run_output.txt`. Nothing was retyped or tidied.

**Did it do the required work?** Problem needed code actually run — it was.
Program handles all three `fork()` outcomes (`<0`, `==0`, `>0`), uses `execvp`,
handles exec returning with `perror` + `_exit(127)`, and the parent `waitpid`s and
reports status via `WIFEXITED`/`WEXITSTATUS` (with a `WIFSIGNALED` arm too). No
diagram is required by either sub-part; none supplied, correctly.

**Technical prose accuracy.** Spot-checked each claim: `exec` never returns on
success; `execvp` searches `PATH` and keeps the pid; `_exit` vs `exit` avoids
flushing the child's copy of the parent's stdio buffers; `waitpid` reaps the child
preventing a zombie. All correct.

**LaTeX / R5.** No `\documentclass`, `\usepackage`, `\begin{document}` or
`\end{document}` (grep-verified). No `\label` and no `\includegraphics` at all, so
no namespacing collisions possible. The single macro defined is
`\lstdefinestyle{p2cstyle}` — correctly namespaced with the problem id. Compiled
the fragment myself in a minimal `article` wrapper carrying only the two packages
from `preamble.txt`: `pdflatex` exit 0, 2 pages, zero warnings, no Overfull/
Underfull boxes. Rendered both pages to PNG and looked at them, plus a 4x upscaled
crop of the output block: code frame, line numbers, comments and the `ls -l`
permission strings (`-rw-r--r--`) all render legibly and faithfully.
`\section*` level matches p1 of this same assignment.

**OUTPUT clean (R4).** `python3 framework/tools/lint_output.py
output/hw_20260921_077701/p2` → `OUTPUT LINT OK`, exit 0. Directory holds only
`answer.tex` and `preamble.txt`. `preamble.txt` is `\usepackage{listings}` +
`\usepackage{xcolor}`, both de-dupable against p1's.

**Downloads (R3).** `downloads.md` present and correctly records
`(nothing installed)` — gcc is pre-existing system software, not a download.

**Length (R8).** Independently counted prose with markup stripped and listings and
the `lstdefinestyle` block excluded: Ex. 2.2 = 200 words, Ex. 2.3 = 211 words,
against a ~190 target (+25% band = 237). Both inside. Zero `---` em-dashes in
either. No padding, no copy-on-write tutorial (the brief explicitly warned against
it), no self-summarising closer.

**R9.** No external source is quoted or characterised anywhere in the answer, so
R9 is not engaged.

### Defects
None blocking or major.

- [1.1] Ex. 2.2 states "exactly one process is not born this way ... pid 1" |
  `answer.tex:18-19` | severity: minor. Strictly, on Linux the kernel also
  hand-builds kernel threads (`kthreadd`, pid 2, and its descendants), so "exactly
  one" is not literally true of a running Linux system. This is the standard
  textbook framing for a question posed at the level of "three ways a process can
  be created", the question is about user-visible processes and `fork()`, and the
  worker identified the same point himself in his uncertainty list. Not worth a
  round trip; recording it so the master is aware. No fix required.

### Resolved since last round
N/A — first round.

### Still outstanding
[1.1] only, deliberately not requiring a fix (cosmetic/pedantic).
