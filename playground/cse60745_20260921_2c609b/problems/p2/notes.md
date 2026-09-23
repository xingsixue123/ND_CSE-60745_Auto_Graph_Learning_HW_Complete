# p2 — working notes

## Source reconciliation (R7)
Three channels checked on rendered page 3 of `CSE 60745_Fall 2026_HW2-Part(A)`:
- `page_003.txt` — full question text present.
- `page_003.png` — matches the text exactly; "DBLP/ACM" is a blue hyperlink; rest of page blank.
- figure files — `manifest.json` gives `"figures": []` for all 3 pages. The single `n_images: 1`
  per page is the Notre Dame monogram in the running header. **No figure to transcribe.**
Brief and page agree. Only note: the page footer reads "Page 2 of 4" while this is *rendered*
page 3 (cover page offsets the printed numbering). Citing rendered index per env.md.

## What the problem needs
- **plain**: yes, dominant. A survey: benchmarks + baselines + metrics for *heterogeneous* graph
  embedding, for node classification and link prediction.
- **diagram**: yes, explicitly graded — "draw the related graph schema". Network schemas are
  typed multigraph templates, so they carry real content here. TikZ inline (no external PDFs
  needed; keeps OUTPUT clean and schemas are pure line art).
- **code**: NOT a computation problem. No number is *derived* by me. But every dataset statistic
  is a factual claim that must be sourced, not recalled. Treat web verification as the
  equivalent of "running the code": no number goes in that I did not read off a source.

