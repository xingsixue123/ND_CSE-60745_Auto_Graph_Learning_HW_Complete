# p5 — Ex. 3.10 — validator checklist

## Round 1
Verdict: PASS

### What I checked and how

**Ground truth (R7).** Source is `input/os_hw_3_problems.md`, plain markdown, no page
images and no figures — the three-channel rule degenerates to one. The brief's
transcription is verbatim-identical to the file's last line. No discrepancy; no figure
to miss. The worker said the same and was right.

**Collision with Ex. 3.9.** `ingest/csv/PaperList.csv` lines 20-26 are 3-1 … 3-7
(merged topic cell carries "Memory Management" only on 3-1; the `3-` prefix confirms
the span). Sibling `p4/answer.tex` uses 3-1, 3-6, 3-4. Grepped the whole list for
far memory / offload / CXL / pool / disaggregat / warehouse — only hit is 6-6 (LegoOS),
different topic group. None of p5's three papers collides. Confirmed independently.

**Papers are real and were actually read.** `pdfinfo` on all three: titles, author
lists, acmart producer, 14/13/14 pages. Copied `scripts/extract.py` into my own dir
and re-ran it against the same PDFs — all three `.txt` byte-identical to the worker's.

**Citations — verified independently, not taken on trust.** Crossref on each DOI, and
each PDF's own ACM Reference Format block:
- 10.1145/3297858.3304053 — ASPLOS '19 (24th), pp. 317-330, 14 authors, order matches
- 10.1145/3503222.3507731 — ASPLOS '22 (27th), pp. 609-621, 11 authors, order matches
- 10.1145/3575693.3578835 — ASPLOS '23 (28th) Vol. 2, pp. 574-587, 13 authors, order matches
Title, venue, year, pages and author order in `answer.tex` all correct. "Daniel Ernst"
agrees with both Crossref and the Pond title page.

**Every load-bearing number traced to a line in the papers.** ~35 claims checked; all
accurate. Spot list with the line I verified at:
- farmem: 32% cold at T=120s (259); 1-52% "even within a cluster" (332 + p4 continuation);
  P=0.2%/min (563); 3x compression / 6.4us (1141, 1151); 15%->20% = "a 30% increase" (937-940);
  4-5% DRAM TCO (1001); "of even a few percentage points" / "offset all potential TCO
  savings" (109-111); IPC "within noise", noise "expected" (1196-1202); 0.01%/0.09% job
  CPU, definition is compression+decompression only (1083-1089); kstaled "less than 11%
  of a single logical CPU core" (761-763); kstaled at 120s frequency, 8-bit age in
  `struct page` (745-750); K-th percentile control (604, 793-795); GP Bandit (869);
  upstream zswap "triggered only on direct reclaim", "unbounded", "bursty" (447-458).
  **K and S: exhaustive grep (604/638/793/801/819/1069) — mentioned six times, never
  assigned a value. The answer's claim is exactly right.**
- TMO: 20-32% = 7-19% + 13% (190-193); Figure 9 caption "normalized to their resident
  memory size" (926-927) vs §4.1 "7-19% of the total memory" (944-945) vs Figure 10
  "normalized to a server's total memory" (961-962) — **the denominator inconsistency is
  real, in adjacent paragraphs, and I found no reconciling footnote either**;
  Senpai r=0.0005, PSI_threshold=0.1%, every six seconds, "iteratively arrived at"
  (772-775); control law (737-741) matches the formula in the answer exactly;
  "not very sensitive to these parameters" (783) vs Config B "violating our design goal"
  (1335); "does not require offline application profiling" (205-207); g-swap = ref [18]
  = the farmem paper (127-130, 1605); "directly contradicts g-swap's assumption"
  (150-154); faster SSD -> higher promotion rate *and* more RPS (1177-1180);
  some/full (579-582); shadow entries / reuse distance (846-856).
- Pond: stranding 25% at p95 (359-361), 100 clusters / 75 days (340); pinning required
  by virtualization acceleration (261-262); 70-90ns at 8-16 sockets, >180ns rack-scale
  (134-135); 158 workloads at 182%: 26%+17%=43% within 5%, 21% >25% (469-481);
  ~50% of VMs touch <50% (148-149); zNUMA traffic 0.06-0.38% (1384, Fig 15);
  emulation = disabling one socket's cores (1245-1248); capacity-only simulator
  (1327-1330); §7 "any individual customer's behavior will have a small impact"
  (1600-1604); §4.4 "most important feature is … untouched memory by a customer's VMs
  in the last week" (1181-1183); 2% misprediction target (1545) / monitor "up to 1%"
  (1538-1539); PDM/TP definition "configurable tail-percentage … e.g., 98%" (520-524);
  Finding #3 30-35% with 20-75% spilled (1427-1432); 7% DRAM / 3.5% server cost
  (1682-1685); "Modern CPUs can connect to multiple EMCs" (813-814); 16 hosts / 12 DDR5
  channels on one EMC (537-538), which is exactly the contention the critique names.

