# Problem id: `p1`

**Course:** CSE 60745 (Fall 2026), University of Notre Dame — *Graph Learning: Techniques & Applications*
**Assignment:** HW-2: Part (A). Total 70 pts; this problem is worth **35 pts**.
**Where it lives:** rendered page **2** of
`/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/ingest/pages/CSE 60745_Fall 2026_HW2-Part(A)/page_002.png`
(text: `page_002.txt`). Anchor text: `Problem 1 (35 pts). Based on the above context, ...`

## Figures

There are **no figures** in this assignment. `manifest.json` lists one image per page, which is the
Notre Dame monogram in the running header — `figures: []` on every page. You do **not** need to read
any figure file. The "draw" instruction in the question means **you** must produce the schema
diagrams yourself.

## Verbatim question text

The paragraph immediately preceding Problem 1 is the "above context" the question refers to, so it
is transcribed too.

> In this class, we have two-fold course objectives. The first one is to explore recent core
> techniques and advances in graph learning research, in the forms of class lectures, selected paper
> presentations and discussion, covering the topics of i) graph embedding techniques, ii) graph
> neural networks, iii) knowledge graphs, and iv) advanced topics on graph learning. Through our
> learning, we want to summarize the benchmarks and baselines that have been widely used for graph
> representation learning for 1) homogeneous graphs, 2) heterogeneous graphs; and 3) knowledge
> graphs.
>
> **Problem 1 (35 pts).** Based on the above context, you are asked to summarize the *benchmarks*,
> *baselines*, and commonly used *evaluation metrics* for graph embedding methods with
> <u>homogeneous graph structures</u> for <u>the task of node classification and link prediction</u>
> as comprehensive as you can.
> *Note:* (1) For the benchmarks, please describe each of the benchmark graphs (e.g., Cora) and draw
> the related graph schema. (2) For the commonly used baselines, please provide the reference (i.e.,
> original paper) of each baseline and briefly describe the method.

(In the original, "Cora" is a blue hyperlink — the course is pointing you at the standard citation
network benchmark. Nothing is hidden behind the link that you need.)

## What you must deliver

A LaTeX **fragment** `answer.tex` in your OUTPUT directory, starting at `\section*{...}` /
`\subsection*{...}` level, plus any `fig_p1_*.pdf` files and a `preamble.txt`. It must contain:

