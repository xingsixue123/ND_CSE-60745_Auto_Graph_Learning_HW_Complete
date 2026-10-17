"""Table 3 timings, measured robustly.

benchmark_step times a single forward+backward, which on a shared CPU is dominated by whatever
else is running: the same sparse model measured 0.06 s with 8 OpenMP threads and 4.74 s with 32
(every strategy hit the same ~4.8 s floor regardless of pair count, i.e. the measurement was
thread-thrash, not work). So: a fixed 8 threads, the step repeated REPEATS times, and the
MINIMUM reported -- the run least disturbed by anything else on the machine. The framework's own
benchmark_step line is printed too, unchanged, for the one cell 19 actually calls.

  ../../.venv-gt/bin/python -u run_timing2.py 2>&1 | tee logs/lastfm_timing2.log
"""
import time

import torch

import gt_framework
from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SPDAttention
from experiments import STRATEGIES

torch.set_num_threads(8)
REPEATS = 7


def lastfm_model(attention_cls):
    return LapPETransformer(attention_cls=attention_cls, dim=32, heads=2, layers=2,
                            out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


def timed(name, model):
    g = LASTFM
    node_fn, pair_fn, pairs_fn = gt_framework._prepare(model, [g])
    model = model.to(DEVICE)
    batch = to_device(make_batch([g], node_fn, pair_fn, pairs_fn))
    n_pairs = batch["pairs"].size(1) if pairs_fn is not None else g["n"] ** 2
    best = float("inf")
    try:
        for _ in range(REPEATS):
            t0 = time.time()
            model(batch).float().sum().backward()
            best = min(best, time.time() - t0)
        print(f"{name:34} pairs attended {n_pairs:>12,} | one step {best:6.2f}s | "
              f"peak GPU memory n/a on CPU")
    except RuntimeError as e:
        print(f"{name:34} pairs attended {n_pairs:>12,} | FAILED: {str(e).splitlines()[0][:80]}")


print(f"\n=== one training step on LastFM, best of {REPEATS}, {torch.get_num_threads()} threads ===")
timed("full: LapPE + SPD", lastfm_model(SPDAttention))
for name, cls in STRATEGIES.items():
    timed(f"sparse: {name}", lastfm_model(cls))

print("\n=== the framework's own benchmark_step, single step, as cell 19 calls it ===")
benchmark_step("full: LapPE + SPD", lastfm_model(SPDAttention))
benchmark_step("sparse: LapPE + SPD", lastfm_model(STRATEGIES["2-hop ball+virtual"]))
print("\ndone")
