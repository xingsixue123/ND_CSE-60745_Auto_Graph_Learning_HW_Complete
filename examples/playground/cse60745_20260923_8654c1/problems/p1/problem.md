# p1 — Task 3: Graph Embedding over Homogeneous Structures (HW2-Part(B), Practice I, 30 pts)

Your problem id is **p1**. Every LaTeX label, figure filename and macro you define must
be namespaced with `p1:` / `fig_p1_` (rule R5).

---

## 0. Where this question lives

The assignment is delivered in two pieces, and **the notebook is the authoritative one**:

- Slide deck `input/CSE60745-Hands-on_HW2-Part(B)-1.pdf`, **rendered pages 7, 8, 9**.
  Rendered page 7 is the divider slide: `HW2-Part(B): 30 pts` / `Practice I: Graph
  Embedding Over Homogeneous Structures`. Page 8 is the task statement, page 9 is a
  pipeline diagram.
  Ingested copies:
  `/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/ingest/pages/CSE60745-Hands-on_HW2-Part(B)-1/page_008.png`
  and `page_009.png`, with the embedded figures at native resolution as
  `page_008_fig_02.jpeg`, `page_009_fig_02.jpeg`, `page_009_fig_03.jpeg`,
  `page_009_fig_04.jpeg`.
  **I have already read those figures.** They are *illustrative recaps only* — a toy
  7-node graph A..G with a numbered walk, a "Walk 1..Walk 5" table of node sequences,
  and a block diagram (hand-crafted features vs. `sample_walks()` → Skip-Gram
  `train_embedding()` → dot product / classifier). They contain **no data and no
  parameter values you must reproduce.** You do not need to redraw them. Look at them
  if you want the intuition; do not invent requirements from them.

- Jupyter notebook **`/home/xing/project/auto_hw_complete/input/graph_embedding-1.ipynb`**
  — READ THIS FILE IN FULL, FIRST. It contains the actual problem definition, the exact
  interfaces you must implement, the provided scaffolding you must not change, and the
  evaluation code that defines the metrics. `specs.md` says explicitly: *"I think it is
  the instruction where real hw guideline and problem definitions are in the jupyter
  notebook"*.

Your scope is **Task 3 only** (notebook sections 1–6). Task 4 (heterogeneous /
metapath2vec, notebook sections 7–8) is a separate problem, p2 — do not do it.

---

## 1. Question text, transcribed from the notebook (section headers verbatim)

