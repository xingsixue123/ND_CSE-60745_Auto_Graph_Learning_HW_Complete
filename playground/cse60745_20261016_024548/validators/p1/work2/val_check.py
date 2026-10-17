"""Independent validator checks: do not reuse the worker's test helpers."""
import math, numpy as np, torch
import scipy.sparse as sp
from scipy.sparse.csgraph import shortest_path, breadth_first_order
from gt_framework import *
import solution as S

ok = True
def chk(name, cond, extra=""):
    global ok
    ok &= bool(cond)
    print(("  PASS  " if cond else "  FAIL  ") + name + ("  " + extra if extra else ""))

rng = np.random.default_rng(7)

# ---------- 1. hop_distances vs scipy csgraph shortest_path ----------
print("1. hop_distances vs scipy.sparse.csgraph.shortest_path")
graphs = [ZINC_GRAPHS["train"][i] for i in rng.choice(10000, 30, replace=False)]
# also a deliberately disconnected graph and a tiny one
worst = 0
for g in graphs:
    n, ei = g["n"], g["edge_index"]
    A = sp.coo_matrix((np.ones(ei.size(1)), (ei[0].numpy(), ei[1].numpy())), shape=(n, n))
    ref = shortest_path(A, method="D", unweighted=True, directed=False)
    got = S.hop_distances(ei, n).numpy().astype(float)
    ref2 = np.where(np.isinf(ref), -1.0, ref)
    worst = max(worst, np.abs(got - ref2).max())
chk("30 random ZINC graphs, exact distances", worst == 0, f"max abs diff {worst}")

# disconnected + isolated node
ei = torch.tensor([[0,1,1,2,4,5],[1,0,2,1,5,4]])
D = S.hop_distances(ei, 7).numpy()
A = sp.coo_matrix((np.ones(6), (ei[0].numpy(), ei[1].numpy())), shape=(7,7))
ref = shortest_path(A, unweighted=True, directed=False)
ref = np.where(np.isinf(ref), -1, ref)
chk("disconnected graph with an isolated node (n=7)", (D == ref).all(), f"\n{D}")

# capped version: everything <= cap must be exact, further-but-reachable == cap, unreachable == -1
g = ZINC_GRAPHS["train"][0]
n, ei = g["n"], g["edge_index"]
A = sp.coo_matrix((np.ones(ei.size(1)), (ei[0].numpy(), ei[1].numpy())), shape=(n, n))
ref = shortest_path(A, unweighted=True, directed=False)
for cap in (1, 3, 8):
    got = S.hop_distances(ei, n, cap=cap).numpy()
    want = np.where(np.isinf(ref), -1, np.minimum(ref, cap))
    chk(f"cap={cap} on a {n}-node ZINC graph", (got == want).all())

# cap on a disconnected graph: unreachable must stay -1, not become cap
ei = torch.tensor([[0,1,1,2,4,5],[1,0,2,1,5,4]])
got = S.hop_distances(ei, 7, cap=1).numpy()
ref = shortest_path(sp.coo_matrix((np.ones(6), (ei[0].numpy(), ei[1].numpy())), shape=(7,7)),
                    unweighted=True, directed=False)
want = np.where(np.isinf(ref), -1, np.minimum(ref, 1))
chk("cap=1 keeps unreachable at -1 on a disconnected graph", (got == want).all(), f"\n{got}")

# the LastFM sparse branch, spot-checked against BFS from 12 sources
print("2. LastFM sparse branch vs per-source BFS")
g = LASTFM
Dl = S.hop_distances(g["edge_index"], g["n"], cap=S.SPD_MAX_DIST).numpy()
Al = sp.coo_matrix((np.ones(g["edge_index"].size(1)),
                    (g["edge_index"][0].numpy(), g["edge_index"][1].numpy())),
                   shape=(g["n"], g["n"])).tocsr()
bad = 0
for s in rng.choice(g["n"], 12, replace=False):
    d = shortest_path(Al, unweighted=True, directed=False, indices=[int(s)])[0]
    want = np.where(np.isinf(d), -1, np.minimum(d, 8))
    bad += int((Dl[s] != want).sum())
chk("12 random LastFM sources match scipy BFS", bad == 0, f"mismatches {bad}")
chk("LastFM distances symmetric", (Dl == Dl.T).all())

