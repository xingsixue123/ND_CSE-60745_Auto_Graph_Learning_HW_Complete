import torch, warnings
warnings.filterwarnings("ignore")
from torch_geometric.datasets import Planetoid, WebKB, WikipediaNetwork, Actor, Coauthor, Amazon, PPI

ROOT = "data"

# claimed: name -> (|V|, |E| distinct unordered incl self-loops, stored entries or None,
#                   d, #cls, h_edge or None)
CLAIM = {
 "Cora":      (2708,   5278,   10556, 1433, 7,  0.81),
 "CiteSeer":  (3327,   4552,   9104,  3703, 6,  0.74),
 "PubMed":    (19717,  44324,  88648, 500,  3,  0.80),
 "Cornell":   (183,    280,    298,   1703, 5,  0.13),
 "Texas":     (183,    295,    325,   1703, 5,  0.11),
 "Wisconsin": (251,    466,    515,   1703, 5,  0.21),
 "Chameleon": (2277,   31421,  36101, 2325, 5,  0.23),
 "Squirrel":  (5201,   198493, 217073,2089, 5,  0.22),
 "Actor":     (7600,   26752,  30019, 932,  5,  0.22),
 "CS":        (18333,  81894,  None,  6805, 15, 0.81),
 "Physics":   (34493,  247962, None,  8415, 5,  0.93),
 "Computers": (13752,  245861, None,  767,  10, 0.78),
 "Photo":     (7650,   119081, None,  745,  8,  0.83),
}

def stats(data):
    ei = data.edge_index
    src, dst = ei[0].tolist(), ei[1].tolist()
    stored = len(src)
    undirected = set()
    selfloops = 0
    for u, v in zip(src, dst):
        if u == v:
            selfloops += 1
        undirected.add((min(u, v), max(u, v)))
    y = data.y
    # h_edge over distinct unordered pairs, self-loops included
    same = sum(1 for (u, v) in undirected if int(y[u]) == int(y[v]))
    h_pairs = same / len(undirected)
    # excluding self-loops
    nosl = [(u, v) for (u, v) in undirected if u != v]
    h_nosl = sum(1 for (u, v) in nosl if int(y[u]) == int(y[v])) / len(nosl)
    # over stored directed entries
    h_dir = sum(1 for u, v in zip(src, dst) if int(y[u]) == int(y[v])) / stored
    return dict(V=data.num_nodes, E=len(undirected), stored=stored, sl=selfloops,
                d=data.num_features, cls=int(y.max()) + 1,
                h=h_pairs, h_nosl=h_nosl, h_dir=h_dir)

loaders = [
 ("Cora",      lambda: Planetoid(ROOT, "Cora")[0]),
 ("CiteSeer",  lambda: Planetoid(ROOT, "CiteSeer")[0]),
 ("PubMed",    lambda: Planetoid(ROOT, "PubMed")[0]),
 ("Cornell",   lambda: WebKB(ROOT, "Cornell")[0]),
 ("Texas",     lambda: WebKB(ROOT, "Texas")[0]),
 ("Wisconsin", lambda: WebKB(ROOT, "Wisconsin")[0]),
 ("Chameleon", lambda: WikipediaNetwork(ROOT, "chameleon", geom_gcn_preprocess=True)[0]),
 ("Squirrel",  lambda: WikipediaNetwork(ROOT, "squirrel", geom_gcn_preprocess=True)[0]),
 ("Actor",     lambda: Actor(ROOT + "/actor")[0]),
 ("CS",        lambda: Coauthor(ROOT, "CS")[0]),
 ("Physics",   lambda: Coauthor(ROOT, "Physics")[0]),
 ("Computers", lambda: Amazon(ROOT, "Computers")[0]),
 ("Photo",     lambda: Amazon(ROOT, "Photo")[0]),
]

print(f"{'dataset':<11}{'|V|':>9}{'|E|':>10}{'stored':>10}{'sl':>5}{'d':>7}{'c':>4}"
      f"{'h':>7}{'h-nosl':>8}{'h-dir':>7}   verdict")
for name, fn in loaders:
    try:
        d = fn()
    except Exception as e:
        print(f"{name:<11} LOAD FAILED: {type(e).__name__} {e}")
        continue
    s = stats(d)
    cV, cE, cSt, cd, cc, ch = CLAIM[name]
    bad = []
    if s["V"] != cV: bad.append(f"V {s['V']}!={cV}")
    if s["E"] != cE: bad.append(f"E {s['E']}!={cE}")
    if cSt is not None and s["stored"] != cSt: bad.append(f"stored {s['stored']}!={cSt}")
    if s["d"] != cd: bad.append(f"d {s['d']}!={cd}")
    if s["cls"] != cc: bad.append(f"cls {s['cls']}!={cc}")
    if ch is not None and abs(round(s["h"], 2) - ch) > 0.005:
        bad.append(f"h {s['h']:.3f}!={ch}")
    print(f"{name:<11}{s['V']:>9}{s['E']:>10}{s['stored']:>10}{s['sl']:>5}{s['d']:>7}"
          f"{s['cls']:>4}{s['h']:>7.3f}{s['h_nosl']:>8.3f}{s['h_dir']:>7.3f}   "
          + ("OK" if not bad else "MISMATCH: " + "; ".join(bad)))

# PPI: claimed 56,944 nodes / 793,632 edges / 50 feat / 121 classes, 20/2/2 split
try:
    tr = PPI(ROOT + "/ppi", split="train")
    va = PPI(ROOT + "/ppi", split="val")
    te = PPI(ROOT + "/ppi", split="test")
    n = sum(g.num_nodes for s in (tr, va, te) for g in s)
    stored = sum(g.edge_index.size(1) for s in (tr, va, te) for g in s)
    und = 0
    sl = 0
    for s in (tr, va, te):
        for g in s:
            ei = g.edge_index
            pairs = set()
            for u, v in zip(ei[0].tolist(), ei[1].tolist()):
                if u == v: sl += 1
                pairs.add((min(u, v), max(u, v)))
            und += len(pairs)
    print(f"\nPPI graphs: train={len(tr)} val={len(va)} test={len(te)} (claim 20/2/2)")
    print(f"PPI nodes={n} (claim 56,944)  stored_entries={stored}  "
          f"distinct_undirected={und} (claim 793,632)  self_loops={sl}")
    print(f"PPI feat={tr[0].num_features} (claim 50)  labels={tr[0].y.size(1)} (claim 121)")
except Exception as e:
    print("PPI FAILED:", type(e).__name__, e)
