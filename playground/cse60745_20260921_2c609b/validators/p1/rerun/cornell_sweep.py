"""
Stress-test the answer's claim that Cornell's published h=0.30 (Zhu et al. 2020)
cannot be reproduced "under any standard definition".

The worker tried 4 definitions. I try 10, including the ones it did not:
symmetrised node homophily, self-loop-inclusive node homophily, degree-weighted,
class homophily (Lim et al. 2021), and adjusted homophily (Platonov et al. 2023).
Raw Geom-GCN files only -- no PyG, no worker code.
"""
import os
from collections import defaultdict

W = "/home/xing/project/auto_hw_complete_graph/playground/cse60745_20260921_2c609b/problems/p1/data"
SETS = [("Cornell", f"{W}/WebKB/cornell/raw", 0.30),
        ("Texas", f"{W}/WebKB/texas/raw", 0.11),
        ("Wisconsin", f"{W}/WebKB/wisconsin/raw", 0.21)]


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


for name, d, pub in SETS:
    lab, E = load(d)
    N = len(lab)
    loops = {u for u, v in E if u == v}
    nosl = [(u, v) for u, v in E if u != v]
    dirent = set(nosl)
    unord = {(min(u, v), max(u, v)) for u, v in nosl}

    res = {}
    res["edge dir+SL"] = (sum(1 for u, v in dirent if lab[u] == lab[v]) + len(loops)) / (len(dirent) + len(loops))
    res["edge dir-SL"] = sum(1 for u, v in dirent if lab[u] == lab[v]) / len(dirent)
    res["edge unord+SL"] = (sum(1 for u, v in unord if lab[u] == lab[v]) + len(loops)) / (len(unord) + len(loops))
    res["edge unord-SL"] = sum(1 for u, v in unord if lab[u] == lab[v]) / len(unord)

    # neighbourhoods
    out = defaultdict(set)
    sym = defaultdict(set)
    for u, v in nosl:
        out[u].add(v)
        sym[u].add(v)
        sym[v].add(u)

    def node_h(nb, over_all):
        f = []
        for v in range(N):
            s = nb.get(v, set())
            if s:
                f.append(sum(1 for u in s if lab[u] == lab[v]) / len(s))
            elif over_all:
                f.append(0.0)
        return sum(f) / len(f) if f else float("nan")

    res["node out (nonzero)"] = node_h(out, False)
    res["node out (all N)"] = node_h(out, True)
    res["node sym (nonzero)"] = node_h(sym, False)
    res["node sym (all N)"] = node_h(sym, True)

    # class homophily (Lim et al. 2021)
    C = set(lab.values())
    deg = {v: len(sym.get(v, set())) for v in range(N)}
    tot = sum(deg.values())
    ch = 0.0
    for c in C:
        Vc = [v for v in range(N) if lab[v] == c]
        if not Vc:
            continue
        dc = sum(deg[v] for v in Vc)
        hc = (sum(sum(1 for u in sym[v] if lab[u] == c) for v in Vc) / dc) if dc else 0.0
        ch += max(0.0, hc - len(Vc) / N)
    res["class homophily"] = ch / (len(C) - 1)

    # adjusted homophily (Platonov et al. 2023)
    he = sum(sum(1 for u in sym[v] if lab[u] == lab[v]) for v in range(N)) / tot
    den = sum((sum(deg[v] for v in range(N) if lab[v] == c) / tot) ** 2 for c in C)
    res["adjusted homophily"] = (he - den) / (1 - den)

    print(f"\n{name}  (Zhu et al. published {pub})")
    for k, v in res.items():
        flag = "  <-- MATCHES PUBLISHED" if abs(v - pub) < 0.015 else ""
        print(f"    {k:22s} {v:7.4f}{flag}")
