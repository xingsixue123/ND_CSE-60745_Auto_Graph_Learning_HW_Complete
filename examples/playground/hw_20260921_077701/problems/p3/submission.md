# p3 — submission (round 2)

## Round 2 — validator defect 1.1, fixed

**[1.1] major — wrong sectioning level. Fixed. Accepted without dispute.**
`answer.tex:1` was `\subsection*{...}`; R5 says the fragment starts at the section
level. I confirmed the validator's reading independently rather than taking it on
trust: `head -1` on the siblings gives `\section*{...}` for both
`output/hw_20260921_077701/p1/answer.tex` and `p2/answer.tex`. Mine was the only
`\subsection*` of the three, so assembled in order Ex. 2.4 would have been typeset
one level down and read as a sub-part of Ex. 2.2. Changed line 1 to `\section*`.
That is a one-token edit; no prose was touched.

Re-verified after the fix:
- recompiled through a wrapper that `\input`s the fragment: 1 page, 0 errors;
- re-rendered to `build/fixed-1.png` and read it back — the heading now sets at
  section weight and wraps over two lines, body unchanged and clean;
- body word count still **212** (prose untouched, as the validator required);
- assertion added to the check that the file starts with `\section*{` and that the
  string `subsection` no longer appears anywhere in it — both pass;
- `lint_output.py` exits 0, `answer.tex` still the only file in OUTPUT.

The validator explicitly did **not** want the answer shortened, so I left the length
alone. Everything below is from round 1 and still holds, except that references to
`\subsection*` are now `\section*`.

---

# Round 1 (original submission)

## What the problem asked

> Ex. 2.4 | (5pts) The amount of time that takes to make a context-switch between
> threads versus that of between processes is much shorter. Explain why.

**No disagreement between the brief and the assignment page.** This assignment is a
plain markdown file, so the usual three channels collapse to two, and I checked both:
`input/hw2_instruction.md` (line 22) and
`ingest/pages/hw2_instruction/alltext.txt`. A `diff` of the two files reports them
byte-for-byte IDENTICAL, and the brief's transcription matches line 22
character-for-character. There are no page PNGs and no figure files for this
assignment, and Ex. 2.4 refers to no figure, so nothing had to be transcribed from an
image. The brief's warning about scope (same-process threads vs. threads of different
processes) is my own reading of the question too, and I made it explicit in the answer.

## What I decided it needed

**plain.** Nothing to compute and nothing to draw. The question says "Explain why",
so the deliverable is a causal argument. No `fig_p3_*.pdf`, no code, no `preamble.txt`
(the answer uses only `\section*`, `\emph` and `\texttt`, all built-in).

## What I did

Wrote the explanation as a single causal chain rather than a threads-vs-processes
comparison table. The chain: (1) the claim only holds for two threads of the *same*
process, and the reason is that cost tracks the change of address space, not the
change of scheduling entity — which is why threads of *different* processes cost a
full process switch; (2) a shared address space means the memory map is untouched, so
no page-table base reload (`CR3` / `TTBR`) and no TLB invalidation; (3) the larger,
indirect half of a process switch's bill is paid after it returns, as stalls on a cold
TLB and caches polluted by the outgoing working set; (4) one clause noting tagged TLBs
(ASIDs/PCIDs) soften but do not remove this, since caches are still displaced; (5)
what a thread switch still pays — register file incl. PC and SP, kernel stack / TCB;
(6) per-process kernel state (open-file table, signal dispositions) is shared and not
swapped; (7) a user-level thread switch skips the kernel trap entirely.

I cite no external source and quote nothing, so R9 has no surface here; the argument
is standard OS material written from scratch in my own words, per the assignment
preamble.

## Intermediate steps and code

No code produced any result in the answer — there is no computed value in it. The
only scripts/commands I ran were checks:

- `notes.md` — my ground-truth reconciliation and plan, written before drafting.
- Channel cross-check (reproduces the IDENTICAL claim above):
  `cd /home/xing/project/auto_hw_complete && diff input/hw2_instruction.md playground/hw_20260921_077701/ingest/pages/hw2_instruction/alltext.txt`
- `build/test.tex` — a throwaway wrapper that `\input`s `OUTPUT/answer.tex` to prove
  the fragment compiles standalone with no extra packages. Reproduce with
  `cd build && pdflatex -interaction=nonstopmode -halt-on-error test.tex`.
  Result: "Output written on test.pdf (1 page)", no errors, no missing packages.
- `build/render-1.png` — `pdftoppm -png -r 110` of that PDF. I read it back and the
  page is clean: no overfull lines, no broken markup, heading and three paragraphs.
- Word count (inline `python3`, strips macros and braces, counts alphanumeric tokens
  in the body, excluding the `\subsection*` heading).

## Results

There are no computed values in `answer.tex` — it is entirely prose, and it quotes no
measured figure from any source. The only numbers I checked are about the answer
itself:

| claim | value | how |
|---|---|---|
| body word count | **212 words** | inline `python3` counter described above |
| R8 target / ceiling | 190 / 237 | from the brief; 212 is 11.5% over target, under the ceiling |
| fragment compiles | 1 page, 0 errors | `pdflatex` on `build/test.tex` |
| R5 fragment check | no `\documentclass`, `\usepackage`, `\begin{document}`, `\end{document}` | asserted in the same inline `python3` |
| `lint_output.py` | `OUTPUT LINT OK`, exit 0 | `python3 framework/tools/lint_output.py output/hw_20260921_077701/p3` |

## Deliverables

- `/home/xing/project/auto_hw_complete/output/hw_20260921_077701/p3/answer.tex` — the whole answer.
- No figures, no `preamble.txt`, no `assets/`. OUTPUT contains exactly one file.
- `PLAYGROUND/downloads.md` records that nothing was installed or downloaded.

## Where I am least confident

- **Length.** 212 words against a 190-word target. I trimmed once from 222 and
  believe every remaining sentence carries a distinct link in the chain, but if the
  validator wants it at target, the two most cuttable pieces are the tagged-TLB
  sentence (it is an aside the brief explicitly caps at "one clause", and mine runs a
  little long) and the final user-level-threads sentence. Cutting either costs a
  little completeness and no correctness.
- **Depth on the hardware.** I name `CR3` and `TTBR` and ASIDs/PCIDs and stop there,
  deliberately, because the brief warns against a treatise on tagged TLBs. If the
  grader's rubric wanted the kernel-side bookkeeping spelled out further (scheduler
  data structures, FPU/SIMD state, which is lazily switched on most systems), that is
  absent by choice rather than oversight. FPU state in particular is a real per-thread
  cost I chose not to mention.
- **The "larger half" claim.** I assert the indirect cost (TLB/cache refill) dominates
  the direct register-saving cost of a process switch. This is well supported in the
  literature but I deliberately quoted no measurement and cited no paper, so it stands
  as a qualitative claim. It is phrased as "the larger half is indirect", not as a
  number, which I think is the right level of commitment for a 5-point question — but
  it is the one claim in the answer that an adversarial reader could ask me to source.
- **Scope framing.** I open by narrowing the claim to same-process threads. That is
  what the brief asks for and I am confident it is correct, but it does mean the
  answer spends its first ~40 words on scoping before reaching the mechanism. A
  grader skimming for "TLB" finds it in sentence four rather than sentence one.
