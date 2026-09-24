"""Is answer.tex's claim true that an all-zero embedding row 'scores exactly chance,
1/21 = 0.0476' because 'the scaffolding breaks ties at random'?

Two independent tests:

(A) Static: does evaluate_ranking's tiebreak RNG vary between runs?  If it is seeded
    with a constant, then identical scores => identical ranks => cold-bucket hit@1
    would be IDENTICAL across embedding seeds.  It is not identical in the worker's
    own data, which would disprove the 'ties' mechanism on its own.

(B) Direct: train one social-graph embedding, fit the real LinkPredictor, and look at
    the 21 candidate scores of the cold-source test queries.  Are they tied?
"""
import numpy as np

from scaffold import (load_data, evaluate_ranking, to_query_tensor, flatten_scores,
                      breakdown_by_source_degree)
from impl import LinkPredictor, WalkEmbedding, _unit, _pair_features

G, splits, country, country_split, N = load_data()

test = splits["test"]
ncand = len(test) // int(test["label"].sum())
print(f"(0) candidates per query = {ncand}  -> chance = 1/{ncand} = {1/ncand:.4f}")

# ---------------------------------------------------------------- (A) tiebreak RNG
import inspect
src = inspect.getsource(evaluate_ranking)
print("\n(A) evaluate_ranking signature/tiebreak:")
for line in src.splitlines():
    if "def evaluate_ranking" in line or "default_rng" in line or "tiebreak" in line:
        print("   ", line.strip())
import scaffold
print(f"    evaluate_link_prediction passes a seed? "
      f"{'seed' in inspect.getsource(scaffold.evaluate_link_prediction).split('evaluate_ranking')[1][:40]}")
r1 = np.random.default_rng(0).random(5)
r2 = np.random.default_rng(0).random(5)
print(f"    tiebreak vector is identical across runs: {np.array_equal(r1, r2)}")
print("    => if cold scores were genuinely tied, cold hit@1 would be IDENTICAL")
print("       across embedding seeds. Worker's measured values:")
print("       DeepWalk x15 cold: 0.0880 / 0.0972 / 0.0556   (they differ)")
print("       DeepWalk x22 cold: 0.0602 / 0.0694 / 0.0185   (they differ)")

# ---------------------------------------------------------------- (B) direct probe
print("\n(B) training DeepWalk x15 seed 0 on G_train to inspect real cold-query scores ...")
emb = WalkEmbedding(seed=0, strategy="uniform", num_walks=15, walk_length=40,
                    dim=128, window=5, negative=5, epochs=5)
walks = []
for s in G.nodes():
    walks.extend(emb.sample_walks(G, s))
Z = np.asarray(emb.train_embedding(walks, N), dtype=float)
print(f"    {len(walks):,} walks; Z {Z.shape}; all-zero rows = {int((np.abs(Z).sum(1)==0).sum())}")

pairs, labels, rows = {}, {}, {}
for name in ("train", "val", "test"):
    pairs[name], labels[name], rows[name] = to_query_tensor(
        splits[name], splits[name][["src", "dst"]].to_numpy(),
        positive_first=(name == "train"))
pred = LinkPredictor()
pred.fit(Z, pairs["train"], labels["train"], pairs["val"], labels["val"])
s_test = np.asarray(pred.score(Z, pairs["test"]), dtype=float)

deg = dict(G.degree())
pos = splits["test"][splits["test"]["label"] == 1]
src_per_query = pos["src"].to_numpy()
cold_q = np.flatnonzero(np.array([deg[s] for s in src_per_query]) == 0)
print(f"    cold-source test queries: {len(cold_q)}")

sc = s_test[cold_q]                       # (n_cold, 21)
spread = sc.max(1) - sc.min(1)
n_tied = int((spread < 1e-12).sum())
print(f"    queries whose 21 candidate scores are ALL TIED: {n_tied} / {len(cold_q)}")
print(f"    score spread within a cold query: min {spread.min():.4f}  "
      f"median {np.median(spread):.4f}  max {spread.max():.4f}")
print(f"    distinct scores per cold query: median "
      f"{int(np.median([len(np.unique(np.round(r,12))) for r in sc]))} of {ncand}")

# what the cold ranking actually keys on: source row is zero, so features depend on the
# CANDIDATE only.  Check that the score is a deterministic function of the candidate.
u0 = Z[pos["src"].to_numpy()[cold_q[0]]]
print(f"    (cold source embedding is all-zero: {bool(np.abs(u0).sum()==0)})")

# empirical hit@1 on the cold bucket, this run
flat = flatten_scores(s_test, rows["test"], len(splits["test"]))
metrics, ranks = evaluate_ranking(splits["test"], flat)
bd = breakdown_by_source_degree(splits["test"], ranks, deg)
print(f"\n    this run's cold-bucket hit@1 = {bd['hit_at_1'].iloc[0]:.4f} "
      f"(worker's x15 seed0 = 0.0880)  MRR = {bd['MRR'].iloc[0]:.4f}")
print(f"    chance would be {1/ncand:.4f}")

# binomial check: is 0.0803 (3-seed mean, n=216x3 effective) consistent with chance?
p = 1 / ncand
se1 = np.sqrt(p * (1 - p) / 216)
print(f"\n    one-seed sd if truly chance = {se1:.4f}; 3-seed-mean sd = {se1/np.sqrt(3):.4f}")
for nm, v in (("x10", 0.0447), ("x15", 0.0803), ("x22", 0.0494)):
    print(f"      {nm} cold {v:.4f} -> {(v - p)/(se1/np.sqrt(3)):+.1f} sd from chance")
