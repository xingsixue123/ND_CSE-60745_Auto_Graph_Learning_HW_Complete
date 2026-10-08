"""The frozen part of Practice3_pyg_basics.ipynb, ported verbatim.

Cells 2, 4, 6, 8, 10, 11 of the notebook (0-indexed), unchanged apart from:
  * only data/task1 is downloaded (data/task3 belongs to Q4, which is not this
    problem);
  * the node2vec features X are cached to run/cache/x_node2vec.pt.  gensim's
    Word2Vec is called with workers=4, which makes SkipGram training
    non-deterministic even with seed=0, so recomputing X per run would give every
    model slightly different inputs.  Computing it once and reusing it keeps every
    row of the results table on identical features.
Nothing in notebook section 5 (evaluate_ranking / GNNLinkPredictor / train_and_eval)
is modified.
"""

import json
import random
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn

from torch_geometric.nn import MessagePassing
from torch_geometric.utils import (add_self_loops, coalesce, degree,
                                   remove_self_loops, softmax, to_undirected)

HERE = Path(__file__).resolve().parent

GITHUB_REPO = "antman9914/CSE60745-Practice"
BRANCH = "main"

REQUIRED = {
    "data/task1": ["split_stats.json", "lp_graph_obs.csv",
                   "lp_train.csv", "lp_val.csv", "lp_test.csv"],
}
RANDOM_SEED = 0

for d, names in REQUIRED.items():
    (HERE / d).mkdir(parents=True, exist_ok=True)
    for name in names:
        if not (HERE / d / name).exists():
            url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{BRANCH}/{d}/{name}"
            urllib.request.urlretrieve(url, HERE / d / name)

torch.manual_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
print("torch", torch.__version__, "| torch_geometric", __import__("torch_geometric").__version__)


# ---------------------------------------------------------------- cell 4: data

def load_social():
    """The two observable graphs and the three query splits."""
    n = json.loads((HERE / "data/task1/split_stats.json").read_text())["n_nodes"]

    def as_edge_index(df):
        e = df[["src", "dst"]].to_numpy().T
        return coalesce(to_undirected(torch.from_numpy(e).long()), num_nodes=n)

    train_edges = pd.read_csv(HERE / "data/task1/lp_graph_obs.csv")
    splits = {s: pd.read_csv(HERE / f"data/task1/lp_{s}.csv")
              for s in ("train", "val", "test")}

    val_pos = splits["val"].query("label == 1")[["src", "dst"]]
    trainval_edges = pd.concat([train_edges[["src", "dst"]], val_pos], ignore_index=True)

    return dict(num_nodes=n, splits=splits,
                ei_train=as_edge_index(train_edges),
                ei_trainval=as_edge_index(trainval_edges))


DATA = load_social()
N_NODES = DATA["num_nodes"]
EI_TRAIN, EI_TRAINVAL = DATA["ei_train"], DATA["ei_trainval"]
SPLITS = DATA["splits"]

PAIRS = {s: torch.from_numpy(df[["src", "dst"]].to_numpy()).long()
         for s, df in SPLITS.items()}
LABELS = {s: torch.from_numpy(df["label"].to_numpy()).float()
          for s, df in SPLITS.items()}

print(f"nodes              {N_NODES}")
print(f"G_train            {EI_TRAIN.size(1) // 2} undirected edges, "
      f"{int((degree(EI_TRAIN[1], N_NODES) == 0).sum())} isolated nodes")
print(f"G_trainval         {EI_TRAINVAL.size(1) // 2} undirected edges, "
      f"{int((degree(EI_TRAINVAL[1], N_NODES) == 0).sum())} isolated nodes")
for s in ("train", "val", "test"):
    df = SPLITS[s]
    print(f"{s:18} {df['query_id'].nunique():>6} queries, {len(df):>6} candidate pairs "
          f"({len(df) // df['query_id'].nunique()} per query)")


# ------------------------------------------------- cell 6: node2vec features

from gensim.models import Word2Vec

N2V_DIM = 64


def neighbour_table(edge_index, num_nodes):
    order = torch.argsort(edge_index[1])
    flat = edge_index[0][order].numpy()
    tgt = edge_index[1][order].numpy()
    ptr = np.searchsorted(tgt, np.arange(num_nodes + 1))
    return flat, ptr


def node2vec_features(edge_index, num_nodes, dim=N2V_DIM, p=1.0, q=0.5,
                      walks_per_node=10, walk_length=20, window=10, epochs=1,
                      seed=RANDOM_SEED):
    flat, ptr = neighbour_table(edge_index, num_nodes)
    nbrs = lambda u: flat[ptr[u]:ptr[u + 1]]
    uniform = (p == 1.0 and q == 1.0)
    nbr_sets = None if uniform else [set(nbrs(u).tolist()) for u in range(num_nodes)]

    rng = random.Random(seed)
    t0 = time.time()
    walks = []
    for _ in range(walks_per_node):
        for start in range(num_nodes):
            if ptr[start] == ptr[start + 1]:
                continue
            walk = [start]
            for _ in range(walk_length - 1):
                cur = nbrs(walk[-1])
                if len(cur) == 0:
                    break
                if uniform or len(walk) == 1:
                    walk.append(int(rng.choice(cur)))
                else:
                    prev, prev_nbrs = walk[-2], nbr_sets[walk[-2]]
                    w = [1 / p if x == prev else (1.0 if x in prev_nbrs else 1 / q)
                         for x in cur]
                    walk.append(int(rng.choices(list(cur), weights=w, k=1)[0]))
            walks.append([str(v) for v in walk])
    t1 = time.time()

    model = Word2Vec(walks, vector_size=dim, window=window, min_count=0, sg=1,
                     negative=5, workers=4, epochs=epochs, seed=seed)
    Z = np.zeros((num_nodes, dim), dtype=np.float32)
    for token in model.wv.index_to_key:
        Z[int(token)] = model.wv[token]
    print(f"  {len(walks):,} walks in {t1 - t0:.1f}s, SkipGram in {time.time() - t1:.1f}s")
    return torch.from_numpy(Z)


