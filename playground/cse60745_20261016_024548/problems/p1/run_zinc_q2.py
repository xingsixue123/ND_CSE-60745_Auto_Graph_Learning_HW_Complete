"""Q2 table: masking strategies on ZINC, 30 epochs, plus their pair counts.

  OMP_NUM_THREADS=8 ../../.venv-gt/bin/python -u run_zinc_q2.py 2>&1 | tee logs/zinc_q2.log
"""
import json

from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer
from experiments import STRATEGIES, count_pairs
from runner import make_runner

run, results = make_runner("logs/zinc_q2_results.json")

print("\n=== Q2: masking strategies, ZINC, 30 epochs ===")
print("pairs per graph, averaged over the 10000 training molecules (full attention = n^2):")
counts = {}
for name, cls in STRATEGIES.items():
    p, full, per_node = count_pairs(cls, ZINC_GRAPHS["train"])
    counts[name] = dict(pairs=p, full=full, per_node=per_node)
    print(f"  {name:26} {p:8.1f} pairs/graph ({100 * p / full:5.1f}% of full), "
          f"{per_node:5.1f} per node")
with open("logs/zinc_pair_counts.json", "w") as f:
    json.dump(counts, f, indent=1)
print()
for name, cls in STRATEGIES.items():
    run(f"sparse: {name}", LapPETransformer(attention_cls=cls))
print("\ndone")
