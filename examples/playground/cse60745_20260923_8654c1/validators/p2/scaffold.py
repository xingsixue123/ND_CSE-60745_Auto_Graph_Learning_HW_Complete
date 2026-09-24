"""Scaffolding copied VERBATIM out of graph_embedding-1.ipynb (sections 1, 2, 5).

Nothing in this file is mine except the removal of the download loop (the data is
already on disk) and the `if __name__` guard.  Do not edit.
"""
import json
import random
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from sklearn.metrics import f1_score

RANDOM_SEED = 0

pd.set_option("display.width", 140)
np.set_printoptions(precision=4, suppress=True)


# ---------------------------------------------------------------- section 2
def load_data():
    """Load the social graph, the link-prediction splits, and the country label."""
    stats = json.loads(Path("data/task1/split_stats.json").read_text())
    n_users = stats["n_nodes"]

    splits = {name: pd.read_csv(f"data/task1/lp_{name}.csv") for name in ("train", "val", "test")}
    train_edges = pd.read_csv("data/task1/lp_graph_obs.csv")[["src", "dst"]]

    G_train = nx.Graph()
    G_train.add_nodes_from(range(n_users), type="U")
    G_train.add_edges_from(train_edges.itertuples(index=False, name=None))

    country = (pd.read_csv("data/task2/node_country.csv")
               .set_index("node_id")["country"].reindex(range(n_users)).to_numpy())
    split = pd.read_csv("data/task3/country_split.csv").set_index("node_id")["split"]
    country_split = {name: np.flatnonzero((split == name).to_numpy())
                     for name in ("train", "val", "test")}
    return G_train, splits, country, country_split, n_users


_LOOKUP_CACHE = {}


def adjacency_lookups(G):
    """(ADJ, DEG) for a graph: ADJ[u] is the set of neighbours of u, DEG[u] its degree."""
    key = ("adj", id(G))
    if key not in _LOOKUP_CACHE:
        adj = {u: set(G.neighbors(u)) for u in G}
        _LOOKUP_CACHE[key] = (adj, {u: len(adj[u]) for u in G})
    return _LOOKUP_CACHE[key]


def typed_adjacency(G):
    """(ADJ_T, TYPE) for a graph with a `type` node attribute."""
    key = ("typed", id(G))
    if key not in _LOOKUP_CACHE:
        ntype = nx.get_node_attributes(G, "type")
        adj_t = {u: defaultdict(list) for u in G}
        for u, v in G.edges():
            adj_t[u][ntype[v]].append(v)
            adj_t[v][ntype[u]].append(u)
        _LOOKUP_CACHE[key] = (adj_t, ntype)
    return _LOOKUP_CACHE[key]


# ---------------------------------------------------------------- section 5
def evaluate_ranking(df, scores, seed=RANDOM_SEED):
    """Compute Hit@1 and MRR within each query, breaking ties uniformly at random."""
    rng = np.random.default_rng(seed)
    d = df[["query_id", "label"]].copy()
    d["score"] = scores
    d["tiebreak"] = rng.random(len(d))
    d = d.sort_values(["query_id", "score", "tiebreak"], ascending=[True, False, True])
    d["rank"] = d.groupby("query_id").cumcount() + 1
    pos = d.loc[d["label"] == 1, ["query_id", "rank"]]
    metrics = {"n_queries": len(pos),
               "hit@1": float((pos["rank"] == 1).mean()),
               "MRR": float((1.0 / pos["rank"]).mean())}
    return metrics, pos.set_index("query_id")["rank"]


def breakdown_by_source_degree(df, ranks, degrees, bins=(0, 1, 2, 4, 8, 16, np.inf)):
    """Split Hit@1 and MRR by how many friends the source user has in the graph."""
    pos = df[df["label"] == 1].set_index("query_id")
    d = pd.DataFrame({"rank": ranks})
    d["src_degree"] = pos.loc[d.index, "src"].map(degrees).to_numpy()
    d["bucket"] = pd.cut(d["src_degree"], bins=list(bins), right=False)
    return d.groupby("bucket", observed=True).agg(
        n_queries=("rank", "size"),
        hit_at_1=("rank", lambda r: (r == 1).mean()),
        MRR=("rank", lambda r: (1.0 / r).mean()),
    ).round(4)


