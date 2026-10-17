import torch
torch.set_num_threads(1)
from hybrid_layer import HybridGTLayer, HybridGT
from variants import AblationGT, LocalOnlyLayer, GlobalOnlyLayer
from gt_framework import *
from gt_framework import _reset

a, b = HybridGT(), AblationGT(HybridGTLayer)
_reset(a); _reset(b)
pa, pb = dict(a.named_parameters()), dict(b.named_parameters())
print("[G] same param names:", set(pa) == set(pb),
      "max|delta|:", max((pa[k]-pb[k]).abs().max().item() for k in pa))

# the ablations must share the *same* init for the parameters they do keep
for cls in (LocalOnlyLayer, GlobalOnlyLayer):
    m = AblationGT(cls); _reset(m)
    pm = dict(m.named_parameters())
    d = max((pa[k]-pm[k]).abs().max().item() for k in pm)
    print(f"[G] {cls.__name__}: shares every parameter name with HybridGT "
          f"({set(pm)==set(pa)}), max|init delta| {d:.3e}")

# and the active-parameter count must equal the hand-computed drop
per_layer_attn = 64*192+192 + 64*64+64 + 2*64      # qkv + proj + norm_global
per_layer_mpnn = 4*64 + 1 + (64*128+128)+(128*64+64) + 2*64   # bond + eps + mpnn + norm_local
tot = sum(p.numel() for p in a.parameters())
print(f"[G] total {tot}; local-only expected {tot-4*per_layer_attn}; "
      f"global-only expected {tot-4*per_layer_mpnn}")
