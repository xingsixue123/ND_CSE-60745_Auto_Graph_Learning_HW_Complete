"""Check the dataset facts that answer.tex states in prose."""
import numpy as np
import scipy.sparse as sp

from gt_framework import *                                  # noqa: F401,F403
from solution import laplacian_eigvecs

ns, ncomp = [], set()
for split, gs in ZINC_GRAPHS.items():
    for g in gs:
        ns.append(g["n"])
        ei, n = g["edge_index"], g["n"]
        A = sp.coo_matrix((np.ones(ei.size(1)), (ei[0].numpy(), ei[1].numpy())), shape=(n, n))
        ncomp.add(sp.csgraph.connected_components(A, directed=False)[0])
print(f"ZINC {len(ns)} graphs: n from {min(ns)} to {max(ns)}; connected components per graph: {sorted(ncomp)}")
print(f"LAP_K = {LAP_K}; smallest graph has {min(ns) - 1} non-trivial eigenvectors available")

g = LASTFM
ei, n = g["edge_index"], g["n"]
A = sp.coo_matrix((np.ones(ei.size(1)), (ei[0].numpy(), ei[1].numpy())), shape=(n, n))
print(f"LastFM n={n}, components={sp.csgraph.connected_components(A, directed=False)[0]}")
V = laplacian_eigvecs(ei, n).numpy()
print(f"LastFM LapPE: scaled channel RMS {np.sqrt((V ** 2).mean(0)).mean():.4f}, "
      f"unscaled {np.sqrt(((V / np.sqrt(n)) ** 2).mean(0)).mean():.5f} (1/sqrt(n) = {1/np.sqrt(n):.5f})")
