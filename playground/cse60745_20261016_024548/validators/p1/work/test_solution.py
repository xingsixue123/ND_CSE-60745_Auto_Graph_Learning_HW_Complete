"""Correctness checks for solution.py.  Run:  ../../.venv-gt/bin/python test_solution.py"""
import math
from collections import deque

import numpy as np
import torch

from gt_framework import *                      # noqa: F401,F403
from solution import (LapPETransformer, SPDAttention, SparseSPDAttention,
                      hop_distances, laplacian_eigvecs, pair_set, DENSE_LIMIT)


def random_graph(n, p, seed):
    g = torch.Generator().manual_seed(seed)
    m = torch.rand(n, n, generator=g) < p
    m = torch.triu(m, 1)
    src, dst = m.nonzero().T
    return to_undirected(torch.stack([torch.cat([src, dst]), torch.cat([dst, src])]), num_nodes=n)


def bfs_reference(edge_index, n):
    adj = [[] for _ in range(n)]
    for a, b in edge_index.T.tolist():
        adj[a].append(b)
    D = np.full((n, n), -1, dtype=np.int64)
    for s in range(n):
        D[s, s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if D[s, w] < 0:
                    D[s, w] = D[s, u] + 1
                    q.append(w)
    return D


def check(name, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    assert ok, name


print("1. hop_distances vs. a plain BFS")
for n, p, seed in [(9, 0.3, 1), (23, 0.12, 2), (37, 0.08, 3), (60, 0.04, 4)]:
    ei = random_graph(n, p, seed)
    ref = bfs_reference(ei, n)
    got = hop_distances(ei, n).numpy().astype(np.int64)
    check(f"exact distances n={n}, {int(ei.size(1))//2} edges, "
          f"{int((ref < 0).sum())} unreachable pairs", np.array_equal(ref, got))
    cap = 3                                      # capped: >cap but reachable -> cap, else -1
    want = np.where((ref > cap), cap, ref)
    check(f"capped at {cap}, n={n}", np.array_equal(hop_distances(ei, n, cap=cap).numpy(), want))

print("2. hop_distances large-graph (sparse) branch agrees with the dense branch")
n = DENSE_LIMIT + 200
ei = random_graph(n, 3.0 / n, 11)
ref = bfs_reference(ei, n)
got = hop_distances(ei, n, cap=8).numpy().astype(np.int64)
check(f"sparse block BFS, n={n}, cap=8", np.array_equal(np.where(ref > 8, 8, ref), got))

print("3. laplacian_eigvecs")
for n, p, seed in [(9, 0.4, 5), (30, 0.15, 6)]:
    ei = random_graph(n, p, seed)
    V = laplacian_eigvecs(ei, n).numpy() / math.sqrt(n)
    A = np.zeros((n, n))
    A[ei[0].numpy(), ei[1].numpy()] = 1.0
    dinv = 1.0 / np.sqrt(np.maximum(A.sum(1), 1.0))
    L = np.eye(n) - dinv[:, None] * A * dinv[None, :]
    w_ref = np.linalg.eigvalsh(L)
    m = min(LAP_K, n - 1)
    rq = [float(V[:, j] @ L @ V[:, j]) for j in range(m)]           # Rayleigh quotients
    check(f"n={n}: eigenvalues match the dense spectrum[1:{m+1}]",
          np.allclose(rq, w_ref[1:m + 1], atol=1e-6))
    check(f"n={n}: columns orthonormal (before the sqrt(n) scaling)",
          np.allclose(V[:, :m].T @ V[:, :m], np.eye(m), atol=1e-6))
    check(f"n={n}: residual ||L v - lambda v|| small",
          max(np.abs(L @ V[:, j] - rq[j] * V[:, j]).max() for j in range(m)) < 1e-6)
n = DENSE_LIMIT + 200                                               # sparse eigsh branch
ei = random_graph(n, 4.0 / n, 12)
V = laplacian_eigvecs(ei, n).numpy() / math.sqrt(n)
A = np.zeros((n, n)); A[ei[0].numpy(), ei[1].numpy()] = 1.0
dinv = 1.0 / np.sqrt(np.maximum(A.sum(1), 1.0))
L = np.eye(n) - dinv[:, None] * A * dinv[None, :]
w_ref = np.linalg.eigvalsh(L)
rq = [float(V[:, j] @ L @ V[:, j]) for j in range(LAP_K)]
check(f"sparse eigsh branch n={n} matches dense eigh", np.allclose(rq, w_ref[1:LAP_K + 1], atol=1e-5))
check("sqrt(n) scaling gives channels of RMS 1",
      abs(float(np.sqrt((laplacian_eigvecs(ei, n).numpy() ** 2).mean(0)).mean()) - 1.0) < 1e-5)

print("4. padding when the graph has fewer than LAP_K non-trivial eigenvectors")
ei = random_graph(5, 0.6, 7)
V = laplacian_eigvecs(ei, 5)
check("n=5 -> 4 eigenvectors + 4 zero columns",
      V.shape == (5, LAP_K) and bool((V[:, 4:] == 0).all()) and bool((V[:, :4] != 0).any()))

print("5. sparse attention == dense attention when the pair set is complete")
torch.manual_seed(0)
n, dim, heads = 12, 16, 4
ei = random_graph(n, 0.25, 8)
dense_att = SPDAttention(dim, heads)
sparse_att = SparseSPDAttention(dim, heads)
sparse_att.load_state_dict(dense_att.state_dict(), strict=False)
torch.nn.init.zeros_(sparse_att.type_table.weight)                  # the only extra term
h = torch.randn(n, dim)
spd = SPDAttention.precompute(ei, n)["spd"]
out_dense = dense_att(h[None], {"spd": spd[None]}, torch.ones(1, n, dtype=torch.bool))[0]
all_pairs = torch.stack(torch.meshgrid(torch.arange(n), torch.arange(n), indexing="ij")).reshape(2, -1)
src, dst = all_pairs
enc = {"spd": spd[dst, src], "pair_type": pair_types(all_pairs, ei, n)}
out_sparse = sparse_att(h, enc, all_pairs)
check(f"max |dense - sparse| = {float((out_dense - out_sparse).abs().max()):.2e}",
      torch.allclose(out_dense, out_sparse, atol=1e-5))

print("6. pair_set structure")
ei = random_graph(40, 0.1, 9)
P = pair_set(ei, 40)
t = pair_types(P, ei, 40)
counts = {k: int((t == i).sum()) for i, k in enumerate(PAIR_TYPES)}
check(f"pair types {counts}", counts["self"] == 40 and counts["edge"] == int(ei.size(1))
      and counts["virtual"] == 81 and counts["other"] > 0)   # 2n+1: both directions + its self loop
check("every node (and the virtual node) is a querier",
      bool(torch.bincount(P[1], minlength=41).min() > 0))
check("deterministic across calls", bool(torch.equal(P, pair_set(ei, 40))))
check("pairs are unique", len({tuple(c) for c in P.T.tolist()}) == P.size(1))

print("7. end-to-end on a handful of ZINC graphs")
model = LapPETransformer(attention_cls=SPDAttention, dim=16, heads=2, layers=2)
gs = ZINC_GRAPHS["val"][:8]
node_fn, pair_fn, pairs_fn = precompute_fns(model)
ensure_precomputed(gs, [node_fn, pair_fn])
out = model(make_batch(gs, node_fn, pair_fn, None))
check(f"dense model output {tuple(out.shape)}", out.shape == (8, 1) and bool(out.isfinite().all()))
model = LapPETransformer(attention_cls=SparseSPDAttention, dim=16, heads=2, layers=2)
node_fn, pair_fn, pairs_fn = precompute_fns(model)
ensure_precomputed(gs, [node_fn, pair_fn])
ensure_pairs(gs, pairs_fn)
b = make_batch(gs, node_fn, pair_fn, pairs_fn)
out = model(b)
check(f"sparse model output {tuple(out.shape)}, {b['pairs'].size(1)} pairs vs "
      f"{sum(g['n'] ** 2 for g in gs)} full", out.shape == (8, 1) and bool(out.isfinite().all()))
model.train()
out.sum().backward()
grads = {n_ for n_, p in model.named_parameters() if p.grad is not None and p.grad.abs().sum() > 0}
check("spd_table, type_table, lap_proj and the virtual start state all get gradient",
      {"blocks.0.attention.spd_table.weight", "blocks.0.attention.type_table.weight",
       "lap_proj.weight", "virtual"} <= grads)

print("\nall checks passed")
