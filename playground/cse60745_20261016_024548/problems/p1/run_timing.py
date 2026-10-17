"""Clean timings for Table 3: one LastFM training step, full attention vs. every masking
strategy.  Run this ALONE on an idle machine -- run_lastfm.py's timings were taken while the
ZINC jobs were using the other cores, so they are not a clean measurement.

  OMP_NUM_THREADS=32 ../../.venv-gt/bin/python -u run_timing.py 2>&1 | tee logs/lastfm_timing.log
"""
from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SPDAttention
from experiments import STRATEGIES


def lastfm_model(attention_cls):
    return LapPETransformer(attention_cls=attention_cls, dim=32, heads=2, layers=2,
                            out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


print("\n=== one training step on LastFM, idle machine (notebook cell 19) ===")
benchmark_step("full: LapPE + SPD", lastfm_model(SPDAttention))
for name, cls in STRATEGIES.items():
    benchmark_step(f"sparse: {name}", lastfm_model(cls))
print("\ndone")
