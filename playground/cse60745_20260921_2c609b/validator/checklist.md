# Master validator checklist — job cse60745_20260921_2c609b

## Round 1 — 2026-09-21

Verdict: **FAIL** (no blocking defects; one major presentation defect)

### What I checked and how

**Assignment re-derived independently.** I did not trust `problems.json`. I re-converted
`input/CSE 60745_Fall 2026_HW2-Part(A).doc` myself with LibreOffice into
`validator/recheck/` and got 3 pages, matching ingest. I read all three ingest channels
(`page_00N.txt`, `page_00N.png`, `manifest.json` — which reports `figures: []` on every
page; the one embedded image per page is the ND header logo, not question content).

Questions found by my own enumeration: **Problem 1 (35 pts)** rendered page 2,
**Problem 2 (35 pts)** rendered page 3. Nothing else. Both answered. 35+35 = 70 = the
stated total, so the points cross-check closes.

*Resolved the "Page 1 of 4" footer scare.* The footer on rendered pages 2–3 reads
"Page N **of 4**" while only 3 pages render. I scanned the raw `.doc` bytes for
`Problem\s*\d` and `(\d+ pts)` in both latin-1 and utf-16-le: only `Problem 1`,
`Problem 2`, `(35 pts)` occur. There is no hidden Problem 3. The "of 4" is a stale Word
NUMPAGES/template field. The master reached the same conclusion in `uncovered` and it is
correct.

**Sub-part coverage.** Each problem's Note demands three things (benchmarks + drawn
schema; baselines + original-paper reference + description; evaluation metrics). All
three present in both answers: P1 §1/§2/§3/§4, P2 §2/§3/§4/§5.

**Correctness — recomputed, not trusted.** P1 claims "Statistics in Table 1 were obtained
by loading each graph and counting". I built a venv with torch/torch_geometric/scipy and
recomputed all 13 rows (`validator/verify_stats.py`). **Every single value matches** —
|V|, distinct-undirected |E|, stored-entry count, feature dim, class count, and h_edge:

    Cora 2708/5278/10556/1433/7/0.810   CiteSeer 3327/4552/9104/3703/6/0.736
    PubMed 19717/44324/88648/500/3/0.802  Cornell 183/280/298/0.132
    Texas 183/295/325/0.112  Wisconsin 251/466/515/0.206
    Chameleon 2277/31421/36101/0.231  Squirrel 5201/198493/217073/0.223
    Actor 7600/26752/30019/0.219  CS 18333/81894/0.808  Physics 34493/247962/0.931
    Computers 13752/245861/0.777  Photo 7650/119081/0.827

Footnote 2's *alternative* conventions also reproduce exactly: Cornell 0.123 excl.
self-loops / 0.131 directed; Texas 0.06 excl.; Wisconsin 0.18 excl.; Chameleon 0.235
directed. Self-loop counts (Texas 16, Wisconsin 16, Actor 93, Squirrel 140) all confirmed.
The Cornell-vs-Zhu-et-al. 0.13/0.30 disagreement is real and honestly flagged rather than
papered over. PPI: 56,944 nodes / 793,632 distinct undirected edges / 50 feat / 121 labels
/ 20-2-2 split — all confirmed (793,632 is correct; the commonly quoted 818,716 is a
different count). OGB Table 2 figures match published OGB values.

**Correctness — P2 arithmetic.** Table 5 claims to be recomputed from HGB's released
files. Every per-type breakdown reconciles to Table 4's published totals, including the
non-obvious ACM case where cite/ref are each other's inverse
(5,343+5,343+2×(9,949+3,025+255,619) = 547,872 exactly). DBLP 2×119,783 = 239,566;
IMDB 2×43,321 = 86,642; Freebase 8 type counts sum to 180,098; C(8,2)+8 = 36;
LastFM 2×12,717+92,834+23,253 = 141,521; ogbn-mag 21,111,007; MAG240M 244,160,499;
Reddit avg degree 492.0. All exact.

**Citations** spot-checked across ~55 baselines (venue + year + author lists): no errors
found. The GAT "commonly miscited as 2017" note and the metapath2vec 9,323,739 erratum
are both correct.

