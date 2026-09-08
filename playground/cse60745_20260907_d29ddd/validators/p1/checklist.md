# Validator checklist — p1 (Part A: Graph Creation and Modification, 30 pts)

## Round 1
Verdict: PASS

### What I verified, and how

**1. Question scope — read the assignment page myself (R7, all three channels).**
- Text (`page_002.txt`): Part A contains exactly Q1 (15 pts) and Q2 (15 pts), no
  further sub-parts. Wording matches the master's brief verbatim.
- Whole-page PNG (`page_002.png`): confirms the layout — Q1, a figure, Q2. Nothing
  in Part A that the brief omitted.
- Figure file (`page_002_fig_01.jpeg`, 428x588 native): the graph.
- No disagreement between brief and page. Worker's claim of "no disagreement" holds.

**2. Figure transcription — re-derived independently (`vtranscribe.py`, my own code).**
I did not read the worker's or master's edge list before running.
- Blue-disc segmentation → exactly 10 blobs, areas 1067–1180 (uniform; nothing split
  or merged). Centroids reproduce the master's to <1 px.
- Digit labels read from my own 6x LANCZOS strip (`label_strip.png`): blob order
  (sorted by y) → `0, 8, 4, 6, 5, 1, 3, 9, 7, 2`. Independent confirmation of the
  disc→label map.
- All 45 pairs tested for straight-segment ink coverage, skipping samples inside any
  disc. **Clean separation: 15 pairs at 1.000, next best 0.710.** No judgement call.
- Mapped through my labels, my 15 edges are *identical* to the worker's:
  (0,1)(0,4)(0,5)(1,2)(1,6)(2,3)(2,7)(3,4)(3,8)(4,9)(5,7)(5,8)(6,8)(6,9)(7,9).

**3. The 5/4/8 collinearity trap — settled by a method different from the worker's.**
The worker used ring-departure-angle drift. I used a perpendicular-offset line fit:
- Node 4's centre is **13.37 px off** the straight 5–8 line (disc radius ~19), so the
  line passes *through the disc but not the centre*.
- Fitting the ink centreline's perpendicular offset from the 5–8 line separately on
  each side of node 4: 5-side slope −0.0001, intercept −1.64 (n=225); 8-side slope
  +0.0011, intercept −1.99 (n=67). Both sides lie on **one straight line** with a
  constant ~1.7 px antialiasing bias and no bend.
- A genuine polyline 5–4–8 would require the offset to reach −13.37 px at node 4.
  It does not. **(5,8) is one edge; (4,5) and (4,8) do not exist.** Confirmed.
- My coverage test independently agrees: (4,5)=0.532, (4,8)=0.475, both far below the
  1.000 band. Also (0,9)=0.710 and (0,6)=0.385 → no (0,6), no (0,9). Traps confirmed.

**4. Worker's own transcription evidence is real, not fabricated.**
Re-ran `work/transcribe.py` (copied into my dir). Every cited number reproduces:
- 14 pairs at 1.000, (5,8) at 0.985, rest <0.55 — matches submission.md exactly.
- Node 4 rings: 57.5/83.5/211.8 constant; 124.0→139.5 and 357.5→342.0 drifting toward
  bearings 145.8 (node 5) and 339.7 (node 8) — matches exactly.
- Node 5: 324.0→328.0 → 5→8=330.5 (not 5→4=325.8). Node 8: 156.2→153.5 → 8→5=150.5
  (not 8→4=159.7). Both match exactly.
- Checked the "exactly three departures" claim at the correct radius r=24: 9 nodes
  show 3 crossings, node 4 shows 5 (3 real + 2 from the pass-through line).
  Total 32 = 2·15 + 2. Consistent.

**5. Global invariants — recomputed by me.**
10 nodes, 15 edges, degree sequence all 3, degree sum 30 = 2|E| (handshake), connected,
0 triangles, girth 5, `nx.is_isomorphic(G, nx.petersen_graph())` → **True**. All match.

**6. Q2 — recomputed independently.**
Remove node 1 (kills (0,1),(1,2),(1,6)), then (0,4), then (0,5) — 5 edges total.
Result: 9 nodes, 10 edges, **2 components**: `{0}` (size 1) and
`{2,3,4,5,6,7,8,9}` (size 8). Remaining edges match. Identical to answer.tex.

