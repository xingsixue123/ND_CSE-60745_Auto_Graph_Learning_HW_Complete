# p5 — Ex. 3.10 submission

## What the problem asked

> Ex. 3.10 | (20pts) Search for three papers on the topic of 'Memory Management'.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper's
> summarization and judgment.

**Brief vs. ground truth: no disagreement.** The source is `input/os_hw_3_problems.md`,
plain markdown, and `problem.md`'s transcription is verbatim-identical to the last line
of that file. Ingest classifies it `text_document` with no `pages` array, so there are no
page PNGs and no figure files — R7's three channels degenerate to one here, and there is
no figure to miss.

The second input, `PaperList.xlsx`, I read through all three channels (CSV export,
rendered-PDF per-page text, page PNGs) because the "papers to avoid" set depends on it.
Its Topics column uses merged cells: the literal string "Memory Management" appears only
on row 3-1, and the column-major PDF extraction shows 6 topic labels for 56 rows, which
is the merged-cell signature. The `3-` ID prefix confirms the grouping independently, so
the set to avoid is 3-1 … 3-7 (`ingest/csv/PaperList.csv` lines 20-26), as the brief says.

**Collision checks, both negative.** Grepping the entire paper list for *far memory,
offload, CXL, pool, disaggregat, warehouse* hits only 6-6 (LegoOS), a different topic
group and not one of mine. The accepted sibling answer for Ex. 3.9 (`../p4/answer.tex`)
uses 3-1, 3-6 and 3-4; none of my three appears there.

## What I decided it needed

**plain.** No number is requested, so there is nothing to compute; nothing is to be shown,
plotted or drawn, so there is no figure. The only work beyond writing was obtaining and
reading the three papers in full and verifying the citations against the publisher.

## What I did

Picked three production-systems papers — Google (2019), Meta (2022), Microsoft (2023) —
that answer a question the 1968–2002 course list never reaches: DRAM is now the dominant
server cost, so which pages leave it. I chose them as a set because they argue with each
other: TMO's §2 and §4.3 are an explicit empirical attack on the Google paper's control
signal, and Pond rejects the page-fault basis of both. That gives each critique somewhere
firm to stand instead of generic hedging.

Downloaded all three PDFs, extracted full text with pymupdf, and read each end to end
(14 + 13 + 14 pages). Wrote the answer as three blocks of citation + summary + critique,
compile-tested the fragment in a minimal master, and looked at all three rendered pages.

**This round was a re-verification round.** `answer.tex` (14:45) had been edited after the
previous `submission.md` (14:30), so that pointer file was stale and I did not trust it. I
re-checked every load-bearing quote and number against `papers/*.txt` from scratch and
re-confirmed all three citations against both Crossref and each PDF's title page. That
found three defects, all now fixed:

1. **Factual.** The answer said "32–64 sockets over 180 ns". Pond attributes ">180ns" to
   *rack-scale* pooling (pond.txt:135); its only statement about 32–64 sockets is that
   they "would combine CXL switches with Pond's multi-headed EMC" (pond.txt:642), with no
   latency figure. Substituting a socket count for "rack-scale" was unsupported. Now reads
   "rack-scale pooling more than 180 ns".
2. **R9.** The block-IO critique quoted TMO's own admission (tmo.txt:626-630) but stopped
   before the paper's reply one line later — "This has worked well for us in production
   across diverse workloads" (tmo.txt:631-632). The answer now quotes that reply, so the
   criticism is aimed at the defence the paper actually offers.
3. **LaTeX.** A single `\S4.1` pulled in the TS1 font `tcrm1095`, which METAFONT must
   generate; `~/.TinyTeX` is read-only, so the compile died *after* laying out all three
   pages. Replaced with "Section~4.1" (also matching the three other cross-references).
   The master would have hit the same failure.