def to_query_tensor(df, X, positive_first=False):
    """Group a flat feature matrix by query: (n_pairs, F) -> (n_queries, n_candidates, F)."""
    labels = df["label"].to_numpy()
    n_cand = len(df) // int(labels.sum())
    n_q = len(df) // n_cand
    rows = np.arange(len(df)).reshape(n_q, n_cand)
    lab = labels.reshape(n_q, n_cand)
    if positive_first:
        cols = np.argsort(-lab, axis=1, kind="stable")
        rows = np.take_along_axis(rows, cols, axis=1)
        lab = np.take_along_axis(lab, cols, axis=1)
    return X[rows], lab, rows


def flatten_scores(scores, rows, n_pairs):
    """Map (n_queries, n_candidates) scores back to the row order of the split."""
    flat = np.empty(n_pairs, dtype=float)
    flat[rows.ravel()] = np.asarray(scores, dtype=float).ravel()
    return flat


def embed_graph(embedder, G, n_nodes):
    """Run the sampler from every node of G, train, and return the (n_nodes, d) matrix."""
    t0 = time.perf_counter()
    walks = []
    for start in G.nodes():
        walks.extend(embedder.sample_walks(G, start))
    assert walks, "sample_walks returned no walks from any node"
    t1 = time.perf_counter()
    Z = np.asarray(embedder.train_embedding(walks, n_nodes), dtype=float)
    assert Z.ndim == 2 and Z.shape[0] == n_nodes, (
        f"train_embedding must return ({n_nodes}, d), got {Z.shape}")
    print(f"    {len(walks):,} walks in {t1 - t0:.1f}s, "
          f"embedding {Z.shape} in {time.perf_counter() - t1:.1f}s", flush=True)
    return Z


def evaluate_link_prediction(Z, predictor, splits, G):
    """Task 1 evaluation on an embedding-based predictor."""
    pairs, labels, rows = {}, {}, {}
    for name in ("train", "val", "test"):
        pairs[name], labels[name], rows[name] = to_query_tensor(
            splits[name], splits[name][["src", "dst"]].to_numpy(),
            positive_first=(name == "train"))

    predictor.fit(Z, pairs["train"], labels["train"], pairs["val"], labels["val"])

    degrees = dict(G.degree())
    out = {}
    for name in ("val", "test"):
        s = np.asarray(predictor.score(Z, pairs[name]), dtype=float)
        assert s.shape == pairs[name].shape[:2], (
            f"score returned {s.shape}, expected {pairs[name].shape[:2]} for {name}")
        flat = flatten_scores(s, rows[name], len(splits[name]))
        metrics, ranks = evaluate_ranking(splits[name], flat)
        out[name] = (metrics, breakdown_by_source_degree(splits[name], ranks, degrees))
    return out


def evaluate_country(Z, y, classifier, node_split):
    """Node classification on the fixed 10/10/80 split."""
    tr, va, te = node_split["train"], node_split["val"], node_split["test"]
    classifier.fit(Z[tr], y[tr], Z[va], y[va])
    rows = {}
    for name, idx in (("val", va), ("test", te)):
        pred = np.asarray(classifier.predict(Z[idx]))
        assert pred.shape == (len(idx),), f"predict returned {pred.shape} for {len(idx)} users"
        rows[name] = {"micro_f1": f1_score(y[idx], pred, average="micro", zero_division=0),
                      "macro_f1": f1_score(y[idx], pred, average="macro", zero_division=0)}
    return pd.DataFrame(rows).T.round(4)


RESULTS = {}


def comparison_table():
    """One row per recorded experiment."""
    return pd.DataFrame({k: v["summary"] for k, v in RESULTS.items()}).T.round(4)
