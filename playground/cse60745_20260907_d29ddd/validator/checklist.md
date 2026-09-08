# Master validator checklist — job cse60745_20260907_d29ddd

## Round 1 — 2026-09-07

Verdict: PASS (with minor defects noted)

### What I did

Read the assignment through all three channels (rule R7):
`alltext.txt` + `page_00N.txt`, the rendered `page_00N.png`, and the native-resolution
figure `page_002_fig_01.jpeg`. Enumerated the questions myself from the assignment text
rather than trusting `problems.json`, then diffed against what was answered.

Read the deliverable `output/.../final/main.pdf` through both channels: rendered all
10 pages to PNG and inspected each, plus extracted text, plus recompiled from source
to read the LaTeX log.

### Coverage — complete, 100/100 pts accounted for

| Question | Pts | Sub-parts required | Answered in | PDF pages |
|---|---|---|---|---|
| Q1 Graph Creation | 15 | build graph from figure; visualize | p1 | 2–3 |
| Q2 Graph Modification | 15 | remove node 1, edges (0,4),(0,5); list components; visualize | p1 | 3–4 |
| Q3 Graph Creation | 10 | node count; edge count; # connected components | p2 | 5 |
| Q4 Graph Essentials | 30 | (a) LCC node+edge count; (b) visualize 2nd-largest CC; (c) plot degree distribution | p2 | 5–7 |
| Q5 Graph Measures | 30 | (a) eigenvector top-10; (b) Katz top-10; (c) avg clustering + avg Jaccard | p3 | 8–10 |

15+15+10+30+30 = 100. No question or sub-part unanswered. Both "visualize" sub-parts
(Q2, Q4b) and the "plot" sub-part (Q4c) are present as actual figures, not prose.

### Correctness — independently recomputed, everything matches

**Q1 figure transcription (the highest-risk item, since it exists only as an image).**
I did not read the edges by eye. I segmented the 10 node discs in
`page_002_fig_01.jpeg` and, for every one of the 45 candidate pairs, sampled along the
segment between the disc boundaries testing for drawn ink. Result: 15 pairs at coverage
1.000, the highest non-edge at 0.558 — a clean separation. The recovered edge set is
identical to the submission's, and is the **Petersen graph** (3-regular, girth 5),
confirmed by `nx.is_isomorphic`. Landing on a named graph independently is strong
corroboration.

The submission's remark about the (5,8) edge is correct and I verified the geometry:
node 4's centre lies 13.6 px off the straight 5–8 line while the disc radius is ~19 px,
so the single edge clips node 4's disc without passing through its centre. My detector
independently rejects (4,5) at 0.469 and (4,8) at 0.356.

**Everything else, recomputed from `input/graph-1.txt`:**

- Q2: 9 nodes, 10 edges, 2 components — {0} and {2,3,4,5,6,7,8,9}. Matches.
- Q3: 26,728 nodes / 26,377 edges / 4,104 components. Matches. (0 self-loops, no duplicate edges — confirmed.)
- Q4a: LCC 13,903 nodes / 16,695 edges. Matches.
- Q4b: 2nd-largest CC 69 nodes / 80 edges; component size list 13903, 69, 30, 30, 29, 26, 23, 21, 21, 20 — no tie for 2nd. Matches, including the claim that the tie is at 3rd place.
- Q4c: min 1, max 59 (node 22777), mean 1.9737, median 1; deg-1 = 13,942, deg-2 = 7,423; 37 distinct degree values. Matches.
- Q5a: top-10 eigenvector nodes **and** values match to all 6 printed digits (16485, 22777, 14618, 21928, 2884, 1197, 9068, 17902, 1324, 25747). Default `nx.eigenvector_centrality` does converge, as claimed.
- Q5b: top-10 Katz nodes and values match exactly (16485, 22777, 9068, 14618, 2884, 17902, 17546, 21928, 1197, 9740).
- Q5c: avg clustering 0.1005391519 → 0.100539 ✓; avg Jaccard 0.0413042246 → 0.041304 ✓.
- Secondary claims spot-checked and correct: λ_max = 8.762217 and 1/λ_max = 0.114126 (so α=0.1 is admissible) ✓; 1,926 triangles ✓; clustering restricted to deg≥2 nodes = 0.210168 ✓; Jaccard excluding endpoints = 0.084305 ✓; 12,908 nodes with eigenvector centrality < 1e-12 ✓; CC2 diameter 17 with hubs of degree 7 and 6 ✓; the stated degree of every named node ✓.

**Figures verified computationally, not by eye:**

