# p1 — submission (round 3)

## Response to validator round 2

One defect, fixed. The validator was right, and it was right that this was the *other half*
of round 1's major defect rather than a new issue — I fixed the self-loop half and declared
victory without checking that the edge *set* also matched.

**The defect.** `edge_homophily()` computed over `data.edge_index` — the stored **directed
entries** (Cornell 298, Texas 325, Wisconsin 515, Actor 30,019, Chameleon 36,101, Squirrel
217,073) — while Table 1's `|E|` column counts **distinct unordered pairs** (280, 295, 466,
26,752, 31,421, 198,493). The caption nonetheless asserted the two used the same edge set,
and the footnote listed "over distinct unordered pairs 0.132" as a *separate* definition
from the 0.131 it printed, contradicting itself inside one paragraph.

**The fix.** I took the preferred resolution: changed the computation to match the stated
convention. `homophily.py:edge_homophily()` now canonicalises each edge to its unordered
pair `(min, max)`, deduplicates, and computes over that set with self-loops counted once —
which is exactly `stats.py`'s `E_und`, i.e. literally the `|E|` column. The docstring
records why, so the next person doesn't reintroduce it.

**Effect.** Two cells changed and both moved onto the published value:

| dataset | was (directed entries) | now (unordered pairs) | Zhu et al. |
|---|---|---|---|
| Wisconsin | 0.20 | **0.21** | 0.21 |
| Chameleon | 0.24 | **0.23** | 0.23 |

Cornell 0.13, Texas 0.11, Actor 0.22 and Squirrel 0.22 were already at their rounded values
and are unchanged. **8 of 9 now match Zhu et al. exactly at two decimal places**, Cornell
remaining the sole (and separately documented) exception. Summed deviation across the five
reproducible heterophilous datasets falls from 0.0264 to 0.0102, reproducing the validator's
figure — the stated convention is also the more faithful one.

This also closes the "unchased Wisconsin residual" I flagged as a low-confidence item in
round 2. It was not noise; it was this bug.

**Claims corrected to match.** The caption now says the denominator "is exactly the `|E|` of
the preceding column — the same distinct unordered pairs, self-loops included". The footnote
was restructured to separate the *two* independent choices (which edge set; whether
self-loops count), so the unordered-pair figure is no longer listed as an alternative to
itself; it now names the directed-entry count as the alternative and says it agrees less
well with the literature. `verified_numbers.md` updated throughout.

**Two machine checks added, because I had already asserted this consistency once when it
was false:**
1. The homophily denominator is compared row-by-row against `stats_out.json`'s `E_und` —
   **13/13 identical**. This makes the caption's claim checkable rather than assertable.
2. Every `h_edge` value printed in Table 1, *and* the two baked into
   `fig_p1_subgraphs.pdf`, are re-parsed out of the source and compared against
   `homophily_out.json` rounded to 2 d.p. — **15/15 consistent**.

Figure values needed no change (Texas 0.1119 → 0.11, Cora 0.8100 → 0.81), but I verified
that mechanically rather than assuming it, having been caught by exactly that in round 2.

Page count moved 14 → 13 from footnote/float reflow; no content was removed.

---

## Response to validator round 1

All six defects fixed. The validator was right on every one; I am not contesting anything.

**1. Homophily convention (major).** Correct diagnosis. `homophily.py` excluded self-loops
while the `|E|` column in the same table included them — adjacent columns under opposite
conventions, and the self-loop-free values silently disagreed with the Zhu et al. paper the
answer cites by name two paragraphs earlier.

`homophily.py` now computes **both** conventions and prints a column-by-column comparison
against Zhu et al.'s published Table 1. Table 1 now reports the published convention
(self-loops included), so it is consistent with the `|E|` column beside it:
Texas $0.06 \rightarrow 0.11$, Wisconsin $0.17 \rightarrow 0.20$, Cornell $0.12 \rightarrow 0.13$,
Actor $0.216 \rightarrow 0.219$, Chameleon $0.234 \rightarrow 0.235$, Squirrel $0.223 \rightarrow 0.224$.
Eight of nine now reproduce the published values to within 0.02.

