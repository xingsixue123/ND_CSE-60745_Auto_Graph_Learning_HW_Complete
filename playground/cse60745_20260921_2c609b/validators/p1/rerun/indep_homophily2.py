"""
Round 2: which edge set reproduces Zhu et al.'s published h?

The worker's round-2 homophily.py computes h over data.edge_index (STORED DIRECTED
ENTRIES), with self-loops now included. But Table 1's |E| column is UNIQUE UNORDERED
PAIRS with self-loops counted once. Those are different denominators for the six
natively-directed benchmarks.

This recomputes both, from the raw Geom-GCN files, no PyG and no worker code.
"""
import os

W = "/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/problems/p1/data"
SETS = [
    ("Cornell", f"{W}/WebKB/cornell/raw", 0.30),
    ("Texas", f"{W}/WebKB/texas/raw", 0.11),
    ("Wisconsin", f"{W}/WebKB/wisconsin/raw", 0.21),
    ("Actor", f"{W}/Actor/raw", 0.22),
    ("Chameleon", f"{W}/Wiki/chameleon/geom_gcn/raw", 0.23),
    ("Squirrel", f"{W}/Wiki/squirrel/geom_gcn/raw", 0.22),
]
# what answer.tex Table 1 prints in the |E| column
TABLE_E = {"Cornell": 280, "Texas": 295, "Wisconsin": 466,
           "Actor": 26752, "Chameleon": 31421, "Squirrel": 198493}


def load(d):
    lab = {}
    with open(os.path.join(d, "out1_node_feature_label.txt")) as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                lab[int(p[0])] = int(p[2])
    E = []
    with open(os.path.join(d, "out1_graph_edges.txt")) as f:
        next(f)
        for line in f:
            p = line.split()
            if len(p) >= 2:
                E.append((int(p[0]), int(p[1])))
    return lab, E


print(f"{'dataset':11s} {'unord+SL':>9s} {'dirent+SL':>10s} {'pub':>5s} "
      f"{'|E|unord':>9s} {'tableE':>8s} {'nDirEnt':>9s}")
print("-" * 70)
for name, d, pub in SETS:
    lab, E = load(d)
    loops = {u for u, v in E if u == v}
    nosl = [(u, v) for u, v in E if u != v]
    unord = {(min(u, v), max(u, v)) for u, v in nosl}
    dirent = set(nosl)                      # PyG coalesces duplicate directed entries

    n_un = len(unord) + len(loops)
    h_un = (sum(1 for u, v in unord if lab[u] == lab[v]) + len(loops)) / n_un
    n_di = len(dirent) + len(loops)
    h_di = (sum(1 for u, v in dirent if lab[u] == lab[v]) + len(loops)) / n_di

    print(f"{name:11s} {h_un:9.4f} {h_di:10.4f} {pub:5.2f} "
          f"{n_un:9,d} {TABLE_E[name]:8,d} {n_di:9,d}")

print()
print("Deviation from Zhu et al. published value, per convention:")
tot_un = tot_di = 0.0
for name, d, pub in SETS:
    if name == "Cornell":
        continue                            # known irreproducible under any convention
    lab, E = load(d)
    loops = {u for u, v in E if u == v}
    nosl = [(u, v) for u, v in E if u != v]
    unord = {(min(u, v), max(u, v)) for u, v in nosl}
    dirent = set(nosl)
    h_un = (sum(1 for u, v in unord if lab[u] == lab[v]) + len(loops)) / (len(unord) + len(loops))
    h_di = (sum(1 for u, v in dirent if lab[u] == lab[v]) + len(loops)) / (len(dirent) + len(loops))
    tot_un += abs(h_un - pub)
    tot_di += abs(h_di - pub)
    print(f"  {name:11s} unord {abs(h_un-pub):.4f}   dirent {abs(h_di-pub):.4f}")
print(f"  {'TOTAL':11s} unord {tot_un:.4f}   dirent {tot_di:.4f}")
