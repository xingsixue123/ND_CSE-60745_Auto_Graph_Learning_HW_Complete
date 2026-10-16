# Master validator checklist — job hw_20261008_5ae5f8 (OS Homework 3)

## Round 1 — 2026-10-08

Verdict: **PASS** (with three minor defects noted, none substantive)

### What I checked and how

**Coverage** — enumerated the questions myself from
`input/os_hw_3_problems.md` (plain markdown; it is the only channel and it
carries the whole assignment) rather than from `problems.json`.
Ten exercises, Ex. 3.1 – Ex. 3.10, worth 10+10+5+5+5+5+10+10+20+20 = 100 pts.
All ten are answered, in assignment order, each under its own heading carrying
the assignment's own point value (including Ex. 3.8's "2 pts each" rider).
Sub-parts checked individually: 3.1 wants an explanation *and* a memory map —
both present (Figure 1); 3.7 wants "why" *and* "which instruction" — both
answered explicitly; 3.8 wants all five algorithms — FIFO, FILO, NRU, LRU, NFU
all described; 3.9 and 3.10 want three papers each, summarised *and* judged —
six papers, each with a `Summary.` and a `Critique.` paragraph. Nothing in the
assignment is unanswered; `uncovered` in problems.json is empty and that is
correct.

**Ex. 3.9 source check** — read `PaperList.xlsx` through all three channels
(`ingest/csv/PaperList.csv`, `pages/PaperList/page_00N.txt`, and the page PNGs).
The CSV flattens the merged "Topics" cells and the column-major PDF text
scrambles the topic order, but the page-3 image's colour banding independently
confirms the Memory Management group is exactly 3-1 … 3-7. The three papers
chosen (3-1, 3-6, 3-4) are all inside it. Ex. 3.10's three papers (far memory,
TMO, Pond) are not on the course list and do not repeat Ex. 3.9's.

**Correctness — recomputed**
- Ex. 3.2's arithmetic, from scratch: 8e12 cells x 0.021 um^2 = 1.68e5 mm^2;
  sqrt = 0.41 m; 2 x 0.41 m / c = 2.7 ns; x 4 GHz = 10.9 ~ 11 cycles;
  1.68e5 / (pi x 150^2) = 2.38 ~ 2.4 wafers. All four figures check out, and
  the 0.021 / 0.025 um^2 SRAM bitcell pair is the right way round for the bound
  to be conservative.
- Ex. 3.3–3.8 against the standard treatment: NRU's (R,M) class numbering,
  aging's shift-right-with-R-in-the-high-bit, the 8-tick resolution limit,
  FIFO's Belady anomaly vs. LRU's stack property, the two-handed clock's
  gap-as-test-interval — all correct. The FILO reading (evict the newest) is
  the right reading of "first-in last-out" and the answer flags that it is a
  reading.

**Correctness — R9, every quotation and characterisation in Ex. 3.9 / 3.10**
Extracted full text from all six source PDFs and checked each quote *and the
passage around it*. Every one is verbatim and in context:
- Denning 1968: "references to the same page tend to cluster in time";
  "Random brings on the highest page traffic, working set the lowest";
  "more than offset by its accuracy"; the i.i.d. interreference assumption at
  eqs. (8)–(11); tau ~ 2T for a 50% residency drop; sigma = tau/K and the K use
  bits; the *checker* in the running list; the hyper-exponential q; the
  l*sigma/N multiprocessor sampling remark and the appendix's t-register
  correction. Confirmed the paper does *not* correct the software scheme
  afterwards — the critique read to the end of that discussion.
- Mach 1987: "about the size of a device driver" (6K pmap); fork 256K 41 ms vs
  145 ms on the RT PC; 23 vs 28 s at 400 buffers and 19 s vs 1:16 generic
  (the 4:1 margin); "approximately 3 weeks" by "a newly hired programmer who
  had not previously either worked on an operating system or programmed in C";
  "allows only one valid mapping for each physical page"; "None of the
  multiprocessors running Mach support TLB consistency"; "rare enough in normal
  application programs" (vs ACIS 4.2a); S3.5's opening "Most of the complexity
  of Mach memory management arises from..." and the shadow-chain GC quote,
  followed — as the critique says — by the locking-rules discussion.
- Superpages OSDI'02: Table 2 reread cell by cell (C4 1.36 -> 0.98,
  SP 1.19 -> 0.98, mcf 1.68 -> 1.22, best single size for mcf 1.31); 18/35 over
  5% and 10 over 25%; factor-of-100 TLB coverage decline and 4-5% -> 30-60%;
  8.9% adversary with 7.2 from PTE replication; the abstract's "these benefits
  are sustained even under stressful workload scenarios"; "may deny the
  benefits of superpages to processes that do not write to all of the base
  pages"; the SHA-1 rejection at "up to 15%" / "60%" — and the very next two
  sentences do propose the two optimisations the critique names, left to future
  work. i386 is named once, in S2.2, and never returned to. "no superpage at
  all" is the paper's "unable to provide even a single 4MB superpage".
