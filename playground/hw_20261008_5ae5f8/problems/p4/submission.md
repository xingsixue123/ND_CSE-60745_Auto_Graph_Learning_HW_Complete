# p4 — Ex. 3.9 (20 pts) — submission

## What the problem asked

> Ex. 3.9 | (20pts) Pick three papers from 'Memory Management' in the paper list.
> Read, summarize, and critically judge them. Write at least 1/3 page for each
> paper's summarization and judgment.

The brief and the assignment text (`input/os_hw_3_problems.md`) agree verbatim; the
only difference is typographic (the markdown uses curly quotes). **No discrepancy.**

I re-derived the brief's claim about the paper list rather than taking it on trust,
and it holds. Four channels:

| channel | what it says |
|---|---|
| `ingest/csv/PaperList.csv` | rows 3-1…3-7; topic cell filled only on 3-1 (merged-cell flattening) |
| `pages/PaperList/page_003.txt` | column-major; 3-6's title is dumped out of order at the page bottom, making the block look like **six** papers |
| `pages/PaperList/page_005.png` | shows `Memory Management` as one tall merged block |
| `input/PaperList.xlsx` → `xl/worksheets/sheet1.xml` | `<mergeCell ref="C20:C26"/>` — **seven** rows |

Invariant check: the six `mergeCell` ranges are C2:C12, C13:C19, C20:C26, C27:C36,
C37:C46, C47:C54 — 11+7+7+10+10+8 = 53, exactly the number of data rows in the CSV.
So the merges partition the list and Memory Management has seven papers. The text
channel is the misleading one and I trusted the CSV + the merge ranges over it.

## What I decided it needed

**plain.** No computation and no figure: the deliverable is three citations, three
summaries and three critiques. The only "computed" artefacts are the word counts
(R8 is a hard constraint here) and the quotation checks (R9).

## What I did

Chose papers **3-1, 3-6 and 3-4** — a theory paper, a kernel-structure paper and a
modern measurement paper — so the three answers connect rather than repeat. Downloaded
each as a full PDF, extracted the text with pymupdf, and read each one end to end,
including appendices and reference lists. Verified every citation against Crossref
rather than reciting it: Crossref confirmed Denning's CACM volume/issue/pages, the
ASPLOS II pagination for Mach, and the OSDI '02 author list and start page for
superpages. (The spreadsheet's title for 3-6 is truncated and its title for 3-2 is a
typo for WSCLOCK; neither typo is reproduced in the answer, and the answer says so.)

For each critique I located the passage in the paper where the issue is raised,
then read **past** it to see what the authors do with it, and framed the criticism
around what they do rather than around an omission. Three places where that changed
the answer:

- Denning does discuss sharing and calls the charging question "still an open
  question, and is under investigation", so I do not accuse him of ignoring it.
- Mach's §3.5 does not merely raise shadow chains and drop them; it garbage-collects
  them and then states the residual case it cannot detect. The criticism is that the
  residual case is never bounded or measured, not that it is unmentioned.
- The superpages authors explicitly acknowledge that demote-on-write denies
  superpages to sparse writers. The criticism is aimed at the alternative they
  discarded (SHA-1 digests), which they rejected on an unoptimised microbenchmark and
  then, in the same paragraph, named two optimisations for and deferred to future work.

**Round 1 got two of those three wrong in the shipped text**, in the exact way R9
describes. See "Round 2" below. The analysis in this section was right; `answer.tex`
did not match it.

## Intermediate steps and code

Paths relative to PLAYGROUND.

| path | what it does |
|---|---|
| `papers/*.pdf` | the three papers (plus two candidates not used), downloaded; see `downloads.md` |
| `papers/*.txt` | per-page text extracted with pymupdf; what I read and quoted from |
| `scripts/wordcount.py` | strips LaTeX and reports words per paper, summary/critique split, em-dash density. Run: `python3 scripts/wordcount.py <OUTPUT>/answer.tex` |
| `scripts/verify_quotes.py` | **rewritten in round 2.** Parses the quotations out of `answer.tex` itself and checks each against the extracted paper text (de-hyphenated, fi/fl ligatures normalised). Prose quotes must match contiguously; citation titles are matched word-in-order, because the two-column scans split Denning's title across the gutter. Run: `python3 scripts/verify_quotes.py` (exits non-zero on any miss) |
| `build/test.tex`, `build/pg-*.png` | compile harness; `pdflatex` the fragment inside a minimal article and render to PNG |
| `notes.md` | channel reconciliation and plan |

