"""p2 — Q3/Q4 computations. Builds the graph and emits every reported number."""
import json
import os
from collections import Counter

import networkx as nx

EDGE_FILE = "/home/xing/project/auto_hw_complete/input/graph-1.txt"
HERE = os.path.dirname(os.path.abspath(__file__))


def build_graph(path=EDGE_FILE):
    """Pinned convention: simple undirected graph, one edge per line."""
    G = nx.Graph()
    n_lines = 0
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            n_lines += 1
            a, b = line.split("\t")
            G.add_edge(int(a), int(b))
    return G, n_lines


def main():
    G, n_lines = build_graph()

    # --- sanity of the raw file ---
    raw_pairs = []
    with open(EDGE_FILE) as fh:
        for line in fh:
            line = line.strip()
            if line:
                a, b = line.split("\t")
                raw_pairs.append((int(a), int(b)))
    self_loops = sum(1 for a, b in raw_pairs if a == b)
    undirected_multiset = Counter(frozenset(p) for p in raw_pairs)
    dup_undirected = sum(1 for k, v in undirected_multiset.items() if v > 1)

    res = {}
    res["n_lines_in_file"] = n_lines
    res["self_loops_in_file"] = self_loops
    res["duplicate_undirected_edges_in_file"] = dup_undirected
    res["networkx_version"] = nx.__version__

    # --- Q3 ---
    res["n_nodes"] = G.number_of_nodes()
    res["n_edges"] = G.number_of_edges()
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    res["n_components"] = len(comps)
    res["component_sizes_top20"] = [len(c) for c in comps[:20]]

    # --- Q4a: largest connected component ---
    lcc_nodes = comps[0]
    LCC = G.subgraph(lcc_nodes)
    res["lcc_n_nodes"] = LCC.number_of_nodes()
    res["lcc_n_edges"] = LCC.number_of_edges()
    res["lcc_frac_of_nodes"] = LCC.number_of_nodes() / G.number_of_nodes()

    # --- Q4b: second largest connected component (selection rule stated) ---
    cc2_nodes = comps[1]
    CC2 = G.subgraph(cc2_nodes)
    res["cc2_n_nodes"] = CC2.number_of_nodes()
    res["cc2_n_edges"] = CC2.number_of_edges()
    # tie check at 2nd place
    sizes = [len(c) for c in comps]
    res["cc2_size"] = sizes[1]
    res["cc2_tie_count"] = sizes.count(sizes[1])
    res["cc3_size"] = sizes[2]
    res["cc3_tie_count"] = sizes.count(sizes[2])
    res["cc2_is_tree"] = nx.is_tree(CC2)
    res["cc2_max_degree"] = max(d for _, d in CC2.degree())
    res["cc2_diameter"] = nx.diameter(CC2)

    # --- Q4c: degree distribution of the WHOLE graph ---
    degs = [d for _, d in G.degree()]
    res["deg_min"] = min(degs)
    res["deg_max"] = max(degs)
    res["deg_mean"] = sum(degs) / len(degs)
    res["deg_sum"] = sum(degs)
    hist = Counter(degs)
    res["degree_histogram"] = {str(k): hist[k] for k in sorted(hist)}
    res["n_distinct_degrees"] = len(hist)
    res["deg_argmax_node"] = max(G.degree(), key=lambda t: t[1])[0]

    # --- global invariants ---
    res["invariant_degsum_eq_2m"] = (sum(degs) == 2 * G.number_of_edges())
    res["invariant_comp_nodes_sum"] = (sum(sizes) == G.number_of_nodes())
    res["invariant_edges_over_comps"] = (
        sum(G.subgraph(c).number_of_edges() for c in comps) == G.number_of_edges()
    )

    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(res, fh, indent=2)

    lines = []
    for k, v in res.items():
        if k == "degree_histogram":
            v = f"<{len(v)} distinct degrees, see results.json>"
        lines.append(f"{k}: {v}")
    txt = "\n".join(lines)
    with open(os.path.join(HERE, "results.txt"), "w") as fh:
        fh.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
