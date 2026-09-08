import networkx as nx, numpy as np
G = nx.Graph()
for line in open('/home/xing/project/auto_hw_complete/input/graph-1.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    a,b = line.split()[:2]
    G.add_edge(int(a),int(b))
print("nodes",G.number_of_nodes(),"edges",G.number_of_edges())
comps = sorted(nx.connected_components(G), key=len, reverse=True)
print("ncomps",len(comps),"giant",len(comps[0]))

# D1.1: spectral radius of giant vs max over all others
def rho(nodes):
    A = nx.to_numpy_array(G.subgraph(nodes))
    return float(np.max(np.abs(np.linalg.eigvalsh(A))))
rg = rho(comps[0])
others = [(rho(c), len(c), G.subgraph(c).number_of_edges()) for c in comps[1:]]
others.sort(reverse=True)
print("rho(giant) = %.6f" % rg)
print("top-5 rho over non-giant components (rho, |V|, |E|):")
for t in others[:5]: print("   %.4f  n=%d m=%d" % t)

# D1.3: fraction of zero-Jaccard edges
z=0
for u,v in G.edges():
    if len(set(G[u]) & set(G[v]))==0: z+=1
m=G.number_of_edges()
print("zero-jaccard edges =",z,"of",m,"=> %.4f%%  -> rounds to %.1f%%"%(100*z/m, round(100*z/m,1)))
