# p1 validator checklist

## Round 1
Verdict: FAIL

### What I verified independently (and that passed)

- **Ground truth (R7).** Read `page_002.txt`, `page_002.png` and `manifest.json` for the
  assignment. Text and page image agree verbatim; `figures: []` on all three pages and the
  single `n_images: 1` is the ND monogram in the header. The worker's channel reconciliation
  is correct and the master's brief matches the page. No figure to transcribe.
- **Table 1 statistics — fully reproduced.** Re-ran `stats.py` against the worker's venv.
  Every row of Table 1 matches the script output exactly (Cora 2,708/5,278/10,556/1,433/7;
  CiteSeer 3,327/4,552; PubMed 19,717/44,324; Coauthor CS 18,333/81,894; Physics
  34,493/247,962; Amazon Computers 13,752/245,861; Photo 7,650/119,081; Cornell 183/280;
  Texas 183/295; Wisconsin 251/466; Actor 7,600/26,752; Chameleon 2,277/31,421; Squirrel
  5,201/198,493; PPI 56,944/793,632/121).
- **Reddit — reproduced.** Re-ran `stats_reddit.py`: N=232,965, E_und=57,307,946,
  E_dir=114,615,892, d=602, C=41. Matches the answer. Average-degree invariant confirmed:
  2*57,307,946/232,965 = 492.0, equal to the GraphSAGE paper's stated figure.
- **Homophily — reproduced twice.** Re-ran `homophily.py` (exact match), then recomputed
  independently from the raw Geom-GCN text files with my own script, no PyG and no worker
  code (`rerun/indep_homophily.py`): Cornell 0.1220, Texas 0.0615, Wisconsin 0.1703, Actor
  0.2165, Chameleon 0.2339, Squirrel 0.2234. The worker's arithmetic is right. (What is
  wrong is the convention and the missing footnote — see 1.1.)
- **OGB figures traced to source.** Every number in Table 2 and every split/metric/negative
  count in the prose greps verbatim out of the worker's downloaded `research/ogb_*.txt`
  (Hits@50/100,000 negatives; Hits@20/~100,000; Hits@100/3,000,000; MRR/1,000 per source;
  papers100M 172 classes and ~1.5M labelled; proteins 8 species/112 tasks/8-d edge features).
  Nothing fabricated.
- **Social/PPI figures traced to source.** BlogCatalog 10,312/333,983, Flickr 80,513/5,899,882,
  YouTube 1,138,499/2,990,443 all found in `research/deepwalk.txt` Table 1; node2vec PPI
  3,890/76,584 found in `research/node2vec.txt`.
- **Citations.** Spot-checked all 36 against my own knowledge and, for the contested ones,
  the primary sources. Venues, years and author lists are correct, including the ones that
  are commonly got wrong (VGAE = NIPS 2016 BDL *workshop*; GRACE = ICML 2020 GRL+ *workshop*;
  Shchur et al. = NeurIPS 2018 R2L *workshop*; BGRL = ICLR 2022; Gasteiger né Klicpera;
  Belkin & Niyogi NIPS 2001 + Neural Computation 2003). One slip found — see 1.4.
- **Figures.** Rendered all three PDFs to PNG and looked at them. Vector, single-page,
  native widths 5.8/4.9/5.4 in, placed at 0.93/0.78/0.84\textwidth so fonts scale ~1:1.
  Measured ink bounding boxes — no clipping (e.g. schema figure ink spans cols 18–846 of
  865). Legible, axes/legends present where needed, link-prediction worked example is
  arithmetically correct (positive at rank 2 → Hits@1=0, Hits@3=1, RR=1/2).
- **LaTeX compliance.** No `\documentclass` / `\usepackage` / `document` environment.
  All 13 labels namespaced `p1:`. Figures referenced by bare filename. The only
  `\renewcommand` (`\arraystretch`, line 510) is scoped inside a `center` environment and
  will not leak into the master. Compiled in a minimal wrapper: exit 0 both passes,
  14 pages, zero undefined references, zero underfull boxes, one overfull hbox of 5.2pt.
- **`lint_output.py`** exits 0. **`downloads.md`** records the venv, torch, torch_geometric,
  scipy, pandas, every dataset and every curl'd document (R3 satisfied).
