# p3 — Ex. 2.4 notes

## Ground-truth check (R7)
Assignment is a markdown file, not a PDF. Only two channels exist:
  - `input/hw2_instruction.md` (source)
  - `ingest/pages/hw2_instruction/alltext.txt`
`diff` of the two: IDENTICAL. No page PNGs, no figure files, no figure referenced
by this question. Nothing to transcribe.

Line 22 of the source reads, verbatim:
  `Ex. 2.4 | (5pts) The amount of time that takes to make a context-switch between
   threads versus that of between processes is much shorter. Explain why.`
The brief's transcription matches character-for-character. No discrepancy to report.

Preamble (line 1) applies: may read sources, must write in own words. I am not
quoting or citing any source, so R9 does not bite.

## What it needs
**plain.** No number to compute, no figure to draw, nothing to run. A causal
explanation. Deliverable is prose only; no code, no fig_p3_*.pdf.

## Plan — the causal chain
1. Scope the claim: two threads *of the same process*. Threads of different
   processes cost a full process switch. Name that boundary explicitly.
2. Shared address space => memory map unchanged => no page-table base reload
   (CR3 / TTBR) => no TLB invalidation.
3. The indirect cost is the larger half: cold TLB + cache polluted by a new
   working set, paid as stalls *after* the switch returns.
4. One clause only on tagged TLBs (ASID/PCID): softens, does not remove (caches
   still polluted). Not a treatise.
5. What a thread switch still pays: register file incl. PC and SP, kernel
   stack / TCB pointer.
6. Per-process kernel state (open-file table, signal dispositions) not swapped.
7. User-level thread switch skips the kernel trap.

## Length discipline (R8)
Target ~190 words. Count with `wc` on the prose before submitting; hard ceiling
237 (target + 25%). Watch for: closing sentence restating the opening,
"it is worth noting", enumerating more hardware than the argument needs.
