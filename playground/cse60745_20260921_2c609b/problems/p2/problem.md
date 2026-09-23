# Problem id: `p2`

**Course:** CSE 60745 (Fall 2026), University of Notre Dame — *Graph Learning: Techniques & Applications*
**Assignment:** HW-2: Part (A). Total 70 pts; this problem is worth **35 pts**.
**Where it lives:** rendered page **3** of
`/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/ingest/pages/CSE 60745_Fall 2026_HW2-Part(A)/page_003.png`
(text: `page_003.txt`). Anchor text: `Problem 2 (35 pts). Based on the above context, ...`
The "above context" paragraph is on rendered page **2**.

## Figures

There are **no figures** in this assignment. `manifest.json` lists one image per page, which is the
Notre Dame monogram in the running header — `figures: []` on every page. You do **not** need to read
any figure file. The "draw" instruction in the question means **you** must produce the schema
diagrams yourself.

## Verbatim question text

> In this class, we have two-fold course objectives. The first one is to explore recent core
> techniques and advances in graph learning research, in the forms of class lectures, selected paper
> presentations and discussion, covering the topics of i) graph embedding techniques, ii) graph
> neural networks, iii) knowledge graphs, and iv) advanced topics on graph learning. Through our
> learning, we want to summarize the benchmarks and baselines that have been widely used for graph
> representation learning for 1) homogeneous graphs, 2) heterogeneous graphs; and 3) knowledge
> graphs.
>
> **Problem 2 (35 pts).** Based on the above context, you are asked to summarize the *benchmarks*,
> *baselines*, and commonly used *evaluation metrics* for graph embedding methods with
> <u>heterogeneous graph structures</u> for <u>the task of node classification and link
> prediction</u> as comprehensive as you can.
> *Note:* (1) For the benchmarks, please describe each of the benchmark graphs (e.g., DBLP/ACM) and
> draw the related graph schema. (2) For the commonly used baselines, please provide the reference
> (i.e., original paper) of each baseline and briefly describe the method.

(In the original, "DBLP/ACM" is a blue hyperlink — the course is pointing you at the standard
bibliographic heterogeneous benchmarks. Nothing is hidden behind the link that you need.)

## What you must deliver

A LaTeX **fragment** `answer.tex` in your OUTPUT directory, starting at `\section*{...}` /
`\subsection*{...}` level, plus any `fig_p2_*.pdf` files and a `preamble.txt`. It must contain:

0. **A short formal set-up.** Define a heterogeneous information network
   $G=(V,E,\phi,\psi)$ with node-type map $\phi:V\to\mathcal{A}$ and edge-type map
   $\psi:E\to\mathcal{R}$, where $|\mathcal{A}|+|\mathcal{R}|>2$; define the **network schema**
   $T_G=(\mathcal{A},\mathcal{R})$ and the **meta-path**. Cite Sun & Han's HIN formalism (Sun et
   al., "PathSim", VLDB 2011; Shi et al., "A Survey of Heterogeneous Information Network Analysis",
   TKDE 2017). This is what makes the rest of the answer precise, and it is the thing that
   distinguishes this problem from Problem 1.
