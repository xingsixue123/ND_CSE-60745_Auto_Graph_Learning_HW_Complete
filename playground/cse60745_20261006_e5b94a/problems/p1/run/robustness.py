"""How reproducible are the headline numbers?

(a) three repeats at the harness seed 0 -- torch's multi-threaded scatter_add sums in a
    non-deterministic order, so identical code gives slightly different floats;
(b) seeds 0, 1, 2 -- so the MyDeepConv vs GCN-8 gap is not a one-seed accident.
"""
import json, statistics as st
from common import train_and_eval
from layers import MyGCNConv, MyDeepConv

CFG = {"GCN-2": (MyGCNConv, 2), "GCN-8": (MyGCNConv, 8), "MyDeepConv-8hop": (MyDeepConv, 1)}
out = {}
for tag, (cls, nl) in CFG.items():
    out[tag] = {"repeat_seed0": [], "seeds": {}}
    for r in range(3):
        out[tag]["repeat_seed0"].append(train_and_eval(f"{tag} rep{r}", cls, n_layers=nl)["test_MRR"])
    for s in (0, 1, 2):
        out[tag]["seeds"][s] = train_and_eval(f"{tag} seed{s}", cls, n_layers=nl, seed=s)["test_MRR"]

print()
for tag, d in out.items():
    r = d["repeat_seed0"]; sv = list(d["seeds"].values())
    print(f"{tag:16} seed0 repeats {min(r):.4f}-{max(r):.4f} (spread {max(r)-min(r):.4f}) | "
          f"seeds 0/1/2 mean {st.mean(sv):.4f} range {min(sv):.4f}-{max(sv):.4f}")
json.dump(out, open("logs/robustness.json", "w"), indent=2)
