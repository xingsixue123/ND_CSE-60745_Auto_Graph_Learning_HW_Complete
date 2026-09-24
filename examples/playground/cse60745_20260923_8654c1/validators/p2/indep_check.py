"""Validator-independent recomputation of p2's Table 1 and Table 2 from the raw pickles.

Deliberately does NOT import or reuse the worker's make_tables.py.
"""
import pickle
import numpy as np

W = "/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/problems/p2/"
P1 = "/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/problems/p1/"

p1_full = pickle.load(open(P1 + "results_full.pkl", "rb"))
p1_seeds = pickle.load(open(P1 + "results_seeds.pkl", "rb"))
p2 = pickle.load(open(W + "results_hetero.pkl", "rb"))
ctl = pickle.load(open(W + "results_control.pkl", "rb"))

print("p1_full keys:", sorted(p1_full.keys()))
print("p1_seeds keys:", sorted(p1_seeds.keys()))
print("p2 keys:", sorted(p2.keys()))
print("ctl keys:", sorted(ctl.keys()))
print()

T3 = ["deepwalk", "node2vec p=1 q=0.5", "node2vec p=1 q=2", "node2vec p=0.25 q=0.25",
      "rwr r=0.15", "degcorr a=1", "triadic"]
CT = ["deepwalk x22"]
T4 = ["hetero-deepwalk", "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U",
      "U-A-U rare-artist a=1"]
ALL = T3 + CT + T4


def runs(n):
    if n in T3:
        return [p1_full[n]] + [p1_seeds[f"{n} | seed{s}"] for s in (1, 2)]
    if n in CT:
        return [ctl[f"{n}|seed{s}"] for s in (0, 1, 2)]
    return [p2[f"{n}|seed{s}"] for s in (0, 1, 2)]


COLS = [
    ("val H@1",   lambda r: r["lp"]["val"][0]["hit@1"]),
    ("val MRR",   lambda r: r["lp"]["val"][0]["MRR"]),
    ("test H@1",  lambda r: r["lp"]["test"][0]["hit@1"]),
    ("test MRR",  lambda r: r["lp"]["test"][0]["MRR"]),
    ("val miF1",  lambda r: r["country"].loc["val", "micro_f1"]),
    ("val maF1",  lambda r: r["country"].loc["val", "macro_f1"]),
    ("test miF1", lambda r: r["country"].loc["test", "micro_f1"]),
    ("test maF1", lambda r: r["country"].loc["test", "macro_f1"]),
]

print("=== TABLE 1 (independent) : 3-seed means ===")
S = {}
for n in ALL:
    rs = runs(n)
    assert len(rs) == 3, n
    S[n] = {c: np.array([f(r) for r in rs]) for c, f in COLS}
    print(f"{n:28s} " + " ".join(f"{S[n][c].mean():.4f}" for c, _ in COLS))

print("\n=== noise floor (mean within-config sd, ddof=1, over all 13) ===")
nf = {c: np.mean([S[n][c].std(ddof=1) for n in ALL]) for c, _ in COLS}
print(" " * 28 + " " + " ".join(f"{nf[c]:.4f}" for c, _ in COLS))

print("\n=== argmax per column (who should be bolded) ===")
for c, _ in COLS:
    b = max(ALL, key=lambda n: S[n][c].mean())
    print(f"{c:10s} -> {b}  ({S[b][c].mean():.4f})")

print("\n=== bucket structure sanity: every run must have 6 buckets in the same order ===")
ref = None
for n in ALL:
    for j, r in enumerate(runs(n)):
        idx = list(r["lp"]["test"][1].index.astype(str))
        nq = r["lp"]["test"][1]["n_queries"].tolist()
        if ref is None:
            ref = (idx, nq)
            print("reference buckets:", idx)
            print("reference n_queries:", nq, "sum", sum(nq))
        if (idx, nq) != ref:
            print(f"  !! MISMATCH {n} seed{j}: {idx} {nq}")
print("all runs share the same bucket index/n_queries: OK")

