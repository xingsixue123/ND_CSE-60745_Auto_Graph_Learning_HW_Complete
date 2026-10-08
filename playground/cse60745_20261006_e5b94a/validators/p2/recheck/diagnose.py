"""Diagnostics: is the low MRR my layer's fault, or the task's?

Imports rgcn_run (which re-runs the frozen harness once at import... no: rgcn_run
guards its run with __main__, so importing only builds the data and the class).
"""
import json, time, numpy as np, torch, torch.nn.functional as F
import rgcn_run as R

H21 = sum(1.0 / k for k in range(1, 22))
print(f"random baseline (21 candidates)  MRR {H21/21:.4f}  hit@1 {1/21:.4f}")

# --- 0. no-GNN baseline: dot product of the raw metapath2vec features
for s in ("val", "test"):
    m = R.evaluate_ranking(R.SPLITS[s], R.GNNLinkPredictor.score(R.X_HETERO, R.PAIRS[s]).numpy())
    print(f"raw X_HETERO dot product  {s:5} MRR {m['MRR']:.4f}  hit@1 {m['hit@1']:.4f}")

# --- 1. full 50-epoch val curve, no early stopping, same seed/optimiser as the harness
torch.manual_seed(R.RANDOM_SEED)
model = R.RGCNLinkPredictor(R.HETERO["num_relations"])
opt = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
g = R.HETERO
print("\nepoch  train_loss   val_MRR  val_hit@1   (no early stopping)")
t0 = time.time()
for epoch in range(1, 51):
    model.train(); opt.zero_grad()
    z = model.encode(R.X_HETERO, g["edge_index"], g["edge_type"])
    assert torch.isfinite(z).all(), f"non-finite embeddings at epoch {epoch}"
    loss = F.binary_cross_entropy_with_logits(model.score(z, R.PAIRS["train"]), R.LABELS["train"])
    loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        z = model.encode(R.X_HETERO, g["edge_index"], g["edge_type"])
        v = R.evaluate_ranking(R.SPLITS["val"], model.score(z, R.PAIRS["val"]).numpy())
    print(f"{epoch:5d}  {float(loss):9.5f}  {v['MRR']:8.4f}  {v['hit@1']:9.4f}")
print(f"50 epochs in {time.time()-t0:.1f}s")

# --- 2. per-relation message magnitudes at init, to check nothing is degenerate
conv = model.convs[0]
with torch.no_grad():
    n = R.HETERO["num_nodes"]
    print("\nper-relation contribution norms at the trained layer-0:")
    print(f"  root W_0 x        mean row norm {conv.root(R.X_HETERO).norm(dim=1).mean():.4f}")
    for r in range(3):
        ei = g["edge_index"][:, g["edge_type"] == r]
        c = conv.propagate(ei, x=conv.rel[r](R.X_HETERO), size=(n, n))
        nz = int((c.abs().sum(1) == 0).sum())
        print(f"  relation {r}        mean row norm {c.norm(dim=1).mean():.4f}   "
              f"all-zero rows (|N_r(i)|=0): {nz}")