- **Scope/consistency constraint.** Strictly homogeneous; no DBLP/ACM/IMDB, no
  metapath2vec/HAN/HGT. Micro-F1, Macro-F1, MRR and Hits@K are defined exactly as the brief
  mandated, so they cannot contradict Problem 2.

### Defects

- **[1.1] Homophily values silently diverge from the source the answer itself cites, and the
  claimed external check was not actually performed.** | `answer.tex` Table 1 `h_edge`
  column (lines 214–219) and `submission.md` lines 127–129 | severity: **major**

  Table 1 reports Texas 0.06, Cornell 0.12, Wisconsin 0.17. Zhu et al. (NeurIPS 2020),
  which `answer.tex` cites by name at lines 72–73 as the source of this benchmark suite,
  publishes Texas **0.11**, Wisconsin **0.21**, Cornell **0.3** (Table 5).

  I traced the cause: `homophily.py` line 24 (`mask = src != dst`) drops self-loops from
  the homophily count, whereas the published convention keeps them. Self-loops are
  trivially same-label, so including them reproduces the published values exactly —
  Texas 0.1119 → "0.11" and Wisconsin 0.2060 → "0.21". (Cornell stays irreconcilable at
  0.132; that one appears to be an error in Zhu et al. themselves, since their |E|=280 for
  Cornell matches this graph exactly.)

  This is compounded by an internal inconsistency *within the same table row*: the `|E|`
  column **does** include self-loops. I verified this exactly — Cornell 277+3=280,
  Texas 279+16=295, Wisconsin 450+16=466, Actor 26,659+93=26,752, Chameleon
  31,371+50=31,421, Squirrel 198,353+140=198,493, and those totals match Zhu et al.'s
  published |E| column exactly. So |E| and h_edge in adjacent columns use opposite
  self-loop conventions.

  The brief was explicit: *"if a figure varies between sources ... say so in a footnote
  rather than silently picking one."* The worker footnoted Cora and Reddit but not this,
  which is the single largest divergence from the literature in the table.

  Separately, `submission.md` asserts *"These agree with the published Geom-GCN / Zhu et al.
  values, which is a further external check."* They do not agree for 3 of 13 datasets.
  A check was claimed that does not hold.

  **To fix:** either (a) switch the homophily denominator/numerator to include self-loops so
  the column matches both the published values and the adjacent |E| column, or (b) keep the
  self-loop-free convention and add a footnote stating the convention, giving the published
  values, and noting the Cornell discrepancy. Either way, correct the claim in
  `submission.md`.

- **[1.2] Table 1 omits the directed/undirected column the brief explicitly required.** |
  `answer.tex` Table 1, columns at line 196/198 | severity: **major**

  The brief, deliverable 1: *"Describe each: domain, #nodes, #edges, node-feature type and
  dimension, #classes, **directed/undirected**, and which task it is normally used for."*
  Table 1's columns are Family, |V|, |E|, d, #cls, feat., h_edge — directedness is absent,
  and it is not stated per-dataset anywhere else in the answer.

  The worker already computed it: `stats.py` prints an `und` column, and
  `verified_numbers.md` carries an `undirected` yes/no for every row. It was measured and
  then dropped from the deliverable. It is not cosmetic here — WebKB/Actor/Chameleon/Squirrel
  are natively **directed** and Planetoid/Coauthor/Amazon are **undirected**, which is
  precisely why the |E| convention differs between the two halves of the table (see 1.1).

  **To fix:** add the column (the data is in `verified_numbers.md`).

- **[1.3] Table 1 caption misdescribes the |E| convention.** | `answer.tex` lines 190–192 |
  severity: minor

  Caption: *"|E| counts distinct undirected edges."* For the six directed benchmarks it is
  distinct undirected edges **plus self-loops** (verified above). The caption should say so,
  or the counts should exclude them. Follows from 1.1 and is fixed by the same edit.

