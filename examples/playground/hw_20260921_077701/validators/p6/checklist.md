# p6 validation checklist — Ex. 2.8, three scheduling papers found by search

## Round 1
Verdict: FAIL

### What I verified independently (all PASSED)

Ground truth / scope
- Brief transcription matches `input/hw2_instruction.md` line 38 verbatim. No discrepancy.
- Exclusion set confirmed from `ingest/csv/PaperList.csv`: 2-1…2-7 is the Scheduling
  group (3-1 starts Memory Management). Grepped the whole list for `liu|layland|wasted
  cores|shinjuku|kaffes|lozi|hard-real-time` — **zero hits**, so none of the three
  chosen papers is on the list anywhere, not just in the Scheduling group.
- Paper 1 adjacency concern (worker's own item 1): Liu & Layland is explicitly offered
  in the brief's candidate pool, and the critique is built on the cost model and (A3)
  rather than on RM-vs-EDF. In bounds. Not a defect.

Provenance
- Re-ran `pdftotext -layout` on all three PDFs myself: output is **byte-identical** to
  the worker's `text/*.txt`. The extracts are genuine.
- Downloaded PDFs are the real papers (checked content, not just filenames).

Liu & Layland — every quotation and number checked against the PDF
- Critical-instant quote (Thm 1), Thm 2 RM-optimality, Thm 7 EDF iff ∑Cᵢ/Tᵢ≤1,
  U=m(2^{1/m}−1) with 0.83 / 0.78 / ln2 — all verified.
- §9 example T=(3,4,5), C₁=C₂=1: 98.3 % / 100 % / 78.3 % verified, and the arithmetic
  reconciles (1/3+1/4+2/5=.9833; 1/3+1/4+1/5=.7833).
- §8 description ("k shortest-period tasks rate-monotonically on the interrupt
  hardware") matches the paper's own wording.
- A4 "bookkeeping time … costs of preemptions can be taken into account" — verbatim.
- §6 "the practical costs of switching between tasks must still be counted" — verbatim,
  and **"then never counts them" is TRUE**: grep for
  `overhead|context switch|switching|preemption cost|swap` over the whole paper returns
  exactly one line (L508). R9 satisfied — the worker engages the A4 hedge and rebuts it
  rather than pretending the paper is silent.
- "most important and least defensible" and "a design goal" quotes — verbatim.
- **"None of our analytic work would remain valid"** (worker's low-confidence item 2):
  I rendered PDF page 15 at 12× with pymupdf and read the line directly. It
  unambiguously reads "None". The worker's reading is correct; item 2 is resolved in
  their favour and needs no change.
- Sha/Rajkumar/Lehoczky 1990 blocking term and Mars Pathfinder 1997 — standard, correct.

Lozi et al. — every number checked
- Abstract invariant quote verbatim. make 13 % / lu 13×; groups {0,1,2,4,6} and
  {1,2,3,4,5,7} with nodes 1,2 in both and two hops apart; Table 1 lu 1040→38 s (27×);
  Table 2 TPC-H #18 −22.2 % and full −13.2 % (correctly attributed to the
  Overload-on-Wakeup row); Table 3 lu 137.59×; Table 5 single 8-node Opteron 6272.
- Table 4 "Impacted applications: All" for exactly three of four bugs (Group Imbalance,
  Sched Group Construction, Missing Sched Domains), and two of those three are
  topology-dependent. The critique's arithmetic is right.
- "Energy waste is proportional." verbatim, and it does follow the 13–24 % / 138 %
  performance sentence, so "proportional to the lost performance" is fair.
- Power gate quote verbatim **and in context** — the paper raises the tradeoff itself and
  the worker quotes its answer before arguing insufficiency. R9 satisfied.
- **"no power measurement anywhere" is TRUE** — I went beyond the worker's grep and
  checked every figure caption and every table in the paper. All figures are runqueue
  heatmaps, topology, and load-balance traces; no power axis, no power table.
- §3.5 "hacks retrofitted" quote verbatim and in context; §5 "core module and
  optimization modules" proposal verified.

Shinjuku — every number checked
- Table 1: sender 2081→298, receiver 2662→1212. Context switch 36–109 cycles.
  "without wasting more than 10 % of the workers' throughput" at 5 µs — verbatim, and the
  arithmetic checks (5 µs × 2.3 GHz = 11 500 cy; 1212/11500 = 10.5 %).
- CFS 6 ms target / 0.75 ms minimum; 5–15 µs quantum; 50 % / 5× at a 300 µs target on
  Bimodal(99.5−0.5, 0.5−500); RocksDB 88 % / 6.6×; 11 workers, 5 M / 9.5 M RPS.
- §3.6 RSS-steering quote, DoS quote, ring-3 remedy and 84-cycle transition, and the
  §3.1 "we run applications in VMX non-root mode ring 0 to avoid the address space
  crossings" — all verbatim.
- **The multi-dispatcher criticism is sound.** Figure 7b/c genuinely does "issue short
  requests with 1µsec fixed service time to stress the dispatcher", so head-of-line
  blocking cannot manifest in the one scaling experiment. I also read the adjacent
  "Connection counts" paragraph of §3.6, which answers a *different* objection (load
  imbalance / connection counts), so the worker's criticism survives its context.
- History: EEVDF in 6.6 (2023), sched_ext in 6.12 (2024), UINTR in Sapphire Rapids —
  all correct. The worker's deliberate refusal to claim mainline UINTR support is right.

Mechanical compliance
- R5: no `\documentclass`, `\usepackage`, `document` env, or `\bibliography`. The
  fragment defines **no `\label` and no macro**, so there is nothing to collide. No
  figures, so no filename namespacing needed. Compiled it myself in a bare
  `\documentclass[11pt]{article}` wrapper with **zero packages**: exit 0, no errors,
  5 pages. Absence of `preamble.txt` is therefore correct.
- R4: `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT contains only `answer.tex`.
- R3: `downloads.md` records all three PDF downloads with URLs; no software installed.
- R8: my independent word count reproduces the worker's exactly (439 / 492 / 487 per
  paper excluding headings, + 65-word search note). Papers 2 and 3 are ~9 % over the
  450 target — well inside the 25 % defect threshold. **Not a defect.**

### Defects

- [1.1] `answer.tex` L89–91: "the only other mention of power is the place where the
  Overload-on-Wakeup fix is switched off by it" is **false**. The paper mentions power
  in at least five other places: footnote 1 on p.1 ("not explicitly configured to save
  power by purposefully leaving cores unused so they can be brought into a low-power
  state"), the intro ("made energy efficiency a top concern"), §2.2 ("the optimizations
  that the scheduler employs to maintain low overhead and to save power"), §2.2.1
  ("Power-related optimizations may further reduce the frequency of load balancing on
  an idle core…"), and §5 ("either in terms of performance or power"). The worker's grep
  pattern `energy|watt|power consum|joule` missed every bare use of "power"; a plain
  `grep -i power` finds them. This is the exact R9 failure mode and a grader finds it
  with one grep. NOTE: the *load-bearing* claim, "the paper contains no power
  measurement anywhere", is correct and I confirmed it — only the "only other mention"
  clause must go. | `OUTPUT/answer.tex` L89–91 | severity: major

- [1.2] `answer.tex` L77–78: "the authors also build a sanity checker and a trace
  visualiser, **under 150 kernel lines between them**". The "less than 150 lines of
  code" sentence appears in §4.2 and refers to the visualisation tool's instrumentation
  alone. The sanity checker's cost is reported separately in §4.1 (implemented in Linux
  3.17; porting to 4.3 "only required changing one line of code"). "Between them" is
  unsupported. | `OUTPUT/answer.tex` L77–78 | severity: minor

- [1.3] `answer.tex` L28–30: "Section~8 mixes the two … **its** worked example,
  T=(3,4,5) …". The worked example and the 98.3 / 100 / 78.3 figures are in §9
  ("Comparison and Comment"), not §8. The worker's own `evidence.md` cites §9 correctly,
  so this is a slip introduced when writing the answer. | `OUTPUT/answer.tex` L28–30 |
  severity: minor

- [1.4] `answer.tex` L98–102: the sched_ext paragraph. Two problems. (a) "That is where
  history **contradicts** the paper" conflates vindication with contradiction: §5
  explicitly proposes "a scheduler that is a collection of modules: the core module and
  optimization modules", so sched_ext's arrival *confirms* the paper's own
  recommendation. Only the EEVDF half bears on §3.5's pessimism that a new design "is
  not a long-term solution". (b) "arrived as `sched_ext`" overstates the match:
  sched_ext is a BPF-based pluggable scheduler *class* that allows a whole scheduler to
  be replaced, not the "core module maintains the invariants while optimization modules
  suggest" architecture §5 describes. Separate the two claims and soften (b). |
  `OUTPUT/answer.tex` L98–102 | severity: minor

- [1.5] `answer.tex` L94–95: "Their **highest-value** fix is therefore disabled on
  virtually every production server." By the paper's own Table 4 ("maximum measured
  performance impact"), Overload-on-Wakeup is the *smallest* of the four at 22 %, against
  138× for Missing Scheduling Domains and 13× for Group Imbalance. It is the largest
  single fix only on the TPC-H database workload (−22.2 % vs −13.1 %). Qualify it, e.g.
  "their highest-value fix on the database workload". | `OUTPUT/answer.tex` L94–95 |
  severity: minor

### Resolved since last round
(none — first round)

### Still outstanding
[1.1] major; [1.2] [1.3] [1.4] [1.5] minor.

Note for the worker: the substance of this answer is in good shape. Every number in all
three papers checks out against the PDFs, the two central critiques are properly R9-built
(they quote the paper's own answer to the objection before arguing it is insufficient),
the "None of our analytic work" reading is correct, and the length is on target. The
defects are all localized sentence-level overreach in the paper-2 critique plus two
citation slips. Do not rewrite the answer; edit the five spans named above.

---

## Round 2
Verdict: PASS

### How I checked
Diffed round-1 against round-2 `answer.tex`. The diff touches exactly the five reported
spans plus two small edits (a word trimmed in the load-metric sentence, `\allowbreak` in
reference [3]'s URL). **Everything else is byte-identical to the text I verified
exhaustively in round 1**, so the previously confirmed numbers and quotations carry over
without re-checking.

### Resolved since last round

- [1.1] **major — FIXED.** The false "only other mention of power" clause is gone. The
  sentence now reads that power "runs through the paper as a design pressure without ever
  being measured --- no power figure, axis or table --- and it bites on the
  Overload-on-Wakeup fix." That is exactly what the evidence supports: power appears in
  the footnote, §2.2, §2.2.1, §5 and the intro, and none of those is a measurement. The
  claim is now both true and still pointed. `evidence.md` L40 records the bad grep
  pattern and the correction, so the audit trail no longer vouches for the error.
- [1.2] **FIXED.** Now "a trace visualiser, the latter needing under 150 lines of kernel
  instrumentation" — the 150 lines is attributed to the visualiser alone, matching §4.2.
- [1.3] **FIXED.** Now "the worked example in Section~9".
- [1.4] **FIXED, and better than I asked.** I had flagged the vindication/contradiction
  conflation for the sched_ext half only. The worker checked and found *neither* half was
  a contradiction: EEVDF replacing CFS is an instance of "new scheduler designs come and
  go", i.e. the §3.5 prediction coming true. The paragraph is now framed as vindication
  of both, and the sched_ext match is explicitly softened ("The fit is loose, since
  `sched_ext` replaces the whole scheduler rather than advising an invariant-keeping
  core"). I verified both new quotations verbatim against the PDF (de-hyphenating the
  extraction first): "new scheduler designs come and go" and "a scheduler that is a
  collection of modules: the core module and optimization modules". The reading of
  sched_ext as "moves policy into BPF programs outside the core" is accurate.
- [1.5] **FIXED.** Now "The fix that wins most on their database workload", which is what
  Table 2 supports (−22.2 % vs −13.1 %), instead of the unsupported "highest-value fix".

### Re-verified mechanically
- Compiles in a bare `\documentclass[11pt]{article}` with **zero packages**: exit 0,
  5 pages. With `geometry margin=1in`: **zero overfull boxes**, confirming the worker's
  claim for that configuration.
- The `\allowbreak` edit is safe: I extracted the rendered text and the URL comes out as
  `https://www.usenix.org/conference/nsdi19/presentation/kaffes` with **no spurious
  spaces** (TeX absorbs the newline after the control word).
- R5: zero hits for `\documentclass|\usepackage|\begin{document}|\bibliography|\label`.
  Still no macros and no figures, so nothing can collide with another problem.
- R4: `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT holds only `answer.tex`.
- R3: `downloads.md` unchanged and still complete; no new downloads or installs.
- R8: my independent count again reproduces the worker's exactly — 442 / 529 / 487 body
  words plus a 54-word search note. Paper 2 grew to 17.6 % over the 450 target, still
  inside the 25 % threshold, and the growth buys real substance (separating the two
  historical claims and qualifying the sched_ext match). Not a defect.

### Still outstanding
None blocking. One cosmetic note, recorded and deliberately not held against the worker:

- (cosmetic) In a *narrow* column — default `article` margins, no `geometry` — reference
  [3]'s URL still produces a 41 pt overfull hbox, because TeX prefers breaking at the last
  `\allowbreak` over a badly underfull earlier line. Two other overfull boxes in that
  configuration are sub-3 pt and invisible. With 1 in margins, which is what the master
  most likely uses, there are none. Not worth another round; if the master's geometry
  turns out to be narrow, breaking the URL after `nsdi19/` would settle it.

### Assessment
The worker verified each reported defect against the PDF before editing rather than
accepting the report, confirmed all five, found [1.4] to be worse than I had described,
corrected the audit trail, and changed nothing that was already passing. The substance —
every number in three papers, both R9-built critiques, the "None of our analytic work"
reading — was verified in round 1 and is untouched. Nothing substantive remains.
