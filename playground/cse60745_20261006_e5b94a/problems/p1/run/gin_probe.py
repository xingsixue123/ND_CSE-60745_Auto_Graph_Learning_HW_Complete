"""Why is GIN the weakest row? Check whether sum aggregation ties the embedding norm
(and so the dot-product score) to node degree."""
import numpy as np, torch
from common import X, EI_TRAIN, N_NODES, GNNLinkPredictor
from layers import MyGCNConv, MyGINConv
from torch_geometric.utils import degree

deg = degree(EI_TRAIN[1], N_NODES).numpy()
m = deg > 0
for name, cls, nl in [("GCN-2", MyGCNConv, 2), ("GIN", MyGINConv, 2)]:
    torch.manual_seed(0)
    model = GNNLinkPredictor(cls, n_layers=nl).eval()
    with torch.no_grad():
        z = model.encode(X, EI_TRAIN).numpy()
    nrm = np.linalg.norm(z, axis=1)
    r = np.corrcoef(np.log(deg[m]), np.log(nrm[m] + 1e-12))[0, 1]
    print(f"{name:6} corr(log degree, log ||z||) = {r:+.3f} | "
          f"||z|| ratio top-decile deg / bottom-decile deg = "
          f"{nrm[m][deg[m] >= np.quantile(deg[m],0.9)].mean() / nrm[m][deg[m] <= np.quantile(deg[m],0.1)].mean():.2f}x")