On R9 generally, I checked every "the paper does not address X" claim against the
surrounding text. This had already changed one critique materially: the natural criticism
of Pond is that it never considers customers gaming the untouched-memory predictor, but
§7 *does* raise exactly that, so that criticism would have been wrong. The defect that
survives reading is narrower and stronger — §7's reply is about aggregation over millions
of customers, whereas §4.4 makes *that customer's own* VM history the model's most
important feature, so the reply does not reach the mechanism.

## Intermediate steps and code

Paths relative to PLAYGROUND.

- `scripts/extract.py` — the only script. Extracts page-delimited full text from each PDF
  in `papers/` to `papers/<name>.txt`. Reproduce: `python3 scripts/extract.py`.
- `papers/farmem.pdf`, `papers/tmo.pdf`, `papers/pond.pdf` — the three papers (sources and
  reasons in `downloads.md`). `papers/*.txt` are the extracted texts I read from and the
  line numbers below refer to.
- `build/master_test.tex` + `build/answer.tex` — minimal master used to compile-test.
  Reproduce: `cd build && pdflatex -interaction=nonstopmode master_test.tex` → exit 0,
  3 pages, no warnings, no overfull boxes, no `missfont.log`. `build/pg-{1,2,3}.png` are
  the renders I looked at; `build/answer_prev.tex` is the pre-round-2 text, for diffing.
- `notes.md` — plan, merged-cell check, citation verification, and the line-numbered R9
  checks for every critique claim, with a round-2 section recording the three fixes.

Citation metadata: `curl https://api.crossref.org/works/<doi>` for the three DOIs
(dl.acm.org returns 403 to WebFetch, so Crossref was the publisher-metadata route).

## Results

No value in this answer is computed by me; every number is quoted from a paper. The
load-bearing ones, each re-verified this round at the stated line in `papers/*.txt`:

| Claim in answer.tex | Source |
|---|---|
| 32% cold at T=120 s; 1–52% "even within a cluster" | farmem.txt:259, 332-337 |
| promotion-rate SLO 0.2%/min of working set | farmem.txt:563, 1072-1073 |
| 3× compression, 6.4 µs decompression | farmem.txt:1141, 1151 |
| coverage 15%→20% = "a 30% increase"; 4–5% DRAM TCO | farmem.txt:937-940, 1001 |
| "of even a few percentage points" / "offset all potential TCO savings" | farmem.txt:109-111 |
| IPC "within noise"; noise "expected" in WSC A/B | farmem.txt:1199-1202 |
| 0.01%/0.09% job CPU; kstaled "less than 11% of a single logical CPU core" | farmem.txt:1087-1088, 761-762 |
| K and S never assigned numeric values | farmem.txt:604, 638, 793, 801, 819, 1069 — all mentions, none a value |
| 20–32% total = 7–19% + 13% | tmo.txt:190-193 |
| Fig 9 "normalized to their resident memory size" vs §4.1 "7-19% of the total memory" | tmo.txt:926-927 vs 944-945 |
| Senpai: r=0.0005, PSI_threshold=0.1%, every six seconds; "iteratively arrived at" | tmo.txt:772-775 |
| "not very sensitive to these parameters" vs Config B "violating our design goal" | tmo.txt:783 (§3.3) vs 1333-1335 (§4.4) |
| "does not require offline application profiling" | tmo.txt:205-207 |
| block-IO stall accounting + "has worked well for us in production" | tmo.txt:626-632 |
| faster SSD → higher promotion rate *and* more RPS | tmo.txt:1177-1180 |
| stranding 25% at p95; traces from 100 clusters / 75 days | pond.txt:359-361, 340 |
| pinning required by virtualization acceleration | pond.txt:261-262 |
| 8–16 sockets add 70–90 ns; rack-scale >180 ns | pond.txt:134-135, 809 |
| 158 workloads at 182%: 43% within 5%, >21% lose >25% | pond.txt:140-142, 385 |
| median 50% untouched; zNUMA traffic 0.06–0.38% | pond.txt:455, 1384 |
| 7% DRAM at 16-socket pool → 3.5% server cost | pond.txt:1682-1685 |
| emulation = disabling one socket's cores; capacity-only simulator | pond.txt:1246-1247, 1327-1329 |
| §7 "any individual customer's behavior will have a small impact" | pond.txt:1600-1605 |
| §4.4 "most important feature is … untouched memory by a customer's VMs in the last week" | pond.txt:1181-1183 |
| 2% misprediction target; monitor mitigates "up to 1%" | pond.txt:1545, 1539 |
| Finding #3: 30–35% slowdown with 20–75% spilled | pond.txt:1427-1432 |

