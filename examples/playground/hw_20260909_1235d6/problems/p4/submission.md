# p4 — Ex. 1.0 — submission

> ## Round 1 corrections (validator FAIL → resubmit)
>
> **[1.1] blocking — accepted, and the validator was right.** I re-rendered Figure 7 at
> 300 dpi myself before touching anything. Confirmed: at two cores the `+`/solid Barrelfish
> curve sits at **~10.3k cycles and is flat to five cores**; the ~5.2k point is Linux's `□`
> and ~5.8k is Windows' `*`. I had swapped Barrelfish and Windows at the left edge.
> Growth 2→32 cores is Barrelfish 1.7× (to ~17.5k), Linux 5.7× (to ~29.5k), Windows 7.9×
> (to ~46k). The conclusion inverts: the multikernel did **not** reduce the constant, it
> roughly **doubled** it and bought a flatter slope — which is precisely the trade the
> authors concede at `multikernel_sosp2009.txt:1128` ("a constant overhead ... of several
> thousand cycles", "constant as the number of cores increases"), a sentence my own
> paragraph quoted two lines later while asserting the opposite. Rewritten at
> `answer.tex:188–205`.
> *Root cause:* I read Fig 7 from a **150 dpi** render. At that resolution the three markers
> at x=2 are a few pixels apart and the legend glyphs are unresolvable; 4× LANCZOS upscaling
> cannot recover glyph identity that was never sampled. Re-rendering at 300 dpi separates
> them cleanly. Logged as an erratum in `notes.md`.
> *While fixing I also tightened one claim the validator did not raise:* the Linux crossover
> is at ~12–13 cores, not the "12–16" I first estimated — verified in `papers/fig7_mid.png`.
>
> **[1.2] minor — accepted.** The Mach abstract opens "Mach is a multiprocessor operating
> system kernel", so "the first word of the abstract" was wrong. Reworded to "the abstract's
> opening sentence announces a ``multiprocessor operating system kernel''" (`answer.tex:118`).
>
> **[1.3] minor — accepted.** `pdfinfo` reports the Multics PDF as **10** pages, not 8. My
> "8" was `file`'s wrong number leaking through, because my `pdfinfo | head -12` truncated
> before the `Pages:` line for that one file. Fixed in `submission.md`, `downloads.md` and
> `notes.md`. The other two counts (16 / 20) were right.
>
> **Validator's "note, no action" re PaperList `3-6`** (Rashid et al., machine-independent
> VM for paged uniprocessor and multiprocessor architectures — the Mach VM paper): agreed,
> and it is a closer near-miss than the `3-3` I flagged, since my Mach summary does lean on
> the VM design. Both sit outside the stated exclusion (1-1..1-11) and both are different
> papers from my 1986 Accetta et al. system paper. I have added it to the "least confident"
> list below so the risk is recorded rather than buried.
>
> Re-verified after editing: compiles clean under `article`+geometry+amsmath **and** under a
> bare `article` with zero packages; 5 pages; **0 overfull/underfull boxes**; lint OK.

## What the problem asked

> Ex. 1.0 (30pts) | Search for three papers on the topic of 'OS History and Architecture'.
> Read, summarize, and critically judge them. Write at least 1/3 page for each paper's
> summarization and judgment. (10pts for each paper)

**The brief and the assignment source agree verbatim** — no discrepancy to report. I checked
`input/hw_questions.md` line 41 directly; it matches the brief's transcription character for
character, including the `Ex. 1.0` label (a typo for 1.10, kept as-is per the brief).

R7 note: the assignment source for this problem is a plain `.md` file, not a PDF. The ingest
manifest classifies it `kind: text_document` with no rendered pages and no figures, so there
is no page-image or figure channel to reconcile — I read the original input file. My problem
refers to no figure. (The three-channel discipline *was* applied to the downloaded papers;
see below.)

I independently re-verified the exclusion boundary two ways rather than taking the brief's
word for it:
- `ingest/csv/PaperList.csv` — row `1-1` carries the topic `OS History and Architecture`,
  rows 1-2..1-11 are blank (merged cell), and row `2-1` begins `Scheduling`.
