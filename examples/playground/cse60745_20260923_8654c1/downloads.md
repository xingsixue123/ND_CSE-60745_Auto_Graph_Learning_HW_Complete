# Downloads / installs for job cse60745_20260923_8654c1

- venv (python 3.11, from ~/miniconda3/envs/py311) | `python -m venv venv` | `playground/cse60745_20260923_8654c1/venv` | shared interpreter for all workers
- gensim 4.4.0 | `PIP_CACHE_DIR=$PWD/.pipcache ./venv/bin/pip install gensim` | `playground/cse60745_20260923_8654c1/venv` | Word2Vec/SkipGram for `train_embedding`
- numpy 2.4.6, scipy 1.17.1, pandas, scikit-learn 1.9.1, networkx 3.6.1, matplotlib | same pip command | same venv | notebook dependencies (sklearn f1_score, nx graph, pandas splits) and plotting
- pip cache | `PIP_CACHE_DIR=$PWD/.pipcache` | `playground/cse60745_20260923_8654c1/.pipcache` | pip needs a writable cache dir
- LastFM-Asia task data (split_stats.json, lp_graph_obs.csv, lp_train/val/test.csv, node_country.csv, hetero_stats.json, user_artist.csv.gz, country_split.csv) | `urllib.request` from https://raw.githubusercontent.com/antman9914/CSE60745-Practice/main/... exactly as the notebook's setup cell does | `playground/cse60745_20260923_8654c1/problems/<pid>/data/` | the assignment dataset
