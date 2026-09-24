"""Structural facts the analysis rests on: who the cold-start users are, and whether
the artist layer actually covers them.

    ../../venv/bin/python cold_start_stats.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scaffold import load_data

G_train, splits, country, country_split, N_USERS = load_data()
hstats = json.loads(Path("data/task3/hetero_stats.json").read_text())
ua = pd.read_csv("data/task3/user_artist.csv.gz")

deg = dict(G_train.degree())
n_art = ua.groupby("user").size().reindex(range(N_USERS), fill_value=0)

iso = [u for u in range(N_USERS) if deg[u] == 0]
iso_with_art = [u for u in iso if n_art[u] > 0]
print(f"users                          : {N_USERS}")
print(f"socially isolated (deg 0)      : {len(iso)}")
print(f"  ... of those, >=1 artist     : {len(iso_with_art)} "
      f"({100*len(iso_with_art)/len(iso):.1f}%)")
print(f"  ... median artists among them: {int(n_art[iso_with_art].median())}")
print(f"users with no artist at all    : {int((n_art == 0).sum())} "
      f"(hetero_stats says {hstats['users_with_no_artist']})")
print(f"artists per user: median {int(n_art.median())}, max {int(n_art.max())}, "
      f"mean {n_art.mean():.1f}")
print(f"artist popularity: median {int(ua.groupby('artist').size().median())}, "
      f"max {int(ua.groupby('artist').size().max())}, "
      f"mean {ua.groupby('artist').size().mean():.1f}")

# how many test queries have a cold source, and are they covered by artists?
for split in ("val", "test"):
    df = splits[split]
    pos = df[df["label"] == 1]
    src = pos["src"].to_numpy()
    d = np.array([deg[s] for s in src])
    cold = src[d == 0]
    print(f"\n{split}: {len(pos)} queries, {int((d == 0).sum())} with a cold source; "
          f"{int((n_art[cold] > 0).sum())} of those cold sources have >=1 artist "
          f"({100*(n_art[cold] > 0).mean():.1f}%)")

# what a U-A-U step actually connects: how many users share >=1 artist with a given user?
# exact all-pairs is 7624^2; sample instead.
rng = np.random.default_rng(0)
art_users = ua.groupby("artist")["user"].apply(set)
user_arts = ua.groupby("user")["artist"].apply(list)
sample = rng.choice([u for u in range(N_USERS) if n_art[u] > 0], 40, replace=False)
reach = []
for u in sample:
    s = set()
    for a in user_arts[u]:
        s |= art_users[a]
    reach.append(len(s) - 1)
print(f"\nU-A-U 2-hop reach (40 sampled users with artists): "
      f"median {int(np.median(reach))}, mean {np.mean(reach):.0f} of {N_USERS-1} other users "
      f"({100*np.mean(reach)/(N_USERS-1):.1f}% of the graph)")
print(f"social 2-hop reach for comparison: median "
      f"{int(np.median([len(set().union(*[set(G_train[v]) for v in G_train[u]]) if list(G_train[u]) else set()) for u in sample if deg[u] > 0]))}")
