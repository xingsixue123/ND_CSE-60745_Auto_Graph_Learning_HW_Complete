# p1 — notes / plan

## Sources read (R7)
- `problem.md` (master's brief).
- `input/graph_embedding-1.ipynb` — read in full. This is the authoritative problem
  definition. Scope = Task 3 = notebook sections 1–6.
- Slide deck rendered pages 8 and 9, all three channels:
  - `page_008.txt`, `page_008.png`, `page_008_fig_02.jpeg`
  - `page_009.txt`, `page_009.png`, `page_009_fig_02/03/04.jpeg`
  Page 8 is the "Recap: Random Walk-Based Graph Embedding" slide (DeepWalk / node2vec /
  struct2vec) plus the two downstream tasks. Page 9 is the pipeline block diagram with
  the toy "Walk 1..Walk 5" table and a heatmap standing in for the embedding matrix.
  **Confirmed: the figures carry no data and no parameter values.** The brief and the
  page agree; no discrepancy found. The only extra thing the slide adds over the
  notebook is the mention of struct2vec and the encouragement to "first re-implement
  DeepWalk/Node2Vec, and then test your own ideas".

## What this problem needs
- **code** — mandatory. Every number in the answer must be measured. Implement the
  four TODOs, run `run_experiment` for several sampling strategies.
- **diagram** — yes. The per-source-degree breakdown is naturally a grouped bar chart,
  and the brief asks for a vector PDF. Also a strategy-vs-metric scatter showing the
  link-prediction / country-classification trade-off.
- **plain** — yes, a substantial analysis section (large part of the marks).

## Design decisions (fixed once, held constant across strategies)
- Walk budget: `num_walks = 10`, `walk_length = 40`, identical for every strategy.
  Only the *transition rule* changes between strategies. This is what makes the
  comparison in section 6 meaningful.
- `train_embedding`: gensim `Word2Vec(sg=1, vector_size=128, window=5, negative=5,
  epochs=5, min_count=0, sample=0, seed=0, workers=1)`.
  `sample=0` (no frequent-token subsampling) on purpose: subsampling would silently
  down-weight hubs and thereby half-implement the degree-corrected strategy below,
  muddying that comparison. `workers=1` for bit-exact reproducibility (gensim's
  multi-worker training is not deterministic).
- `LinkPredictor`: L2-normalise Z, feature = concat[hadamard(u,v), |u-v|, cos, dot,
  ||u-v||] -> 2d+3 = 259 dims, StandardScaler, LogisticRegression; C picked from
  {0.1, 1, 10} by **validation MRR**.
- `CountryClassifier`: L2-normalise Z, StandardScaler, multinomial LogisticRegression;
  C picked from {0.1, 1, 10, 100} by **validation micro-F1**.
  Both downstream models are identical code for every strategy (notebook demands it).

## Strategies
| name | transition rule | hypothesis |
|---|---|---|
| `deepwalk` | uniform over neighbours | baseline (DeepWalk) |
| `node2vec_p1_q0.5` | 2nd-order, p=1, q=0.5 | outward/BFS-ish, homophily-leaning |
| `node2vec_p1_q2` | 2nd-order, p=1, q=2 | inward, structural-equivalence-leaning |
| `node2vec_p0.25_q0.25` | 2nd-order, p=0.25, q=0.25 | low return prob, wide exploration |
| `rwr_0.15` | uniform, but restart at `start` w.p. 0.15 | personalised/local context should help LP, hurt global class structure |
| `degcorr_a1` | P(x) ∝ deg(x)^-1 | uniform walks over-visit hubs; equalising visits should lift the low-degree buckets |
| `triadic` | P(x) ∝ 1 + |N(cur) ∩ N(x)| | triangle-closing walk stays inside communities -> homophily -> should help both tasks |

`rwr`, `degcorr` and `triadic` are the "own ideas" required by item 4 of the brief.

## Ground truth to check loading against (split_stats.json)
n_nodes 7624, full 27806 edges, G_train 19464 edges, 666 isolated, mean deg 5.106,
max deg 153, 734 components; val/test 4171 x 21.
