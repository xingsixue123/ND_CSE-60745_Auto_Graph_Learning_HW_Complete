"""How often does a TYPE-BLIND uniform walk on H take a social (U-U) step?

The answer justifies the claim in the analysis that a type-blind DeepWalk on H is
"de facto U-A-U": a user has ~395 artist neighbours and ~5 social ones, so uniform
neighbour choice almost never uses the sparse, informative edge type.

    ../../venv/bin/python typeblind_steps.py
"""
import collections
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scaffold import load_data, typed_adjacency
from impl import WalkEmbedding

G, splits, country, country_split, N = load_data()
h = json.loads(Path("data/task3/hetero_stats.json").read_text())
ua = pd.read_csv("data/task3/user_artist.csv.gz")
H = G.copy()
H.add_nodes_from(range(N, N + h["n_artists"]), type="A")
H.add_edges_from(ua.itertuples(index=False, name=None))
_, ntype = typed_adjacency(H)

e = WalkEmbedding(seed=0, strategy="uniform", num_walks=2, walk_length=40)
rng = np.random.default_rng(0)
probe = [int(x) for x in rng.choice(N, 400, replace=False)]

cnt = collections.Counter()
for s in probe:
    for w in e.sample_walks(H, s):
        for a, b in zip(w, w[1:]):
            cnt[ntype[a] + ntype[b]] += 1

tot = sum(cnt.values())
print(f"type-blind uniform walk on H, {tot:,} sampled steps from {len(probe)} users")
print(f"  step type counts: {dict(cnt)}")
print(f"  social U-U fraction = {cnt['UU']/tot:.4f}  ({100*cnt['UU']/tot:.2f}%)")
