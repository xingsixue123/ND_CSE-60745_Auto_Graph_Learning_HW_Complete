# p1 — Ex. 3.1 (10 pts) — notes

## Ground-truth check (R7)
Source is `input/os_hw_3_problems.md`, a plain markdown text file.
`ingest/manifest.json` records it as `kind: "text_document"` with **no `pages` list**,
so there are no page PNGs and no extracted figure files — the three R7 channels
(text / page render / figure files) collapse into the single text channel for this
input. Verified with:
  diff input/os_hw_3_problems.md ingest/pages/os_hw_3_problems/alltext.txt  -> identical
The brief's verbatim transcription of Ex. 3.1 also matches the source exactly
(checked word by word, incl. the curly apostrophe in "CPU's"). No discrepancy to report.
There is no figure in the assignment to read; the memory map is one I draw.

## What the problem needs
- **plain**: the design decision + justification. This is the bulk of the marks.
- **diagram**: REQUIRED. "Explain your idea by drawing the memory map." TikZ inline.
- **code**: none. There is nothing to compute — no numbers, counts or data. Any
  addresses I show are an illustrative instance I choose, not a computed result.

## The design I will defend
Without an MMU every address the CPU emits goes straight to the bus: virtual == physical.
The program is linked to begin at 0 and to be contiguous, so *physical* 0 must belong to
the application. Only one of the two tenants can own 0, so:
  - application program: loaded verbatim at physical 0, occupying [0, F) contiguously
    (text, data/bss, heap growing up, stack growing down from F).
  - OS: loaded at the **high end** of RAM, occupying [F, M) and growing downward.
  - F = top of the user region = bottom of the OS.
Loader needs no relocation at all; switching programs just overwrites [0, F).

## Two complications I must address (brief flags both)
1. **Trap/interrupt vector table.** On most real CPUs the hardware fetches vectors from
   fixed *low* addresses (x86 real-mode IVT 0x00000-0x003FF; 68000 0x000-0x3FF;
   ARM 0x00000000), which collides with giving 0 to the program. Resolution: use a
   **vector base register** — 68010+ VBR, ARM VBAR/VTOR, MIPS EBase, RISC-V mtvec,
   x86 IDTR — set to the base of the OS region. One register, consulted only when an
   exception is dispatched; it performs no translation on ordinary loads/stores, so it
   is not an MMU. If the CPU hard-wires vectors at 0 with no such register, the
   assumption cannot be honoured: vectors stay at 0 and the loader must relocate the
   program, which is the thing the question is trying to avoid. Say this, don't hide it.
   The reset vector is the one address that genuinely cannot move; it is satisfied from
   boot ROM/firmware before RAM is in play.
2. **Protection at the boundary.** No MMU means no per-access permission check. I allow
   myself a single **fence/limit register** holding F: every user-mode address is
   compared against it and traps if >= F. Compare-only, no address arithmetic, so no
   translation — distinct from a *base* register, which would add to every address and
   is the beginning of an MMU. State that this is a design choice. Without the fence
   nothing stops the application from overwriting the OS.

## Length budget (R8)
10-pt design question whose answer is carried partly by a required figure.
Interpolating the table (5pt -> ~190 words, 10pt essay -> ~550): target ~320 words
of prose, hard ceiling ~400. Count it before submitting.

## Plan
1. Write answer.tex with TikZ memory map inline. preamble.txt = \usepackage{tikz}.
2. Compile a standalone test wrapper in PLAYGROUND, render to PNG, LOOK at it, fix.
3. Word-count the prose. 4. lint_output.py. 5. submission.md.