- **[1.4] YouTube attributed to the wrong Tang & Liu paper.** | `answer.tex` line 103 |
  severity: minor

  The sentence covers BlogCatalog, Flickr **and YouTube** under "(Tang & Liu, KDD 2009)".
  The worker's own downloaded `research/deepwalk.txt` shows DeepWalk citing **[39]** for
  BlogCatalog and Flickr but **[40]** for YouTube (line 818: "YouTube [40]") — a different
  Tang & Liu paper (CIKM 2009, *Scalable learning of collective behavior based on sparse
  social dimensions*). The brief required real, checkable references per baseline/benchmark.

  **To fix:** split the citation, or drop YouTube from that parenthetical.

- **[1.5] Actor is given the wrong node type in the schema figure.** |
  `fig_p1_schema_families.pdf`, "Web hyperlink" panel | severity: minor

  The panel types the node as **Web page** with relation **links to**, and lists Actor among
  its members. Actor's nodes are actors and its edges are Wikipedia co-occurrence — which
  `answer.tex` §1.3 (lines 79–81) itself describes correctly. The figure contradicts the
  prose. `fig_p1_subgraphs.pdf` gets this right ("web-page hyperlink / actor co-occurrence").

  **To fix:** either split Actor into its own family or relabel the panel to cover both.

### Noted, not held against the submission

