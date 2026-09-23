# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`

All installs live inside PLAYGROUND (`.venv/`, `data/`, `research/`) and can be removed
by deleting those three directories.

- python venv | `python3 -m venv .venv` | `PLAYGROUND/.venv` | isolated interpreter so `pip` works (base conda env is read-only)
- torch 2.14.0+cpu | `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu` | `PLAYGROUND/.venv` | required by torch_geometric
- torch_geometric 2.8.0.post1 | `.venv/bin/pip install torch_geometric` | `PLAYGROUND/.venv` | load the benchmark graphs and compute their true statistics rather than quoting numbers from memory
- scipy 1.18.1 | `.venv/bin/pip install scipy` | `PLAYGROUND/.venv` | required by the PyG loaders for Planetoid / Coauthor / Amazon / Flickr
- pandas 3.0.6 | `.venv/bin/pip install pandas` | `PLAYGROUND/.venv` | required by PyG's `AttributedGraphDataset` (BlogCatalog)
- PyG benchmark datasets | auto-downloaded by `stats.py` and `homophily.py` | `PLAYGROUND/data/` | Planetoid (Cora/CiteSeer/PubMed), WebKB, Actor, WikipediaNetwork, Coauthor, Amazon, AttributedGraphDataset, Flickr, PPI — source of the statistics table and the homophily numbers
- Reddit dataset (GraphSAGE) | auto-downloaded by `stats_reddit.py` | `PLAYGROUND/data/Reddit` | ~1.5 GB; used to verify Reddit's node/edge/feature/class counts
- OGB documentation pages | `curl https://ogb.stanford.edu/docs/nodeprop/` and `.../linkprop/` | `PLAYGROUND/research/ogb_*.html` | authoritative OGB statistics, split protocols and metrics (the OGB graphs are far too large to download here)
- PyG dataset cheatsheet | `curl https://pytorch-geometric.readthedocs.io/en/latest/cheatsheet/data_cheatsheet.html` | `PLAYGROUND/research/pyg_cheatsheet.html` | intended cross-check; it is explicitly incomplete, so I loaded the datasets instead
- DeepWalk and node2vec PDFs | `curl https://arxiv.org/pdf/1403.6652` and `https://arxiv.org/pdf/1607.00653` | `PLAYGROUND/research/*.pdf` | primary source for the BlogCatalog / Flickr / YouTube / PPI-subgraph statistics quoted in the answer
