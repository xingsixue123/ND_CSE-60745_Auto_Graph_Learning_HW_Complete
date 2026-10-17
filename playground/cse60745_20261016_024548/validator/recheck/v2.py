import numpy as np, torch, math, scipy.sparse as sp
from gt_framework import *
from solution import pair_set, SparseSPDAttention, SPDAttention, LapPETransformer

tr = ZINC_GRAPHS["train"]

def two_hop_extra(ei, n):
    A = sp.coo_matrix((np.ones(ei.size(1)), (ei[0].numpy(), ei[1].numpy())), shape=(n,n)).tocsr()
    b = ((A + A@A) > 0).tocoo()
    return [torch.from_numpy(np.stack([b.row, b.col])).long()]

STRATS = {
 "self+edges":        lambda ei,n: pair_set(ei,n,n_cycles=0,virtual=False),
 "+virtual":          lambda ei,n: pair_set(ei,n,n_cycles=0,virtual=True),
 "2hop+virtual(sub)": lambda ei,n: SparseSPDAttention.attention_pairs(ei,n),
 "+4reg expander":    lambda ei,n: pair_set(ei,n,n_cycles=2,virtual=True),
 "+8reg expander":    lambda ei,n: pair_set(ei,n,n_cycles=4,virtual=True),
}
print("=== ZINC train, mean pairs/graph (n^2 mean = 556.8) ===")
for name,f in STRATS.items():
    tot = sum(f(g["edge_index"], g["n"]).size(1) for g in tr)
    m = tot/len(tr)
    print(f"  {name:20} {m:8.1f}  {100*m/556.8:5.1f}% of full")

print("=== LastFM pairs ===")
L=LASTFM
for name,f in STRATS.items():
    p = f(L["edge_index"], L["n"])
    print(f"  {name:20} {p.size(1):>12,}  {100*p.size(1)/L['n']**2:7.3f}%")
print(f"  full                 {L['n']**2:>12,}")
