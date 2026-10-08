"""All six table rows across seeds 0/1/2 on the cached node2vec features, so the
submission can say which rows are stable and which are not."""
import json, statistics as st
from common import MySAGEConv, train_and_eval
from layers import MyGCNConv, MyGATConv, MyGINConv, MyDeepConv

CFG = {"GraphSAGE": (MySAGEConv, 2), "GCN-2": (MyGCNConv, 2), "GAT": (MyGATConv, 2),
       "GIN": (MyGINConv, 2), "GCN-8": (MyGCNConv, 8), "MyDeepConv-8hop": (MyDeepConv, 1)}
out = {}
for tag, (cls, nl) in CFG.items():
    out[tag] = [train_and_eval(f"{tag} s={s}", cls, n_layers=nl, seed=s)["test_MRR"]
                for s in (0, 1, 2)]
json.dump(out, open("logs/seeds_all.json", "w"), indent=2)
print()
for tag, v in out.items():
    print(f"{tag:16} seed0 {v[0]:.4f} | seeds 0/1/2 mean {st.mean(v):.4f} "
          f"range {min(v):.4f}-{max(v):.4f}")
