"""Q5 part (b): Katz centrality, top-10.

Defaults in networkx: alpha=0.1, beta=1.0, max_iter=1000, tol=1e-6, normalized=True.
Admissibility alpha < 1/lambda_max was checked in q5_spectrum.py.
"""

import json
import time

import networkx as nx
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl

from build_graph import build

G, _ = build()
print("nx", nx.__version__)

out = {}

# ---------------------------------------------------------------- default call
print("\n--- attempt 1: nx.katz_centrality(G) with DEFAULT parameters ---")
t0 = time.time()
try:
    kz_default = nx.katz_centrality(G)
    out["default_converged"] = True
    print("CONVERGED in %.2f s" % (time.time() - t0))
except nx.PowerIterationFailedConvergence as e:
    kz_default = None
    out["default_converged"] = False
    out["default_error"] = "%s: %s" % (type(e).__name__, e)
    print("FAILED after %.2f s -> %s: %s" % (time.time() - t0, type(e).__name__, e))

# --------------------------------------------------------------- numpy variant
print("\n--- attempt 2: nx.katz_centrality_numpy(G) (exact linear solve) ---")
t0 = time.time()
kz_numpy = nx.katz_centrality_numpy(G)
print("done in %.2f s" % (time.time() - t0))

# --------------------------------------- independent exact solve, my own code
# Katz:  x = (I - alpha*A)^{-1} * beta * 1 ,  then networkx normalises to ||x||_2 = 1
print("\n--- attempt 3: my own sparse solve of (I - alpha A) x = beta*1 ---")
alpha, beta = 0.1, 1.0
nodes = list(G)
A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csc", dtype=float)
M = sp.eye(len(nodes), format="csc") - alpha * A
t0 = time.time()
x = spl.spsolve(M, np.full(len(nodes), beta))
print("done in %.2f s" % (time.time() - t0))
print("min raw x %.6f  max raw x %.6f  (all positive => series converged)"
      % (x.min(), x.max()))
x_norm = x / np.linalg.norm(x)
kz_mine = dict(zip(nodes, x_norm))


def top10(d):
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:10]


print("\nkatz_numpy: L2 norm %.10f, min %.6e"
      % (sum(v * v for v in kz_numpy.values()) ** 0.5, min(kz_numpy.values())))

for name, d in [("katz_centrality (defaults)", kz_default),
                ("katz_centrality_numpy", kz_numpy),
                ("my own sparse solve", kz_mine)]:
    if d is None:
        continue
    print("\n=== TOP 10 by %s ===" % name)
    for i, (n, v) in enumerate(top10(d), 1):
        print("%2d  node %-8d  %.12e   degree %d" % (i, n, v, G.degree(n)))

if kz_default is not None:
    print("\nmax |default - numpy|      : %.3e" % max(abs(kz_default[n] - kz_numpy[n]) for n in G))
print("max |numpy   - my solve|   : %.3e" % max(abs(kz_numpy[n] - kz_mine[n]) for n in G))

# how much do the ranks agree?
if kz_default is not None:
    a = [n for n, _ in top10(kz_default)]
    b = [n for n, _ in top10(kz_numpy)]
    print("\ntop-10 default == top-10 numpy (as ordered list):", a == b)
    print("top-10 sets equal:", set(a) == set(b))

out["top10_default"] = ([(int(n), float(v)) for n, v in top10(kz_default)]
                        if kz_default is not None else None)
out["top10_numpy"] = [(int(n), float(v)) for n, v in top10(kz_numpy)]
out["top10_mine"] = [(int(n), float(v)) for n, v in top10(kz_mine)]
out["degrees"] = {int(n): G.degree(n) for n, _ in top10(kz_numpy)}
with open("results/q5b_katz.json", "w") as fh:
    json.dump(out, fh, indent=2)
print("\nwrote results/q5b_katz.json")
