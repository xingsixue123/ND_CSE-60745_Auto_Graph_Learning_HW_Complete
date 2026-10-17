"""Ablations of the two LapPE design choices, ZINC, 30 epochs, SPD attention throughout.

  OMP_NUM_THREADS=4 ../../.venv-gt/bin/python -u run_ablation.py 2>&1 | tee logs/zinc_ablation.log
"""
from gt_framework import *                                  # noqa: F401,F403
from solution import SPDAttention
from experiments import NoFlipLapPETransformer, RawLapPETransformer
from runner import make_runner

run, results = make_runner("logs/zinc_ablation_results.json")

print("\n=== Q1 ablations (compare with 'LapPE + SPD (cell 14)' in logs/zinc_q1.log) ===")
run("ablation: no sqrt(n) scaling", RawLapPETransformer(attention_cls=SPDAttention))
run("ablation: no sign flip", NoFlipLapPETransformer(attention_cls=SPDAttention))
print("\ndone")
