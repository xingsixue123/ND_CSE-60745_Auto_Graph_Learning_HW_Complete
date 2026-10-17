"""Validator's own reproduction of two Table-2 rows against the delivered solution.py."""
import json, torch
from gt_framework import *            # noqa
from solution import LapPETransformer, SparseSPDAttention
from experiments import STRATEGIES

print("threads:", torch.get_num_threads())
out = {}
for r in range(2):
    out[f"cell18 repeat {r+1}"] = run_graph_task(f"VAL cell18 repeat {r+1}",
                                                 LapPETransformer(attention_cls=SparseSPDAttention))
out["local+virtual"] = run_graph_task("VAL local+virtual",
                                      LapPETransformer(attention_cls=STRATEGIES["local+virtual"]))
out["local"] = run_graph_task("VAL local", LapPETransformer(attention_cls=STRATEGIES["local"]))
print(json.dumps(out, indent=1))
