# p1 — Ex. 3.1 — worker validator checklist

## Round 1
Verdict: PASS

### Defects
(none blocking, major, or minor-but-actionable)

### Checks performed and what they showed

**Question identity (R7, ground truth).** Source is `input/os_hw_3_problems.md`, a plain
markdown file — manifest records `kind: "text_document"`, `pages` absent, so the three R7
channels genuinely collapse to one text channel here; there is no page PNG and no figure
file to reconcile, and no figure in the assignment. Verified independently:
`diff input/os_hw_3_problems.md ingest/pages/os_hw_3_problems/alltext.txt` → identical.
Read line 1 of the input directly: the brief's transcription is verbatim, including the
curly apostrophe in "CPU's". Brief and ground truth agree.

**Both sub-parts answered.** "how would you load the program and OS" → OS at the high end
of RAM growing down, application loaded verbatim at physical 0 growing up, program owns
[0,F). "Explain your idea by drawing the memory map" → inline TikZ figure present. This is
the expected answer (Tanenbaum MOS Fig. 3-1(b) variant); the worker's RAM-at-top reading
tracks the question's "loaded in the main memory" better than the ROM variant does.
The two things the brief told it not to dodge are both addressed: the low-address vector
table (requires a vector base register, set to F; names the failure case where vectors are
hard-wired at 0) and the boundary (one fence/limit register, declared as a design choice,
with the comparison-vs-addition line drawn explicitly).

**Brief's required labels.** 0, top of program region, bottom of OS, top of OS, physical
top — all five present; top-of-OS and physical-top coincide by construction (OS occupies
the top 8 MiB), so four distinct labels cover five requirements.

**Numbers.** No computed values in the answer; the only arithmetic is the illustrative
addresses, re-derived here: 64 MiB = 0x0400_0000; top byte 0x03FF_FFFF = 0x0400_0000−1 ✓;
F = 0x0400_0000 − 0x0080_0000 = 0x0380_0000 ✓; top of program = F−1 = 0x037F_FFFF ✓.
Internally consistent.

**Architecture claims spot-checked.** 68000 vector table 0x000–0x3FF (256×4 B) ✓;
x86 real-mode IVT 0x00000–0x003FF ✓; ARM low vectors at 0 ✓; VBR introduced on the 68010 ✓;
ARM VBAR ✓; RISC-V `mtvec` ✓; reset vector served from boot ROM ✓. No defect.
R9 has no purchase — nothing is quoted beyond the question itself, which I checked verbatim.

**LaTeX compliance (R5).** No `\documentclass`, `\usepackage`, or `document` environment
(grep, exit 1). Single label `\label{p1:fig:memmap}`, namespaced. No absolute paths. No
external figure file (map is inline TikZ, the brief's preferred option), so no bare-filename
question arises.

**Independent compile.** Built my own wrapper (`validators/p1/check/master.tex`) using only
amsmath/amssymb/graphicx/geometry plus the two lines of the delivered `preamble.txt`, with
dummy fragments before *and* after the input so the fragment is not first in the document:
pdflatex exit 0 both passes, 2 pages, **0 Overfull/Underfull**, no LaTeX warnings, no
undefined references. Hostile variants also exit 0 with no overfull:
  (a) master pre-loads `decorations.pathreplacing` in its preamble — duplicate `\usetikzlibrary` is harmless;
  (b) xelatex instead of pdflatex (in case another problem forces ctex);
  (c) margin=1.25in; (d) no `geometry` at all.
Measured natural width of the tikzpicture = 348 pt, under textwidth in every realistic
master geometry. The body-level `\usetikzlibrary` (worker's own concern #2) is not fragile
in any configuration I could construct; no change needed.

**Figure looked at.** Rendered my compile at 150 dpi and again at 400 dpi, cropped the
figure and upscaled 2x LANCZOS. Vector output (pymupdf reports 18 drawing objects on p.1,
no raster). All labels legible at print size, no overlapping text, no clipped glyphs, both
braces render and span the right regions, address labels read unambiguously as a boundary
pair at the fence. Also verified the worker's self-reported iteration was real: `build/pg-1.png`
does show "vector table" colliding with the thick fence rule, and the delivered version clears it.

**R8 length.** Counted independently: **351 prose words** excluding the figure and caption
(339 excluding the `\paragraph` run-in headings); caption 25 words. Worker claimed 353 —
accurate. For a 10-point design question whose answer is part-carried by a required figure,
this is inside target; it is not over any plausible target by a quarter. One `---` in the
whole file, in the section heading; no em-dashes in prose. No R8 defect.

**Hygiene.** `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT holds exactly `answer.tex`
and `preamble.txt`. `OUTPUT/answer.tex` is md5-identical to both `build/answer.tex` and
`verify/answer.tex`; `preamble.txt` identical to `build/preamble.txt`. `downloads.md` present,
`- (nothing installed)`, consistent with an empty playground (no venv, no fetched files).
Every self-reported claim in `submission.md` that I could check held up.

### Cosmetic notes (reported, not required to fix)
- The map is schematic while the caption gives concrete sizes: the OS band is ~36% of the
  drawing against 12.5% of real memory, and the 1 KiB vector table is ~30% of the OS band.
  Universal practice for memory maps; adding "(not to scale)" to the caption would close it.
- `\section*` is unnumbered. The master's call, one character either way.
- Worker's own concern #1 (the caption) should be **dismissed**, not acted on: the "no caption"
  rule in Diagram standards targets shipped `fig_*.pdf` files the master captions itself. This
  figure is inline TikZ, which the master cannot caption, and deleting `\caption{}` would break
  `Figure~\ref{p1:fig:memmap}` — a `\label` in a `figure` with no `\caption` binds to the
  section counter, not the figure number. Keep it as delivered.

### Resolved since last round
(n/a — first round)

### Still outstanding
None.
