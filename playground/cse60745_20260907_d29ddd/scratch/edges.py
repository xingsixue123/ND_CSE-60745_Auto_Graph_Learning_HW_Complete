import numpy as np, itertools
dark = np.load('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/scratch/dark.npy')
blue = np.load('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/scratch/blue.npy')
H, W = dark.shape
nodes = {
    0: (78.5, 43.7), 8: (290.4, 91.7), 4: (210.3, 121.4), 6: (372.2, 196.8),
    5: (74.9, 213.2), 1: (194.4, 260.6), 3: (340.2, 322.8), 9: (244.4, 369.4),
    7: (96.5, 483.1), 2: (234.7, 530.7),
}
R = 18.0  # node radius approx


def hit(x, y, rad=1):
    xi, yi = int(round(x)), int(round(y))
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            ny, nx = yi + dy, xi + dx
            if 0 <= ny < H and 0 <= nx < W and (dark[ny, nx] or blue[ny, nx]):
                return True
    return False


res = []
for u, v in itertools.combinations(sorted(nodes), 2):
    x1, y1 = nodes[u]; x2, y2 = nodes[v]
    L = np.hypot(x2 - x1, y2 - y1)
    ts = np.linspace(R / L, 1 - R / L, 200)
    ok = sum(hit(x1 + t * (x2 - x1), y1 + t * (y2 - y1)) for t in ts)
    frac = ok / len(ts)
    res.append((frac, u, v))
res.sort(reverse=True)
for f, u, v in res:
    print('%.3f  (%d,%d)' % (f, u, v))
