# p1 — working notes

## Channel reconciliation (R7)
- `page_002.txt` (text): full Problem 1 statement present, matches brief verbatim.
- `page_002.png` (render): visually identical content; "Cora" appears as a blue hyperlink;
  underlines on "homogeneous graph structures" and "the task of node classification and link
  prediction". Only image on page = ND monogram in header.
- figure files: none. `manifest.json` lists `figures: []` for all 3 pages (n_images:1 is the
  header monogram). So there is no figure to transcribe — the "draw" instruction means *I* must
  produce the schema diagrams.
- No disagreement between brief and page. Page 3 = Problem 2 (heterogeneous) -> confirms my
  scope is strictly homogeneous.

## What this problem needs
- **plain**: yes, dominant. A survey write-up (benchmarks / baselines / metrics).
- **diagram**: yes, explicitly graded ("draw the related graph schema"). TikZ schema diagrams,
  one per schema family, plus illustrative subgraph sketches.
- **code**: NOT for a computed result — there is no quantity to compute. BUT every dataset
  statistic I quote is a factual claim that must be *verified against an authoritative source*,
  not recalled. Plan: pull numbers from OGB's official site + PyG dataset cheatsheet + original
  papers, and record the source for each row.

## Plan
1. Verify benchmark statistics (nodes/edges/features/classes) from primary sources.
2. Verify every baseline citation (authors, title, venue, year) — no invented references.
3. Build TikZ schema figures; render and look at them.
4. Write answer.tex (fragment, everything namespaced `p1`), preamble.txt.
5. lint_output.py, then submission.md.

## Number-discipline rule for this problem
Any statistic that I cannot tie to a source gets dropped or footnoted as varying. Where sources
genuinely disagree (Cora edges: 5429 vs 5278 vs 10556), footnote the discrepancy rather than
silently picking one.

## Outcome log

- All small/medium benchmark statistics **computed** by loading the graphs via PyG
  (`stats.py`, `stats_reddit.py`); homophily ratios computed by `homophily.py`.
  Results consolidated in `verified_numbers.md`.
- OGB statistics taken from the official OGB docs (too large to download); saved in
  `research/ogb_*.txt`.
- BlogCatalog / Flickr / YouTube / node2vec-PPI statistics taken from the original
  DeepWalk and node2vec PDFs (`research/deepwalk.txt`, `research/node2vec.txt`).
- Citations independently audited by a sub-agent against Crossref/arXiv/PMLR. It found
  **6 real errors** in my draft, all fixed: struc2vec author is Sav\*a\*rese not Saverese;
  APPNP author is now Gasteiger (not Klicpera); GraphSAGE is NIPS 2017 not NeurIPS 2017
  (rename happened in 2018); Laplacian Eigenmaps NIPS-2001 and NeurComp-2003 are two
  papers with *different titles*, not a reprint; Page/Brin TR is a weak cite for
  *Personalized* PageRank -> added Jeh & Widom WWW 2003.
- Two non-obvious invariant checks passed:
  - Reddit: 2 x 57,307,946 / 232,965 = 492.0, exactly the average degree the GraphSAGE
    paper states. Confirms 57.3M (not the 11.6M some pages quote) for this copy.
  - Cora: PyG's 10,556 directed entries = 2 x 5,278, reconciling the 5,429/5,278/10,556
    spread as one graph counted three ways.
- Discovered and documented a genuine trap: **BlogCatalog, Flickr and PPI each name two
  different graphs** in this literature, with wildly different statistics.

## Length
Compiles to 14 dense pages (11pt, 1in margins), vs. the brief's "4-7 page" target. Every
page is >90% full; the last page is 94.5% full, so there is no padding or float waste.
The gap is between the brief's *page* target and the brief's own *coverage* mandate
(~20 benchmarks described, ~30 baselines with references, ~12 metrics with formulas,
3 tables, 3 figures). I compressed by removing statistics from prose where they already
appear in the tables (which is also what the brief asks for) and cutting the meta-commentary
and summary; cutting further would mean dropping mandated content. Flagged for the validator.

## LaTeX trap found
The default `itemize` bullet is a TS1 glyph; TinyTeX ships `tcrm1095.tfm` but no matching
Type1 file, so any fragment using a plain `\item` bullet **kills the master compile** with
"Font tcrm1095 at 600 not found". Fixed self-containedly with `label=$\bullet$` on every
list rather than by forcing `lmodern`/`fontenc` on the master document.
