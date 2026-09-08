"""Cross-checks for the eigenvector-centrality answer.

(1) Does the DEFAULT nx.eigenvector_centrality call behave the same under the two
    networkx versions available on this machine (3.3 and 3.6.1)? This script is
    pure-python-networkx only (no scipy), so it runs under BOTH interpreters.
(2) Why does the default answer disagree with the exact one at ranks 7/8?
    networkx stops when the L1 change is < n_nodes*tol = 26728*1e-6 = 2.67e-2,
    which is a loose absolute bound; we quantify the residual.
(3) Independent check of the Perron vector via the Rayleigh quotient / residual.
(4) Distribution facts used in the write-up's interpretation.
"""

import json

import networkx as nx

from build_graph import build

G, _ = build()
n = G.number_of_nodes()
print("nx", nx.__version__, "| nodes", n)


def top10(d):
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:10]


ec = nx.eigenvector_centrality(G)   # DEFAULTS
print("\ndefault call succeeded (no PowerIterationFailedConvergence raised)")
print("networkx default stopping rule: L1 change < n*tol = %d * 1e-6 = %.4e" % (n, n * 1e-6))

print("\n=== TOP 10, nx.eigenvector_centrality(G) defaults, nx %s ===" % nx.__version__)
for i, (v, val) in enumerate(top10(ec), 1):
    print("%2d  node %-8d  %.12e  degree %d" % (i, v, val, G.degree(v)))

# --- residual of the returned vector: how close is A x to lambda x ? ----------
# Rayleigh quotient lambda = x^T A x / x^T x   (x is L2-normalised by networkx)
Ax = {u: sum(ec[w] for w in G[u]) for u in G}
xx = sum(val * val for val in ec.values())
lam = sum(ec[u] * Ax[u] for u in G) / xx
resid = max(abs(Ax[u] - lam * ec[u]) for u in G)
l1resid = sum(abs(Ax[u] - lam * ec[u]) for u in G)
print("\nRayleigh quotient of the default vector : %.10f" % lam)
print("max |Ax - lambda x| (inf-norm residual)  : %.3e" % resid)
print("L1 residual                              : %.3e" % l1resid)
print("(exact lambda_max from scipy elsewhere   : 8.762217269069)")

# --- interpretation facts ----------------------------------------------------
vals = sorted(ec.values(), reverse=True)
print("\nnodes with centrality < 1e-12 : %d of %d (%.2f%%)"
      % (sum(1 for v in vals if v < 1e-12), n, 100.0 * sum(1 for v in vals if v < 1e-12) / n))
print("nodes with centrality < 1e-6  : %d (%.2f%%)"
      % (sum(1 for v in vals if v < 1e-6), 100.0 * sum(1 for v in vals if v < 1e-6) / n))
top_nodes = [u for u, _ in top10(ec)]
comp = nx.node_connected_component(G, top_nodes[0])
print("all top-10 lie in the giant component (n=%d): %s"
      % (len(comp), all(u in comp for u in top_nodes)))
# do the top-10 nodes coincide with the top-10 by degree?
topdeg = [u for u, _ in sorted(G.degree(), key=lambda kv: (-kv[1], kv[0]))[:10]]
print("top-10 by degree            :", topdeg)
print("top-10 by eigenvector       :", top_nodes)
print("overlap between the two     :", len(set(topdeg) & set(top_nodes)))

with open("results/q5a_default_nx%s.json" % nx.__version__, "w") as fh:
    json.dump({"nx": nx.__version__,
               "top10": [(int(u), float(v)) for u, v in top10(ec)],
               "rayleigh": lam, "inf_residual": resid}, fh, indent=2)
print("\nwrote results/q5a_default_nx%s.json" % nx.__version__)