## Risk register
1. **Dataset statistics are the main failure mode.** DBLP/ACM/IMDB have several mutually
   incompatible versions (HAN's, GTN's, MAGNN's, HGB's, HeCo's). Recalling a number from memory
   produces a confidently wrong table. Rule for this problem: *every* count in the stats table
   must be traceable to a fetched source, and the table must say which version it is.
2. **Fabricated citations.** Venue/year must be verified, not recalled.
3. Scope creep into homogeneous graphs (Problem 1's territory).

## Invariant checks to run on the stats table
- node-type counts must sum to the stated |V|; edge-type counts must sum to the stated |E|.
- a benchmark described as multi-label (IMDB/Freebase in HGB) must be flagged as such where
  Micro-F1 is discussed.

## Plan
1. Research pass: verify benchmark stats + baseline citations against primary sources.
2. Cross-check sums; record discrepancies between versions rather than silently picking one.
3. Draw ~7 TikZ schemas, compile, look at the rendered pages.
4. Write answer.tex, compile standalone in playground, inspect, lint OUTPUT.

---

## Session 2 (resume) — visual inspection and copy-out

The first session was killed mid-inspection. Steps 1–3 above were already complete and were
**not** redone. What this session found and fixed, all layout defects, no content changes:

1. **Table 3 (dataset versions) ran 75.4pt past the right margin.** Its column spec was a
   vestigial `llrrrrl` with every data row wrapped in `\multicolumn{4}{l}{...}`. Replaced with
   `@{}llp{0.40\textwidth}l@{}` at `\footnotesize`, so the node-count column wraps.
2. **Table 5 (summary) ran 86.0pt past the right margin** — "MAE, RMSE" was visibly clipped off
   the page. `\footnotesize` + `\tabcolsep=4pt` + `@{}` ends + two cells shortened.
3. **The schema figure overran the bottom of the text block** and the page number was
   overprinted between the Freebase sub-label and the caption. It was one float holding all
   seven schemas. Split into three figures (Fig 1 DBLP/ACM/IMDB/LastFM, Fig 2 ogbn-mag/Yelp,
   Fig 3 Freebase).
4. **ogbn-mag and Yelp were butting into each other** in the 0.54/0.44 two-up row: Yelp's
   "friend" self-loop label sat directly beside ogbn-mag's "Field of study" node, so the two
   schemas read as one connected graph. Both now get a full-width row.
5. **Float packing.** After the split, a `\clearpage` before Section 4 forced the leftover float
   onto a near-empty page (13 pages, two pages under 1% ink). Moved the meta-path table ahead of
   the figures and dropped the `\clearpage`, so Fig 3 sits at the top of page 7 with Section 4
   text below it. Back to 12 pages, no sparse page.
6. **12.3pt overfull line** in the opening HIN paragraph (unbreakable `29(1):17--37` citations)
   — wrapped that paragraph in `sloppypar`.

Residual: one 3.6pt overfull on page 8 (~1.3mm, not visible). Verified programmatically that no
page has ink beyond the 6.5in text block.

### Verification caveat for session 2
`/tmp/hgbdata` (the 389 MB HGB download) **has been cleaned up**, so `verify_hgb.py` can no
longer be re-run. The per-type counts therefore rest on `hgb_verify_output.txt` from session 1.
To keep the claim checkable I added `check_invariants.py`, which re-derives the published Table 1
totals from the Table 2 breakdown as those numbers appear in the delivered answer, and re-checks
the Section 2.3 version arithmetic. It passes. `hgb_info/*.info.dat` still independently
corroborates the *schema* (node types, relation types, class names) though not the counts.

---

## Session 3 — validator round 1 (FAIL), defect [1.1] and [1.2]

### [1.1] Freebase schema — the validator was right, and the true fact is stronger

The old Figure 3 drew Freebase as a **star**: BOOK in the centre, 8 edges out. The validator
showed that 8 of 36 relation types were drawn and that the caption ("Conventions as in Figure 1",
whose convention is "inverse relations are omitted") told the reader the only omission was
inverses. It also noted Table 2 quotes `MUSIC-and-MUSIC` (283,670 edges) as a headline example
of a relation that appeared nowhere in the figure.

Before redrawing I re-derived the structure from `hgb_info/Freebase.info.dat` (the file is plain
tab-delimited text, *not* JSON like DBLP/ACM — that is why the first parse attempt failed). Result
confirms the validator and goes further:

- 36 link types, **zero** inverse pairs — every one is a distinct forward relation.
- 8 incident to BOOK, 28 not. BOOK *is* adjacent to all 7 other types (that claim was fine).
- **The schema is complete.** $\binom{8}{2}=28$ unordered type pairs, each carrying exactly one
  relation, plus one self-relation per type: $28+8=36$. Every pair is present exactly once; none
  is repeated. So Freebase's schema is $K_8$ with a loop at every vertex.

That makes the star drawing not a simplification but simply the wrong shape. Figure redrawn as
the full complete schema (28 chords + 8 self-loops), and the caption now states completeness, the
$28+8=36$ decomposition, and the no-inverses contrast with DBLP/ACM/IMDB — which is the sentence
the validator said was worth marks. `check_invariants.py` now re-derives all of this from the
`.info.dat` file, so the claim is reproducible rather than asserted.

**Two TikZ traps hit while redrawing** (both produced silently-missing self-loops, no error):
1. `\foreach \n/\o/\i` — `\o` and `\i` are LaTeX built-ins (ø and dotless ı). Renamed to
   `\nd/\oa/\ia`.
2. A self-loop drawn between two *coordinates* degenerates; it needs a real node with a shape.
   Fixed by naming the circles `(nB)`…`(nBu)` and looping on those, after they are placed.
Also `out=\a+26` does not evaluate inside `to[...]` — the out/in angles are now explicit numbers.
Labels needed `label distance=9.5mm` to clear the loops.

### [1.2] Amazon — described, and used to make a point
Added a paragraph. Verified against the HGB PDF (arXiv:2112.14936) rather than from memory: 1 node
type (product, 10,099), 2 relation types, 148,659 edges, and the paper's own wording is
"**co-viewing and co-purchasing**", on "the subset preprocessed by GATNE". So it satisfies
$|\mathcal{A}|+|\mathcal{R}|=1+2=3>2$ with a single node type — the edge case that justifies
stating the definition as a sum. Also found direct support for the meta-path point: HGB's Table 4
note says vacant entries are "due to lack of meta-paths on those datasets", and MAGNN's Amazon
entry is blank. Cited that rather than making an unverified leaderboard claim.

### Not actioned
[1.3] and [1.4] were explicitly informational. On [1.4] (length): the validator checked for padding
and found none, and said not to cut coverage. The answer grew to 13 pages because the Freebase fix
enlarged a figure and Amazon added a paragraph — both were the requested fixes.

### Float packing — deliberately left alone
Section 3 carries ~1.7 pages of floats with almost no interleaving text, so LaTeX emits float
pages. I tried four arrangements (table before/after the figures, one/two/three figures) and every
one produced three float pages; the ink differences were noise. Since pagination in the assembled
master document will differ anyway, I merged the six small schemas into one well-filled figure and
stopped there rather than churning further. Margin correctness and legibility are
pagination-independent and both verified.
