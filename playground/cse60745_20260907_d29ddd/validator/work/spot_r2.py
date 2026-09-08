import networkx as nx, numpy as np
G=nx.Graph()
for l in open('/home/xing/project/auto_hw_complete/input/graph-1.txt'):
    l=l.strip()
    if not l or l.startswith('#'): continue
    a,b=l.split()[:2]; G.add_edge(int(a),int(b))

top10eig=[16485,22777,14618,21928,2884,1197,9068,17902,1324,25747]
deg=dict(G.degree())
top10deg=[n for n,_ in sorted(deg.items(), key=lambda kv:-kv[1])[:10]]
print("top10 by degree:", top10deg)
print("overlap with eig top10 =", len(set(top10eig)&set(top10deg)), "(claim: 6)")

# exact eigenvector column
ex=nx.eigenvector_centrality_numpy(G)
top_ex=sorted(ex.items(), key=lambda kv:-kv[1])[:10]
print("exact top10:", [(n,round(v,6)) for n,v in top_ex])
claimed_exact={16485:0.492371,22777:0.422581,14618:0.177494,21928:0.139695,2884:0.133861,
               1197:0.133738,17902:0.109103,9068:0.102654,1324:0.100053,25747:0.094399}
bad=[(n,round(abs(ex[n]-v),8)) for n,v in claimed_exact.items() if abs(ex[n]-v)>5e-6]
print("exact-column mismatches >5e-6:", bad if bad else "none")
print("exact puts 17902 ahead of 9068?", ex[17902]>ex[9068], "(claim: yes)")

# default eigenvector column
d=nx.eigenvector_centrality(G)
claimed_def={16485:0.491844,22777:0.419863,14618:0.177656,21928:0.139183,2884:0.133813,
             1197:0.133186,9068:0.111138,17902:0.109219,1324:0.100115,25747:0.094368}
bad=[(n,round(abs(d[n]-v),8)) for n,v in claimed_def.items() if abs(d[n]-v)>5e-6]
print("default-column mismatches >5e-6:", bad if bad else "none")

# max Jaccard over edges
mx=max(len(set(G[u])&set(G[v]))/len(set(G[u])|set(G[v])) for u,v in G.edges())
print("max edge Jaccard = %.6f (claim 2/3=%.6f)"%(mx,2/3))
