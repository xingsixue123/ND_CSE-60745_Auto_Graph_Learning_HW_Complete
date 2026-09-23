"""
Fully independent recomputation of edge homophily for the WebKB / Actor / Wikipedia
graphs, straight from the raw Geom-GCN text files. No PyG, no worker code.

Reports h under several conventions, because the published values (Zhu et al. 2020
Table 1: Cornell .30, Texas .11, Wisconsin .21, Actor .22, Squirrel .22, Chameleon .23)
are computed on the SYMMETRISED, DE-DUPLICATED graph, whereas the raw file is a
directed edge list.
"""
import os

W = "/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/problems/p1/data"

SETS = [
    ("Cornell", f"{W}/WebKB/cornell/raw"),
    ("Texas", f"{W}/WebKB/texas/raw"),
    ("Wisconsin", f"{W}/WebKB/wisconsin/raw"),
    ("Actor", f"{W}/Actor/raw"),
    ("Chameleon", f"{W}/Wiki/chameleon/geom_gcn/raw"),
    ("Squirrel", f"{W}/Wiki/squirrel/geom_gcn/raw"),
]


def load(d):
    lab = {}
    with open(os.path.join(d, "out1_node_feature_label.txt")) as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            lab[int(p[0])] = int(p[2])
    edges = []
    with open(os.path.join(d, "out1_graph_edges.txt")) as f:
        next(f)
        for line in f:
            p = line.split()
            if len(p) < 2:
                continue
            edges.append((int(p[0]), int(p[1])))
    return lab, edges


def h_of(pairs, lab):
    if not pairs:
        return float("nan")
    return sum(1 for u, v in pairs if lab[u] == lab[v]) / len(pairs)


print(f"{'dataset':12s} {'h_raw':>8s} {'h_undir':>8s} {'n_raw':>9s} {'n_undir':>9s}")
print("-" * 52)
for name, d in SETS:
    if not os.path.isdir(d):
        print(f"{name:12s}  MISSING {d}")
        continue
    lab, edges = load(d)
    raw = [(u, v) for u, v in edges if u != v]
    undir = {(min(u, v), max(u, v)) for u, v in raw}
    undir = sorted(undir)
    print(f"{name:12s} {h_of(raw, lab):8.4f} {h_of(undir, lab):8.4f} "
          f"{len(raw):9,d} {len(undir):9,d}")