- `ingest/pages/PaperList/page_001.png` — the green colour band covers exactly rows 1-1
  through 1-11, and a new blue band starts at 2-1.
Both agree: the off-limits group is exactly 1-1..1-11. None of my three papers is in it.

## What I decided it needed

**plain only.** No code, no diagram. Nothing is computed and nothing is plotted; the question
asks for reading, summary and judgment. The one thing that made this question real work was
the instruction to actually find and read the papers rather than write from memory of titles.

## What I did

Searched the literature with WebSearch (three separate searches, one per candidate),
downloaded all three full texts by `curl` into `papers/`, and read each end to end. I chose a
set with an argument running through it: three successive answers to *what may the OS assume
about the machine, and where should OS function live?* — Multics 1965 (one maximal system on
symmetric shared memory) → Mach 1986 (decompose it into a minimal kernel plus user servers) →
Multikernel 2009 (abandon shared memory as the organising assumption). A secondary thread
emerged while reading and became the closing paragraph: the three show a steady rise in
evidentiary standards with no matching fall in the confidence of the architectural claim.

For each paper I wrote the summary from the mechanisms actually named in the text, and built
the critical judgment around what the paper's own evaluation does and does not demonstrate.
The sharpest criticisms are grounded in numbers I extracted myself (see Results).

**Three-channel reading of the papers.** Full `pdftotext` for all three. For the Multikernel
paper the graphs vanish and the tables interleave their columns under text extraction, so I
rendered pages 10 and 13 at 150 dpi with `pdftoppm`, cropped and upscaled 4× LANCZOS with
PIL, and read Figures 6 and 7 and Tables 2/3 visually. Two of my strongest criticisms come
only from that visual channel and are invisible in the text channel.

Incidental trap worth flagging: `file` misreports the page counts of all three PDFs
(6/8/6 pages). `pdfinfo` is correct — **10 / 16 / 20**. I nearly re-downloaded on the
assumption the files were truncated; they are complete.

## Intermediate steps and code

No analysis scripts — this is a prose answer. The reproducible commands are:

- `papers/` — the three downloaded PDFs plus `pdftotext` extractions (`*.txt`). Downloads and
  their source URLs are recorded in `downloads.md`.
- Text extraction: `cd papers && pdftotext <name>.pdf <name>.txt` (all three).
- Figure/table verification (Multikernel):
  - `pdftoppm -r 150 -f 10 -l 10 -png multikernel_sosp2009.pdf mk_p10` → crop + 4× LANCZOS
    → `papers/tab23_zoom.png` (Tables 2 & 3; text is legible at 150 dpi).
  - `pdftoppm -r 150 -f 13 -l 13 -png multikernel_sosp2009.pdf mk_p13` → `papers/fig6_zoom.png`
    (Fig 6, shootdown protocols) and `papers/fig7_zoom.png` (Fig 7) — **the 150 dpi Fig 7 crop
    is the one that produced defect 1.1; superseded, kept only as evidence of the error.**
  - `pdftoppm -r 300 -f 13 -l 13 -png multikernel_sosp2009.pdf mk_p13_hi` → `papers/fig7_hi.png`
    (full Fig 7), `papers/fig7_leftedge.png` (x∈[2,10], marker identity), `papers/fig7_mid.png`
    (x∈[9,23], Linux crossover). **These are the authoritative Fig 7 readings.**
- `notes.md` — full reading notes, every number with its provenance, plus the caveat on
  graph-read precision and the list of historical context used.
- Compile test: `build/test.tex` (article + geometry + amsmath) and `build/bare.tex`
  (bare `article`, no packages at all). Both compile clean; 5 pages; **0 overfull/underfull
  boxes**. The bare compile is why there is no `preamble.txt` — the fragment needs nothing.
- `python3 framework/tools/lint_output.py <OUTPUT>` → `OUTPUT LINT OK`, exit 0.

## Results

Every number asserted in `answer.tex`, and where it came from:

