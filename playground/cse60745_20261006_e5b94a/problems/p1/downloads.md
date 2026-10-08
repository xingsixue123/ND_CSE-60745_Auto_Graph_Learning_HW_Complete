# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`

- python venv | `python3 -m venv --system-site-packages .venv` | `./.venv` | isolated env; `--system-site-packages` reuses the preinstalled torch 2.13.0+cpu instead of a ~200 MB wheel
- torch_geometric 2.8.0.post1 | `PIP_CACHE_DIR=$PWD/.pipcache ./.venv/bin/pip install torch_geometric gensim pandas scikit-learn scipy matplotlib` | `./.venv/lib/python3.12/site-packages/torch_geometric` | `MessagePassing`, `degree`, `add_self_loops`, `remove_self_loops`, `softmax` — the whole assignment is built on it
- gensim 4.4.0 | same pip command | `./.venv/.../gensim` | notebook cell 6 builds the node2vec input features with `gensim.models.Word2Vec`
- pandas 3.0.6 | same pip command | `./.venv/.../pandas` | notebook `load_social()` and `evaluate_ranking()` are written in pandas
- scikit-learn 1.9.1 | same pip command | `./.venv/.../sklearn` | part of the master's recipe; not used directly by my code
- scipy 1.18.1 | same pip command | `./.venv/.../scipy` | gensim dependency
- matplotlib 3.11.2 | same pip command | `./.venv/.../matplotlib` | draws `fig_p1_depth.pdf`; base python3 has no matplotlib and the brief rules out the py311 env
- pip cache | side effect of the installs above | `./.pipcache` | `~/.cache/pip` is read-only, so `PIP_CACHE_DIR` was redirected into the playground
- matplotlib config dir | side effect of running matplotlib | `./run/.mplcache`, `./nbcheck/.mpl` | `~/.config/matplotlib` is read-only, so `MPLCONFIGDIR` was redirected into the playground
- LastFM Asia task-1 data (`split_stats.json`, `lp_graph_obs.csv`, `lp_train.csv`, `lp_val.csv`, `lp_test.csv`) | `urllib.request.urlretrieve` from `https://raw.githubusercontent.com/antman9914/CSE60745-Practice/main/data/task1/`, by `run/common.py` | `./run/data/task1/` | the graph and the three query splits the whole problem is evaluated on
- the same task-1 files, second copy | downloaded again by the notebook's own unmodified setup cell during the end-to-end notebook check | `./nbcheck/data/task1/` | the completed notebook was executed in its own directory to prove it runs
- task-3 data (`hetero_stats.json`, `user_artist.csv.gz`, 7.9 MB) | downloaded by the notebook's unmodified setup cell, which fetches both task1 and task3 | `./nbcheck/data/task3/` | NOT used by me — Q4's data. It arrives only because I ran the notebook's setup cell verbatim rather than editing it
- cached node2vec features | computed once by `run/common.py`, saved with `torch.save` | `./run/cache/x_node2vec.pt` | gensim's `Word2Vec(workers=4)` is non-deterministic, so the features are computed once and reused, keeping every reported row on identical inputs
- Li, Han & Wu (AAAI 2018) PDF | `WebFetch` of `https://arxiv.org/pdf/1801.07606`, text extracted with pymupdf to `run/logs/li2018.txt` | `./.claudecfg/projects/.../tool-results/webfetch-*.pdf` | to read Theorem 1 and the proposed remedies in full before citing them (rule R9)
