# Validator checklist — p1 (Ex. 1.1–1.4)

## Round 1
Verdict: PASS

### What I checked, and how

**Question fidelity (independent read of the source).**
Read `/home/xing/project/auto_hw_complete/input/hw_questions.md` myself. Lines 5, 9, 13, 17
are Ex. 1.1–1.4 and match the brief's transcription word for word. The brief's claim that p1
covers exactly 1.1–1.4 is correct; 1.5–1.0 belong to other workers. No brief-vs-source
disagreement to report.

**R7 / three channels.** Verified independently from
`ingest/manifest.json`: the only rendered document is `PaperList.xlsx` (6 pages), and every
page reports `n_images: 0` and `"figures": []`. `hw_questions.md` is `kind: text_document`
and is not rendered because it is already text. There is no image channel anywhere in this
assignment, so R7 is genuinely vacuous here — the worker's claim is accurate and it was
honest to state it as vacuous rather than fake a figure read.

**Deliverable type.** Correctly judged **plain only**. Nothing in 1.1–1.4 asks for a number,
count, ranking, plot or drawing, so the absence of code and figures is correct, not a gap.
No computed values appear in `answer.tex`, so there is nothing that could be fabricated.

**Sub-part coverage** (this is where 5-pt questions are lost). All present:
- 1.1 — role (format dispatch on the `execve` path, `ENOEXEC` on no match) **and** location
  (offset 0, opening field of the header). Both parts visible under bold run-in headings.
- 1.2 — six regions listed *and* explained: text, `.data`, BSS, heap, mmap region, stack,
  with growth directions stated (heap up, stack down).
- 1.3 — both halves. What the machine is (stored-program, single memory for code+data,
  fetch–decode–execute, von Neumann bottleneck) **and** the "how are they related" half,
  which gets its own full paragraph.
- 1.4 — all four parts: meaning, seven possible reasons, etymology of "segmentation",
  etymology of "core".

**Technical accuracy — spot-audited every factual claim.** ELF `0x7F 'E' 'L' 'F'`, `#!` =
`0x23 0x21`, PE `MZ`, Java `0xCAFEBABE`, `ENOEXEC`, BSS size-only-on-disk, `brk`/`sbrk` vs
`mmap`, `SIGSEGV` default disposition, split-L1 as modified-Harvard, magnetic-core etymology
— all correct. Found no factual error.

**Quote corruption.** The `\segmentation"` backslashes are correctly diagnosed as
LaTeX-to-markdown mangling and are **not** reproduced; `answer.tex` uses proper `` ``…'' ``
quotes. Confirmed in the source and in the render.

**Build — compiled it myself, twice, in two different wrappers.**
- Minimal wrapper (`geometry`, `amsmath`, `amssymb`, `enumitem`): exit 0 on both passes,
  2 pages, `grep -i 'warning|undefined|overfull|underfull|not found'` on the log returns
  **nothing**.
- Stress wrapper adding `[T1]fontenc`, `lmodern`, `graphicx`, `booktabs`, `hyperref` (a
  realistic merged master): exit 0 both passes, 2 pages, no warnings, no duplicate-label or
  undefined-reference complaints. The fragment survives a hostile preamble.

**R5 compliance.** No `\documentclass`, `\usepackage`, `\begin{document}` or
`\end{document}` in `answer.tex` (grepped). All five labels namespaced: `p1:sec:main`,
`p1:sec:magic`, `p1:sec:segments`, `p1:sec:vonneumann`, `p1:sec:segfault`. No figures, so no
filename-namespacing or absolute-path risk. `preamble.txt` is a single
`\usepackage{enumitem}`, which is genuinely required (the lists use `nosep`, `leftmargin`
and `label=`).

**Figure readability.** N/A — no figures. I did render both pages of my own compile at
110 dpi and read them: headings legible, bullets render, no overfull lines, no clipping.

**R4 OUTPUT clean.** `lint_output.py output/hw_20260909_1235d6/p1` → `OUTPUT LINT OK`,
exit 0. Directory contains only `answer.tex` and `preamble.txt`. All scratch (`build/`,
logs, `.aux`, PNGs, bisect cases `t2`–`tb`) correctly stayed in PLAYGROUND.

**R3 downloads.md.** Present, records `- (nothing installed)`. Accurate — the run used only
`pdflatex`, `pdftoppm`, `pdfinfo`, `python3`, all preinstalled per `env.md`. Nothing was
fetched.

**Worker's environment finding — independently reproduced.** I ran the worker's three-line
minimal case myself and got the identical failure:
`!pdfTeX error: pdflatex (file tcrm1095): Font tcrm1095 at 600 not found`, preceded by
`cp: cannot create ... /home/xing/.TinyTeX/texmf-var/fonts/pk/... : Read-only file system`.
Plain `\begin{itemize}\item one\end{itemize}` really does fail on this box: the TS1 bullet
has no Type1 font, pdfTeX falls back to METAFONT, and `texmf-var` is read-only. The
`label=$\bullet$` workaround (bullet from `cmsy`) is correct, minimal, and confined to the
fragment. Declining to push `lmodern`/`fontenc` into `preamble.txt` was the right call — it
would restyle every other problem's fragment. **This finding should be passed upstream to
the master; any other worker using a bare `itemize` will fail the final compile.**

### Defects
None blocking, major, or actionable. Every claim in `submission.md` that I could test
independently held up; nothing was overstated.

### Minor observations (noted, not requiring a fix)
- [1.m1] `\label` immediately after a starred `\section*`/`\subsection*` is inert — starred
  headings set no counter, so a `\ref` to these would resolve to a stale number. Nothing
  references them and they are correctly namespaced, so there is no collision risk.
  Cosmetic only. | `answer.tex:2,5,25,58,80` | severity: minor
- [1.m2] Ex. 1.4 says the default `SIGSEGV` action is to "kill the process and write out a
  core dump". Strictly, the `(core dumped)` half is conditional on `ulimit -c` and
  `core_pattern`; a core is often suppressed in practice. The answer never claims otherwise
  and no grader would deduct. | `answer.tex:87–88` | severity: minor
- [1.m3] Ex. 1.2 omits the argv/environ block above the stack and does not break out
  `.rodata`. The worker flagged this itself as a deliberate boundary call and chose
  over-inclusion of the mmap region instead, which is the better trade for "list all".
  | `answer.tex:30–51` | severity: minor
- [1.m4] Ex. 1.4 runs longer than the spec's "few sentences", but it carries four distinct
  sub-questions, so the length is proportionate to the parts being graded. Total output is
  2 pages for 20 pts. | severity: minor

### Resolved since last round
N/A — first round.

### Still outstanding
Nothing substantive. The four minor observations above are cosmetic and do not warrant
another round.
