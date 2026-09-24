"""Section 6: run every sampling strategy through `run_experiment` and save the results.

    ../../venv/bin/python run_all.py
"""
import pickle
import sys
import time

import numpy as np
import pandas as pd

from scaffold import (RANDOM_SEED, RESULTS, breakdown_by_source_degree, comparison_table,
                      embed_graph, evaluate_country, evaluate_link_prediction, load_data)
from impl import CountryClassifier, LinkPredictor, WalkEmbedding

# ------------------------------------------------------------------ section 2 (verbatim)
G_train, splits, country, country_split, N_USERS = load_data()
train_df, val_df, test_df = splits["train"], splits["val"], splits["test"]

n_iso = sum(1 for _, d in G_train.degree() if d == 0)
print(f"G_train: {G_train.number_of_edges():,} edges, {n_iso} isolated users")
for name, df in splits.items():
    n_q = int(df["label"].sum())
    print(f"{name:>5}: {n_q:>6} queries x {len(df) // n_q:>2} candidates")
print(f"country: {len(set(country))} classes; users split "
      + " / ".join(f"{k} {len(v)}" for k, v in country_split.items()))

degs = [d for _, d in G_train.degree()]
print(f"sanity: mean deg {np.mean(degs):.3f}, max deg {max(degs)}, "
      f"components {sum(1 for _ in __import__('networkx').connected_components(G_train))}")


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


# ------------------------------------------------------------------ section 6
BASE = dict(num_walks=10, walk_length=40, dim=128, window=5, negative=5, epochs=5)

STRATEGIES = [
    ("deepwalk",             dict(strategy="uniform")),
    ("node2vec p=1 q=0.5",   dict(strategy="node2vec", p=1.0, q=0.5)),
    ("node2vec p=1 q=2",     dict(strategy="node2vec", p=1.0, q=2.0)),
    ("node2vec p=0.25 q=0.25", dict(strategy="node2vec", p=0.25, q=0.25)),
    ("rwr r=0.15",           dict(strategy="rwr", restart=0.15)),
    ("degcorr a=1",          dict(strategy="degcorr", alpha=1.0)),
    ("triadic",              dict(strategy="triadic")),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, kw in STRATEGIES:
        if only and name not in only:
            continue
        t0 = time.perf_counter()
        run_experiment(name, WalkEmbedding(seed=RANDOM_SEED, **BASE, **kw), G_train, N_USERS)
        print(f"    total {time.perf_counter() - t0:.1f}s\n", flush=True)

    tab = comparison_table()
    pd.set_option("display.max_columns", None)
    print(tab.to_string())
    if only:            # a filtered run must not clobber the full-sweep artefacts
        print("\nfiltered run: results NOT written")
    else:
        tab.to_csv("results_comparison.csv")
        with open("results_full.pkl", "wb") as f:
            pickle.dump(RESULTS, f)
        print("\nwrote results_comparison.csv and results_full.pkl")
