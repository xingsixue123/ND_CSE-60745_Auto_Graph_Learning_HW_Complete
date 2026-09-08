"""Shared graph construction for p3 (Q5).

Pinned convention (from problem.md, shared with worker p2/Q3):
  simple undirected networkx.Graph, one node per distinct integer id appearing in
  the file, one edge per line, tab-separated pair.

Reference numbers to reproduce: 26728 nodes, 26377 edges, 4104 connected components.
"""

import networkx as nx

EDGE_FILE = "/home/xing/project/auto_hw_complete/input/graph-1.txt"


def build():
    G = nx.Graph()
    n_lines = 0
    with open(EDGE_FILE) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            n_lines += 1
            a, b = line.split("\t")
            G.add_edge(int(a), int(b))
    return G, n_lines


if __name__ == "__main__":
    G, n_lines = build()
    print("lines read              :", n_lines)
    print("nodes                   :", G.number_of_nodes())
    print("edges                   :", G.number_of_edges())
    print("connected components    :", nx.number_connected_components(G))
    print("self loops              :", nx.number_of_selfloops(G))
    comps = sorted((len(c) for c in nx.connected_components(G)), reverse=True)
    print("largest component size  :", comps[0])
    print("2nd largest comp size   :", comps[1])
    print("nx version              :", nx.__version__)

    # global invariant: degree sum == 2 * |E|
    deg_sum = sum(d for _, d in G.degree())
    print("degree sum              :", deg_sum, "== 2|E| ?", deg_sum == 2 * G.number_of_edges())
    # duplicate-edge check: lines read vs distinct edges
    print("lines == edges (no dups):", n_lines == G.number_of_edges())
