"""Independent recomputation of p3 (Q5) from scratch. Does NOT use worker code."""
import json, sys
import networkx as nx
import numpy as np

PATH = "/home/xing/project/auto_hw_complete/input/graph-1.txt"

# ---------- build graph independently (own parser) ----------
edges = []
seen = set()
selfloops = 0
with open(PATH) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        a, b = line.split("\t")
        u, v = int(a), int(b)
        if u == v:
            selfloops += 1
        key = (u, v) if u < v else (v, u)
        if key in seen:
            print("DUPLICATE", key)
        seen.add(key)
        edges.append((u, v))

G = nx.Graph()
G.add_edges_from(edges)
n, m = G.number_of_nodes(), G.number_of_edges()
ncc = nx.number_connected_components(G)
comps = sorted(nx.connected_components(G), key=len, reverse=True)
degsum = sum(d for _, d in G.degree())
print(f"lines={len(edges)} distinct_undirected={len(seen)} selfloops={selfloops}")
print(f"NODES={n} EDGES={m} COMPONENTS={ncc}")
print(f"largest_cc nodes={len(comps[0])} edges={G.subgraph(comps[0]).number_of_edges()}"
      f" second={len(comps[1])}")
print(f"degree_sum={degsum} 2m={2*m} invariant_ok={degsum == 2*m}")
print(f"nx version={nx.__version__}")

res = {"n": n, "m": m, "ncc": ncc, "lcc_n": len(comps[0]),
       "lcc_m": G.subgraph(comps[0]).number_of_edges(), "second": len(comps[1])}

nodes = list(G.nodes())
idx = {u: i for i, u in enumerate(nodes)}

# ---------- (a) eigenvector centrality ----------
print("\n=== (a) EIGENVECTOR ===")
try:
    ev_def = nx.eigenvector_centrality(G)
    print("DEFAULT CALL: CONVERGED")
    conv = True
except nx.PowerIterationFailedConvergence as e:
    print("DEFAULT CALL: FAILED TO CONVERGE", e)
    ev_def = None
    conv = False

def top10(d):
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:10]