> # Task 3 — Graph Embedding Applications
>
> **Dataset.** LastFM Asia social network: 7,624 users from Asian countries, 27,806
> mutual-follower edges ([Last.FM Asia](https://snap.stanford.edu/data/feather-lastfm-social.html)).
>
> **Your job.** Learn user node embeddings from random walks, then use it for two
> downstream tasks and find out the contributions of different random walk sampling
> strategies:
>
> 1. **Friend recommendation** — exactly the Practice 1 problem: same 70/15/15 edge
>    split, same queries, same evaluation pipeline. Dataset statistics:
>
>    | split | queries | positives : negatives |
>    |-------|---------|-----------------------|
>    | train | 19,464  | 1 : 5                 |
>    | val   | 4,171   | 1 : 20                |
>    | test  | 4,171   | 1 : 20                |
>
> 2. **Country classification** — predict a user's country (18 classes) from the
>    embedding. The users are split **10% train / 10% val / 80% test**, stratified by
>    country.
>
>    | split | users |
>    |-------|-------|
>    | train | 763   |
>    | val   | 763   |
>    | test  | 6,098 |
>
> **What you implement.** Three interfaces for random walk based graph embedding:
>
> | interface | section | what it does |
> |---|---|---|
> | `sample_walks(G, start)` | 3 | given a graph and a start node, return a set of random walks |
> | `train_embedding(walks, n_nodes)` | 3 | turn the walks into an `(n_nodes, d)` node embedding matrix |
> | `LinkPredictor` / `CountryClassifier` | 4 | how the embedding is used for downstream ML model |
>
> You can try to reproduce DeepWalk and node2vec, and then test other random walk based
> embedding methods, including your own ideas. Please run the cells sequentially in
> Google Colab, and don't modify other parts of the code unless necessary.

> ## 3. Your implementation — graph embedding
> Two methods. `sample_walks` is where random walk sampling strategy is implemented.
> `train_embedding` updates node embedding matrix.

> ## 4. Your implementation — downstream models
> `LinkPredictor` receives the embedding matrix and the candidate pairs directly. How a
> pair `(u, v)` is turned into a feature vector from `Z[u]` and `Z[v]` is part of what
> you design inside `fit` and `score`: the node2vec paper compares average, Hadamard
> (element-wise product), absolute difference and squared difference, and nothing stops
> you from concatenating several or adding Task 1 structural features next to them.
>
> `CountryClassifier` is an ordinary node classifier on top of the embedding.
>
> **Keep both of these fixed while you compare sampling strategies in sections 7 and 8.**
> The comparison is only meaningful if the embedding is the one thing that changes.

> ## 6. Sampling Strategy Comparison
> Record every strategy with `run_experiment` under a distinct name and look at
> `comparison_table()`. The question is not only which strategy is best overall but
> which downstream task each one helps, and whether the same embedding is best for
> both.

The exact docstrings of the four TODOs (argument shapes, return shapes, the assertion
that `score` must return continuous scores with higher = more likely) are in the
notebook. **Read them there; obey the shapes exactly.** In particular:

- `sample_walks(self, G, start)` → list of lists of int, each starting with `start`;
  the framework calls it once per node of G. Returning `[]` is allowed.
- `train_embedding(self, walks, n_nodes)` → `(n_nodes, d)` float ndarray; nodes absent
  from every walk still need a row (zeros).
- `LinkPredictor.fit(Z, pairs_train, y_train, pairs_val, y_val)`;
  `pairs_train` is `(19464, 6, 2)` with the **positive always at index 0** along axis 1;
  `pairs_val` is `(4171, 21, 2)` with the positive at an unknown position.
  `LinkPredictor.score(Z, pairs)` → `(n_queries, n_candidates)` continuous scores.
- `CountryClassifier.fit(Z_train, y_train, Z_val, y_val)` with `Z_train` `(763, d)`;
  `CountryClassifier.predict(Z)` → `(n,)` predicted country ids.

---

## 2. What you must actually do

1. **Implement all four TODOs** (TODO 1 `sample_walks`, TODO 2 `train_embedding`,
   TODO 3a `LinkPredictor`, TODO 3b `CountryClassifier`) so that the notebook's
   provided `run_experiment` / `comparison_table` machinery runs end to end.
2. **Actually run it.** This is not a paper exercise — the deliverable must contain real
   measured numbers produced on this machine, not plausible-looking invented ones. A
   table of numbers you did not compute is the worst possible failure here.
3. **Reproduce DeepWalk** (uniform random walk) and **node2vec** (2nd-order biased walk
   with return parameter *p* and in-out parameter *q*). Run node2vec at more than one
   (p, q) setting if you can afford it — the contrast between homophily-leaning (q<1)
   and structural-equivalence-leaning (q>1) walks is exactly the "which strategy helps
   which task" question section 6 asks.
4. **Add at least one sampling strategy of your own** and say what hypothesis it tests
   (e.g. degree-biased / weighted-by-common-neighbours next-step selection, restart
   walks, walk-length or walks-per-node ablation, mixing walk lengths, ...). It does not
   have to win; it has to be motivated and measured.
5. **Hold `LinkPredictor` and `CountryClassifier` fixed across every strategy** — the
   notebook demands this. Say so in the write-up.
6. Report, for every strategy: link-prediction **Hit@1 and MRR on val and test**, the
   **per-source-degree Hit@1/MRR breakdown** that `breakdown_by_source_degree` produces
   (bins `[0,1) [1,2) [2,4) [4,8) [8,16) [16,inf)`), and country classification
   **micro-F1 / macro-F1 on val and test**.
7. **Analyse.** Which strategy wins friend recommendation, which wins country
   classification, is it the same one, and why (homophily vs. structural equivalence;
   the 666 isolated / cold-start users in the observed graph; macro-F1 vs micro-F1 on an
   imbalanced 18-class label). The analysis is a large part of the marks — a table with
   no interpretation is a weak answer.

---

## 3. Data — already downloaded for you, do not re-download

The notebook's setup cell fetches the data from GitHub. **I have already fetched it.**
It is at:

```
/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/data/
    task1/split_stats.json      task1/lp_graph_obs.csv
    task1/lp_train.csv          task1/lp_val.csv       task1/lp_test.csv
    task2/node_country.csv
    task3/country_split.csv     task3/hetero_stats.json  task3/user_artist.csv.gz
```

That directory is **outside your playground and is read-only**. Either point
`Path("data/...")` at it via a symlink inside your own playground, or copy it in — do
not try to write there. (Task 3 needs task1 + task2 + `task3/country_split.csv` only.)

Verified ground truth from `split_stats.json`, use it to sanity-check your loading:
`n_nodes = 7624`, full graph `27806` edges, observed training graph `19464` edges,
`666` isolated nodes, mean degree `5.106`, max degree `153`, `734` connected
components; val/test have `4171` queries × 21 candidates, of which ~5.1% are
cold-start.

## 4. Environment — already set up for you, do not reinstall

A venv with everything you need already exists and is **read-only to you but runnable**:

```
/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/venv/bin/python
```

It has gensim 4.4.0, numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.1, pandas,
networkx 3.6.1, matplotlib. Use `gensim.models.Word2Vec(..., sg=1)` for the Skip-Gram —
the notebook says "You can use gensim to implement SkipGram". Set `MPLCONFIGDIR` to a
dir inside your playground before importing matplotlib, or it warns.

The machine has 32 cores and ~114 GB free RAM; `Word2Vec(workers=16)` is fine.
If you need a package that is not there, make your **own** venv inside your playground
and append it to
`/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/downloads.md`
(rule R3) — but you almost certainly do not need to.

Work in a plain `.py` script in your playground, not a notebook; you are reproducing
the notebook's cells, not required to deliver one. Do **not** change the provided
scaffolding (`load_data`, `adjacency_lookups`, `typed_adjacency`, `evaluate_ranking`,
`breakdown_by_source_degree`, `to_query_tensor`, `flatten_scores`, `embed_graph`,
`evaluate_link_prediction`, `evaluate_country`, `run_experiment`, `comparison_table`) —
copy them verbatim out of the notebook. Keep `RANDOM_SEED = 0`.

Budget note: DeepWalk with 10 walks × length 40 from each of 7,624 nodes is ~76k walks
and trains in well under a minute; a plain second-order node2vec sampler in Python is
the slow part. Precompute the alias/transition structure or keep the neighbour sets in
`adjacency_lookups(G)` rather than recomputing per step. Budget a few minutes per
strategy, not hours. If a strategy is genuinely too slow, reduce walks-per-node and
say so rather than silently changing the protocol between strategies.

---

## 5. Deliverable

Write `answer.tex` into your OUTPUT directory as a **LaTeX fragment** — no
`\documentclass`, no `\begin{document}`, no `\usepackage` (those go one per line in
`preamble.txt`). It starts at `\section{...}` level. It is a **homework submission,
not a lab notebook**.

It should contain, roughly in this order:

1. A short statement of the approach: what `sample_walks` does for each strategy, what
   `train_embedding` does (Skip-Gram hyper-parameters: dimension, window, negative
   samples, epochs), how a pair `(u,v)` becomes a feature vector in `LinkPredictor`,
   and what classifier `CountryClassifier` uses. State the fixed hyper-parameters in a
   small table so the runs are reproducible.
2. **Compact code listings of the four implemented interfaces only** (`sample_walks`,
   `train_embedding`, `LinkPredictor`, `CountryClassifier`). Use `lstlisting` or
   `verbatim`. Do **not** paste the provided scaffolding, the data loading, the
   evaluation toolset, or any debugging output. If a listing runs long, show the method
   bodies and elide boilerplate with a comment. This is a coding assignment, so the
   grader does want to see the implementation — but only the part you wrote.
3. The **comparison table** (one row per strategy, the columns `comparison_table()`
   produces), as a real LaTeX `tabular`/`booktabs` table, not a pasted pandas repr.
4. The **per-source-degree breakdown** for at least the best strategy and the baseline,
   and a figure if it helps (a grouped bar chart of Hit@1 by degree bucket, or a
   strategy-vs-metric plot). Any figure must be a **vector PDF** named
   `fig_p1_<something>.pdf` in your OUTPUT dir, included by **bare filename**.
   Generate it with the venv's matplotlib.
5. The **analysis** asked for in section 6 — which strategy helps which task, whether
   one embedding is best for both, and why. Be concrete and reference your numbers.

Every number in the write-up must come from a run you actually performed. If something
did not converge or you had to cut a strategy for time, say so explicitly — an honest
negative result is worth marks; a fabricated table is worth none.

Namespace everything: `\label{p1:tab:comparison}`, `fig_p1_degree.pdf`, etc.
Keep the fragment focused; a good answer here is a few pages, not fifteen.