**PDF, both channels.** Rebuilt from `final/` in `validator/build/`: compiles clean, 28
pages, zero undefined references, zero multiply-defined labels, 3 overfull hboxes all
≤5.2pt (~2mm, inside tables), 0 underfull. Programmatic margin scan: the only blocks
outside the text box are the fancyhdr header and footer (by design); no body content
overflows. All labels namespaced `p1:`/`p2:`. Figures referenced by bare filename.
Read figure content at native/400dpi zoom, not the downscaled page render: Fig. 1
(7 degenerate schemas), Fig. 2 (homophilous vs heterophilous subgraphs — panels do show
what the caption claims), Fig. 3 (LP protocol), Fig. 4 (7 HIN schemas), Fig. 5 (Freebase
complete K8 + 8 self-loops, book shaded). All legible at printed size.

**Format.** Cover page reproduced as required ("including the cover page"). Worker dirs
`p1/` and `p2/` both pass `lint_output.py`. (`lint_output.py` on `final/` reports
"missing answer.tex" etc. — that linter targets worker deliverable dirs under R4, not the
assembled `final/`; not a defect.)

### Defects

- [D1.1] **§4.3 is a section heading with no body, and its table lands after the section
  that follows it.** `p1.tex:706` emits `\subsubsection*{4.3 Which metric is reported on
  which dataset}` and then immediately a `\begin{table}[htbp]`. Nothing else. Table 3
  (`\label{p1:tab:metrics}`, `p1.tex:712`) is **never `\ref`'d anywhere in the
  document**, so the float has no anchor text and drifts to rendered page 15. The reader
  therefore sees, on rendered page 14: an empty numbered subsection "4.3", immediately
  followed by "5. Summary" — then turns to a mostly-blank page 15 holding an
  unintroduced table. It reads as a dropped section, and a summary should not precede
  the material it summarises.
  *Where:* `output/.../final/p1.tex:706-712`; rendered pages 14–15 of `main.pdf`.
  *Severity:* **major**.
  *Resolution:* give §4.3 a one- or two-sentence body that introduces and
  `\ref`s Table~\ref{p1:tab:metrics}, and/or change the float to `[H]` (the `float`
  package is already loaded in `main.tex`) so the table stays inside §4.3, ahead of §5.

- [D1.2] **Two more tables are orphaned with no cross-reference.** Same root cause as
  D1.1, milder because text does surround them. Table 8 (`\label{p2:tab:summary}`,
  `p2.tex:739`) is never `\ref`'d; §5.3 "Summary: dataset → target → task → metric"
  (`p2.tex:733`) contains only a "Closing remark." paragraph that never mentions the
  table, which floats alone onto rendered page 28. Table 7
  (`\label{p2:tab:metapaths}`, `p2.tex:324`) is never `\ref`'d either and appears at the
  top of rendered page 22 with no textual introduction — §3's prose mentions only
  Figures 4 and 5.
  *Severity:* **minor**.
  *Resolution:* add `\ref`s from the surrounding prose; consider `[H]` for Table 8 so
  §5.3 is not an empty-looking heading.

- [D1.3] **Not every described benchmark has a drawn schema in Problem 2.** The Note
  says "describe each of the benchmark graphs (e.g., DBLP/ACM) and draw the related
  graph schema." Schemas are drawn for DBLP, ACM, IMDB, LastFM, ogbn-mag/MAG240M, Yelp
  and Freebase. AMiner, Douban, HGB-PubMed, MovieLens and Amazon are described in §2.2
  with no drawn schema. Amazon is the notable one: §2.2 explicitly says its schema is
  "a single node carrying two distinct self-relations" and then does not draw it, even
  though the text leans on it to motivate the |A|+|R|>2 definition.
  *Severity:* **minor**.
  *Resolution:* a small one-node/two-self-loop glyph for Amazon and a 3-type sketch for
  AMiner would close this cheaply; both are already verbally specified in the text.

- [D1.4] **Six baselines are described twice.** DeepWalk, LINE, node2vec, GCN, GAT and
  GraphSAGE get full paragraphs in P1 §3 and one-line restatements in P2 §4.1. P2
  justifies this explicitly ("they are the control condition"), and each fragment must
  stand alone, so this is defensible — recorded for the record, not for action.
  *Severity:* **minor**, no action required.

### Resolved since last round

(none — first round)

### Still outstanding

(none carried in — first round)

### Where I looked and found nothing

Coverage vs. the assignment's own pages; hidden questions in the raw `.doc`; all 13
recomputable P1 dataset rows plus every alternative-convention figure in footnote 2;
PPI and OGB statistics; every arithmetic reconciliation in P2 Tables 4–6; ~55 citations;
LaTeX compile warnings, undefined/duplicate labels, margin overflow, label namespacing,
figure legibility at native resolution, cover-page requirement, worker-dir lint.