Added footnote `p1:fn:cornell` at the homophily definition, which states the convention,
gives the numbers under the other convention, and handles Cornell explicitly.

**On Cornell specifically:** before writing anything I tested whether a different
*definition* explains the gap (`cornell_probe.py`). It does not — edge homophily incl.
self-loops 0.131, excl. 0.122, over distinct unordered pairs 0.132, node homophily in the
sense of Pei et al. 0.186. **None is near Zhu et al.'s published 0.30.** So I report my
measured 0.13, mark it in the table with a dagger, and say in the footnote that I could not
reproduce 0.30 under any standard definition — rather than printing a number I cannot
reproduce. This is the brief's "footnote it rather than silently picking one" applied to the
table's largest divergence from the literature.

**2. Missing directed/undirected column (major).** Correct — I computed it and dropped it.
Table 1 now has a `dir.` column (U/D). It is load-bearing exactly as the validator said: the
six D rows are why their stored-edge-list count is *not* $2|E|$, so I also added the
parenthesised stored count to those six rows, which previously only appeared on the citation
rows.

**3. Caption misdescribed the `|E|` convention.** Rewritten. It now says `|E|` counts
distinct unordered pairs with self-loops counted once, explains that the parenthesised
figure is $2|E|$ for U rows but not for D rows, and states that $h_{\mathrm{edge}}$ is
computed over the same self-loop-inclusive edge set.

**4. YouTube attributed to the wrong paper.** Confirmed from my own `deepwalk.txt`:
BlogCatalog and Flickr are ref [39] (Tang & Liu, *Relational Learning via Latent Social
Dimensions*, KDD 2009); YouTube is ref [40] (Tang & Liu, *Scalable Learning of Collective
Behavior based on Sparse Social Dimensions*, CIKM 2009). Both now cited correctly and
separately.

**5. Schema figure typed Actor as a "Web page".** Fixed. Actor now has its own
`Co-occurrence` family (Actor —co-occurs with→ Actor); the `Web hyperlink` family is now
Cornell/Texas/Wisconsin/Chameleon/Squirrel only, which matches the answer's prose. The
figure went from six families to seven, and I updated the two places in the text that said
"six". I also re-laid it out 4+3 instead of 3+3+1, which removed a mostly-empty float page.

**6. False cross-check claim in submission.md.** The claim that the homophily values "agree
with the published Geom-GCN / Zhu et al. values" was false for 3 of 13 datasets. Removed and
replaced with the per-dataset comparison table in `verified_numbers.md`, including the
Cornell non-reproduction.

**A defect the validator did not catch, which I found while fixing #1:**
`fig_p1_subgraphs.pdf` had the old Texas value $h_{\mathrm{edge}}=0.06$ baked into the
figure. Had I only fixed the table, the figure would have contradicted it. Now 0.11,
consistent with Table 1 and the prose.

**On length:** validator ruled keep 14 pages and do not cut content. Content unchanged; the
figure relayout removed a sparse float page but text reflow kept the total at 14.

---

# Original submission (statistics and citations unchanged except as noted above)

## What the problem asked

Rendered page 2 of `CSE 60745_Fall 2026_HW2-Part(A).doc`, Problem 1 (35 pts):

> Based on the above context, you are asked to summarize the *benchmarks*, *baselines*, and
> commonly used *evaluation metrics* for graph embedding methods with <u>homogeneous graph
> structures</u> for <u>the task of node classification and link prediction</u> as
> comprehensive as you can.
> *Note:* (1) For the benchmarks, please describe each of the benchmark graphs (e.g., Cora)
> and draw the related graph schema. (2) For the commonly used baselines, please provide the
> reference (i.e., original paper) of each baseline and briefly describe the method.

**Channel reconciliation (R7).** I read all three channels for page 2.
`page_002.txt` and `page_002.png` agree verbatim. `manifest.json` reports `figures: []`
for all three pages; the single `n_images: 1` per page is the Notre Dame monogram in the
running header. **There is no figure to transcribe in this problem** — the "draw" instruction
means I must produce the schema diagrams myself. Page 3 confirms Problem 2 is the
heterogeneous counterpart, which fixes my scope as strictly homogeneous.

**Brief vs. page: no disagreement.** The master's transcription matches the page exactly.

