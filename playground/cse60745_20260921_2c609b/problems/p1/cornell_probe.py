import torch
from stats import ROOT
from torch_geometric.datasets import WebKB

for name in ["Cornell", "Texas", "Wisconsin"]:
    d = WebKB(root=f"{ROOT}/WebKB", name=name)[0]
    ei, y = d.edge_index, d.y
    N = d.num_nodes
    src, dst = ei[0], ei[1]

    # 1. edge homophily, self-loops included / excluded
    h_in = float((y[src] == y[dst]).float().mean())
    m = src != dst
    h_ex = float((y[src[m]] == y[dst[m]]).float().mean())

    # 2. node homophily (Pei et al., Geom-GCN): mean over nodes of the fraction of
    #    neighbours sharing the node's label
    fracs = []
    for v in range(N):
        nb = dst[(src == v) & (dst != v)]
        if nb.numel():
            fracs.append(float((y[nb] == y[v]).float().mean()))
    h_node = sum(fracs) / len(fracs)

    # 3. edge homophily over DISTINCT UNDIRECTED pairs (dedup), loops included
    lo = torch.minimum(src, dst).long(); hi = torch.maximum(src, dst).long()
    key = torch.unique(lo * N + hi)
    u, v = key // N, key % N
    h_und = float((y[u] == y[v]).float().mean())

    print(f"{name:10s} h_edge_incl={h_in:.3f}  h_edge_excl={h_ex:.3f}  "
          f"h_node={h_node:.3f}  h_edge_undirected={h_und:.3f}")
