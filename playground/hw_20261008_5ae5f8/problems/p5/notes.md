# p5 — Ex. 3.10 notes

## Ground truth check (R7)
Source is `input/os_hw_3_problems.md`, a plain markdown file. Ingest produced only
`ingest/pages/os_hw_3_problems/alltext.txt` (no PNGs, no figure files) — consistent with
`manifest.json` (`kind: text_document`, no `pages` array). So the three-channel rule
degenerates to one channel here; there is no figure to miss.

Verbatim from the source file (last line of the file):

    Ex. 3.10 | (20pts) Search for three papers on the topic of 'Memory Management'.
    Read, summarize, and critically judge them. Write at least 1/3 page for each
    paper's summarization and judgment.

This matches problem.md exactly. No discrepancy between brief and page.

Second input, `PaperList.xlsx`: checked all three channels. CSV
(`ingest/csv/PaperList.csv`) + rendered PDF page text + page PNGs. The Topics column is
merged: only row 3-1 carries the literal string "Memory Management"; rows 3-2..3-7 have
an empty topic cell. The `3-` ID prefix confirms the group independently, and the
column-major PDF text extraction (topics land on rendered page 4, titles on page 3)
shows 6 topic labels for 56 rows, which is the merged-cell signature. So the set to
avoid is 3-1 .. 3-7, as the brief says.

## What this needs
**plain** only. No computation, no figure. The work is: find three real papers NOT on
the course Memory Management list, obtain the full PDFs, read them end to end, and write
a summary + critique for each. "code" is not applicable (no number is asked for);
"diagram" is not applicable (nothing to plot).

The one place where tooling matters: I must actually download and read the full papers,
and verify each citation against the paper's own title page / publisher page rather
than from memory.

## Plan
1. Pick three papers that (a) are not 3-1..3-7, (b) are recent enough to cover ground
   the 1968-2002 list does not, (c) are obtainable in full, and (d) argue with each
   other, so the critique has somewhere to stand.
2. Download PDFs into `papers/`, extract full text with pymupdf, read all of it.
3. Verify citation metadata from the PDF front matter plus the publisher/DOI page.
4. Write answer.tex: ~400-450 words per paper, 60/40 summary/critique.

## Candidate triple (production-scale memory management, 2019-2023)
- Google, "Software-defined far memory in warehouse-scale computers", ASPLOS 2019
- Meta, "TMO: Transparent Memory Offloading in Datacenters", ASPLOS 2022
- Microsoft, "Pond: CXL-Based Memory Pooling for Cloud Platforms", ASPLOS 2023
Rationale: three different answers to the same modern question (DRAM is the dominant
cost of a datacenter server), and TMO explicitly argues against the Google design, which
gives the critique real purchase instead of generic hedging.

## Selection outcome
All three downloaded and read end to end (text extracted with `scripts/extract.py`;
14 + 13 + 14 pages, references included). None is on the course list; none is Ex. 3.9's
set (3-1, 3-6, 3-4, per the sibling answer in OUTPUT/../p4/answer.tex, which I checked so
as not to duplicate its framing either).

## Citation verification
Crossref (api.crossref.org, authoritative publisher metadata) for each DOI, cross-checked
against each PDF's own title page and ACM Reference Format block. Both agree:
- 10.1145/3297858.3304053 — ASPLOS '19, Providence RI, pp. 317-330, 14 authors
- 10.1145/3503222.3507731 — ASPLOS '22, Lausanne, pp. 609-621, 11 authors
- 10.1145/3575693.3578835 — ASPLOS '23 Vol. 2, Vancouver BC, pp. 574-587, 13 authors
Crossref lowercases TMO's title; the paper's own title page uses title case, so I used
the paper's. Crossref/ACM say "Dan Ernst" on one index page but the Pond title page and
its ACM Reference Format both say "Daniel Ernst" — I used the paper.
dl.acm.org returns 403 to WebFetch, hence Crossref.

## R9 discipline — each critique claim checked against the surrounding text
- farmem: the "within noise" point uses the paper's own §2 threshold ("a few percentage
  points ... offset all potential TCO savings") and §6.4's own caveat about WSC A/B noise.
  I do NOT claim they ignored app-level metrics: §6.2 says they monitored them. The claim
  is about unstated resolution. `K`/`S` absence verified by grep (notes: lines 604/638/
  793/801/819/1069 mention them, none assigns a value).
- TMO: the "not very sensitive to these parameters" sentence is at tmo.txt:783 and the
  contradicting Config B result at tmo.txt:1332-1335. §3.3 line 787 does flag automated
  tuning as future work, so I criticised the insensitivity claim, not a missing plan.
- Pond: §7 "Robustness of ML" (pond.txt:1600-1605) DOES raise gaming — the naive critique
  would have been wrong. The real defect is that its two-sentence answer is about
  aggregate multiplexing while §4.4 (pond.txt:1181-1183) makes per-customer history the
  model's most important feature. Stranding inconsistency: pond.txt:359-360 vs 440-441.

## Length
Brief's budget: 400-450 prose words per paper, ~1,200-1,350 total.
Achieved (prose only, excluding citations and lead-in): 411 / 410 / 453.
Grand total including citations: ~1,580.

---

## Round 2 — independent re-verification (answer.tex had been edited after submission.md)

`answer.tex` was last written 14:45, `submission.md` 14:30, so the pointer file was stale.
I re-verified every load-bearing claim against `papers/*.txt` from scratch rather than
trusting it. All citation metadata re-confirmed against Crossref AND each PDF title page.

**One factual defect found and fixed.** The answer read "32--64 sockets over 180\,ns".
Pond says ">180ns for *rack-scale* pooling" (pond.txt:135); the only statement about
32--64 sockets is that they "would combine CXL switches with Pond's multi-headed EMC"
(pond.txt:642), with no latency figure. Substituting a socket count for "rack-scale" was
unsupported. Now reads "rack-scale pooling more than 180\,ns".

**One R9 strengthening.** The block-IO critique quoted the paper's own admission
(tmo.txt:626-630, "we cannot attribute a portion of a stall on block IO to the device
being oversubscribed or simply expected latency") but stopped before the paper's reply at
tmo.txt:631-632, "This has worked well for us in production across diverse workloads."
R9 says name what the source does next, so the answer now quotes that reply.

**One LaTeX defect found and fixed.** A single `\S4.1` pulled in the TS1/text-companion
font `tcrm1095`, which METAFONT must generate; `~/.TinyTeX` is read-only, so the compile
died with "Font tcrm1095 at 600 not found" *after* laying out all 3 pages. Replaced with
"Section~4.1", which also matches how the other three cross-references are written.
Fragment now compiles with nothing beyond amsmath/amssymb/graphicx/geometry, so still no
`preamble.txt`. This mattered: the master would have hit the same failure.

**Length.** Pond was 463 prose words (brief's ceiling 450). Trimmed to 452, mostly by
cutting the R8 signpost "Two ideas make pooled memory usable anyway" and the redundant
"conflates a slow backend with a loaded one". Final: 437 / 450 / 452, prose total 1,339
against the brief's 1,200-1,350.

**No-collision re-check.** PaperList.csv rows 20-26 are exactly 3-1..3-7; grepping the
whole list for far memory / offload / CXL / pool / disaggregat / warehouse hits only
6-6 (LegoOS), a different topic group and not one of mine. Sibling p4 (Ex. 3.9) used
3-1, 3-6 and 3-4 — no overlap.
