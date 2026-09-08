# p2 validator checklist — Q3 Graph Creation + Q4 Graph Essentials

## Round 1
Verdict: PASS

### What I checked and how

**Assignment page, all three channels (R7).**
Read `ingest/pages/CSE 60745_Fall 2026_HW1/page_003.txt` and `page_003.png` myself.
The text matches the brief's verbatim quote word for word. The PNG confirms a
text-only page (Part B header, Q3, Q4, Q5 — no graphics). `ls` of the ingest dir
confirms no `page_003_fig_*` file exists (only `page_002_fig_01.jpeg`). The worker's
claim of "no disagreement between brief and page" is correct; there was nothing to
transcribe from an image.
Also confirmed `input/` holds exactly one data file, `graph-1.txt`, tab-separated
(`cat -A` shows `^I`), matching the brief's note that the assignment's `graph.txt`
is attached under a different name.

**Numbers — independently re-derived, not just re-run.**
Wrote `verify.py` (this dir), which never imports networkx: it parses the file into
dict-of-sets adjacency and does iterative BFS for components. Every quantity claimed
in `answer.tex` reproduced exactly:

| Claim | answer.tex | my independent BFS |
|---|---|---|
| nodes / edges / components | 26728 / 26377 / 4104 | 26728 / 26377 / 4104 |
| self-loops / duplicate edges | 0 / 0 | 0 / 0 |
| LCC nodes / edges (induced) | 13903 / 16695 | 13903 / 16695 |
| LCC share nodes / edges | 52.0% / 63.3% | 52.02% / 63.29% |
| top-10 component sizes | 13903,69,30,30,29,26,23,21,21,20 | identical |
| tie at 2nd place / 3rd place | 1 (unique) / 2 | 1 / 2 |
| CC2 nodes / edges | 69 / 80 | 69 / 80 |
| CC2 diameter / max deg / cycles | 17 / 7 / 12 | 17 / 7 / 12 |
| CC2 degree hist | {1:19,2:29,3:7,4:11,5:1,6:1,7:1} | identical |
| deg min/max/mean/median | 1 / 59 / 1.974 / 1 | 1 / 59 / 1.973735 / 1 |
| N(1), N(2), frac deg<=2 | 13942 (52.2%), 7423 (27.8%), 79.93% | 13942 (52.16%), 7423 (27.77%), 79.93% |
| distinct degrees / argmax node | 37 / node 22777 | 37 / [22777] (unique) |
| whole-graph cycles m-n+c, forest edges n-c | 3753 / 22624 | 3753 / 22624 |

Global invariants I checked myself: degree sum 52754 = 2m; component sizes sum to n;
induced component edge counts sum to m. All hold.
No number appears in `answer.tex` that is absent from computed output — nothing
fabricated.

**Worker's own scripts re-run.** Copied `analyze.py`/`crosscheck.py` here and ran
them. `analyze.py` exit 0 and its `results.json` is byte-identical (key-sorted diff)
to the worker's. `crosscheck.py` exit 0, prints "ALL THREE CHANNELS AGREE" across
nx 3.6.1, nx 3.3 and a no-networkx union-find. The cross-check is genuine, not a
tautology: the third channel really does avoid networkx.

**Did it do the required kind of work?** Q3 and Q4(a) are computed, not hand-waved.
Q4(b) "Show visualization" -> `fig_p2_cc2.pdf` exists. Q4(c) "Plot" -> 
`fig_p2_degree_dist.pdf` exists. All four sub-deliverables present.

**Figures are real, and are what they claim to be.** Regenerated both PDFs from
`figs.py` (patched output dir) into `regen/`; rendered both regenerated and delivered
PDFs to PNG and compared with PIL — **pixel-identical**, so the delivered figures are
the output of the reviewed code and not a stale or hand-edited artifact.
Counted the node markers in `fig_p2_cc2.pdf` at 400 dpi by colour-masking saturated
pixels and labelling blobs: **69 markers**, matching the claimed CC2 size. (My first
mask gave 68 because `mx<250` excluded the bright yellow degree-7 hub; correcting the
mask gives 69. The miscount was mine, not the worker's.)

**Figure readability.** Rendered both at 150 dpi and viewed; then compiled the
fragment and viewed the figures *at printed size* (300 dpi crop of the compiled page).
Both are legible: axes labelled with meaning ("Degree $k$", "Number of nodes $N(k)$",
"Fraction of nodes $P(k)$"), colour bar labelled "Node degree", no overlapping or
clipped text, no rasterization (vector PDF, `pdf.fonttype 42`), no chartjunk, no title
duplicating the caption. The CC2 drawing's prose claims check out visually: a degree-7
and a degree-6 hub adjacent near the centre, and a degree-2 chain to the upper right.
The no-labels decision is justified and stated in the answer.

**LaTeX compliance (R5).** `grep` finds no `\documentclass`, `\usepackage`,
`\begin{document}` or `\end{document}` in `answer.tex`. All five labels namespaced:
`p2:tab:q3`, `p2:tab:q4`, `p2:fig:cc2`, `p2:tab:deg`, `p2:fig:deg`. Both
`\includegraphics` use bare filenames (`fig_p2_cc2.pdf`, `fig_p2_degree_dist.pdf`),
no absolute paths. `preamble.txt` is three clean `\usepackage` lines
(graphicx, booktabs, amsmath) — all three are actually used.
Compiled it myself in a minimal wrapper: pdflatex exit 0, **zero `!` errors**, no
undefined references after the second pass, no overfull/underfull box warnings,
3 pages.

**OUTPUT clean (R4).** `python3 framework/tools/lint_output.py <OUTPUT>` ->
"OUTPUT LINT OK", exit 0. Directory holds only `answer.tex`, `preamble.txt` and the
two `fig_p2_*.pdf`. Scratch (`compiletest/`, `.mplconfig/`, `chk_*.png`,
`cc2_labelled_variant.pdf`, `results.*`) correctly stayed in the playground.

**Downloads recorded (R3).** `downloads.md` says "(nothing installed)" and explains
why (both interpreters pre-existing). I confirmed no venv or downloaded artifact
exists in the playground. Accurate.

### Defects
None blocking or major. Cosmetic only, recorded for the record — not grounds to
withhold a pass:

- [1.1] `fig_p2_degree_dist.pdf`, right panel | the log–log x-axis carries labelled
  major ticks only at $10^0$ and $10^1$, so the tail out to $k=59$ has no labelled
  tick to read against. Adding a minor-tick formatter or a marked $k=59$ point would
  help a grader. | severity: minor
- [1.2] `answer.tex:135` | "the largest degrees ($36$, $38$, $40$, $51$, $57$, $59$)
  are each realised by a single node" is true, but degrees $30$ and $32$ are also
  realised exactly once, so the sentence could be misread as listing *all* the
  singleton degrees. | severity: minor

### Resolved since last round
(nothing — first round)

### Still outstanding
[1.1], [1.2] — both cosmetic; the answer is correct and complete without them.
