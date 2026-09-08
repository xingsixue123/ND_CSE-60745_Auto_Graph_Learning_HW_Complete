# p1 — submission

## What the problem asked

Part A of CSE 60745 HW1 (rendered page 2), worth 30 pts, in two questions:

- **Q1 (15 pts)** — "Create the following undirected graph and show visualization of
  this graph." The graph itself exists *only* as an embedded figure.
- **Q2 (15 pts)** — "Based on graph created in Q1, remove node 1, edge (0, 4) and
  edge (0, 5). List remaining components and visualize remaining graph."

**Brief vs. assignment page:** no disagreement. `page_002.txt` carries the Q1/Q2
wording verbatim as the master transcribed it, and my independent transcription of
the figure reproduced the master's 15-edge list exactly, including both of the traps
it warned about. I did not take the master's edge list on trust — see below.

## What I decided it needed

All three:

- **code** — Q2 asks for the connected components of a modified graph. That is a
  computed result, so it is computed in networkx, not asserted.
- **diagram** — both questions explicitly say "visualization"/"visualize". Two vector
  PDF figures are required; an answer without them is incomplete.
- **plain** — the write-up: node set, edge list, what was removed, the component list,
  and before/after counts.

The real risk in this problem is the **figure transcription**, since every downstream
number depends on the edge list. I treated that as the main task.

## What I did

1. Read the page through all three channels. Text confirms the question wording and,
   as expected, contains no trace of the graph. The whole-page PNG shows a figure is
   present but is downscaled. `page_002_fig_01.jpeg` (428x588, native) is the channel
   I transcribed from.
2. **Transcribed the figure programmatically, not by eye.** Segmented the blue node
   discs by colour and flood-filled them (exactly 10 blobs, very uniform in area, so
   nothing was split or merged). Read the digit inside each disc from a 4x-upscaled
   crop. Then tested **all 45 vertex pairs** for ink coverage along the straight
   centre-to-centre segment, skipping samples inside any disc.
3. **Disambiguated the collinear cases by measurement.** Pairwise ink coverage alone
   cannot tell "5–4 plus 4–8" from a single "5–8" drawn through node 4's disc. So at
   each node I measured the angular positions of ink crossings on rings of radius
   r = 24, 32, 42, 55 px: a true incident edge holds a **constant** angle in r, while
   a line merely passing near the centre **drifts** toward the far node's bearing.
4. **Checked global invariants**, then computed Q2 in networkx and drew both figures
   with a shared, fixed layout.

## Intermediate steps and code

Paths relative to PLAYGROUND.

- `work/transcribe.py` — the figure transcription. Detects node discs, reads nothing
  from the master's brief, computes the 45 pairwise ink-coverage scores and the
  per-node departure angles at four ring radii. Reproduce with:
  `python3 work/transcribe.py`
- `work/labels_strip.png` — the ten node discs cropped and upscaled 4x LANCZOS into
  one strip, so the digit in each disc can be read directly. Generated inline; this
  is what fixes the disc→label mapping.
- `work/solve.py` — builds the graph, prints all Q1/Q2 facts, and writes both figure
  PDFs. Reproduce with:
  `MPLCONFIGDIR=$PWD/.mplcfg /home/xing/miniconda3/envs/py311/bin/python work/solve.py`
  (must be the py311 interpreter: base `python3` has networkx but no matplotlib.)
- `work/solve_out.txt` — the captured stdout of that run; every number below is in it.
- `work/zoom_fig_p1_q1_graph.png`, `work/zoom_fig_p1_q2_graph.png` — 2.2x zooms on
  node 4, used to confirm the bowed (5,8) edge really clears the disc.
- `work/tex/` — a throwaway `\documentclass{article}` wrapper that `\input`s
  `answer.tex`, used to verify the fragment compiles. Two passes, exit 0, no
  undefined references and no overfull/underfull boxes.
- `notes.md` — the full reasoning, including the per-node angle measurements.

## Results

Every value below comes from `work/solve_out.txt` unless stated otherwise.

**Q1.**
- Nodes: **10** (`0..9`). Edges: **15**.
- Edge list: `(0,1) (0,4) (0,5) (1,2) (1,6) (2,3) (2,7) (3,4) (3,8) (4,9) (5,7)
  (5,8) (6,8) (6,9) (7,9)`.
- Degree sequence: all **3**. Degree sum **30** = 2|E| = 2·15 (handshake lemma).
- Connected: **True**, 1 component. Triangles: **0**. Girth: **5**.
- `nx.is_isomorphic(G, nx.petersen_graph())` → **True**. The graph is the
  **Petersen graph**.

