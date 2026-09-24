"""Validator's own, independent recomputation of everything answer.tex claims."""
import pickle, json
import numpy as np, pandas as pd

R0 = pickle.load(open("worker_results_full.pkl", "rb"))
RS = pickle.load(open("worker_results_seeds.pkl", "rb"))
print("R0 keys:", list(R0.keys()))
print("RS keys:", list(RS.keys()))
NAMES = list(R0.keys())

def trio(name, f):
    return np.array([f(R0[name])] + [f(RS[f"{name} | seed{s}"]) for s in (1, 2)])

COLS = {
    "val H@1":  lambda r: r["lp"]["val"][0]["hit@1"],
    "val MRR":  lambda r: r["lp"]["val"][0]["MRR"],
    "test H@1": lambda r: r["lp"]["test"][0]["hit@1"],
    "test MRR": lambda r: r["lp"]["test"][0]["MRR"],
    "val miF1": lambda r: r["country"].loc["val", "micro_f1"],
    "val maF1": lambda r: r["country"].loc["val", "macro_f1"],
    "test miF1":lambda r: r["country"].loc["test", "micro_f1"],
    "test maF1":lambda r: r["country"].loc["test", "macro_f1"],
}

print("\n=== MEAN over seeds 0,1,2 (validator recomputation) ===")
mean = pd.DataFrame({c: {n: trio(n, f).mean() for n in NAMES} for c, f in COLS.items()})
print(mean.round(4).to_string())

print("\n=== per-column argmax (is triadic best everywhere?) ===")
for c in COLS:
    am = mean[c].idxmax()
    print(f"  {c:10s} best = {am:24s} {mean[c].max():.4f}   triadic={mean[c]['triadic']:.4f}")

print("\n=== mean within-strategy sd (noise floor) ===")
sd = pd.DataFrame({c: {n: trio(n, f).std(ddof=1) for n in NAMES} for c, f in COLS.items()})
print(sd.mean().round(4).to_string())

print("\n=== spread / noise ratio ===")
for c in COLS:
    sp = mean[c].max() - mean[c].min()
    print(f"  {c:10s} spread {sp:.4f}  noise {sd[c].mean():.4f}  ratio {sp/sd[c].mean():.2f}")

print("\n=== per-seed raw values, triadic vs deepwalk (test MRR / test maF1) ===")
for c in ("test MRR", "test maF1", "val H@1", "test H@1", "val miF1", "test miF1", "val MRR"):
    d = trio("deepwalk", COLS[c]); t = trio("triadic", COLS[c])
    print(f"  {c:10s} deepwalk {np.round(d,4)}  triadic {np.round(t,4)}  "
          f"triadic>deepwalk on {int((t>d).sum())}/3 seeds")

print("\n=== TABLE 2 recomputation (test split, mean of 3 seeds) ===")
for n in ("deepwalk", "triadic", "rwr r=0.15"):
    h = np.array([trio(n, lambda r, i=i: r["lp"]["test"][1]["hit_at_1"].iloc[i]).mean() for i in range(6)])
    m = np.array([trio(n, lambda r, i=i: r["lp"]["test"][1]["MRR"].iloc[i]).mean() for i in range(6)])
    print(f"  {n:24s} hit {np.round(h,4)}")
    print(f"  {' '*24} mrr {np.round(m,4)}")
print("  n_queries:", R0["deepwalk"]["lp"]["test"][1]["n_queries"].tolist())
print("  buckets  :", [str(x) for x in R0["deepwalk"]["lp"]["test"][1].index.tolist()])

# ---------------- data-derived claims
print("\n=== country label distribution (data, independent of worker code) ===")
country = pd.read_csv("data/task2/node_country.csv").set_index("node_id")["country"].reindex(range(7624))
split = pd.read_csv("data/task3/country_split.csv").set_index("node_id")["split"]
vc = country.value_counts()
print("  n classes:", country.nunique(), " largest:", vc.max(), " smallest:", vc.min())
tr = country[ (split=="train").reindex(country.index).fillna(False).to_numpy() ]
print("  smallest class id:", vc.idxmin(), " count in 763-train split:",
      int((tr == vc.idxmin()).sum()))
te = country[(split=="test").reindex(country.index).fillna(False).to_numpy()]
print("  test users:", len(te), " majority-class rate on test:", round(te.value_counts().max()/len(te), 4))

print("\n=== chance baselines for 21 candidates ===")
H21 = sum(1.0/k for k in range(1, 22))
print("  chance hit@1 = 1/21 =", round(1/21, 4), "  chance MRR = H21/21 =", round(H21/21, 4))
