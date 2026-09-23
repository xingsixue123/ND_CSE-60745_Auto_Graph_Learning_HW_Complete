# p2 submission — Ex. 2.2 and Ex. 2.3

## What the problem asked

**Ex. 2.2 (5 pts).** Three ways a process can be created are listed: (1) a human
double-clicks an icon or types a command; (2) a running process creates a child
prompted by an external event; (3) a running process creates a child by explicitly
executing something like `fork()`. The question: explain why case 3 in general
covers cases 1 and 2.

**Ex. 2.3 (5 pts).** Write a small program that uses `fork()` and `exec()` to run
the `ls` command.

**Brief vs. source: no discrepancy.** The assignment is plain markdown at
`input/hw2_instruction.md`. Ingest produced only
`ingest/pages/hw2_instruction/alltext.txt` and no page PNGs or figure files — I
confirmed by listing that directory (exactly one file in it) and by
`diff alltext.txt input/hw2_instruction.md`, which reported them identical. So the
three-channel rule (R7) genuinely collapses to one channel here; there is no figure
in this assignment and nothing hidden in an image channel. The brief's verbatim
transcription matches lines 9–18 of the markdown word for word, including the
preamble instruction not to copy answers.

## What I decided it needed

- **Ex. 2.2 — plain.** An argument, no computation and no figure.
- **Ex. 2.3 — code, actually compiled and actually run.** The question asks for a
  program, so a listing in `answer.tex` is required rather than a code dump, and the
  quoted output has to be output I really saw. No diagram.

## What I did

For 2.2 I made the argument that cases 1 and 2 describe the *trigger* for creation,
not the *creator*. A click or a keystroke is an input event delivered by the kernel
to a process that is already running — the desktop shell/window manager, or the
command shell — and that process is what calls `fork()`. Case 2 is the identical
mechanism with a software trigger instead of a human one. I closed on the structural
reason this makes case 3 the general rule rather than one option of three: pid 1
(`init`/`systemd`) is the only process the kernel hand-builds at boot, and every
other process on the system is the child of some running process. Per the brief I
deliberately did not pad this with copy-on-write material.

For 2.3 I wrote `forkexec.c`, compiled it with the system gcc, and ran it in a
scratch directory containing two small files so the `ls` output would be short and
quotable. I then separately exercised the exec-failure path by running the same
binary with `PATH` pointed at a directory that does not exist, so the `perror` +
`_exit(127)` branch is demonstrated rather than merely asserted. I verified
programmatically that the listing pasted into `answer.tex` is byte-identical to the
`forkexec.c` I compiled, and that the quoted output block is byte-identical to the
captured `run_output.txt` — neither was retyped or tidied.

## Intermediate steps and code

All paths relative to PLAYGROUND.

| path | what it is |
|---|---|
| `notes.md` | the ground-truth check and the plan, written before starting |
| `forkexec.c` | the C program; the source of truth for the listing in `answer.tex` |
| `forkexec` | the compiled binary |
| `rundir/` | scratch dir holding `alpha.txt` (1 byte) and `beta.txt` (2 bytes), the two files `ls` reports |
| `run_output.txt` | real captured output of the normal run |
| `run_output_failpath.txt` | real captured output of the exec-failure run |
| `tex/` | compile test: `master.tex` wrapper, `build.log`, `master.pdf`, page PNGs I inspected |

Reproduce:

```sh
# compile (emits no warnings under -Wall -Wextra)
gcc -Wall -Wextra -o forkexec forkexec.c

# normal run -> run_output.txt
cd rundir && ../forkexec

# exec-failure branch -> run_output_failpath.txt
cd rundir && PATH=/nonexistent-dir ../forkexec
```

Compiler actually used: `gcc (Debian 12.2.0-14+deb12u1) 12.2.0` at `/usr/bin/gcc`.
gcc was present; I did not have to work around its absence.

## Results

Every concrete claim in `answer.tex` and where it came from:

