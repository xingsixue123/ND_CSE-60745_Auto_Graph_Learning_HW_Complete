#!/usr/bin/env python3
"""Re-derive the HGB/HNE PubMed network schema drawn in Figure 3 of answer.tex.

Source of truth: hgb_info/PubMed.info.dat -- the verbatim `info.dat` that ships
inside HNE's PubMed.zip.  HGB's PubMed is HNE's PubMed; HGB's own PubMed_ini.zip
ships node.dat/link.dat but no info.dat, so the *names* come from HNE while the
*counts* were confirmed against HGB's link.dat (see downloads.md).

Checks the three claims the figure and its caption make:
  1. exactly 4 node types, named GENE/DISEASE/CHEMICAL/SPECIES;
  2. exactly 10 relation types, whose edge counts sum to 244,986;
  3. the schema is COMPLETE in the undirected sense -- every one of the
     C(4,2)=6 unordered type pairs carries exactly one relation, and every one
     of the 4 types carries exactly one self-relation, 6+4=10.
  4. the link-prediction target is DISEASE-and-DISEASE, a self-relation.

Run:  python3 verify_pubmed_schema.py
"""
import itertools
import pathlib
import re
import sys

INFO = pathlib.Path(__file__).with_name("hgb_info") / "PubMed.info.dat"

# Per-relation edge counts recovered from HGB's link.dat by the research pass.
# Only their SUM is asserted against the published total 244,986; the schema
# shape below is derived purely from info.dat.
EDGE_COUNTS = {
    0: 16_105, 1: 25_962, 2: 42_637, 3: 31_277, 4: 51_323,
    5: 62_187, 6: 6_297, 7: 3_155, 8: 5_245, 9: 798,
}
PUBLISHED_TOTAL = 244_986
PUBLISHED_NODES = 63_109
NODE_COUNTS = {"GENE": 13_561, "DISEASE": 20_163, "CHEMICAL": 26_522, "SPECIES": 2_863}


def parse(text):
    """Return (node types, link types, target link type) from info.dat."""
    ntypes = {}
    for m in re.finditer(r"^(\d+)\s+([A-Z]+)\s*$", text, re.M):
        ntypes[int(m.group(1))] = m.group(2)

    links = {}
    for m in re.finditer(r"^(\d+)\s+(\d+)\s+(\d+)\s+([A-Za-z-]+)\s*$", text, re.M):
        links[int(m.group(1))] = (int(m.group(2)), int(m.group(3)), m.group(4))

    tgt = re.search(r"Targeting:\s*Link Type\s*\((\d+),(\d+),(\d+)\)", text)
    return ntypes, links, tuple(int(g) for g in tgt.groups()) if tgt else None


def main():
    if not INFO.exists():
        print(f"MISSING SOURCE: {INFO}", file=sys.stderr)
        return 2
    text = INFO.read_bytes().decode("utf-8", "replace")
    ntypes, links, target = parse(text)
    ok = True

    def check(desc, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        print(f"  [{'OK' if good else 'FAIL'}] {desc}" + (f"  ({detail})" if detail else ""))

    print("== HGB/HNE PubMed schema, re-derived from hgb_info/PubMed.info.dat ==")

    expected_names = {0: "GENE", 1: "DISEASE", 2: "CHEMICAL", 3: "SPECIES"}
    check("4 node types, named as drawn", ntypes == expected_names, str(ntypes))
    check(f"node counts sum to {PUBLISHED_NODES:,}",
          sum(NODE_COUNTS.values()) == PUBLISHED_NODES,
          " + ".join(f"{v:,}" for v in NODE_COUNTS.values()))

    check("10 relation types", len(links) == 10, f"got {len(links)}")
    check(f"edge counts sum to published total {PUBLISHED_TOTAL:,}",
          sum(EDGE_COUNTS.values()) == PUBLISHED_TOTAL,
          f"got {sum(EDGE_COUNTS.values()):,}")

    # --- the completeness invariant the caption asserts ---
    pairs = [frozenset((s, e)) for s, e, _ in links.values()]
    selfrel = [p for p in pairs if len(p) == 1]
    cross = [p for p in pairs if len(p) == 2]
    all_cross = {frozenset(c) for c in itertools.combinations(range(4), 2)}

    check("no relation is drawn twice (each unordered pair appears once)",
          len(set(pairs)) == len(pairs), f"{len(set(pairs))} distinct of {len(pairs)}")
    check("all C(4,2)=6 unordered type pairs are realised",
          set(cross) == all_cross, f"{len(set(cross))} of 6")
    check("all 4 types carry a self-relation",
          len(set(selfrel)) == 4, f"{len(set(selfrel))} of 4")
    check("schema is COMPLETE: 6 pairwise + 4 self = 10",
          len(set(cross)) + len(set(selfrel)) == 10 == len(links),
          f"{len(set(cross))} + {len(set(selfrel))} = {len(set(cross)) + len(set(selfrel))}")

    # --- LP target ---
    tgt_start, tgt_end, tgt_type = target
    meaning = links[tgt_type][2]
    check("LP target is DISEASE-and-DISEASE, a self-relation on the labelled type",
          (tgt_start, tgt_end) == (1, 1) and meaning == "DISEASE-and-DISEASE"
          and ntypes[tgt_start] == "DISEASE",
          f"Targeting Link Type ({tgt_start},{tgt_end},{tgt_type}) = {meaning}")

    print("\n-- relation list as drawn --")
    for i in sorted(links):
        s, e, m = links[i]
        print(f"   {i}: {ntypes[s]:8s} -- {ntypes[e]:8s}  {m:26s} {EDGE_COUNTS[i]:>7,}")

    print("\n" + ("ALL INVARIANTS HOLD" if ok else "SOME INVARIANTS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
