"""Round-2 validator recomputation: the NEW val-degree table and the new prose claims."""
import pickle
import numpy as np, pandas as pd

R0 = pickle.load(open("worker_results_full.pkl", "rb"))
RS = pickle.load(open("worker_results_seeds.pkl", "rb"))
NAMES = list(R0.keys())

def trio(name, f):
    return np.array([f(R0[name])] + [f(RS[f"{name} | seed{s}"]) for s in (1, 2)])

# ---------------- TABLE 3: the six val_hit@1_deg* columns, all 7 strategies
print("=== TABLE 3 recomputation: VAL hit@1 by source degree, mean over seeds {0,1,2} ===")
V = {}
for n in NAMES:
    V[n] = np.array([trio(n, lambda r, i=i: r["lp"]["val"][1]["hit_at_1"].iloc[i]).mean()
                     for i in range(6)])
BK = ["0 (cold)", "1", "2-3", "4-7", "8-15", "16+"]
df = pd.DataFrame(V, index=BK).T.round(4)
print(df.to_string())

print("\n  val bucket n_queries:", R0["deepwalk"]["lp"]["val"][1]["n_queries"].tolist())
print("  (answer.tex claims 213, 261, 524, 842, 973, 1358)")
print("  val bucket index    :", [str(x) for x in R0["deepwalk"]["lp"]["val"][1].index.tolist()])

print("\n  argmax per bucket (answer bolds these):")
for i, b in enumerate(BK):
    col = {n: V[n][i] for n in NAMES}
    am = max(col, key=col.get)
    ties = [n for n in NAMES if abs(col[n] - col[am]) < 5e-5]
    print(f"    {b:9s} best = {am:24s} {col[am]:.4f}   ties: {ties}")

print(f"\n  triadic wins {sum(1 for i in range(6) if max(NAMES, key=lambda n: V[n][i])=='triadic')}"
      f"/6 val degree buckets  (answer claims 'only three of the six')")

# ---------------- cross-check Table 3 against run_experiment's own recorded columns
print("\n=== cross-check: Table 3 vs run_experiment's recorded summary row (seed 0) ===")
row = R0["deepwalk"]["summary"]
rec = [row[k] for k in row if k.startswith("val_hit@1_deg")]
direct = [R0["deepwalk"]["lp"]["val"][1]["hit_at_1"].iloc[i] for i in range(6)]
print("  summary row  :", [round(x, 4) for x in rec])
print("  breakdown obj:", [round(x, 4) for x in direct])
print("  identical:", np.allclose(rec, direct))

# ---------------- prose claims
print("\n=== prose claims ===")
vmac = {n: trio(n, lambda r: r["country"].loc["val", "macro_f1"]).mean() for n in NAMES}
sdmac = np.mean([trio(n, lambda r: r["country"].loc["val", "macro_f1"]).std(ddof=1) for n in NAMES])
sp = max(vmac.values()) - min(vmac.values())
print(f"  val macro-F1: triadic {vmac['triadic']:.4f}  deepwalk {vmac['deepwalk']:.4f} "
      f" degcorr {vmac['degcorr a=1']:.4f}")
print(f"    delta triadic-deepwalk = {vmac['triadic']-vmac['deepwalk']:.4f} (claims +0.0194)")
print(f"    noise {sdmac:.4f} (claims 0.0077)  -> {(vmac['triadic']-vmac['deepwalk'])/sdmac:.2f} sd (claims 2.5)")
print(f"    spread {sp:.4f} (claims 0.0411)  ratio {sp/sdmac:.2f} (claims 5.4x)")
print(f"    worst is {min(vmac, key=vmac.get)} (claims deg-corrected 0.6421)")

tmac = {n: trio(n, lambda r: r["country"].loc["test", "macro_f1"]).mean() for n in NAMES}
print(f"  test macro-F1 delta triadic-deepwalk = {tmac['triadic']-tmac['deepwalk']:.4f} (claims +0.0141)")

th = {n: trio(n, lambda r: r["lp"]["test"][0]["hit@1"]).mean() for n in NAMES}
print(f"  test Hit@1 spread = {max(th.values())-min(th.values()):.4f} (claims 0.0198 / '32x')")
tm = {n: trio(n, lambda r: r["lp"]["test"][0]["MRR"]).mean() for n in NAMES}
print(f"  test MRR   spread = {max(tm.values())-min(tm.values()):.4f}")

# bucket-size claim "4-16x smaller than the full split"
vq = np.array(R0["deepwalk"]["lp"]["val"][1]["n_queries"].tolist(), float)
print(f"\n  full val split = 4171 queries; bucket sizes {vq.astype(int).tolist()}")
print(f"  4171/bucket ratios: {np.round(4171/vq, 1).tolist()}  (answer says buckets are '4-16x smaller')")
