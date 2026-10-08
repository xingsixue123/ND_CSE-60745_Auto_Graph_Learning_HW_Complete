"""The depth sweep repeated over three seeds, so fig_p1_depth.pdf can show spread
rather than a single run."""
import json
from common import train_and_eval
from layers import MyGCNConv, MyDeepConv

def deep_with_K(k):
    return type(f"D{k}", (MyDeepConv,),
                {"__init__": lambda s, i, o, k=k: MyDeepConv.__init__(s, i, o, K=k)})

out = {"MyGCNConv": {}, "MyDeepConv": {}}
for d in (2, 4, 6, 8):
    out["MyGCNConv"][d] = [train_and_eval(f"GCN d={d} s={s}", MyGCNConv, n_layers=d,
                                          seed=s)["test_MRR"] for s in (0, 1, 2)]
for d in (2, 4, 6, 8):
    out["MyDeepConv"][d] = [train_and_eval(f"Deep d={d} s={s}", deep_with_K(d), n_layers=1,
                                           seed=s)["test_MRR"] for s in (0, 1, 2)]
json.dump(out, open("logs/sweep_seeds.json", "w"), indent=2)
print()
for k, v in out.items():
    for d, r in v.items():
        print(f"{k:11} hops={d}  seeds {['%.4f' % x for x in r]}  mean {sum(r)/3:.4f}")