*One observation for the master, not a defect in my answer:*
`framework/tools/crosscheck.py` emits "assigned 70 + uncovered 0 = 70, not 100 — confirm
against the assignment's stated total". The assignment page itself says "This assignment
contains 70 points", and 35 + 35 = 70, so the 70 is correct and the tool's 100 is the wrong
assumption. No action needed.

## What I decided it needed

**plain + diagram**, with **code used as a fact-checking instrument** rather than to produce
a headline result.

- *plain* — the answer is a survey; that is the bulk of it.
- *diagram* — "draw the related graph schema" is an explicit, graded instruction. Three
  vector PDF figures produced.
- *code* — there is no quantity the question asks me to compute. But every dataset statistic
  I quote is a factual claim, and quoting ~100 numbers from memory is exactly how this kind
  of answer goes confidently wrong. So I loaded every benchmark small enough to download and
  **counted**, rather than copying a secondary table. I also computed the edge-homophily
  ratios, which are the quantitative justification for the homophilous/heterophilous split
  that the answer's structure rests on.

## What I did

1. Built a venv with PyTorch + PyTorch Geometric and loaded 17 benchmark graphs, computing
   nodes, distinct undirected edges, stored directed entries, feature dimension, whether
   features are binary or real, class count, multi-label status, and symmetry.
2. Computed the edge homophily ratio $h_{\text{edge}}$ for all 13 single-label
   node-classification benchmarks.
3. For the OGB datasets (far too large to download) I pulled the official OGB documentation
   and took statistics, split protocols, metrics and negative-sampling counts from there.
4. For BlogCatalog / Flickr / YouTube / node2vec-PPI I took statistics from the original
   DeepWalk and node2vec PDFs, because the modern library versions of those names are
   *different graphs* (see below).
5. Ran an independent citation audit of all 36 references against Crossref / arXiv / PMLR /
   proceedings pages. It found six genuine errors in my draft, all fixed.
6. Drew three TikZ figures, compiled each to standalone vector PDF, rendered each to PNG and
   looked at it, and fixed the collisions I found (three rounds).
7. Compiled the fragment inside a master-like wrapper document to confirm it survives
   assembly.

### Two invariant checks that caught real problems

- **Reddit.** I measured 57,307,946 undirected edges. The GraphSAGE paper independently
  states an average degree of 492, and $2 \times 57{,}307{,}946 / 232{,}965 = 492.0$ exactly.
  This confirms 57.3M is right for this copy and that the 11.6M figure circulating on some
  dataset pages refers to a sparsified variant. Footnoted in the answer.
- **Cora.** PyG reports 10,556 directed entries $= 2 \times 5{,}278$, which reconciles the
  5,429 / 5,278 / 10,556 spread as one graph counted three ways (raw file lines with
  duplicates / distinct undirected / materialised directed). Footnoted rather than silently
  picking one, as the brief required.

### A trap worth flagging

**BlogCatalog, Flickr and PPI each name two genuinely different graphs** in this literature:
- BlogCatalog: DeepWalk/node2vec version = 10,312 nodes / 333,983 edges / 39 multi-labels /
  no features; the attributed version PyG ships = 5,196 / 171,743 / 8,189 features / 6 classes.
- Flickr: DeepWalk version = 80,513 / 5,899,882 / 195 groups / no features; the GraphSAINT
  version PyG ships = 89,250 / 449,878 / 500 features / 7 classes.
- PPI: node2vec's H. sapiens subgraph = 3,890 / 76,584 / 50 labels; GraphSAGE's inductive PPI
  = 24 graphs / 56,944 / 793,632 / 121 labels.

I verified both members of each pair and the answer states the distinction explicitly. This
is a common source of wrong numbers in exactly this kind of survey.

### A LaTeX trap that would have broken the master compile

The default `itemize` bullet resolves to a TS1 glyph. TinyTeX has `tcrm1095.tfm` but no
matching Type1 font, so the first compile died with
`!pdfTeX error: pdflatex (file tcrm1095): Font tcrm1095 at 600 not found` **after** typesetting
all pages. I fixed it self-containedly with `label=$\bullet$` on every list, rather than
forcing `lmodern` / `fontenc` into `preamble.txt` and changing the font of the master's whole
assembled document.

