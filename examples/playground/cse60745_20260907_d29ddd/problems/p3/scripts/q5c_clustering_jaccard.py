"""Q5 part (c): average clustering coefficient, and average Jaccard similarity
over all connected node pairs (i.e. over all edges).

Both quantities are computed twice: once with the networkx API and once with a
hand-rolled implementation from raw neighbour sets, so neither number rests on a
single library call.
"""

import json

import networkx as nx

from build_graph import build

G, _ = build()
n, m = G.number_of_nodes(), G.number_of_edges()
print("nx", nx.__version__, "| nodes", n, "edges", m)

out = {"n": n, "m": m}

# ================= average clustering coefficient =================
avg_clust_nx = nx.average_clustering(G)
print("\nnx.average_clustering(G)        = %.16f" % avg_clust_nx)

# hand-rolled: c_u = 2*T_u / (d_u*(d_u-1)), and c_u := 0 when d_u < 2
tri = nx.triangles(G)          # number of triangles through each node
total, n_lowdeg = 0.0, 0
per_node = {}
for u in G:
    d = G.degree(u)
    if d < 2:
        c = 0.0
        n_lowdeg += 1
    else:
        c = 2.0 * tri[u] / (d * (d - 1))
    per_node[u] = c
    total += c
avg_clust_mine = total / n
print("hand-rolled average clustering  = %.16f" % avg_clust_mine)
print("difference                      = %.3e" % abs(avg_clust_nx - avg_clust_mine))
print("nodes with degree < 2 (contribute 0 by convention): %d of %d (%.2f%%)"
      % (n_lowdeg, n, 100.0 * n_lowdeg / n))
print("nodes with clustering > 0       : %d" % sum(1 for c in per_node.values() if c > 0))
print("total triangles in graph        : %d" % (sum(tri.values()) // 3))

# mean over only the nodes of degree >= 2, for context (NOT the reported answer)
deg2 = [c for u, c in per_node.items() if G.degree(u) >= 2]
print("(context) mean over deg>=2 nodes: %.16f  over %d nodes" % (sum(deg2) / len(deg2), len(deg2)))

out["avg_clustering_nx"] = avg_clust_nx
out["avg_clustering_mine"] = avg_clust_mine
out["n_degree_lt_2"] = n_lowdeg
out["n_triangles"] = sum(tri.values()) // 3
out["mean_clustering_deg_ge_2"] = sum(deg2) / len(deg2)

# ================= average Jaccard over all edges =================
# networkx: for edge (u,v), J = |N(u) & N(v)| / |N(u) | N(v)| with RAW neighbour
# sets (so v in N(u) and u in N(v); an isolated edge scores 0).
vals_nx = [p for _, _, p in nx.jaccard_coefficient(G, G.edges())]
avg_j_nx = sum(vals_nx) / len(vals_nx)
print("\n--- Jaccard over all %d edges ---" % m)
print("pairs scored by networkx        = %d  (== m ? %s)" % (len(vals_nx), len(vals_nx) == m))
print("nx.jaccard_coefficient average  = %.16f" % avg_j_nx)

# hand-rolled from raw neighbour sets
nbr = {u: set(G[u]) for u in G}
tot, cnt, n_zero, n_one = 0.0, 0, 0, 0
for u, v in G.edges():
    a, b = nbr[u], nbr[v]
    un = len(a | b)
    j = (len(a & b) / un) if un else 0.0
    tot += j
    cnt += 1
    if j == 0.0:
        n_zero += 1
    if j == 1.0:
        n_one += 1
avg_j_mine = tot / cnt
print("hand-rolled average Jaccard     = %.16f" % avg_j_mine)
print("difference                      = %.3e" % abs(avg_j_nx - avg_j_mine))
print("edges scored                    = %d" % cnt)
print("edges with J == 0               = %d (%.2f%%)" % (n_zero, 100.0 * n_zero / cnt))
print("edges with J == 1               = %d" % n_one)
print("max J = %.6f   min J = %.6f" % (max(vals_nx), min(vals_nx)))

# variant WITHOUT the endpoints in the neighbour sets, to show the convention matters
tot2 = 0.0
for u, v in G.edges():
    a, b = nbr[u] - {v}, nbr[v] - {u}
    un = len(a | b)
    tot2 += (len(a & b) / un) if un else 0.0
print("(variant, endpoints EXCLUDED)   = %.16f   <-- NOT the reported answer" % (tot2 / cnt))

out["avg_jaccard_nx"] = avg_j_nx
out["avg_jaccard_mine"] = avg_j_mine
out["n_edges_scored"] = cnt
out["n_jaccard_zero"] = n_zero
out["max_jaccard"] = max(vals_nx)
out["avg_jaccard_endpoints_excluded"] = tot2 / cnt

with open("results/q5c_clustering_jaccard.json", "w") as fh:
    json.dump(out, fh, indent=2)
print("\nwrote results/q5c_clustering_jaccard.json")