- Far memory ASPLOS'19: T=120 s, 32% cold, 1%–52% within one cluster;
  kstaled run "at a frequency of 120 s" with "8 bits per page ... in the
  struct page"; P = 0.2%/min; GP Bandit; 3x at median, 6.4 us; 15% hand-tuned
  -> 20% autotuned = "a 30% increase"; 4–5% TCO; "of even a few percentage
  points" / "offset all potential TCO savings"; "within noise"; "less than 11%
  of a single logical CPU core"; 0.01% / 0.09%. Confirmed independently that
  K and S are indeed never given numeric values anywhere in the paper.
- TMO ASPLOS'22: the 20-32% = 7-19% + 13% decomposition is the paper's own
  sentence, and the two denominators really do conflict — Figure 9's caption
  reads "normalized to their resident memory size" while S4.1 reads "7-19% of
  the total memory". Also verified "does not require offline application
  profiling"; "iteratively arrived at"; reclaim_ratio 0.0005,
  PSI_threshold 0.1%, every six seconds; "TMO's effectiveness is not very
  sensitive to these parameters" and, two sentences later, the future-work
  note the critique credits them with; Config B's "significant RPS regression,
  violating our design goal"; "has worked well for us in production"; and the
  fast-SSD/higher-promotion-rate/higher-RPS result (Figure 12 caption).
- Pond ASPLOS'23: 100 clusters; 8-16 sockets at 70-90 ns, rack-scale >180 ns;
  43% within 5% and >21% losing above 25% at 182%; "~50% of all VMs touch less
  than 50% of their rented memory"; zNUMA traffic 0.06-0.38%; RandomForest +
  LightGBM quantile regression; 7% DRAM at 16 sockets = 3.5% of server cost;
  emulation "by disabling all cores in one socket"; "Modern CPUs can connect to
  multiple EMCs"; S7's "any individual customer's behavior will have a small
  impact" plus the discount clause; the model's top feature being percentiles
  "by a customer's VMs in the last week"; the 2% misprediction target against
  "mitigate up to 1% of mispredictions" (hence "at most half"); Finding #3's
  "30-35% with 20-75% of workload memory spilled".

**The PDF** — read `output/.../final/main.pdf` through both channels: rendered
all 11 pages at 160 dpi and looked at them, and extracted the text. Recompiled
the document from the shipped sources in my own directory: exit 0, **zero**
Overfull/Underfull boxes, no undefined or multiply-defined references, 11 pages
matching the shipped PDF. Both TikZ figures (the memory map, the two-handed
clock ring) render as vector art, are legible at printed size, and are
semantically right — I checked the clock's sweep direction (counter-clockwise,
30 deg -> 120 deg) against which hand is drawn leading, and the R=1/R=0 shading
on either side of the gap. No missing-file boxes, no raw LaTeX source leaking
into the output, no duplicated or orphaned sections. Page 11 is a three-line
spill of the last paragraph, not an orphan section.

**Redundancy and altitude** — no code dumps, no repeated boilerplate across
problems, no debugging residue, no figure used twice. Cross-references between
the clustered short answers (3.3 -> 3.7/3.8, 3.4 -> 3.8, 3.5 -> 3.4) are used
to avoid re-defining LRU/NFU in four places, which is the right call.

**R8 length** — counted. 5-pointers: 3.3 = 237, 3.4 = 225, 3.5 = 232,
3.6 = 253 words (the last two include ~20 words of figure labels), against a
190-word target with a 290 allowance for sub-parts; 3.5 and 3.6 both have
labelled sub-parts. 10-pointers: 3.1 = 402 words of prose (figure stripped),
3.2 = 392, 3.7 = 330, 3.8 = 367. Per paper in 3.9 / 3.10: 527, 569, 543, 525,
534, 545 words against the 550-word target for a paper summary and critique.
Nothing is over target by a quarter. No defect.

**Format compliance** — `specs.md` imposes nothing beyond pointing at the
instructions file; no cover page, naming or ordering requirement to violate.
`lint_output.py` is clean on p1–p5 and on `final` with `--final`.

