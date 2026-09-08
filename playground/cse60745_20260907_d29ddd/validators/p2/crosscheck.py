"""p2 — independent verification of every Q3/Q4 count.

Channel A: networkx (whatever version this interpreter has).
Channel B: pure-Python union-find + dicts, no networkx at all.
Both must agree with results.json produced by analyze.py under py311/nx 3.3.
"""
import json
import os
from collections import Counter, defaultdict

EDGE_FILE = "/home/xing/project/auto_hw_complete/input/graph-1.txt"
HERE = os.path.dirname(os.path.abspath(__file__))


def read_edges():
    edges = []
    with open(EDGE_FILE) as fh:
        for line in fh:
            line = line.strip()
            if line:
                a, b = line.split("\t")
                edges.append((int(a), int(b)))
    return edges


def pure_python():
    edges = read_edges()
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)

    parent = {n: n for n in nodes}

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    groups = defaultdict(set)
    for n in nodes:
        groups[find(n)].add(n)
    comps = sorted(groups.values(), key=len, reverse=True)

    deg = Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1

    def induced_edge_count(cset):
        return sum(1 for a, b in edges if a in cset and b in cset)

    return {
        "n_nodes": len(nodes),
        "n_edges": len(set(frozenset(e) for e in edges)),
        "n_components": len(comps),
        "component_sizes_top20": [len(c) for c in comps[:20]],
        "lcc_n_nodes": len(comps[0]),
        "lcc_n_edges": induced_edge_count(comps[0]),
        "cc2_n_nodes": len(comps[1]),
        "cc2_n_edges": induced_edge_count(comps[1]),
        "deg_min": min(deg.values()),
        "deg_max": max(deg.values()),
        "deg_mean": sum(deg.values()) / len(nodes),
    }


def via_networkx():
    import networkx as nx
    G = nx.Graph()
    for a, b in read_edges():
        G.add_edge(a, b)
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    degs = [d for _, d in G.degree()]
    return {
        "networkx_version": nx.__version__,
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "n_components": len(comps),
        "component_sizes_top20": [len(c) for c in comps[:20]],
        "lcc_n_nodes": G.subgraph(comps[0]).number_of_nodes(),
        "lcc_n_edges": G.subgraph(comps[0]).number_of_edges(),
        "cc2_n_nodes": G.subgraph(comps[1]).number_of_nodes(),
        "cc2_n_edges": G.subgraph(comps[1]).number_of_edges(),
        "deg_min": min(degs),
        "deg_max": max(degs),
        "deg_mean": sum(degs) / len(degs),
    }


def main():
    a = via_networkx()
    b = pure_python()
    with open(os.path.join(HERE, "results.json")) as fh:
        ref = json.load(fh)

    keys = [k for k in b if k != "networkx_version"]
    ok = True
    print(f"networkx here = {a['networkx_version']}  (reference run used {ref['networkx_version']})")
    print(f"{'key':<28}{'nx':>22}{'pure-python':>22}{'reference':>22}   match")
    for k in keys:
        va, vb, vr = a[k], b[k], ref[k]
        if isinstance(va, float):
            m = abs(va - vb) < 1e-9 and abs(va - vr) < 1e-9
        else:
            m = (va == vb == vr)
        ok &= m
        sa, sb, sr = (str(v)[:20] for v in (va, vb, vr))
        print(f"{k:<28}{sa:>22}{sb:>22}{sr:>22}   {'OK' if m else 'MISMATCH'}")
    print("\nALL THREE CHANNELS AGREE" if ok else "\n*** DISAGREEMENT ***")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
