"""Framework code of task6_graph_transformer-1.ipynb, extracted VERBATIM.

Cells 3, 5, 7, 8, 9 in full; the two demo classes of cell 11 (without the run
line); PAIR_TYPES and pair_types() from cell 16.  Nothing here is an answer to
Q1/Q2/Q3 -- the TODO cells (13, 16 SparseSPDAttention, 21) are NOT included.
Import this module and define your own classes on top of it.
"""


# ===================== notebook cell 3 =====================
try:
    import torch_geometric
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "torch_geometric"], check=True)

import json
import math
import random
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import f1_score

from torch_geometric.datasets import ZINC
from torch_geometric.utils import coalesce, softmax as segment_softmax, to_dense_batch, to_undirected

GITHUB_REPO = "antman9914/CSE60745-Practice"
BRANCH = "main"
REQUIRED = {
    "data/task2": ["edges_all.csv", "node_country.csv"],
    "data/task3": ["country_split.csv"],
}
for d, names in REQUIRED.items():
    Path(d).mkdir(parents=True, exist_ok=True)
    for name in names:
        if not (Path(d) / name).exists():
            url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{BRANCH}/{d}/{name}"
            urllib.request.urlretrieve(url, Path(d) / name)

RANDOM_SEED = 0
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("torch", torch.__version__, "| torch_geometric", torch_geometric.__version__, "| device", DEVICE)


# ===================== notebook cell 5 =====================
def load_zinc():
    out = {}
    for split in ("train", "val", "test"):
        ds = ZINC("data/zinc", subset=True, split=split)
        out[split] = [dict(n=d.num_nodes, x=d.x.view(-1).long(), edge_index=d.edge_index,
                           edge_attr=d.edge_attr.long(), y=d.y.float(), enc={}) for d in ds]
    return out


def load_lastfm():
    country = (pd.read_csv("data/task2/node_country.csv")
               .set_index("node_id")["country"])
    n = len(country)
    e = pd.read_csv("data/task2/edges_all.csv")[["src", "dst"]].to_numpy().T
    edge_index = coalesce(to_undirected(torch.from_numpy(e).long()), num_nodes=n)
    split = (pd.read_csv("data/task3/country_split.csv")
             .set_index("node_id")["split"].reindex(range(n)))
    masks = {f"{s}_mask": torch.from_numpy((split == s).to_numpy()) for s in ("train", "val", "test")}
    y = torch.from_numpy(country.reindex(range(n)).to_numpy()).long()
    return dict(n=n, x=None, edge_index=edge_index, edge_attr=None, y=y, enc={}, **masks)


ZINC_GRAPHS = load_zinc()
LASTFM = load_lastfm()
N_COUNTRIES = int(LASTFM["y"].max()) + 1

for s, gs in ZINC_GRAPHS.items():
    print(f"ZINC {s:5} {len(gs):6} graphs, {np.mean([g['n'] for g in gs]):.1f} nodes on average")
print(f"LastFM      {LASTFM['n']} nodes, {LASTFM['edge_index'].size(1) // 2} edges, "
      f"{N_COUNTRIES} countries, train/val/test users "
      f"{int(LASTFM['train_mask'].sum())}/{int(LASTFM['val_mask'].sum())}/{int(LASTFM['test_mask'].sum())}")


# ===================== notebook cell 7 =====================
def ensure_precomputed(graphs, fns):
    """Run every precompute function once per graph and cache its output."""
    for g in graphs:
        cache = g.setdefault("cache", {})
        for fn in fns:
            if fn is not None and fn not in cache:
                cache[fn] = {k: torch.as_tensor(v) for k, v in fn(g["edge_index"], g["n"]).items()}
                for k, v in cache[fn].items():
                    assert v.size(0) == g["n"], f"precompute output '{k}' has {v.size(0)} rows, expected {g['n']}"


def precompute_fns(model):
    """(node-level precompute, pair-level precompute, attention_pairs) of a model."""
    attention_cls = getattr(model, "attention_cls", None)
    return (type(model).precompute,
            attention_cls.precompute if attention_cls is not None else None,
            getattr(attention_cls, "attention_pairs", None))


