# Problem p2 — Q3 Hybrid Graph Transformer (30 pts)

**Problem id: `p2`.** Namespace every LaTeX label, every figure filename and every macro
you define with `p2:` / `fig_p2_` (rule R5 below).

---

## 1. Where this comes from

Assignment document: `/home/xing/project/auto_hw_complete/input/CSE 60745_Fall 2026_HW3(B).doc`

Ingested at `INGEST/pages/CSE 60745_Fall 2026_HW3(B)/` — **rendered page 2** (page 1 is
the cover page). Anchor text: `Q3: Hybrid Graph Transformer (30 pts)`.

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
> **Q3: Hybrid Graph Transformer (30 pts)**
> Complete HybridGTLayer() to implement a hybrid graph transformer composed of both
> MPNN-based local attention and transformer-based global attention. You can implement
> GraphGPS or design your own hybrid structures.

(Q1 and Q2 are on the same page and belong to a different worker. Do not answer them.)

Reference [4], Rampášek et al., "Recipe for a general, powerful, scalable graph
transformer" (NeurIPS 2022), is the GraphGPS paper the question names. If you build an
argument on what it says, read the surrounding passage, not just the sentence you quote
(rule R9 below).

## 2. The real question is in the notebook

Second input file, **read it**:
`/home/xing/project/auto_hw_complete/input/task6_graph_transformer-1.ipynb`

It is also ingested as plain text at
`INGEST/pages/task6_graph_transformer-1/alltext.txt` (22 cells; the notebook has no
stored outputs and no embedded images, so that text is the complete notebook).

Read cells 6-11 as well as the three below: cell 8 defines `Attention`,
`TransformerBlock`, `GraphTransformer` and `graph_mean_pool`; cell 9 defines
`run_graph_task`; cell 11 is the demo. They are the conventions your layer lives inside.

Below are the question cells **verbatim**. Cell 21 is the signature you must match
exactly, and cell 22 is the driver that will call it.
