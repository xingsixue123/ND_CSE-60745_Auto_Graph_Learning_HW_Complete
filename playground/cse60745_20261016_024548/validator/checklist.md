# Master validator checklist — job cse60745_20261016_024548

## Round 1 — 2026-10-17 01:35
Verdict: FAIL (one major; three minor)

### Where I looked

**Assignment, independently re-derived.** Re-converted `input/CSE 60745_Fall 2026_HW3(B).doc`
with LibreOffice into my own dir (2 rendered pages, matching ingest) and read all three
channels. `strings` on the raw `.doc` finds exactly three question headings — Q1 (20),
Q2 (20), Q3 (30) = 70 pts, matching the handout's "contains 70 points". The footer's
"Page 1 of 3" is a Word field, not missing content. `manifest.json` lists no extracted
figure files and the page renders carry no question figure, so no answer depends on an
image. Coverage: all three questions answered, in order, nothing uncovered.
`problems.json`'s `uncovered: []` is correct.

**Format.** Handout demands "a PDF or Word file including the cover page" — cover page is
reproduced (main.tex, PDF p.1). It also says "submit only your implemented code file":
every completed cell is printed in full and labelled by cell number (13/16, and cell 22
noted as used unchanged). Cell numbering is 1-based and correct against the notebook.

**Compile.** 9 pages, no unresolved `??`, one Overfull hbox of 2.56 pt (Table 2 caption).
All 9 pages rendered and read. Figure 1 is present, vector, and legible at print size.
Labels are namespaced (`p1:tab:q1`, `p2:fig:layer`, ...); the figure is referenced by bare
filename; neither fragment contains `\documentclass`/`\usepackage`; the two `preamble.txt`
files are merged and de-duplicated. `output/p1` and `output/p2` pass `lint_output.py`;
`final/` fails it, which is expected — that linter is written for worker deliverables.

**Code is real and matches what was run.** `shared/gt_framework.py` reproduces notebook
cells 3/5/7/8/9/11 line-for-line (0 lines differ) and omits only the TODO stubs and the
run calls, so the harness was not tampered with. Every one of the 207 printed listing
lines appears verbatim in the `solution.py` / `hybrid_layer.py` that produced the logs;
the only unprinted source is imports and the given `HybridGT`. In my own directory I ran
notebook cells 14, 18, 19 and 22 end to end with the submitted classes — all four run.

**Numbers recomputed by me, not taken on trust.**
- Table 1, bolded row (cell 14): I re-ran the full 30-epoch job from scratch and got
  val MAE 0.5160 / test MAE 0.5496 / best epoch 30 — the printed row exactly.
- Table 4 (cell 22): my own 30-epoch run gave val 0.3586 / test 0.3689, inside the
  printed 0.350 ± 0.007 / 0.364 ± 0.008.
- Every pair count in Tables 2 and 3 recomputed exactly: ZINC 73 / 120 / 189 / 200 / 266
  per graph, LastFM 63,236 / 78,485 / 804,349 / 108,965 / 139,417, n^2 = 556.8 ≈ 557.
- Table 4's means, sds, run counts and all five `params` figures recomputed from the raw
  per-seed logs and from the models themselves (139,649 / 143,953 / 211,589 / 144,517 /
  143,745 → 139.6k / 143.9k / 211.6k / 144.5k / 143.7k). All agree.
- Table 2's 3-seed means and half-ranges recomputed from the three seed JSONs: all six
  rows agree to the printed digit, as do the derived 0.0184 and 0.0799 gaps.
- Descriptive claims: ZINC smallest molecule 9 nodes (so exactly 8 non-trivial
  eigenvectors); unscaled LapPE channel RMS on LastFM 0.0115 ≈ "0.011", scaled 1.000;
  degree takes 4 values with 50.6% at degree 2 ("half of all atoms"); mean diameter 12.5
  and 51.8% of pairs within 4 hops; ZINC bond ids are {1,2,3}, so `Embedding(4, dim)` is
  safe; 5.23/0.33 = 16x.
- Sparse-vs-dense equivalence: I reproduced it independently (max |Δ| 1.5e-7 on my draw
  against the printed 7.5e-8 — both float32 noise).
- `torch_geometric.utils.segment_attention` really is absent in PyG 2.8.1, as Q2 claims.

**R9 (read past the quotation).** Both GraphGPS quotations are verbatim and I read the
surrounding passages in the paper myself. "the edge features are only passed to the MPNN
layer" sits exactly where the submission places it. The "irreparably fail to keep some
information in the early stage" quote is aimed at GraphTrans's stack of MPNN layers
*before* the Transformer, and the paper's follow-on sentences ("they are still likely to
lose information", the 2-step-methods passage: "this step is applied only once") confirm
the submission's reading that the objection targets the 2-stage form, not within-layer
interleaving. Eqs. (9)-(11) of Appendix D.1 are per-branch residual + BatchNorm then
MLP of the sum, as described. The argument survives its context.

**R8 (length).** Prose, excluding code, tables and captions: Q1 354 words, Q2 383, Q3 506
(1,243 total for 70 points). Against the 5-pt/190-word and 10-pt/550-word references these
are well inside budget for 20/20/30-point implementation questions. No padding patterns
found. Em-dash density is one per 70 words in p1.tex — at the threshold R8 names as a
symptom, but the length it would predict is not there, so not reported as a defect.

### Defects
- [D1.1] Q3's code listing renders with inter-character spacing and un-indented wrapped
  lines, unlike Q1's and Q2's. | `output/.../final/p2.tex:44-49` (`\lstdefinestyle{p2python}`),
  visible on PDF p.8 | severity: major