- **Length: 14 compiled pages vs. the brief's "roughly 4–7".** The worker flagged this itself
  and asked for a ruling. I measured page fill with pymupdf: 85%+ text coverage on 12 of 14
  pages, no float-waste pages, no padding or repetition. The brief's own coverage mandate
  (~20 benchmarks each described, ~30 baselines each with a reference and a 2–4 sentence
  description, ~12 metrics with formulas, 3 tables, 3 figures) cannot fit in 4–7 pages, and
  both the brief ("comprehensiveness is the graded axis") and the assignment itself ("as
  comprehensive as you can") resolve the conflict in favour of coverage. **Keep the length.**
  Do not cut content to hit the page number.
- The worker's claim that "the last page is 94.5% full" is wrapper-dependent; under my
  wrapper (11pt, 1in margins) page 14 is a 4-line orphan. Page breaks belong to the master,
  so this is not actionable.
- Seven labels are defined but never referenced (`p1:tab:metrics`, `p1:eq:ap`, `p1:eq:hits`,
  `p1:eq:macrof1`, `p1:eq:microf1`, `p1:eq:mrr`, `p1:eq:ndcg`). Harmless.
- `\usepackage{longtable}` is declared in `preamble.txt` but no longtable is used. Harmless.
- PubMed |E| 44,324 vs 44,327 in Zhu et al. — below the noise floor, not worth a footnote.
- The worker's point that `crosscheck.py`'s "70 != 100" warning is a tool-side wrong
  assumption is correct: the assignment page says "This assignment contains 70 points".

### Resolved since last round
(none — first round)

### Still outstanding
[1.1], [1.2], [1.3], [1.4], [1.5]

---

## Round 2
Verdict: FAIL

### Resolved since last round

- **[1.2] RESOLVED — directed/undirected column.** Table 1 now carries a `dir.` column (U/D).
  I checked every row against `stats.py`'s `und` output: Planetoid/Coauthor/Amazon/Social/PPI
  = U, WebKB/Actor/Chameleon/Squirrel = D. All correct. The worker went further than asked
  and added the parenthesised stored-edge-list count to the six D rows; I verified all six
  independently from the raw files (Cornell 298, Texas 325, Wisconsin 515, Actor 30,019,
  Chameleon 36,101, Squirrel 217,073) — exact matches.
- **[1.3] PARTIALLY RESOLVED.** The `|E|` half of the caption is now correct: it says
  "distinct unordered pairs, with self-loops counted once", which is exactly what I measured
  (Cornell 277+3=280 etc.). But the caption's new claim about `h_edge` is false — see [2.1].
- **[1.4] RESOLVED — YouTube citation.** `answer.tex` lines 123–125 now split the two:
  BlogCatalog/Flickr → Tang & Liu, *Relational Learning via Latent Social Dimensions*,
  KDD 2009 (DeepWalk ref [39]); YouTube → Tang & Liu, *Scalable Learning of Collective
  Behavior based on Sparse Social Dimensions*, CIKM 2009 (ref [40]). Matches
  `research/deepwalk.txt` line 818.
- **[1.5] RESOLVED — Actor mis-typed in the schema figure.** Re-rendered and looked at
  `fig_p1_schema_families.pdf`: Actor now has its own **Co-occurrence** family
  (Actor —co-occurs with→ Actor); **Web hyperlink** is Cornell/Texas/Wisconsin/Chameleon/
  Squirrel only. Seven families in a 4+3 layout, all legible, no clipping. Both "six" →
  "seven" updates made (lines 304, 312). I checked the four other occurrences of "six" in
  the text (lines 83, 111, 137) — all refer to correct, different things.
- **[1.6 / submission] RESOLVED — false cross-check claim removed** and replaced with a
  per-dataset comparison in `verified_numbers.md`, including the Cornell non-reproduction.
- **Self-caught regression, credited.** The worker found and fixed a stale
  $h_{\mathrm{edge}}=0.06$ for Texas baked into `fig_p1_subgraphs.pdf`. I confirmed it now
  reads 0.11, consistent with Table 1 and the prose. Catching a figure/table contradiction
  that I had not flagged is exactly the right instinct.
- **[1.1] Cornell handling — RESOLVED, and verified harder than claimed.** The answer reports
  its measured 0.13, daggers it, and footnotes that 0.30 could not be reproduced. I did not
  take this on trust: I ran `cornell_probe.py` (reproduces the footnote's four values
  exactly: 0.131 / 0.122 / 0.186 / 0.132) and then swept **ten** definitions of my own from
  the raw files (`rerun/cornell_sweep.py`) — edge homophily over directed entries and over
  unordered pairs, each with and without self-loops; node homophily out-neighbour and
  symmetrised, each over nonzero-degree and over all N; class homophily (Lim et al. 2021);
  adjusted homophily (Platonov et al. 2023). Cornell's highest value under any of them is
  **0.186**. Nothing approaches 0.30. The answer's claim is honest and now independently
  corroborated. Reporting the measured value with the disagreement flagged is the right call.

### Defects

- **[2.1] `h_edge` is computed over a different edge set than the one the caption, the
  footnote and `verified_numbers.md` all say it uses.** | `homophily.py` lines 30–35;
  `answer.tex` table caption and footnote `p1:fn:cornell`; `verified_numbers.md` line 61 |
  severity: **major**

  This is the unfixed half of round-1 [1.1]. The self-loop half is genuinely fixed; the
  edge-set half is not.

  `edge_homophily()` computes `h` over `data.edge_index` — the **stored directed entries**.
  For the six D rows that set has 298 / 325 / 515 / 30,019 / 36,101 / 217,073 members
  (confirmed by `homophily_out.json`'s own `n_entries` field). But Table 1's `|E|` column is
  **distinct unordered pairs**: 280 / 295 / 466 / 26,752 / 31,421 / 198,493. Different
  denominators.

  Yet the caption states `h_edge` is "computed over the \emph{same} self-loop-inclusive edge
  set as $|E|$", the footnote repeats "which is also the convention used for the $|E|$
  column, so the two columns are consistent", and `verified_numbers.md` line 61 says the
  same. For the seven U rows the claim is harmless (a symmetric edge list gives an identical
  ratio); for the six D rows — precisely the rows this distinction was raised about — it is
  false. The footnote even lists "over distinct unordered pairs $0.132$" for Cornell as a
  *separate* definition from the $0.131$ it reports, so the two halves of the same footnote
  contradict each other.

  **This is not merely cosmetic: the stated convention is the more accurate one.** I computed
  both against Zhu et al. (`rerun/indep_homophily2.py`), summed absolute deviation over the
  five reproducible heterophilous datasets:

      unordered pairs + self-loops (what the caption says):  0.0102
      stored directed entries + self-loops (what it does):   0.0264

  At the table's 2-decimal display precision two cells are affected, and both currently
  disagree with the published values while the stated convention would match them exactly:

      Wisconsin   printed 0.20   stated convention 0.2060 -> 0.21   published 0.21
      Chameleon   printed 0.24   stated convention 0.2312 -> 0.23   published 0.23

  This also fully explains the worker's own open item ("Wisconsin is 0.196 vs a published
  0.21 ... I have not chased down the residual", submission lines 241–242). The residual is
  the edge set. Note the worker's own `cornell_probe.py` already prints the right quantity —
  `h_edge_undirected`, which gives Wisconsin 0.206 and Texas 0.112 — so the evidence was in
  its own output.

  **To fix — either is acceptable, (a) preferred:**
  (a) Compute `h` over the deduplicated unordered-pair set plus self-loops (the quantity
      `cornell_probe.py` already calls `h_edge_undirected`). Update Wisconsin 0.20 → 0.21
      and Chameleon 0.24 → 0.23, and the footnote's "Wisconsin $0.17$ rather than $0.20$"
      → "rather than $0.21$". Cornell becomes 0.132 → still 0.13, dagger unchanged. This
      makes the caption true *and* improves literature agreement.
  (b) Keep the directed-entry computation and instead correct the three places that claim
      it matches `|E|`, stating plainly that `h` is computed over the stored edge list
      (the parenthesised figure) rather than over `|E|`.

- **[2.2] Stale header line in `verified_numbers.md`.** | `verified_numbers.md` lines 8–9 |
  severity: minor

  The header still reads "`E_und` = distinct unordered pairs (self-loops **excluded** from
  the homophily count)", which is the round-1 convention and now contradicts the corrected
  section below it (lines 33+) and the `h_edge (incl. loops)` column in the same table.
  Playground documentation only, not the deliverable, but it is the audit trail.

### Re-verified this round (still clean)

- `lint_output.py` exit 0. OUTPUT contains only `answer.tex`, three `fig_p1_*.pdf`,
  `preamble.txt`.
- Fragment compiles in a minimal wrapper: exit 0 both passes, 14 pages, **zero** undefined
  or multiply-defined references, two overfull hboxes of 4.9pt and 5.2pt (both under the
  8pt bar). No `\documentclass` / `\usepackage` / `document` environment.
- All **14** labels namespaced `p1:` (new `p1:fn:cornell` included). Figures still
  referenced by bare filename.
- `fig_p1_schema_families.pdf` grew to 478pt native and is now included at `\textwidth`;
  at 6.5in textwidth that is a 0.98 scale factor, so fonts remain ~1:1 and legible. Checked
  by rendering, not by assumption.
- Every Table 1 `h_edge` cell matches `homophily_out.json`'s `h_incl_selfloops` to the
  printed precision — internally consistent with the (wrong-edge-set) computation.
- Statistics, OGB figures, DeepWalk/node2vec figures and the 36 citations were verified in
  round 1 and are unchanged; spot-checked that Table 1/Table 2 bodies did not drift.
- `downloads.md` unchanged and still complete (`cornell_probe.py` needs no new downloads).
- Length: 14 pages, unchanged, as I ruled last round. Figure relayout removed a sparse float
  page. Correct — do not cut content.

### Still outstanding
[2.1] blocking, [2.2] minor

---

## Round 3
Verdict: PASS

### Resolved since last round

- **[2.1] RESOLVED — `h_edge` now computed over the edge set the caption claims.** The worker
  took resolution (a). `homophily.py:edge_homophily()` now canonicalises each edge to
  `(min,max)`, deduplicates via `torch.unique`, and computes over that set with self-loops
  counted once.

  I re-ran it and compared against the independent raw-file values I computed in round 2
  (`rerun/indep_homophily2.py`, no PyG, no worker code). Exact agreement on all six directed
  graphs: Cornell 0.132, Texas 0.112, Wisconsin 0.206, Actor 0.219, Chameleon 0.231,
  Squirrel 0.223. The denominators are now 280 / 295 / 466 / 26,752 / 31,421 / 198,493 —
  identical to the `|E|` column.

  The two affected cells moved onto the published values as predicted:
  **Wisconsin 0.20 → 0.21**, **Chameleon 0.24 → 0.23**. Eight of the nine datasets Zhu et al.
  publish now agree *exactly* at two decimal places; Cornell remains the documented
  exception. The seven U rows are unchanged, as expected for symmetric loop-free graphs.

  The three false claims are corrected. The caption now reads "its denominator being exactly
  the $|E|$ of the preceding column — the same distinct unordered pairs, self-loops
  included", which I verified is true 13/13. The footnote was restructured to separate the
  two independent choices (which edge set; whether self-loops count), so it no longer lists
  the unordered-pair figure as an alternative to itself; it now correctly names the
  directed-entry count as the alternative (Chameleon 0.235 vs 0.231 — matches my
  computation) and notes it agrees less well with the literature. Every number in the
  rewritten footnote checks out against my round-2 ten-definition sweep: Cornell 0.132 /
  0.123 / 0.131 / 0.186, self-loop counts 16/16/93/140, and the excl-self-loop values
  correctly updated to Texas 0.06 and Wisconsin 0.18.

- **The worker's own "unchased Wisconsin residual"** (round-2 low-confidence item #2) is
  closed, and it was this bug rather than noise, as diagnosed.

### Verified this round

- **Both claimed machine checks are true.** The submission asserts two new checks with
  specific pass counts. No script implementing them exists (see [3.1]), so I wrote my own
  (`rerun/verify_claims.py`) and confirmed the results independently:
  - homophily denominator vs `stats_out.json`'s `E_und`: **13/13 identical**, as claimed.
  - every Table 1 `h_edge` cell re-parsed out of `answer.tex` vs `homophily_out.json`
    rounded to 2 d.p.: **13/13**; plus the two values baked into the subgraphs figure
    source (Cora 0.81, Texas 0.11): **2/2**. Total **15/15**, as claimed.
- Table 1 re-read in full: every `|V|`, `|E|`, stored-entry count, `d`, `#cls`, `feat.` and
  `dir.` value is unchanged from the values I verified against `stats.py` in rounds 1–2. No
  drift.
- Compiles in a minimal wrapper: exit 0 both passes, **13 pages**, zero undefined or
  multiply-defined references, two overfull hboxes (4.9pt, 5.2pt, both under the 8pt bar),
  zero underfull.
- Page density 82–86% on all 13 pages; the round-2 four-line orphan page is gone. No content
  was removed — the reduction is footnote/float reflow, as claimed.
- `lint_output.py` exit 0. No `\documentclass` / `\usepackage` / `document`. All 14 labels
  namespaced `p1:`. Figures referenced by bare filename.
- Figure PDFs unchanged since round 2 (verified by mtime and re-render); already checked
  legible, unclipped, correctly scaled.

### Defects (all minor — noted, not blocking)

- **[3.1] The two "machine checks" were not saved as scripts.** | `submission.md` lines
  45–52; the code table lists no such file | severity: minor

  Every other entry in the "Intermediate steps and code" table names a file and a reproduce
  command; these two name neither, and no script in the playground reads `stats_out.json`
  alongside `homophily_out.json` or parses `answer.tex`. The checks were evidently performed
  — I independently reproduced both results exactly, which would not happen by chance across
  15 values — but they are not reproducible artifacts. Given the worker's own stated reason
  for adding them ("because I had already asserted this consistency once when it was
  false"), a saved script is the point. Recommend saving it as e.g. `consistency_check.py`
  and listing it in the code table.

- **[3.2] `verified_numbers.md` line 8 is still stale.** | `verified_numbers.md` line 8 |
  severity: minor — *carried over from [2.2], not fixed*

  Still reads "`E_und` = distinct unordered pairs (self-loops **excluded** from the homophily
  count)". Self-loops are now *included*, and the clarifying line the worker added five lines
  below ("`h_edge` columns are over distinct unordered pairs (denominator = `E_und`)")
  directly contradicts it. Playground audit trail only, not the deliverable.

- **[3.3] Code table page count stale.** | `submission.md` code table, `master_test.tex` row |
  severity: minor. Says "→ 14 pages, exit 0"; it is now 13.

### Why this passes

Both major defects from rounds 1 and 2 are genuinely fixed, and fixed in the direction that
*improves* agreement with the published literature rather than merely silencing the
objection. I re-derived the corrected numbers independently rather than accepting the
worker's, and they match exactly. The deliverable — `answer.tex`, three figures,
`preamble.txt` — is correct, complete against every element the brief enumerated, compiles
clean, lints clean, and is fully namespaced.

The three remaining items are documentation hygiene inside the playground. None touches the
graded artifact, and none represents a wrong or unsupported number. Per my own standard,
remaining objections that are all cosmetic warrant a pass with notes.

### Still outstanding
[3.1], [3.2], [3.3] — all minor, none blocking.
