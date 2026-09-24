"""Round-3: test the claim I made in round 2, that a cold (all-zero) source row makes all
21 candidate scores TIE, so the query scores at chance 1/21.

The validator says that is false: with u = 0, _pair_features still emits |u-v| = |v| and
||u-v|| = ||v||, which vary by candidate, so the predictor ranks on candidate-only
features and the scores are distinct.

This script trains DeepWalk x15 at seed 0 (the token-matched control, cold hit@1 = 0.0880)
and inspects the ACTUAL scores of the 216 cold-source test queries.

    ../../venv/bin/python tie_check.py
"""
import numpy as np

from scaffold import (embed_graph, evaluate_ranking, flatten_scores, load_data,
                      to_query_tensor, RANDOM_SEED)
from impl import LinkPredictor, WalkEmbedding, _pair_features, _unit

G_train, splits, country, country_split, N_USERS = load_data()
BASE = dict(walk_length=40, dim=128, window=5, negative=5, epochs=5)

print("training DeepWalk x15 seed 0 (token-matched control) ...", flush=True)
Z = embed_graph(WalkEmbedding(seed=0, strategy="uniform", num_walks=15, **BASE),
                G_train, N_USERS)[:N_USERS]

deg = dict(G_train.degree())
pairs, labels, rows = {}, {}, {}
for name in ("train", "val", "test"):
    pairs[name], labels[name], rows[name] = to_query_tensor(
        splits[name], splits[name][["src", "dst"]].to_numpy(),
        positive_first=(name == "train"))

lp = LinkPredictor()
lp.fit(Z, pairs["train"], labels["train"], pairs["val"], labels["val"])
S = lp.score(Z, pairs["test"])                      # (n_queries, 21)

test = splits["test"]
qids = test["query_id"].drop_duplicates().to_numpy()
src = test[test["label"] == 1].set_index("query_id").loc[qids, "src"].to_numpy()
cold = np.where(np.array([deg.get(int(s), 0) for s in src]) == 0)[0]
print(f"\ncold-source test queries: {len(cold)}")

# --- 1. is the source row actually all-zero? ---
nz = np.array([np.abs(Z[int(src[i])]).max() for i in cold])
print(f"source rows all-zero: {(nz == 0).sum()} / {len(cold)}")

# --- 2. are the 21 candidate scores tied? ---
ndist = np.array([len(np.unique(np.round(S[i], 9))) for i in cold])
spread = np.array([S[i].max() - S[i].min() for i in cold])
print(f"distinct scores per cold query: min {ndist.min()} median {int(np.median(ndist))} "
      f"max {ndist.max()}  (21 = all distinct, 1 = all tied)")
print(f"queries with ANY tie (<21 distinct): {(ndist < 21).sum()} / {len(cold)}")
print(f"queries fully tied (1 distinct):     {(ndist == 1).sum()} / {len(cold)}")
print(f"score spread max-min: min {spread.min():.3f} median {np.median(spread):.3f} "
      f"max {spread.max():.3f}")

# --- 3. does the tiebreak vector vary between calls? ---
flat = flatten_scores(S, rows["test"], len(test))
m1, _ = evaluate_ranking(test, flat)
m2, _ = evaluate_ranking(test, flat)
r1 = np.random.default_rng(RANDOM_SEED).random(len(test))
r2 = np.random.default_rng(RANDOM_SEED).random(len(test))
print(f"\ntiebreak vector identical across calls: {np.array_equal(r1, r2)} "
      f"(evaluate_ranking is never passed a seed; default = RANDOM_SEED)")
print(f"evaluate_ranking deterministic: {m1 == m2}")

# --- 4. reproduce the reported cold hit@1 ---
_, ranks = evaluate_ranking(test, flat)
pos = test[test["label"] == 1].set_index("query_id")
d = ranks.to_frame("rank")
d["src_degree"] = pos.loc[d.index, "src"].map(deg).to_numpy()
c = d[d["src_degree"] == 0]
print(f"\ncold bucket: n={len(c)} hit@1 {(c['rank']==1).mean():.4f} "
      f"MRR {(1.0/c['rank']).mean():.4f}   (reported x15 seed0 cold hit@1 = 0.0880)")
print(f"chance would be 1/21 = {1/21:.4f}, chance MRR = {np.mean(1/np.arange(1,22)):.4f}")

# --- 5. what would TRUE chance look like? binomial spread on n=216 ---
p = 1 / 21
sd = np.sqrt(p * (1 - p) / len(c))
obs = (c["rank"] == 1).mean()
print(f"\nif cold really were chance: hit@1 ~ {p:.4f} +- {sd:.4f} (binomial sd, n={len(c)})")
print(f"observed {obs:.4f} = {(obs - p)/sd:+.1f} binomial sd above chance")
