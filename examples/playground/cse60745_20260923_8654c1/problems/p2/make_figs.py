"""Write the two vector PDFs straight into OUTPUT.

    MPLCONFIGDIR=$PWD/.mplcache ../../venv/bin/python make_figs.py
"""
import pickle
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("/home/xing/project/auto_hw_complete/output/cse60745_20260923_8654c1/p2")
OUT.mkdir(parents=True, exist_ok=True)

P1_0 = pickle.load(open("../p1/results_full.pkl", "rb"))
P1_S = pickle.load(open("../p1/results_seeds.pkl", "rb"))
P2 = pickle.load(open("results_hetero.pkl", "rb"))
CTL = pickle.load(open("results_control.pkl", "rb"))
CTL.update(pickle.load(open("results_tokens.pkl", "rb")))
T3 = set(P1_0)


def runs(name):
    if name in T3:
        return [P1_0[name]] + [P1_S[f"{name} | seed{s}"] for s in (1, 2)]
    if name.startswith("deepwalk x"):
        return [CTL[f"{name}|seed{s}"] for s in (0, 1, 2)]
    return [P2[f"{name}|seed{s}"] for s in (0, 1, 2)]


def bucket(name, col, i, split="test"):
    return np.array([r["lp"][split][1][col].iloc[i] for r in runs(name)])


def overall(name, key="hit@1", split="test"):
    return np.array([r["lp"][split][0][key] for r in runs(name)])


plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
                     "xtick.labelsize": 9.5, "ytick.labelsize": 9.5, "legend.fontsize": 9,
                     "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})

LBL = ["0\n(cold)", "1", "2–3", "4–7", "8–15", "≥16"]
NQ = P1_0["deepwalk"]["lp"]["test"][1]["n_queries"].to_numpy().astype(int)

# ================================================================= fig 1: degree breakdown
SHOW = [("deepwalk x15", "DeepWalk on $G$ (token-matched)", "#4C72B0"),
        ("metapath U-A-U", "U-A-U  (0% social steps)", "#DD8452"),
        ("metapath U-U-A-U", "U-U-A-U  (33% social)", "#55A868"),
        ("metapath U-U-U-A-U", "U-U-U-A-U  (50% social)", "#C44E52")]

fig, ax = plt.subplots(figsize=(6.0, 2.95))
x = np.arange(6)
w = 0.2
for j, (name, lab, c) in enumerate(SHOW):
    m = np.array([bucket(name, "hit_at_1", i).mean() for i in range(6)])
    e = np.array([bucket(name, "hit_at_1", i).std(ddof=1) for i in range(6)])
    ax.bar(x + (j - 1.5) * w, m, w, yerr=e, capsize=2, label=lab, color=c,
           error_kw={"lw": 0.8})
ax.set_xticks(x)
ax.set_xticklabels([f"{l}\nn={n}" for l, n in zip(LBL, NQ)])
ax.set_xlabel("source user's degree in the social graph $G_{\\mathrm{train}}$")
ax.set_ylabel("test Hit@1")
ax.set_ylim(0, 0.95)
ax.set_yticks(np.arange(0, 0.71, 0.1))
ax.legend(loc="upper left", ncol=2, frameon=False, columnspacing=1.0)
ax.grid(axis="y", lw=0.4, alpha=0.35)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(OUT / "fig_p2_degree.pdf")
plt.close(fig)
print("wrote fig_p2_degree.pdf")

# ================================================================= fig 2: social-step sweep
SWEEP = [("metapath U-A-U", 0.0), ("metapath U-U-A-U", 1 / 3),
         ("metapath U-U-U-A-U", 0.5), ("deepwalk x15", 1.0)]
xs = [s for _, s in SWEEP]

fig, ax = plt.subplots(figsize=(6.0, 3.05))
for key, lab, c, mk in (("all", "all 4,171 test queries", "#4C72B0", "o"),
                        ("cold", "cold-start users only (social degree 0)", "#DD8452", "s")):
    m, e = [], []
    for name, _ in SWEEP:
        v = overall(name) if key == "all" else bucket(name, "hit_at_1", 0)
        m.append(v.mean())
        e.append(v.std(ddof=1))
    ax.errorbar(xs, m, yerr=e, marker=mk, color=c, label=lab, lw=1.8, capsize=3, ms=6)

ax.set_xticks(xs)
ax.set_xticklabels(["0\nU-A-U", "1/3\nU-U-A-U", "1/2\nU-U-U-A-U", "1\nDeepWalk on $G$\n(token-matched)"])
ax.set_xlabel("fraction of walk steps that are social (U–U), set by the meta-path schema")
ax.set_ylabel("test Hit@1")
ax.set_ylim(0, 0.82)
ax.set_yticks(np.arange(0, 0.71, 0.1))
ax.legend(loc="upper left", frameon=False)
ax.grid(lw=0.4, alpha=0.35)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(OUT / "fig_p2_social.pdf")
plt.close(fig)
print("wrote fig_p2_social.pdf")
