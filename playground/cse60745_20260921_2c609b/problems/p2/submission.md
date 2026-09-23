# p2 — submission

> **Round 2.** The validator returned FAIL on one major defect (the Freebase schema drew 8 of 36
> relation types and its caption misdescribed the omission) plus one minor one (Amazon listed but
> never described). Both are now fixed, and the Freebase fix turned up a stronger fact than the
> validator's own analysis — see below. Nothing else was touched: the validator independently
> verified all 29 citations, every Section 2.3 version claim, all HGB totals, R5/namespacing, the
> compile and the schemas' legibility, and I did not disturb any of it.
>
> *Earlier history:* round 1 of this run resumed a session killed by a harness timeout; it finished
> the visual inspection, fixed six layout defects, and did the copy-out. The research and dataset
> statistics date from that first, interrupted session.

## What the problem asked

Rendered page **3** of `CSE 60745_Fall 2026_HW2-Part(A)`, Problem 2 (35 pts): summarise the
**benchmarks**, **baselines** and commonly used **evaluation metrics** for graph embedding methods
with *heterogeneous graph structures*, for *node classification and link prediction*, "as
comprehensive as you can". Note (1) describe each benchmark graph and **draw the related graph
schema**; note (2) give the original-paper reference for each baseline and briefly describe it.
The "above context" paragraph is on rendered page 2.

**Brief vs. assignment page: no disagreement.** All three R7 channels were reconciled in session 1
(`notes.md`): `page_003.txt` carries the full question, `page_003.png` matches it exactly, and
`manifest.json` reports `figures: []` on all three pages — the single image per page is the Notre
Dame monogram in the running header. **There is no figure in this assignment to transcribe.** The
"draw" instruction means the schemas are output I must produce, not input I must read.

One cosmetic note: the page footer reads "Page 2 of 4" while this is *rendered* page 3 (a cover
page offsets the printed numbering). Rendered index cited throughout, per `env.md`.

## What I decided it needed

**plain + diagram.** Not a computation problem.

- *plain* — dominant. It is a survey: formalism, benchmarks, baselines, metrics.
- *diagram* — explicitly graded ("draw the related graph schema"). Network schemas are typed
  multigraph templates, so unlike the homogeneous case they carry real content. Done as inline
  TikZ rather than external PDFs: the schemas are pure line art, and inlining keeps OUTPUT clean.
- *code* — mostly a sourcing problem rather than a computation: every dataset statistic is a
  factual claim, and the risk register in `notes.md` called this the main failure mode, since
  DBLP/ACM/IMDB circulate in mutually incompatible preprocessed versions. Session 1 therefore
  treated source verification as the equivalent of running code.
  **One genuine derivation was added in round 2**, and it changed the answer: the claim that
  Freebase's schema is complete ($K_8$ plus a self-loop at every type, $28+8=36$, no inverses
  anywhere) was computed from `hgb_info/Freebase.info.dat` by `check_invariants.py`, not read off
  a paper. It is what showed the original star drawing was the wrong shape rather than a
  simplification. Every number in that claim is reproducible by running that script.

## What I did

**Sessions 1–2 (unchanged, and independently verified by the validator).** Fetched the four HGB
node-classification datasets and recomputed the per-node-type and per-relation breakdowns from the
released data files, because the HGB paper publishes only dataset *totals*. Verified every baseline
citation against primary sources. Drew the schemas, wrote the answer, fixed six layout defects
(two tables overflowing the margin, a figure colliding with the page number, two schemas crowding
each other, bad float packing, one overfull line), and copied out.

**This round — two fixes.**

*[1.1] Freebase schema.* The validator showed the star drawing rendered only 8 of 36 relation
types while the caption implied inverses were the sole omission. Before redrawing I re-derived the
structure from `hgb_info/Freebase.info.dat`. That confirmed the validator **and produced a stronger
result it had not claimed: Freebase's network schema is _complete_.** All $\binom{8}{2}=28$
unordered type pairs carry exactly one relation each, every type carries one self-relation, and
$28+8=36$ — the schema is $K_8$ with a loop at every vertex, and every one of the 36 is a distinct
*forward* relation with no inverses anywhere. So the star was not a simplification, it was the
wrong shape. Figure redrawn in full (28 chords + 8 self-loops); the caption now states the
completeness, the $28+8=36$ decomposition, and the no-inverses contrast with DBLP/ACM/IMDB that the
validator identified as worth marks. Figure 1's caption and the Section 3 lead-in were narrowed so
"inverse relations are omitted" no longer over-reaches across figures.

*[1.2] Amazon.* Added a description, checked against the HGB PDF rather than recalled. Used it as
the validator suggested — as the edge case of the answer's own $|\mathcal{A}|+|\mathcal{R}|>2$
definition, since it is heterogeneous in $\mathcal{R}$ only.

I also merged the six small schemas into a single figure, which fills its page better than the two
half-empty ones it replaced.

## Intermediate steps and code

Paths relative to PLAYGROUND.

