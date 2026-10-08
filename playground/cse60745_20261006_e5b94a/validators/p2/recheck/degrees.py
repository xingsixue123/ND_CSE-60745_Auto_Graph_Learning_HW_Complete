"""Exact |N_r(i)| = 0 counts per relation (in-degree, i.e. the target side of each
edge), and the degree statistics behind the normalisation discussion in answer.tex."""
import torch, rgcn_run as R

g = R.HETERO
N, nu = g["num_nodes"], g["n_users"]
names = ["friend", "listens", "listened_by"]
degs = []
for r in range(3):
    ei = g["edge_index"][:, g["edge_type"] == r]
    d = torch.zeros(N).index_add_(0, ei[1], torch.ones(ei.size(1)))
    degs.append(d)
    print(f"relation {r} {names[r]:12} edges {ei.size(1):>9} | "
          f"|N_r(i)|=0 for {int((d == 0).sum()):>6} of {N} nodes "
          f"({int((d[:nu] == 0).sum())} users, {int((d[nu:] == 0).sum())} artists) | "
          f"mean degree over nodes with |N_r(i)|>0: {float(d[d > 0].mean()):.1f}")
D = torch.stack(degs)
print(f"nodes with |N_r(i)|=0 for at least one r: {int((D == 0).any(0).sum())} of {N}")
print(f"nodes with |N_r(i)|=0 for all three r   : {int((D == 0).all(0).sum())} of {N}")
