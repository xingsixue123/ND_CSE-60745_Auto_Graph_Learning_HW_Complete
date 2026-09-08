#!/usr/bin/env python3
"""Independent re-derivation of every number claimed in p2/answer.tex.
Deliberately does NOT reuse the worker's code. Uses BFS + dicts only
(no networkx) so a networkx misuse cannot be replicated."""
import collections, json, sys

PATH = "/home/xing/project/auto_hw_complete/input/graph-1.txt"

adj = collections.defaultdict(set)
raw_lines = 0
selfloops = 0
seen_pairs = set()
dups = 0
edges = []
with open(PATH) as f:
    for line in f:
        s = line.strip()
        if not s:
            continue
        raw_lines += 1
        parts = s.split("\t")
        assert len(parts) == 2, (raw_lines, repr(line))
        u, v = int(parts[0]), int(parts[1])
        if u == v:
            selfloops += 1
        key = (min(u, v), max(u, v))
        if key in seen_pairs:
            dups += 1
        seen_pairs.add(key)
        edges.append(key)
        adj[u].add(v)
        adj[v].add(u)

n = len(adj)
m = len(seen_pairs)
print(f"raw lines        : {raw_lines}")
print(f"self-loops       : {selfloops}")
print(f"duplicate edges  : {dups}")
print(f"nodes            : {n}")
print(f"edges (distinct) : {m}")

# --- connected components by iterative BFS ---
seen = set()
comps = []
for start in adj:
    if start in seen:
        continue
    q = collections.deque([start])
    seen.add(start)
    comp = []
    while q:
        x = q.popleft()
        comp.append(x)
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                q.append(y)
    comps.append(comp)

comps.sort(key=len, reverse=True)
print(f"components       : {len(comps)}")
print(f"top-10 sizes     : {[len(c) for c in comps[:10]]}")

def induced_edges(nodes):
    s = set(nodes)
    return sum(1 for a in s for b in adj[a] if b in s) // 2

lcc = comps[0]
cc2 = comps[1]
print(f"LCC  nodes/edges : {len(lcc)} / {induced_edges(lcc)}")
print(f"CC2  nodes/edges : {len(cc2)} / {induced_edges(cc2)}")
sizes = [len(c) for c in comps]
print(f"ties at size {sizes[1]}: {sizes.count(sizes[1])}   ties at size {sizes[2]}: {sizes.count(sizes[2])}")

# --- invariants ---
degsum = sum(len(adj[x]) for x in adj)
assert degsum == 2 * m, (degsum, 2 * m)
assert sum(sizes) == n
assert sum(induced_edges(c) for c in comps) == m
print(f"INVARIANTS OK: degsum {degsum} == 2m {2*m}; sizes sum {sum(sizes)} == n; comp edges sum == m")

# --- degree distribution ---
degs = [len(adj[x]) for x in adj]
hist = collections.Counter(degs)
mn, mx = min(degs), max(degs)
mean = degsum / n
sdegs = sorted(degs)
median = (sdegs[n // 2 - 1] + sdegs[n // 2]) / 2 if n % 2 == 0 else sdegs[n // 2]
print(f"degree min/max/mean/median : {mn} / {mx} / {mean:.6f} / {median}")
print(f"N(1)={hist[1]} ({100*hist[1]/n:.2f}%)  N(2)={hist[2]} ({100*hist[2]/n:.2f}%)")
print(f"frac deg<=2 : {100*(hist[1]+hist[2])/n:.4f}%")
print(f"distinct degree values : {len(hist)}")
maxnode = [x for x in adj if len(adj[x]) == mx]
print(f"max degree node(s) : {maxnode}")
top = sorted(hist)[-8:]
print(f"top degrees and counts : {[(k, hist[k]) for k in top]}")

# --- LCC / cycles / shares ---
print(f"cycles whole graph m-n+c : {m - n + len(comps)}")
print(f"forest edges n-c : {n - len(comps)}")
print(f"LCC share nodes {100*len(lcc)/n:.2f}%  edges {100*induced_edges(lcc)/m:.2f}%")
cc2m = induced_edges(cc2)
print(f"CC2 cycles : {cc2m - len(cc2) + 1}")
cc2hist = collections.Counter(len(adj[x] & set(cc2)) for x in cc2)
print(f"CC2 degree hist : {dict(sorted(cc2hist.items()))}")
print(f"CC2 max degree : {max(len(adj[x]) for x in cc2)}")

# CC2 diameter via BFS from every node
def ecc(src, s):
    d = {src: 0}
    q = collections.deque([src])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in s and y not in d:
                d[y] = d[x] + 1
                q.append(y)
    return max(d.values())

s2 = set(cc2)
print(f"CC2 diameter : {max(ecc(x, s2) for x in cc2)}")