Merge-range check (the seven-paper invariant) was a one-liner:

    python3 -c "import zipfile,re; s=zipfile.ZipFile('<INPUT>/PaperList.xlsx').read('xl/worksheets/sheet1.xml').decode(); print(re.search(r'<mergeCells.*?</mergeCells>',s,re.S).group(0))"

## Results

Every number in `answer.tex` is read from the paper named, not computed by me.

| claim in answer.tex | value | source |
|---|---|---|
| Denning, CACM volume/issue/pages | 11(5):323–333, May 1968 | paper folios 323…333 + Crossref `10.1145/363095.363141` |
| Denning first presented at SOSP | Gatlinburg TN, Oct 1967 | footnote on paper p.1 |
| working-set reentry rate | λ(τ)=[1−F_x(τ)]/x̄ | eq. (10), `denning_ws_1968.txt` |
| concavity bound | ω(t,2τ) ≤ 2ω(t,τ) | eq. (5) |
| recommended τ | ≈ 2T | §3, "Choice of τ" |
| sampling skew | lσ/N, not σ | p.8; appendix gives the matching nτ correction for the hardware timer only |
| Mach pages | ASPLOS II, Oct 1987, pp. 31–39 | paper folios 31…39, © line `…/87/1000-0031`, Crossref `10.1145/36205.36181` |
| Mach fork 256K, RT PC | 41 ms vs 145 ms | Table 7-1 |
| Mach compile, 400 buffers | 23 s vs 28 s (generic: 19 s vs 1:16) | Table 7-2 |
| MD module size | ≈ 6K bytes on a VAX | §9 |
| RT PC pmap effort | ≈ 3 weeks | §4 |
| Superpages citation | OSDI '02, Boston, Dec 2002, pp. 89–104 | Crossref `10.1145/1060289.1060299` gives authors + start page 89; the paper body is 16 pp → 89–104 |
| TLB coverage trend | ÷100 per decade, 1986–2001 | §2.1 / Fig. 1 |
| TLB miss cost | 4–5% (1980s) → 30–60% | §2.1 |
| benchmark gains | 18/35 over 5%, 10 over 25% | §6.3 |
| mcf multi-size vs best single | 1.68 vs 1.31 | Table 2 |
| single-size collapse | C4 1.36→0.98, SP 1.19→0.98, mcf 1.68→1.22 | Table 2 ("All" vs "4MB" columns) |
| FFTW after fragmentation | 55% speedup within two runs | §6.5 |
| PTE-replication share of adversary overhead | 7.2 of 8.9 percentage points | §6.6 |
| implementation size | 3500 lines | §6.1 |

Length (R8), from `scripts/wordcount.py`, excluding headings and citation lines:

    paper 3-1   summary 255  critique 219  total 474   (54/46)
    paper 3-6   summary 264  critique 245  total 509   (52/48)
    paper 3-4   summary 255  critique 246  total 501   (51/49)
    intro 58                       BODY TOTAL 1542
    em-dashes: 1 in 1542 words

Against the brief's 400–450/paper and 1200–1350 total: 14% over the ceiling, inside
R8's 25% defect threshold (1688) but up from round 1's 1464. I am not hiding the
direction of travel: the three R9 fixes added 117 words, because each one replaced an
asserted absence with what the paper actually does next, and that is strictly more
text than the false shorter version. A trim pass then took 1581 back to 1542. I
stopped there rather than cut further, because what remains is quotes, section
numbers and table values; cutting more would start removing the anchoring that the
R9 fixes exist to supply.

Quotations: `scripts/verify_quotes.py` → 11 checked (3 titles, 8 prose), all verified
verbatim, exit 0.

Compile: `pdflatex` on the fragment inside a minimal article exits 0, no warnings,
3 pages — about one page per paper, comfortably over the assignment's 1/3-page floor.
`lint_output.py` on OUTPUT: OK.

## Deliverables

- `<OUTPUT>/answer.tex` — the fragment. No `\documentclass`, no `\usepackage`, no
  `document` environment; starts at `\section*{Ex.~3.9 …}`.
- No figures (the question needs none).
- No `preamble.txt`: the fragment uses only base LaTeX plus what amsmath/amssymb
  already provide, which the brief lists as assumed.

Namespacing: the fragment defines no labels, no macros and no figure files, so there
is nothing that can collide with another problem.

## Round 2 — validator defects and what I changed

The validator was right on all six. I re-checked each against my own extraction before
touching the text, rather than taking the report on faith; all six reproduce.

