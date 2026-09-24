"""Measure the ACTUAL Skip-Gram corpus (walks AND tokens) for every configuration.

Round-2 defect [1.1]: the round-1 control was matched on walk *count*, but gensim's
training cost and effective data scale with *tokens*.  Meta-path walks dead-end mid-way
(defect [1.2]), so walks != tokens/40 for the U-U-A-U and U-U-U-A-U schemas.

Walk generation only -- no Skip-Gram training -- so this is seconds, not minutes.

    ../../venv/bin/python corpus_size.py
"""
import time

import numpy as np

import json as _json
from pathlib import Path

import pandas as pd

from scaffold import load_data
from impl import WalkEmbedding
from hetero import MetaPathWalkEmbedding

BASE = dict(walk_length=40, dim=128, window=5, negative=5, epochs=5)

G_train, splits, country, country_split, N_USERS = load_data()

# section 7, verbatim (same construction as run_hetero.py)
hstats = _json.loads(Path("data/task3/hetero_stats.json").read_text())
N_ARTISTS = hstats["n_artists"]
user_artist = pd.read_csv("data/task3/user_artist.csv.gz")
H_train = G_train.copy()
H_train.add_nodes_from(range(N_USERS, N_USERS + N_ARTISTS), type="A")
H_train.add_edges_from(user_artist.itertuples(index=False, name=None))
assert H_train.number_of_nodes() == 15466
assert H_train.number_of_edges() == G_train.number_of_edges() + hstats["n_user_artist_edges"]
N_H = N_USERS + N_ARTISTS


def corpus(embedder, G, n_nodes, label):
    """Replicate embed_graph's walk collection exactly, but only count."""
    t0 = time.perf_counter()
    walks, toks, full, starts = 0, 0, 0, 0
    lens = []
    for node in range(n_nodes):
        ws = embedder.sample_walks(G, node)
        if ws:
            starts += 1
        for w in ws:
            walks += 1
            toks += len(w)
            lens.append(len(w))
            if len(w) == BASE["walk_length"]:
                full += 1
    lens = np.array(lens)
    print(f"{label:34s} starts {starts:6,}  walks {walks:8,}  tokens {toks:10,}  "
          f"mean_len {lens.mean():5.1f}  full {100*full/walks:5.1f}%  "
          f"[{time.perf_counter()-t0:.1f}s]", flush=True)
    return dict(label=label, starts=starts, walks=walks, tokens=toks,
                mean_len=float(lens.mean()), pct_full=100.0 * full / walks)


rows = []
# --- Task 3 configurations on the social graph (walk from users only) ---
for nw in (10, 15, 22):
    rows.append(corpus(WalkEmbedding(seed=0, strategy="uniform", num_walks=nw, **BASE),
                       G_train, N_USERS, f"DeepWalk on G, {nw} walks/node"))

# --- Task 4 configurations on the heterogeneous graph (walk from ALL nodes of H) ---
rows.append(corpus(WalkEmbedding(seed=0, strategy="uniform", num_walks=10, **BASE),
                   H_train, N_H, "type-blind DeepWalk on H"))
for schema in ("UAU", "UUAU", "UUUAU"):
    rows.append(corpus(MetaPathWalkEmbedding(schema=schema, seed=0, num_walks=10, **BASE),
                       H_train, N_H, f"metapath {'-'.join(schema)}"))
rows.append(corpus(MetaPathWalkEmbedding(schema="UAU", alpha=1.0, seed=0, num_walks=10, **BASE),
                   H_train, N_H, "U-A-U rare-artist a=1"))

ctl22 = next(r for r in rows if r["label"] == "DeepWalk on G, 22 walks/node")
print(f"\n{'config':34s} {'tokens':>10s}  {'vs x22 control':>15s}")
for r in rows:
    print(f"{r['label']:34s} {r['tokens']:10,}  {100*(r['tokens']/ctl22['tokens']-1):+14.1f}%")

tgt = next(r for r in rows if r["label"] == "metapath U-U-U-A-U")["tokens"]
print(f"\nU-U-U-A-U needs {tgt:,} tokens == {tgt/BASE['walk_length']:,.0f} full-length walks")
n_walkable = sum(1 for _, d in G_train.degree() if d > 0)
for nw in (14, 15):
    t = n_walkable * nw * BASE["walk_length"]
    print(f"  DeepWalk on G x{nw}: {n_walkable*nw:,} walks = {t:,} tokens ({100*(t/tgt-1):+.1f}%)")

import json
json.dump(rows, open("corpus_size.json", "w"), indent=1)
print("\nwrote corpus_size.json")
