import networkx as nx

G = nx.Graph()
for ln in open('/home/xing/project/auto_hw_complete/input/graph-1.txt'):
    p = ln.split()
    if len(p) == 2:
        G.add_edge(int(p[0]), int(p[1]))
print('n,m,c', G.number_of_nodes(), G.number_of_edges(), nx.number_connected_components(G))

# eigenvector, default params
try:
    ev = nx.eigenvector_centrality(G)
    print('EIG default: CONVERGED')
except Exception as e:
    print('EIG default: FAILED ->', type(e).__name__)
    ev = None

evn = nx.eigenvector_centrality_numpy(G)
print('EIG numpy top10:')
for n, v in sorted(evn.items(), key=lambda kv: -kv[1])[:10]:
    print('   %8d  %.6f' % (n, v))
if ev:
    print('EIG default top10:')
    for n, v in sorted(ev.items(), key=lambda kv: -kv[1])[:10]:
        print('   %8d  %.6f' % (n, v))

try:
    kz = nx.katz_centrality(G)
    print('KATZ default: CONVERGED')
except Exception as e:
    print('KATZ default: FAILED ->', type(e).__name__)
    kz = None
kzn = nx.katz_centrality_numpy(G)
print('KATZ numpy top10:')
for n, v in sorted(kzn.items(), key=lambda kv: -kv[1])[:10]:
    print('   %8d  %.6f' % (n, v))

print('avg clustering %.10f' % nx.average_clustering(G))

tot = 0.0
cnt = 0
for u, v, p in nx.jaccard_coefficient(G, G.edges()):
    tot += p
    cnt += 1
print('avg jaccard over %d edges = %.10f' % (cnt, tot / cnt))

import numpy as np
import scipy.sparse.linalg as sla
A = nx.to_scipy_sparse_array(G, format='csr', dtype=float)
lam = sla.eigsh(A, k=1, which='LA', return_eigenvectors=False)[0]
print('lambda_max %.6f  1/lambda_max %.6f  (default alpha=0.1 admissible: %s)' % (lam, 1 / lam, 0.1 < 1 / lam))
