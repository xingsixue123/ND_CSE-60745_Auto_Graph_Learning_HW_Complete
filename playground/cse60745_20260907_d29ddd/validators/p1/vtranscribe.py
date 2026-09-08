"""Independent validator transcription of page_002_fig_01.jpeg.
Deliberately does NOT read the master's or worker's edge list."""
import numpy as np
from PIL import Image
from collections import deque

FIG = "/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_002_fig_01.jpeg"
im = Image.open(FIG).convert("RGB")
A = np.asarray(im).astype(int)
H, W, _ = A.shape
print("image", W, "x", H)

R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]
# matplotlib C0 = (31,119,180)
blue = (B > R + 40) & (B > 80) & (R < 150)
print("blue px", blue.sum())

# connected components of blue
lab = -np.ones((H, W), int)
comps = []
for y in range(H):
    for x in range(W):
        if blue[y, x] and lab[y, x] < 0:
            q = deque([(y, x)]); lab[y, x] = len(comps); pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx_ = cy+dy, cx+dx
                    if 0 <= ny < H and 0 <= nx_ < W and blue[ny, nx_] and lab[ny, nx_] < 0:
                        lab[ny, nx_] = len(comps); q.append((ny, nx_))
            comps.append(pts)
comps = [c for c in comps if len(c) > 200]
print("blue blobs (>200px):", len(comps), "areas:", sorted(len(c) for c in comps))

cent = []
for c in comps:
    ys = np.array([p[0] for p in c]); xs = np.array([p[1] for p in c])
    cent.append((xs.mean(), ys.mean(), np.sqrt(len(c)/np.pi)))
cent.sort(key=lambda t: (t[1], t[0]))
for i, (x, y, r) in enumerate(cent):
    print(f"blob{i}: x={x:.1f} y={y:.1f} r={r:.1f}")

# ---- ink mask: dark (edges + digits), and disc mask
dark = (R < 130) & (G < 130) & (B < 130)
disc = np.zeros((H, W), bool)
YY, XX = np.mgrid[0:H, 0:W]
for (x, y, r) in cent:
    disc |= ((XX-x)**2 + (YY-y)**2) <= (r+3.0)**2
ink = dark & ~disc  # black line ink outside discs
print("ink px outside discs", ink.sum())

def ink_near(px, py, rad=2.5):
    x0, x1 = int(px-rad), int(px+rad)+1
    y0, y1 = int(py-rad), int(py+rad)+1
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
        return False
    return ink[y0:y1, x0:x1].any()

# ---- test all 45 pairs
N = len(cent)
res = []
for i in range(N):
    for j in range(i+1, N):
        xi, yi, ri = cent[i]; xj, yj, rj = cent[j]
        L = np.hypot(xj-xi, yj-yi)
        n = int(L*2)
        hit = tot = 0
        for k in range(n+1):
            t = k/n
            px, py = xi+(xj-xi)*t, yi+(yj-yi)*t
            # skip if inside ANY disc
            inside = False
            for (cx, cy, cr) in cent:
                if (px-cx)**2 + (py-cy)**2 <= (cr+4.0)**2:
                    inside = True; break
            if inside:
                continue
            tot += 1
            if ink_near(px, py):
                hit += 1
        res.append((hit/max(tot,1), i, j, tot))
res.sort(reverse=True)
print("\n--- pairwise straight-segment ink coverage (top 22) ---")
for cov, i, j, tot in res[:22]:
    print(f"blob{i}-blob{j}: cov={cov:.3f}  samples={tot}")
np.save("/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/validators/p1/cent.npy", np.array(cent))
