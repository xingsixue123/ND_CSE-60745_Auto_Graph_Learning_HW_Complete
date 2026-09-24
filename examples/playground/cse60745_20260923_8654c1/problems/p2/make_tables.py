"""Emit every LaTeX table body and every prose number from the pickles, so that no
number in answer.tex is typed by hand.

    ../../venv/bin/python make_tables.py > tables.tex

Task 3 rows come from p1's own artefacts (read-only) and are NOT re-run.
"""
import pickle

import numpy as np

P1_0 = pickle.load(open("../p1/results_full.pkl", "rb"))      # p1, seed 0
P1_S = pickle.load(open("../p1/results_seeds.pkl", "rb"))     # p1, seeds 1 and 2
P2 = pickle.load(open("results_hetero.pkl", "rb"))            # mine, seeds 0,1,2
CTL = pickle.load(open("results_control.pkl", "rb"))          # WALK-matched control (x22)
CTL.update(pickle.load(open("results_tokens.pkl", "rb")))     # TOKEN-matched control (x15)

# chance level for link prediction: 21 candidates per query, ties broken at random,
# so an all-zero embedding row scores exactly 1/21.
CHANCE = 1.0 / 21

T3 = ["deepwalk", "node2vec p=1 q=0.5", "node2vec p=1 q=2", "node2vec p=0.25 q=0.25",
      "rwr r=0.15", "degcorr a=1", "triadic"]
CT = ["deepwalk x15", "deepwalk x22"]
T4 = ["hetero-deepwalk", "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U",
      "U-A-U rare-artist a=1"]

TEX = {"deepwalk": "DeepWalk (uniform)", "node2vec p=1 q=0.5": "node2vec $p{=}1,q{=}0.5$",
       "node2vec p=1 q=2": "node2vec $p{=}1,q{=}2$",
       "node2vec p=0.25 q=0.25": "node2vec $p{=}q{=}0.25$",
       "rwr r=0.15": "RWR $r{=}0.15$", "degcorr a=1": "deg-corrected $\\alpha{=}1$",
       "triadic": "triadic",
       "hetero-deepwalk": "type-blind DeepWalk on $H$",
       "metapath U-A-U": "metapath \\textsf{U-A-U}",
       "metapath U-U-A-U": "metapath \\textsf{U-U-A-U}",
       "metapath U-U-U-A-U": "metapath \\textsf{U-U-U-A-U}",
       "U-A-U rare-artist a=1": "\\textsf{U-A-U} rare-artist $\\alpha{=}1$",
       "deepwalk x22": "DeepWalk $\\times22$ (walk-matched)",
       "deepwalk x15": "DeepWalk $\\times15$ (token-matched)"}

# measured Skip-Gram corpus (corpus_size.py). walks, tokens.
CORPUS = {"deepwalk": (69580, 2783200), "deepwalk x15": (104370, 4174800),
          "deepwalk x22": (153076, 6123040), "hetero-deepwalk": (154470, 6178800),
          "metapath U-A-U": (152930, 6117200), "metapath U-U-A-U": (148000, 3593757),
          "metapath U-U-U-A-U": (148000, 4068117),
          "U-A-U rare-artist a=1": (152930, 6117200)}

# fraction of walk steps that are social (U-U), by construction of the cycle
SOCIAL_FRAC = {"metapath U-A-U": 0.0, "metapath U-U-A-U": 1 / 3,
               "metapath U-U-U-A-U": 0.5, "deepwalk": 1.0,
               "U-A-U rare-artist a=1": 0.0}


def runs(name):
    """The three per-seed result dicts for a strategy, whichever task it belongs to."""
    if name in T3:
        return [P1_0[name]] + [P1_S[f"{name} | seed{s}"] for s in (1, 2)]
    if name in CT:
        return [CTL[f"{name}|seed{s}"] for s in (0, 1, 2)]
    return [P2[f"{name}|seed{s}"] for s in (0, 1, 2)]


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
ALL = T3 + CT + T4
S = {n: {k: np.array([f(r) for r in runs(n)]) for k, f in M.items()} for n in ALL}
ORDER = list(M)

