# p2 notes — Ex. 2.2 + Ex. 2.3

## Ground truth check (R7)

The assignment is `input/hw2_instruction.md`, plain markdown. Ingest produced only
`ingest/pages/hw2_instruction/alltext.txt` — no `page_*.png`, no `page_*_fig_*.*`.
Verified with `ls`: the directory contains exactly one file. Verified with
`diff alltext.txt input/hw2_instruction.md` → identical. So the "three channels"
rule collapses to one channel here, and there is genuinely no figure content to
miss. The brief's transcription of Ex. 2.2 and Ex. 2.3 matches lines 9-18 of the
markdown verbatim. No discrepancy between brief and source.

## What each part needs

- **Ex. 2.2 — plain.** Argument only, no code, no diagram. Target ~190 words.
  Core claim: in case 1 the human does not create a process; the click/keystroke is
  an input event delivered to an already-running process (desktop shell, window
  manager, or command shell), and *that* process forks. Case 2 is identical
  mechanism, trigger is software rather than human. So 1 and 2 are instances of 3
  differing only in what prompted the running process to fork. Closing point: pid 1
  (init/systemd) is the one process the kernel hand-builds at boot; every other
  process descends from it by fork, which is what makes case 3 the general
  mechanism rather than a third alternative.
  Do NOT pad with copy-on-write tutorial.

- **Ex. 2.3 — code, actually run.** C program, fork() + execvp(), compiled with
  gcc 12.2.0 (/usr/bin/gcc, confirmed present) and executed. Must handle all three
  fork return cases, handle exec returning (= failure) with perror + _exit, and
  waitpid in the parent reporting exit status. Listing goes in answer.tex
  (explicitly asked for a program). Quote real trimmed output.

## Plan

1. Write `forkexec.c` in playground.
2. Compile: `gcc -Wall -Wextra -o forkexec forkexec.c`
3. Run it, capture real output to `run_output.txt`.
4. Also test the exec-failure path (rename target) to confirm the perror branch works.
5. Write answer.tex with lstlisting, style named `p2cstyle`.
6. preamble.txt: \usepackage{listings}, \usepackage{xcolor}.
7. lint_output.py, then submission.md.

No figure needed. No pip installs needed (gcc is system, not a download → nothing
to record in downloads.md).
