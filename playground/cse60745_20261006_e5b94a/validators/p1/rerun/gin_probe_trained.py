"""Validator check: does the Q3 degree-coupling claim survive TRAINING, and does it
survive measuring in train() mode where BatchNorm actually normalises?"""
import numpy as np, torch
import torch.nn.functional as F
from common import (X, EI_TRAIN, N_NODES, GNNLinkPredictor, SPLITS, PAIRS, LABELS,
                    evaluate_ranking)
from layers import MyGCNConv, MyGINConv
from torch_geometric.utils import degree

deg = degree(EI_TRAIN[1], N_NODES).numpy()
m = deg > 0

def stats(z):
    nrm = np.linalg.norm(z, axis=1)
    r = np.corrcoef(np.log(deg[m]), np.log(nrm[m] + 1e-12))[0, 1]
    hi = nrm[m][deg[m] >= np.quantile(deg[m], 0.9)].mean()
    lo = nrm[m][deg[m] <= np.quantile(deg[m], 0.1)].mean()
    return r, hi / lo

for name, cls in [("GCN-2", MyGCNConv), ("GIN", MyGINConv)]:
    torch.manual_seed(0)
    model = GNNLinkPredictor(cls, n_layers=2)
    # (a) at init, eval mode -- the worker's measurement
    model.eval()
    with torch.no_grad():
        r0, q0 = stats(model.encode(X, EI_TRAIN).numpy())
    # (b) at init, train mode -- BatchNorm actually normalising (dropout off via p=0)
    model.train(); model.dropout = 0.0
    with torch.no_grad():
        r1, q1 = stats(model.encode(X, EI_TRAIN).numpy())
    # (c) after training to the harness's early-stopping point
    torch.manual_seed(0)
    model = GNNLinkPredictor(cls, n_layers=2)
    opt = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    best = {"MRR": -1.0, "epoch": 0}
    for epoch in range(1, 201):
        model.train(); opt.zero_grad()
        z = model.encode(X, EI_TRAIN)
        loss = F.binary_cross_entropy_with_logits(
            model.score(z, PAIRS["train"]), LABELS["train"])
        loss.backward(); opt.step()
        model.eval()
        with torch.no_grad():
            val = evaluate_ranking(SPLITS["val"],
                                   model.score(model.encode(X, EI_TRAIN), PAIRS["val"]).numpy())
        if val["MRR"] > best["MRR"]:
            best = dict(epoch=epoch, **val)
            snap = {k: v.detach().clone() for k, v in model.state_dict().items()}
        if epoch - best["epoch"] >= 50:
            break
    model.load_state_dict(snap); model.eval()
    with torch.no_grad():
        r2, q2 = stats(model.encode(X, EI_TRAIN).numpy())
    print(f"{name:6} init/eval  corr {r0:+.3f} ratio {q0:6.2f}x   "
          f"init/train corr {r1:+.3f} ratio {q1:6.2f}x   "
          f"trained(ep{best['epoch']}) corr {r2:+.3f} ratio {q2:6.2f}x   "
          f"val MRR {best['MRR']:.4f}")
