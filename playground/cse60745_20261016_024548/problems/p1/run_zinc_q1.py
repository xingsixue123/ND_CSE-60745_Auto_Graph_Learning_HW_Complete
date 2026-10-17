"""Q1 table: ZINC, 30 epochs, dense attention.  Baselines + the two encodings + cell 14.

  OMP_NUM_THREADS=8 ../../.venv-gt/bin/python -u run_zinc_q1.py 2>&1 | tee logs/zinc_q1.log
"""
from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SPDAttention
from runner import make_runner

run, results = make_runner("logs/zinc_q1_results.json")

print("\n=== Q1: structural encodings, ZINC, 30 epochs, dense attention ===")
run("none: plain attention", GraphTransformer())
run("demo: centrality + CN", CentralityTransformer(attention_cls=CNAttention))
run("LapPE only", LapPETransformer(attention_cls=Attention))
run("SPD only", GraphTransformer(attention_cls=SPDAttention))
run("LapPE + SPD (cell 14)", LapPETransformer(attention_cls=SPDAttention))
print("\ndone")
