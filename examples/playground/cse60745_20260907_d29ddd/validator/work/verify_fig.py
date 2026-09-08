import numpy as np, itertools, math, sys
from PIL import Image
from collections import deque
D='/home/xing/project/auto_hw_complete/playground/cse60745_20260907_d29ddd/validator/work/'

def blobs(path):
    im = Image.open(path).convert('RGB'); a=np.asarray(im).astype(int)
    R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]
    blue=(B>110)&(B-R>35)&(B-G>20)
    orange=(R>150)&(R-B>60)
    nodemask=blue|orange
    gray=a.mean(axis=2)
    dark=(gray<175)&(~nodemask)
    H,W=dark.shape
    seen=np.zeros_like(nodemask,bool); out=[]
    for y in range(H):
        for x in range(W):
            if nodemask[y,x] and not seen[y,x]:
                q=deque([(y,x)]); seen[y,x]=True; n=0; sx=0; sy=0
                while q:
                    cy,cx=q.popleft(); n+=1; sx+=cx; sy+=cy
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<H and 0<=nx<W and nodemask[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx]=True; q.append((ny,nx))
                if n>2000: out.append((sx/n, sy/n, (n/math.pi)**0.5))
    return out, dark, nodemask, W, H

def degree_scan(cx,cy,r,dark,W,H,pad):
    """count contiguous dark arcs on a circle of radius r+pad -> node degree"""
    rr=r+pad; N=2000; vals=[]
    for i in range(N):
        th=2*math.pi*i/N
        x=int(round(cx+rr*math.cos(th))); y=int(round(cy+rr*math.sin(th)))
        v=False
        if 0<=x<W and 0<=y<H:
            v=dark[max(0,y-1):y+2, max(0,x-1):x+2].any()
        vals.append(v)
    runs=0
    for i in range(N):
        if vals[i] and not vals[i-1]: runs+=1
    if all(vals): runs=0
    return runs

for name, expect in [('fig_p1_q1_graph', {'0':3,'1':3,'2':3,'3':3,'4':3,'5':3,'6':3,'7':3,'8':3,'9':3}),
                     ('fig_p1_q2_graph', None)]:
    cents,dark,nm,W,H = blobs(D+name+'.png')
    print('==',name,' node blobs:',len(cents))
    # normalize coords to 0..1 for identification
    for cx,cy,r in sorted(cents,key=lambda c:c[1]):
        degs=[degree_scan(cx,cy,r,dark,W,H,p) for p in (5,9,14,20)]
        print('  x=%.3f y=%.3f r=%.0f  degree@pads%s'%(cx/W, cy/H, r, degs))
