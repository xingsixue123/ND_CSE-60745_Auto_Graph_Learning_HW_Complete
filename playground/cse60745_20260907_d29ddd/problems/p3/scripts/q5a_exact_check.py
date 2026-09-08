"""Independent confirmation of the EXACT eigenvector centrality.

nx.eigenvector_centrality_numpy is itself a scipy call, so to avoid resting on one
routine we recompute the Perron vector with our own scipy.sparse.linalg.eigsh and
verify the residual ||A x - lambda x||_inf directly.
"""

import json

import networkx as nx
import numpy as np
import scipy.sparse.linalg as spl

from build_graph import build

G, _ = build()
nodes = list(G)
A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csr", dtype=float)

lam, vec = spl.eigsh(A, k=1, which="LA", tol=0, maxiter=100000)
lam = float(lam[0])
v = np.asarray(vec[:, 0]).ravel()
if v.sum() < 0:
    v = -v                      # Perron vector: choose the nonnegative sign
v = v / np.linalg.norm(v)
mine = dict(zip(nodes, v))

resid = np.abs(A @ v - lam * v).max()
print("my eigsh lambda_max        : %.12f" % lam)
print("residual ||Ax - lam x||_inf: %.3e" % resid)
print("min entry (should be >= ~0): %.3e" % v.min())

nx_exact = nx.eigenvector_centrality_numpy(G)
print("\nmax |mine - nx_numpy| over all nodes: %.3e"
      % max(abs(mine[u] - nx_exact[u]) for u in G))


def top10(d):
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:10]


print("\n=== TOP 10, my own eigsh Perron vector ===")
for i, (u, val) in enumerate(top10(mine), 1):
    print("%2d  node %-8d  %.12e  degree %d" % (i, u, val, G.degree(u)))

a = [u for u, _ in top10(mine)]
b = [u for u, _ in top10(nx_exact)]
print("\nordered top-10 identical to nx.eigenvector_centrality_numpy:", a == b)

# ---- assemble the exact numbers that go into the LaTeX table ----------------
default_ec = nx.eigenvector_centrality(G)          # defaults, headline answer
rows = []
for rank, (u, dv) in enumerate(top10(default_ec), 1):
    rows.append({"rank": rank, "node": int(u), "degree": G.degree(u),
                 "default": float(dv), "exact": float(nx_exact[u])})
print("\n=== FINAL TABLE ROWS (ordered by the DEFAULT-parameter values) ===")
print("%4s %8s %6s %22s %22s" % ("rank", "node", "deg", "default", "exact(numpy)"))
for r in rows:
    print("%4d %8d %6d %22.12e %22.12e" % (r["rank"], r["node"], r["degree"],
                                           r["default"], r["exact"]))
print("\nset(top10 default) == set(top10 exact):",
      set(u for u, _ in top10(default_ec)) == set(b))
print("ordered equal:", [u for u, _ in top10(default_ec)] == b)

with open("results/q5a_final_rows.json", "w") as fh:
    json.dump({"lambda_max": lam, "rows": rows,
               "exact_top10": [(int(u), float(val)) for u, val in top10(nx_exact)]},
              fh, indent=2)
print("\nwrote results/q5a_final_rows.json")
