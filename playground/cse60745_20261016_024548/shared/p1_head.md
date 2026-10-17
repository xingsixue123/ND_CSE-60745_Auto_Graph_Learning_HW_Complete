# Problem p1 — Q1 Structural Encoding (20 pts) + Q2 Efficient Graph Transformer (20 pts)

**Problem id: `p1`.** Namespace every LaTeX label, every figure filename and every macro
you define with `p1:` / `fig_p1_` (rule R5 below).

These two questions are one problem because the notebook makes Q2 a subclass of Q1:
`class SparseSPDAttention(SPDAttention)` (cell 16), run as
`LapPETransformer(attention_cls=SparseSPDAttention)` (cell 18). Q2 inherits Q1's
parameters, Q1's `precompute` and Q1's absolute encoding. Answer them as one coherent
implementation.

---

## 1. Where this comes from

Assignment document: `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3(B).doc`

Ingested at `INGEST/pages/CSE 60745_Fall 2026_HW3(B)/` — **rendered page 2** (page 1 is
the cover page). Anchor text: `Q1: Structural Encoding in Graph Transformer (20 pts)`.

The document has **no figures**. Both rendered pages contain exactly one image, the Notre
Dame monogram in the running header; I read both page PNGs and confirmed it. Nothing in
this problem depends on an image, so there is no figure file you need to open. The text
channel and the page image agree verbatim.

### Assignment text, transcribed verbatim from rendered page 2

> \* This assignment contains 70 points. You are encouraged to finish independently. Any
> submitted work that it copied from any source or too similar to be an independent
> write-up will not be given credit. Please submit this homework (as a PDF or Word file
> including the cover page) to ND Canvas by **11:59pm on Monday, 10/26/2026**.
>
> In this assignment, you will practice the implementation of basic graph transformers.
> Please use Google Colab for experiments and **submit only your implemented code file**.
> Useful papers for this assignment are listed as follows:
>
> [1] Chen, Dexiong, Leslie O'Bray, and Karsten Borgwardt. "Structure-aware transformer for
> graph representation learning." In ICML 2022.
> [2] Ying, Chengxuan, Tianle Cai, Shengjie Luo, Shuxin Zheng, Guolin Ke, Di He, Yanming
> Shen, and Tie-Yan Liu. "Do transformers really perform badly for graph representation?."
> In NeurIPS 2021.
> [3] Shirzad, Hamed, Ameya Velingker, Balaji Venkatachalam, Danica J. Sutherland, and Ali
> Kemal Sinop. "Exphormer: Sparse transformers for graphs." In ICML 2023.
> [4] Rampášek, Ladislav, Michael Galkin, Vijay Prakash Dwivedi, Anh Tuan Luu, Guy Wolf,
> and Dominique Beaini. "Recipe for a general, powerful, scalable graph transformer." In
> NeurIPS 2022.
> [5] Wu, Qitian, Wentao Zhao, Chenxiao Yang, Hengrui Zhang, Fan Nie, Haitian Jiang, Yatao
> Bian, and Junchi Yan. "Sgformer: Simplifying and empowering transformers for large-graph
> representations." In NeurIPS 2023.
>
> **Q1: Structural Encoding in Graph Transformer (20 pts)**
> Complete LapPETransformer() and SPDAttention() to implement graph Laplacian absolute
> structural encoding and shortest path distance-based relative structural encoding in graph
> transformer. You may refer to the demo in Section 4 for implementation ideas.
>
> **Q2: Efficient Graph Transformer (20 pts)**
> Complete SparseSPDAttention() to implement attention mask for sparse graph attention. You
> only need to specify the node pairs used for attention in your implementation. It is
> encouraged to test different masking strategies.

(Q3 is on the same page and belongs to a different worker. Do not answer it.)

## 2. The real question is in the notebook

Second input file, **read it**:
`/home/xing/project/auto_hw_complete/input/task6_graph_transformer-1.ipynb`

It is also ingested as plain text at
`INGEST/pages/task6_graph_transformer-1/alltext.txt` (22 cells; the notebook has no
stored outputs and no embedded images, so that text is the complete notebook).

"The demo in Section 4" that Q1 points you at is notebook cells 10-11:
`CentralityTransformer` (absolute encoding) and `CNAttention` (relative encoding). Read
them; they are the template for both of your Q1 classes.

Below are the question cells **verbatim**. The TODO cells are the signatures you must
match exactly — the framework calls them by name.
