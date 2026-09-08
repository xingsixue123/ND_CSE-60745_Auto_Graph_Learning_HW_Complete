"""Spectral radius of the adjacency matrix, and the Katz admissibility check.

Katz centrality x = beta*1 + alpha*A*x  has a convergent Neumann series
(and the standard Katz interpretation) only when alpha < 1/lambda_max.
NetworkX defaults are alpha=0.1, beta=1.0, so we must check lambda_max < 10.
"""

import networkx as nx
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

from build_graph import build

G, _ = build()
nodes = list(G)
A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csr", dtype=float)
print("A shape", A.shape, "nnz", A.nnz, "symmetric:", (abs(A - A.T) > 1e-12).nnz == 0)

# largest-magnitude eigenvalue of the whole (disconnected) adjacency matrix
vals, vecs = spl.eigsh(A, k=3, which="LA", tol=0)
vals = np.sort(vals)[::-1]
print("\ntop-3 eigenvalues (LA):", vals)
lam = float(vals[0])
print("lambda_max            = %.12f" % lam)
print("1/lambda_max          = %.12f" % (1.0 / lam))
print("networkx default alpha= 0.1")
print("is 0.1 < 1/lambda_max ?", 0.1 < 1.0 / lam)

# sanity: lambda_max >= sqrt(max degree) and >= mean degree
maxdeg = max(d for _, d in G.degree())
print("\nmax degree %d -> sqrt = %.4f (lower bound on lambda_max)" % (maxdeg, maxdeg ** 0.5))
print("lambda_max <= max degree ? %s (%.4f <= %d)" % (lam <= maxdeg, lam, maxdeg))

# per-component spectral radii: which component carries the Perron vector?
print("\n--- spectral radius of the 5 largest components ---")
comps = sorted(nx.connected_components(G), key=len, reverse=True)[:5]
for c in comps:
    sub = G.subgraph(c)
    if sub.number_of_nodes() < 3:
        continue
    Asub = nx.to_scipy_sparse_array(sub, format="csr", dtype=float)
    k = min(2, Asub.shape[0] - 1)
    v = spl.eigsh(Asub, k=k, which="LA", tol=0, return_eigenvectors=False)
    print("  component n=%-6d m=%-6d  lambda_max=%.10f"
          % (sub.number_of_nodes(), sub.number_of_edges(), max(v)))

# the true global max over ALL components (small ones could in principle win)
best, best_c = -1.0, None
for c in nx.connected_components(G):
    sub = G.subgraph(c)
    n = sub.number_of_nodes()
    if n == 1:
        r = 0.0
    elif n == 2:
        r = 1.0
    else:
        Asub = nx.to_scipy_sparse_array(sub, format="csr", dtype=float).toarray()
        r = float(np.max(np.linalg.eigvalsh(Asub)))
    if r > best:
        best, best_c = r, c
print("\nmax spectral radius over all 4104 components: %.12f (component size %d)"
      % (best, len(best_c)))
print("matches global lambda_max ?", abs(best - lam) < 1e-8)

np.save("results/lambda_max.npy", np.array([lam]))
