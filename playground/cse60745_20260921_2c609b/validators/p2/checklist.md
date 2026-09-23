# Validator checklist — p2

## Round 1
Verdict: FAIL

### What I verified independently (so the worker does not redo it)

- **R7, all three channels.** Read `page_003.txt`, `page_003.png`, and both `manifest.json`
  files. `figures: []` on all 3 pages; the single `n_images: 1` per page is the ND monogram.
  **Brief and assignment page agree verbatim.** No figure to transcribe. Worker's reading is right.
- **Compile.** Built `answer.tex` in my own minimal wrapper with only the 8 packages from
  `preamble.txt` + geometry. 12 pages, exit 0, **zero errors, zero undefined/multiply-defined
  refs**, one 3.63pt overfull hbox (lines 519–526). Matches the worker's claim exactly.
- **Lint.** `lint_output.py` exits 0. OUTPUT holds only `answer.tex` + `preamble.txt`.
- **R5 / namespacing.** No `\documentclass`/`\usepackage`/`document`. All 8 labels `p2:`-prefixed,
  all 4 macros `\pTwo*`, all 4 TikZ styles `p2*`. No `\includegraphics`, no absolute paths. Clean.
- **Visual inspection.** Rendered all 12 pages at 130 dpi and read them, plus 4x LANCZOS crops of
  the ACM schema, the Yelp schema, Table 2 and Table 3. All schemas legible, no label collisions,
  no clipped table text, nothing past the right margin, no near-empty page. The session-2 layout
  fixes are real and held.
- **`verify_hgb.py` is a genuine derivation**, not hardcoded output — I read it; it parses
  `node.dat`/`link.dat`/`label.dat` and counts. Its `PUBLISHED` dict is transcribed from the paper
  and used only as the comparison target.
- **Freebase edge breakdown — the one check `check_invariants.py` declined to do.** I summed all
  36 relation counts from `hgb_verify_output.txt`: **1,057,688 exactly**, and 36 link types, and
  node types sum to 180,098. Worker's stated weakness #5 is **resolved**; it need not worry about it.
- **HGB published totals** independently confirmed against arXiv:2112.14936 Table 2 (all 7 rows,
  incl. Amazon 10,099/1/148,659/2, LastFM 20,612/3/141,521/3, PubMed 63,109/4/244,986/10,
  Freebase 180,098/8/1,057,688/36, book, 7 classes), plus the 2-hop 1:1 negative sampling and the
  ROC-AUC/MRR LP metrics.
- **All 29 baseline citations checked against primary sources.** Nothing fabricated. The four the
  worker flagged as least certain all hold: GAT = ICLR **2018** (arXiv Oct 2017); HERec = TKDE
  **31(2):357–370, 2019**; ESim = arXiv:1610.09769, **never published in a venue** (shichuan.org
  mislabels the PDF "2017. KDD ESim" — a third-party error, the worker is right); HDGI =
  arXiv:1911.08538, AAAI-20 DLGMA workshop **under a different title**, non-archival. Also verified
  ie-HGCN TKDE 35(2):1637–1650 2023, HPN TKDE 35(1):521–532 2023, RSHN ICDM 2019.
- **All Section 2.3 version claims verified against the source PDFs**, including the subtle one:
  HAN's Table 2 really does print 14,328 papers in the Paper-Author/Paper-Conf rows and **14,327**
  in the Paper-Term row. Also confirmed HAN DBLP term 8,789 / P–T 88,420; HAN ACM 3,025/5,835/56,
  P–A 9,744; HeCo ACM 4,019/7,167/60, P–A 13,407; HeCo Freebase = a *movie* graph 3,492/33,401/
  2,502/4,459; HeCo AMiner 6,564/13,329/35,890; MAGNN IMDb 4,278/2,081/5,257 single-label 3-class;
  GTN DBLP 18,405 nodes with term dropped, 4 edge types; metapath2vec's footnote-2 erratum
  ("The count 9,323,739 is the paper-author link count", authors = 1,693,531).
- **Coverage vs. the brief.** All 6 required schemas drawn (+Freebase = 7). All 29 required
  baselines present with references. All required metrics with formulas. The Micro/Macro-F1, MRR
  and Hits@K definitions match the Problem-1 consistency constraint exactly.

This is well-sourced work. The defect list is short because the sourcing held up, not because I
did not look.

### Defects

