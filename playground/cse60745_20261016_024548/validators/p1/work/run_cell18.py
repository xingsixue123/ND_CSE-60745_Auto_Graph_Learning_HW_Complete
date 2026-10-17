"""Notebook cell 18, run three times in one process at a fixed 8 threads.

Two things come out of this.  (1) It is cell 18 against the final SparseSPDAttention, so it
checks that pointing the class at the 2-hop ball and making the sign flip conditional did not
change ZINC: the reference is the "sparse: 2-hop ball+virtual" row of run_zinc_q2.py, measured
before both edits.  (2) The three repeats are identical in every input -- same seed, same
weights, same batch order -- so their spread is pure run-to-run noise: the sparse forward
accumulates with index_add_, whose order across CPU threads is not fixed.

  OMP_NUM_THREADS=8 ../../.venv-gt/bin/python -u run_cell18.py 2>&1 | tee logs/zinc_cell18.log
"""
import json

import torch

from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SparseSPDAttention

print(f"threads: {torch.get_num_threads()}")
runs = []
for r in range(3):
    runs.append(run_graph_task(f"sparse: LapPE + SPD (cell 18, repeat {r + 1})",
                               LapPETransformer(attention_cls=SparseSPDAttention)))
    with open("logs/zinc_cell18_results.json", "w") as f:
        json.dump({"repeats": runs}, f, indent=1)

ref = json.load(open("logs/zinc_q2_results.json"))["sparse: 2-hop ball+virtual"]
for key in ("val", "test"):
    v = [r[key] for r in runs]
    print(f"{key:>5} MAE over 3 identical repeats: {v[0]:.4f} {v[1]:.4f} {v[2]:.4f} | "
          f"spread {max(v) - min(v):.4f} | reference row (before the two edits) {ref[key]:.4f}")
print("\ndone")
