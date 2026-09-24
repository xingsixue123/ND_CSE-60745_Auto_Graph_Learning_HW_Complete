"""Emit the LaTeX table bodies from the pickled results, so that no number in
answer.tex is ever typed by hand.

    ../../venv/bin/python make_tables.py > tables.tex
"""
import pickle

import numpy as np

R0 = pickle.load(open("results_full.pkl", "rb"))
RS = pickle.load(open("results_seeds.pkl", "rb"))
NAMES = list(R0.keys())
TEX = {"deepwalk": "DeepWalk (uniform)", "node2vec p=1 q=0.5": "node2vec $p{=}1,q{=}0.5$",
       "node2vec p=1 q=2": "node2vec $p{=}1,q{=}2$",
       "node2vec p=0.25 q=0.25": "node2vec $p{=}q{=}0.25$",
       "rwr r=0.15": "RWR $r{=}0.15$", "degcorr a=1": "deg-corrected $\\alpha{=}1$",
       "triadic": "triadic"}


def seeds(name, getter):
    return np.array([getter(R0[name])] + [getter(RS[f"{name} | seed{s}"]) for s in (1, 2)])


M = {
    "lp_val_hit": lambda r: r["lp"]["val"][0]["hit@1"],
    "lp_val_mrr": lambda r: r["lp"]["val"][0]["MRR"],
    "lp_test_hit": lambda r: r["lp"]["test"][0]["hit@1"],
    "lp_test_mrr": lambda r: r["lp"]["test"][0]["MRR"],
    "cc_val_micro": lambda r: r["country"].loc["val", "micro_f1"],
    "cc_val_macro": lambda r: r["country"].loc["val", "macro_f1"],
    "cc_test_micro": lambda r: r["country"].loc["test", "micro_f1"],
    "cc_test_macro": lambda r: r["country"].loc["test", "macro_f1"],
}
S = {n: {k: seeds(n, f) for k, f in M.items()} for n in NAMES}

# ------------------------------------------------------------------ table 1: comparison
ORDER = ["lp_val_hit", "lp_val_mrr", "lp_test_hit", "lp_test_mrr",
         "cc_val_micro", "cc_val_macro", "cc_test_micro", "cc_test_macro"]
best = {k: max(NAMES, key=lambda n: S[n][k].mean()) for k in ORDER}

print("% ---- TABLE 1: comparison_table(), mean over seeds {0,1,2}")
for n in NAMES:
    cells = []
    for k in ORDER:
        m = S[n][k].mean()
        cells.append(f"\\textbf{{{m:.4f}}}" if best[k] == n else f"{m:.4f}")
    print(f"{TEX[n]} & " + " & ".join(cells) + " \\\\")

print("\n% ---- TABLE 1b: seed spread (sd over 3 seeds), same columns")
for n in NAMES:
    print(f"{TEX[n]} & " + " & ".join(f"{S[n][k].std(ddof=1):.4f}" for k in ORDER) + " \\\\")

# ------------------------------------------------------------------ table 2: degree breakdown
print("\n% ---- TABLE 2: per-source-degree breakdown, TEST split, mean over seeds {0,1,2}")
LBL = ["$0$ (cold)", "$1$", "$2$--$3$", "$4$--$7$", "$8$--$15$", "$\\ge 16$"]
SHOW = ["deepwalk", "triadic", "rwr r=0.15"]
bk = R0["deepwalk"]["lp"]["test"][1]


def bmean(name, col, i):
    return seeds(name, lambda r: r["lp"]["test"][1][col].iloc[i]).mean()


for i, lab in enumerate(LBL):
    cells = [lab, str(int(bk["n_queries"].iloc[i]))]
    for n in SHOW:
        cells += [f"{bmean(n, 'hit_at_1', i):.4f}", f"{bmean(n, 'MRR', i):.4f}"]
    print(" & ".join(cells) + " \\\\")
print("% delta triadic-deepwalk hit@1 per bucket: "
      + ", ".join(f"{bmean('triadic','hit_at_1',i)-bmean('deepwalk','hit_at_1',i):+.4f}"
                  for i in range(6)))

# ------------------------------------------------------------------ numbers quoted in prose
# ------------------------------------------- table 3: comparison_table()'s val_hit@1_deg* cols
print("\n% ---- TABLE 3: the six val_hit@1_deg* columns of comparison_table(),")
print("%      all 7 strategies, mean over seeds {0,1,2}")


def vbucket(name, i):
    return seeds(name, lambda r: r["lp"]["val"][1]["hit_at_1"].iloc[i]).mean()


vbest = [max(NAMES, key=lambda n: vbucket(n, i)) for i in range(6)]
for n in NAMES:
    cells = []
    for i in range(6):
        v = f"{vbucket(n, i):.4f}"
        cells.append(f"\\textbf{{{v}}}" if vbest[i] == n else v)
    print(f"{TEX[n]} & " + " & ".join(cells) + " \\\\")
vq = R0["deepwalk"]["lp"]["val"][1]["n_queries"].to_numpy()
print("% val n_queries per bucket: " + ", ".join(str(int(x)) for x in vq))

print("\n% ---- inline numbers")
for k in ORDER:
    mu = {n: S[n][k].mean() for n in NAMES}
    sd = np.mean([S[n][k].std(ddof=1) for n in NAMES])
    lo, hi = min(mu, key=mu.get), max(mu, key=mu.get)
    print(f"% {k}: best {hi} {mu[hi]:.4f} | worst {lo} {mu[lo]:.4f} | "
          f"spread {mu[hi]-mu[lo]:.4f} | mean within-strategy sd {sd:.4f} | "
          f"ratio {(mu[hi]-mu[lo])/sd:.2f}")