# ---------- 3. laplacian eigenvectors ----------
print("3. laplacian_eigvecs: subspace and eigenvalues")
for g in [ZINC_GRAPHS["train"][i] for i in rng.choice(10000, 5, replace=False)]:
    n, ei = g["n"], g["edge_index"]
    A = np.zeros((n, n)); A[ei[0].numpy(), ei[1].numpy()] = 1.0
    deg = A.sum(1); Dm = np.diag(1/np.sqrt(np.maximum(deg, 1)))
    L = np.eye(n) - Dm @ A @ Dm
    w, V = np.linalg.eigh(L)
    got = S.laplacian_eigvecs(ei, n).numpy() / math.sqrt(n)
    m = min(LAP_K, n - 1)
    # Rayleigh quotients must equal w[1:m+1]
    rq = np.array([got[:, j] @ L @ got[:, j] for j in range(m)])
    chk(f"n={n}: Rayleigh quotients == eigenvalues 1..{m}", np.allclose(rq, w[1:m+1], atol=1e-6),
        f"max diff {np.abs(rq - w[1:m+1]).max():.2e}")
    chk(f"n={n}: orthonormal, orthogonal to the trivial eigenvector",
        np.allclose(got[:, :m].T @ got[:, :m], np.eye(m), atol=1e-6)
        and abs(got[:, :m].T @ (np.sqrt(np.maximum(deg,1)))).max() < 1e-5)
    chk(f"n={n}: columns {m}..{LAP_K} are zero padding", (m >= LAP_K or np.abs(got[:, m:]).max() == 0))

# ---------- 4. the 2-hop ball pair set is exactly {d<=2} + virtual ----------
print("4. SparseSPDAttention.attention_pairs == {d(i,j)<=2} + one virtual node")
for g in [ZINC_GRAPHS["train"][i] for i in rng.choice(10000, 20, replace=False)]:
    n, ei = g["n"], g["edge_index"]
    D = S.hop_distances(ei, n).numpy()
    want = {(int(i), int(j)) for i in range(n) for j in range(n) if 0 <= D[i, j] <= 2}
    want |= {(int(i), n) for i in range(n)} | {(n, int(i)) for i in range(n)} | {(n, n)}
    p = S.SparseSPDAttention.attention_pairs(ei, n)
    got = {(int(a), int(b)) for a, b in zip(*p.tolist())}
    if got != want:
        chk(f"n={n}", False, f"missing {len(want-got)} extra {len(got-want)}")
        break
else:
    chk("20 ZINC graphs: pair set is exactly the 2-hop ball + virtual node", True)

# ---------- 5. independent dense reference for the SPARSE forward ----------
print("5. sparse forward vs an independently written dense reference (real pair set)")
torch.manual_seed(3)
gs = [ZINC_GRAPHS["train"][i] for i in range(4)]
for gg in gs:
    gg.setdefault("cache", {})
ensure_precomputed(gs, [S.LapPETransformer.precompute, S.SPDAttention.precompute])
ensure_pairs(gs, S.SparseSPDAttention.attention_pairs)
b = make_batch(gs, S.LapPETransformer.precompute, S.SPDAttention.precompute,
               S.SparseSPDAttention.attention_pairs)
dim, heads = 16, 4
att = S.SparseSPDAttention(dim, heads)
M = b["batch"].size(0)
h = torch.randn(M, dim)
out = att(h, b["pair_enc"], b["pairs"]).detach()