| # | defect | fix |
|---|---|---|
| 1.1 | "the sole empirical support **anywhere**" — false. §2 invokes Fine et al.\ and Varian & Coffman's experiments twice ("have experimental evidence to support this"; "Their experiments … confirm that…") and Belady's comparison. | Narrowed to the ranking, which is what the argument actually needs: "Denning does lean on measurement elsewhere, invoking Fine et al.\ and Varian and Coffman in Section 2, but the ranking itself rests on one sentence of the conclusion citing…" |
| 1.2 | "we are told **only** that such faults are 'rare enough…'" — the sentence continues "…**that Mach is able to outperform a version of UNIX (IBM ACIS 4.2a) on the RT**". The quote was cut exactly where the paper gives its justification. | Rewritten to name that justification and say why it is weak, which also ties the point back to the first critique paragraph: the ACIS result "is again an end-to-end win … which no more separates that cost than the fork figures do. The fault rate itself is never reported." |
| 1.3 | "**and then leaves it there**" — R9 names this phrasing. §3.5 says Mach garbage-collects shadow objects, and the next sentence carries the discussion into the locking rules. | Rewritten to state what §3.5 does: Mach "does collapse them, garbage-collecting a shadow once the intermediate is recognised as redundant", the authors are candid the collector is incomplete, and "the discussion turns from there to that collector's locking rules, leaving the admitted residue with no bound on chain length and no cost". |
| 1.4 | ``Sustained even under stressful workload scenarios'' silently re-capitalised; and `verify_quotes.py` checked a *different* string, so its exit 0 did not cover this quote. | Quote the abstract's clause as written: "The abstract's ``these benefits are sustained even under stressful workload scenarios''". **And fixed the root cause** — the verifier no longer has a hardcoded list; it parses quotations out of `answer.tex`, so what is checked is always what ships. |
| 1.5 | τ ≈ 2T stated as the recommendation; §3 says "a value comparable to the memory traverse time T", with 2T the example conditional on a 50% tolerance. | "he recommends a τ comparable to the traverse time T, τ ≈ 2T being the value that holds the resulting drop in page residency to 50%." |
| 1.6 | SHA-1 rejection cited at "up to 15%", omitting the 60% worst case from the same passage. | "costing up to 15%, and 60% on a saturated sequential read". The criticism is unchanged and survives: the paper itself says those overheads "can be reduced using a variety of optimizations" and defers evaluating them. |

Defect 1.4 was the useful one, because it was a process failure rather than a wording
failure: a verifier that checks a hardcoded copy of a quotation cannot catch the
quotation drifting. The rewritten script would have failed round 1.

Also in round 2: split a 140-word Mach critique paragraph in two, and re-ran everything.

Re-verification after the fixes: `pdflatex` exit 0, zero warnings, zero over/underfull
boxes, 3 pages. `lint_output.py` exit 0. `verify_quotes.py` 11/11, exit 0. Rendered all
three pages to PNG and read them to confirm the shipped text matches the intent — the
round-1 renders were stale at one point and I nearly checked the wrong thing.

## Where I am least confident

1. **Length.** 1542 against a 1200–1350 target, up from 1464 in round 1. Inside R8's
   threshold, but the direction is wrong and the responsibility is mine: the R9 fixes
   cost words, and I chose accuracy over brevity each time. If a third round wants it
   shorter, the superpages "sustained even under stressful workload scenarios"
   paragraph (48 words) is the one I would drop first — it is the weakest of that
   paper's three critique points.
2. **The i386 inference in the superpages critique.** The paper never runs on i386; I
   use its own Table 2 "4MB-only" column as a proxy for a two-page-size machine. The
   validator examined this and judged it fair as written, but it remains the one place
   I argue beyond what the paper states.
3. **Choice of three.** Picked for coverage and for availability of full text. 3-2
   (WSCLOCK) would have paired more tightly with Denning; I stopped searching for it
   once three full PDFs were in hand rather than establish it was unobtainable.
4. **OCR fidelity of the two scanned papers.** Denning (1968) and Mach (1987) are
   scans and the extraction is noisy ("Math" for "Mach", mangled equations). Every
   quoted string is re-checked by `verify_quotes.py` against that extraction, but the
   extraction is the scan's OCR, not the printed page. All quoted passages read
   cleanly, and the validator independently re-extracted and matched them, so I do not
   think any is an OCR artefact.
5. **Withdrawn since round 1.** The superpages page range 89–104, which I flagged as
   inferred, was independently confirmed against the USENIX record.
