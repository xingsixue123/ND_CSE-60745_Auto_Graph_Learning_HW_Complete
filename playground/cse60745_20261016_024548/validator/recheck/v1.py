import numpy as np, torch, math, scipy.sparse as sp
from gt_framework import *            # loads ZINC_GRAPHS, LASTFM
from solution import (laplacian_eigvecs, hop_distances, pair_set,
                      LapPETransformer, SPDAttention, SparseSPDAttention, PAIR_TYPES)

tr = ZINC_GRAPHS["train"]
ns = np.array([g["n"] for g in tr])
print("ZINC train: n min/mean/max =", ns.min(), round(ns.mean(),2), ns.max())
print("mean n^2 over train =", round((ns.astype(float)**2).mean(),1))

# edge_attr range
ea = torch.cat([g["edge_attr"] for g in tr[:3000]])
print("ZINC edge_attr unique:", sorted(set(ea.tolist())))

# degree centrality distribution on ZINC train
deg = torch.cat([torch.bincount(g["edge_index"][0], minlength=g["n"]) for g in tr])
vals, cnt = torch.unique(deg, return_counts=True)
print("ZINC degree values:", vals.tolist(), "fractions:", [round(float(c)/len(deg),4) for c in cnt])

# LastFM: unscaled LapPE channel RMS
L = LASTFM
ev_scaled = laplacian_eigvecs(L["edge_index"], L["n"])     # already * sqrt(n)
unscaled = ev_scaled / math.sqrt(L["n"])
print("LastFM unscaled LapPE per-channel RMS:",
      [round(float(unscaled[:,j].pow(2).mean().sqrt()),4) for j in range(unscaled.size(1))])
print("LastFM scaled   LapPE per-channel RMS:",
      [round(float(ev_scaled[:,j].pow(2).mean().sqrt()),3) for j in range(ev_scaled.size(1))])
