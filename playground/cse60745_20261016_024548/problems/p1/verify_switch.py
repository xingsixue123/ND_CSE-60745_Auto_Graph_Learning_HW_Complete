"""Check that the renamed classes build exactly the pair sets that were measured."""
import numpy as np
import scipy.sparse as sp
import torch

from gt_framework import *                                  # noqa: F401,F403
from solution import SparseSPDAttention, pair_set
from experiments import STRATEGIES


def old_ball(edge_index, num_nodes):
    """Ball2SPDAttention.attention_pairs exactly as it was when Table 2 was measured."""
    n = num_nodes
    A = sp.coo_matrix((np.ones(edge_index.size(1)), (edge_index[0].numpy(), edge_index[1].numpy())),
                      shape=(n, n)).tocsr()
    ball = ((A + A @ A) > 0).tocoo()
    extra = torch.from_numpy(np.stack([ball.row, ball.col])).long()
    return pair_set(edge_index, num_nodes, n_cycles=0, virtual=True, extra=[extra])


def old_expander2(edge_index, num_nodes):
    """SparseSPDAttention.attention_pairs as it was (EXPANDER_CYCLES = 2)."""
    return pair_set(edge_index, num_nodes, n_cycles=2, virtual=True)


graphs = ZINC_GRAPHS["train"][:200] + ZINC_GRAPHS["val"][:50] + [LASTFM]
ok = True
for name, fn_old in (("2-hop ball+virtual", old_ball), ("local+expander+virtual", old_expander2)):
    cls = STRATEGIES[name]
    for g in graphs:
        a = cls.attention_pairs(g["edge_index"], g["n"])
        b = fn_old(g["edge_index"], g["n"])
        if not torch.equal(a, b):
            ok = False
            print(f"  MISMATCH {name} on a graph with n={g['n']}")
            break
    else:
        print(f"  PASS  {name}: identical pair sets on {len(graphs)} graphs "
              f"(including LastFM, {cls.attention_pairs(LASTFM['edge_index'], LASTFM['n']).size(1):,} pairs)")
print("all pair sets unchanged by the rename" if ok else "RENAME CHANGED A PAIR SET")
assert ok
