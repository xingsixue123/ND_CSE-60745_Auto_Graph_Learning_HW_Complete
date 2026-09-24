"""Figures for the write-up.  Vector PDF, written straight into OUTPUT.

    MPLCONFIGDIR=$PWD/.mplcache ../../venv/bin/python make_figs.py
"""
import os
import pickle

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".mplcache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = "/home/xing/project/auto_hw_complete/output/cse60745_20260923_8654c1/p1"
RAND_HIT1 = 1.0 / 21.0

plt.rcParams.update({
    "font.size": 10, "axes.labelsize": 11, "legend.fontsize": 9,
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "figure.dpi": 110,
})

R0 = pickle.load(open("results_full.pkl", "rb"))
RS = pickle.load(open("results_seeds.pkl", "rb"))
NAMES = list(R0.keys())
SHORT = {"deepwalk": "DeepWalk", "node2vec p=1 q=0.5": "n2v $q{=}0.5$",
         "node2vec p=1 q=2": "n2v $q{=}2$", "node2vec p=0.25 q=0.25": "n2v $p{=}q{=}0.25$",
         "rwr r=0.15": "RWR $r{=}0.15$", "degcorr a=1": "deg-corr $\\alpha{=}1$",
         "triadic": "triadic"}


def across_seeds(name, getter):
    """The three seed-0/1/2 values of one scalar metric for one strategy."""
    return np.array([getter(R0[name])] + [getter(RS[f"{name} | seed{s}"]) for s in (1, 2)])


# ---------------------------------------------------------------- fig 1: degree buckets
SHOW = ["deepwalk", "triadic", "rwr r=0.15"]      # baseline, best, worst
buckets = R0["deepwalk"]["lp"]["test"][1]
for _n in NAMES:                                   # bucket order must match across runs
    for _r in [R0[_n]] + [RS[f"{_n} | seed{s}"] for s in (1, 2)]:
        assert list(_r["lp"]["test"][1].index) == list(buckets.index)
labels = ["0 (cold)", "1", "2-3", "4-7", "8-15", "16+"]
x = np.arange(len(labels))
w = 0.26

fig, ax = plt.subplots(figsize=(5.8, 3.3))
for i, name in enumerate(SHOW):
    vals = np.array([across_seeds(name, lambda r, b=b: r["lp"]["test"][1]["hit_at_1"].iloc[b]).mean()
                     for b in range(len(labels))])
    err = np.array([across_seeds(name, lambda r, b=b: r["lp"]["test"][1]["hit_at_1"].iloc[b]).std(ddof=1)
                    for b in range(len(labels))])
    ax.bar(x + (i - 1) * w, vals, w, yerr=err, capsize=2.5, label=SHORT[name],
           error_kw=dict(lw=0.8))
ax.axhline(RAND_HIT1, ls="--", lw=1.1, color="0.35", label="random ($1/21$)")
n = buckets["n_queries"].to_numpy()
ax.set_xticks(x, [f"{l}\n$n{{=}}{ni}$" for l, ni in zip(labels, n)])
ax.set_xlabel("degree of the source user in $G_{\\mathrm{train}}$")
ax.set_ylabel("test Hit@1")
ax.set_ylim(0, 0.86)
ax.legend(frameon=False, ncol=2, loc="upper left", columnspacing=1.2, handlelength=1.6)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_p1_degree.pdf")
print("wrote fig_p1_degree.pdf")

# ---------------------------------------------------------------- fig 2: task trade-off
fig, ax = plt.subplots(figsize=(5.8, 3.9))
mk = ["o", "s", "^", "v", "D", "P", "*"]
col = ["C0", "C1", "C2", "C3", "C4", "C5", "k"]     # triadic (the winner) in black
for i, name in enumerate(NAMES):
    mrr = across_seeds(name, lambda r: r["lp"]["test"][0]["MRR"])
    mac = across_seeds(name, lambda r: r["country"].loc["test", "macro_f1"])
    ax.errorbar(mrr.mean(), mac.mean(), xerr=mrr.std(ddof=1), yerr=mac.std(ddof=1),
                marker=mk[i], ms=8 if i == 6 else 7, color=col[i], capsize=2.5, lw=0,
                elinewidth=0.9, label=SHORT[name])
ax.set_xlabel("friend recommendation: test MRR")
ax.set_ylabel("country classification: test macro-F1")
ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.01),
          handletextpad=0.2, columnspacing=1.0, fontsize=8.5)
fig.tight_layout()
fig.savefig(f"{OUT}/fig_p1_tradeoff.pdf")
print("wrote fig_p1_tradeoff.pdf")

# ---------------------------------------------------------------- numbers for the text
rows = {}
for name in NAMES:
    rows[name] = {
        "lp_val_MRR": across_seeds(name, lambda r: r["lp"]["val"][0]["MRR"]),
        "lp_test_MRR": across_seeds(name, lambda r: r["lp"]["test"][0]["MRR"]),
        "lp_val_hit1": across_seeds(name, lambda r: r["lp"]["val"][0]["hit@1"]),
        "lp_test_hit1": across_seeds(name, lambda r: r["lp"]["test"][0]["hit@1"]),
        "cc_test_micro": across_seeds(name, lambda r: r["country"].loc["test", "micro_f1"]),
        "cc_test_macro": across_seeds(name, lambda r: r["country"].loc["test", "macro_f1"]),
        "cc_val_micro": across_seeds(name, lambda r: r["country"].loc["val", "micro_f1"]),
    }
summ = pd.DataFrame({k: {m: f"{v.mean():.4f}+-{v.std(ddof=1):.4f}" for m, v in d.items()}
                     for k, d in rows.items()}).T
pd.set_option("display.width", 220); pd.set_option("display.max_columns", None)
print(summ.to_string())
summ.to_csv("results_seed_summary.csv")

for m in ("lp_test_MRR", "cc_test_macro", "cc_test_micro"):
    sds = np.array([rows[n][m].std(ddof=1) for n in NAMES])
    means = np.array([rows[n][m].mean() for n in NAMES])
    print(f"{m}: between-strategy spread {means.max()-means.min():.4f} | "
          f"mean within-strategy sd {sds.mean():.4f} | best={NAMES[int(means.argmax())]}")