def ensure_pairs(graphs, pairs_fn):
    """Compute (once) the attention pairs of every graph (Q2)."""
    for g in graphs:
        cached = g.get("pairs")
        if cached is None or cached[0] is not pairs_fn:
            pairs = torch.as_tensor(pairs_fn(g["edge_index"], g["n"])).long()
            assert pairs.dim() == 2 and pairs.size(0) == 2, f"expected [2, P], got {tuple(pairs.shape)}"
            assert pairs.numel() == 0 or int(pairs.min()) >= 0, "node ids must be non-negative"
            # ids >= num_nodes are virtual nodes; the largest id fixes how many there are
            n_virtual = max(0, int(pairs.max()) + 1 - g["n"]) if pairs.numel() else 0
            g["pairs"] = (pairs_fn, pairs, n_virtual, pair_types(pairs, g["edge_index"], g["n"]))


def make_batch(graphs, node_fn, pair_fn=None, pairs_fn=None):
    """Concatenate graphs.

    Dense mode (pairs_fn is None): pair-level features are padded to [B, N, N].
    Sparse mode: each graph's virtual nodes follow its real nodes, the attention pairs are
    concatenated into batch["pairs"], and pair-level features are read off at those pairs,
    one value per pair ([P]; 0 for pairs with a virtual node).
    """
    xs, eis, eas, bvec, virt, prs = [], [], [], [], [], []
    node_keys = list(graphs[0]["cache"][node_fn]) if node_fn is not None else []
    pair_keys = list(graphs[0]["cache"][pair_fn]) if pair_fn is not None else []
    node_feats = {k: [] for k in node_keys}
    pair_feats = {k: [] for k in pair_keys + (["pair_type"] if pairs_fn is not None else [])}
    offset = 0
    for gi, g in enumerate(graphs):
        n = g["n"]
        nv = g["pairs"][2] if pairs_fn is not None else 0
        if g["x"] is not None:
            xs.append(torch.cat([g["x"], torch.zeros(nv, dtype=torch.long)]))
        eis.append(g["edge_index"] + offset)
        if g["edge_attr"] is not None:
            eas.append(g["edge_attr"])
        bvec.append(torch.full((n + nv,), gi, dtype=torch.long))
        virt.append(torch.cat([torch.zeros(n, dtype=torch.bool), torch.ones(nv, dtype=torch.bool)]))
        for k in node_keys:
            t = g["cache"][node_fn][k]
            node_feats[k].append(torch.cat([t, torch.zeros((nv,) + tuple(t.shape[1:]), dtype=t.dtype)]))
        if pairs_fn is not None:
            p = g["pairs"][1]
            src, dst = p
            real = (src < n) & (dst < n)
            for k in pair_keys:
                full = g["cache"][pair_fn][k]
                vals = torch.zeros(p.size(1), dtype=full.dtype)
                vals[real] = full[dst[real], src[real]]                     # value for "dst attends to src"
                pair_feats[k].append(vals)
            pair_feats["pair_type"].append(g["pairs"][3])
            prs.append(p + offset)
        offset += n + nv
    out = dict(x=torch.cat(xs) if xs else None, edge_index=torch.cat(eis, 1),
               edge_attr=torch.cat(eas) if eas else None, batch=torch.cat(bvec),
               virtual=torch.cat(virt), num_graphs=len(graphs), pair_enc={})
    out.update({k: torch.cat(v) for k, v in node_feats.items()})
    if pairs_fn is not None:
        out["pairs"] = torch.cat(prs, 1)
        out["pair_enc"] = {k: torch.cat(v) for k, v in pair_feats.items()}
    elif pair_fn is not None:
        N = max(g["n"] for g in graphs)
        for k in pair_keys:
            t0 = graphs[0]["cache"][pair_fn][k]
            buf = torch.zeros((len(graphs), N, N), dtype=t0.dtype)
            for b, g in enumerate(graphs):
                buf[b, :g["n"], :g["n"]] = g["cache"][pair_fn][k]
            out["pair_enc"][k] = buf
    return out