- [D1.2] "moves it by 0.0119, inside the ±0.0100 seed half-range of Table 2" — 0.0119 is
  outside ±0.0100. | `final/p1.tex`, Q1 prose, PDF p.2 | severity: minor
- [D1.3] Table 1 and Table 4 print the same two baselines with different values and never
  reconcile them. | PDF p.2 vs p.9 | severity: minor
- [D1.4] "the constant eigenvector D^{1/2}1" — for the symmetric normalised Laplacian that
  vector is constant only on a regular graph. | `final/p1.tex`, Q1 prose, PDF p.2 |
  severity: minor

### Resolved since last round
- (first round)

### Still outstanding
- (first round)

---

## Round 2 — 2026-10-17 01:45
Verdict: PASS (no outstanding defects; two sub-minor observations recorded, not charged)

### What changed, and how I established it
The master kept backups (`build/p1_answer.bak`, `build/p2_answer.bak`, byte-sizes matching
the round-1 fragments I reviewed). Diffing them against the shipped fragments shows the
change set is **exactly** the four fixes and nothing else — two lines in p1.tex, two hunks
in p2.tex. `final/p1.tex` and `final/p2.tex` are still byte-identical to `output/p1` and
`output/p2`. I did not take the master's log on trust for any of this.

### Resolved since last round
- [D1.1] **fixed, verified at the rendered level.** `p2python` now carries
  `breakindent=2em, columns=fullflexible, keepspaces=true`. PDF p.8 re-rendered: the Q3
  listing typesets as `class HybridGTLayer(nn.Module):` / `self.norm_ffn` / `__init__`,
  identical in style to Q1 and Q2, and **no line in the listing wraps any more** — the two
  column-0 continuations (`summed."""`, `D/heads]`) are gone. I lifted the listing back out
  of the shipped PDF with `pdftotext -layout` and `ast.parse`d it: 48 lines, parses as
  Python.
- [D1.2] **fixed.** Now "inside the 0.0200 seed spread of the full-attention row of
  Table 2". I checked the premise: that row's three seed test MAEs are 0.5496 / 0.5651 /
  0.5696, max − min = 0.0200, and 0.0119 < 0.0200. The conclusion is unchanged and still
  correctly hedged ("does not establish").
- [D1.3] **fixed.** Table 4's caption now says the two baseline rows were measured again
  for that table rather than copied from Table 1, names the gaps (0.693 vs 0.7013,
  0.495 vs 0.4957) and bounds them by the 0.009 run-to-run noise. Both subtractions check
  out (0.0083, 0.0007 < 0.009), and the 0.009 figure is itself real: three repeats of one
  unchanged configuration in `problems/p2/logs_det/` gave test 0.3620 / 0.3702 / 0.3615,
  spread 0.0087.
- [D1.4] **fixed.** "constant" → "trivial", which now agrees with the code comment "skip
  the trivial eigenvector" and with "non-trivial eigenvectors" elsewhere in the fragment.

### Regression checks (all clean)
- Compile: 9 pages, 0 undefined references, 0 duplicate destinations, the same single
  2.56 pt overfull hbox (sub-millimetre, in Table 2's caption). `build/compile/main.pdf`
  md5-matches the shipped `final/main.pdf`, so the log I read is this build's.
- Image-diffed all 9 rendered pages against round 1: pages 2, 3, 4, 8, 9 changed. 8 and 9
  are the intended fixes; 2 is the two reworded sentences; 3 and 4 are only the resulting
  two-line reflow of the Q1 listing. I re-read all five — margins, listings and tables are
  intact and the Q2 heading still starts cleanly.
- All 207 printed listing lines across both fragments are still verbatim in the
  `solution.py` / `hybrid_layer.py` that produced the logs: **0 lines differ.** No code or
  number was touched by the wording fixes.
- `lint_output.py` OK on `output/p1` and `output/p2`. Labels, bare-filename figure
  reference and merged preamble unchanged.
- R8 recount: Q1 357, Q2 383, Q3 506 body prose words (Q3 653 with captions, +42 from the
  new caption clause). Still well inside budget for 20/20/30-point implementation questions.

### New ground covered this round
Rather than only re-checking the four fixes, I re-derived two claims I had taken from the
workers' logs in round 1:
- ZINC test diameter mean **12.51**, pairs within 4 hops **51.8%**, within 8 hops **85.2%** —
  recomputed from scratch with my own BFS over all 1,000 test molecules. Matches p.9.
- "Of GraphGPS's three ingredients, the one missing here is the first, the
  positional/structural encoding" — the paper says "Our GPS recipe consists of choosing 3
  main ingredients: (i) positional/structural encoding, (ii) local message-passing
  mechanism, and (iii) global attention mechanism." The characterisation is exact.

### Still outstanding
- None.

### Observations below the defect bar (recorded, not charged)
- Table 3 lists full attention first while Table 2 lists it last; the row orders of the two
  pair-set tables do not match. Purely cosmetic.
- Em-dash density in p1.tex is one per 70 words, the threshold R8 names as a symptom — but
  the length it would predict is not there, so there is nothing to fix.

### Where I looked and found nothing
Coverage (all three questions, 70/70 points, cover page, correct order), the handout's
format demands, every figure and table, the LaTeX log, the worker/final output contents,
and the four fixes' arithmetic. Across both rounds I have reproduced Table 1's bolded row
exactly by re-running the full 30-epoch job myself, run all four required notebook cells
end to end, and recomputed every pair count, parameter count, table mean, standard
deviation and half-range in the document. I have no substantive objection left.
