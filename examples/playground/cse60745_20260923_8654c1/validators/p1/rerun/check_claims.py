"""Verify every per-bucket claim made in the analysis, seed-averaged."""
import pickle
import numpy as np
import pandas as pd

R0 = pickle.load(open("results_full.pkl", "rb"))
RS = pickle.load(open("results_seeds.pkl", "rb"))
NAMES = list(R0.keys())
BK = ["0", "1", "2-3", "4-7", "8-15", "16+"]

def bucket_mean(name, col="hit_at_1", split="test"):
    a = np.array([[r["lp"][split][1][col].iloc[b] for b in range(6)]
                  for r in [R0[name]] + [RS[f"{name} | seed{s}"] for s in (1, 2)]])
    return a.mean(0), a.std(0, ddof=1)

print("=== TEST hit@1 by bucket, mean over 3 seeds")
M = {n: bucket_mean(n)[0] for n in NAMES}
print(pd.DataFrame(M, index=BK).T.round(4).to_string())
print("\n=== delta vs DeepWalk (test hit@1)")
print(pd.DataFrame({n: M[n] - M["deepwalk"] for n in NAMES}, index=BK).T.round(4).to_string())
print("\n=== TEST MRR by bucket, mean over 3 seeds")
Mm = {n: bucket_mean(n, "MRR")[0] for n in NAMES}
print(pd.DataFrame(Mm, index=BK).T.round(4).to_string())
print("\n=== cold bucket (test hit@1) per strategy per seed")
for n in NAMES:
    v = [R0[n]["lp"]["test"][1]["hit_at_1"].iloc[0]] + \
        [RS[f"{n} | seed{s}"]["lp"]["test"][1]["hit_at_1"].iloc[0] for s in (1, 2)]
    print(f"  {n:24s} {v}")