def to_device(obj):
    if torch.is_tensor(obj):
        return obj.to(DEVICE)
    if isinstance(obj, dict):
        return {k: to_device(v) for k, v in obj.items()}
    return obj


# ===================== notebook cell 8 =====================
class Attention(nn.Module):
    """Multi-head attention among the nodes of each graph, with no structural information."""

    def __init__(self, dim, heads):
        super().__init__()
        self.heads = heads
        self.qkv, self.out = nn.Linear(dim, 3 * dim), nn.Linear(dim, dim)

    @staticmethod
    def precompute(edge_index, num_nodes):
        """Pair-level features of one graph: a dict of [num_nodes, num_nodes] tensors."""
        return {}

    def forward(self, h, enc, mask):
        """h    : [B, N, dim], node states of each graph, padded to N nodes
        enc  : dict of pair-level features from precompute, each [B, N, N] (unused here)
        mask : [B, N] bool, False marks padding
        Returns [B, N, dim]."""
        B, N, D = h.shape
        q, k, v = self.qkv(h).view(B, N, 3, self.heads, D // self.heads).permute(2, 0, 3, 1, 4)
        scores = q @ k.transpose(-1, -2) / math.sqrt(D // self.heads)      # [B, H, N, N]
        scores = scores.masked_fill(~mask[:, None, None, :], float("-inf"))
        weights = torch.softmax(scores, dim=-1).nan_to_num(0.0)
        return self.out((weights @ v).transpose(1, 2).reshape(B, N, D))


class TransformerBlock(nn.Module):
    def __init__(self, attention, dim):
        super().__init__()
        self.attention = attention
        self.norm1, self.norm2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        self.ffn = nn.Sequential(nn.Linear(dim, 2 * dim), nn.ReLU(), nn.Linear(2 * dim, dim))

    def forward(self, h, enc, mask_or_pairs):
        h = h + self.attention(self.norm1(h), enc, mask_or_pairs)
        return h + self.ffn(self.norm2(h))


class GraphTransformer(nn.Module):
    """Graph transformer with full attention inside every graph."""

    def __init__(self, attention_cls=Attention, dim=64, heads=4, layers=4, out_dim=1,
                 num_atom_types=21, graph_level=True):
        super().__init__()
        self.attention_cls, self.dim, self.graph_level = attention_cls, dim, graph_level
        self.sparse = hasattr(attention_cls, "attention_pairs")             # Q2: attention on chosen pairs
        self.atom = nn.Embedding(num_atom_types, dim) if num_atom_types else None
        self.virtual = nn.Parameter(torch.zeros(dim))                       # start state of virtual nodes
        self.blocks = nn.ModuleList([TransformerBlock(attention_cls(dim, heads), dim) for _ in range(layers)])
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Sequential(nn.Linear(dim, dim), nn.ReLU(), nn.Linear(dim, out_dim))

    @staticmethod
    def precompute(edge_index, num_nodes):
        """Node-level features of one graph: a dict of [num_nodes, ...] tensors."""
        return {}

    def inject_absolute(self, h, batch):
        """Absolute encoding hook, applied once to the input node states h [num_nodes, dim].
        The precompute output is in batch[key], [num_nodes, ...]."""
        return h

    def forward(self, batch):
        M = batch["batch"].size(0)
        h = self.atom(batch["x"]) if self.atom is not None else torch.zeros(M, self.dim, device=batch["batch"].device)
        h = self.inject_absolute(h, batch)
        if self.sparse:
            h = torch.where(batch["virtual"][:, None], self.virtual.expand(M, -1), h)
            for block in self.blocks:
                h = block(h, batch["pair_enc"], batch["pairs"])
            h = self.norm(h)
        else:
            h, mask = to_dense_batch(h, batch["batch"])                      # [B, N, dim], [B, N]
            for block in self.blocks:
                h = block(h, batch["pair_enc"], mask)
            h = self.norm(h)[mask]                                           # back to [num_nodes, dim]
        if self.graph_level:
            return self.head(graph_mean_pool(h, batch["batch"], ~batch["virtual"]))
        return self.head(h)


def graph_mean_pool(h, batch, keep):
    """Mean of h over the nodes with keep=True (the real nodes), per graph."""
    G = int(batch.max()) + 1
    s = torch.zeros(G, h.size(1), device=h.device).index_add_(0, batch[keep], h[keep])
    c = torch.zeros(G, device=h.device).index_add_(0, batch[keep], torch.ones_like(batch[keep], dtype=h.dtype))
    return s / c.clamp(min=1)[:, None]


# ===================== notebook cell 9 =====================
EPOCHS_ZINC = 30
EPOCHS_LASTFM = 200
LAP_K = 8                   # number of Laplacian eigenvectors (Q1)


def _reset(model):
    """Re-initialise every layer under the fixed seed, so each run starts from the same
    weights however many random numbers earlier cells used."""
    torch.manual_seed(RANDOM_SEED)
    for m in model.modules():
        if m is not model and hasattr(m, "reset_parameters"):
            m.reset_parameters()


def _prepare(model, graphs):
    node_fn, pair_fn, pairs_fn = precompute_fns(model)
    ensure_precomputed(graphs, [node_fn, pair_fn])
    if pairs_fn is not None:
        ensure_pairs(graphs, pairs_fn)
    return node_fn, pair_fn, pairs_fn


def run_graph_task(name, model, epochs=None, lr=1e-3, batch_size=128):
    """Train on ZINC train, select the epoch on val MAE, report val and test MAE."""
    epochs = epochs or EPOCHS_ZINC
    data = ZINC_GRAPHS
    for split in data.values():
        node_fn, pair_fn, pairs_fn = _prepare(model, split)
    _reset(model)
    rng = np.random.default_rng(RANDOM_SEED)
    model = model.to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    def predict(graphs):
        batch = to_device(make_batch(graphs, node_fn, pair_fn, pairs_fn))
        return model(batch).view(-1), torch.cat([g["y"] for g in graphs]).to(DEVICE)

    def mae(split):
        model.eval()
        err, n = 0.0, 0
        with torch.no_grad():
            for i in range(0, len(data[split]), 256):
                p, y = predict(data[split][i:i + 256])
                err += (p - y).abs().sum().item()
                n += len(y)
        return err / n

    best, t0 = dict(val=float("inf")), time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        order = rng.permutation(len(data["train"]))
        for i in range(0, len(order), batch_size):
            p, y = predict([data["train"][j] for j in order[i:i + batch_size]])
            loss = F.l1_loss(p, y)
            opt.zero_grad()
            loss.backward()
            opt.step()
        v = mae("val")
        if v < best["val"]:
            best = dict(val=v, test=mae("test"), epoch=epoch)
    secs = time.time() - t0
    print(f"{name:34} val MAE {best['val']:.4f} | test MAE {best['test']:.4f} | "
          f"best epoch {best['epoch']:3d} | {secs / epochs:.1f}s/epoch")
    return best


def run_node_task(name, model, epochs=None, lr=1e-3):
    """Full-batch training on LastFM, select on val micro-F1, report val and test micro-F1."""
    epochs = epochs or EPOCHS_LASTFM
    g = LASTFM
    node_fn, pair_fn, pairs_fn = _prepare(model, [g])
    _reset(model)
    model = model.to(DEVICE)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    batch = to_device(make_batch([g], node_fn, pair_fn, pairs_fn))
    y = g["y"].to(DEVICE)
    masks = {s: g[f"{s}_mask"].to(DEVICE) for s in ("train", "val", "test")}

    def logits():
        return model(batch)[~batch["virtual"]]

    def f1(split, out):
        return f1_score(y[masks[split]].cpu(), out[masks[split]].argmax(1).cpu(), average="micro")

    best, t0 = dict(val=-1.0), time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        loss = F.cross_entropy(logits()[masks["train"]], y[masks["train"]])
        opt.zero_grad()
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            out = logits()
        v = f1("val", out)
        if v > best["val"]:
            best = dict(val=v, test=f1("test", out), epoch=epoch)
    secs = time.time() - t0
    print(f"{name:34} val micro-F1 {best['val']:.4f} | test micro-F1 {best['test']:.4f} | "
          f"best epoch {best['epoch']:3d} | {secs / epochs:.2f}s/epoch")
    return best


def benchmark_step(name, model):
    """Time one training step on LastFM and count the node pairs that attention touches."""
    g = LASTFM
    node_fn, pair_fn, pairs_fn = _prepare(model, [g])
    model = model.to(DEVICE)
    batch = to_device(make_batch([g], node_fn, pair_fn, pairs_fn))
    n_pairs = batch["pairs"].size(1) if pairs_fn is not None else g["n"] ** 2
    if DEVICE.type == "cuda":
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    try:
        t0 = time.time()
        model(batch).float().sum().backward()
        if DEVICE.type == "cuda":
            torch.cuda.synchronize()
        secs = time.time() - t0
        mem = f"{torch.cuda.max_memory_allocated() / 2**30:.2f} GB" if DEVICE.type == "cuda" else "n/a on CPU"
        print(f"{name:34} pairs attended {n_pairs:>12,} | one step {secs:6.2f}s | peak GPU memory {mem}")
    except RuntimeError as e:
        print(f"{name:34} pairs attended {n_pairs:>12,} | FAILED: {str(e).splitlines()[0][:80]}")


# ===================== notebook cell 11 (demo classes only) =====================
class CentralityTransformer(GraphTransformer):
    """Absolute encoding: degree centrality, added to the input once."""

    def __init__(self, *args, max_degree=64, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_degree = max_degree
        self.degree_table = nn.Embedding(max_degree + 1, self.dim)

    @staticmethod
    def precompute(edge_index, num_nodes):
        return {"deg": torch.bincount(edge_index[0], minlength=num_nodes)}

    def inject_absolute(self, h, batch):
        return h + self.degree_table(batch["deg"].clamp(max=self.max_degree))


class CNAttention(Attention):
    """Relative encoding: number of common neighbours, one learnable bias per head."""

    def __init__(self, dim, heads, max_cn=8):
        super().__init__(dim, heads)
        self.max_cn = max_cn
        self.cn_table = nn.Embedding(max_cn + 1, heads)

    @staticmethod
    def precompute(edge_index, num_nodes):
        A = torch.zeros(num_nodes, num_nodes)
        A[edge_index[0], edge_index[1]] = 1.0
        return {"cn": (A @ A).long()}

    def forward(self, h, enc, mask):
        B, N, D = h.shape
        q, k, v = self.qkv(h).view(B, N, 3, self.heads, D // self.heads).permute(2, 0, 3, 1, 4)
        scores = q @ k.transpose(-1, -2) / math.sqrt(D // self.heads)      # [B, H, N, N]
        bias = self.cn_table(enc["cn"].clamp(max=self.max_cn))            # [B, N, N, H]
        scores = scores + bias.permute(0, 3, 1, 2)
        scores = scores.masked_fill(~mask[:, None, None, :], float("-inf"))
        weights = torch.softmax(scores, dim=-1).nan_to_num(0.0)
        return self.out((weights @ v).transpose(1, 2).reshape(B, N, D))


# ===================== notebook cell 16 (PAIR_TYPES / pair_types only) =====================
PAIR_TYPES = ("self", "edge", "virtual", "other")     # labels the framework gives attention pairs


def pair_types(pairs, edge_index, num_nodes):
    """Label every pair: a virtual node at either end, a self loop, a graph edge, or other."""
    src, dst = pairs
    total = max(num_nodes, int(pairs.max()) + 1 if pairs.numel() else 0)   # ids that can occur
    is_edge = torch.isin(src * total + dst, edge_index[0] * total + edge_index[1])
    t = torch.full_like(src, PAIR_TYPES.index("other"))
    t[is_edge] = PAIR_TYPES.index("edge")
    t[src == dst] = PAIR_TYPES.index("self")
    t[(src >= num_nodes) | (dst >= num_nodes)] = PAIR_TYPES.index("virtual")
    return t

