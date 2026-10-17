"""LastFM country classification (cell 19's run_node_task) for every masking strategy.

Cell 19 only asks for the submitted one; the others are here because Q2 asks for different
masking strategies to be tested, and on the large graph this is the comparison that matters.
Full attention is NOT trained here: one step costs seconds against the sparse models'
milliseconds (Table 3), so 200 epochs of it would dominate the whole experiment budget.

  OMP_NUM_THREADS=16 ../../.venv-gt/bin/python -u run_lastfm_nodetask.py 2>&1 | tee logs/lastfm_nodetask.log
"""
import json

from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer
from experiments import NoFlipLapPETransformer, RawLapPETransformer, STRATEGIES


def lastfm_model(attention_cls, cls=LapPETransformer):
    return cls(attention_cls=attention_cls, dim=32, heads=2, layers=2,
               out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


SUBMITTED = "local+expander+virtual"      # overwritten below once the ZINC seeds have spoken
results = {}
print("\n=== LastFM country classification, 200 epochs (cell 19) ===")
for name, cls in STRATEGIES.items():
    results[name] = run_node_task(f"sparse: {name}", lastfm_model(cls))
    with open("logs/lastfm_nodetask_results.json", "w") as f:
        json.dump(results, f, indent=1)
print("\n=== LapPE ablations on LastFM, submitted pair set ===")
sub = STRATEGIES[SUBMITTED]
for label, cls in (("no sqrt(n) scaling", RawLapPETransformer), ("no sign flip", NoFlipLapPETransformer)):
    results[f"ablation: {label}"] = run_node_task(f"ablation: {label}", lastfm_model(sub, cls))
    with open("logs/lastfm_nodetask_results.json", "w") as f:
        json.dump(results, f, indent=1)
print("\ndone")
