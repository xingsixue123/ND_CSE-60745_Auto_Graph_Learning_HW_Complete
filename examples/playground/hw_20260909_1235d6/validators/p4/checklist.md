# Validator checklist — p4 (Ex. 1.0, three papers on OS History and Architecture)

## Round 1
Verdict: FAIL

### What I verified independently (all passed)

- **Question text.** `input/hw_questions.md` line 41 matches the brief verbatim, including
  the `Ex. 1.0` label. No discrepancy. Source is a `.md`, so there is no page-image or
  figure channel for the assignment itself — the worker's R7 note is correct.
- **Exclusion boundary.** `ingest/csv/PaperList.csv`: row `1-1` carries the topic
  `OS History and Architecture`, rows `1-2`..`1-11` blank (merged cell), `2-1` begins
  `Scheduling`. Off-limits group is exactly 1-1..1-11. None of the three chosen papers is
  in it, and none is one of Ex 1.9's three.
- **Papers really downloaded and readable.** All three PDFs present in `papers/` with
  `pdftotext` extractions. `downloads.md` records all three with source URLs (R3 satisfied).
- **Every text-sourced number in `answer.tex`** — re-grepped in the extractions, 15/15 exact:
  quarter-million segments/words (`multics:204`), 64/1024-word pages (`:191`), "few hundred"
  / "simple scaling" / "hazardous" (`:410-411`), "retrogressed" (`:37`), "fire-walls" +
  execute-only bit (`:232`), "no clear-cut demarcation" (`:222`), "the supervisor does not
  have a special processor" (`:145`), mailboxes (`:174`), three named backup contingencies
  (`:336-341`), delegable budgets (`:306`), on-line reference manual (`:384`), six-paper
  session ("companion papers[1-5]", `:21`); Mach 0.7 ms/1024 B vs ~1.2 ms 4.3BSD and
  "extensive performance comparisons ... have not yet been done" (`mach:651-657`), threads
  "expected by Summer 1986" (`:702`), 512-byte VAX MD page (`:344`), 24 MB message (`:507`),
  "staggering number"/"mind-boggling array" (`:71,74`), "a function of its servers rather
  than its kernel" (`:117`), shared/copy/none inheritance and lower-only max protection
  (`:240,252-256`); Multikernel 6000 lines/58 files/"heroic" (`:157`), 7135 C + 337 asm
  (`:765`), <30 cycles vs ~12,000 extra (`:332-334`), capabilities "a mistake" (`:941`),
  "wrong to draw any quantitative conclusions" (`:1861`), "complete system is a failure
  unit" (`:1908`), "very much a placeholder" (`:1178`), offload tuning + 18697 vs 8924
  req/s (`:1826-1833`), 951.7 Mbit/s UDP (`:1781`), Table 4 loopback 2154/1823 Mbit/s and
  21/77 Dcache misses per packet (row labels confirmed at `:1379-1384`), "several thousand
  cycles" for the CPU-driver/monitor split (`:1131`).
- **Table 3.** Re-read: URPC 450 cycles / 3.42 msgs-per-kcycle / 9 Icache + 8 Dcache lines;
  L4 IPC 424 / 2.36 / 25 + 13. Exactly as claimed. (It is in fact text-extractable, just
  column-interleaved — the submission overstates this as visual-channel-only, harmless.)
- **Figure 6, re-rendered myself** at 300 dpi from page 13 and cropped/upscaled. At 32 cores:
  NUMA-aware multicast ~3.15k, multicast ~4.8k, unicast ~12.7k, broadcast ~13.8k. All four
  match the answer.
- **Figure 7, re-rendered myself.** At 32 cores: Barrelfish ~17.5k, Linux ~29.5k, Windows
  ~46k. Matches. **At 2 cores it does not** — see defect 1.1.
- **LaTeX.** No `\documentclass` / `\usepackage` / `document` environment (R5 ok). All five
  labels namespaced `p4:`. No ASCII `"` (the one grep hit is the `\"u` umlaut in
  `Sch\"upbach`). Compiled inside two wrappers of my own: `article`+`geometry` and a bare
  `article` with zero packages — both exit 0, 5 pages, **0 overfull/underfull boxes**. The
  absence of `preamble.txt` is therefore correct, not an omission.
- **OUTPUT clean.** `python3 framework/tools/lint_output.py output/.../p4` → `OUTPUT LINT OK`,
  exit 0. Only `answer.tex` present.
- **Length.** My own count: 2952 words total — intro 178, Multics 729, Mach 832, Multikernel
  828, comparison 268, references 117. Each paper clears the ~300–400 word floor about 2×.
  Both required halves (Summary / Critical judgment) present for all three. House style
  matches the described Ex 1.9 shape.