- The quoted program output, verbatim from `run_output.txt`:

      total 8
      -rw-r--r-- 1 xing xing 1 Sep 21 16:37 alpha.txt
      -rw-r--r-- 1 xing xing 2 Sep 21 16:37 beta.txt
      parent: child 100 exited with status 0

  Child pid 100, exit status 0. Produced by `cd rundir && ../forkexec`.

- The failure-branch claim, verbatim from `run_output_failpath.txt`:

      execvp: No such file or directory
      parent: child 107 exited with status 127

  Produced by `cd rundir && PATH=/nonexistent-dir ../forkexec`. Status 127 is the
  `_exit(127)` in the child's exec-failed path, so the parent's `WEXITSTATUS`
  reporting is confirmed working too.

- `gcc 12.2.0, Debian Linux` — from `gcc --version`.
- `/usr/bin/ls` — from `which ls`. (I originally wrote `/bin/ls`; on this Debian 12
  box `/bin` is a symlink to `usr/bin` and `execvp`'s `PATH` search resolves to
  `/usr/bin/ls`, so I corrected it.)
- Word counts, measured with a script over the prose only (markup stripped, listings
  and the `lstdefinestyle` block excluded): Ex. 2.2 = 200 words, Ex. 2.3 prose = 218
  words, against the R8 target of ~190 for a 5-point answer. Both are inside the
  +25% threshold. Ex. 2.2 contains no em-dashes; Ex. 2.3 contains one.

Compile check: `answer.tex` was `\input` into a minimal `article` wrapper carrying
only the two packages from `preamble.txt`; `pdflatex` succeeded with zero warnings,
producing 2 pages. I rendered both pages to PNG and looked at them: the code frame,
the line numbers, the syntax colouring and the output block all render legibly, and
there is no stray empty caption.

## Deliverables

In OUTPUT:

- `answer.tex` — the fragment. Starts at `\section*{...}`, matching the style p1 of
  this same assignment used. Contains no `\documentclass`, `\usepackage`, or
  `document` environment (checked by grep). The only macro it defines is
  `\lstdefinestyle{p2cstyle}`, namespaced with the problem id. It defines no
  `\label` and references no figures.
- `preamble.txt` — `\usepackage{listings}` and `\usepackage{xcolor}`.
- No figures; this problem needs none.

`python3 framework/tools/lint_output.py output/hw_20260921_077701/p2` exits 0.

Nothing was downloaded or installed; `downloads.md` records that the only tool used
was the pre-existing system gcc.

## Where I am least confident

1. **The pid numbers in the quoted output are real but not reproducible.** A
   re-run gets a different pid, so a validator re-running the program will see
   `child <something else>`, not 100 and 107. The pids are genuine captures, not
   invented, but they cannot be matched by re-execution. Only the structure of the
   lines and the exit statuses (0 and 127) are reproducible.
2. **`ls -l` output depends on the directory.** I quote the listing of
   `rundir/`, which I created for the purpose. A validator running the binary from a
   different cwd will get different file lines. I used `-l` rather than bare `ls` so
   the output was unambiguously real; a validator wanting an exact match should
   `cd rundir` first. The timestamps will still differ from any fresh recreation of
   those files.
3. **Length of Ex. 2.3.** At 218 prose words it is over the ~190 target, though
   inside the +25% band. If it needs to come down, the most cuttable sentence is the
   `_exit`-versus-`exit` stdio-buffer explanation, which is a real and defensible
   point but is the least central to "what each branch does".
4. **The claim about pid 1 in Ex. 2.2.** It is correct for Unix/Linux as the
   question frames it, but I stated it as a flat fact; strictly, the kernel also
   hand-builds internal kernel threads (pid 2, `kthreadd`, and its children) that are
   not forked from pid 1 by a userspace process. I judged that out of scope for a
   5-point question framed around `fork()` and did not qualify it. If a grader is
   pedantic about "exactly one process is not born this way", that is the sentence
   they would flag.
5. **The `\section*` level.** I matched p1 of this assignment, which uses
   unnumbered `\section*`. If the master expects numbered `\section`, this is a
   one-character change, but I could not see the master document to confirm.