if ev_def:
    t = top10(ev_def)
    print("top10 default:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["ev_default_top10"] = [(u, G.degree(u), val) for u, val in t]

HAVE_SCIPY = True
try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spl
except ImportError:
    HAVE_SCIPY = False

if HAVE_SCIPY:
    ev_np = nx.eigenvector_centrality_numpy(G)
    t = top10(ev_np)
    print("top10 eigenvector_centrality_numpy:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["ev_numpy_top10"] = [(u, G.degree(u), val) for u, val in t]

    # my own power iteration, high precision, on my own sparse matrix
    A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csr", dtype=float)
    x = np.ones(n) / np.sqrt(n)
    for it in range(200000):
        y = A @ x
        nrm = np.linalg.norm(y)
        y = y / nrm
        if np.abs(y - x).sum() < 1e-12:
            x = y
            break
        x = y
    lam = float(x @ (A @ x))
    print(f"my power iteration: iters={it} lambda={lam:.12f}")
    if x.sum() < 0:
        x = -x
    mine = {u: float(x[idx[u]]) for u in nodes}
    t = top10(mine)
    print("top10 my own power iteration:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["ev_mine_top10"] = [(u, G.degree(u), val) for u, val in t]
    res["lambda_max"] = lam
    print(f"max|mine - nx_numpy| = {max(abs(mine[u]-ev_np[u]) for u in nodes):.3e}")

    # residual of the DEFAULT vector
    if ev_def:
        d = np.array([ev_def[u] for u in nodes])
        d = d / np.linalg.norm(d)
        rq = float(d @ (A @ d))
        r_inf = float(np.abs(A @ d - rq * d).max())
        r_l1 = float(np.abs(A @ d - rq * d).sum())
        print(f"default vector: Rayleigh={rq:.7f} inf_resid={r_inf:.3e} L1_resid={r_l1:.3e}")
        res["default_rayleigh"] = rq
        res["default_inf_resid"] = r_inf
        res["default_l1_resid"] = r_l1
        near0 = sum(1 for u in nodes if ev_def[u] < 1e-12)
        print(f"nodes with default centrality < 1e-12: {near0} ({100*near0/n:.2f}%)")
        res["near_zero"] = near0

    # Katz admissibility
    print(f"lambda_max={lam:.12f} 1/lambda_max={1/lam:.12f} alpha=0.1 admissible={0.1 < 1/lam}")
    res["inv_lambda"] = 1 / lam

    # per-component spectral radius (top few)
    radii = []
    for c in comps[:50]:
        if len(c) < 2:
            continue
        sub = G.subgraph(c)
        Ac = nx.to_scipy_sparse_array(sub, format="csr", dtype=float)
        if len(c) < 200:
            w = np.linalg.eigvalsh(Ac.toarray())
            radii.append((float(w.max()), len(c)))
        else:
            w = spl.eigsh(Ac, k=1, which="LA", return_eigenvectors=False)
            radii.append((float(w[0]), len(c)))
    radii.sort(reverse=True)
    print("top 5 component spectral radii:", [(f"{r:.4f}", s) for r, s in radii[:5]])

# ---------- (b) Katz ----------
print("\n=== (b) KATZ ===")
try:
    kz_def = nx.katz_centrality(G)
    print("DEFAULT CALL: CONVERGED")
except nx.PowerIterationFailedConvergence as e:
    print("DEFAULT CALL: FAILED", e)
    kz_def = None

if kz_def:
    t = top10(kz_def)
    print("top10 katz default:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["katz_default_top10"] = [(u, G.degree(u), val) for u, val in t]

if HAVE_SCIPY:
    kz_np = nx.katz_centrality_numpy(G)
    t = top10(kz_np)
    print("top10 katz_centrality_numpy:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["katz_numpy_top10"] = [(u, G.degree(u), val) for u, val in t]

    # my own solve of (I - alpha A) x = beta * 1
    alpha, beta = 0.1, 1.0
    A = nx.to_scipy_sparse_array(G, nodelist=nodes, format="csc", dtype=float)
    M = sp.eye(n, format="csc") - alpha * A
    xk = spl.spsolve(M.tocsc(), beta * np.ones(n))
    print(f"my spsolve: min entry={xk.min():.6f} (positive => admissible)")
    xkn = xk / np.linalg.norm(xk)
    mine_k = {u: float(xkn[idx[u]]) for u in nodes}
    t = top10(mine_k)
    print("top10 my own spsolve:")
    for r, (u, val) in enumerate(t, 1):
        print(f"  {r:2d} node={u:6d} deg={G.degree(u):3d} val={val:.6f}")
    res["katz_mine_top10"] = [(u, G.degree(u), val) for u, val in t]
    if kz_def:
        print(f"max|katz_default - mine| = {max(abs(kz_def[u]-mine_k[u]) for u in nodes):.3e}")
    print(f"max|katz_numpy   - mine| = {max(abs(kz_np[u]-mine_k[u]) for u in nodes):.3e}")

# ---------- (c) clustering + Jaccard ----------
print("\n=== (c) CLUSTERING / JACCARD ===")
ac = nx.average_clustering(G)
print(f"nx.average_clustering = {ac!r}")
res["avg_clustering"] = ac

adj = {u: set(G.neighbors(u)) for u in nodes}
tot = 0.0
deg_lt2 = 0
ge2_vals = []
tri_total = 0
for u in nodes:
    Nu = adj[u]
    d = len(Nu)
    if d < 2:
        deg_lt2 += 1
        continue
    links = 0
    Nl = list(Nu)
    for i in range(len(Nl)):
        for j in range(i + 1, len(Nl)):
            if Nl[j] in adj[Nl[i]]:
                links += 1
    tri_total += links
    c = 2.0 * links / (d * (d - 1))
    tot += c
    ge2_vals.append(c)
my_ac = tot / n
print(f"my hand-rolled average_clustering = {my_ac!r}  diff={abs(my_ac-ac):.3e}")
print(f"deg<2 nodes = {deg_lt2} ({100*deg_lt2/n:.2f}%)  deg>=2 = {n-deg_lt2}")
print(f"mean clustering over deg>=2 nodes = {tot/len(ge2_vals):.6f}")
print(f"triangles (nx.triangles sum/3) = {sum(nx.triangles(G).values())//3}; my links-count/3 = {tri_total//3}")
res["deg_lt2"] = deg_lt2
res["mean_ge2"] = tot / len(ge2_vals)
res["triangles"] = sum(nx.triangles(G).values()) // 3

# Jaccard via networkx
jc = list(nx.jaccard_coefficient(G, G.edges()))
print(f"pairs scored by nx.jaccard_coefficient = {len(jc)} (should equal m={m})")
avg_jc = sum(p for _, _, p in jc) / len(jc)
print(f"nx average Jaccard = {avg_jc!r}")

# hand-rolled, raw neighbour sets
vals = []
for u, v in G.edges():
    Nu, Nv = adj[u], adj[v]
    inter = len(Nu & Nv)
    union = len(Nu | Nv)
    vals.append(inter / union if union else 0.0)
my_j = sum(vals) / len(vals)
print(f"my hand-rolled average Jaccard = {my_j!r}  diff={abs(my_j-avg_jc):.3e}")
print(f"edges scoring 0: {sum(1 for x in vals if x == 0)} ({100*sum(1 for x in vals if x==0)/len(vals):.2f}%)")
print(f"max edge Jaccard = {max(vals):.6f}")
res["avg_jaccard"] = avg_jc
res["zero_edges"] = sum(1 for x in vals if x == 0)
res["max_jaccard"] = max(vals)

# endpoints-excluded variant
vals2 = []
for u, v in G.edges():
    Nu, Nv = adj[u] - {v}, adj[v] - {u}
    union = len(Nu | Nv)
    vals2.append(len(Nu & Nv) / union if union else 0.0)
print(f"endpoints-excluded average Jaccard = {sum(vals2)/len(vals2)!r}")
res["avg_jaccard_excl"] = sum(vals2) / len(vals2)

with open(sys.argv[1] if len(sys.argv) > 1 else "indep_results.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
print("\nDONE")
