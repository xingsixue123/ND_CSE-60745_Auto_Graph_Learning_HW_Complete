"""
Load every small homogeneous benchmark through PyTorch Geometric and report the
ground-truth statistics, so that no number in answer.tex is quoted from memory.

For each dataset we report:
  N                  number of nodes
  E_dir              number of entries in edge_index (PyG stores an undirected
                     edge twice, so this is the "directed"/"stored" edge count)
  E_und              number of distinct undirected edges (unordered pairs,
                     self-loops counted once)
  undirected         whether edge_index is symmetric
  selfloops          number of self-loop entries
  d                  node-feature dimension
  feat               'binary' if x in {0,1}, else 'real'
  C                  number of classes (or number of binary tasks if multilabel)
  multilabel         whether y is a label matrix rather than a vector

Usage:  ./.venv/bin/python stats.py           (writes stats_out.json + prints a table)
"""
import json
import os
import sys
import traceback

import torch

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(ROOT, exist_ok=True)


def summarize(name, data, num_classes=None, note=""):
    ei = data.edge_index
    N = int(data.num_nodes)
    E_dir = int(ei.size(1))

    src, dst = ei[0], ei[1]
    selfloops = int((src == dst).sum())

    # distinct undirected edges: canonicalise each pair as (min, max) and dedupe
    lo = torch.minimum(src, dst).to(torch.int64)
    hi = torch.maximum(src, dst).to(torch.int64)
    key = lo * N + hi
    E_und = int(torch.unique(key).numel())

    # symmetry test: is the set of ordered pairs closed under transposition?
    fwd = torch.unique(src.to(torch.int64) * N + dst.to(torch.int64))
    bwd = torch.unique(dst.to(torch.int64) * N + src.to(torch.int64))
    undirected = bool(fwd.numel() == bwd.numel() and torch.equal(fwd, bwd))

    x = getattr(data, "x", None)
    if x is None:
        d, feat = 0, "none"
    else:
        d = int(x.size(1))
        vals = torch.unique(x)
        feat = "binary" if vals.numel() <= 2 and bool(
            ((vals == 0) | (vals == 1)).all()) else "real"

    y = getattr(data, "y", None)
    multilabel = bool(y is not None and y.dim() > 1 and y.size(1) > 1)
    if multilabel:
        C = int(y.size(1))
    elif num_classes is not None:
        C = int(num_classes)
    elif y is not None:
        C = int(y.max()) + 1
    else:
        C = None

    return dict(name=name, N=N, E_dir=E_dir, E_und=E_und, undirected=undirected,
                selfloops=selfloops, d=d, feat=feat, C=C,
                multilabel=multilabel, note=note)


def main():
    from torch_geometric.datasets import (Planetoid, WebKB, Actor,
                                          WikipediaNetwork, Coauthor, Amazon,
                                          AttributedGraphDataset, PPI, Flickr)

    jobs = []
    for n in ["Cora", "CiteSeer", "PubMed"]:
        jobs.append((f"{n} (Planetoid)",
                     lambda n=n: Planetoid(root=f"{ROOT}/Planetoid", name=n)))
    for n in ["Cornell", "Texas", "Wisconsin"]:
        jobs.append((f"{n} (WebKB)",
                     lambda n=n: WebKB(root=f"{ROOT}/WebKB", name=n)))
    jobs.append(("Actor", lambda: Actor(root=f"{ROOT}/Actor")))
    for n in ["chameleon", "squirrel"]:
        jobs.append((f"{n} (WikipediaNetwork)",
                     lambda n=n: WikipediaNetwork(root=f"{ROOT}/Wiki", name=n,
                                                  geom_gcn_preprocess=True)))
    for n in ["CS", "Physics"]:
        jobs.append((f"Coauthor {n}",
                     lambda n=n: Coauthor(root=f"{ROOT}/Coauthor", name=n)))
    for n in ["Computers", "Photo"]:
        jobs.append((f"Amazon {n}",
                     lambda n=n: Amazon(root=f"{ROOT}/Amazon", name=n)))
    for n in ["BlogCatalog", "Flickr"]:
        jobs.append((f"{n} (AttributedGraphDataset)",
                     lambda n=n: AttributedGraphDataset(root=f"{ROOT}/Attr", name=n)))
    jobs.append(("Flickr (GraphSAINT)", lambda: Flickr(root=f"{ROOT}/FlickrSAINT")))

    results = []
    for label, ctor in jobs:
        try:
            ds = ctor()
            results.append(summarize(label, ds[0], getattr(ds, "num_classes", None)))
            print("ok  ", label, flush=True)
        except Exception as e:
            print("FAIL", label, repr(e)[:200], flush=True)
            traceback.print_exc(file=sys.stdout)
            results.append(dict(name=label, error=repr(e)[:300]))

    # PPI is a *set* of 24 graphs (inductive), so it needs its own accounting.
    try:
        tot_n = tot_e = 0
        ngraphs = 0
        d = C = None
        for split in ["train", "val", "test"]:
            ds = PPI(root=f"{ROOT}/PPI", split=split)
            for g in ds:
                tot_n += int(g.num_nodes)
                tot_e += int(g.edge_index.size(1))
                ngraphs += 1
                d = int(g.x.size(1))
                C = int(g.y.size(1))
        results.append(dict(name="PPI (all 24 graphs)", N=tot_n, E_dir=tot_e,
                            E_und=tot_e // 2, undirected=True, selfloops=None,
                            d=d, feat="real", C=C, multilabel=True,
                            note=f"{ngraphs} graphs; inductive split 20/2/2"))
        print("ok   PPI", ngraphs, "graphs", flush=True)
    except Exception as e:
        print("FAIL PPI", repr(e)[:200], flush=True)
        results.append(dict(name="PPI", error=repr(e)[:300]))

    with open("stats_out.json", "w") as f:
        json.dump(results, f, indent=2)

    hdr = f"{'dataset':34s} {'N':>12s} {'E_dir':>12s} {'E_und':>12s} {'und':>5s} {'loops':>6s} {'d':>6s} {'feat':>7s} {'C':>5s} {'ml':>3s}"
    print("\n" + hdr)
    print("-" * len(hdr))
    for r in results:
        if "error" in r:
            print(f"{r['name']:34s} ERROR {r['error'][:60]}")
            continue
        print(f"{r['name']:34s} {r['N']:12,d} {r['E_dir']:12,d} {r['E_und']:12,d} "
              f"{str(r['undirected']):>5s} {str(r['selfloops']):>6s} {r['d']:6d} "
              f"{r['feat']:>7s} {str(r['C']):>5s} {str(r['multilabel'])[0]:>3s}")


if __name__ == "__main__":
    main()
