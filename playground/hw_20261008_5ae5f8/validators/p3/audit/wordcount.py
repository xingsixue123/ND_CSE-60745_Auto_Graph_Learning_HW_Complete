#!/usr/bin/env python3
"""Count prose words per \section* block in a LaTeX fragment, R8 check.

Strips: comments, the whole tikzpicture env, math, LaTeX control words,
and braces. Counts a 'word' as a run of letters/digits/'-' with a letter in it.
"""
import re, sys

TARGETS = {"3.3": 190, "3.4": 190, "3.5": 190, "3.6": 190, "3.7": 290, "3.8": 330}

src = open(sys.argv[1]).read()
src = re.sub(r'(?<!\\)%.*', '', src)                      # comments
src = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', ' ',
             src, flags=re.S)                             # the figure
blocks, cur, name = [], [], None
for line in src.splitlines():
    m = re.match(r'\s*\\section\*\{Ex\.\\?\s*(\d+\.\d+)', line)
    if m:
        if name: blocks.append((name, "\n".join(cur)))
        name, cur = m.group(1), []
    elif name is not None:
        cur.append(line)
if name: blocks.append((name, "\n".join(cur)))

def words(t):
    t = re.sub(r'\$[^$]*\$', ' X ', t)                    # inline math -> 1 token
    t = re.sub(r'\\[a-zA-Z@]+\*?', ' ', t)                # control words
    t = re.sub(r'\\[^a-zA-Z]', ' ', t)                    # control symbols
    t = re.sub(r'[{}\[\]&~^_]', ' ', t)
    t = t.replace('---', ' ').replace('--', ' ')
    return [w for w in re.findall(r"[A-Za-z0-9'\-]+", t) if re.search('[A-Za-z]', w)]

tot = ttot = 0
print(f"{'ex':>5} {'words':>6} {'target':>7} {'ratio':>6}  verdict")
for n, body in blocks:
    w = len(words(body)); t = TARGETS[n]
    tot += w; ttot += t
    r = w / t
    v = "OK" if r <= 1.25 else "OVER 1.25x -> DEFECT"
    print(f"{n:>5} {w:>6} {t:>7} {r:>5.2f}x  {v}")
print(f"{'TOT':>5} {tot:>6} {ttot:>7} {tot/ttot:>5.2f}x  "
      f"{'OK' if tot/ttot <= 1.25 else 'OVER'}")
em = src.count('---')
print(f"\nem-dashes: {em}  -> one per {tot/max(em,1):.0f} words "
      f"(R8 flags denser than 1 per 70)")