### Defects
- [D1.1] Ex. 3.10, paper 3 (Pond), Summary, p.10 of main.pdf: "leftover memory
  cannot be rented, reaching 25% at the 95th percentile" fuses two separate
  statements — the introduction's "up to 25% of DRAM becomes stranded" and
  S3.1's summary bullet "3-27% of stranded memory in production at the 95th
  percentile, with some outliers at 36%". The number is inside the paper's own
  range and matches its headline figure, so nothing downstream changes; the
  attribution is just imprecise. Resolution: say "up to 25%" or quote the
  3-27% range. | severity: minor
- [D1.2] `output/.../p1/answer.tex` (and `final/p1.tex`):
  `\usetikzlibrary{decorations.pathreplacing}` is issued in the document body
  rather than declared in `p1/preamble.txt`. It compiles and `lint_output.py`
  is clean, but a library load belongs in the preamble, and a second problem
  loading the same library would issue it twice. Resolution: move it to
  preamble.txt. | severity: minor
- [D1.3] `final/main.tex` gives no `\author`, so latex emits
  "LaTeX Warning: No \author given". Nothing in specs.md or the assignment
  requires a name, so this is a cosmetic observation only. | severity: minor

### Resolved since last round
- (first round)

### Still outstanding
- (first round)

### Where I looked and found nothing
Recomputed Ex. 3.2's four numeric claims; reread Table 2 and Table 7-1/7-2 of
the two measurement papers cell by cell; opened all six cited PDFs and checked
every quotation against the sentences that follow it (R9), which is where I
expected the failure and did not find one — in three places the critique
explicitly reports what the source does next with the material it is quoting;
re-derived the Memory Management paper group from the spreadsheet through all
three ingest channels; and recompiled the document looking for overfull boxes
and broken references, of which there are none.

---

## Round 2 — 2026-10-08

Verdict: **PASS** (one minor defect noted; one round-1 defect withdrawn as my error)

### What changed, and what I re-checked

Diffed the submission against my round-1 snapshot. `main.tex`, `p2.tex`,
`p3.tex` and `p4.tex` are byte-identical; `p1.tex`, `p5.tex` and
`preamble.tex` changed, each by a single hunk. So coverage, numbering, points,
and the whole of Ex. 3.2–3.9 are untouched and carry over from round 1. I
re-ran the mechanical checks in full and re-verified the two edits against
their sources.

- Recompiled from the shipped sources: exit 0, **zero** Overfull/Underfull
  boxes, no undefined or multiply-defined references, 11 pages. Extracted the
  text of my rebuild and of the shipped `main.pdf` and compared: **identical**,
  so the shipped PDF really is built from the shipped sources and is not stale.
- `lint_output.py` clean on p1–p5 and on `final` with `--final`.
- Re-rendered and looked at page 1 and page 10, the two pages the edits touch.
- Re-counted words: p1 prose 401; the six paper sub-answers 527 / 569 / 543 /
  525 / 534 / 550. Still on the 550-word target; the Pond edit added five words.

### Resolved since last round
- **[D1.2] fixed.** `\usetikzlibrary{decorations.pathreplacing}` now sits in
  `p1/preamble.txt` and is merged into `final/preamble.tex` after
  `\usepackage{tikz}`, and the line is gone from the body of `p1.tex`. I
  checked the consequence rather than just the diff: page 1's memory map still
  renders both `decorate`/`brace` spans correctly, so the library is loading in
  its new position.