# ------------------------------------------------------------------ table 1: combined
best = {k: max(ALL, key=lambda n: S[n][k].mean()) for k in ORDER}
print("% ---- TABLE 1: combined Task 3 + Task 4, mean over seeds {0,1,2}")
for group, names in (("TASK 3 (social graph G)", T3),
                     ("BUDGET CONTROLS (social graph G)", CT),
                     ("TASK 4 (heterogeneous graph H)", T4)):
    print(f"% -- {group}")
    for n in names:
        cells = [f"\\textbf{{{S[n][k].mean():.4f}}}" if best[k] == n else f"{S[n][k].mean():.4f}"
                 for k in ORDER]
        print(f"{TEX[n]} & " + " & ".join(cells) + " \\\\")

print(f"\n% ---- noise floor: mean within-strategy sd over all {len(ALL)} strategies")
nf = {k: np.mean([S[n][k].std(ddof=1) for n in ALL]) for k in ORDER}
print("\\textit{noise floor (mean sd)} & "
      + " & ".join(f"{nf[k]:.4f}" for k in ORDER) + " \\\\")

# ------------------------------------------------------------------ table 2: degree breakdown
LBL = ["$0$ (cold)", "$1$", "$2$--$3$", "$4$--$7$", "$8$--$15$", "$\\ge 16$"]
SHOW = ["deepwalk x15", "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U"]


def bstat(name, col, i, split="test"):
    return np.array([r["lp"][split][1][col].iloc[i] for r in runs(name)])


print("\n% ---- TABLE 2: per-source-degree breakdown, TEST split, mean over seeds {0,1,2}")
print("%      source degree is degree in G_train (the SOCIAL graph) in every row")
nq = P1_0["deepwalk"]["lp"]["test"][1]["n_queries"].to_numpy()
for i, lab in enumerate(LBL):
    cells = [lab, str(int(nq[i]))]
    mu = {(n, c): bstat(n, c, i).mean() for n in SHOW for c in ("hit_at_1", "MRR")}
    top = {c: max(SHOW, key=lambda n: mu[(n, c)]) for c in ("hit_at_1", "MRR")}
    for n in SHOW:
        for c in ("hit_at_1", "MRR"):
            v = f"{mu[(n, c)]:.4f}"
            cells.append(f"\\textbf{{{v}}}" if top[c] == n else v)
    print(" & ".join(cells) + " \\\\")

print("\n% ---- inline: per-bucket deltas vs Task-3 DeepWalk, test hit@1")
for n in T4:
    print(f"% {n}: "
          + ", ".join(f"{bstat(n,'hit_at_1',i).mean()-bstat('deepwalk','hit_at_1',i).mean():+.4f}"
                      for i in range(6)))

print("\n% ---- inline: cold bucket (deg 0), test, per-seed values")
for n in ["deepwalk", "triadic"] + T4:
    v = bstat(n, "hit_at_1", 0)
    print(f"% {n}: hit@1 {v.mean():.4f} +- {v.std(ddof=1):.4f}  (seeds {np.round(v,4).tolist()})"
          f"  MRR {bstat(n,'MRR',0).mean():.4f}")

print("\n% ---- inline: aggregate table, best/worst/spread per column")
for k in ORDER:
    mu = {n: S[n][k].mean() for n in ALL}
    lo, hi = min(mu, key=mu.get), max(mu, key=mu.get)
    print(f"% {k}: best {hi} {mu[hi]:.4f} | worst {lo} {mu[lo]:.4f} | "
          f"spread {mu[hi]-mu[lo]:.4f} | noise {nf[k]:.4f} | ratio {(mu[hi]-mu[lo])/nf[k]:.2f}")

print("\n% ---- inline: social-step fraction sweep (test hit@1 overall vs cold bucket)")
for n in ["metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U", "deepwalk"]:
    ov, cold = S[n]["lp_test_hit"], bstat(n, "hit_at_1", 0)
    print(f"% social={SOCIAL_FRAC[n]:.3f} {n}: overall {ov.mean():.4f}+-{ov.std(ddof=1):.4f} "
          f" cold {cold.mean():.4f}+-{cold.std(ddof=1):.4f}")

print("\n% ---- inline: rare-artist vs plain U-A-U")
for k in ORDER:
    a, b = S["metapath U-A-U"][k], S["U-A-U rare-artist a=1"][k]
    print(f"% {k}: plain {a.mean():.4f} rare {b.mean():.4f} delta {b.mean()-a.mean():+.4f} "
          f"({(b.mean()-a.mean())/nf[k]:+.1f} noise sd)")

print("\n% ---- inline: type-blind DeepWalk on H vs metapath U-A-U")
for k in ORDER:
    a, b = S["metapath U-A-U"][k], S["hetero-deepwalk"][k]
    print(f"% {k}: UAU {a.mean():.4f} typeblind {b.mean():.4f} delta {b.mean()-a.mean():+.4f}")

