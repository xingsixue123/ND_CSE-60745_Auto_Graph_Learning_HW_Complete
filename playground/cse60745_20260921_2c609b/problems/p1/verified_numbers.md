# Verified numbers used in answer.tex

Two provenance classes:
- **[C]** computed here by loading the graph (`stats.py`, `stats_reddit.py`, `homophily.py`).
- **[O]** taken from the official OGB documentation (`research/ogb_nodeprop.txt`, `research/ogb_linkprop.txt`).
- **[P]** taken from the original paper PDF (`research/deepwalk.txt`, `research/node2vec.txt`).

`E_und` = distinct unordered pairs (self-loops excluded from the homophily count);
`E_dir` = number of columns in PyG's `edge_index` (an undirected edge appears twice).

## Node-classification benchmarks — [C] from `stats_out.json`

`h_edge` columns are over **distinct unordered pairs** (denominator = `E_und`), which is the
convention Table 1 states and uses.

| dataset | N | E_und | E_dir | d | feat | C | undirected | h_edge (incl. loops) | h_edge (excl. loops) | self-loops |
|---|---|---|---|---|---|---|---|---|---|---|
| Cora | 2,708 | 5,278 | 10,556 | 1,433 | binary | 7 | yes | 0.810 | 0.810 | 0 |
| CiteSeer | 3,327 | 4,552 | 9,104 | 3,703 | binary | 6 | yes | 0.736 | 0.736 | 0 |
| PubMed | 19,717 | 44,324 | 88,648 | 500 | real (TF-IDF) | 3 | yes | 0.802 | 0.802 | 0 |
| Coauthor CS | 18,333 | 81,894 | 163,788 | 6,805 | binary | 15 | yes | 0.808 | 0.808 | 0 |
| Coauthor Physics | 34,493 | 247,962 | 495,924 | 8,415 | binary | 5 | yes | 0.931 | 0.931 | 0 |
| Amazon Computers | 13,752 | 245,861 | 491,722 | 767 | binary | 10 | yes | 0.777 | 0.777 | 0 |
| Amazon Photo | 7,650 | 119,081 | 238,162 | 745 | binary | 8 | yes | 0.827 | 0.827 | 0 |
| Cornell | 183 | 280 | 298 | 1,703 | binary | 5 | **no** | 0.132 | 0.123 | 3 |
| Texas | 183 | 295 | 325 | 1,703 | binary | 5 | **no** | 0.112 | 0.061 | 16 |
| Wisconsin | 251 | 466 | 515 | 1,703 | binary | 5 | **no** | 0.206 | 0.178 | 16 |
| Actor | 7,600 | 26,752 | 30,019 | 932 | binary | 5 | **no** | 0.219 | 0.217 | 93 |
| Chameleon | 2,277 | 31,421 | 36,101 | 2,325 | binary | 5 | **no** | 0.231 | 0.230 | 50 |
| Squirrel | 5,201 | 198,493 | 217,073 | 2,089 | binary | 5 | **no** | 0.223 | 0.222 | 140 |
| Reddit | 232,965 | 57,307,946 | 114,615,892 | 602 | real | 41 | yes | — | — | 0 |
| Flickr (GraphSAINT) | 89,250 | 449,878 | 899,756 | 500 | real | 7 | yes | — | — | 0 |
| BlogCatalog (attributed) | 5,196 | 171,743 | 343,486 | 8,189 | binary | 6 | yes | — | — | 0 |
| PPI (GraphSAGE, 24 graphs) | 56,944 | 793,632 | 1,587,264 | 50 | real | 121 (multi-label) | yes | — | — | — |

### Homophily convention (fixed over rounds 1 and 2)

Two independent choices are involved, and I got each wrong once:

- **Round 1 defect — self-loops.** I excluded them; the published convention (Zhu et al.,
  NeurIPS 2020) includes them. A self-loop trivially satisfies $y_u=y_v$.
- **Round 2 defect — which edge set.** Having fixed self-loops, I was still computing over
  `data.edge_index` (stored *directed* entries: 298/325/515/30,019/36,101/217,073) while the
  `|E|` column counts distinct unordered pairs (280/295/466/26,752/31,421/198,493) — and the
  caption claimed they were the same set. Computing over directed entries weights a
  reciprocated arc twice as heavily as a one-way arc, which only matters for the six
  directed graphs.

**Now: edge homophily over distinct unordered pairs, self-loops included** — so the
denominator of $h$ is literally the `|E|` column. `homophily.py` prints `#pairs`, which can
be checked against `E_und` above row by row.

| dataset | mine (pairs, incl. loops) | Zhu et al. | agrees at 2 d.p.? |
|---|---|---|---|
| Cora | 0.810 | 0.81 | yes |
| CiteSeer | 0.736 | 0.74 | yes |
| PubMed | 0.802 | 0.80 | yes |
| Texas | 0.112 | 0.11 | yes |
| Wisconsin | 0.206 | 0.21 | yes |
| Actor | 0.219 | 0.22 | yes |
| Chameleon | 0.231 | 0.23 | yes |
| Squirrel | 0.223 | 0.22 | yes |
| **Cornell** | **0.132** | **0.30** | **NO** |

