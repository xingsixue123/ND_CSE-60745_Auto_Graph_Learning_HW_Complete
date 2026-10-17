"""Seed-robustness check for the Q2 ranking: repeat the masking-strategy comparison
(and dense full attention) under two further seeds.

  OMP_NUM_THREADS=6 ../../.venv-gt/bin/python -u run_seeds.py <seed> 2>&1 | tee logs/zinc_seed<seed>.log

Both the training seed (gt_framework.RANDOM_SEED, read by _reset and run_graph_task) and the
seed of the random expander (solution.RANDOM_SEED, read by pair_set) are moved, and every
cached pair set is dropped so the strategies are rebuilt for the new seed.
"""
import json
import sys

import gt_framework
import solution
from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SPDAttention
from experiments import STRATEGIES
from runner import make_runner

seed = int(sys.argv[1])
gt_framework.RANDOM_SEED = seed
solution.RANDOM_SEED = seed
for split in ZINC_GRAPHS.values():
    for g in split:
        g.pop("pairs", None)                                # force every pair set to be rebuilt

run, results = make_runner(f"logs/zinc_seed{seed}_results.json")
print(f"\n=== Q2 strategies, ZINC, 30 epochs, seed {seed} ===")
run("full attention", LapPETransformer(attention_cls=SPDAttention))
for name, cls in STRATEGIES.items():
    for split in ZINC_GRAPHS.values():
        for g in split:
            g.pop("pairs", None)
    run(f"sparse: {name}", LapPETransformer(attention_cls=cls))
print("\ndone")
