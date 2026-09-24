"""How big is seed noise?  Re-run every strategy at seeds 1 and 2 (seed 0 is in
results_full.pkl already) so that the spread *between* strategies can be compared
against the spread *within* a strategy.

    ../../venv/bin/python seed_study.py
"""
import pickle

import pandas as pd

from scaffold import RESULTS, comparison_table
from impl import WalkEmbedding
from run_all import BASE, STRATEGIES, G_train, N_USERS, run_experiment

if __name__ == "__main__":
    rows = {}
    for seed in (1, 2):
        for name, kw in STRATEGIES:
            tag = f"{name} | seed{seed}"
            run_experiment(tag, WalkEmbedding(seed=seed, **BASE, **kw), G_train, N_USERS)
            rows[tag] = RESULTS[tag]["summary"]

    tab = pd.DataFrame(rows).T.round(4)
    pd.set_option("display.max_columns", None)
    print(tab.to_string())
    tab.to_csv("results_seeds.csv")
    with open("results_seeds.pkl", "wb") as f:
        pickle.dump({k: v for k, v in RESULTS.items() if "seed" in k}, f)
    print("\nwrote results_seeds.csv")