Under the corrected convention **8 of 9 match the published values exactly at two decimal
places** (previously Wisconsin printed 0.20 vs published 0.21, and Chameleon 0.24 vs 0.23).
Summed deviation across the five reproducible heterophilous datasets drops from 0.0264
(directed entries) to 0.0102 (unordered pairs) — the stated convention is also the more
faithful one. This additionally explains the "unchased Wisconsin residual" I flagged in
round 2: it was the edge-set bug, not noise.

**Cornell does not reproduce under any definition I tried** (`cornell_probe.py`):
over unordered pairs 0.132, the same excluding self-loops 0.123, over stored directed
entries 0.131, node homophily (Pei et al.) 0.186 — none is near 0.30. I report my measured
0.13, dagger it in Table 1, and footnote the discrepancy rather than printing a number I
cannot reproduce.

**Note the `|E|` convention:** `E_und` counts distinct unordered pairs *including*
self-loops (counted once). This is what makes Cornell 280 (= 277 + 3) and Texas 295
(= 279 + 16) match Zhu et al.'s published `|E|`. Both the `|E|` and `h_edge` columns of
Table 1 therefore now use the same self-loop-inclusive convention.

**Directedness:** the six WebKB/Actor/Wikipedia graphs have a **non-symmetric** stored
`edge_index` (verified by the symmetry test in `stats.py`), which is exactly why their
`E_dir` is not twice `E_und`. All other graphs listed are undirected.

**Invariant check on Reddit.** The GraphSAGE paper states an average degree of 492.
`2 * 57,307,946 / 232,965 = 492.0`. The computed edge count reproduces the paper's own
average degree, which is an independent confirmation that 57.3M (not the 11.6M that
circulates on some dataset pages) is the right undirected edge count for this copy.

**Cora edge count.** The frequently quoted 5,429 is the number of lines in the original
`cora.cites` file, which contains duplicate and self-referential entries. After
de-duplication and symmetrisation PyG reports 10,556 directed entries = **5,278**
distinct undirected edges. All three figures (5,429 / 5,278 / 10,556) therefore refer to
the same graph; the answer footnotes this.

## Name collisions — different graphs sharing one name [P]

- **BlogCatalog**: DeepWalk/node2vec version = 10,312 nodes, 333,983 edges, 39 multi-labels,
  *no node features*. The attributed version loaded by PyG = 5,196 / 171,743 / 8,189 feats / 6 classes.
- **Flickr**: DeepWalk version = 80,513 nodes, 5,899,882 edges, 195 groups, no features.
  GraphSAINT version (PyG `Flickr`) = 89,250 / 449,878 / 500 feats / 7 classes.
- **PPI**: node2vec H.-sapiens subgraph = 3,890 nodes, 76,584 edges, 50 labels.
  GraphSAGE inductive PPI = 24 graphs, 56,944 nodes, 793,632 edges, 50 feats, 121 labels.
- YouTube [P, DeepWalk Table 1] = 1,138,499 nodes, 2,990,443 edges, 47 groups.
- node2vec Wikipedia word co-occurrence [P] = 4,777 nodes, 184,812 edges, 40 labels.

## OGB node property prediction [O]

| dataset | N | E | d | C | dir | split | metric |
|---|---|---|---|---|---|---|---|
| ogbn-arxiv | 169,343 | 1,166,243 | 128 (avg. word2vec) | 40 | directed | time (<=2017 / 2018 / >=2019) | Accuracy |
| ogbn-products | 2,449,029 | 61,859,140 | 100 (BoW + PCA) | 47 | undirected | sales rank | Accuracy |
| ogbn-papers100M | 111,059,956 | 1,615,685,872 | 128 | 172 | directed | time | Accuracy |
| ogbn-proteins | 132,534 | 39,561,252 | no node feats; 8-dim edge feats | 112 binary tasks | undirected | species | ROC-AUC |

## OGB link property prediction [O]

| dataset | N | E | d | split | metric | negatives |
|---|---|---|---|---|---|---|
| ogbl-collab | 235,868 | 1,285,465 | 128 | time (<=2017 / 2018 / 2019) | Hits@50 | 100,000 shared |
| ogbl-ppa | 576,289 | 30,326,273 | 58-dim one-hot species | throughput | Hits@100 | 3,000,000 shared |
| ogbl-citation2 | 2,927,963 | 30,561,187 | 128 word2vec | time | MRR | 1,000 per source node |
| ogbl-ddi | 4,267 | 1,334,889 | none | protein-target | Hits@20 | ~100,000 shared |

OGB footnote (verbatim): "For undirected graphs, the loaded graphs will have the doubled
number of edges because we add the bidirectional edges automatically." So the counts above
are undirected edge counts for the undirected datasets.
