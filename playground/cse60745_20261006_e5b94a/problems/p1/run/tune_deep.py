"""Select MyDeepConv's two hyper-parameters on VALIDATION MRR only, at K=8.

alpha (teleport probability) and the dropout inside the prediction MLP are the two knobs
the APPNP paper itself exposes. Selection is on val MRR; the test column is printed only
so the final row can be quoted, and plays no part in the choice.
"""
import json
from common import train_and_eval
from layers import MyDeepConv

rows = []
for alpha in (0.1, 0.2, 0.3):
    for drop in (0.0, 0.2, 0.5):
        cls = type("D", (MyDeepConv,), {"__init__": lambda s, i, o, a=alpha, d=drop:
                                        MyDeepConv.__init__(s, i, o, K=8, alpha=a, dropout=d)})
        r = train_and_eval(f"a={alpha} p={drop}", cls, n_layers=1)
        rows.append(dict(alpha=alpha, dropout=drop, **r))

best = max(rows, key=lambda r: r["MRR"])
print(f"\nval-best: alpha={best['alpha']} dropout={best['dropout']} "
      f"val MRR {best['MRR']:.4f} | test MRR {best['test_MRR']:.4f}")
json.dump(rows, open("logs/tune_deep.json", "w"), indent=2)
