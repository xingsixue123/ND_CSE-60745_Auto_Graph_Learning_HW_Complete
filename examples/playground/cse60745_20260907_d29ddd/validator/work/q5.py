import networkx as nx, time
G = nx.read_edgelist('/home/xing/project/auto_hw_complete/input/graph-1.txt', nodetype=int)
print('G', G.number_of_nodes(), G.number_of_edges(), flush=True)

# (a) eigenvector centrality, default params
try:
    t=time.time(); ec = nx.eigenvector_centrality(G); print('eigen OK default %.1fs'%(time.time()-t), flush=True)
except Exception as e:
    print('eigen default FAILED:', type(e).__name__, e, flush=True)
    ec = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-8)
    print('eigen with max_iter=1000 OK', flush=True)
top = sorted(ec.items(), key=lambda kv:-kv[1])[:10]
print('TOP10 EIGENVECTOR:')
for n,v in top: print('  %d  %.6f'%(n,v))

# numpy cross-check
ec2 = nx.eigenvector_centrality_numpy(G)
top2 = sorted(ec2.items(), key=lambda kv:-abs(kv[1]))[:10]
print('TOP10 EIGENVECTOR (numpy):')
for n,v in top2: print('  %d  %.6f'%(n,v))
