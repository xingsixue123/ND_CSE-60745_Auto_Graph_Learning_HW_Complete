# Downloads and installs — master (job cse60745_20261016_024548)

One line per item: `- <name> | <how> | <path> | <why>`

- Python venv `.venv-gt` | `python3 -m venv .venv-gt` | `PLAYGROUND/.venv-gt` | shared runtime for all workers; nothing else on this box has torch+PyG+pandas+sklearn in one interpreter
- PyTorch 2.14.1+cpu | `PIP_CACHE_DIR=$PWD/.pipcache ./.venv-gt/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch` | `PLAYGROUND/.venv-gt` | the notebook is PyTorch; no GPU on this box, so the CPU wheel
- torch_geometric 2.8.1, pandas, scipy, scikit-learn (+ deps) | `PIP_CACHE_DIR=$PWD/.pipcache ./.venv-gt/bin/pip install torch_geometric pandas scipy scikit-learn` | `PLAYGROUND/.venv-gt` | imported by notebook cell 3 (ZINC dataset, f1_score, CSV loading, sparse linear algebra)
- pip cache | `PIP_CACHE_DIR=$PWD/.pipcache` | `PLAYGROUND/.pipcache` | `~/.cache/pip` is read-only in the sandbox
- ZINC (subset) dataset | `torch_geometric.datasets.ZINC("data/zinc", subset=True, ...)`, downloaded from dropbox/github as the notebook does | `PLAYGROUND/shared/data/zinc` | the dataset all three questions are evaluated on; pre-fetched once so workers copy instead of re-downloading
- LastFM Asia CSVs (`edges_all.csv`, `node_country.csv`, `country_split.csv`) | `urllib.request.urlretrieve` from `raw.githubusercontent.com/antman9914/CSE60745-Practice/main/...`, exactly the URLs in notebook cell 3 | `PLAYGROUND/shared/data/task2`, `PLAYGROUND/shared/data/task3` | Q2's large-graph benchmark
