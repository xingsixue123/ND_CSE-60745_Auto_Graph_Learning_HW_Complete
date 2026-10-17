"""LastFM with the final code: every masking strategy, plus the two LapPE ablations on the
submitted pair set.  Replaces logs/lastfm_nodetask.log, which was measured before the sign
flip was made conditional.

  OMP_NUM_THREADS=10 ../../.venv-gt/bin/python -u run_lastfm_final.py 2>&1 | tee logs/lastfm_final.log
"""
import json

from gt_framework import *                                  # noqa: F401,F403
from solution import LapPETransformer, SparseSPDAttention
from experiments import AlwaysFlipLapPETransformer, RawLapPETransformer, STRATEGIES

SUBMITTED = "2-hop ball+virtual"


def model(attention_cls, cls=LapPETransformer):
    return cls(attention_cls=attention_cls, dim=32, heads=2, layers=2,
               out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)


results = {}


def save():
    with open("logs/lastfm_final_results.json", "w") as f:
        json.dump(results, f, indent=1)


print("\n=== LastFM country classification, 200 epochs (cell 19), final code ===")
for name, cls in STRATEGIES.items():
    results[name] = run_node_task(f"sparse: {name}", model(cls))
    save()

print("\n=== LapPE ablations, submitted pair set ===")
for label, cls in (("ablation: sign flip forced on", AlwaysFlipLapPETransformer),
                   ("ablation: no sqrt(n) scaling", RawLapPETransformer)):
    results[label] = run_node_task(label, model(STRATEGIES[SUBMITTED], cls))
    save()
print("\ndone")
