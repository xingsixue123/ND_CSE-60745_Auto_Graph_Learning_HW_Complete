"""Control for the walk-budget confound.

Task-3 DeepWalk walks from the 6,958 non-isolated users only -> 69,580 walks.
Every Task-4 run walks from all 15,466 nodes of H -> ~152,930 walks, i.e. 2.2x the
Skip-Gram corpus.  So "U-U-U-A-U beats DeepWalk" could be nothing but a bigger corpus.

This runs Task-3 DeepWalk on G_train with num_walks=22 (6,958 x 22 = 153,076 walks,
matching the Task-4 corpus to within 0.1%) at seeds 0,1,2.  If the extra budget explains
the gain, this control should catch up with U-U-U-A-U.  If it does not, the gain is the
artist structure.

    ../../venv/bin/python control_budget.py
"""
import pickle
import time

import numpy as np
import pandas as pd

from scaffold import (RESULTS, embed_graph, evaluate_country, evaluate_link_prediction,
                      load_data)
from impl import CountryClassifier, LinkPredictor, WalkEmbedding

G_train, splits, country, country_split, N_USERS = load_data()
n_walkable = sum(1 for _, d in G_train.degree() if d > 0)
print(f"G_train: {n_walkable} non-isolated users; 22 walks each = {n_walkable*22:,} walks "
      f"(Task-4 corpus is 152,930)\n")

BASE = dict(walk_length=40, dim=128, window=5, negative=5, epochs=5)


def run(name, embedder):
    print(f"[{name}]", flush=True)
    Z = embed_graph(embedder, G_train, N_USERS)[:N_USERS]
    lp = evaluate_link_prediction(Z, LinkPredictor(), splits, G_train)
    cc = evaluate_country(Z, country, CountryClassifier(), country_split)
    v, t = lp["val"][0], lp["test"][0]
    RESULTS[name] = {"summary": {}, "lp": lp, "country": cc}
    print(f"    val hit@1 {v['hit@1']:.4f} MRR {v['MRR']:.4f} | "
          f"test hit@1 {t['hit@1']:.4f} MRR {t['MRR']:.4f} | "
          f"cc test micro {cc.loc['test','micro_f1']:.4f} macro {cc.loc['test','macro_f1']:.4f} | "
          f"cold hit@1 {lp['test'][1]['hit_at_1'].iloc[0]:.4f}", flush=True)


for seed in (0, 1, 2):
    t0 = time.perf_counter()
    run(f"deepwalk x22|seed{seed}",
        WalkEmbedding(seed=seed, strategy="uniform", num_walks=22, **BASE))
    print(f"    total {time.perf_counter()-t0:.1f}s\n", flush=True)

with open("results_control.pkl", "wb") as f:
    pickle.dump(RESULTS, f)

g = lambda k: np.array([RESULTS[f"deepwalk x22|seed{s}"]["lp"]["test"][0][k] for s in (0, 1, 2)])
c = lambda k: np.array([RESULTS[f"deepwalk x22|seed{s}"]["country"].loc["test", k] for s in (0, 1, 2)])
cold = np.array([RESULTS[f"deepwalk x22|seed{s}"]["lp"]["test"][1]["hit_at_1"].iloc[0] for s in (0, 1, 2)])
print("\nDeepWalk x22 (3-seed mean):")
print(f"  test hit@1 {g('hit@1').mean():.4f}+-{g('hit@1').std(ddof=1):.4f}  "
      f"test MRR {g('MRR').mean():.4f}+-{g('MRR').std(ddof=1):.4f}")
print(f"  cc test micro {c('micro_f1').mean():.4f}  macro {c('macro_f1').mean():.4f}")
print(f"  cold bucket hit@1 {cold.mean():.4f}")
print("\ncompare: DeepWalk x10 0.6009/0.7207/0.7629/0.6833/0.0447 ; "
      "U-U-U-A-U 0.6163/0.7361/0.7887/0.6353/0.2824")
print("wrote results_control.pkl")
