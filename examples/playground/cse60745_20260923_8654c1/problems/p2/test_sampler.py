"""Correctness gates for MetaPathWalkEmbedding, on a tiny hand-built graph and on H_train.

    ../../venv/bin/python test_sampler.py
"""
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from scaffold import load_data, typed_adjacency
from hetero import MetaPathWalkEmbedding

# ---------------------------------------------------------------- 1. toy graph
# users 0,1,2 ; artists 10,11.  social edges 0-1, 1-2 ; likes 0-10, 1-10, 2-11.
T = nx.Graph()
T.add_nodes_from([0, 1, 2], type="U")
T.add_nodes_from([10, 11], type="A")
T.add_edges_from([(0, 1), (1, 2), (0, 10), (1, 10), (2, 11)])
_, ntype = typed_adjacency(T)

for schema, expect_from_U, expect_from_A in [
        ("UAU",   "UAUAUAUA", "AUAUAUAU"),
        ("UUAU",  "UUAUUAUU", "AUUAUUAU"),
        ("UUUAU", "UUUAUUUA", "AUUUAUUU")]:
    e = MetaPathWalkEmbedding(schema=schema, num_walks=20, walk_length=8, seed=0)
    for start, expect in ((0, expect_from_U), (10, expect_from_A)):
        for w in e.sample_walks(T, start):
            got = "".join(ntype[v] for v in w)
            assert expect.startswith(got), f"{schema} from {start}: {got} !~ {expect}"
            for a, b in zip(w, w[1:]):
                assert T.has_edge(a, b), f"{schema}: {a}-{b} is not an edge"
    print(f"  toy {schema:6s}: type sequence and edge existence OK")

# a user with no artist must yield nothing under UAU.  NB: scaffold's typed_adjacency
# caches on id(G), so this needs a fresh graph object that stays alive, not a mutated T.
T2 = nx.Graph()
T2.add_nodes_from([0, 1, 3], type="U")
T2.add_nodes_from([10], type="A")
T2.add_edges_from([(0, 1), (3, 0), (0, 10), (1, 10)])
e = MetaPathWalkEmbedding(schema="UAU", num_walks=5, walk_length=8, seed=0)
assert e.sample_walks(T2, 3) == [], "user with no artist should give no U-A-U walk"
print("  toy UAU   : artist-less user correctly yields []")

# ---------------------------------------------------------------- 2. real H_train
G_train, splits, country, country_split, N_USERS = load_data()
hstats = json.loads(Path("data/task3/hetero_stats.json").read_text())
ua = pd.read_csv("data/task3/user_artist.csv.gz")
H = G_train.copy()
H.add_nodes_from(range(N_USERS, N_USERS + hstats["n_artists"]), type="A")
H.add_edges_from(ua.itertuples(index=False, name=None))
_, ntypeH = typed_adjacency(H)

rng = np.random.default_rng(0)
probe = list(rng.choice(N_USERS, 300, replace=False)) + \
        list(rng.choice(range(N_USERS, N_USERS + hstats["n_artists"]), 100, replace=False))

for schema in ("UAU", "UUAU", "UUUAU"):
    e = MetaPathWalkEmbedding(schema=schema, num_walks=2, walk_length=40, seed=0)
    cyc = schema[:-1]
    nsteps = Counter()
    for s in probe:
        s = int(s)
        for w in e.sample_walks(H, s):
            k = cyc.index(ntypeH[s])
            rot = cyc[k:] + cyc[:k]
            for i, v in enumerate(w):
                assert ntypeH[v] == rot[i % len(rot)], f"{schema}: wrong type at {i}"
                if i:
                    assert H.has_edge(w[i - 1], v)
                    nsteps[ntypeH[w[i - 1]] + ntypeH[v]] += 1
    tot = sum(nsteps.values())
    frac_uu = nsteps["UU"] / tot
    print(f"  H_train {schema:6s}: {tot:,} steps, social(U-U) fraction {frac_uu:.3f} "
          f"(expect {cyc.count('U') and (cyc.count('U') - 1 + (cyc[0] == 'U' and cyc[-1] == 'U')) / len(cyc):.3f})")

# rare-artist weighting must actually prefer low-degree artists
adj_t, _ = typed_adjacency(H)
deg_a = {a: len(adj_t[a]["U"]) for a in range(N_USERS, N_USERS + hstats["n_artists"])}
for alpha in (None, 1.0):
    e = MetaPathWalkEmbedding(schema="UAU", alpha=alpha, num_walks=4, walk_length=40, seed=0)
    hit = [deg_a[v] for s in probe[:300] for w in e.sample_walks(H, int(s))
           for v in w if v >= N_USERS]
    print(f"  rare-artist alpha={alpha}: mean popularity of visited artist "
          f"{np.mean(hit):8.1f}  median {np.median(hit):7.1f}  (n={len(hit):,})")

print("\nall sampler gates passed")
