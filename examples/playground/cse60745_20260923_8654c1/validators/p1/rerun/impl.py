"""The four TODOs of graph_embedding-1.ipynb sections 3 and 4.

TODO 1  WalkEmbedding.sample_walks
TODO 2  WalkEmbedding.train_embedding
TODO 3a LinkPredictor.fit / .score
TODO 3b CountryClassifier.fit / .predict
"""
import random

import numpy as np
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from scaffold import RANDOM_SEED, adjacency_lookups


# ======================================================================================
# TODO 1 + TODO 2
# ======================================================================================
class WalkEmbedding:
    """Random-walk node embeddings: walks -> SkipGram -> one vector per node.

    A sampling strategy is just a set of constructor arguments:

      strategy : "uniform"   DeepWalk, next node uniform over N(cur)
                 "node2vec"  2nd-order biased walk with return p and in-out q
                 "rwr"       uniform walk that restarts at `start` w.p. `restart`
                 "degcorr"   next node w.p. proportional to deg(x) ** (-alpha)
                 "triadic"   next node w.p. proportional to 1 + |N(cur) & N(x)|
      num_walks, walk_length : the walk budget, identical for every strategy
      dim, window, negative, epochs : Skip-Gram hyper-parameters
    """

    def __init__(self, seed=RANDOM_SEED, **params):
        self.seed = seed
        self.params = params
        self.strategy = params.get("strategy", "uniform")
        self.num_walks = params.get("num_walks", 10)
        self.walk_length = params.get("walk_length", 40)
        self._rng = random.Random(seed)
        self._tables = {}          # cached per-node transition tables

    # ---------------------------------------------------------------- helpers
    def _nbr_lists(self, G):
        """Per-node sorted neighbour *list* (cheaper and more deterministic to sample
        from than the sets returned by adjacency_lookups)."""
        key = (id(G), "nbrs")
        if key not in self._tables:
            adj, _ = adjacency_lookups(G)
            self._tables[key] = {u: sorted(adj[u]) for u in G}
        return self._tables[key]

    def _weighted_tables(self, G):
        """Per-node (neighbour list, cumulative weights) for the 1st-order biased walks."""
        key = (id(G), self.strategy, self.params.get("alpha"))
        if key in self._tables:
            return self._tables[key]
        adj, deg = adjacency_lookups(G)
        alpha = self.params.get("alpha", 1.0)
        tables = {}
        for u in G:
            nbrs = sorted(adj[u])
            if not nbrs:
                tables[u] = ((), ())
                continue
            if self.strategy == "degcorr":
                w = [deg[x] ** (-alpha) for x in nbrs]
            elif self.strategy == "triadic":
                w = [1.0 + len(adj[u] & adj[x]) for x in nbrs]
            else:
                w = [1.0] * len(nbrs)
            cum, s = [], 0.0
            for wi in w:
                s += wi
                cum.append(s)
            tables[u] = (nbrs, cum)
        self._tables[key] = tables
        return tables

    # ==================================================================================
    # TODO 1 of 3 - sampling.
    # ==================================================================================
    def sample_walks(self, G, start):
        """Return the `num_walks` walks of length `walk_length` that begin at `start`."""
        adj, deg = adjacency_lookups(G)
        if deg[start] == 0:                       # isolated node: nothing to walk on
            return []
        rng = self._rng
        L, R = self.walk_length, self.num_walks
        strat = self.strategy

        if strat == "node2vec":
            NBR = self._nbr_lists(G)
            p, q = self.params.get("p", 1.0), self.params.get("q", 1.0)
            inv_p, inv_q, wmax = 1.0 / p, 1.0 / q, max(1.0 / p, 1.0, 1.0 / q)
            walks = []
            for _ in range(R):
                walk = [start]
                walk.append(rng.choice(NBR[start]))            # 1st step is unbiased
                while len(walk) < L:
                    cur, prev = walk[-1], walk[-2]
                    cn = NBR[cur]
                    prev_nbrs = adj[prev]
                    while True:                                # rejection sampling
                        x = rng.choice(cn)
                        w = inv_p if x == prev else (1.0 if x in prev_nbrs else inv_q)
                        if rng.random() * wmax < w:
                            break
                    walk.append(x)
                walks.append(walk)
            return walks

        if strat in ("degcorr", "triadic"):
            tables = self._weighted_tables(G)
            walks = []
            for _ in range(R):
                walk = [start]
                while len(walk) < L:
                    nbrs, cum = tables[walk[-1]]
                    if not nbrs:
                        break
                    walk.append(rng.choices(nbrs, cum_weights=cum, k=1)[0])
                walks.append(walk)
            return walks

        NBR = self._nbr_lists(G)                   # "uniform" (DeepWalk) and "rwr"
        restart = self.params.get("restart", 0.0) if strat == "rwr" else 0.0
        walks = []
        for _ in range(R):
            walk = [start]
            while len(walk) < L:
                if restart and rng.random() < restart:
                    walk.append(start)             # teleport home, then carry on
                else:
                    walk.append(rng.choice(NBR[walk[-1]]))
            walks.append(walk)
        return walks

    # ==================================================================================
    # TODO 2 of 3 - training.
    # ==================================================================================
    def train_embedding(self, walks, n_nodes):
        """Skip-Gram with negative sampling over the walk corpus (gensim)."""
        d = self.params.get("dim", 128)
        model = Word2Vec(
            sentences=[[str(v) for v in w] for w in walks],
            vector_size=d, window=self.params.get("window", 5),
            sg=1, hs=0, negative=self.params.get("negative", 5),
            epochs=self.params.get("epochs", 5),
            min_count=0, sample=0, seed=self.seed, workers=1)
        Z = np.zeros((n_nodes, d), dtype=float)   # nodes never walked keep a zero row
        kv = model.wv
        idx = [int(k) for k in kv.index_to_key]
        Z[idx] = kv.vectors
        return Z


