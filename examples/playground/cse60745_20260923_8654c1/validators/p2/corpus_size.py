"""Exact Skip-Gram corpus size (tokens, not walks) for every configuration.

The write-up matches the walk-budget control to Task 4 by WALK COUNT
("153,076 vs 152,930, within 0.1%").  Skip-Gram consumes tokens.  Meta-path walks
dead-end whenever the next required type is absent, so walk count != corpus size.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scaffold import load_data, typed_adjacency
from impl import WalkEmbedding
from hetero import MetaPathWalkEmbedding

G, splits, country, country_split, N = load_data()
h = json.loads(Path("data/task3/hetero_stats.json").read_text())
ua = pd.read_csv("data/task3/user_artist.csv.gz")
H = G.copy()
H.add_nodes_from(range(N, N + h["n_artists"]), type="A")
H.add_edges_from(ua.itertuples(index=False, name=None))
typed_adjacency(H)

BASE = dict(num_walks=10, walk_length=40, dim=128, window=5, negative=5, epochs=5)

CFG = [
    ("Task3 DeepWalk x10 (G)", WalkEmbedding(seed=0, strategy="uniform", **BASE), G),
    ("CONTROL DeepWalk x22 (G)",
     WalkEmbedding(seed=0, strategy="uniform",
                   **{**BASE, "num_walks": 22}), G),
    ("type-blind DeepWalk (H)", WalkEmbedding(seed=0, strategy="uniform", **BASE), H),
    ("metapath U-A-U", MetaPathWalkEmbedding(schema="UAU", seed=0, **BASE), H),
    ("metapath U-U-A-U", MetaPathWalkEmbedding(schema="UUAU", seed=0, **BASE), H),
    ("metapath U-U-U-A-U", MetaPathWalkEmbedding(schema="UUUAU", seed=0, **BASE), H),
    ("U-A-U rare alpha=1", MetaPathWalkEmbedding(schema="UAU", alpha=1.0, seed=0, **BASE), H),
]

print(f"{'config':28s} {'walks':>10s} {'tokens':>12s} {'mean len':>9s} {'%len40':>7s}")
rows = {}
for name, emb, graph in CFG:
    nw = 0
    ntok = 0
    nfull = 0
    for s in graph.nodes():
        for w in emb.sample_walks(graph, s):
            nw += 1
            ntok += len(w)
            nfull += (len(w) == 40)
    rows[name] = (nw, ntok)
    print(f"{name:28s} {nw:10,d} {ntok:12,d} {ntok/nw:9.1f} {100*nfull/nw:6.1f}%")

print()
ctl = rows["CONTROL DeepWalk x22 (G)"]
for name, (nw, ntok) in rows.items():
    print(f"{name:28s} walks vs control {100*nw/ctl[0]-100:+6.1f}%   "
          f"tokens vs control {100*ntok/ctl[1]-100:+6.1f}%")