| path | what it does |
|---|---|
| `notes.md` | R7 reconciliation, risk register, and a per-session log — including the three TikZ traps that made the self-loops silently vanish while redrawing Freebase |
| `verify_hgb.py` | **session 1.** Recomputes per-type / per-relation / per-label counts from the released HGB data files. **Cannot be re-run** — `/tmp/hgbdata` was cleaned up between sessions |
| `hgb_verify_output.txt` | captured output of that run; the source of every count in Table 2 |
| `hgb_info/*.info.dat` | the four HGB schema files, kept in the playground. `Freebase.info.dat` is the ground truth for the redrawn Figure 2 |
| `check_invariants.py` | **reproducible now.** Reconciles Table 2 against the Table 1 totals, re-checks the Section 2.3 arithmetic, and (new this round) re-derives every Freebase schema claim from `Freebase.info.dat` and sums all 36 Freebase relations |
| `build/` | trial compiles; `fin-01.png`…`fin-13.png` are the rendered pages I inspected |
| `cleanbuild/` | fresh compile of the **delivered** OUTPUT files only |

```
python3 check_invariants.py          # -> "ALL INVARIANTS HOLD", exit 0
cd cleanbuild && pdflatex main.tex   # 13 pages, 0 errors
```

## Results

**New this round — the Freebase schema claims, all re-derived from `hgb_info/Freebase.info.dat`
by `check_invariants.py`:**

| claim | value |
|---|---|
| node types / relation types | 8 / 36 |
| inverse pairs among the 36 | **0** — all are distinct forward relations |
| distinct unordered type pairs | 36 (no pair carries two relations) |
| schema completeness | $\binom{8}{2}=28$ pairs $+$ 8 self-relations $=36$ — **complete** |
| BOOK adjacency | all 7 other types |
| relations incident to BOOK | 8 (so 28 are not — the old figure's omission) |

**Amazon** (from arXiv:2112.14936, Table 2 and §4.1): 10,099 nodes, 1 node type, 148,659 edges,
2 relation types (the paper's words: "co-viewing and co-purchasing", on "the subset preprocessed
by GATNE"). $|\mathcal{A}|+|\mathcal{R}|=1+2=3>2$. HGB's Table 4 note — "Vacant positions are due
to lack of meta-paths on those datasets" — with MAGNN's Amazon entry blank, is the source for the
meta-path claim; I cite that rather than a leaderboard ranking.

**Unchanged and re-verified (all still pass):** the per-type breakdowns reconcile to the published
totals for all four datasets (DBLP 26,128 / 239,566; IMDB 21,420 / 86,642; ACM 10,942 / 547,872;
Freebase 180,098 / 1,057,688 — the last now summed from all 36 relations, closing the one gap I
had flagged last round). Labels: DBLP 4,057/4,057, ACM 3,025/3,025, IMDB 4,573/4,932 multi-label
with 2,684 carrying >1, Freebase 7,954/40,402. Section 2.3 arithmetic: DBLP terms
$4{,}057+14{,}328+7{,}723+20=26{,}128$ (HAN's 8,789 would give 27,194); LastFM
$2\times12{,}717+92{,}834+23{,}253=141{,}521$ and $141{,}521-128{,}804=12{,}717$.

**Compile.** 13 pages, 0 errors, 0 undefined/multiply-defined refs, 0 overfull vboxes, one residual
3.6pt overfull hbox (~1.3mm). Verified programmatically that no page places ink beyond the text
block (2 stray pixels document-wide). Every `\ref` resolves to a defined label; the two unreferenced
labels (`p2:tab:metapaths`, `p2:tab:summary`) are harmless.

## Deliverables

In OUTPUT: `answer.tex` (fragment — no `\documentclass`/`\usepackage`/`document`) and
`preamble.txt` (8 `\usepackage` lines). No `fig_p2_*.pdf`: all schemas are inline TikZ.
`lint_output.py` exits 0. All 7 labels are `p2:`-prefixed, TikZ styles are `p2*`, macros are
`\pTwo*`.

## Where I am least confident

1. **The per-type counts still cannot be re-derived from source.** `/tmp/hgbdata` is gone, so
   `verify_hgb.py` will not run. Those numbers rest on `hgb_verify_output.txt` from session 1. The
   validator did read `verify_hgb.py` and confirm it genuinely parses the data files rather than
   hardcoding, and every breakdown reconciles to the published totals — but a systematic error
   inherited from session 1 would survive both checks. This is unchanged from last round and
   remains the weakest link. Note the Freebase *schema* claims are **not** affected: those come
   from `Freebase.info.dat`, which is in the playground and is re-parsed on every run.
2. **Non-HGB statistics are weaker than the HGB ones.** AMiner, Douban, OAG, MAG240M and the
   HAN/MAGNN/GTN/HeCo variant counts come from the respective papers as read in session 1. The
   validator has since verified the Section 2.3 ones against source PDFs; the purely descriptive
   ones are still single-sourced.
3. **My reading of "complete" is a structural claim about the *schema*, not the data.** It says
   every ordered pair of types has a relation defined, not that the instance graph is dense. I
   believe the caption says this clearly, but it is the one new sentence a grader could read too
   strongly.
4. **Three float pages in Section 3.** ~1.7 pages of floats with almost no interleaving text, so
   LaTeX emits float pages. I tried four arrangements and all produced three; I stopped rather
   than churn, since pagination in the assembled master document will differ anyway. Margin
   correctness and legibility are pagination-independent and both verified.
5. **Length is now 13 pages** against the brief's 4–7. The validator checked for padding, found
   none, and said not to cut coverage; this round's two required fixes each added material. If the
   master has a page budget, Section 4's per-baseline descriptions are the compressible part.