- `fig_p1_q1_graph.pdf`: annulus scan around each disc gives degree 3 for all 10 nodes → 3-regular, consistent with Petersen.
- `fig_p1_q2_graph.pdf`: node 0 (orange) has degree 0; degree sum over the other 8 nodes = 20 = 2×10 edges. Correct.
- `fig_p2_cc2.pdf`: exactly 69 node markers, and their area tiers match the true CC2 degree histogram {7:1, 6:1, 5:1, 4:11, 3:7, 2:29, 1:19}. Correct.

### PDF and format

- Compiles clean from the shipped sources; 10 pages, A4. No undefined or multiply-defined references.
- All 4 figures embed as vector graphics and render (no missing-file boxes). Legible at printed size.
- Equations render as math, not raw source. Question numbering (Q1–Q5, Q4a/b/c, Q5a/b/c) matches the assignment.
- No duplicated or orphaned sections from a bad `\input`.
- Cover page present, reproducing the assignment's own header block (including its "Sumission" typo — faithful, not an error).
- `lint_output.py` exits 0 on p1, p2 and p3. `final/` contains no `.aux`/`.log` residue.
- Altitude is appropriate: no pasted code dumps, no repeated boilerplate, no duplicated figures, no debugging residue.

### Defects

- [D1.1] `p3.tex` Q5(a) "Interpretation", PDF p.8: claims the giant component's spectral radius is 8.7622 "versus at most **3.63** for every other component". The true maximum over the 4,103 non-giant components is **3.9193** (a 9-node, 16-edge component); the next values are 3.8182, 3.7677, then 3.6331. It looks like only the components largest by *node count* were checked, missing smaller-but-denser ones. The conclusion drawn (the principal eigenvector is supported on the giant component) is unaffected. | Resolution: change `3.63` to `3.92`. | severity: **minor**
- [D1.2] `p2.tex` lines 69–72, PDF p.5: overfull `\hbox` of 26.73 pt — the inline `\texttt{sorted(nx.connected_components(G), key=len, reverse=True)[1]}` will not break, so the line overhangs the right text margin by ~0.37 in. Visible in the render; no text is lost off the paper. | Resolution: break the code across two lines, or wrap the paragraph in `\sloppy`. | severity: **minor**
- [D1.3] `p3.tex` Q5(c), PDF p.10: "21,167 of the 26,377 edges (**80.3%**)" — 21167/26377 = 80.25%, which rounds to 80.2%. The count 21,167 itself is correct. | Resolution: change `80.3` to `80.2`. | severity: **minor**

### Withdrawn during this round