_CACHE = HERE / "cache" / "x_node2vec.pt"
if _CACHE.exists():
    X = torch.load(_CACHE)
    print("node2vec features  loaded from cache", _CACHE.name)
else:
    X = node2vec_features(EI_TRAIN, N_NODES, p=1.0, q=0.5)
    _CACHE.parent.mkdir(parents=True, exist_ok=True)
    torch.save(X, _CACHE)
X.requires_grad_(False)

n_zero = int((X.abs().sum(1) == 0).sum())
print(f"node2vec features  {tuple(X.shape)}")
print(f"all-zero rows      {n_zero}  (= the users with no training edge)")
print(f"mean row norm      {X[X.abs().sum(1) > 0].norm(dim=1).mean():.2f}")


# ------------------------------------------------------- cell 8: the demo layer

class MySAGEConv(MessagePassing):
    """GraphSAGE, mean aggregator. Complete implementation -- read, do not edit."""

    def __init__(self, in_channels, out_channels):
        super().__init__(aggr="mean")
        self.lin_nbr = nn.Linear(in_channels, out_channels, bias=False)
        self.lin_root = nn.Linear(in_channels, out_channels, bias=True)
        self.reset_parameters()

    def reset_parameters(self):
        super().reset_parameters()
        self.lin_nbr.reset_parameters()
        self.lin_root.reset_parameters()

    def forward(self, x, edge_index):
        agg = self.propagate(edge_index, x=x)
        return self.lin_nbr(agg) + self.lin_root(x)

    def message(self, x_j):
        return x_j


# ----------------------------------------------- cells 10, 11: the frozen harness

def evaluate_ranking(df, scores, seed=RANDOM_SEED):
    rng = np.random.default_rng(seed)
    d = df[["query_id", "label"]].copy()
    d["score"] = scores
    d["tiebreak"] = rng.random(len(d))
    d = d.sort_values(["query_id", "score", "tiebreak"], ascending=[True, False, True])
    d["rank"] = d.groupby("query_id").cumcount() + 1
    pos = d.loc[d["label"] == 1, ["query_id", "rank"]]
    return {"hit@1": float((pos["rank"] == 1).mean()),
            "MRR": float((1.0 / pos["rank"]).mean())}


class GNNLinkPredictor(nn.Module):
    """node2vec features -> conv stack -> dot-product score per candidate pair."""

    def __init__(self, conv_cls, in_channels=N2V_DIM, hidden=64, n_layers=2, dropout=0.5):
        super().__init__()
        dims = [in_channels] + [hidden] * n_layers
        self.convs = nn.ModuleList(
            [conv_cls(dims[i], dims[i + 1]) for i in range(n_layers)])
        for conv in self.convs:
            conv.reset_parameters()
        self.dropout = dropout

    def encode(self, x, edge_index):
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            if i < len(self.convs) - 1:
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
        return x

    @staticmethod
    def score(z, pairs):
        return (z[pairs[:, 0]] * z[pairs[:, 1]]).sum(-1)


def train_and_eval(name, conv_cls, epochs=200, lr=0.01, weight_decay=5e-4, patience=50,
                   seed=RANDOM_SEED, **model_kwargs):
    """Train on the training queries, select on validation MRR, report test."""
    torch.manual_seed(seed)
    model = GNNLinkPredictor(conv_cls, **model_kwargs)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    best, t0 = {"MRR": -1.0, "epoch": 0}, time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        opt.zero_grad()
        z = model.encode(X, EI_TRAIN)
        loss = F.binary_cross_entropy_with_logits(
            model.score(z, PAIRS["train"]), LABELS["train"])
        loss.backward()
        opt.step()

        model.eval()
        with torch.no_grad():
            val = evaluate_ranking(
                SPLITS["val"],
                model.score(model.encode(X, EI_TRAIN), PAIRS["val"]).numpy())
        if val["MRR"] > best["MRR"]:
            with torch.no_grad():
                test = evaluate_ranking(
                    SPLITS["test"],
                    model.score(model.encode(X, EI_TRAINVAL), PAIRS["test"]).numpy())
            best = dict(epoch=epoch, **val,
                        **{f"test_{k}": v for k, v in test.items()})
        if epoch - best["epoch"] >= patience:
            break

    best["secs"] = time.time() - t0
    best["params"] = sum(p.numel() for p in model.parameters())
    print(f"{name:14} val MRR {best['MRR']:.4f} hit@1 {best['hit@1']:.4f} | "
          f"test MRR {best['test_MRR']:.4f} hit@1 {best['test_hit@1']:.4f} | "
          f"epoch {best['epoch']:3d} | {best['secs']:5.1f}s")
    return best