**7. Reproducibility.** Re-ran `work/solve.py` with OUT redirected into my own dir:
stdout is **byte-identical** to `work/solve_out.txt` (diff empty). Regenerated figure
PDFs have identical path counts (26 / 20) and identical text content. Every number in
`answer.tex` traces to that stdout. Nothing fabricated.

**8. Figures — opened and looked at them.**
Rendered both PDFs at 150 dpi and inspected.
- Pure vector: `get_images()` = **0 raster images** in both. Text layer present
  (10 labels Q1, 9 labels Q2).
- Page size 341.6 x 413.6 pt, typeset at `0.62\textwidth` ≈ 3.9 in — inside the 3–6 in
  target. Node labels legible, white bold on blue, no overlap, no clipping.
- Layout shared between Q1 and Q2 (same `CENTRES` dict), so the modification is
  directly comparable. Node 0 orange and visibly isolated in Q2. Correct.
- Drawn edges match the verified edge lists.

**9. LaTeX compliance.**
- No `\documentclass` / `\usepackage` / `document` environment in `answer.tex` (R5). ✓
- Both labels namespaced: `p1:fig:q1`, `p1:fig:q2`. No unnamespaced labels. ✓
- Figures referenced by **bare filename**, no absolute paths. ✓
- Compiles clean in a minimal wrapper: two passes, exit 0, no errors, no undefined
  references. Also compiles with **only the two packages declared in preamble.txt**
  (graphicx, booktabs) — no undeclared dependency. ✓
- Rendered output inspected page by page: tables, display math, `\ttfamily` snippet
  and both figures all typeset correctly.

**10. OUTPUT hygiene and downloads.**
- `lint_output.py` → `OUTPUT LINT OK`, exit 0. Only `answer.tex`, `preamble.txt`,
  `fig_p1_q1_graph.pdf`, `fig_p1_q2_graph.pdf`. ✓
- `downloads.md` says "(nothing installed)". Verified: no venv, no pip artifacts in
  the worker playground; only `.mplcfg`, `figs/`, `work/tex/` scratch dirs, which it
  correctly lists as caches rather than installs. Accurate (R3). ✓

**11. Deliverable completeness against the brief.**
Q1 and Q2 as separate subsections ✓; node set and explicit edge list, readably
formatted as an adjacency table, not a code dump ✓; construction stated ✓; Q1
visualization ✓; Q2 removals stated ✓; components listed explicitly as node sets ✓;
Q2 visualization ✓; before/after node/edge counts in a table ✓. No script dump.

### Defects
None blocking or major.

- [1.1] `submission.md:70` claims the test compile had "no overfull/underfull boxes".
  My compile shows one **overfull \hbox, 1.1974 pt** at `answer.tex:92` (the `E(H)`
  display). 1.2 pt ≈ 0.4 mm — invisible in the rendered page, which I checked.
  | `answer.tex:92` | severity: minor — noted, not requiring a fix.
- [1.2] The `\ttfamily`-in-`center` construction snippet is a blunt way to set code
  and could be restyled by the master's preamble. Worker already disclosed this.
  | `answer.tex:38-43` | severity: minor — cosmetic only; renders correctly as-is.

Neither is worth another round.

### Notes forwarded to the master (not defects in p1)
The worker flagged that a stock `\begin{itemize}` fails to compile on this machine:
its `\textbullet` needs TS1 font `tcrm1000`, METAFONT must generate it, and the PK
cache write fails against read-only `~/.TinyTeX`. I independently hit the same thing —
my own compile only succeeded after setting a writable `TEXMFVAR`. p1's fragment
sidesteps it by using `enumerate`, so p1 is safe, but **other problems' fragments will
hit this** and the master should set `TEXMFVAR` to a writable directory before the
final assembly.

### Judgement call reviewed, not a defect
Edge (5,8) is drawn bowed (`arc3,rad=0.30`) rather than straight through node 4's
disc. This deviates from the assignment's drawing but reproduces the same *graph*,
which is what Q1 asks for, and it removes the exact ambiguity that makes the original
figure hard to read — necessary in Q2, where node 4 survives and a straight (5,8)
would read as 5–4–8. It is disclosed in the Q1 body text and in the figure caption.
Correct call; withdrawn as a concern.

### Resolved since last round
(n/a — first round)

### Still outstanding
Nothing substantive.
