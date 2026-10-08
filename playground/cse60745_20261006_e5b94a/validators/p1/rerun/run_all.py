"""Every number reported in answer.tex.

Main table: GraphSAGE (control), GCN(2), GAT, GIN, GCN(8), MyDeepConv(8 hops).
Depth sweep for fig_p1_depth.pdf: receptive field 2/4/6/8 for MyGCNConv (= n_layers)
and for MyDeepConv (= K, at n_layers=1).

train_and_eval is the notebook's own, unmodified.  The only thing done from outside it
is to subclass MyDeepConv to fix K, because GNNLinkPredictor constructs a layer as
conv_cls(in, out) and gives no other way to pass a hyper-parameter.
"""
import json

from common import MySAGEConv, train_and_eval
from layers import MyGCNConv, MyGATConv, MyGINConv, MyDeepConv


def deep_with_K(k):
    """MyDeepConv with K fixed, so the harness's conv_cls(in, out) call still works."""
    return type(f"MyDeepConv_K{k}", (MyDeepConv,),
                {"__init__": lambda self, i, o, k=k: MyDeepConv.__init__(self, i, o, K=k)})


results, sweep = {}, {"MyGCNConv": {}, "MyDeepConv": {}}

print("=== main table ===")
results["GraphSAGE"] = train_and_eval("GraphSAGE", MySAGEConv, n_layers=2)
results["GCN2"] = train_and_eval("GCN, 2 layers", MyGCNConv, n_layers=2)
results["GAT"] = train_and_eval("GAT", MyGATConv, n_layers=2)
results["GIN"] = train_and_eval("GIN", MyGINConv, n_layers=2)
results["GCN8"] = train_and_eval("GCN, 8 layers", MyGCNConv, n_layers=8)
results["MyDeepConv"] = train_and_eval("MyDeepConv", deep_with_K(8), n_layers=1)

print("\n=== depth sweep: receptive field 2 / 4 / 6 / 8 ===")
for d in (2, 4, 6, 8):
    sweep["MyGCNConv"][d] = train_and_eval(f"GCN hops={d}", MyGCNConv, n_layers=d)
for d in (2, 4, 6, 8):
    sweep["MyDeepConv"][d] = train_and_eval(f"Deep hops={d}", deep_with_K(d), n_layers=1)

json.dump({"results": results, "sweep": sweep}, open("logs/results.json", "w"), indent=2)
print("\nwrote logs/results.json")
