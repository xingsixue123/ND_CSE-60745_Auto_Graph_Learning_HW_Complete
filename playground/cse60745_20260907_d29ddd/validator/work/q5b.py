import networkx as nx, time
G = nx.read_edgelist('/home/xing/project/auto_hw_complete/input/graph-1.txt', nodetype=int)
try:
    t=time.time(); kc = nx.katz_centrality(G); print('katz OK default %.1fs'%(time.time()-t), flush=True)
except Exception as e:
    print('katz default FAILED:', type(e).__name__, str(e)[:200], flush=True)
    kc = None
if kc:
    print('TOP10 KATZ:')
    for n,v in sorted(kc.items(), key=lambda kv:-kv[1])[:10]: print('  %d  %.6f'%(n,v))
t=time.time()
ac = nx.average_clustering(G)
print('avg clustering coefficient = %.10f  (%.1fs)'%(ac, time.time()-t), flush=True)
t=time.time()
s=0.0; n=0
for u,v,p in nx.jaccard_coefficient(G, G.edges()):
    s+=p; n+=1
print('avg Jaccard over %d connected pairs = %.10f (%.1fs)'%(n, s/n, time.time()-t))
