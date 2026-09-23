#!/usr/bin/env python3
"""
Independently recompute the per-node-type and per-relation counts of the four HGB
node-classification datasets from the official HGB data release.

Why this script exists: the HGB paper (Lv et al., KDD 2021) publishes only TOTALS
(#nodes, #node types, #edges, #edge types) in its Table 2 -- it never prints a
per-type breakdown. The breakdown is wanted for the homework's statistics table, so
it has to be derived from the released data files and then checked against the
published totals. If the derived per-type counts sum to the published totals, the
derivation is confirmed.

Data layout (HGB release), tab-separated:
  node.dat   : node_id \t node_name \t node_type \t [attributes]
  link.dat   : src \t dst \t link_type \t weight
  label.dat  : node_id \t node_name \t node_type \t label(s)   (comma-sep if multi-label)
  label.dat.test : same, held-out test split

Run:  python3 verify_hgb.py /tmp/hgbdata
"""
import sys
import os
import json
from collections import Counter, defaultdict

# Published HGB Table 2 totals, transcribed from arXiv:2112.14936.
# These are the numbers the derivation must reproduce.
PUBLISHED = {
    "DBLP":     dict(nodes=26128,  node_types=4, edges=239566,  edge_types=6, target="author", classes=4),
    "IMDB":     dict(nodes=21420,  node_types=4, edges=86642,   edge_types=6, target="movie",  classes=5),
    "ACM":      dict(nodes=10942,  node_types=4, edges=547872,  edge_types=8, target="paper",  classes=3),
    "Freebase": dict(nodes=180098, node_types=8, edges=1057688, edge_types=36, target="BOOK",  classes=7),
}

TYPE_NAMES = {
    "DBLP":     {0: "author", 1: "paper", 2: "term", 3: "venue"},
    "IMDB":     {0: "movie", 1: "director", 2: "actor", 3: "keyword"},
    "ACM":      {0: "paper", 1: "author", 2: "subject", 3: "term"},
    "Freebase": {0: "BOOK", 1: "FILM", 2: "MUSIC", 3: "SPORTS",
                 4: "PEOPLE", 5: "LOCATION", 6: "ORGANIZATION", 7: "BUSINESS"},
}

SUBDIR = {"DBLP": "dblp/DBLP", "IMDB": "imdb/IMDB",
          "ACM": "acm/ACM", "Freebase": "freebase/Freebase"}


def count_nodes(path):
    """Return (per-type node counts, per-type feature dimension)."""
    per_type = Counter()
    featdim = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            ntype = int(parts[2])
            per_type[ntype] += 1
            # 4th column, when present and non-empty, is the comma-separated attribute vector
            if ntype not in featdim:
                if len(parts) > 3 and parts[3].strip():
                    featdim[ntype] = len(parts[3].split(","))
                else:
                    featdim[ntype] = 0
    return per_type, featdim


def count_links(path):
    per_type = Counter()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            per_type[int(parts[2])] += 1
    return per_type


def count_labels(paths):
    """Return (#labelled nodes, #distinct classes, #nodes carrying >1 label, per-split sizes)."""
    classes = set()
    n_labelled = 0
    n_multi = 0
    split_sizes = {}
    for tag, path in paths:
        if not os.path.exists(path):
            split_sizes[tag] = None
            continue
        n_here = 0
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    continue
                parts = line.split("\t")
                labs = [x for x in parts[3].split(",") if x != ""]
                classes.update(labs)
                n_here += 1
                n_labelled += 1
                if len(labs) > 1:
                    n_multi += 1
        split_sizes[tag] = n_here
    return n_labelled, len(classes), n_multi, split_sizes


def link_meaning(root, name):
    """Pull the human-readable relation names out of info.dat (JSON for 3 of the 4)."""
    info = os.path.join(root, "info.dat")
    if not os.path.exists(info):
        return {}
    raw = open(info, encoding="utf-8").read()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        # Freebase ships info.dat as plain text, not JSON
        out = {}
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) == 4 and parts[0].isdigit() and "-" in parts[3]:
                out[int(parts[0])] = parts[3]
        return out
    lt = obj.get("link.dat", {}).get("link type", {})
    return {int(k): v.get("meaning", "?") for k, v in lt.items()}


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "/tmp/hgbdata"
    all_ok = True

    for ds in ("DBLP", "IMDB", "ACM", "Freebase"):
        root = os.path.join(base, SUBDIR[ds])
        if not os.path.isdir(root):
            print(f"!! {ds}: directory not found at {root} -- SKIPPED")
            all_ok = False
            continue

        nodes, featdim = count_nodes(os.path.join(root, "node.dat"))
        links = count_links(os.path.join(root, "link.dat"))
        meanings = link_meaning(root, ds)
        n_lab, n_cls, n_multi, splits = count_labels([
            ("train+val", os.path.join(root, "label.dat")),
            ("test", os.path.join(root, "label.dat.test")),
        ])

        pub = PUBLISHED[ds]
        tot_n, tot_e = sum(nodes.values()), sum(links.values())
        ok_n = tot_n == pub["nodes"]
        ok_e = tot_e == pub["edges"]
        ok_nt = len(nodes) == pub["node_types"]
        ok_et = len(links) == pub["edge_types"]
        ok_c = n_cls == pub["classes"]
        all_ok &= ok_n and ok_e and ok_nt and ok_et and ok_c

        print("=" * 68)
        print(f"{ds}")
        print("=" * 68)
        print("  node types:")
        for t in sorted(nodes):
            print(f"    {t} {TYPE_NAMES[ds].get(t,'?'):<14} {nodes[t]:>10,}   feat_dim={featdim.get(t,0)}")
        print(f"    {'TOTAL':<17} {tot_n:>10,}   published={pub['nodes']:,}  "
              f"{'MATCH' if ok_n else 'MISMATCH'}")
        print("  relation types:")
        for t in sorted(links):
            print(f"    {t:>2} {meanings.get(t,'?'):<26} {links[t]:>10,}")
        print(f"    {'TOTAL':<29} {tot_e:>10,}   published={pub['edges']:,}  "
              f"{'MATCH' if ok_e else 'MISMATCH'}")
        print(f"  #node types = {len(nodes)} (published {pub['node_types']}) "
              f"{'MATCH' if ok_nt else 'MISMATCH'}")
        print(f"  #edge types = {len(links)} (published {pub['edge_types']}) "
              f"{'MATCH' if ok_et else 'MISMATCH'}")
        print(f"  labels: target={pub['target']}  labelled_nodes={n_lab:,}  "
              f"distinct_classes={n_cls} (published {pub['classes']}) "
              f"{'MATCH' if ok_c else 'MISMATCH'}")
        print(f"          nodes with >1 label = {n_multi:,} "
              f"-> {'MULTI-LABEL' if n_multi > 0 else 'single-label'}")
        print(f"          split sizes: {splits}")
        if splits.get("train+val") and splits.get("test"):
            tr, te = splits["train+val"], splits["test"]
            print(f"          train+val fraction = {tr/(tr+te):.4f} (HGB states 24%+6% = 30%)")
        print()

    print("=" * 68)
    print("ALL PUBLISHED TOTALS REPRODUCED" if all_ok else "SOME CHECKS FAILED")
    print("=" * 68)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
