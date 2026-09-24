"""TOKEN-matched control -- the fix for round-2 defect [1.1].

Round 1's control matched Task 4 on walk *count* (DeepWalk x22 = 153,076 walks vs
U-U-U-A-U's 148,000).  But meta-path walks dead-end mid-way, so U-U-U-A-U emits only
4,068,117 tokens against the x22 control's 6,123,040 -- the control was handed 50% more
training data than the row it exists to adjudicate.  gensim's cost and effective data
scale with tokens, not walks (measured: corpus_size.py).

DeepWalk on G_train with num_walks=15 emits 6,958 x 15 x 40 = 4,174,800 tokens, i.e.
+2.6% vs U-U-U-A-U -- a genuine token match, and the small residual still favours the
control, so the comparison stays conservative in the same direction.

Identical code path to control_budget.py: same BASE hyper-parameters, same
embed_graph/evaluate_* from p1, seeds 0,1,2.

    ../../venv/bin/python control_tokens.py
"""
import pickle
import time

import numpy as np

from scaffold import (RESULTS, embed_graph, evaluate_country, evaluate_link_prediction,
                      load_data)
from impl import CountryClassifier, LinkPredictor, WalkEmbedding

G_train, splits, country, country_split, N_USERS = load_data()
n_walkable = sum(1 for _, d in G_train.degree() if d > 0)
NW = 15
tok = n_walkable * NW * 40
print(f"G_train: {n_walkable} non-isolated users; {NW} walks each = {n_walkable*NW:,} walks "
      f"= {tok:,} tokens")
print(f"target (U-U-U-A-U) = 4,068,117 tokens -> {100*(tok/4068117-1):+.1f}%\n", flush=True)

BASE = dict(walk_length=40, dim=128, window=5, negative=5, epochs=5)


def run(name, embedder):
    print(f"[{name}]", flush=True)
    Z = embed_graph(embedder, G_train, N_USERS)[:N_USERS]
    lp = evaluate_link_prediction(Z, LinkPredictor(), splits, G_train)
    cc = evaluate_country(Z, country, CountryClassifier(), country_split)
    v, t = lp["val"][0], lp["test"][0]
    RESULTS[name] = {"summary": {}, "lp": lp, "country": cc}
    print(f"    val hit@1 {v['hit@1']:.4f} MRR {v['MRR']:.4f} | "
          f"test hit@1 {t['hit@1']:.4f} MRR {t['MRR']:.4f} | "
          f"cc test micro {cc.loc['test','micro_f1']:.4f} macro {cc.loc['test','macro_f1']:.4f} | "
          f"cold hit@1 {lp['test'][1]['hit_at_1'].iloc[0]:.4f}", flush=True)


for seed in (0, 1, 2):
    t0 = time.perf_counter()
    run(f"deepwalk x{NW}|seed{seed}",
        WalkEmbedding(seed=seed, strategy="uniform", num_walks=NW, **BASE))
    print(f"    total {time.perf_counter()-t0:.1f}s\n", flush=True)

with open("results_tokens.pkl", "wb") as f:
    pickle.dump(RESULTS, f)

g = lambda k: np.array([RESULTS[f"deepwalk x{NW}|seed{s}"]["lp"]["test"][0][k] for s in (0, 1, 2)])
gv = lambda k: np.array([RESULTS[f"deepwalk x{NW}|seed{s}"]["lp"]["val"][0][k] for s in (0, 1, 2)])
c = lambda k, sp: np.array([RESULTS[f"deepwalk x{NW}|seed{s}"]["country"].loc[sp, k] for s in (0, 1, 2)])
cold = np.array([RESULTS[f"deepwalk x{NW}|seed{s}"]["lp"]["test"][1]["hit_at_1"].iloc[0] for s in (0, 1, 2)])
print(f"\nDeepWalk x{NW} token-matched control (3-seed mean):")
print(f"  val  hit@1 {gv('hit@1').mean():.4f}  MRR {gv('MRR').mean():.4f}")
print(f"  test hit@1 {g('hit@1').mean():.4f}+-{g('hit@1').std(ddof=1):.4f}  "
      f"MRR {g('MRR').mean():.4f}+-{g('MRR').std(ddof=1):.4f}")
print(f"  cc val micro {c('micro_f1','val').mean():.4f} macro {c('macro_f1','val').mean():.4f}")
print(f"  cc test micro {c('micro_f1','test').mean():.4f} macro {c('macro_f1','test').mean():.4f}")
print(f"  cold bucket hit@1 {cold.mean():.4f}+-{cold.std(ddof=1):.4f}")
print("\ncompare U-U-U-A-U: 0.6163 / 0.7361 / 0.7887 / 0.6353 / cold 0.2824")
print(f"        walk-matched x22 control: 0.6179 / 0.7292 / 0.7624 / 0.6852 / cold 0.0494")
print("wrote results_tokens.pkl")
