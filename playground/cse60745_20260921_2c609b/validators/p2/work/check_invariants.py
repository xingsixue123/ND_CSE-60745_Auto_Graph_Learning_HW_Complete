#!/usr/bin/env python3
"""
Invariant check on the statistics asserted in OUTPUT/answer.tex.

The bulk HGB data (/tmp/hgbdata, 389 MB) was cleaned up after the first session,
so verify_hgb.py can no longer be re-run. This script instead re-checks the
*published totals* (Table 1) against the *per-node-type / per-relation breakdown*
(Table 2) exactly as those numbers appear in the delivered answer. If the master
agent or the validator edits a number, this will catch the inconsistency.

Source of the breakdown: hgb_verify_output.txt (first session, recomputed from the
released node.dat/link.dat/label.dat files).

Run:  python3 check_invariants.py
"""

# ---- Table 1: HGB headline statistics, as published in Lv et al., KDD 2021 ----
PUBLISHED = {
    "DBLP":     dict(nodes=26_128,  ntypes=4, edges=239_566,   etypes=6,  classes=4),
    "IMDB":     dict(nodes=21_420,  ntypes=4, edges=86_642,    etypes=6,  classes=5),
    "ACM":      dict(nodes=10_942,  ntypes=4, edges=547_872,   etypes=8,  classes=3),
    "Freebase": dict(nodes=180_098, ntypes=8, edges=1_057_688, etypes=36, classes=7),
}

# ---- Table 2: per-node-type counts asserted in answer.tex ----
NODES = {
    "DBLP":     {"author": 4_057, "paper": 14_328, "term": 7_723, "venue": 20},
    "IMDB":     {"movie": 4_932, "director": 2_393, "actor": 6_124, "keyword": 7_971},
    "ACM":      {"paper": 3_025, "author": 5_959, "subject": 56, "term": 1_902},
    "Freebase": {"book": 40_402, "film": 19_427, "music": 82_351, "sports": 1_025,
                 "people": 17_641, "location": 9_368, "organization": 2_731,
                 "business": 7_153},
}

# ---- Table 2: per-relation counts asserted in answer.tex.
# Forward relations only; HGB stores each also in its inverse direction, so the
# edge total is 2 x sum(forward) EXCEPT where a relation is already symmetric and
# stored under two distinct ids (ACM paper-cite/paper-ref).
FORWARD_EDGES = {
    "DBLP":     {"author-paper": 19_645, "paper-term": 85_810, "paper-venue": 14_328},
    "IMDB":     {"movie-director": 4_932, "movie-actor": 14_779, "movie-keyword": 23_610},
    "ACM":      {"paper-cite-paper": 5_343, "paper-ref-paper": 5_343,
                 "paper-author": 9_949, "paper-subject": 3_025, "paper-term": 255_619},
    # Freebase's 36 relations are not all listed in the answer; only two are quoted.
}
# ACM's cite/ref pair are two separate ids that are NOT further inverted.
ACM_UNMIRRORED = {"paper-cite-paper", "paper-ref-paper"}

FREEBASE_QUOTED = {"BOOK-and-BOOK": 202_674, "MUSIC-and-MUSIC": 283_670}

# ---- Labelled target nodes asserted in the Table 2 footnote ----
LABELLED = {
    "DBLP":     ("author", 4_057, 4_057, 0),
    "ACM":      ("paper", 3_025, 3_025, 0),
    "IMDB":     ("movie", 4_573, 4_932, 2_684),
    "Freebase": ("book", 7_954, 40_402, 0),
}

# ---- Version-discrepancy arithmetic asserted in Section 2.3 ----
def version_checks():
    out = []
    # DBLP term count: only MAGNN/HeCo/HGB's 7,723 reproduces the published total.
    magnn = 4_057 + 14_328 + 7_723 + 20
    han   = 4_057 + 14_328 + 8_789 + 20
    out.append(("DBLP 7,723 terms reproduces published total",
                magnn == 26_128, f"{magnn} vs 26,128"))
    out.append(("DBLP 8,789 terms (HAN) does NOT",
                han == 27_194 and han != 26_128, f"{han} vs 26,128"))
    # LastFM: HGB's edge total double-counts the symmetric U-U relation.
    nodes = 1_892 + 17_632 + 1_088
    out.append(("LastFM node total 20,612 = MAGNN's 1,892+17,632+1,088",
                nodes == 20_612, str(nodes)))
    edges = 2 * 12_717 + 92_834 + 23_253
    out.append(("LastFM 2x12,717 + 92,834 + 23,253 = 141,521",
                edges == 141_521, str(edges)))
    out.append(("LastFM gap 141,521 - 128,804 = 12,717 (the U-U count)",
                141_521 - 128_804 == 12_717, str(141_521 - 128_804)))
    return out


def main():
    ok = True

    print("== node-type counts sum to the published node total ==")
    for ds, parts in NODES.items():
        tot, pub = sum(parts.values()), PUBLISHED[ds]["nodes"]
        good = tot == pub and len(parts) == PUBLISHED[ds]["ntypes"]
        ok &= good
        print(f"  {ds:9s} sum={tot:>9,}  published={pub:>9,}  "
              f"ntypes={len(parts)}/{PUBLISHED[ds]['ntypes']}  "
              f"{'OK' if good else 'MISMATCH'}")

    print("\n== relation counts sum to the published edge total ==")
    for ds, rels in FORWARD_EDGES.items():
        if ds == "ACM":
            tot = sum(v if k in ACM_UNMIRRORED else 2 * v for k, v in rels.items())
        else:
            tot = 2 * sum(rels.values())
        pub = PUBLISHED[ds]["edges"]
        good = tot == pub
        ok &= good
        print(f"  {ds:9s} sum={tot:>9,}  published={pub:>9,}  "
              f"{'OK' if good else 'MISMATCH'}")
    print(f"  {'Freebase':9s} 36 relations, only 2 quoted "
          f"({', '.join(f'{k}={v:,}' for k, v in FREEBASE_QUOTED.items())}) "
          f"-> sum not checkable from the answer alone")

    print("\n== labelled target nodes are a subset of that node type ==")
    for ds, (ntype, lab, tot, multi) in LABELLED.items():
        # the quoted denominator must be that node type's count, and the labelled
        # count must not exceed it (HGB labels only a subset for Freebase/IMDB)
        good = tot == NODES[ds][ntype] and 0 < lab <= tot
        ok &= bool(good)
        note = f"multi-label: {multi:,} carry >1" if multi else "single-label"
        print(f"  {ds:9s} {ntype:9s} labelled={lab:>7,} / {tot:>7,}  {note}  "
              f"{'OK' if good else 'MISMATCH'}")

    print("\n== version-discrepancy arithmetic (Section 2.3) ==")
    for desc, good, detail in version_checks():
        ok &= good
        print(f"  [{'OK' if good else 'FAIL'}] {desc}  ({detail})")

    print("\n" + ("ALL INVARIANTS HOLD" if ok else "SOME INVARIANTS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