**From the papers' text** (`papers/*.txt`, verifiable with grep):
| Claim in answer | Value | Source |
|---|---|---|
| Multics segments per user / words per segment | ~1/4 million each | multics_fjcc1965.txt:204 |
| Multics page sizes | 64 or 1024 words | multics_fjcc1965.txt:191 |
| Multics capacity claim | "a few hundred" users, by "simple scaling", "hazardous" | multics_fjcc1965.txt:411 |
| Mach VM microbenchmark | <0.7 ms/1024 B vs ~1.2 ms for 4.3BSD, MicroVAX II | mach_usenix1986.txt:655 |
| Mach: no perf comparisons done | verbatim quote | mach_usenix1986.txt:651 |
| Mach threads unimplemented | "expected by Summer 1986" | mach_usenix1986.txt:702 |
| Mach VAX MD page size | 512 bytes | mach_usenix1986.txt:344 |
| Multikernel shared-state cost | <30 cycles (1 core) vs ~12,000 extra (16 cores) | multikernel:332 |
| Windows 7 dispatcher lock | 6000 lines, 58 files, "heroic" | multikernel:157 |
| CPU driver size | 7135 lines C + 337 asm | multikernel:765 |
| IP loopback | 2154 vs 1823 Mbit/s; 21 vs 77 Dcache misses/pkt | Table 4 |
| GbE UDP echo | 951.7 vs 951 Mbit/s | multikernel:1781 |
| Web server | 18697 vs 8924 req/s (= 2.10×) | multikernel:1832 |
| Capabilities "a mistake" | verbatim quote | multikernel:941 |
| "wrong to draw any quantitative conclusions" | verbatim quote | multikernel:1861 |
| "complete system is a failure unit" | verbatim quote | multikernel:1908 |

**From the visual channel** (read off rendered figures — these are the ones the text channel
cannot give you):
| Claim in answer | Value | Source |
|---|---|---|
| URPC vs L4 IPC latency | **450 vs 424 cycles**; 3.42 vs 2.36 msgs/kcycle; 9+8 vs 25+13 cache lines | Table 3, `tab23_zoom.png` |
| Shootdown protocols @32 cores | NUMA-aware multicast ~3.1k; multicast ~4.8k; unicast ~12.7k; broadcast ~13.8k cycles | Fig 6, `fig6_zoom.png` |
| End-to-end unmap @32 cores | Barrelfish ~17.5k, Linux ~29.5k, Windows ~46k cycles | Fig 7, `fig7_hi.png` (300 dpi) |
| End-to-end unmap @2 cores | **Barrelfish ~10.3k, Linux ~5.2k, Windows ~5.8k** (corrected, round 1) | Fig 7, `fig7_leftedge.png` |
| Growth 2→32 cores | Barrelfish 1.7×, Linux 5.7×, Windows 7.9× | derived from the two rows above |
| Barrelfish flat region | flat from 2 to ~5 cores | `fig7_leftedge.png` |
| Linux crossover | ~12–13 cores | `fig7_mid.png` |
| ">four-fifths is Barrelfish's own overhead" | 3.1k baseline of 17.5k end-to-end ⇒ ~82% | Fig 6 vs Fig 7, cross-read |

Table 1 (LRPC) was cross-checked arithmetically against the stated clock speeds and is
self-consistent: 845/2.66 = 318 ns, 757/2.8 = 270, 1463/2.5 = 585, 1549/2.0 = 774. ✓

## Deliverables

- `/home/xing/project/auto_hw_complete/output/hw_20260909_1235d6/p4/answer.tex` — the whole
  deliverable. LaTeX fragment starting at `\section*`; no `\documentclass`, no `\usepackage`,
  no `document` environment. All four labels namespaced `p4:` (`p4:sec:multics`,
  `p4:sec:mach`, `p4:sec:multikernel`, `p4:sec:together`, `p4:sec:refs`). LaTeX quotes
  throughout, no ASCII `"`. No figures, no `assets/`.
- **No `preamble.txt`** — deliberate, and verified: the fragment compiles under a bare
  `article` class with zero packages loaded.