# ======================================================================================
# TODO 3a
# ======================================================================================
def _unit(Z):
    """Row-wise L2 normalisation; all-zero rows (isolated users) stay zero."""
    n = np.linalg.norm(Z, axis=1, keepdims=True)
    return Z / np.where(n == 0.0, 1.0, n)


def _pair_features(Z, pairs):
    """(n_q, n_cand, 2) -> (n_q * n_cand, 2d + 3): [u*v, |u-v|, cos, dot, ||u-v||]."""
    u, v = Z[pairs[..., 0]], Z[pairs[..., 1]]
    u, v = u.reshape(-1, Z.shape[1]), v.reshape(-1, Z.shape[1])
    had, dif = u * v, np.abs(u - v)
    dot = had.sum(1, keepdims=True)
    l2 = np.linalg.norm(u - v, axis=1, keepdims=True)
    nu, nv = np.linalg.norm(u, axis=1, keepdims=True), np.linalg.norm(v, axis=1, keepdims=True)
    cos = dot / np.maximum(nu * nv, 1e-12)
    return np.hstack([had, dif, cos, dot, l2])


class LinkPredictor:
    """Rank candidate friends for a source user from node embeddings."""

    C_GRID = (0.1, 1.0, 10.0)

    def fit(self, Z, pairs_train, y_train, pairs_val, y_val):
        Zn = _unit(np.asarray(Z, dtype=float))
        Xtr = _pair_features(Zn, pairs_train)
        ytr = np.asarray(y_train).ravel()
        self.scaler = StandardScaler().fit(Xtr)
        Xtr = self.scaler.transform(Xtr)

        Xva = self.scaler.transform(_pair_features(Zn, pairs_val))
        nq, nc = pairs_val.shape[:2]
        pos_val = np.argmax(np.asarray(y_val), axis=1)

        best = (-1.0, None)
        for C in self.C_GRID:                      # model selection on validation MRR
            clf = LogisticRegression(C=C, max_iter=2000, solver="lbfgs",
                                     random_state=RANDOM_SEED)
            clf.fit(Xtr, ytr)
            s = clf.decision_function(Xva).reshape(nq, nc)
            # rank of the positive within its query (ties counted pessimistically)
            sp = s[np.arange(nq), pos_val][:, None]
            rank = 1 + (s > sp).sum(1)
            mrr = float(np.mean(1.0 / rank))
            if mrr > best[0]:
                best = (mrr, clf, C)
        self.val_mrr_, self.clf, self.C_ = best[0], best[1], best[2]
        return self

    def score(self, Z, pairs):
        Zn = _unit(np.asarray(Z, dtype=float))
        X = self.scaler.transform(_pair_features(Zn, pairs))
        return self.clf.decision_function(X).reshape(pairs.shape[:2])


# ======================================================================================
# TODO 3b
# ======================================================================================
class CountryClassifier:
    """Predict a user's country from their embedding (multinomial logistic regression)."""

    C_GRID = (0.1, 1.0, 10.0, 100.0)

    def fit(self, Z_train, y_train, Z_val, y_val):
        Xtr = _unit(np.asarray(Z_train, dtype=float))
        self.scaler = StandardScaler().fit(Xtr)
        Xtr = self.scaler.transform(Xtr)
        Xva = self.scaler.transform(_unit(np.asarray(Z_val, dtype=float)))

        best = (-1.0, None, None)
        for C in self.C_GRID:                      # model selection on validation micro-F1
            clf = LogisticRegression(C=C, max_iter=5000, solver="lbfgs",
                                     random_state=RANDOM_SEED)
            clf.fit(Xtr, y_train)
            acc = float((clf.predict(Xva) == np.asarray(y_val)).mean())
            if acc > best[0]:
                best = (acc, clf, C)
        self.val_micro_f1_, self.clf, self.C_ = best
        return self

    def predict(self, Z):
        return self.clf.predict(self.scaler.transform(_unit(np.asarray(Z, dtype=float))))
