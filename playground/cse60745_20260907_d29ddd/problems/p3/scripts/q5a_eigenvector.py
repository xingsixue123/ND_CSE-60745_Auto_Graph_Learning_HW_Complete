"""Q5 part (a): eigenvector centrality, top-10.

Protocol demanded by problem.md: call the DEFAULT networkx function first and
record honestly whether it converges. Only fall back if it genuinely fails.
"""

import json
import time

import networkx as nx

from build_graph import build

G, _ = build()
print("nx", nx.__version__, "| nodes", G.number_of_nodes(), "edges", G.number_of_edges())

out = {}

# ---------------------------------------------------------------- default call
print("\n--- attempt 1: nx.eigenvector_centrality(G) with DEFAULT parameters ---")
t0 = time.time()
try:
    ec_default = nx.eigenvector_centrality(G)
    out["default_converged"] = True
    print("CONVERGED in %.2f s" % (time.time() - t0))
except nx.PowerIterationFailedConvergence as e:
    ec_default = None
    out["default_converged"] = False
    out["default_error"] = "%s: %s" % (type(e).__name__, e)
    print("FAILED after %.2f s -> %s: %s" % (time.time() - t0, type(e).__name__, e))

# ------------------------------------------------------------- numpy fallback
print("\n--- attempt 2: nx.eigenvector_centrality_numpy(G) (exact, no max_iter) ---")
t0 = time.time()
ec_numpy = nx.eigenvector_centrality_numpy(G)
print("done in %.2f s" % (time.time() - t0))

# --------------------------------------------- raised-max_iter power iteration
print("\n--- attempt 3: power iteration with max_iter=100000, tol=1e-10 ---")
t0 = time.time()
try:
    ec_hi = nx.eigenvector_centrality(G, max_iter=100000, tol=1e-10)
    print("CONVERGED in %.2f s" % (time.time() - t0))
except nx.PowerIterationFailedConvergence as e:
    ec_hi = None
    print("FAILED after %.2f s -> %s" % (time.time() - t0, e))


def top10(d):
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:10]


# networkx's numpy variant can return an eigenvector with an arbitrary sign
# convention; it normalises to unit L2 norm. Report as returned, but check sign.
mn = min(ec_numpy.values())
print("\nec_numpy: min value %.6e  max value %.6e" % (mn, max(ec_numpy.values())))
print("ec_numpy L2 norm: %.10f" % (sum(v * v for v in ec_numpy.values()) ** 0.5))

print("\n=== TOP 10 by eigenvector_centrality_numpy ===")
for i, (n, v) in enumerate(top10(ec_numpy), 1):
    print("%2d  node %-8d  %.12e   degree %d" % (i, n, v, G.degree(n)))

if ec_default is not None:
    print("\n=== TOP 10 by eigenvector_centrality (defaults) ===")
    for i, (n, v) in enumerate(top10(ec_default), 1):
        print("%2d  node %-8d  %.12e   degree %d" % (i, n, v, G.degree(n)))

if ec_hi is not None:
    print("\n=== TOP 10 by eigenvector_centrality (max_iter=100000) ===")
    for i, (n, v) in enumerate(top10(ec_hi), 1):
        print("%2d  node %-8d  %.12e   degree %d" % (i, n, v, G.degree(n)))
    # agreement with the exact numpy answer
    diff = max(abs(ec_hi[n] - ec_numpy[n]) for n in G)
    print("\nmax |power-iteration - numpy| over all nodes: %.3e" % diff)

# which component do the top nodes live in?
top_nodes = [n for n, _ in top10(ec_numpy)]
comp = nx.node_connected_component(G, top_nodes[0])
print("\ncomponent containing the #1 node: %d nodes, %d edges"
      % (len(comp), G.subgraph(comp).number_of_edges()))
print("all top-10 in that same component:", all(n in comp for n in top_nodes))
print("degrees of that component:", sorted((G.degree(n) for n in comp), reverse=True)[:15])

out["top10_numpy"] = [(int(n), float(v)) for n, v in top10(ec_numpy)]
if ec_hi is not None:
    out["top10_hi"] = [(int(n), float(v)) for n, v in top10(ec_hi)]
out["component_of_top1"] = sorted(int(x) for x in comp)
with open("results/q5a_eigenvector.json", "w") as fh:
    json.dump(out, fh, indent=2)
print("\nwrote results/q5a_eigenvector.json")
