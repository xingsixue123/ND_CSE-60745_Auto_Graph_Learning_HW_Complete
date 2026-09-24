"""Validator's independent unit tests of the four TODOs: do they do what answer.tex says?"""
import collections
import numpy as np
from scaffold import load_data, adjacency_lookups
from impl import WalkEmbedding

G, splits, country, csplit, N = load_data()
adj, deg = adjacency_lookups(G)
BASE = dict(num_walks=10, walk_length=40, dim=128, window=5, negative=5, epochs=5)

iso = [u for u in G if deg[u] == 0]
print(f"isolated nodes: {len(iso)}  (answer claims 666), non-isolated {N-len(iso)} (claims 6958)")

STRATS = {
    "uniform": dict(strategy="uniform"),
    "node2vec": dict(strategy="node2vec", p=1.0, q=0.5),
    "rwr": dict(strategy="rwr", restart=0.15),
    "degcorr": dict(strategy="degcorr", alpha=1.0),
    "triadic": dict(strategy="triadic"),
}

print("\n=== shape / contract tests ===")
for name, kw in STRATS.items():
    e = WalkEmbedding(seed=0, **BASE, **kw)
    assert e.sample_walks(G, iso[0]) == [], f"{name}: isolated node must return []"
    bad = 0
    nonedge = 0
    for v in [u for u in G if deg[u] > 0][:5] + [u for u in G if deg[u] > 20][:3]:
        w = e.sample_walks(G, v)
        assert len(w) == 10, f"{name}: {len(w)} walks, expected 10"
        for walk in w:
            if len(walk) != 40: bad += 1
            if walk[0] != v: bad += 1
            for a, b in zip(walk, walk[1:]):
                if not G.has_edge(a, b):
                    nonedge += 1
                    if name != "rwr" or b != v:
                        bad += 1
    print(f"  {name:9s} 10 walks x len40 starting at start: {'OK' if bad==0 else 'FAIL'}"
          f"   (non-edge steps: {nonedge}{' = restarts, all -> start' if name=='rwr' else ''})")

print("\n=== empirical transition distribution vs the stated rule ===")
# pick a node with several neighbours
v = max(range(200), key=lambda u: deg[u])
nbrs = sorted(adj[v])
print(f"  probe node {v}, degree {deg[v]}")

def empirical(kw, n=200000):
    e = WalkEmbedding(seed=7, **BASE, **kw)
    e.num_walks, e.walk_length = n, 2       # n walks of length 2 = n single steps from v
    c = collections.Counter(w[1] for w in e.sample_walks(G, v))
    return np.array([c[x] for x in nbrs], dtype=float) / n

for name, rule in (("uniform", np.ones(len(nbrs))),
                   ("degcorr", np.array([deg[x] ** -1.0 for x in nbrs])),
                   ("triadic", np.array([1.0 + len(adj[v] & adj[x]) for x in nbrs]))):
    emp = empirical(STRATS[name])
    want = rule / rule.sum()
    print(f"  {name:9s} max|emp-theory| = {np.abs(emp-want).max():.5f}   "
          f"{'OK' if np.abs(emp-want).max() < 0.01 else 'MISMATCH'}")

print("\n=== node2vec 2nd-order weights (p, q) ===")
# after step prev -> cur, P(x) must be prop to 1/p (x==prev), 1 (x in N(prev)), 1/q else
for p, q in ((1.0, 0.5), (1.0, 2.0), (0.25, 0.25)):
    e = WalkEmbedding(seed=11, **BASE, strategy="node2vec", p=p, q=q)
    prev = v
    cur = max(nbrs, key=lambda x: deg[x])
    cn = sorted(adj[cur])
    w = np.array([(1/p if x == prev else (1.0 if x in adj[prev] else 1/q)) for x in cn])
    want = w / w.sum()
    # drive the sampler directly on the prev->cur state
    cnt = collections.Counter()
    NBR = e._nbr_lists(G); rng = e._rng
    inv_p, inv_q, wmax = 1/p, 1/q, max(1/p, 1.0, 1/q)
    for _ in range(300000):
        while True:
            x = rng.choice(NBR[cur])
            ww = inv_p if x == prev else (1.0 if x in adj[prev] else inv_q)
            if rng.random() * wmax < ww: break
        cnt[x] += 1
    emp = np.array([cnt[x] for x in cn], float) / 300000
    print(f"  p={p} q={q}: max|emp-theory| = {np.abs(emp-want).max():.5f}  "
          f"{'OK' if np.abs(emp-want).max() < 0.01 else 'MISMATCH'}")

print("\n=== train_embedding: zero rows ===")
e = WalkEmbedding(seed=0, **BASE, strategy="uniform")
walks = []
for s in G.nodes():
    walks.extend(e.sample_walks(G, s))
print("  total walks:", len(walks), "(answer claims 69,580)")
Z = e.train_embedding(walks, N)
zr = int((np.abs(Z).sum(1) == 0).sum())
print("  Z shape:", Z.shape, " all-zero rows:", zr, " == n isolated:", zr == len(iso))
print("  zero rows are exactly the isolated nodes:",
      set(np.flatnonzero(np.abs(Z).sum(1) == 0).tolist()) == set(iso))