1. **Benchmarks.** A comprehensive survey of the standard *heterogeneous*-graph benchmarks used for
   node classification and link prediction. At minimum cover:
   - bibliographic: **DBLP** (Author–Paper–Term–Venue/Conference), **ACM** (Author–Paper–Subject,
     plus Paper–Paper citation), **AMiner**, **OGB's ogbn-mag** (Author–Paper–Institution–Field of
     study);
   - movie: **IMDB** (Movie–Actor–Director, optionally Keyword);
   - business/review: **Yelp** (Business–User–Service–Rating level), **Amazon**;
   - academic/social: **Freebase** (HGB version), **LastFM** (User–Artist–Tag), **Douban Movie**,
     **MovieLens / ML-100K** as a user–item bipartite HIN, **PubMed** in its HGB heterogeneous form;
   - the standardised suites: **HGB (Heterogeneous Graph Benchmark)** of Lv et al. KDD'21, and
     **OGB-MAG / OGB-LSC MAG240M**; note HGB exists precisely because earlier papers used
     inconsistent DBLP/ACM/IMDB preprocessing.
   *Describe each*: domain, node types and counts per type, edge/relation types and counts, which
   node type is labelled and how many classes, what the features are, and the task(s) it is used
   for. Put the statistics in a table. **Get the numbers right**; where a dataset has several
   incompatible versions in circulation (DBLP and ACM notoriously do — HAN's, MAGNN's, GTN's and
   HGB's DBLP differ in node counts), say which version your numbers are for and note the
   discrepancy. That caveat is itself worth marks.
2. **Graph schemas — this is the explicitly graded "draw" instruction, and it carries real content
   here (unlike the homogeneous case).** Draw the **network schema** of each benchmark family as a
   TikZ diagram: typed nodes as labelled circles/rectangles, typed relations as labelled edges.
   At minimum draw: DBLP (A–P, P–T, P–V), ACM (A–P, P–S, P–P), IMDB (M–A, M–D, M–K), ogbn-mag
   (A–P, A–I, P–P, P–F), Yelp, and LastFM. Alongside each schema, list the **meta-paths** commonly
   used on it (DBLP: APA, APCPA, APTPA; ACM: PAP, PSP; IMDB: MAM, MDM; ogbn-mag: PAP, PAIAP) and
   say what semantic relation each meta-path encodes. Use TikZ inline, or emit standalone
   `fig_p2_*.pdf` files — either is fine, but the schemas must be legible and typed.
3. **Baselines.** Survey the commonly used heterogeneous graph-embedding baselines **with the
   original paper reference for each** and a 2–4 sentence description. Cover, grouped by family:
   - homogeneous methods applied as baselines (the papers always report them): DeepWalk, LINE,
     node2vec, GCN, GAT, GraphSAGE — say explicitly that they ignore type information, which is the
     point of reporting them;
   - meta-path / random-walk HIN embedding: **metapath2vec** (Dong et al. KDD'17), **HIN2Vec** (Fu
     et al. CIKM'17), **ESim** (Shang et al. 2016), **HERec** (Shi et al. TKDE'18), PTE (Tang et al.
     KDD'15);
   - heterogeneous GNNs: **R-GCN** (Schlichtkrull et al. ESWC'18), **HAN** (Wang et al. WWW'19),
     **MAGNN** (Fu et al. WWW'20), **GTN** (Yun et al. NeurIPS'19), **HetGNN** (Zhang et al.
     KDD'19), **HGT** (Hu et al. WWW'20), **HGB/simple-HGN** (Lv et al. KDD'21), **ie-HGCN**,
     **RSHN**, **HPN**;
   - self-supervised heterogeneous: **DMGI** (Park et al. AAAI'20), **HDGI**, **HeCo** (Wang et al.
     KDD'21);
   - and, because HINs overlap with KGs for link prediction: **TransE** (Bordes et al. NIPS'13),
     DistMult, ComplEx, ConvE, RotatE — mention them as the relation-aware link-prediction
     baselines that heterogeneous link-prediction papers (and HGB's LP track) report.
   References must be real and checkable: author list (or first author et al.), title, venue, year.
   Do **not** invent citations. If unsure of a venue/year, verify it with WebSearch/WebFetch — you
   have unrestricted network access.
4. **Evaluation metrics**, split by task:
   - *Node classification*: **Micro-F1 and Macro-F1** (the dominant pair in the HIN literature),
     Accuracy, ROC-AUC; note that HIN benchmarks usually label **one** node type (e.g. the author in
     DBLP, the paper in ACM), that IMDB/Freebase in HGB are **multi-label**, so Micro-F1 there is
     computed over the pooled label matrix, and that the standard unsupervised protocol is
     embed → freeze → train a linear/logistic classifier at varying training ratios (20/40/60/80%),
     plus NMI/ARI on k-means clustering of the embeddings, which HAN/MAGNN/HeCo all report.
   - *Link prediction*: **AUC-ROC**, **Average Precision / AUPRC**, **MRR**, **Hits@K**,
     Precision@K/Recall@K; explain that in a HIN, link prediction is stated *per relation type*
     (predict A–P, or P–V), that negatives are sampled type-consistently, and that HGB's LP track
     reports ROC-AUC and MRR.
   Give formulas for Micro/Macro-F1, AP, MRR, Hits@K, NMI using `amsmath`. A table mapping
   *dataset → target node type → task → metric normally reported* is a strong close.

## Consistency constraint (important)

A sibling worker is answering Problem 1 (the *homogeneous* version) and defines the same shared
metrics. Use exactly these standard definitions so the two answers cannot contradict each other:
- Micro-F1 = F1 over the pooled confusion matrix (equals accuracy in single-label multi-class);
  Macro-F1 = unweighted mean of per-class F1.
- MRR = mean over queries of 1/rank of the first true item.
- Hits@K = fraction of positive edges ranked in the top K against the sampled negatives.
Keep your scope strictly to **heterogeneous** graphs. Do not re-survey Cora/CiteSeer/PubMed as
homogeneous citation benchmarks or re-describe GCN/GAT at length — mention homogeneous methods only
in their role as type-agnostic baselines. You may note in one sentence that the homogeneous case is
addressed in Problem 1.

## Rules you must follow

- `answer.tex` is a **fragment**: no `\documentclass`, `\begin{document}`, `\end{document}`,
  `\usepackage`. Extra packages go one-per-line in `preamble.txt` as literal `\usepackage{...}`.
  You will certainly want `tikz`, `booktabs`, `amsmath`, `amssymb`, `longtable` — all installed.
- **Namespace everything with `p2`**: `\label{p2:tab:benchmarks}`, `\label{p2:fig:dblp-schema}`,
  figure files `fig_p2_*.pdf`, and any macro you define (`\p2xxx` is not a legal macro name — use
  e.g. `\pTwoMicroF`). Unnamespaced labels collide with Problem 1 and break the master compile.
- Reference figures by **bare filename**, never an absolute path.
- The answer is a homework submission, not a lab notebook: state the content a grader needs and
  stop. No code dumps, no exploration log.
- Scratch work (scripts, downloads, .aux/.log) stays in your PLAYGROUND, never in OUTPUT. Record any
  download in `downloads.md`.

## Length and depth

35 points, "as comprehensive as you can". Aim for roughly 4–7 compiled pages: substantial tables,
six or more typed schema diagrams, and dense-but-readable prose. Comprehensiveness is the graded
axis — breadth of coverage with correct citations beats a short elegant essay. But do not pad: every
benchmark listed must be actually described, every baseline listed must have a real reference.

---

# !! RESUME NOTICE — READ THIS FIRST (written by the master, not part of the original brief) !!

**This run was interrupted. You are resuming, not starting over. Do NOT redo the research.**

A previous session of you did nearly all of this work and was killed by a harness timeout at the
very last step — after writing and compiling the answer, while it was visually inspecting its own
rendered pages. Its work is intact in this playground. What is on disk right now:

- `answer.tex` (~43 KB) — **complete**. Opens with a `p2`-namespaced `\tikzset` block, then
  `\section*{Problem 2: ...}`, the HIN/schema/meta-path formalism, the benchmark tables, the
  per-dataset descriptions, the TikZ network schemas, the baselines, the metrics, and a closing
  remark about incompatible DBLP/ACM/IMDB versions.
- `preamble.txt` — 8 `\usepackage` lines (fontenc, lmodern, amsmath, amssymb, booktabs, multirow,
  array, tikz). Fine as-is.
- `notes.md` — the R7 three-channel reconciliation and the risk register. Already done; its
  conclusion was that there is **no figure to transcribe** (the one image per page is the ND
  monogram in the running header, `figures: []` on all three pages).
- `verify_hgb.py`, `hgb_verify_output.txt`, `hgb_info/` — the dataset-statistic verification the
  previous session ran against fetched sources. Reuse these; do not re-fetch.
- `downloads.md` — already records what was installed. Keep appending if you add anything.
- `build/test_wrapper.pdf` — the previous session's trial compile: **12 pages, zero LaTeX errors,
  zero undefined references** (`build/test_wrapper.log` confirms). `build/pg-01.png` …
  `build/pg-12.png` are the rendered pages of exactly that PDF.

## What is actually left to do

1. **The deliverable was never copied out.** `output/cse60745_20260921_2c609b/p2/` is **empty**.
   This is the one thing that must happen.
2. Finish the visual inspection the previous session had started — read `build/pg-01.png` through
   `build/pg-12.png` and check the TikZ schemas are legible, tables are not overfull, and no page
   is mostly white. Fix anything genuinely wrong; do not rewrite prose that is already fine.
3. Then copy `answer.tex` and `preamble.txt` into your OUTPUT dir and run
   `python3 framework/tools/lint_output.py <your OUTPUT>`.

The `missfont.log` in `build/` is stale — it is from early probe files that predate `lmodern`
being added to `preamble.txt`. The final wrapper compiled with no missing fonts. Ignore it.

Spend your effort on verification and on the copy-out, not on regenerating work that already
exists and already compiles.

---

# !! ROUND-2 REVISION REQUEST (master, after the MASTER validator reviewed the assembled document) !!

Your answer already **PASSED** your own worker-validator, and the master validator then verified it
again independently and found the content correct — it reconciled your Table 5 against HGB's
published totals exactly, including the non-obvious ACM case where cite/ref are mutual inverses
(5,343+5,343+2*(9,949+3,025+255,619) = 547,872). **Do not re-do research and do not rewrite prose
that is already correct.** There are exactly two things to fix, both raised against the assembled
28-page PDF.

## [D1.2] Two tables are never `\ref`'d, so they float away from their text

`\label`s that nothing references give LaTeX no anchor, so the float drifts to wherever it fits.

- **Table 7** (`p2.tex:324` in the assembled copy, the meta-path table) — never `\ref`'d.
- **Table 8** (`p2.tex:739`, the dataset/task/metric table) — never `\ref`'d. Worse, the section it
  belongs to (§5.3) contains only your "Closing remark.", which never mentions the table, so the
  table floats **alone onto the last page**.

*Fix:* give each table a one-sentence lead-in in its own section that references it by
`Table~\ref{...}`, exactly as you already do elsewhere. Consider `[H]` placement (the `float`
package is loaded by the master's `main.tex`, so `[H]` is available to you) where the table should
sit exactly where it is written. I made the identical fix in Problem 1 for the same defect, so the
two answers stay stylistically consistent.

## [D1.3] Five benchmarks are described but have no schema drawn

The question's Note says to describe each benchmark graph **and draw the related graph schema**, so
a described-but-undrawn benchmark is a partial miss on an explicitly graded instruction. Missing:
**AMiner, Douban, HGB-PubMed, MovieLens, Amazon.**

**Amazon is the important one** — your §2.2 already specifies its schema verbally and leans on it to
motivate the $|\mathcal{A}|+|\mathcal{R}|>2$ definition (a single node type with two relation types
is the clean illustration that heterogeneity can come from relations alone). Drawing it closes that
argument.

*Fix:* add one more schema figure, in the same TikZ style you already use (`p2ent`, `p2rel`,
`p2el`, `\pTwoTgt` etc. are already defined at the top of your `answer.tex`), covering these five.
Group them into a single figure if that reads better — a second full-width schema plate alongside
your existing Figure 4 would be consistent.

**Every relation you draw must come from a source you have already verified**, not from memory —
`hgb_info/` and `hgb_verify_output.txt` in your playground are the HGB dataset info you already
fetched, and HGB-PubMed and Amazon are both HGB datasets, so their type/relation lists are
derivable from what is already on disk. If you genuinely cannot source a schema for one of the
five, **say so in one line in the caption and omit that one** rather than guessing — an
unverifiable schema is worse than an acknowledged gap. The master validator recomputes these.

## Scope

Nothing else. Do not expand coverage, do not add benchmarks, do not restructure. Both fixes are
additive. Your page count will grow slightly; that is expected and fine. Re-compile, re-read your
rendered pages, re-copy to OUTPUT, re-run the lint.
