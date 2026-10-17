import torch, time
torch.set_num_threads(4)
from gt_framework import *
from hybrid_layer import HybridGT
from variants import *
graphs = ZINC_GRAPHS["train"][:16]
ensure_precomputed(graphs, [HybridGT.precompute])
b = make_batch(graphs, HybridGT.precompute)
for cls in [None, LocalOnlyLayer, GlobalOnlyLayer, SequentialLayer, GatedLayer]:
    m = HybridGT() if cls is None else HybridGT(layer_cls=cls)
    o = m(b); o.sum().backward()
    nog = [n for n,p in m.named_parameters() if p.grad is None]
    print(f"{(cls.__name__ if cls else 'HybridGTLayer'):18} out {tuple(o.shape)} finite {bool(torch.isfinite(o).all())} "
          f"params {sum(p.numel() for p in m.parameters()):7d} no-grad {nog}")
# timing: one epoch-equivalent of 79 steps
m = HybridGT(); opt = torch.optim.Adam(m.parameters(), 1e-3)
t0=time.time()
for i in range(0, 128*10, 128):
    g = ZINC_GRAPHS["train"][i:i+128]
    ensure_precomputed(g, [HybridGT.precompute])
    bb = make_batch(g, HybridGT.precompute)
    p = m(bb).view(-1); y = torch.cat([x["y"] for x in g])
    loss = F.l1_loss(p,y); opt.zero_grad(); loss.backward(); opt.step()
print(f"10 train steps in {time.time()-t0:.2f}s -> ~{(time.time()-t0)/10*79:.1f}s/epoch (4 threads)")