print("\n=== TABLE 2 (independent), TEST split, 3-seed means ===")
SHOW = ["deepwalk x22", "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U"]
for i in range(6):
    cells = []
    for n in SHOW:
        h = np.array([r["lp"]["test"][1]["hit_at_1"].iloc[i] for r in runs(n)])
        m = np.array([r["lp"]["test"][1]["MRR"].iloc[i] for r in runs(n)])
        cells += [f"{h.mean():.4f}", f"{m.mean():.4f}"]
    print(f"bucket{i} n={ref[1][i]:5d} " + " ".join(cells))

print("\n=== headline claims ===")
u = S["metapath U-U-U-A-U"]
c22 = S["deepwalk x22"]
d10 = S["deepwalk"]
print(f"U-U-U-A-U test H@1 {u['test H@1'].mean():.4f} - ctl {c22['test H@1'].mean():.4f} "
      f"= {u['test H@1'].mean()-c22['test H@1'].mean():+.4f} "
      f"({(u['test H@1'].mean()-c22['test H@1'].mean())/nf['test H@1']:+.1f} sd)")
print(f"U-U-U-A-U test MRR {u['test MRR'].mean():.4f} - ctl {c22['test MRR'].mean():.4f} "
      f"= {u['test MRR'].mean()-c22['test MRR'].mean():+.4f} "
      f"({(u['test MRR'].mean()-c22['test MRR'].mean())/nf['test MRR']:+.1f} sd)")
print(f"budget alone (x10->x22): H@1 {c22['test H@1'].mean()-d10['test H@1'].mean():+.4f}  "
      f"MRR {c22['test MRR'].mean()-d10['test MRR'].mean():+.4f}  "
      f"miF1 {c22['test miF1'].mean()-d10['test miF1'].mean():+.4f}")
print(f"U-U-U-A-U vs x10 test H@1 = {u['test H@1'].mean()-d10['test H@1'].mean():+.4f}")
print(f"country U-U-U-A-U vs ctl: miF1 {u['test miF1'].mean()-c22['test miF1'].mean():+.4f} "
      f"({(u['test miF1'].mean()-c22['test miF1'].mean())/nf['test miF1']:.1f} sd)  "
      f"maF1 {u['test maF1'].mean()-c22['test maF1'].mean():+.4f} "
      f"({(u['test maF1'].mean()-c22['test maF1'].mean())/nf['test maF1']:.1f} sd)")

print("\n--- rare-artist vs plain U-A-U ---")
for c, _ in COLS:
    a, b = S["metapath U-A-U"][c], S["U-A-U rare-artist a=1"][c]
    print(f"  {c:10s} {a.mean():.4f} -> {b.mean():.4f}  delta {b.mean()-a.mean():+.4f} "
          f"({(b.mean()-a.mean())/nf[c]:+.1f} sd)")

print("\n--- type-blind vs U-A-U test H@1 ---")
print(f"  {S['hetero-deepwalk']['test H@1'].mean()-S['metapath U-A-U']['test H@1'].mean():+.4f}")
print("  all 8 columns typeblind > UAU? ",
      all(S["hetero-deepwalk"][c].mean() > S["metapath U-A-U"][c].mean() for c, _ in COLS))

print("\n--- cold bucket ---")
COLD = ["deepwalk", "deepwalk x22", "metapath U-A-U", "metapath U-U-A-U", "metapath U-U-U-A-U"]
cvals = {}
for n in COLD:
    v = np.array([r["lp"]["test"][1]["hit_at_1"].iloc[0] for r in runs(n)])
    cvals[n] = v
    print(f"  {n:24s} {v.mean():.4f} +- {v.std(ddof=1):.4f}  seeds {np.round(v,4).tolist()}")
cold_nf = np.mean([cvals[n].std(ddof=1) for n in COLD])
print(f"  cold noise floor (mean sd over those 5) = {cold_nf:.4f}")
c0 = cvals["deepwalk x22"].mean()
for n in ("metapath U-A-U", "metapath U-U-U-A-U"):
    d = cvals[n].mean()
    print(f"  {n}: ratio {d/c0:.2f}x gap {d-c0:.4f} = {(d-c0)/cold_nf:.1f} cold sd")
