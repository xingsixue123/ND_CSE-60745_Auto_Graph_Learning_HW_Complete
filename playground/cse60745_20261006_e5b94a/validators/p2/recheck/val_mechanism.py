"""Test answer.tex's causal claim: 'Averaging *within* the two ~400-degree listening
relations smooths the users flat; pooling ... reaches val MRR 0.286.'

Under pooling, each relation-r term for node i is scaled by |N_r(i)|/c_i relative to the
per-relation mean. Measure that scale factor per relation, for users and for artists."""
import torch, json, pandas as pd, numpy as np
from pathlib import Path

stats = json.loads(Path("data/task3/hetero_stats.json").read_text())
nu, na = stats["n_users"], stats["n_artists"]
N = nu + na
ua = pd.read_csv("data/task3/user_artist.csv.gz")
u = torch.from_numpy(ua["user"].to_numpy()).long()
a = torch.from_numpy(ua["artist"].to_numpy()).long()

# relation 0 (friend) from the same G_train the run uses
import re
src = Path("rgcn_run.py").read_text()
ns = {}
exec(compile(src.split("# ===== cell 7")[0], "run", "exec"), ns)   # cells 3 + 5
EI_TRAIN = ns["EI_TRAIN"]

deg = torch.zeros(3, N)
deg[0] = torch.bincount(EI_TRAIN[1], minlength=N).float()      # friend -> user
deg[1] = torch.bincount(a, minlength=N).float()                # listens -> artist
deg[2] = torch.bincount(u, minlength=N).float()                # listened_by -> user
c_pooled = deg.sum(0)

print(f"{'':12}{'mean |N_r(i)|':>16}{'mean c_i':>12}{'scale |N_r|/c_i':>18}")
for r, name in enumerate(["friend", "listens", "listened_by"]):
    for grp, lo, hi in [("users", 0, nu), ("artists", nu, N)]:
        m = deg[r, lo:hi] > 0
        if m.sum() == 0:
            continue
        d = deg[r, lo:hi][m]; c = c_pooled[lo:hi][m]
        print(f"rel {r} {name:12} {grp:8} n={int(m.sum()):5d} "
              f"mean|N_r|={d.mean():8.1f}  mean c_i={c.mean():8.1f}  "
              f"mean scale={(d/c).mean():.4f}")

print("\nInterpretation for a USER (the node type the friend task scores):")
mu = deg[0, :nu] > 0
print(f"  friend term      scaled by {(deg[0,:nu][mu]/c_pooled[:nu][mu]).mean():.4f}  "
      f"(i.e. {1/(deg[0,:nu][mu]/c_pooled[:nu][mu]).mean():.1f}x WEAKER under pooling)")
mv = deg[2, :nu] > 0
print(f"  listened_by term scaled by {(deg[2,:nu][mv]/c_pooled[:nu][mv]).mean():.4f}  "
      f"(essentially unchanged under pooling)")