**R9 — I opened every passage behind a "the paper does not address X" claim.** All three
survive, and each one names what the paper does next:
- TMO block-IO: the answer quotes the admission (626-630) *and* the paper's reply one
  line later, "has worked well for us in production" (631-632). I also read §4.4's
  separate IO-PSI discussion (1351-1361) — that passage is a case where high IO PSI was
  *correct* (bytecode misses really did cost RPS), so it is not a defence against the
  device-speed/oversubscription conflation. "The paper's only answer" stands.
- Pond gaming: §7 does raise it; the answer says so and then shows why the aggregate
  reply ("millions of customers") misses a model whose top feature is that customer's
  own VM history. Correct, and the stronger criticism.
- Pond's other §7 answer (discounts) appears exactly once in the paper (1604) and is
  never implemented or evaluated — "a clause" is accurate.
- farmem autotuner: the answer does *not* claim app metrics were ignored (§6.2 at
  1011-1013 says they were monitored); it criticises the missing resolution. Correct.
- TMO insensitivity: the answer credits the paper for flagging automated tuning as
  future work (787-789) and aims the criticism at the insensitivity claim instead. Correct.

**R8 — I counted.** My own tokenizer: 441 / 452 / 453 prose words, total **1,346**;
lead-in 69; whole file 1,676 including citations. Brief's budget is 400-450 per paper
and 1,200-1,350 total. Within it. Summary/critique split 57/42, 50/49, 52/47. Two
em-dashes in 1,346 words. No padding, no restatement, no signposting.

**R5 / LaTeX.** No `\documentclass`, `\usepackage`, `document` environment. No `\label`,
no `\includegraphics`, no `\ref` — nothing needing namespacing, correctly. Compiled it
myself in a fresh minimal wrapper (amsmath, amssymb, graphicx, geometry): exit 0, no
warnings, no overfull/underfull boxes, no `missfont.log`. Rendered to PNG and read the
pages — clean layout, nothing clipped or overlapping. No `preamble.txt` needed, correct.

**R4 / R3.** `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT holds only `answer.tex`.
`downloads.md` lists all three PDFs with source URL, path and reason, and records that
nothing was installed; no venv, wheel or pip cache anywhere in the playground.

**Does it answer the question asked?** "Search for three papers … Read, summarize, and
critically judge them. Write at least 1/3 page for each." Three papers, none from the
course list, each with full citation + summary + critique, each block far above 1/3 page.
`needs: plain` is the right call — nothing to compute, nothing to draw.

### Defects
None blocking or major.

### Minor observations (reported, not blocking)
- [1.1] `answer.tex:134-135` — "The result is 7% less DRAM at a 16-socket pool, or 3.5%
  of server cost." That is the paper's own abstract/conclusion headline (pond.txt:1682-1685),
  but it assumes a **222%** latency increase; Finding #9 (1562-1564) gives **9%** at 16
  sockets under 182%. The surrounding sentences establish the 182% configuration, so a
  reader could attach 7% to the wrong row. The number is the paper's, so this is
  looseness of context, not a wrong figure. | severity: minor
- [1.2] `answer.tex:128` — "21% lose more than 25%" drops the intro's "more than 21%"
  (pond.txt:142), though §3.3 (480-481) says exactly "21%". Errs in the paper's favour;
  the worker disclosed it. | severity: minor
- [1.3] `answer.tex:120` — "reaching 25% at the 95th percentile" omits the paper's
  qualifier "during high utilization periods" (pond.txt:360-361); the preceding clause
  ("when all cores of a server are rented") substantially carries it. | severity: minor
- [1.4] Pond's CCS concepts are Cloud computing / Emerging architectures, not Memory
  Management as on the other two papers. The paper is squarely about memory pooling and
  allocation, so the topic fit is fine, but it is the one of the three a strict grader
  could query. | severity: minor
- [1.5] Two blocks come in at 452 and 453 prose words against the brief's 450 ceiling,
  by my tokenizer. Three words. | severity: minor

### Resolved since last round
n/a — first round.

### Still outstanding
Nothing substantive. The five items above are cosmetic and do not change what a grader
would award.
