# p4 notes — Ex. 2.5 + Ex. 2.6

## Ground truth check (R7)

The assignment is `input/hw2_instruction.md`, a plain markdown file. Ingest produced
only `ingest/pages/hw2_instruction/alltext.txt` — no page PNGs, no figure files (checked
with `ls`; the directory has exactly one file). `diff input/hw2_instruction.md
ingest/pages/hw2_instruction/alltext.txt` reports the files IDENTICAL, so the text
channel is the whole document and there is nothing else to reconcile it against. The
document contains no figure.

Line 26 of the markdown (Ex. 2.5) and line 30 (Ex. 2.6) match the brief's transcription
word for word, including the hint. No discrepancy between brief and source.

## What it needs

**plain only.** Nothing to compute (no data, no numbers) and no figure to reproduce.
The brief flags a lifecycle state diagram as *optional*; I am not making one — the
question asks for pseudo-code plus an explanation, the brief itself says the right way
to close the explanation is a sketch in words, and a decorative figure would spend
length budget (R8) without earning a mark.

Only verification work: the LaTeX fragment must compile. I will build it against a
throwaway wrapper in `build/`.

## Plan

1. Four `algorithm`/`algpseudocode` floats, kernel-side, labelled `p4:alg:fork`,
   `p4:alg:exec`, `p4:alg:waitpid`, `p4:alg:exit`. The hint is the trap: these are the
   implementations of the calls, operating on the process table / PCB, not user code
   that calls them.
   - fork: the two saved-return-value lines are the "returns twice" phenomenon and must
     be visible in the code.
   - exec: copy argv/envp into the kernel *before* tearing down the old address space
     (they live in it); magic number picks the loader; does not return on success.
   - waitpid: the reaping step (free PCB + pid) is the point; ECHILD vs WNOHANG vs block.
   - exit: re-parent children to init, mark ZOMBIE, PCB survives — this is what 2.6 is about.
2. Inter-relation explanation, 300–350 words: fork/exec as the one mechanism for
   "run a new program" and why the split buys the redirection window; exit/waitpid as
   the matching pair because the status must outlive the child; shell lifecycle sketch.
3. Ex. 2.6, 190–220 words: definition, why the kernel keeps the PCB, cost, that SIGKILL
   does nothing, how it clears (wait / SIGCHLD / parent dies and init adopts), `Z` and
   `defunct` in `ps`, zombie vs orphan, and the leak failure mode in one sentence.
4. `preamble.txt`: `\usepackage{algorithm}` + `\usepackage{algpseudocode}` (both
   installed per env.md). Nothing else needed.
5. Compile test, word count against R8 targets, `lint_output.py`.

## Sources

Standard OS material (Bach, *The Design of the Unix Operating System*, ch. 7;
Tanenbaum; the POSIX descriptions of fork/execve/waitpid/_exit). No quotation is used,
so R9 does not bite, but no sentence characterises what a source says either.