# reference: build the [M, M] score matrix by hand, -inf outside the pair set
qkv = att.qkv(h).view(M, 3, heads, dim // heads)
q, k, v = qkv[:, 0], qkv[:, 1], qkv[:, 2]
src, dst = b["pairs"]
scores = torch.full((heads, M, M), float("-inf"))
for p in range(src.numel()):
    i, j = int(dst[p]), int(src[p])             # i attends to j
    s = (q[i] * k[j]).sum(-1) / math.sqrt(dim // heads)
    d = -1 if int(b["pair_enc"]["pair_type"][p]) == PAIR_TYPES.index("virtual") else int(b["pair_enc"]["spd"][p])
    bucket = att.max_dist + 1 if d < 0 else min(d, att.max_dist)
    s = s + att.spd_table.weight[bucket] + att.type_table.weight[int(b["pair_enc"]["pair_type"][p])]
    scores[:, i, j] = s
w = torch.softmax(scores, dim=-1)
ref = torch.einsum("hij,jhd->ihd", w, v).reshape(M, dim)
ref = att.out(ref).detach()
diff = (out - ref).abs().max().item()
chk("sparse forward matches the hand-built dense reference", diff < 1e-5, f"max abs diff {diff:.2e}")

# check the spd values the framework hands over really are d(querier, attended)
bad = 0
off = 0
for gg in gs:
    n = gg["n"]; nv = gg["pairs"][2]
    D = S.hop_distances(gg["edge_index"], n).numpy()
    pp = gg["pairs"][1]
    for p in range(pp.size(1)):
        s_, d_ = int(pp[0, p]), int(pp[1, p])
        if s_ < n and d_ < n:
            idx = off + p
            # locate this pair in the batch tensors
    off += pp.size(1)
# simpler: rebuild expected spd for the whole batch
exp = []
for gg in gs:
    n = gg["n"]; pp = gg["pairs"][1]
    D = S.hop_distances(gg["edge_index"], n).numpy()
    for p in range(pp.size(1)):
        s_, d_ = int(pp[0, p]), int(pp[1, p])
        exp.append(int(D[d_, s_]) if (s_ < n and d_ < n) else 0)
chk("enc['spd'] == D[querier, attended] for every pair",
    (torch.tensor(exp) == b["pair_enc"]["spd"].long()).all().item())

# ---------- 6. dense forward reference ----------
print("6. dense SPDAttention forward vs a hand-built reference")
b2 = make_batch(gs, S.LapPETransformer.precompute, S.SPDAttention.precompute, None)
hb, mask = to_dense_batch(torch.randn(sum(g["n"] for g in gs), dim),
                          torch.cat([torch.full((g["n"],), i) for i, g in enumerate(gs)]))
datt = S.SPDAttention(dim, heads)
o = datt(hb, b2["pair_enc"], mask).detach()
B, N, _ = hb.shape
qkv = datt.qkv(hb).view(B, N, 3, heads, dim // heads)
q, k, v = qkv[:, :, 0], qkv[:, :, 1], qkv[:, :, 2]
sc = torch.einsum("bihd,bjhd->bhij", q, k) / math.sqrt(dim // heads)
bk = b2["pair_enc"]["spd"].long().clamp(min=-1)
bk = torch.where(bk < 0, torch.full_like(bk, datt.max_dist + 1), bk.clamp(max=datt.max_dist))
sc = sc + datt.spd_table(bk).permute(0, 3, 1, 2)
sc = sc.masked_fill(~mask[:, None, None, :], float("-inf"))
wgt = torch.softmax(sc, -1).nan_to_num(0.0)
ref = datt.out(torch.einsum("bhij,bjhd->bihd", wgt, v).reshape(B, N, dim)).detach()
chk("dense forward matches", (o - ref).abs().max().item() < 1e-6,
    f"max abs diff {(o - ref).abs().max().item():.2e}")

# ---------- 7. pair counts reported in the tables ----------
print("7. pair counts")
tot = 0; full = 0
for gg in ZINC_GRAPHS["train"]:
    p = S.SparseSPDAttention.attention_pairs(gg["edge_index"], gg["n"])
    tot += p.size(1); full += gg["n"] ** 2
print(f"  2-hop ball+virtual: {tot/10000:.4f} pairs/graph, full n^2 {full/10000:.4f}, "
      f"{100*tot/full:.2f}% -> table says 189 / 557 / 34%")
chk("pairs/graph 189.2", abs(tot/10000 - 189.1828) < 0.01)
chk("n^2 556.8", abs(full/10000 - 556.8356) < 0.01)
pl = S.SparseSPDAttention.attention_pairs(LASTFM["edge_index"], LASTFM["n"]).size(1)
print(f"  LastFM: {pl:,} pairs -> table says 804,349 ({100*pl/7624**2:.3f}%)")
chk("LastFM 804,349 pairs", pl == 804349)
chk("LastFM n^2 = 58,125,376", 7624**2 == 58125376)

print("\nALL OK" if ok else "\nSOME CHECKS FAILED")
