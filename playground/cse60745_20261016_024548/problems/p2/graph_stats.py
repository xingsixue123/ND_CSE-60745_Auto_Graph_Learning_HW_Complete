"""How far can 4 rounds of message passing reach on ZINC? Measured, not assumed."""
import torch
torch.set_num_threads(1)
from gt_framework import ZINC_GRAPHS

import numpy as np

def bfs_all(ei, n):
    adj = [[] for _ in range(n)]
    for s, d in zip(ei[0].tolist(), ei[1].tolist()):
        adj[s].append(d)
    D = np.full((n, n), -1, dtype=np.int32)
    for s in range(n):
        D[s, s] = 0
        frontier = [s]
        d = 0
        while frontier:
            d += 1
            nxt = []
            for u in frontier:
                for v in adj[u]:
                    if D[s, v] < 0:
                        D[s, v] = d
                        nxt.append(v)
            frontier = nxt
    return D

for split in ["test"]:
    gs = ZINC_GRAPHS[split]
    diam, n_nodes, cov4, cov8 = [], [], [], []
    for g in gs:
        D = bfs_all(g["edge_index"], g["n"])
        assert (D >= 0).all(), "disconnected graph"
        diam.append(int(D.max()))
        n_nodes.append(g["n"])
        cov4.append(float((D <= 4).mean()))
        cov8.append(float((D <= 8).mean()))
    print(f"ZINC {split}: {len(gs)} graphs, nodes {min(n_nodes)}-{max(n_nodes)} "
          f"(mean {np.mean(n_nodes):.1f})")
    print(f"  diameter: mean {np.mean(diam):.1f}, median {int(np.median(diam))}, "
          f"min {min(diam)}, max {max(diam)}")
    print(f"  fraction of node pairs within 4 hops (= the 4-layer MPNN's reach): "
          f"mean {np.mean(cov4)*100:.1f}%")
    print(f"  fraction of node pairs within 8 hops: mean {np.mean(cov8)*100:.1f}%")
    print(f"  graphs whose diameter is <= 4: {np.mean(np.array(diam) <= 4)*100:.1f}%")

# how much does the degree-centrality encoding actually say about a node?
import collections
cnt = collections.Counter()
for split in ("train", "val", "test"):
    for g in ZINC_GRAPHS[split]:
        cnt.update(torch.bincount(g["edge_index"][0], minlength=g["n"]).tolist())
tot = sum(cnt.values())
print("\ndegree distribution over all ZINC nodes (the whole absolute encoding HybridGT has):")
for d in sorted(cnt):
    print(f"  degree {d}: {cnt[d]:7d} nodes ({100*cnt[d]/tot:5.1f}%)")
print(f"  -> {len(cnt)} distinct values over {tot} nodes")
