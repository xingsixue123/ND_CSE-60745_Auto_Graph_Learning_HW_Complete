"""Task 4: the meta-path-bounded sampler.

This is the ONLY thing that changes relative to Task 3.  `MetaPathWalkEmbedding`
subclasses p1's `WalkEmbedding` and overrides `sample_walks` and nothing else, so
`train_embedding` -- and therefore every Skip-Gram hyper-parameter -- as well as
`LinkPredictor` and `CountryClassifier` are literally the same code Task 3 measured.

Schema convention
-----------------
A schema is a symmetric type string, e.g. "UAU" or "UUAU" (last type == first).  Its
repeating cycle is `schema[:-1]`:

    "UAU"   -> cycle "UA"   -> U A U A U A ...      (0   of the steps are social)
    "UUAU"  -> cycle "UUA"  -> U U A U U A U ...    (1/3 of the steps are social)
    "UUUAU" -> cycle "UUUA" -> U U U A U U U A ...  (1/2 of the steps are social)

`embed_graph` starts a walk from every node of H, artists included.  An artist start
uses the rotation of the cycle that begins with "A", i.e. the same meta-path read from
the other end ("UA" -> "AU", "UUA" -> "AUU").  Artists therefore get trained vectors,
which act as shared context for the users; they are sliced off before evaluation.

A walk that cannot take its first step (a user with no artist under "UAU", a socially
isolated user under "UUAU") is dropped, exactly as p1's `sample_walks` returns `[]` for
an isolated node -- so such nodes keep an all-zero embedding row in both tasks and the
cold-start comparison stays like-for-like.
"""
import random

from impl import WalkEmbedding
from scaffold import RANDOM_SEED, typed_adjacency


class MetaPathWalkEmbedding(WalkEmbedding):
    """Meta-path bounded random walks (metapath2vec).

    Constructor arguments (the schema is selected through the constructor, as the
    notebook asks):

      schema : symmetric type string, e.g. "UAU", "UUAU", "UUUAU"
      alpha  : if not None, a step *into* an artist draws it with probability
               proportional to deg(a) ** (-alpha) instead of uniformly -- the
               "rare-artist" variant.  Steps into a user are always uniform.
      num_walks, walk_length, dim, window, negative, epochs : inherited, unchanged.
    """

    def __init__(self, schema="UAU", alpha=None, seed=RANDOM_SEED, **params):
        super().__init__(seed=seed, **params)
        assert len(schema) >= 2 and schema[0] == schema[-1], f"schema not symmetric: {schema}"
        self.schema = schema
        self.cycle = schema[:-1]
        self.alpha = alpha

    # ------------------------------------------------------------------ transition tables
    def _typed_tables(self, G):
        """node -> {target_type: (neighbour list, cumulative weights or None)}."""
        key = (id(G), "metapath", self.alpha)
        if key in self._tables:
            return self._tables[key]
        adj_t, ntype = typed_adjacency(G)
        deg_a = {a: len(adj_t[a].get("U", ())) for a in adj_t if ntype[a] == "A"}
        tables = {}
        for u, byt in adj_t.items():
            row = {}
            for t, nbrs in byt.items():
                if not nbrs:
                    continue
                if t == "A" and self.alpha is not None:
                    cum, s = [], 0.0
                    for a in nbrs:
                        s += max(deg_a[a], 1) ** (-self.alpha)
                        cum.append(s)
                    row[t] = (nbrs, cum)
                else:
                    row[t] = (nbrs, None)
            tables[u] = row
        self._tables[key] = (tables, ntype)
        return self._tables[key]

    # ------------------------------------------------------------------ TODO 1, extended
    def sample_walks(self, G, start):
        """`num_walks` type-constrained walks of length `walk_length` starting at `start`."""
        tables, ntype = self._typed_tables(G)
        t0 = ntype[start]
        if t0 not in self.cycle:                      # this schema never visits that type
            return []
        k = self.cycle.index(t0)
        rot = self.cycle[k:] + self.cycle[:k]         # cycle rotated to the start's type
        m, L, rng = len(rot), self.walk_length, self._rng

        walks = []
        for _ in range(self.num_walks):
            walk, i = [start], 0
            while len(walk) < L:
                entry = tables[walk[-1]].get(rot[(i + 1) % m])
                if entry is None:                     # no neighbour of the required type
                    break
                nbrs, cum = entry
                walk.append(rng.choice(nbrs) if cum is None
                            else rng.choices(nbrs, cum_weights=cum, k=1)[0])
                i += 1
            if len(walk) > 1:                         # a 1-node walk teaches Skip-Gram nothing
                walks.append(walk)
        return walks