Citations verified twice over — Crossref and each PDF's own title page agree on title,
venue, author list and order: ASPLOS '19 (24th) pp. 317–330, 14 authors; ASPLOS '22 (27th)
pp. 609–621, 11 authors; ASPLOS '23 (28th) Vol. 2 pp. 574–587, 13 authors. Crossref
lowercases TMO's title; I used the paper's own title case. Both sources say "Daniel
Ernst" for Pond.

Word counts, prose only (excluding citations and the 60-word lead-in), against the
brief's 400–450 target: **437 / 450 / 452**, prose total **1,339** (brief: 1,200–1,350).
Summary/critique split 58/42, 51/49, 52/48. Em-dashes: 2.

## Deliverables

- `OUTPUT/answer.tex` — the fragment. No `\documentclass`, `\usepackage` or `document`
  environment; starts at `\section*{Ex.~3.10 …}`.
- No `preamble.txt`: needs nothing beyond amsmath/amssymb/graphicx/geometry.
- No figures (the question asks for none).
- No `\label` and no `\includegraphics`, so nothing required namespacing; the only
  identifier is the section heading.
- `python3 framework/tools/lint_output.py <OUTPUT>` → `OUTPUT LINT OK`, exit 0.

## Where I am least confident

1. **Selection taste.** All three papers are datacenter capacity-cost papers from one
   five-year window. That is deliberate — it is what lets each critique cite the others —
   but a marker who wanted three *unrelated* memory-management topics could fairly call
   the set narrow. The marks are for summary and critique, so I took the trade.
2. **"the monitor mitigates at most half of them"** reads Pond's "QoS monitor to mitigate
   up to 1% of mispredictions" (pond.txt:1539) as 1 percentage point of VMs against
   the 2% misprediction target (pond.txt:1545), i.e. half. The paper does not say outright
   whether that 1% is in the same units as the 2%; same-units is the natural reading given
   the sentence sits beside it, but a reading of "1% *of* the mispredicting VMs" is not
   excluded, and that would make the claim far too generous rather than too harsh.
3. **"21% lose more than 25%"** slightly understates Pond, which says "*more than* 21% of
   workloads suffer a performance loss above 25%" (pond.txt:142). I dropped the "more
   than" for readability; it errs in the paper's favour.
4. **The TMO denominator criticism is my inference, not an admission.** The two texts say
   what I quote (Figure 9's caption "normalized to their resident memory size" vs §4.1's
   "7-19% of the total memory"). I am confident they are inconsistent; I am less confident
   that no footnote elsewhere reconciles them, though I searched and found none.
5. **The farmem "no resolution given" point** rests on the absence of a power analysis. I
   searched for one and found none, but absence of evidence in a 14-page paper is weaker
   than a positive contradiction. The §2-versus-§6.2 tension it rides on is solid, and I
   do *not* claim they ignored application metrics — farmem.txt:1196-1198 says they
   monitored them, and the answer says so.
6. **Pond has an internal stranding inconsistency I chose not to use**: the §3.1 text says
   25% at p95 with outliers at 30% (pond.txt:359-361), while the summary bullet of the
   same section says 3–27% at p95 with outliers at 36% (pond.txt:440-441). I quote only
   the §3.1 figure. I could not tell whether the bullet covers a different slice, and the
   paper does not say, so I left it out rather than assert a contradiction I cannot pin.
7. I read each paper's body and conclusion closely but skimmed the reference lists; a
   claim contradicted only by something in a cited work would have been missed.
