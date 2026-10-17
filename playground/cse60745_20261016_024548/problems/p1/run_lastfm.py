"""LastFM experiments (notebook cell 19): one training step of full vs. sparse attention,
then country classification with the sparse model.

  ../../.venv-gt/bin/python -u run_lastfm.py 2>&1 | tee logs/lastfm.log
"""
import json
import time

from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SPDAttention, SparseSPDAttention
from experiments import STRATEGIES


def lastfm_model(attention_cls):
    return LapPETransformer(attention_cls=attention_cls, dim=32, heads=2, layers=2,
                            out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


t0 = time.time()
print("precomputing LapPE and SPD for the 7624-node LastFM graph ...")
node_fn, pair_fn, _ = precompute_fns(lastfm_model(SPDAttention))
ensure_precomputed([LASTFM], [node_fn, pair_fn])
cache = LASTFM["cache"]
print(f"  lap {tuple(cache[node_fn]['lap'].shape)} {cache[node_fn]['lap'].dtype}, "
      f"spd {tuple(cache[pair_fn]['spd'].shape)} {cache[pair_fn]['spd'].dtype}, "
      f"{time.time() - t0:.1f}s")
spd = cache[pair_fn]["spd"]
hist = {int(d): int((spd == d).sum()) for d in range(-1, 9)}
print(f"  spd histogram (-1 = unreachable, 8 = 8 or more hops): {hist}")

print("\npairs per strategy on LastFM (full attention = 7624^2 = 58,125,376):")
for name, cls in STRATEGIES.items():
    t = time.time()
    try:
        p = cls.attention_pairs(LASTFM["edge_index"], LASTFM["n"]).size(1)
        print(f"  {name:26} {p:12,} pairs ({100 * p / LASTFM['n'] ** 2:6.3f}% of full), "
              f"{p / LASTFM['n']:7.1f} per node, built in {time.time() - t:.1f}s")
    except (MemoryError, RuntimeError) as e:
        print(f"  {name:26} FAILED: {str(e).splitlines()[0][:80]}")

print("\n=== one training step, full vs. sparse (notebook cell 19) ===")
benchmark_step("full: LapPE + SPD", lastfm_model(SPDAttention))
for name in ("local", "local+virtual", "local+expander+virtual"):
    benchmark_step(f"sparse: {name}", lastfm_model(STRATEGIES[name]))

print("\n=== country classification, 200 epochs (notebook cell 19) ===")
best = run_node_task("sparse: LapPE + SPD", lastfm_model(SparseSPDAttention))
with open("logs/lastfm_results.json", "w") as f:
    json.dump({"run_node_task sparse: LapPE + SPD": best}, f, indent=1)
print("\ndone")
