"""Is the alpha=0.3 choice a plateau or a spike? Refine the alpha grid at dropout=0, K=8.
Selection still on val MRR."""
import json
from common import train_and_eval
from layers import MyDeepConv

rows = []
for alpha in (0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5):
    cls = type("D", (MyDeepConv,), {"__init__": lambda s, i, o, a=alpha:
                                    MyDeepConv.__init__(s, i, o, K=8, alpha=a, dropout=0.0)})
    rows.append(dict(alpha=alpha, **train_and_eval(f"alpha={alpha}", cls, n_layers=1)))
json.dump(rows, open("logs/tune_alpha.json", "w"), indent=2)
