"""Independent recomputation of the ZINC facts quoted in answer.tex, using networkx
rather than the worker's hand-rolled BFS."""
import torch, numpy as np, networkx as nx, collections
torch.set_num_threads(1)
from gt_framework import ZINC_GRAPHS

diam, cov4 = [], []
for g in ZINC_GRAPHS["test"]:
    G = nx.Graph()
    G.add_nodes_from(range(g["n"]))
    G.add_edges_from(g["edge_index"].t().tolist())
    assert nx.is_connected(G)
    sp = dict(nx.all_pairs_shortest_path_length(G))
    diam.append(nx.diameter(G))
    n = g["n"]
    within4 = sum(1 for u in sp for v, d in sp[u].items() if d <= 4)
    cov4.append(within4 / (n * n))
print(f"[nx] test graphs {len(diam)}: mean diameter {np.mean(diam):.2f}, median {np.median(diam)}, "
      f"min {min(diam)}, max {max(diam)}")
print(f"[nx] mean fraction of ordered node pairs within 4 hops: {np.mean(cov4)*100:.2f}%")

cnt = collections.Counter()
for split in ("train", "val", "test"):
    for g in ZINC_GRAPHS[split]:
        G = nx.Graph(); G.add_nodes_from(range(g["n"])); G.add_edges_from(g["edge_index"].t().tolist())
        cnt.update(dict(G.degree()).values())
tot = sum(cnt.values())
print(f"[nx] degrees over all {tot} ZINC nodes: " +
      ", ".join(f"{d}:{c} ({100*c/tot:.1f}%)" for d, c in sorted(cnt.items())))
