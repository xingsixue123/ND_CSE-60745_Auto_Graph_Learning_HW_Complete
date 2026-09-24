"""Task 4, notebook sections 7 and 8.

    ../../venv/bin/python run_hetero.py            # all schemas, seeds 0,1,2
    ../../venv/bin/python run_hetero.py --seeds 0  # quick single-seed pass

Sections 2, 5 and 7 are the notebook's own code, copied verbatim.  Section 8 is mine.
Writes results_hetero.csv / results_hetero.pkl (full sweep only).
"""
import argparse
import json
import pickle
import time
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from scaffold import (RANDOM_SEED, RESULTS, embed_graph, evaluate_country,
                      evaluate_link_prediction, load_data)
from impl import CountryClassifier, LinkPredictor, WalkEmbedding
from hetero import MetaPathWalkEmbedding

# ------------------------------------------------------------------ section 2 (verbatim)
G_train, splits, country, country_split, N_USERS = load_data()

# ------------------------------------------------------------------ section 7 (verbatim)
hstats = json.loads(Path("data/task3/hetero_stats.json").read_text())
N_ARTISTS = hstats["n_artists"]
user_artist = pd.read_csv("data/task3/user_artist.csv.gz")


def add_artists(G_social):
    """Return a copy of a social graph with the artist nodes and user-artist edges added."""
    H = G_social.copy()
    H.add_nodes_from(range(N_USERS, N_USERS + N_ARTISTS), type="A")
    H.add_edges_from(user_artist.itertuples(index=False, name=None))
    return H


t0 = time.perf_counter()
H_train = add_artists(G_train)
print(f"user-artist: {N_ARTISTS} artists, {len(user_artist):,} edges, "
      f"{user_artist['user'].nunique()} of {N_USERS} users like at least one artist")
print(f"H_train: {H_train.number_of_nodes():,} nodes, {H_train.number_of_edges():,} edges "
      f"(built in {time.perf_counter() - t0:.1f}s)")

# ------------------------------------------------------------------ sanity gates (mine)
assert H_train.number_of_nodes() == N_USERS + N_ARTISTS == 15466
assert H_train.number_of_edges() == G_train.number_of_edges() + hstats["n_user_artist_edges"]
assert N_USERS - user_artist["user"].nunique() == hstats["users_with_no_artist"]
assert user_artist["artist"].min() == hstats["artist_id_offset"]
print("sanity: H_train matches hetero_stats.json\n", flush=True)

N_NODES = N_USERS + N_ARTISTS


# ------------------------------------------------------------------ section 5 (verbatim)
def run_experiment(name, embedder, G, n_nodes, predictor_factory=None, classifier_factory=None):
    """Embed G, evaluate both downstream tasks, and record the result under `name`."""
    predictor_factory = predictor_factory or LinkPredictor
    classifier_factory = classifier_factory or CountryClassifier

    print(f"[{name}]", flush=True)
    Z = embed_graph(embedder, G, n_nodes)[:N_USERS]

    lp = evaluate_link_prediction(Z, predictor_factory(), splits, G_train)
    cc = evaluate_country(Z, country, classifier_factory(), country_split)

    v, t = lp["val"][0], lp["test"][0]
    row = {"lp_val_hit@1": v["hit@1"], "lp_val_MRR": v["MRR"],
           "lp_test_hit@1": t["hit@1"], "lp_test_MRR": t["MRR"]}
    for bucket, hit in lp["val"][1]["hit_at_1"].items():
        row[f"val_hit@1_deg{bucket.left:.0f}+"] = hit
    row.update({"country_val_microF1": cc.loc["val", "micro_f1"],
                "country_test_microF1": cc.loc["test", "micro_f1"],
                "country_test_macroF1": cc.loc["test", "macro_f1"]})
    RESULTS[name] = {"summary": row, "lp": lp, "country": cc}

    print(f"    link prediction: val hit@1 {v['hit@1']:.4f} MRR {v['MRR']:.4f}   |   "
          f"test hit@1 {t['hit@1']:.4f} MRR {t['MRR']:.4f}")
    print(f"    country:         val micro-F1 {cc.loc['val', 'micro_f1']:.4f}   |   "
          f"test micro-F1 {cc.loc['test', 'micro_f1']:.4f} macro-F1 {cc.loc['test', 'macro_f1']:.4f}",
          flush=True)
    return RESULTS[name]


# ------------------------------------------------------------------ section 8 (mine)
# Identical walk budget and Skip-Gram hyper-parameters to Task 3.
BASE = dict(num_walks=10, walk_length=40, dim=128, window=5, negative=5, epochs=5)

SCHEMAS = [
    # name,                       factory(seed)
    ("hetero-deepwalk",           lambda s: WalkEmbedding(seed=s, strategy="uniform", **BASE)),
    ("metapath U-A-U",            lambda s: MetaPathWalkEmbedding(schema="UAU", seed=s, **BASE)),
    ("metapath U-U-A-U",          lambda s: MetaPathWalkEmbedding(schema="UUAU", seed=s, **BASE)),
    ("metapath U-U-U-A-U",        lambda s: MetaPathWalkEmbedding(schema="UUUAU", seed=s, **BASE)),
    ("U-A-U rare-artist a=1",     lambda s: MetaPathWalkEmbedding(schema="UAU", alpha=1.0,
                                                                  seed=s, **BASE)),
]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()

    full = (args.seeds == [0, 1, 2]) and not args.only
    for seed in args.seeds:
        for name, factory in SCHEMAS:
            if args.only and name not in args.only:
                continue
            t = time.perf_counter()
            run_experiment(f"{name}|seed{seed}", factory(seed), H_train, N_NODES)
            print(f"    total {time.perf_counter() - t:.1f}s\n", flush=True)

    tab = pd.DataFrame({k: v["summary"] for k, v in RESULTS.items()}).T.round(4)
    pd.set_option("display.max_columns", None)
    print(tab.to_string())
    if full:
        tab.to_csv("results_hetero.csv")
        with open("results_hetero.pkl", "wb") as f:
            pickle.dump(RESULTS, f)
        print("\nwrote results_hetero.csv and results_hetero.pkl")
    else:
        print("\npartial run: results NOT written")
