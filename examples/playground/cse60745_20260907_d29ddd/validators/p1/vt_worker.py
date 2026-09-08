"""Programmatic transcription of the HW figure into a graph.

Channel: page_002_fig_01.jpeg at native resolution (428x588).

Method
------
1. Segment the blue node discs by colour, label connected components, take
   centroids and radii.
2. Build an "ink" mask of the dark line strokes (dark, non-blue pixels).
3. For every unordered pair (u,v), sample densely along the straight segment
   u->v, skipping any sample that falls inside ANY node disc, and ask what
   fraction of the remaining samples has ink within a small tolerance.
   A true edge covers ~100%.
4. The pair test alone cannot distinguish "5-4 and 4-8" from a single edge
   "5-8" drawn through node 4's disc.  So we additionally measure, at each
   node, the angular directions in which strokes depart the node, on rings of
   several radii.  A departure whose angle is CONSTANT in r points at a true
   neighbour; an angle that DRIFTS with r belongs to a chord that passes near
   but not through the centre.
"""
import numpy as np
from PIL import Image

FIG = ('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/'
       'ingest/pages/CSE 60745_Fall 2026_HW1/page_002_fig_01.jpeg')

a = np.asarray(Image.open(FIG).convert('RGB')).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# ---------- 1. node discs -------------------------------------------------
blue = (B - R > 40) & (B > 100)
lab = np.zeros((H, W), int)
cur = 0
comps = []
for y in range(H):
    for x in range(W):
        if blue[y, x] and lab[y, x] == 0:
            cur += 1
            stack, pix = [(y, x)], []
            lab[y, x] = cur
            while stack:
                cy, cx = stack.pop()
                pix.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and blue[ny, nx] and lab[ny, nx] == 0:
                            lab[ny, nx] = cur
                            stack.append((ny, nx))
            if len(pix) > 200:
                comps.append(np.array(pix))

nodes = []
for pix in comps:
    cy, cx = pix[:, 0].mean(), pix[:, 1].mean()
    rad = np.sqrt(len(pix) / np.pi)          # equal-area radius
    nodes.append((cx, cy, rad, len(pix)))
nodes.sort(key=lambda t: (t[1], t[0]))
print(f'# blue discs found: {len(nodes)}')
for i, (cx, cy, rad, n) in enumerate(nodes):
    print(f'  disc{i}: centre=({cx:7.2f},{cy:7.2f})  r_eq={rad:5.2f}  area={n}')

cxs = np.array([n[0] for n in nodes])
cys = np.array([n[1] for n in nodes])
# node disc radius including the dark label glyph inside: use a fixed generous
# radius derived from the equal-area radius of the discs
RAD = float(np.median([n[2] for n in nodes]))
print(f'\nmedian disc radius = {RAD:.2f} px')

# ---------- 2. ink mask ---------------------------------------------------
gray = a.mean(axis=2)
ink = (gray < 170) & (~blue)
print(f'ink pixels: {ink.sum()}')

# distance-to-ink via a small dilation stack (tolerance for antialiasing)
def dilate(m, k):
    out = m.copy()
    for _ in range(k):
        o = out.copy()
        o[1:, :] |= out[:-1, :]
        o[:-1, :] |= out[1:, :]
        o[:, 1:] |= out[:, :-1]
        o[:, :-1] |= out[:, 1:]
        out = o
    return out

ink_d = dilate(ink, 2)          # ~2px tolerance

inside_any = None
def inside_disc_mask(x, y, margin=3.0):
    d = np.hypot(x[:, None] - cxs[None, :], y[:, None] - cys[None, :])
    return (d < RAD + margin).any(axis=1)

# ---------- 3. pairwise straight-segment ink coverage --------------------
N = len(nodes)
print('\n# pairwise segment ink coverage (skipping samples inside any disc)')
cov = {}
for i in range(N):
    for j in range(i + 1, N):
        x0, y0 = cxs[i], cys[i]
        x1, y1 = cxs[j], cys[j]
        L = int(np.hypot(x1 - x0, y1 - y0) * 2)
        t = np.linspace(0, 1, max(L, 30))
        xs, ys = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
        keep = ~inside_disc_mask(xs, ys)
        if keep.sum() < 8:
            continue
        xi = np.clip(np.round(xs[keep]).astype(int), 0, W - 1)
        yi = np.clip(np.round(ys[keep]).astype(int), 0, H - 1)
        c = ink_d[yi, xi].mean()
        cov[(i, j)] = c

for (i, j), c in sorted(cov.items(), key=lambda kv: -kv[1]):
    if c > 0.55:
        print(f'  {i:2d}-{j:2d}  coverage={c:.3f}')

# ---------- 4. departure-angle analysis at each node ---------------------
print('\n# departure angles at each node, per ring radius')
rings = [24, 32, 42, 55]

def departures(i, r):
    """angles (deg) of ink arcs on a circle of radius r about node i"""
    th = np.linspace(0, 2 * np.pi, 1440, endpoint=False)
    xs = cxs[i] + r * np.cos(th)
    ys = cys[i] + r * np.sin(th)
    ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
    hit = np.zeros(len(th), bool)
    xi = np.clip(np.round(xs).astype(int), 0, W - 1)
    yi = np.clip(np.round(ys).astype(int), 0, H - 1)
    hit[ok] = ink[yi[ok], xi[ok]]
    # suppress arc positions that lie inside a *different* node's disc
    other = inside_disc_mask(xs, ys, margin=1.0)
    for k in range(len(th)):
        if other[k]:
            d_self = r
            # if it is our own disc it can't be (r > RAD); so it's another node
            hit[k] = False
    # group contiguous runs (circularly)
    idx = np.where(hit)[0]
    if len(idx) == 0:
        return []
    runs, start, prev = [], idx[0], idx[0]
    for k in idx[1:]:
        if k - prev > 3:
            runs.append((start, prev))
            start = k
        prev = k
    runs.append((start, prev))
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][1] == len(th) - 1:
        runs[0] = (runs[-1][0] - len(th), runs[0][1])
        runs.pop()
    out = []
    for s, e in runs:
        mid = ((s + e) / 2) % len(th)
        out.append(np.degrees(th[int(round(mid)) % len(th)]))
    return sorted(out)

ang = {}
for i in range(N):
    ang[i] = {r: departures(i, r) for r in rings}

def bearing(i, j):
    return np.degrees(np.arctan2(cys[j] - cys[i], cxs[j] - cxs[i])) % 360

pass

for i in range(N):
    print(f'\n node disc{i} at ({cxs[i]:.1f},{cys[i]:.1f})')
    for r in rings:
        s = '  '.join(f'{v:6.1f}' for v in ang[i][r])
        print(f'   r={r:3d}: {s}')
    bs = sorted(((bearing(i, j), j) for j in range(N) if j != i))
    print('   bearings to other discs: ' +
          '  '.join(f'{j}@{b:.1f}' for b, j in bs))