- [1.1] **The Freebase network schema (Figure 3) draws 8 of the 36 relation types, and its caption
  misrepresents the omission.** | `OUTPUT/answer.tex` lines 432–457 (the `p2:fig:schemasc` figure,
  its sub-label line 451 and caption lines 453–455) | severity: **major**

  From `hgb_info/Freebase.info.dat` (which is in the playground and still checkable), the 36 link
  types are all *distinct forward* relations — there are **no inverse pairs** (e.g. `BOOK-to-FILM`
  exists, `FILM-to-BOOK` does not). Exactly **8** of them are incident to BOOK; the other **28**
  connect non-BOOK type pairs (`FILM-and-FILM`, `MUSIC-and-MUSIC`, `MUSIC-in-FILM`,
  `PEOPLE-on-LOCATION`, `LOCATION-and-LOCATION`, `ORGANIZATION-for-BUSINESS`, …). The drawn star
  shows only the 8. Three things make this misleading rather than a fair simplification:

  1. The caption ends "Conventions as in Figure~\ref{p2:fig:schemas}", and Figure 1's stated
     convention is "**Inverse relations are omitted** throughout" — so the only omission the
     reader is told about is inverses, when in fact 28 non-inverse relations are missing.
  2. Section 1 (lines 42–45) has already trained the reader to read an inflated edge-type count as
     forward+inverse: "which is why the released benchmarks below count 6 or 8 'edge types' where
     a reader might expect 3 or 4". So "36 relations in total" reads as ~18 forward + 18 inverse.
     It is not; all 36 are forward.
  3. The answer's own Table 2 (line 146–147) quotes **`MUSIC-and-MUSIC` 283,670** — the single
     largest relation in the dataset, 27% of all its edges — as one of two exemplars. That
     relation is nowhere in the figure the reader is pointed to. Table and figure contradict.

  The factual claim "BOOK is adjacent to all 7 other types" is **correct** (I checked: via
  BOOK-to-FILM, BOOK-on-SPORTS, BOOK-on-LOCATION, BOOK-about-ORGANIZATION, MUSIC-in-BOOK,
  PEOPLE-to-BOOK, BUSINESS-about-BOOK, plus the BOOK-and-BOOK self-loop). The problem is only the
  completeness of the drawing and what the caption says about it.

  Cheapest correct fix: keep the star, and say what it is. Replace the "Conventions as in
  Figure 1" sentence with something like — *"Only the 8 relations incident to BOOK are drawn;
  Freebase's schema is not in fact a star, as a further 28 relation types connect the other seven
  types to each other (the largest single relation in the dataset is MUSIC–MUSIC, 283,670 edges).
  Unlike DBLP/ACM/IMDB, none of Freebase's 36 relation types are inverses — all 36 are distinct
  forward relations."* That last sentence is worth marks on its own, since it is exactly the kind
  of version/preprocessing nuance the rest of Section 2.3 is built on. Drawing the full 8-type
  relation graph instead is also acceptable but is not required.

- [1.2] **Amazon is listed in two tables but never described.** | `OUTPUT/answer.tex` — appears
  only as a row in Table~\ref{p2:tab:hgb} (line 102) and Table~\ref{p2:tab:summary} (line 724);
  there is no `\paragraph` for it in Section 2.2, unlike every other benchmark | severity: minor

  The brief asked for Amazon under "at minimum cover", and for each benchmark to state domain,
  node/edge types and counts, labels and task. Two or three sentences would close it. Worth
  noting: HGB's Amazon has **1 node type and 2 edge types** (co-viewed / co-bought), which makes
  it the one benchmark in the whole answer that is heterogeneous in $\mathcal{R}$ only — it
  satisfies the answer's own $|\mathcal{A}|+|\mathcal{R}|>2$ as $1+2=3$. Connecting the definition
  in Section 1 to this edge case would turn a gap into a point. MovieLens/ML-100K is similarly
  thin (one clause, line 213, no statistics), though it is a less standard benchmark.

- [1.3] **R3 deviation: the 389 MB HGB download landed in `/tmp/hgbdata`, outside PLAYGROUND.** |
  `PLAYGROUND/downloads.md` | severity: minor

  Recorded honestly and at length rather than hidden, and the directory has since been cleaned up,
  so there is nothing left to remove. Noting it only so the record is complete; **no action
  needed** and I am not asking for anything here.

- [1.4] **Length overruns the brief's target.** 12 compiled pages against the brief's "roughly 4–7
  compiled pages". | whole document | severity: minor

  I checked for padding and did not find it — every benchmark listed is described, every baseline
  has a real verified reference, and the tables are dense rather than airy. So this is a
  note, not a demand to cut. If the master's assembled document has a page budget, the
  compressible material is Section 4's per-baseline descriptions (currently 2–4 sentences each).
  **Do not cut coverage to hit a page count** — comprehensiveness is the graded axis here.

### Resolved since last round
(first round — nothing to resolve)

### Still outstanding
- [1.1] Freebase schema completeness / caption — **the only one that must be fixed.**
- [1.2] Amazon description — should be fixed, cheap.
- [1.3] informational only, no action.
- [1.4] informational only, no action.

---

## Round 2
Verdict: PASS

### What changed, and what I did about it

Diffed the delivered `answer.tex` against my round-1 copy. Exactly five regions changed: the
Freebase paragraph, a new Amazon paragraph, the Section 3 lead-in, the merge of Figures 1+2 into
one float, and the redrawn Freebase figure. Nothing else moved, so I did **not** re-verify the 29
citations or the Section 2.3 version claims — those were verified against primary sources in round
1 and are byte-identical.

### Verification performed this round

