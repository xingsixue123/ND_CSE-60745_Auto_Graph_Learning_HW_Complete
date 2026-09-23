"""
Edge homophily ratio for every single-label node-classification benchmark we cite.

    h = |{(u,v) in E : y_u == y_v}| / |E|

This is the "edge homophily" of Zhu et al. (NeurIPS 2020). It is what separates the
classic citation/co-purchase benchmarks (h high) from the WebKB/Actor/Wikipedia
benchmarks (h low), and it is the reason the second group is used as a stress test
for GNNs that assume homophily. Computed, not quoted.

Usage: ./.venv/bin/python homophily.py
"""
import json
import torch
from stats import ROOT
from torch_geometric.datasets import (Planetoid, WebKB, Actor, WikipediaNetwork,
                                      Coauthor, Amazon)


def edge_homophily(data):
    """Edge homophily over DISTINCT UNORDERED PAIRS, self-loops included.

    This must match the edge set that Table 1's |E| column counts, which is
    stats.py's E_und: each unordered pair {u,v} counted once, self-loops counted
    once. Computing instead over data.edge_index (the stored *directed* entries)
    double-weights every reciprocated arc relative to a one-way arc, which for the
    six directed WebKB/Wikipedia/Actor graphs is a different quantity -- that was
    the round-2 defect. For an undirected, self-loop-free graph the two agree
    exactly, which is why the citation/co-authorship/co-purchase rows are unaffected.

    Returns (h_pairs_incl_loops, h_pairs_excl_loops, n_pairs, n_selfloops).
    """
    y = data.y
    N = int(data.num_nodes)
    src, dst = data.edge_index[0].long(), data.edge_index[1].long()

    # canonicalise each edge as the unordered pair (min, max) and deduplicate
    lo = torch.minimum(src, dst)
    hi = torch.maximum(src, dst)
    key = torch.unique(lo * N + hi)
    u, v = key // N, key % N

    same = (y[u] == y[v]).float()
    h_incl = float(same.mean())

    loop = u == v
    n_loops = int(loop.sum())
    h_excl = float(same[~loop].mean())

    return h_incl, h_excl, int(key.numel()), n_loops


def main():
    jobs = [
        ("Cora", lambda: Planetoid(root=f"{ROOT}/Planetoid", name="Cora")),
        ("CiteSeer", lambda: Planetoid(root=f"{ROOT}/Planetoid", name="CiteSeer")),
        ("PubMed", lambda: Planetoid(root=f"{ROOT}/Planetoid", name="PubMed")),
        ("Coauthor CS", lambda: Coauthor(root=f"{ROOT}/Coauthor", name="CS")),
        ("Coauthor Physics", lambda: Coauthor(root=f"{ROOT}/Coauthor", name="Physics")),
        ("Amazon Computers", lambda: Amazon(root=f"{ROOT}/Amazon", name="Computers")),
        ("Amazon Photo", lambda: Amazon(root=f"{ROOT}/Amazon", name="Photo")),
        ("Cornell", lambda: WebKB(root=f"{ROOT}/WebKB", name="Cornell")),
        ("Texas", lambda: WebKB(root=f"{ROOT}/WebKB", name="Texas")),
        ("Wisconsin", lambda: WebKB(root=f"{ROOT}/WebKB", name="Wisconsin")),
        ("Actor", lambda: Actor(root=f"{ROOT}/Actor")),
        ("Chameleon", lambda: WikipediaNetwork(root=f"{ROOT}/Wiki", name="chameleon",
                                               geom_gcn_preprocess=True)),
        ("Squirrel", lambda: WikipediaNetwork(root=f"{ROOT}/Wiki", name="squirrel",
                                              geom_gcn_preprocess=True)),
    ]
    # Published values from Zhu et al., "Beyond Homophily in Graph Neural Networks",
    # NeurIPS 2020, Table 1 -- used purely as an external cross-check.
    published = {"Cora": 0.81, "CiteSeer": 0.74, "PubMed": 0.80, "Cornell": 0.30,
                 "Texas": 0.11, "Wisconsin": 0.21, "Actor": 0.22, "Chameleon": 0.23,
                 "Squirrel": 0.22}

    out = {}
    hdr = (f"{'dataset':20s} {'h_pairs_incl':>13s} {'h_pairs_excl':>13s} "
           f"{'#pairs':>10s} {'#loops':>7s} {'published':>10s} {'match?':>7s}")
    print(hdr)
    print("-" * len(hdr))
    for name, ctor in jobs:
        h_with, h_without, m, nl = edge_homophily(ctor()[0])
        pub = published.get(name)
        ok = "" if pub is None else ("yes" if abs(round(h_with, 2) - pub) < 0.011 else "NO")
        out[name] = dict(h_incl_selfloops=round(h_with, 4),
                         h_excl_selfloops=round(h_without, 4),
                         n_entries=m, n_selfloops=nl, published=pub)
        print(f"{name:20s} {h_with:13.3f} {h_without:13.3f} {m:10,d} {nl:7d} "
              f"{'-' if pub is None else f'{pub:.2f}':>10s} {ok:>7s}")
    json.dump(out, open("homophily_out.json", "w"), indent=2)


if __name__ == "__main__":
    main()
