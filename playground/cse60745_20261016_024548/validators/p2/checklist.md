# Validator checklist — p2 (Q3: Hybrid Graph Transformer, 30 pts)

## Round 1
Verdict: PASS

### What I checked, and how

**Ground truth (R7).** Read `ingest/.../CSE 60745_Fall 2026_HW3(B)/page_002.txt` and
`page_002.png` myself. Q3's wording in the brief and in `answer.tex` is verbatim from the
page. `manifest.json` reports `figures: []` and `n_images: 1` for both pages; the page PNG
confirms the single image is the ND monogram in the header, so there is no figure channel
for this problem and nothing in the answer rests on one. `pdfinfo` reports 2 pages (the
"Page 1 of 3" footer is a stale field in the source `.doc`, not a missing page).
Cells 20/21/22 in `ingest/pages/task6_graph_transformer-1/alltext.txt` match the brief;
`HybridGT` in `hybrid_layer.py` is byte-identical to cell 22's class (checked with difflib,
not by eye), and the `lstlisting` in `answer.tex` is byte-identical to the
`HybridGTLayer` block of `hybrid_layer.py`, so the listing is the code that ran.
`diff shared/gt_framework.py problems/p2/gt_framework.py` → identical, i.e. the framework
was not edited.

**Correctness, re-derived independently** (`validators/p2/rerun/val_check.py`, written
without reusing the worker's `check_isolation.py` code paths):
- [A] whole-model: each of 12 ZINC graphs run alone vs inside one batch, max |Δ prediction|
  = 4.5e-08. No cross-molecule attention leak — the failure mode the brief warns about.
- [B] permuting the graph order in the batch changes nothing (Δ = 0.0).
- [F] deliberately merging two graphs into one `batch` id *does* change their outputs
  (1.9e-01) and leaves every other graph bit-identical — the mask is doing real work, the
  isolation is not an accident of the data.
- [C] `local_branch` reproduced by a dense per-edge reference loop, Δ = 0.0 (GINE formula
  and src/dst direction correct).
- [D] `edge_index` is symmetric with symmetric bond types, so the direction convention
  cannot matter; [E] bond ids over all 10000 train graphs are {1,2,3}, embedding sized 4
  as the brief instructed.
- `val_abl.py`: `AblationGT(HybridGTLayer)` has identical parameter names and identical
  post-`_reset` initialisation to `HybridGT()` (Δ = 0.0), and for `LocalOnlyLayer` /
  `GlobalOnlyLayer` too — so an ablation row differs only by the branch it drops. The
  reported active-parameter counts (211589 / 144517 / 143745 / 244613) match my own
  hand-computed per-layer arithmetic exactly.

**Numbers.** Re-aggregated every `### result` line in `logs/` with my own script: all seven
rows of Table 1 (val/test mean and sd to 3 dp, params, run counts) reproduce exactly. The
logs are genuine console captures, not hand-written. I re-ran `hybrid seed 0 epochs 30`
from scratch in my own directory: test MAE 0.3749 vs the worker's 0.3693 — 0.0056 apart,
inside the 0.0087 run-to-run floor the worker measured and disclosed in `logs_det/`. Adding
my run to the sample moves hybrid's mean to 0.366, which leaves the headline conclusion
(global branch within noise of removing it) intact.

**Facts quoted about ZINC.** Recomputed with networkx instead of the worker's hand-rolled
BFS: mean test-split diameter 12.51 (claim 12.5), 51.78% of node pairs within 4 hops (claim
51.8%), degree takes 4 values over 277,864 nodes with 50.6% at degree 2 (claim identical).

**R9.** Downloaded-paper text checked for both quotations and their surroundings.
"the edge features are only passed to the MPNN layer" is §3.3 *Update function*, used for
exactly the claim it makes. "these layers could irreparably fail to keep some information
in the early stage" is §3.3 *Preventing early smoothing*, and the answer correctly scopes it
to GraphTrans's MPNN-block-then-Transformer rather than to per-layer stacking — then
measures the stacked variant instead of resting on the paper. GraphGPS Eqs. (9)-(11) are in
Appendix D.1 and are the per-branch residual+BatchNorm form the answer says it follows. "3
main ingredients: (i) positional/structural encoding, (ii) local message-passing, (iii)
global attention" is verbatim from the abstract.

**Deliverables.** `answer.tex` compiles clean in a minimal wrapper with only the packages in
`preamble.txt` (+geometry): 4 pages, no Overfull/Underfull boxes, no undefined references
after a second pass. No `\documentclass` / `\usepackage` / `document` env. Every label,
the figure filename and the listing style are namespaced (`p2:fig:layer`, `p2:tab:zinc`,
`fig_p2_layer.pdf`, `p2python`); figure referenced by bare filename; no absolute paths;
nothing from Q1/Q2 mentioned. Figure rendered to PNG and read: legible at print size,
382pt wide, vector, no overlapping or clipped text, and it accurately depicts the code
(two branches → residual+LayerNorm each → sum → residual MLP → LayerNorm).
`lint_output.py` exits 0. `downloads.md` records the one download (the GraphGPS PDF) and
the two copies.

**Length (R8).** Worker's `wordcount.py` reports 475 prose words; my own independent count
gives 481. Target is ~400, so ~19% over — inside R8's quarter tolerance.

### Defects
- [1.1] `answer.tex` p.4: "Every hybrid run peaks in the final three epochs" is true of the
  six logged runs (best epochs 28-30) but is not robust: my independent re-run of the
  identical configuration (`hybrid`, seed 0, 30 epochs) peaked at epoch 26. The conclusion
  it supports ("30 stops it early") is independently carried by the 100-epoch runs peaking
  at epochs 94 and 98, so only the universal phrasing is at fault. | severity: minor
- [1.2] The 93-word table caption restates two things the prose immediately below already
  says (the run-to-run noise floor; that the bold row is the submitted layer, not the best
  number). Captions are excluded from the R8 count, so this is not a rule breach, but it is
  the "summarising your own answer" failure mode parked in a caption; ~35 words could go. |
  severity: minor
- [1.3] `answer.tex` p.4: "Of GraphGPS's three ingredients, the one missing here is the
  first, the positional/structural encoding." Degree centrality *is* a structural encoding
  — which the two preceding sentences themselves argue — so "missing" overstates what the
  measurement shows; "weakest" would match the evidence. | severity: minor
- [1.4] `answer.tex` p.1: "a residual two-layer MLP follows: GraphGPS Eqs. (9)-(11)".
  Eq. (11) is `X = MLP(X_M + X_T)` with no residual or norm around the MLP; the residual and
  BatchNorm around the MLP come from the Figure D.1 caption ("After each functional block
  (an MPNN layer, a global attention layer, an MLP) we apply residual connections followed
  by batch normalization"). The implementation is faithful to GraphGPS; only the equation
  numbers are slightly under-cited. | severity: minor
- [1.5] `\label{p2:tab:zinc}` is defined but never `\ref`'d. | severity: minor (cosmetic)

### Resolved since last round
(first round)

### Still outstanding
1.1-1.5, all minor. None of them changes a number, a conclusion, the compile, or the
grade-bearing content, so they do not hold up the submission.
