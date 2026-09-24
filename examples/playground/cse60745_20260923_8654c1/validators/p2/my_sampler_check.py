"""Validator's own check of MetaPathWalkEmbedding, written from the spec, not from
the worker's test_sampler.py.

Checks on the REAL H_train:
  1. every consecutive pair in a walk is a real edge of H
  2. the type sequence is exactly the schema cycle, rotated to the start type
  3. walk length is walk_length whenever the walk does not dead-end
  4. the social-step fraction is the designed 0 / 1/3 / 1/2
  5. users with no artist give [] under UAU; socially isolated users give [] under UUAU
  6. the total walk count per schema matches what run_hetero.log reports
  7. rare-artist alpha=1 really samples artists ~ 1/deg(a)
"""
import collections
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scaffold import load_data, typed_adjacency
from hetero import MetaPathWalkEmbedding

G, splits, country, country_split, N = load_data()
h = json.loads(Path("data/task3/hetero_stats.json").read_text())
ua = pd.read_csv("data/task3/user_artist.csv.gz")
H = G.copy()
H.add_nodes_from(range(N, N + h["n_artists"]), type="A")
H.add_edges_from(ua.itertuples(index=False, name=None))
adj_t, ntype = typed_adjacency(H)
print(f"H: {H.number_of_nodes():,} nodes {H.number_of_edges():,} edges")

deg_social = dict(G.degree())
n_art = ua.groupby("user").size().reindex(range(N), fill_value=0)
iso_users = {u for u in range(N) if deg_social[u] == 0}
noart_users = {u for u in range(N) if n_art[u] == 0}
print(f"socially isolated users: {len(iso_users)} | users with no artist: {len(noart_users)}"
      f" | both: {len(iso_users & noart_users)}")

BASE = dict(num_walks=10, walk_length=40, dim=128, window=5, negative=5, epochs=5)
rng = np.random.default_rng(7)

for schema, want_social in (("UAU", 0.0), ("UUAU", 1 / 3), ("UUUAU", 0.5)):
    emb = MetaPathWalkEmbedding(schema=schema, seed=0, **BASE)
    cycle = schema[:-1]
    probe = [int(x) for x in rng.choice(N, 150, replace=False)] + \
            [int(x) for x in rng.choice(range(N, N + h["n_artists"]), 50, replace=False)]

    bad_edge = bad_type = 0
    lens = collections.Counter()
    steps = collections.Counter()
    for s in probe:
        t0 = ntype[s]
        k = cycle.index(t0)
        rot = cycle[k:] + cycle[:k]
        for w in emb.sample_walks(H, s):
            lens[len(w)] += 1
            for i, (a, b) in enumerate(zip(w, w[1:])):
                if not H.has_edge(a, b):
                    bad_edge += 1
                if ntype[b] != rot[(i + 1) % len(rot)]:
                    bad_type += 1
                steps[ntype[a] + ntype[b]] += 1
    tot = sum(steps.values())
    got_social = steps["UU"] / tot
    print(f"\nschema {schema:6s} cycle {cycle}")
    print(f"  non-edges in walks : {bad_edge}   (must be 0)")
    print(f"  type violations    : {bad_type}   (must be 0)")
    print(f"  walk lengths       : {dict(lens)}")
    print(f"  step types         : {dict(steps)}")
    print(f"  social fraction    : {got_social:.4f}  designed {want_social:.4f}")

    # dead-end behaviour
    if schema == "UAU":
        vic = [u for u in list(noart_users)[:5]]
        print(f"  users with no artist -> walks: "
              f"{[len(emb.sample_walks(H, u)) for u in vic]}  (must all be 0)")
    if schema == "UUAU":
        vic = [u for u in list(iso_users - noart_users)[:5]]
        print(f"  socially isolated users -> walks: "
              f"{[len(emb.sample_walks(H, u)) for u in vic]}  (must all be 0)")

    # full corpus size
    total = sum(len(emb.sample_walks(H, s)) for s in H.nodes())
    print(f"  TOTAL walks over all {H.number_of_nodes():,} nodes = {total:,}")

# ---- rare artist
print("\n=== rare-artist alpha=1 ===")
plain = MetaPathWalkEmbedding(schema="UAU", seed=0, **BASE)
rare = MetaPathWalkEmbedding(schema="UAU", alpha=1.0, seed=0, **BASE)
art_pop = ua.groupby("artist").size()
probe = [int(x) for x in rng.choice([u for u in range(N) if n_art[u] > 0], 200, replace=False)]
for tag, e in (("uniform", plain), ("alpha=1", rare)):
    pops = []
    for s in probe:
        for w in e.sample_walks(H, s):
            pops += [art_pop[v] for v in w if ntype[v] == "A"]
    print(f"  {tag:8s}: median visited-artist popularity {np.median(pops):.1f} "
          f"mean {np.mean(pops):.1f}  (n={len(pops):,})")
print(f"  dataset artist popularity median = {art_pop.median():.1f}")

# direct check the weighting is 1/deg on a single node
u = probe[0]
arts = adj_t[u]["A"]
counts = collections.Counter()
import random
r = random.Random(0)
tables, _ = rare._typed_tables(H)
nbrs, cum = tables[u]["A"]
for _ in range(200000):
    counts[r.choices(nbrs, cum_weights=cum, k=1)[0]] += 1
w = np.array([1.0 / art_pop[a] for a in nbrs])
w = w / w.sum()
emp = np.array([counts[a] for a in nbrs], dtype=float)
emp /= emp.sum()
print(f"  node {u}: {len(nbrs)} artists; max |empirical - 1/deg| prob error = "
      f"{np.abs(emp - w).max():.5f} (should be ~1e-3 sampling noise)")
