# p4 — Ex. 3.9 — validator checklist

## Round 1
Verdict: FAIL

### What I verified independently (all PASS)

- **Question.** `input/os_hw_3_problems.md:33` matches the brief verbatim. Ex. 3.9 is
  "pick three from the paper list" (Ex. 3.10 is the "search for three" variant); the
  worker answered 3.9. Correct.
- **Seven-paper claim.** Re-read `xl/worksheets/sheet1.xml` myself: `<mergeCell
  ref="C20:C26"/>`, and the six merge ranges sum to 53 = CSV data rows. 3-1, 3-4, 3-6
  are all inside C20:C26. Worker's reconciliation holds.
- **Citations.** Denning: folios 323…333, page footers read "Volume 11 / Number 5 /
  May, 1968", and ref [17] in the same issue is 313–322 — CACM 11(5):323–333 confirmed;
  the SOSP footnote reads "Gatlinburg, Tenn., October 1–4, 1967". Mach: © line
  `0-89791-238-1/87/1000-0031`, folios 31…38 over 9 PDF pages → 31–39; author list and
  order match the title page exactly (incl. "Bolosky", which the OCR mangles).
  Superpages: USENIX record confirms pp. 89–104.
- **Every number in the Results table.** Re-extracted all three PDFs with pymupdf into
  my own dir and checked each: Table 2 (C4 1.36→0.98, SP 1.19→0.98, mcf 1.68→1.22,
  best single 1.31), 18/35 >5% and 10 >25%, 3500 lines, ÷100 per decade 1986–2001,
  4–5%→30–60%, FFTW 55% in two runs, 7.2 of 8.9 pp, Mach fork 41/145 ms, compile
  23/28 s and 19 s/1:16 (= the 4:1 margin), 6K bytes, 3 weeks, four data structures,
  §3.1 "Physical memory in Mach is treated primarily as a cache for the contents of
  virtual memory objects", eq. (5), eq. (10), lσ/N vs the appendix's nτ. All correct.
  No fabricated numbers.
- **All 8 quotations** located in my own extraction (see [1.4] for one caveat).
- **R5/R4/R3.** No `\documentclass`/`\usepackage`/`document`. No labels, macros or
  figure files at all, so nothing can collide. `lint_output.py` exits 0. `downloads.md`
  lists all five fetches, including the two candidates not used.