- House style matches the brief's description of Ex 1.9: `\section*{Ex.\ 1.0 --- ...}`, intro
  naming the three papers and why they go together, one `\subsection*` per paper with run-in
  `\textbf{Summary.}` / `\textbf{Critical judgment.}`, a `The Three Together` comparative
  subsection, then `References` as an `enumerate` with `[{[1]}]`-style custom labels.

Length: ~2990 words total — intro 182, Multics 737, Mach 840, Multikernel 841, comparison
271, references 119. The floor is ~300–400 words per paper; each paper clears it about 2×.
I judged the extra length earned rather than padding, since the brief asks for named
mechanisms as evidence of reading plus genuine criticism, and both halves are substantive.
A reviewer who disagrees should cut from the *summaries* (the mechanism catalogues), not the
critical judgments, which carry the marks.

## Where I am least confident

1. **Figure-read precision — and I got one wrong last round, so weight this accordingly.**
   The cycle counts from Figures 6 and 7 are read off plotted curves; the paper publishes no
   data table for them. Round 1 proved this is the genuinely fragile part of my evidence: I
   misassigned two curves at Figure 7's left edge from a 150 dpi render and it inverted a
   conclusion. All Figure 7 values are now re-read at 300 dpi with the marker identity
   checked against the legend glyphs at three separate magnifications, and the corrected
   reading is independently corroborated by the paper's own prose about constant overhead.
   Remaining exposure: the *values* are good to roughly the nearest 0.5k cycles, so the
   derived growth ratios (1.7× / 5.7× / 7.9×) carry perhaps ±0.3 each, and "~12–13 cores"
   for the crossover could reasonably be read as 12–14. The *orderings* and the qualitative
   claims (Barrelfish starts higher, is flat to ~5 cores, ends lowest and flattest) are
   unambiguous at 300 dpi. The "more than four-fifths" figure inherits error from both Fig 6
   and Fig 7 and would survive anything from ~75% to ~85%.

2. **Two near-misses against the supplied list, not one.** I originally flagged only
   PaperList **3-3**, "The Multics Virtual Memory: Concepts and Design" (Bensoussan et al.
   1972). The validator correctly pointed out a closer one: **3-6**, Rashid et al.'s
   machine-independent virtual memory paper, which is the Mach VM work — and my Mach summary
   does lean on that subject (external pagers, address maps, the MD/MI split). Both rows sit
   in *Memory Management*, outside the stated exclusion group (1-1..1-11), and both are
   different papers from the ones I wrote about (Corbató & Vyssotsky 1965; Accetta et al.
   1986). The validator ruled the selection stands, and I agree, but this is the call most
   open to a grader taking a stricter line. If it were overturned, the brief's own
   suggestions (Xen, Plan 9, Singularity) substitute cleanly for either paper without
   disturbing the historical arc or the closing comparison.

3. **Historical claims not sourced from these three PDFs.** The "what history vindicated /
   refuted" passages rest on standard history outside the three papers — Bell Labs leaving
   Multics in 1969; x86-64 largely abolishing segmentation; Mach 3.0's user-space server
   being slow; Chen & Bershad (1993) attributing that to memory-system behaviour; Liedtke's
   L4 cutting IPC by "roughly an order of magnitude"; XNU being Mach-derived; Barrelfish
   staying a research vehicle; Arrakis/IX. I believe all are accurate and I deliberately
   hedged the one quantitative item ("roughly an order of magnitude") rather than quoting a
   figure I did not verify from source. I did **not** re-download those papers to check.
   These are listed in `notes.md` under "Historical context used in the judgments".

4. **One list paper is cited as context.** Liedtke's *On µ-Kernel Construction* is list paper
   1-8. It appears in exactly one sentence of the Mach judgment as historical context and is
   **not** written about and **not** in my reference list. I think this is clearly within
   bounds — you cannot honestly assess Mach's performance legacy without mentioning the work
   that refuted it — but I am flagging it rather than hoping it goes unnoticed.

5. **Length**, as discussed above — the one place a reviewer might reasonably push back in
   the other direction from the requirement.
