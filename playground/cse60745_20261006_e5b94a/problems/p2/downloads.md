# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`

- venv (python3.12, --system-site-packages) | `python3 -m venv --system-site-packages .venv` | `.venv/` | isolated interpreter; reuses the preinstalled torch 2.13.0+cpu instead of a 200 MB wheel
- torch_geometric 2.8.0.post1 | `PIP_CACHE_DIR=$PWD/.pipcache ./.venv/bin/pip install torch_geometric` | `.venv/lib/python3.12/site-packages/torch_geometric` | `MessagePassing` base class the question is built on
- gensim 4.4.0 | same pip command | `.venv/.../gensim` | `Word2Vec` / SkipGram for notebook cell 26's metapath2vec features
- pandas 3.0.6 | same pip command | `.venv/.../pandas` | notebook cells 5, 11, 25 read CSVs and group with pandas
- scikit-learn 1.9.1 | same pip command | `.venv/.../sklearn` | listed in the master's verified recipe; pulled in for parity (not used directly by my cells)
- scipy 1.18.1 | same pip command | `.venv/.../scipy` | gensim / sklearn dependency
- pip wheel cache | created by the installs above | `.pipcache/` | `~/.cache/pip` is read-only (rule R3 / env.md)
- data/task1/{split_stats.json,lp_graph_obs.csv,lp_train.csv,lp_val.csv,lp_test.csv} | downloaded by notebook cell 3 from `https://raw.githubusercontent.com/antman9914/CSE60745-Practice/main/` | `run/data/task1/` | the LastFM-Asia social graph and the three query splits
- data/task3/{hetero_stats.json,user_artist.csv.gz} | same, notebook cell 3 | `run/data/task3/` | the user-artist bipartite graph (3,014,361 rows) that supplies relations 1 and 2
- R-GCN paper (Schlichtkrull et al., arXiv:1703.06103v4) | `curl -sL -o refs/rgcn_1703.06103.pdf https://arxiv.org/pdf/1703.06103v4` | `refs/rgcn_1703.06103.pdf` | rule R9: read Eq. (2), section 2.2 and section 5.2 in context before characterising what the paper says about $c_{i,r}$ and about the basis / block decompositions