- **Compile.** `pdflatex` inside a minimal wrapper: exit 0, zero warnings, zero
  over/underfull boxes, 4 pages (3 at the worker's 1in margins). Rendered to PNG and
  read it — clean, math sets correctly, ~1 page per paper, far over the 1/3-page floor.

### Defects

- [1.1] **Denning critique asserts an absence the paper contradicts.** "the sole
  empirical support anywhere is one sentence citing Oppenheimer and Weizer's simulation
  of the RCA Spectra 70/46" | `answer.tex:54–56` | severity: **major**
  Denning's §2 Background appeals to empirical evidence three more times: "Fine et al.
  [10] and Varian and Coffman [11] have experimental evidence to support this, namely,
  that references will be scattered over a large collection of pages"; "Their
  experiments, as well as those of Varian and Coffman [11], confirm that should there
  not be enough core memory…"; and "Belady [13] has compared some of the algorithms
  mathematically." The word "anywhere" makes the sentence false. The surrounding
  argument is sound and survives — Denning runs no experiment of his own and the
  four-policy ranking is asserted, not demonstrated — so narrow the claim to the
  ranking: e.g. "the only support offered for it is one sentence citing…". This is the
  R9 failure mode the brief flags, findable with one grep.

- [1.2] **Mach quotation truncated immediately before the clause that answers it.**
  "we are told only that such faults are ``rare enough in normal application programs''"
  | `answer.tex:107–110` | severity: **major**
  The paper's sentence continues: "…rare enough in normal application programs **that
  Mach is able to outperform a version of UNIX (IBM ACIS 4.2a) on the RT which avoids
  such aliasing altogether by using shared segments instead of shared pages.**" So the
  paper does not leave "rare enough" as a bare adjective; it offers the ACIS comparison
  as its evidence. "We are told only that…" is therefore inaccurate. The stronger and
  accurate version is already available from your own first critique paragraph: the only
  evidence for rarity is the same end-to-end comparison against ACIS that cannot
  separate `pmap` from copy-on-write, and the fault rate itself is never measured.

- [1.3] **"and then leaves it there"** | `answer.tex:113` | severity: **major**
  R9 names this exact phrasing. §3.5 does not leave it there: the sentence before the
  quote says "Mach automatically garbage collects shadow objects when it recognizes that
  an intermediate shadow is no longer needed", and the sentence after it continues —
  "Moreover, the need to allow the paging daemon to access the memory object structures,
  perform garbage collection and still allow virtual memory operations to operate in
  parallel on multiple CPUs has resulted in complex object locking rules." Note also
  that `submission.md` claims the opposite of what shipped: "Mach's §3.5 does not merely
  raise shadow chains and drop them; … The criticism is that the residual case is never
  bounded or measured, not that it is unmentioned." That is the right framing; put it in
  `answer.tex`. The rest of the sentence ("no bound on chain length, no cost, and an
  evaluation whose benchmarks all run with memory to spare") is accurate and can stand.

- [1.4] **Quotation silently re-capitalised, and the verifier checks a different
  string.** ``Sustained even under stressful workload scenarios'' | `answer.tex:157` |
  severity: minor
  The abstract reads "these benefits are **s**ustained even under stressful workload
  scenarios". As printed, the quote presents as a verbatim sentence opening that does
  not exist. Use ``[s]ustained…'' or quote the fuller clause. Separately,
  `scripts/verify_quotes.py:48` checks `'these benefits are sustained even under
  stressful workload scenarios'` — not the string in `answer.tex` — so the script's
  exit 0 does not actually cover this quotation.

- [1.5] **τ ≈ 2T presented as Denning's recommendation** | `answer.tex:29` |
  severity: minor
  §3 "Choice of τ" states the recommendation as "a value comparable to the memory
  traverse time T"; τ ≈ 2T is the worked example conditional on a chosen tolerance —
  "should we wish to limit the drop to 50 percent, we should have to choose τ ≈ 2T".
  One clause ("to hold the residency drop to 50%") makes it exact.

- [1.6] **SHA-1 rejection basis presented selectively** | `answer.tex:166` |
  severity: minor
  The answer cites the "up to 15%" microbenchmark; the same passage also reports "The
  pathological case of a large sequential read when the CPU is saturated incurs a
  worst-case degradation of 60%", which is part of the authors' stated basis. The
  criticism survives intact — the paper itself says "these overheads can be reduced
  using a variety of optimizations" and defers their evaluation to future work — but
  omitting 60% makes the rejection look thinner than the paper makes it.

### Noted, not a defect

- **Length.** My independent count: 450 / 463 / 493 per paper, 1464 body words against
  the brief's 400–450 and 1200–1350 — 8.4% over the ceiling, well inside R8's
  25%-over defect threshold. One em-dash in 1464 words (R8's symptom threshold is one
  per 70). The worker disclosed the overage accurately. The fixes above are all
  single-clause rewrites and should not add net words; [1.1] and [1.2] can shorten it.
- **Page range 89–104** flagged by the worker as inferred: independently confirmed
  against the USENIX record. Withdrawn as a concern.
- **i386 inference** (`answer.tex:151–153`), flagged by the worker as its weakest point:
  "i386" occurs exactly once in the paper, in §2.2, so "never returns to" is literally
  true, and the answer credits Table 2 as the source of the implication rather than the
  paper. Fair as written.

### Resolved since last round
(none — first round)

### Still outstanding
[1.1] [1.2] [1.3] [1.4] [1.5] [1.6]

## Round 2
Verdict: PASS

### Resolved since last round

- [1.1] **FIXED.** Now: "No experiment here tests the ranking. Denning does lean on
  measurement elsewhere, invoking Fine et al. and Varian and Coffman in Section~2, but
  the ranking itself rests on one sentence of the conclusion citing Oppenheimer and
  Weizer…". I checked the attribution by offset: §2 spans idx 6817–16913 in my
  extraction, and all three empirical citations (Fine/Varian at 13833, "Various studies
  concerning behavior" at 15623, Belady at 16312) fall inside it, so "Section~2" is
  right. The O&W sentence is in §7 Conclusions, so "one sentence of the conclusion" is
  right. The false "anywhere" is gone and the surviving argument is the accurate one.
- [1.2] **FIXED.** Now: "…the evidence that these faults stay ``rare enough in normal
  application programs'' is again an end-to-end win, over IBM's ACIS~4.2a, which no more
  separates that cost than the fork figures do. The fault rate itself is never reported."
  The truncated clause is restored as the paper's own justification, and the criticism is
  rebuilt on it rather than on a pretended absence. Section~5 is the correct location.
- [1.3] **FIXED.** "leaves it there" is gone. Now states that Mach does collapse chains
  ("garbage-collecting a shadow once the intermediate is recognised as redundant"), that
  the authors are candid the collector is incomplete, and — the R9 requirement — what the
  paper does next: "The discussion turns from there to that collector's locking rules".
  That matches §3.5's "Moreover, the need to allow the paging daemon … has resulted in
  complex object locking rules." "Main source of complexity" matches "Most of the
  complexity of Mach memory management arises from…". The residual criticism (no bound,
  no cost, benchmarks run with memory to spare) is unchanged and still accurate.
- [1.4] **FIXED, both halves.** The quote is now ``these benefits are sustained even
  under stressful workload scenarios'', verbatim and attributed to the abstract. And
  `scripts/verify_quotes.py` was genuinely rewritten to parse the quotations out of
  `answer.tex` itself rather than from a hand-maintained list; it now checks 11 strings
  (3 titles + 8 prose) and exits 0. I ran it, and separately re-ran my own normaliser
  against my own pymupdf extraction — both agree, all 11 verbatim.
- [1.5] **FIXED.** Now: "he recommends a τ comparable to the traverse time T, τ≈2T being
  the value that holds the resulting drop in page residency to 50\%." Exactly what §3
  says.
- [1.6] **FIXED.** Now: "…costing up to 15\%, and 60\% on a saturated sequential read".
  Matches "The pathological case of a large sequential read when the CPU is saturated
  incurs a worst-case degradation of 60%."

### Checked for regressions introduced by the fixes (none found)

The edits also rewrote some text I had not objected to, so I re-verified the new claims:

- "mapped files" (new, Mach summary) — supported: §3.3, "to implement a memory mapped
  file, virtual memory is created with its pager specified as the file system."
- "external pagers running as ordinary user tasks" — "A pager may be either internal to
  the Mach kernel or an external user-state task."
- "charged with 7.2 of the adversary's 8.9 percentage points" — unchanged in substance,
  still matches §6.6.
- Re-ran the unchanged numeric claims (fork 41/145 ms, 23/28 s and the 4:1 margin,
  Table 2's four speedups, 18/35 and 10/35, 3500 lines, 55% in two runs): all still
  correct.
- Compile: `pdflatex` in a minimal wrapper, exit 0, zero warnings, zero over/underfull
  boxes, 4 pages; rendered all four to PNG and read them — clean, no overlap or
  clipping. `lint_output.py` exits 0. No `\documentclass`/`\usepackage`/`document`, and
  still zero labels, macros and figure files, so nothing can collide with another
  problem. `downloads.md` unchanged and complete.

### Still outstanding

- **Length, noted and not failed.** My independent count is 1545 body words (worker
  reports 1542) against the brief's 1200–1350 — 14% over the ceiling, up from round 1's
  1464. Per paper: 477 / 509 / 501 against 400–450. This is inside R8's explicit
  25%-over defect threshold (~1688), and the increase is traceable line-for-line to the
  three R9 fixes this round demanded: replacing an asserted absence with what the source
  actually does next is necessarily longer than the false short version. The worker
  reported the overage and its direction honestly rather than burying it. If a further
  round is ever spent on this problem, the Mach critique (509) is the place to trim; I
  am not spending one on it, because another edit pass risks the correctness
  regressions that this round only narrowly avoided.
- Minor bookkeeping: `submission.md`'s Results table still lists "recommended τ | ≈ 2T"
  rather than the corrected phrasing now in `answer.tex`. Does not affect the
  deliverable.

Nothing substantive remains. Passing.