- An initial marker count on `fig_p2_cc2.pdf` returned 68 rather than 69 nodes. This was an
  artefact of my own detector: the brightness cap `max(RGB) < 252` excluded the brightest
  viridis-yellow marker (the degree-7 hub, #FDE725). Re-run without the cap gives exactly 69.
  Not a defect in the submission.

### Where I looked and found nothing

Coverage against my own enumeration of the assignment; every reported number in all three
fragments recomputed from the source data; all four figures verified structurally rather
than visually; all 10 PDF pages inspected as images; LaTeX log inspected for reference and
box warnings; output-directory hygiene linted.

### Verdict rationale

All substantive checks pass: coverage is complete, every graded quantity is independently
confirmed correct, all figures encode the right graphs, and the document compiles and reads
as a homework submission. The three defects are minor — one wrong number in a voluntary
interpretive aside, one line-breaking overhang, one rounding slip — and none affects a
requested answer. Passing with these noted; D1.1 and D1.3 are one-number edits and should
be fixed if the master makes any further pass over the document.

## Round 2 — 2026-09-07

Verdict: PASS (with one minor defect noted)

### What I did

Round 1 was already a full pass (coverage enumerated from the assignment itself, every
reported number recomputed from `graph-1.txt`, all four figures verified structurally,
all 10 PDF pages inspected). Round 2 is a much smaller submission, so rather than repeat
that wholesale I (a) established exactly what changed, (b) verified each change actually
fixes the defect it claims to, (c) checked the change did not break anything downstream,
and (d) spent the remaining effort on claims I had leaned on least in round 1.

**Change surface.** Diffed all five shipped sources against my round-1 copies and md5'd
the four figures. All four figures are **byte-identical**. `main.tex`, `preamble.tex` and
`p1.tex` are **identical**. Exactly three edits, one per round-1 defect — no collateral
edits, no silent rewrites. Verified the shipped `main.pdf` is genuinely rebuilt from these
sources (pdftotext of the shipped PDF is identical to pdftotext of my own recompile).

### Resolved since last round

- **[D1.1] fixed.** `p3.tex:62` now reads `3.9193` (was `3.63`). Independently recomputed
  the spectral radius of every one of the 4,104 components by dense `eigvalsh` on each
  induced subgraph: ρ(giant) = 8.762217, and the top non-giant values are **3.9193**
  (n=9, m=16), 3.8182, 3.7677, 3.6331, 3.5873. The new number is exactly the true maximum,
  and it is the same value I derived independently in round 1. Confirmed on PDF p.8.
- **[D1.2] fixed.** `p2.tex` now breaks the long `\texttt{sorted(...)}` call out into a
  `\begin{center}` block on its own line. Recompiled from the shipped sources: **zero**
  `Overfull` and zero `Underfull` warnings in the entire log (was 26.73 pt overfull), 10
  pages, no undefined/multiply-defined references. Confirmed visually on rendered p.5 —
  the code line now sits inside the text block.
- **[D1.3] fixed.** `p3.tex:141` now reads `80.2\%`. Recomputed: 21,167 of 26,377 edges
  have zero-Jaccard endpoints = 80.2479% → 80.2%. The count 21,167 re-confirmed. PDF p.10.

### Regression check on the reflow

The added `center` block lengthens p2 by two lines, which pushed text across page
boundaries (p.5→6 and p.6→7). I checked this did not damage the layout rather than
assuming it: per-page text diff shows pages 1–4 and 9 byte-identical, and the only changes
on 5/6/7 are the two migrating sentences. Page count is still 10. Rendered pages 5, 6 and 7
and inspected them: Figure 3 (CC2, with colour bar and caption) and Figure 4 (degree
distribution, both panels) still render as vector graphics in their correct sections, no
missing-file boxes, no orphaned headings, no stranded captions, no page left absurdly
sparse. Pages 8 and 10 differ only in the two corrected numbers.

### Additional independent checks (claims I had scrutinised least in round 1)

Run against `input/graph-1.txt`; the exact/numpy columns required scipy, so these were run
under the py311 env (NetworkX 3.3, SciPy 1.16.3):

- "only 6 of these 10 nodes are also in the top 10 by degree" — true top-10 by degree is
  {22777, 16485, 9068, 17546, 14618, 1770, 17902, 2403, 2884, 7262}; overlap with the
  eigenvector top-10 is exactly **6**. ✓
- The entire fifth "Centrality (exact)" column of Table 4 — all ten values reproduce
  `eigenvector_centrality_numpy` to within 5e-6 (**no mismatches**), as does the whole
  fourth "default" column. ✓
- "the exact computation puts node 17902 ahead of node 9068" — true. ✓
- "the largest value attained by any edge is 2/3" — max edge Jaccard = 0.666667. ✓

### Format / hygiene

`lint_output.py` exits 0 on all three worker dirs (`p1`, `p2`, `p3`); each holds only
`answer.tex`, `preamble.txt` and its `fig_*.pdf`. `final/` carries no `.aux`/`.log`
residue. The merged `preamble.tex` (amsmath, booktabs, float, graphicx) is exactly the
de-duplicated union of the three worker `preamble.txt` files. `p3`'s reference to
`graph.txt` is correct — the assignment text itself names the file `graph.txt`, and `p2`
explicitly notes it ships as `graph-1.txt`.

### Defects

- [D2.1] The two numeric corrections were applied only to `output/.../final/p2.tex` and
  `final/p3.tex`, and were **not** propagated back to the worker deliverables:
  `output/.../p3/answer.tex:61` still says `3.63` and `:139` still says `80.3\%`, and
  `p2/answer.tex:71` still carries the unbroken overfull code line. The OUTPUT tree
  therefore contains two copies of the same claim disagreeing with each other, and a
  re-assembly from the worker dirs would silently reintroduce all three round-1 defects.
  The graded artefact (`final/main.pdf`) is correct, so no answer is affected. | Resolution:
  copy the three corrected lines back into `p2/answer.tex` and `p3/answer.tex`. |
  severity: **minor**

### Still outstanding

- None. D1.1, D1.2 and D1.3 are all genuinely fixed in the assembled document.

### Where I looked and found nothing

Full source diff and figure checksums; recompile from shipped sources with log inspection
for box and reference warnings; per-page text diff and visual inspection of every reflowed
page; independent recomputation of both corrected numbers plus four previously
under-checked claims; preamble merge; output-directory lint on all three worker dirs.

### Verdict rationale

The submission does exactly the three things round 1 asked for, does nothing else, and both
corrected numbers are exactly right against my own recomputation. The overfull box is gone
outright rather than papered over, and the page reflow it caused damages nothing. Coverage
and correctness were established in round 1 and the change surface is too small to have
disturbed them — figures are byte-identical and pages 1–4 and 9 are unchanged. The one
remaining defect is a provenance inconsistency in intermediate files that does not touch
the answer document. Passing with that minor defect noted.
