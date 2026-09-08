from PIL import Image
import numpy as np
from collections import deque

p = '/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/ingest/pages/CSE 60745_Fall 2026_HW1/page_002_fig_01.jpeg'
im = Image.open(p).convert('RGB')
a = np.array(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
blue = (B > 110) & (R < 120) & (B - R > 45)
H, W = blue.shape

seen = np.zeros_like(blue, bool)
comps = []
for y in range(H):
    for x in range(W):
        if blue[y, x] and not seen[y, x]:
            q = deque([(y, x)]); seen[y, x] = True; pix = []
            while q:
                cy, cx = q.popleft(); pix.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and blue[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
            if len(pix) > 200:
                arr = np.array(pix)
                comps.append((arr[:, 1].mean(), arr[:, 0].mean(), len(pix)))
print('n nodes found', len(comps))
for c in comps:
    print('cx=%.1f cy=%.1f area=%d' % c)

# darkness mask for lines (black-ish)
gray = a.mean(axis=2)
dark = gray < 170

np.save('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/scratch/dark.npy', dark)
np.save('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/scratch/blue.npy', blue)
import json
json.dump([[c[0], c[1]] for c in comps], open('/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/scratch/nodes.json', 'w'))