### Defects

- **[1.1] Figure 7 misread: Barrelfish's 2-core data point is Linux's, and the conclusion
  drawn from it is inverted.** | `OUTPUT/answer.tex` lines 191–193 (and its source,
  `notes.md:90`) | severity: **blocking**

  The answer states Barrelfish's unmap curve rises "from roughly 5.5k cycles at two cores,
  merely with a gentler slope than Linux's", and concludes "The multikernel reduced the
  constant; it did not remove the scaling term."

  I re-rendered page 13 of `multikernel_sosp2009.pdf` at 300 dpi and cropped the x ∈ [2,8]
  region of Figure 7 at high magnification. Per the legend (Windows = `*`, Linux = `□`,
  Barrelfish = `+`, Barrelfish being the only solid line), at 2 cores:

      Barrelfish  ~10.3k cycles   (flat from cores 2 through 5)
      Linux        ~5.2k cycles
      Windows      ~5.8k cycles   (crosses above Barrelfish at ~5 cores)

  So ~5.5k is **Linux's** point, not Barrelfish's. `notes.md:90` records
  "(Barrelfish ~5.5k, Linux ~5k, Windows ~10k)" — Barrelfish and Windows were swapped at the
  left edge of the plot, and the error propagated verbatim into the deliverable.

  This is not just a wrong number; it reverses the criticism. Corrected:
  Barrelfish 10.3k → 17.5k is **1.7×** over 2→32 cores, while Linux 5.2k → 29.5k is **5.7×**.
  The multikernel did not "reduce the constant" — it roughly **doubled** it, and bought a
  much flatter slope with it. That is precisely the trade the paper itself concedes at
  `multikernel_sosp2009.txt:1131` ("adding a constant overhead on current hardware of several
  thousand cycles. However, this is constant as the number of cores increases"), which the
  answer already cites two sentences later — so as written the paragraph now contradicts
  itself.

  Fix: either restate with the correct readings and re-aim the criticism at the fixed cost
  (Barrelfish is the *slowest* of the three below ~5 cores, paying ~2× Linux's constant for
  the CPU-driver/monitor split, and only wins past ~13 cores), or delete the clause. Note
  that the paper's own text at `:1364` already attributes the gap to "inefficiencies in the
  message dispatch loop of the user-level threads package", so the ">four-fifths is
  Barrelfish's own overhead" claim in the preceding clause survives and should be kept.

- **[1.2] "``multiprocessor'' is the first word of the abstract" is false.** |
  `OUTPUT/answer.tex` line 118 | severity: minor

  The abstract opens "Mach is a multiprocessor operating system kernel and environment under
  development at Carnegie Mellon University" (`mach_usenix1986.txt:10`). The first word is
  "Mach"; "multiprocessor" is the fourth. The rhetorical point is sound — replace with
  "the abstract's opening sentence" or "the first line of the abstract".

- **[1.3] Page-count provenance is wrong for the Multics PDF.** | `submission.md:56`,
  `downloads.md:6` | severity: minor

  Both assert 8 pages and that "`pdfinfo` is correct — 8 / 16 / 20". `pdfinfo
  multics_fjcc1965.pdf` reports **10** pages (16 and 20 for the other two are right). Does
  not affect the deliverable, but the submission presents this as a verified cross-check.

### Notes (not defects, no action required)

- The worker flagged PaperList row `3-3` (Multics Virtual Memory) as the near-miss on its
  Paper 1. It missed a closer one on Paper 2: row **`3-6`** is Rashid et al.,
  "Machine-Independent Virtual Memory Management for Paged Uniprocessor and Multiprocessor
  Architectures" — the Mach VM paper — and the answer's Mach summary leans heavily on exactly
  that subject (external pagers, MD/MI split, `pmap`). It sits in the *Memory Management*
  group, outside the stated exclusion (1-1..1-11), and Accetta et al. 1986 is a different
  paper, so I am **not** overturning the selection. Worth being aware of.
- The Liedtke (list paper 1-8) mention in the Mach judgment is one sentence of historical
  context and is not in the reference list. I agree with the worker that this is in bounds.
- Table 1 (LRPC) arithmetic re-checked: 845/2.66=318, 757/2.8=270, 1463/2.5=585,
  1549/2.0=774 ns. Self-consistent, and not relied on in the answer.

### Resolved since last round
(none — first round)

### Still outstanding
- [1.1] blocking
- [1.2] minor
- [1.3] minor

## Round 2
Verdict: PASS

### Re-verification of the round-1 defects (all independently re-measured, not taken on trust)

- **[1.1] blocking → RESOLVED.** `answer.tex:188–205` rewritten. I re-cropped my own 300 dpi
  render of page 13 at two new magnifications rather than reusing the round-1 crop. The new
  text now matches measurement on every value: Barrelfish ~10.3k at 2 cores, flat to ~5 cores,
  vs Linux ~5.2k and Windows ~5.8k; at 32 cores 17.5k / 29.5k / 46k; growth 1.7× / 5.7× / 7.9×
  (arithmetic checks: 17.5/10.3=1.70, 29.5/5.2=5.67, 46/5.8=7.93). The conclusion is now the
  right way round — "did not reduce the constant cost ... roughly *doubled* it and bought a
  much flatter curve" — and it is correctly tied to the authors' own concession at
  `multikernel_sosp2009.txt:1128–1131`, which I re-read: "adding a constant overhead on
  current hardware of several thousand cycles. However, this is constant as the number of
  cores increases." Both quoted fragments are verbatim.
  - The unraised improvement is also correct: I cropped x ∈ [4,17] with the axis ticks
    visible. Barrelfish (`+`, solid) runs above Linux (`□`) through core 11, the two are
    coincident at 12–13, and Linux is clearly above from 14 on. "Around twelve or thirteen
    cores" is right; the round-1 note's "12–16" was indeed loose.
  - The Summary paragraph was updated in step (`:168–169`, 17k → 17.5k, 29k → 29.5k), so
    summary and judgment no longer disagree. `grep` for the stale phrasings
    (`5.5k`, `reduced the constant`, `scaling term`, `about 17k`, `gentler slope`) returns
    nothing.
  - "More than four-fifths" still holds against the revised denominator: 3.1/17.5 = 17.7%,
    leaving 82.3%.

- **[1.2] minor → RESOLVED.** `answer.tex:118–119` now reads "the abstract's opening sentence
  announces a ``multiprocessor operating system kernel''", which is exactly what
  `mach_usenix1986.txt:10` says.

- **[1.3] minor → RESOLVED.** `downloads.md:6` now says 10 reflowed pages; `submission.md:94`
  now says 10 / 16 / 20. Matches `pdfinfo`.

- **PaperList `3-6` note** — acknowledged and moved into the submission's "least confident"
  list rather than left buried. Selection stands, as I ruled in round 1.

### Additional checks this round (nothing found)

- **No regressions elsewhere.** Only three regions changed. Everything I verified in round 1
  is byte-identical or consistent; all 15 text-sourced numbers still present and unaltered.
- **Claims I had not yet checked in round 1, now checked and correct:** UDP echo "951.7
  against 951 Mbit/s" — Linux's 951 confirmed at `multikernel:1783`; "one dedicated RPC server
  sustains twice the update rate of all 16 shared-memory threads together" — `:372`, "twice as
  many updates per second as all 16 shared-memory threads combined"; "one-phase commit for
  unmapping a page, two-phase commit for capability retyping" — `:1038` and `:1048`, exactly
  as stated; SKB holding hardware facts "in a subset of first-order logic" — `:1065`.
- **Compile.** Rebuilt in my own two wrappers: `article`+`geometry` and bare `article`, both
  exit 0, **0 overfull/underfull boxes**, no errors. 5 pages under geometry (7 under bare
  article's wider default margins — expected, not a defect).
- **R5 / namespacing.** No `\documentclass` / `\usepackage` / `document` environment. All five
  labels still `p4:`-prefixed. No `\includegraphics`, no absolute paths, no ASCII `"`.
- **Lint.** `lint_output.py` → `OUTPUT LINT OK`, exit 0. OUTPUT contains only `answer.tex`.
- **Length.** Recounted: 3083 words — intro 178, Multics 729, Mach 834, Multikernel 957,
  comparison 268, references 117. The Multikernel section grew by ~130 words with the rewrite.
  Still comfortably over the ~300–400 word floor per paper; both required halves present.
- **downloads.md** complete and accurate (R3).

### Resolved since last round
- [1.1] blocking — Figure 7 misread and inverted conclusion
- [1.2] minor — "first word of the abstract"
- [1.3] minor — Multics PDF page count

### Still outstanding
None. The one residual is inherent, not a defect: Figures 6 and 7 have no published data
table, so their values are graph reads good to roughly ±0.5k cycles. The worker states this
exposure explicitly and hedges every such number with "about"/"roughly"/"some" in the answer,
and the qualitative claims that carry the argument are unambiguous at 300 dpi. That is the
right way to handle it.