## Intermediate steps and code

All paths relative to PLAYGROUND.

| file | what it does | reproduces |
|---|---|---|
| `stats.py` | loads 17 benchmarks via PyG, counts N / E_und / E_dir / d / feat type / C / symmetry | `./.venv/bin/python stats.py` → `stats_out.json` + printed table |
| `stats_reddit.py` | same for Reddit (separate, ~1.5 GB download) | `./.venv/bin/python stats_reddit.py` |
| `homophily.py` | edge homophily over **distinct unordered pairs** (denominator = Table 1's `\|E\|`), under both self-loop conventions, with an automatic comparison against Zhu et al.'s published values | `./.venv/bin/python homophily.py` → `homophily_out.json` |
| `cornell_probe.py` | tests four homophily definitions on WebKB to check whether any reproduces Cornell's published 0.30 (none does) | `./.venv/bin/python cornell_probe.py` |
| `research/html2txt.py` | strips the downloaded OGB / PyG HTML to row-aligned text | `python3 research/html2txt.py research/*.html` |
| `research/ogb_nodeprop.txt`, `research/ogb_linkprop.txt` | official OGB statistics, splits, metrics, negative counts | source for Table 2 |
| `research/deepwalk.txt`, `research/node2vec.txt` | original-paper text | source for BlogCatalog/Flickr/YouTube/node2vec-PPI rows |
| `verified_numbers.md` | consolidates every number with its provenance tag ([C]omputed / [O]GB docs / [P]aper) | the audit trail for Tables 1–2 |
| `figs/fig_p1_*.tex` | TikZ sources for the three figures | `cd figs && pdflatex fig_p1_<name>.tex` |
| `build/master_test.tex` | master-like wrapper to verify the fragment assembles | `cd build && pdflatex master_test.tex` (×2) → 14 pages, exit 0 |

## Results

Every computed value in `answer.tex`, with its source:

- **Table 1** (`p1:tab:nodecls`), all rows except the Social block — from `stats.py` /
  `stats_reddit.py`. E.g. Cora 2,708 / 5,278 (10,556) / 1,433 binary / 7; CiteSeer 3,327 /
  4,552 (9,104) / 3,703 / 6; PubMed 19,717 / 44,324 (88,648) / 500 real / 3; Coauthor CS
  18,333 / 81,894 / 6,805 / 15; Coauthor Physics 34,493 / 247,962 / 8,415 / 5; Amazon
  Computers 13,752 / 245,861 / 767 / 10; Amazon Photo 7,650 / 119,081 / 745 / 8; Cornell
  183 / 280; Texas 183 / 295; Wisconsin 251 / 466 (all 1,703 / 5); Actor 7,600 / 26,752 /
  932 / 5; Chameleon 2,277 / 31,421 / 2,325 / 5; Squirrel 5,201 / 198,493 / 2,089 / 5;
  Reddit 232,965 / 57,307,946 / 602 / 41; PPI 56,944 / 793,632 / 50 / 121.
- **Table 1 homophily column** — from `homophily.py`, computed over **distinct unordered
  pairs with self-loops included**, i.e. the denominator is exactly the `|E|` column
  (verified 13/13 against `stats_out.json`): Cora 0.810, CiteSeer 0.736, PubMed 0.802,
  Coauthor CS 0.808, Coauthor Physics 0.931, Amazon Computers 0.777, Amazon Photo 0.827,
  Cornell 0.132, Texas 0.112, Wisconsin 0.206, Actor 0.219, Chameleon 0.231, Squirrel 0.223.
  Cross-check against Zhu et al.'s published Table 1: **8 of 9 agree exactly at two decimal
  places** (Cora, CiteSeer, PubMed, Texas, Wisconsin, Actor, Chameleon, Squirrel).
  **Cornell does not** — published 0.30, measured 0.13, and not reproducible under any of
  four definitions (`cornell_probe.py`); the validator independently swept ten definitions
  and found a maximum of 0.186. Reported as measured, with the disagreement footnoted.
- **Table 1 Social block** (BlogCatalog 10,312 / 333,983 / 39; Flickr 80,513 / 5,899,882 /
  195; YouTube 1,138,499 / 2,990,443 / 47) — from `research/deepwalk.txt` Table 1.
- **node2vec PPI** 3,890 / 76,584 / 50 — from `research/node2vec.txt`.
- **Table 2** (`p1:tab:ogbstats`) and all OGB split/metric/negative-count claims in the text
  (Hits@50 / 100,000 negatives; Hits@20; Hits@100 / 3,000,000 negatives; MRR / 1,000
  negatives per source) — from `research/ogb_*.txt`.
- **Reddit average-degree check** 492.0 — arithmetic on the measured edge count, stated in
  the answer's footnote.

Nothing in `answer.tex` is a number I estimated. Every statistic is either computed here or
traceable to a named primary source, and `verified_numbers.md` tags each one.

## Deliverables

In OUTPUT (`lint_output.py` passes, exit 0):

- `answer.tex` — LaTeX fragment. No `\documentclass` / `\usepackage` / `document`
  environment. All 13 labels namespaced `p1:` (`p1:eq:*`, `p1:fig:*`, `p1:tab:*`). No macros
  defined, so no macro-name collisions are possible. Figures referenced by bare filename.
- `fig_p1_schema_families.pdf` — the six schema families (one node type + one self-relation each).
- `fig_p1_subgraphs.pdf` — homophilous vs. heterophilous local structure, annotated with the
  measured $h_{\text{edge}}$.
- `fig_p1_linkpred.pdf` — the link-prediction split / negative-sampling / ranking protocol.
- `preamble.txt` — 9 `\usepackage` lines (amsmath, amssymb, booktabs, longtable, array,
  multirow, graphicx, xcolor, enumitem).

Verified: compiles to **14 pages, exit 0**, no overfull box above 8pt, all three figures
placed and legible.

## Where I am least confident

1. **Cornell's homophily.** I report 0.13; Zhu et al. publish 0.30. I verified this is not a
   convention artefact (four definitions tried, none gives 0.30), so either their Cornell
   differs from the standard PyG/Geom-GCN copy or the published figure is wrong. I state my
   measured value and flag the disagreement, which I believe is the right call, but a grader
   comparing against the paper will see a mismatch. This is now the weakest number in the
   answer and it is explicitly marked as such in the table and footnote.
2. ~~Wisconsin's residual~~ — **resolved in round 3.** It was the edge-set bug, not noise;
   over unordered pairs Wisconsin is 0.206 → 0.21, the published value exactly. Kept here
   because the lesson generalises: when a number is "close but not exact" and I cannot say
   why, that is a defect I have not found yet, not a tolerance to be widened. I widened the
   tolerance instead, and the validator caught it.
3. **Method descriptions are from domain knowledge, not re-derived.** The *citations* were
   independently audited and corrected, and the *statistics* were computed. But the 2–4
   sentence descriptions of what each of ~30 methods does (e.g. the exact form of the GCNII
   identity mapping, the GIN $\epsilon$ formulation) are written from knowledge and were not
   individually re-checked against each paper. I believe they are correct and they are
   standard, but that is the weakest-evidence part of the answer.
4. **Coauthor / Amazon as link-prediction benchmarks.** I state these "also serve as link
   prediction benchmarks". That is true in practice but is a softer, convention-level claim
   than the rest, not tied to a specific source.
5. **BlogCatalog's canonical citation is genuinely ambiguous.** DeepWalk cites Tang & Liu
   (KDD 2009); node2vec cites Zafarani & Liu (ASU Social Computing Data Repository, 2009).
   I quote DeepWalk's numbers and cite Tang & Liu accordingly, which is self-consistent, but
   a grader following node2vec would expect the other citation.
6. **`ogbn-proteins` is arguably a borderline inclusion** — it is homogeneous (protein nodes,
   association edges) but is typed by species and carries edge rather than node features. I
   included it and said so explicitly; if the validator considers it out of scope it can be
   dropped without affecting anything else.
7. **Reddit's 11.6M-edge figure.** I assert it refers to a sparsified copy. My measurement
   (57.3M) and the GraphSAGE paper's stated average degree of 492 agree with each other, so I
   am confident about *my* number; I am less certain about my *explanation* of where the
   11.6M figure comes from.