**Transcription evidence** (from `work/transcribe.py` output):
- 14 pairs scored ink coverage **1.000**, one pair — (5,8) — scored **0.985**, and
  every other pair scored **below 0.55**. Clean separation, no judgement call.
- Node 4's ring crossings: 57.5 / 83.5 / 211.8 hold constant (→ nodes 3, 9, 0), while
  two others drift hard, 124.0→139.5 and 357.5→342.0, converging on the bearings of
  node 5 (145.8) and node 8 (339.7). Those two are the ends of the single edge (5,8)
  crossing node 4's disc. So **no (4,5) and no (4,8)**. Symmetrically node 5 drifts
  324.0→328.0 toward 5→8 = 330.5 (not 5→4 = 325.8) and node 8 drifts 156.2→153.5
  toward 8→5 = 150.5 (not 8→4 = 159.7).
- Node 6 has no crossing near bearing 207.6 (node 0) and node 9 none near 243.0
  (node 0) or 245.3 (node 1), so **no (0,6) and no (0,9)**.
- All 10 nodes show exactly three constant-angle departures.

**Q2.** After removing node 1 (which also removes (0,1), (1,2), (1,6)), then (0,4),
then (0,5) — five edges in total:
- Nodes: **9** (`0,2,3,4,5,6,7,8,9`). Edges: **10**.
- Remaining edges: `(2,3) (2,7) (3,4) (3,8) (4,9) (5,7) (5,8) (6,8) (6,9) (7,9)`.
- Connected components: **2** — `{0}` (size 1, isolated) and
  `{2,3,4,5,6,7,8,9}` (size 8, containing all ten remaining edges).

## Deliverables

In OUTPUT:
- `answer.tex` — the fragment. No `\documentclass` / `\usepackage` /
  `document` environment; starts at `\section*`. Both labels namespaced
  (`p1:fig:q1`, `p1:fig:q2`); figures referenced by bare filename.
- `fig_p1_q1_graph.pdf` — Q1 visualization. Pure vector (0 raster images, 10 text
  labels), 341.6 x 413.6 pt, typeset at 0.62\textwidth ≈ 3.9 in.
- `fig_p1_q2_graph.pdf` — Q2 visualization. Pure vector (0 raster images, 9 text
  labels), same page size and layout.
- `preamble.txt` — `\usepackage{graphicx}`, `\usepackage{booktabs}`.

`python3 framework/tools/lint_output.py <OUTPUT>` → **OUTPUT LINT OK**, exit 0.

Both figures use the measured disc centres of the assignment's own drawing as the
layout, so node positions are identical between Q1 and Q2 and match the original
figure — the modification is visually obvious and a grader can compare side by side.
Node 0 is drawn orange in Q2 to make the isolated component unmistakable.

## Where I am least confident

- **The one deliberate deviation from the original drawing** is that I draw edge
  (5,8) with a bow (`arc3,rad=0.30`) so it visibly clears node 4. Faithfully
  reproducing the original straight line would recreate the exact ambiguity that
  makes this figure hard to read, and in Q2 (where node 4 survives) it would look
  like 5–4–8. I think bowing is the right call, but it is a judgement call and a
  grader comparing pixel-for-pixel with the assignment will see the difference. It
  is disclosed in the Q1 text and in the Q1 caption.
- **The transcription itself I am now confident in**, more so than I expected to be:
  the pairwise coverage separates cleanly (1.000 / 0.985 vs. <0.55, nothing in
  between), the drift measurements resolve both collinear traps in the same direction
  from both endpoints, and the result is isomorphic to the Petersen graph. That last
  point is the strongest evidence — a single misread edge would almost certainly break
  either 3-regularity or girth 5. If I am wrong, the most likely place is still the
  5/4/8 collinearity, since that is the only relation the coverage test alone could
  not settle.
- **`\ttfamily` in a `center` block** (the three-line construction snippet) is a
  slightly blunt way to typeset code. If the master's preamble loads something that
  restyles it, it may look off. It is only cosmetic.
- **Environment issue worth flagging upward, not a defect in my answer:** a stock
  `\begin{itemize}` does **not** compile on this machine. Its bullet is `\textbullet`
  from the TS1 encoding, which needs the `tcrm1000` font; that font is not prebuilt,
  METAFONT generates it, and the PK cache write then fails because `~/.TinyTeX` is
  read-only — a fatal `!pdfTeX error: ... Font tcrm1000 at 600 not found`. I
  reproduced this with a three-line document containing nothing but an itemize.
  Setting a writable `TEXMFVAR` fixes it. I avoided the problem in my own fragment by
  using `enumerate` (plain digits, no TS1), but **other problems' fragments will hit
  this**, and the master should either set `TEXMFVAR` to a writable directory or
  prebuild the font.