### Withdrawn
- **[D1.1] withdrawn — my error, not the master's.** I reported that "reaching
  25% at the 95th percentile" fused two statements in the Pond paper. It did
  not. Pond S3.1's body says verbatim: "At the 95th percentile, stranding
  reaches 25% during high utilization periods." That is direct support for the
  wording as it stood. In round 1 I matched the claim only against S3.1's
  closing summary bullet ("3-27% ... at the 95th percentile, with some outliers
  at 36%"), which sits about a page later and gives different numbers from the
  body, and I did not search the section body for the 25% itself. The original
  sentence was correct and correctly sourced, and should not have been flagged.

### Defects
- [D2.1] Ex. 3.10, paper 3 (Pond), Summary, p.10 of main.pdf: the replacement
  wording "leftover memory cannot be rented --- 3--27\% of it at the 95th
  percentile, depending on the cluster" misattributes the range. The 3-27%
  comes from Pond's Figure 2, whose x-axis is the percentage of scheduled CPU
  cores; each bucket pools hourly snapshots from all 100 clusters, and the
  range is the 95th-percentile band read across *utilization* buckets, not
  across clusters. The paper reports no per-cluster stranding breakdown at all
  (Figure 2 is its only stranding figure), attributes within-bucket spread to
  "different VM mixes", and ties the top of the range to load: "stranding is an
  artifact of highly utilized nodes" and "At the 95th percentile, stranding
  reaches 25% during high utilization periods". Resolution: either revert to
  the round-1 sentence, which was right, or change the trailing clause to
  something like "once most of a server's cores are booked". | severity: minor
- [D1.3] carried forward: `final/main.tex` gives no `\author`, so latex warns
  "No \author given". Nothing in specs.md or the assignment asks for a name, so
  I am not treating this as something to fix; it stays recorded only as an
  observation. | severity: minor

### Still outstanding
- [D1.3] not addressed, and deliberately so — see above.

### Why this is a pass
The substantive work was verified in round 1 and is unchanged: full coverage of
Ex. 3.1-3.10 at 100 points, correct technical content, ~60 quotations and
numeric claims checked against the six source PDFs with their surrounding
context, a clean compile with legible figures, and lengths on target. Round 2
fixes one real defect and, acting on a bad call of mine, swaps a correct
sentence for one with a smaller error in it. D2.1 is a single misattributed
qualifying clause inside a 550-word summary; the numbers in it are the paper's
own and nothing downstream depends on it. A minor defect alone is not grounds
to withhold a pass, so I am passing with it noted.

---

## Round 3 — 2026-10-08

Verdict: **PASS**

### What changed

One file, one hunk. `main.tex`, `preamble.tex`, `p1.tex`, `p2.tex`, `p3.tex`
and `p4.tex` are byte-identical to round 2. `p5.tex` changed, and it is now
**byte-identical to the round-1 version**: the Pond stranding sentence is back
to "leftover memory cannot be rented, reaching 25\% at the 95th percentile".
No files were added or removed from `final/`.

So the submitted document is round-1 content throughout, plus round 2's fix
moving the tikz library into the preamble. Every word of it has now been
verified across three rounds.

### Resolved since last round
- **[D2.1] fixed.** The master took the first of the two resolutions I offered
  and reverted the clause. The restored wording is the one Pond S3.1 supports
  verbatim — "At the 95th percentile, stranding reaches 25% during high
  utilization periods" — so the misattribution to cluster-to-cluster variation
  is gone and nothing incorrect replaced it. Confirmed in the shipped PDF's
  page-10 text, not just in the source.

### What I re-checked this round
- Recompiled from the shipped sources: exit 0, **zero** Overfull/Underfull
  boxes, no undefined or multiply-defined references, 11 pages. Extracted text
  from my rebuild and from the shipped `main.pdf`: **identical**, so the
  shipped PDF is built from the shipped sources and is not a stale artifact.
- `lint_output.py` clean on p1-p5 and on `final` with `--final`.
- Pulled the question headings straight out of the PDF text: Ex. 3.1 (10 pts),
  3.2 (10), 3.3 (5), 3.4 (5), 3.5 (5), 3.6 (5), 3.7 (10), 3.8 (10, 2 pts each),
  3.9 (20), 3.10 (20) — ten questions, assignment order, 100 points.
- Re-rendered all 11 pages. Vector-drawing counts per page are 14 on page 1 and
  24 on page 4, matching round 1 exactly, which is independent evidence that
  both TikZ figures still draw in full after the library move rather than
  merely compiling without error.
- Read page 7 as an image. That was the one page I had previously read only as
  text, so every page of the final PDF has now been read through both channels.
- Re-counted words: Ex. 3.1 401, 3.2 393, 3.3 231, 3.4 222, 3.5 230, 3.6 233,
  3.7 326, 3.8 362; the six paper sub-answers 527 / 569 / 543 / 525 / 534 /
  545. All on target; nothing within a quarter of the R8 ceiling.

### Defects
- (none new)
- [D1.3] carried forward and deliberately not fixed: `final/main.tex` gives no
  `\author`, so latex warns "No \author given". Nothing in specs.md or the
  assignment front matter asks for a name, and the master has none to use.
  Recorded as an observation, not as work to do. | severity: minor

### Still outstanding
- [D1.3] only, by design.

### Closing state of the defect list
- [D1.1] withdrawn in round 2 — my error, not a defect in the work. Pond S3.1's
  body supports the original sentence verbatim; I had compared it only against
  the section's closing summary bullet.
- [D1.2] fixed in round 2 and still correct in round 3.
- [D2.1] fixed in round 3.
- [D1.3] open, cosmetic, nothing requires it.

Nothing substantive is left to blame. Coverage is complete and checked against
the assignment itself rather than against `problems.json`; the technical
answers to Ex. 3.1-3.8 were verified against first principles and recomputed
where they were recomputable; every quotation and numeric claim in Ex. 3.9 and
3.10 was checked against the six source PDFs *with its surrounding context*,
which is where this pipeline usually fails and where this submission holds up;
and the document compiles clean with legible figures at the right lengths.