1. **Benchmarks.** A comprehensive survey of the standard *homogeneous*-graph benchmarks used for
   node classification and link prediction. At minimum cover: the citation networks **Cora,
   CiteSeer, PubMed**; **WebKB / Cornell-Texas-Wisconsin** or **Actor**/**Chameleon-Squirrel** as
   heterophilous counterexamples; **Coauthor CS / Coauthor Physics** and **Amazon Computers /
   Amazon Photo**; social/interaction graphs **BlogCatalog**, **Flickr**, **PPI**, **Reddit**;
   and the OGB suite **ogbn-arxiv, ogbn-products, ogbn-papers100M** (node classification) and
   **ogbl-collab, ogbl-ppa, ogbl-citation2, ogbl-ddi** (link prediction).
   *Describe each*: domain, #nodes, #edges, node-feature type and dimension, #classes,
   directed/undirected, and which task it is normally used for. Put the statistics in a table —
   a well-organised table is worth more than prose here. **Get the numbers right** (e.g. Cora is
   2708 nodes / 5429 (or 10556 directed) edges / 1433 binary bag-of-words features / 7 classes); if
   a figure varies between sources (Cora edge count is reported as 5278, 5429 or 10556 depending on
   de-duplication and directedness), say so in a footnote rather than silently picking one.
   State the standard split protocol where it matters (Planetoid 20-per-class semi-supervised split
   vs. the 60/20/20 "full-supervised" split; OGB's fixed time/species splits).
2. **Graph schemas — this is the explicitly graded "draw" instruction.** Draw the schema of the
   benchmark graphs. A homogeneous graph has a *single* node type and a *single* edge type, so the
   schema is small: e.g. `Paper --cites--> Paper`, `User --follows--> User`, `Protein
   --interacts--> Protein`. Draw these as TikZ self-loop schema diagrams, and **also** draw a small
   illustrative subgraph sketch so the diagram is not vacuous. Group the benchmarks by schema
   family (citation / co-authorship / co-purchase / social / biological / web-page hyperlink) and
   give one schema diagram per family — that is the honest reading of "the related graph schema" for
   homogeneous graphs, and say so in one sentence so the grader sees you understood why the schema
   is degenerate here. Use TikZ inline; if you prefer, emit standalone `fig_p1_*.pdf` files.
3. **Baselines.** Survey the commonly used homogeneous graph-embedding baselines **with the original
   paper reference for each** and a 2–4 sentence description of the method. Cover, grouped by
   family:
   - matrix-factorisation / spectral: Laplacian Eigenmaps (Belkin & Niyogi 2001), GraRep (Cao et
     al. CIKM'15), HOPE (Ou et al. KDD'16), NetMF (Qiu et al. WSDM'18);
   - random-walk / skip-gram: **DeepWalk** (Perozzi et al. KDD'14), **LINE** (Tang et al. WWW'15),
     **node2vec** (Grover & Leskovec KDD'16), struc2vec (Ribeiro et al. KDD'17);
   - autoencoder: SDNE (Wang et al. KDD'16), **GAE/VGAE** (Kipf & Welling NIPS-W'16);
   - GNN / message passing: **GCN** (Kipf & Welling ICLR'17), **GraphSAGE** (Hamilton et al.
     NeurIPS'17), **GAT** (Veličković et al. ICLR'18), JK-Net, GIN (Xu et al. ICLR'19), SGC (Wu et
     al. ICML'19), APPNP (Klicpera et al. ICLR'19), GCNII, and for link prediction **SEAL** (Zhang &
     Chen NeurIPS'18) and NBFNet;
   - self-supervised/contrastive: DGI (Veličković et al. ICLR'19), GRACE, GraphCL, BGRL;
   - and the non-learned link-prediction heuristics that every link-prediction paper reports as
     baselines: Common Neighbors, Jaccard, Adamic–Adar, Resource Allocation, Preferential
     Attachment, Katz, Personalized PageRank, SimRank.
   References must be real and checkable: author list (or first author et al.), title, venue, year.
   Do **not** invent citations. If unsure of a venue/year, verify it with WebSearch/WebFetch — you
   have unrestricted network access.
4. **Evaluation metrics**, split by task:
   - *Node classification*: Accuracy, **Micro-F1 and Macro-F1** (and why Macro-F1 matters under
     class imbalance), Precision/Recall, ROC-AUC (one-vs-rest for multi-class), and the convention
     of reporting mean ± std over 10/100 random splits or seeds. Mention the standard evaluation
     protocol for unsupervised embeddings: freeze the embedding, train a one-vs-rest logistic
     regression on it, report Micro/Macro-F1 at varying training ratios.
   - *Link prediction*: **AUC-ROC**, **Average Precision / AUPRC**, Precision@K and Recall@K,
     **Hits@K** (OGB's ogbl-collab uses Hits@50, ogbl-ddi Hits@20, ogbl-ppa Hits@100), **MRR**
     (ogbl-citation2), and NDCG. Explain the negative-sampling protocol and why AUC is optimistic on
     sparse graphs relative to AP/Hits@K.
   Give the formula for the non-obvious ones (Micro/Macro-F1, AP, MRR, Hits@K, NDCG) using
   `amsmath`. A table mapping *dataset → task → metric normally reported* is a strong way to close
   this section.

## Consistency constraint (important)

A sibling worker is answering Problem 2 (the *heterogeneous* version) and will define the same
shared metrics. Define Micro-F1 / Macro-F1 / AUC-ROC / AP / MRR / Hits@K in the standard way so the
two answers cannot contradict each other:
- Micro-F1 = F1 computed over the pooled confusion matrix (equals accuracy in single-label
  multi-class); Macro-F1 = unweighted mean of per-class F1.
- MRR = mean over queries of 1/rank of the first true item.
- Hits@K = fraction of positive edges ranked in the top K against the sampled negatives.
Keep your scope strictly to **homogeneous** graphs — do not survey DBLP/ACM/IMDB or metapath2vec/HAN
/HGT; those belong to Problem 2. You may note in one sentence that the heterogeneous case is
addressed in Problem 2.

## Rules you must follow

- `answer.tex` is a **fragment**: no `\documentclass`, `\begin{document}`, `\end{document}`,
  `\usepackage`. Extra packages go one-per-line in `preamble.txt` as literal `\usepackage{...}`.
  You will certainly want `tikz`, `booktabs`, `amsmath`, `amssymb`, `longtable` — all installed.
- **Namespace everything with `p1`**: `\label{p1:tab:benchmarks}`, `\label{p1:fig:citation-schema}`,
  figure files `fig_p1_*.pdf`, and any macro you define (`\p1xxx` is not a legal macro name — use
  e.g. `\pOneMicroF`). Unnamespaced labels collide with Problem 2 and break the master compile.
- Reference figures by **bare filename**, never an absolute path.
- The answer is a homework submission, not a lab notebook: state the content a grader needs and
  stop. No code dumps, no exploration log.
- Scratch work (scripts, downloads, .aux/.log) stays in your PLAYGROUND, never in OUTPUT. Record any
  download in `downloads.md`.

## Length and depth

35 points, "as comprehensive as you can". Aim for roughly 4–7 compiled pages: substantial tables, a
handful of schema diagrams, and dense-but-readable prose. Comprehensiveness is the graded axis —
breadth of coverage with correct citations beats a short elegant essay. But do not pad: every
benchmark listed must be actually described, every baseline listed must have a real reference.
