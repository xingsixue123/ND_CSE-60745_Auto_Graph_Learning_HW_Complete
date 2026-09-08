# p1 — Part A: Graph Creation and Modification

## What this problem needs

- **code** — Q2 asks for the connected components of a modified graph; that is a
  computed result, so it must actually be computed (networkx), not asserted.
- **diagram** — both Q1 ("show visualization of this graph") and Q2 ("visualize
  remaining graph") explicitly demand a drawing. Two vector PDFs required.
- **plain** — the write-up: node/edge lists, what was removed, the component list.

The hard part is not Q1/Q2 arithmetic; it is **transcribing the figure correctly**.
Everything downstream depends on the edge list.

## Plan

1. Read the assignment page through all three channels (text, page PNG, figure file).
2. Transcribe the figure *programmatically*, not by eye. Detect the blue node discs,
   test every candidate pair for ink coverage, and disambiguate collinear cases with
   a departure-angle-vs-radius measurement.
3. Verify with a global invariant (degree sum, regularity, and ideally isomorphism).
4. Compute Q2 in networkx; draw both figures with a shared fixed layout.
5. Write the fragment; test-compile it; lint OUTPUT.

## Channel reconciliation

- `page_002.txt` carries the full question text for Q1 and Q2 and matches the
  master's brief verbatim. It contains **no** trace of the graph, as expected.
- `page_002.png` (whole page) shows a figure is present but is downscaled; node
  labels are not reliably readable there.
- `page_002_fig_01.jpeg` (428x588, native) is legible and is the channel I used for
  the transcription. I additionally cropped each node disc and upscaled it 4x
  (`work/labels_strip.png`) to read the digit inside each disc.

No disagreement between the brief and the page. The brief's transcription is
correct — I reproduced it independently (see below) rather than trusting it.

## Transcription method and result

`work/transcribe.py`:

- **Node discs**: threshold `B - R > 40`, flood-fill connected components, keep blobs
  > 200 px. Found exactly **10** discs, each ~1150-1260 px area (equal-area radius
  ~19.6 px) — very uniform, so no disc was split or merged.
- **Labels**: cropped a 40x40 box at each centre, upscaled 4x LANCZOS into
  `work/labels_strip.png`, and read the digits: in centre order (sorted by y then x)
  they are **0, 8, 4, 6, 5, 1, 3, 9, 7, 2**. This matches the master's mapping.
- **Edge test**: for each of the 45 pairs, sample along the straight centre-to-centre
  segment, discard samples inside any node disc, and measure the fraction covered by
  ink (dark, non-blue, dilated 2 px). 14 pairs scored 1.000 and one scored 0.985;
  every other pair scored below 0.55. Clean separation, no judgement call.
- **Collinearity disambiguation**: at each node, measure the angular positions of ink
  crossings on rings of radius r = 24, 32, 42, 55 px. A true incident edge holds a
  **constant** angle across r; a line merely passing near the centre **drifts**.

### The two traps, re-measured independently

1. **No edge (4,5), no edge (4,8).** Node 4's five ring crossings are at
   57.5/83.5/211.8 (constant → nodes 3, 9, 0) and two that drift hard:
   124.0→139.5 and 357.5→342.0. Those two converge on the bearings of node 5
   (145.8) and node 8 (339.7) respectively — i.e. they are the two ends of the
   single straight edge **(5,8)** crossing node 4's disc. Symmetrically, node 5's
   crossing drifts 324.0→328.0 toward 5→8 = 330.5 (not 5→4 = 325.8) and node 8's
   drifts 156.2→153.5 toward 8→5 = 150.5 (not 8→4 = 159.7). Confirms the master.
2. **No edge (0,6), no edge (0,9).** Node 6 has crossings at 128.8/161.5/232.0 →
   nodes 9, 1, 8; nothing near 207.6 (the bearing to node 0). Node 9 has
   145.5/261.2/303.8 → nodes 7, 4, 6; nothing near 243.0 (node 0) or 245.3 (node 1).
   So 0's neighbours are the *near* nodes 4 and 1, not the far collinear ones.

Every one of the 10 nodes shows exactly **three** constant-angle departures at the
inner radii. (At r = 55 some nodes pick up extra crossings from unrelated edges
passing through the ring — expected, and ignored.)

### Resulting edge list (15 edges)

    (0,1) (0,4) (0,5) (1,2) (1,6) (2,3) (2,7) (3,4) (3,8)
    (4,9) (5,7) (5,8) (6,8) (6,9) (7,9)

### Invariants that confirm it

- Degree sequence is all 3s; degree sum 30 = 2 x 15. Handshake lemma holds.
- Connected, triangle-free, **girth 5**.
- **Isomorphic to the Petersen graph** (`nx.is_isomorphic(G, nx.petersen_graph())`
  returns `True`). This is a much stronger check than 3-regularity: the Petersen
  graph is the canonical 3-regular girth-5 graph on 10 vertices, and a misread edge
  would essentially always destroy either the regularity or the girth. Landing on it
  is strong evidence the transcription is exactly right.
- Q2's instruction to remove edges (0,4) and (0,5) presupposes both exist — they do.

## Q2 computation (`work/solve.py`)

Remove node 1 (taking (0,1), (1,2), (1,6) with it), then edges (0,4) and (0,5).
Five edges gone. Result: 9 nodes, 10 edges, **2 components**: `{0}` (isolated) and
`{2,3,4,5,6,7,8,9}`.

## Figures

Layout = the measured pixel centres of the discs (y flipped). Deterministic, shared
between both figures, and it reproduces the assignment's own drawing so a grader can
compare side by side.

One deliberate deviation: the edge (5,8) is drawn with `arc3,rad=0.30` so it visibly
bows clear of node 4. Otherwise my figure would reproduce the original's ambiguity
and look like it has edges (5,4) and (4,8). Note `connectionstyle` is **ignored** by
`nx.draw_networkx_edges` for undirected graphs unless `arrows=True` is passed (the
default LineCollection path silently drops it) — the first attempt at this had no
effect and had to be fixed.

Both figures were rendered to PNG and inspected, including a 2.2x zoom on node 4 to
confirm the bowed edge actually clears the disc (`work/zoom_*.png`).

## LaTeX environment gotcha

A stock `\begin{itemize}` **fails to compile** on this machine: its bullet is
`\textbullet` from the TS1 encoding, which needs `tcrm1000`; that font is not
prebuilt, METAFONT generates it, and then the PK cache write fails because
`~/.TinyTeX` is read-only, producing a fatal
`!pdfTeX error: ... Font tcrm1000 at 600 not found`. Verified this reproduces with a
three-line document containing nothing but an itemize. Setting a writable `TEXMFVAR`
fixes it, but I cannot control the master's environment, so I used `enumerate`
(plain digits, no TS1) in `answer.tex` instead. This is worth flagging upward.
