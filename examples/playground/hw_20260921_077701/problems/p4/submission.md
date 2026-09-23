# p4 submission — Ex. 2.5 (20 pts) + Ex. 2.6 (5 pts)

## What the problem asked

Ex. 2.5: write pseudo-code for `exec()`, `fork()`, `waitpid()` and `exit()`, and explain
how the four are inter-related. The hint is the trap: *"write code to implement each
system call, not use these system calls in some code"* — i.e. the kernel-side
implementation, not a user program that calls `fork()`.

Ex. 2.6: what a zombie process is.

**Source check (R7).** The assignment is `input/hw2_instruction.md`, plain markdown.
`ingest/pages/hw2_instruction/` contains exactly one file, `alltext.txt` — no page PNGs
and no figure files, so the text channel is the only channel that exists here, and
`diff input/hw2_instruction.md ingest/.../alltext.txt` reports the two IDENTICAL. The
document contains no figure anywhere, so there is nothing for the image/figure channels
to carry. Line 26 (Ex. 2.5) and line 30 (Ex. 2.6) of the markdown match the brief's
transcription word for word, hint included. **No discrepancy between the brief and the
assignment page.**

The brief's note about the arithmetic in 2.5 (4 × 2.5 + 2.5 = 12.5 ≠ 20) is correct and
is in the source; per the brief I did not try to reconcile it.

## What I decided it needed

**plain only.** There is nothing to compute (no data, no numeric answer) and nothing to
execute — "write a pseudo-code" is explicitly pseudo-code, and running it is not
possible or asked for. I deliberately did **not** make the optional
`fig_p4_lifecycle.pdf` state diagram: the brief marks it optional, it earns no mark the
prose does not already earn, and the brief itself says the right way to close the
explanation is a lifecycle sketch in words. So there is no figure in OUTPUT by choice,
not by omission.

The only thing that needed verifying by running something was the LaTeX: that the
fragment compiles, has no overfull lines, and renders legibly.

## What I did

Four `algorithm`/`algpseudocode` floats, each the kernel-side implementation operating on
the process table / PCB, with `\textsc{Current}` as the caller's PCB and negative
`errno`-style returns:

- **`fork`** — `EAGAIN` on exhausted PCB slot or pid; copy of uid/gid/cwd/root/umask/
  signal dispositions/limits; copy-on-write address space with writable pages marked
  read-only in both; per-descriptor reference-count increment; link into the parent's
  child list; **child's saved return register set to 0 and the parent's to the child pid**
  (the "returns twice" phenomenon, called out in one sentence under the float); enqueue on
  the ready queue.
- **`exec`** — `namei`, permission check (`ENOENT`/`EACCES`), **magic number selects the
  loader** (`ENOEXEC` otherwise); `argv`/`envp` copied into the kernel *before* the old
  address space is destroyed, with an explicit "point of no return" marker separating the
  reportable errors from the irreversible part; map text/data/bss rather than read; caught
  signals reset to default while ignored dispositions and the blocked mask survive;
  close-on-exec descriptors closed; set-uid; args pushed on the new stack; saved PC set to
  the entry point; annotated that on success it **does not return to the caller**.
- **`waitpid`** — rescan loop; `ECHILD` when no matching child exists at all; on a
  `ZOMBIE` child: copy out status, accumulate child CPU time, unlink, `FreePCB` +
  `FreePid` (labelled "the reaping step"), return the pid; else `WNOHANG` → 0, `EINTR` on
  a pending signal, otherwise sleep on the wait channel.
- **`exit`** — close all descriptors (dropping file reference counts), release the address
  space and cwd/root/timers/locks, **re-parent children to `init`** and signal/wake `init`
  for any that are already zombies, save status and accounting in the PCB, mark `ZOMBIE`
  (PCB and pid stay allocated), `SIGCHLD` + wakeup to the parent, call the scheduler and
  never return.

Then the inter-relation explanation as two pairs bracketing a process's life
(fork+exec = the only way to run a new program, and why the split buys the
redirection window; exit+waitpid = the status must outlive the child), closed with the
shell's cycle in one sentence. Then Ex. 2.6.

## Intermediate steps and code

No computation, so no result-producing scripts. The only executed artefacts are the
LaTeX build and the render checks, all in `build/`:

- `build/wrap.tex` — throwaway wrapper (`\documentclass`, geometry, amsmath, amssymb,
  algorithm, algpseudocode) that `\input`s a copy of the deliverable.
  Reproduce: `cd build && cp <OUTPUT>/answer.tex . && pdflatex -halt-on-error wrap.tex`.
  Result: exit 0, 4 pages, **zero Overfull/Underfull boxes**
  (`grep -n "Overfull\|Underfull" build/wrap.log` is empty).
- `build/f-*.png`, `build/*_zoom*.png`, `build/final_p*.png` — `pdftoppm -r 150` renders
  plus PIL LANCZOS crops that I read back to check the pseudo-code layout. Two rounds:
  the first showed three `\Comment`s wrapping onto the next line at the left margin
  (fork's copy-on-write comment, exec's BuildImage comment, exit's ZOMBIE comment), which
  I fixed by shortening them / splitting them into separate `\State` lines; the second
  render is clean.
- `<` and `>` inside `\texttt{}` (in `ls > out` and `<defunct>`) were checked explicitly
  with `pdftotext -f 3 -l 4 build/wrap.pdf`, which reports them as literal `>` and
  `<defunct>` — cmtt has those glyphs, so no `\textless`/`\textgreater` is needed.

Word counts (R8), counted with a regex strip of LaTeX macros, headings excluded:
**inter-relation explanation 340 words** (target 300–350), **Ex. 2.6 223 words**
(target 190–220, over by 1.4%). The intro paragraph before Algorithm 1 is a further 61
words setting the notation.

## Results

Nothing in `answer.tex` is a computed value — there are no numbers to reproduce. The two
verifiable claims about the deliverable itself are:

| claim | how checked |
|---|---|
| the fragment compiles standalone | `pdflatex -halt-on-error` in `build/`, exit 0, 4 pages |
| no overfull/underfull boxes | `grep "Overfull\|Underfull" build/wrap.log` → no matches |
| R5: no `\documentclass`/`\usepackage`/`document` env | `grep` over `answer.tex` → no matches |
| all four labels namespaced | `p4:alg:fork`, `p4:alg:exec`, `p4:alg:waitpid`, `p4:alg:exit` |
| OUTPUT clean | `framework/tools/lint_output.py` → `OUTPUT LINT OK` |

## Deliverables

- `<OUTPUT>/answer.tex` — the fragment: four algorithm floats, the inter-relation
  explanation, and Ex. 2.6.
- `<OUTPUT>/preamble.txt` — `\usepackage{algorithm}` and `\usepackage{algpseudocode}`
  (both installed; `algorithm.sty` pulls in `float` itself, so `[H]` works without my
  requesting `float`).
- No figures, by the decision explained above.

## Where I am least confident

1. **Ex. 2.6 is 223 words against a 190–220 target.** Three words over. I judged the
   orphan/zombie distinction and the `EAGAIN` leak sentence worth keeping rather than
   trimming further, but if the validator wants it inside the band the last paragraph is
   the cheapest cut.
2. **Level of detail in the pseudo-code is a judgement call.** I aimed at "a grader who
   knows Unix but not Linux source": no `task_struct`, no `mm_struct`, no
   `copy_process()`. A grader expecting something closer to real kernel identifiers would
   find these abstract. I think the brief asks for exactly this level.
3. **`EINTR` in `waitpid` and set-uid in `exec`** are correct POSIX behaviour but were not
   demanded by the brief; they add two lines each. If the validator reads them as padding
   they can go without damaging the answer.
4. **Signal-disposition semantics across `exec`** are the subtlest line in the four
   algorithms: caught signals revert to default, `SIG_IGN` is preserved, and the blocked
   mask is inherited. I have stated all three, and I am confident in them, but they are
   the place where a reader most likely disagrees with the phrasing.
5. **The "point of no return" marker in `exec`** is my framing, not standard pseudo-code
   notation. It is there because it is the one structural fact about `exec` that the code
   would otherwise hide (errors before it are reportable; after it, there is no caller to
   report to). It is a `\Statex`, so it carries no line number and cannot be mistaken for
   an executable step.
6. **No source is quoted anywhere**, so R9 does not apply to this answer; nothing in it
   characterises what any author says or fails to say. The material is standard (Bach ch.
   7, Tanenbaum, the POSIX descriptions), written from scratch in my own phrasing per the
   assignment's "put the answers in your own way".