- **[1.1] re-derived independently, from scratch.** I parsed `hgb_info/Freebase.info.dat` myself
  rather than trusting the worker's script, and computed: 36 link types; 8 self-relations, one per
  type; 28 cross-type relations spanning 28 *distinct* unordered pairs; `C(8,2)=28` with
  **zero missing pairs and zero duplicated pairs**; and **zero ordered pairs appearing in both
  directions**, i.e. no inverses anywhere. So the schema is exactly $K_8$ plus a loop at every
  vertex, $28+8=36$. **The worker's claim is correct, and it is strictly stronger than the defect
  I raised.** I said the star was an under-drawing; the truth is it was the wrong shape. Withdrawn
  and superseded — the answer now states something I had not established.
- **The redrawn figure is right and legible.** Rendered page 8 and read it: 8 typed circles in an
  octagon, all 28 chords present as light background lines, and — the part most likely to have
  silently failed — **all 8 self-loops render**, one radially outward from each type. BOOK shaded
  as the target. Caption arithmetic checks: 283,670/1,057,688 = 26.8%, so "27% of the graph" holds.
- **[1.2] Amazon — every new claim verified verbatim against arXiv:2112.14936.** HGB §4.2.2 reads
  "We use the subset preprocessed by GATNE [5], containing **electronics** category products with
  **co-viewing and co-purchasing** links between them" — the worker's wording tracks the source
  almost word for word. GATNE ref [5] = Cen, Zou, Zhang, Yang, Zhou & Tang, KDD'19, pp. 1358–1368:
  correct. Table 4's caption is "Vacant positions ("-") are due to lack of meta-paths on those
  datasets", and MAGNN's Amazon cells are indeed "-", while RGCN / GATNE / Simple-HGN all have
  numbers. **Note the worker attributed the blank to MAGNN only — which is exactly right**; HAN is
  not a row in HGB's LP table at all, so the obvious sloppier version of this sentence would have
  been wrong. It didn't make that error.
- **Compile / compliance re-run on the delivered files.** 13 pages, exit 0, zero errors, zero
  undefined or multiply-defined refs. The removed `p2:fig:schemasb` leaves **no dangling `\ref`**
  (checked every label/ref pair). R5 clean. All 7 labels `p2:`-prefixed. `lint_output.py` exits 0;
  OUTPUT still holds only `answer.tex` + `preamble.txt`.
- **Margin check, all 13 pages, programmatic.** No ink in the left or top margins on any page.
  Bottom-margin ink is the page number only (by design). One page has 6 stray pixels past the right
  edge — the known 3.63pt overfull hbox, ~0.8mm, below visual threshold.
- **`check_invariants.py` re-run.** It now genuinely re-derives the Freebase schema from
  `Freebase.info.dat` and sums all 36 relations to 1,057,688, closing the one gap the worker had
  flagged as unverifiable last round. Its output matches my independent derivation exactly.

### Resolved since last round
- **[1.1] Freebase schema — RESOLVED**, and over-delivered. Figure redrawn complete; caption now
  states the $28+8=36$ decomposition and the no-inverses contrast with DBLP/ACM/IMDB. The
  Section 3 lead-in and Figure 1's caption were narrowed so "inverse relations are omitted" no
  longer over-reaches across figures. The Table-2 / Figure tension I identified (MUSIC–MUSIC quoted
  but undrawable) is gone — that relation is now both drawn and named in the caption.
- **[1.2] Amazon — RESOLVED.** Full description added, sourced not recalled, and used as the edge
  case of the answer's own $|\mathcal{A}|+|\mathcal{R}|>2$ definition.
- **[1.3] R3 deviation — unchanged, still informational.** The `/tmp/hgbdata` download remains
  disclosed in `downloads.md` and the directory is gone. No action.

### Still outstanding
Nothing blocking or substantive. Three cosmetic notes, recorded and **explicitly not requiring
another round**:

- [2.1] **Three consecutive float pages (6–8).** Page 6 carries Table 4 vertically centred with
  ~45% fill; pages 7–8 are the two schema figures. This is ordinary LaTeX float-page behaviour
  given ~1.7 pages of floats with little interleaving text. The worker reports trying four
  arrangements. I agree with its judgement to stop: the fragment is `\input` into the master's
  document, where pagination changes completely, so tuning float placement here is wasted work.
  Margin correctness and legibility — the pagination-*independent* properties — are both verified.
  severity: minor.
- [2.2] **13 pages against the brief's 4–7 target.** I checked for padding in round 1 and found
  none, and I told the worker not to cut coverage; the two fixes I required each added material, so
  this growth is my doing, not the worker's. Flagging for the master only: if there is a page
  budget, Section 4's per-baseline descriptions are the compressible part. severity: minor.
- [2.3] **Per-type counts in Table 2 still rest on `hgb_verify_output.txt`**, since `/tmp/hgbdata`
  is gone and `verify_hgb.py` cannot re-run. I read that script and confirmed it genuinely parses
  the data files; every breakdown reconciles to totals I verified against the published paper; and
  the Freebase schema claims are now independent of it. Residual risk is a systematic error
  inherited from session 1 — low, and the worker discloses it honestly. Not worth a re-download.
  severity: minor.

Passing. The two defects I raised are fixed, the fix to the major one is independently re-derived
and correct, and everything still outstanding is cosmetic or disclosed.