# ------------------------------------------------------------------ corpus / token table
print("\n% ---- TABLE 3: measured Skip-Gram corpus (corpus_size.py)")
ctl_tok = CORPUS["deepwalk x22"][1]
for n in ["deepwalk", "deepwalk x15", "deepwalk x22", "hetero-deepwalk",
          "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U"]:
    w, t = CORPUS[n]
    print(f"% {n:24s} walks {w:8,}  tokens {t:10,}  mean_len {t/w:5.1f}  "
          f"vs x22 {100*(t/ctl_tok-1):+6.1f}%")
uuu_tok = CORPUS["metapath U-U-U-A-U"][1]
for nm in ("deepwalk x15", "deepwalk x22"):
    print(f"% U-U-U-A-U vs {nm}: tokens {uuu_tok:,} vs {CORPUS[nm][1]:,} "
          f"= {100*(uuu_tok/CORPUS[nm][1]-1):+.1f}%")

print("\n% ---- inline: THE CONTROLS. U-U-U-A-U vs BOTH controls")
print("%      x22 = walk-matched (round 1, gave the control ~50% more tokens)")
print("%      x15 = token-matched (round 2 fix; control still has +2.6% tokens)")
for k in ORDER:
    x10, x15, x22 = S["deepwalk"][k], S["deepwalk x15"][k], S["deepwalk x22"][k]
    uuu = S["metapath U-U-U-A-U"][k]
    print(f"% {k}: x10 {x10.mean():.4f} x15 {x15.mean():.4f} x22 {x22.mean():.4f} "
          f"| U-U-U-A-U {uuu.mean():.4f} "
          f"| vs x15 {uuu.mean()-x15.mean():+.4f} ({(uuu.mean()-x15.mean())/nf[k]:+.1f} sd) "
          f"| vs x22 {uuu.mean()-x22.mean():+.4f} ({(uuu.mean()-x22.mean())/nf[k]:+.1f} sd)")
print("% budget alone (x10 -> x15 -> x22), per column:")
for k in ORDER:
    x10, x15, x22 = S["deepwalk"][k].mean(), S["deepwalk x15"][k].mean(), S["deepwalk x22"][k].mean()
    print(f"%   {k}: {x10:.4f} -> {x15:.4f} ({x15-x10:+.4f}) -> {x22:.4f} ({x22-x10:+.4f} total)")

COLD = ["deepwalk", "deepwalk x15", "deepwalk x22", "metapath U-A-U", "metapath U-U-A-U",
        "metapath U-U-U-A-U"]
# NB (round 3): an earlier version anchored this bucket on chance = 1/21, on the theory that
# an all-zero source row ties all 21 candidates.  That is FALSE and was measured false in
# tie_check.py: with u=0, _pair_features still emits |u-v|=|v| and ||u-v||=||v||, which vary
# by candidate, so 0 of 216 cold queries are fully tied (median 20 distinct scores).  The
# tiebreak vector is also constant (evaluate_ranking is never passed a seed), so it adds no
# variance.  The cold bucket is therefore anchored on the MEASURED token-matched control.
CREF = "deepwalk x15"
print(f"\n% ---- inline: COLD bucket, anchored on the measured control ({CREF})")
print(f"% (chance would be 1/21 = {CHANCE:.4f}; the social-only baselines sit ABOVE it "
      f"because the ranker falls back on candidate-only features -- see tie_check.log)")
for nm in COLD:
    c = bstat(nm, "hit_at_1", 0)
    print(f"% cold {nm:22s}: {c.mean():.4f} +- {c.std(ddof=1):.4f}  "
          f"(seeds {np.round(c,4).tolist()})  MRR {bstat(nm,'MRR',0).mean():.4f}")
cold_nf = np.mean([bstat(n, "hit_at_1", 0).std(ddof=1) for n in COLD])
ctl0 = bstat(CREF, "hit_at_1", 0).mean()
print(f"% cold-bucket noise floor (mean sd over those {len(COLD)}): {cold_nf:.4f}")
print(f"% cold reference ({CREF}) = {ctl0:.4f}")
for nm in ("metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U"):
    d = bstat(nm, "hit_at_1", 0).mean()
    print(f"% cold {nm} vs {CREF}: ratio {d/ctl0:.2f}x, gap {d-ctl0:.4f} "
          f"= {(d-ctl0)/cold_nf:.1f} cold-bucket sd")
