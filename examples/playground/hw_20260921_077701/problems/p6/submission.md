# p6 — submission (round 2)

## Round 2: what changed

All five defects are fixed. I checked each one against the PDF before editing rather
than taking the report on trust; **all five were real**, and one of them was worse than
reported.

- **[1.1] major — the false "only other mention of power" clause.** Confirmed and
  removed. `grep -i power` over `text/lozi_eurosys16.txt` returns eleven lines
  (footnote 1 at L84–85, §2.2 at L188, §2.2.1 at L263, the §3.3 fix at L446–451, §5 at
  L693 and L710/L717, plus a reference title at L864). My round-1 pattern
  `energy|watt|power consum|joule` matched only one of them. This is exactly the R9
  failure the brief warns about, and I made it while writing an R9-motivated critique.
  The load-bearing claim — that no power is ever *measured* — survives, and the
  validator confirmed it independently by checking every figure caption and table; the
  sentence now says power "runs through the paper as a design pressure without ever
  being measured --- no power figure, axis or table", which is what I can actually
  defend.
- **[1.5] — "highest-value fix".** Confirmed wrong. Table 4's "maximum measured
  performance impact" column puts Overload-on-Wakeup *last* at 22 %, behind 13×, 27× and
  138×. It leads only on the database workload (−22.2 % vs −13.1 %, Table 2). Now reads
  "the fix that wins most on their database workload".
- **[1.4] — the sched\_ext paragraph.** Confirmed, and checking it showed the paragraph
  was wrong in a way the report understates. I had called both EEVDF and `sched_ext`
  places where "history contradicts the paper". *Neither* is. §3.5 says "The takeaway is
  that new scheduler designs come and go", so CFS being replaced by EEVDF is the
  prediction coming true, not a refutation; and §5 explicitly proposes "a scheduler that
  is a collection of modules: the core module and optimization modules", so `sched_ext`
  vindicates it. The paragraph now reads as vindication of both, with the `sched_ext`
  match softened as asked ("the fit is loose, since `sched_ext` replaces the whole
  scheduler rather than advising an invariant-keeping core").
- **[1.2] — "under 150 kernel lines between them".** Confirmed. The sentence is at
  L710–711, inside §4.2, and covers the visualiser's instrumentation only; §4.1 reports
  the sanity checker separately. Now attributes the 150 lines to the visualiser alone.
- **[1.3] — §8 vs §9.** Confirmed: §8 (L687) states the mixed algorithm, §9 (L769)
  contains the $T=(3,4,5)$ example. My `evidence.md` had it right and the answer had it
  wrong. Now reads "the worked example in Section~9".

I did **not** touch anything else: the validator verified every other number and both
central critiques, and the brief says not to rewrite passing work.

Two follow-on notes:

- `evidence.md` has been corrected at the five corresponding rows, including the bad
  grep pattern that caused [1.1], so the audit trail no longer vouches for the error.
- **Paper 2 grew from 492 to 529 words** (17.6 % over the 450 target, inside the 25 %
  defect threshold, but up from 9 %). The growth is almost entirely [1.4]: separating
  vindication from contradiction and qualifying the `sched_ext` match genuinely needs
  more words than the incorrect one-liner it replaces. I clawed back ~20 words by
  merging two sentences in the Table 4 paragraph and tightening the tools sentence, and
  stopped there rather than cutting substance the validator had passed.
- One unrelated typographic fix: reference [3]'s URL overran the right margin by 75 pt.
  Added `\allowbreak` at the slashes — still zero packages required. The document now
  compiles with **no overfull boxes at all**.

## What the problem asked

Ex. 2.8 (22.5 pts): "Search for three papers on the topic of 'Scheduling'. Read,
summarize, and critically judge them. Write at least 1/3 page for each paper's
summarization and judgment. (7.5pts for each paper)"

Ground truth is `/home/xing/project/auto_hw_complete/input/hw2_instruction.md`, a plain
markdown file — no PDF, no pages, no figures for this assignment (the ingest for it is a
byte copy at `ingest/pages/hw2_instruction/alltext.txt`). I read the markdown directly.
**The brief's transcription matches the assignment line for line** (assignment line 38);
I found no discrepancy. The preamble on line 1 ("you cannot just copy the answers, put
the answers in your own way") also applies; everything in `answer.tex` is written from
the PDFs in my own words, with quotations kept short and marked.

The brief adds one constraint the question does not spell out: because Ex. 2.7 is the
"pick from the course list" counterpart, the three papers must **not** be on the list's
Scheduling group (2-1 … 2-7). I verified that grouping independently against
`ingest/csv/PaperList.csv`: row `2-1` carries the merged `Scheduling` label, rows
`2-2`…`2-7` are blank continuation rows of that merge, and row `3-1` starts the next
topic (`Memory Management`). So the exclusion set is exactly those seven, and none of my
three papers is among them.

## What I decided it needed

**plain.** No number in the answer is computed by me — every figure is a number reported
*by* one of the three papers, so this is a reading-and-writing task, not a code or
diagram task. There is nothing in the question that says "show", "plot" or "draw". I did
write one throwaway script (word counting, below) but only to police my own length
against rule R8; it produces nothing that appears in the answer.

## What I did

Picked three papers for spread — one classical/analytic (1973), one OS-kernel (2016),
one datacentre (2019) — so the three critiques would rest on different kinds of evidence
(a proof with no experiment; a bug study on one machine; a systems evaluation with a
scaling limit). Downloaded all three PDFs, extracted the full text, and read each end to
end. For the Liu & Layland scan, OCR is unreliable, so I **re-verified every quotation
against a 300 dpi render of the page** before using it; that check changed one thing (see
"least confident"). For each paper I then applied R9 deliberately: before writing that an
author leaves something open, I read the paper's own limitations/discussion text, quoted
what it says about its own weakness, and argued why that answer is insufficient. Two of
the three critiques are built that way (Lozi's power gate, Shinjuku's ring-3 plan).

One selection note for transparency: the brief supplied a candidate pool of freely
available scheduling papers. Papers 1–3 were chosen from that pool; I verified
availability, downloaded, and read them myself rather than taking the pool on trust.

## Intermediate steps and code

Paths relative to PLAYGROUND (`.../problems/p6/`).

- `papers/liu_layland_1973.pdf`, `papers/lozi_eurosys16.pdf`, `papers/shinjuku_nsdi19.pdf`
  — the three source PDFs. Download commands and URLs are in `downloads.md`.
- `text/*.txt` — full text of each paper.
  Reproduce: `pdftotext -layout papers/<name>.pdf text/<name>.txt`
- `text/ll_p15-15.png`, `text/ll_p16-16.png` — 300 dpi renders of Liu & Layland pp. 60–61.
  Reproduce: `pdftoppm -r 300 -f 15 -l 15 -png papers/liu_layland_1973.pdf text/ll_p15`
- `text/ll_p15_crop.png`, `ll_p15_crop2.png`, `ll_p16_crop.png` — PIL crops upscaled 2×
  (LANCZOS) of the conclusion paragraphs, used to confirm the three quotations from that
  paper by eye against the scan.
- `evidence.md` — **the audit table.** Every quotation and every number in `answer.tex`,
  with the line in `text/<paper>.txt` (and, for paper 1, the image) it came from. This is
  the file to check the answer against.
- `build/master.tex` + `build/bare.tex` — compile tests of the fragment.
  Reproduce: `cd build && pdflatex master.tex` (3 pages, no errors); `bare.tex` proves the
  fragment needs **no** packages beyond `article`.
- `notes.md` — the up-front plan and the exclusion-set check.

No venv, no pip, no third-party code. `downloads.md` lists the three PDF downloads.

## Results

There are no self-computed results. Every figure quoted in `answer.tex` is the paper's
own, and each is traced in `evidence.md`. The ones a validator is most likely to check:

| claim in answer.tex | paper | where |
|---|---|---|
| $U=m(2^{1/m}-1)$; 0.83 / 0.78 / $\ln 2$ | L&L | Thms 3–5, pp. 51–54 (`text/liu_layland_1973.txt` L323–324, L368, L474–480) |
| EDF feasible iff $\sum C_i/T_i\le1$ | L&L | Thm 7, p. 56 (L582–584) |
| mixed 98.3 % vs EDF 100 % vs RM 78.3 % | L&L | §9, p. 60 (L772–781). Arithmetic reconciles: $1/3+1/4+2/5=.9833$, $1/3+1/4+1/5=.7833$ |
| make 13 % faster, `lu` 13× | Lozi | §3.1 (L357–364) |
| `lu` 1040 s → 38 s (27×) | Lozi | Table 1 (L381) |
| TPC-H q18 −22.2 %, full −13.2 % | Lozi | Table 2 (L474–480) |
| `lu` 137.59× | Lozi | Table 3 (L520) |
| one 8-node Opteron 6272 machine only | Lozi | Table 5 (L547–556) |
| "Energy waste is proportional." | Lozi | §1 (L71) |
| power never *measured* (no figure, axis or table) | Lozi | `grep -i power` returns 11 lines (L84–85, L188, L263, L446–451, L693, L710, L717, L864), none a measurement. Round 1 used a narrower pattern and drew a stronger conclusion than it supported — see round-2 notes above. |
| Overload-on-Wakeup is the *smallest* of the four by max measured impact (22 % vs 13×, 27×, 138×) | Lozi | Table 4 (L588–604) |
| 2081→298 sender, 2662→1212 receiver, 36–109 cycle ctx switch | Shinjuku | Tables 1–2 (L290–300, L350–413) |
| <10 % throughput at 5 µs quantum | Shinjuku | L380–384; check: 5 µs × 2.3 GHz = 11 500 cy, 1212/11500 = 10.5 % |
| 50 % / 5× bimodal; 88 % / 6.6× RocksDB | Shinjuku | L638–640, L760–762 |
| 11 workers, 5 M / 9.5 M RPS; that experiment uses fixed 1 µs requests | Shinjuku | L740–753 |
| CFS 6 ms target / 0.75 ms minimum preemption | Shinjuku | §3.1 (L279–281) |

External history claims (each checked by web search on 2026-09-21, not from memory):
EEVDF replaced CFS in Linux 6.6 (2023); `sched_ext` mainlined in 6.12 (2024); Intel
user interrupts (UINTR) shipped in Sapphire Rapids. Sha/Rajkumar/Lehoczky 1990 and the
1997 Mars Pathfinder priority inversion are standard, and [4] is cited in the answer.

Length (rule R8), measured by `python3` word count with math blobs counted as one token:
**442 / 529 / 487 words** for papers 1/2/3 (round 1: 439 / 492 / 487), plus a 54-word
note on how I searched, plus references. Target was 400–450 per paper; paper 2 is now
17.6 % over and paper 3 ~8 %, both inside the 25 % defect threshold. See the round-2
notes for why paper 2 grew. Compiled, each paper occupies roughly a full page —
comfortably over the assignment's "at least 1/3 page" floor.

## Deliverables

- `OUTPUT/answer.tex` — the fragment. No `\documentclass`, `\usepackage` or `document`
  environment; verified to compile inside a bare `article` with **no packages at all**.
- No `preamble.txt` — nothing beyond base LaTeX is used.
- No figures (the problem needs none).
- `python3 framework/tools/lint_output.py <OUTPUT>` → `OUTPUT LINT OK`, exit 0.

Namespacing: the fragment defines no `\label` and no macro, so there is nothing to
collide with another problem. Headings are unnumbered `\section*` / `\subsection*`.

## Where I am least confident

0. **My grep discipline, after [1.1].** The defect was not a reading error but a search
   error: I built a critique on a pattern narrow enough to confirm what I expected. For
   round 2 I re-ran the plain-substring check (`grep -i power`) and also re-checked the
   two other places where I assert a paper is silent about something — Liu & Layland
   never counting switching costs, and Shinjuku never measuring the multi-dispatcher
   policy cost. Both still hold (the validator independently confirmed the first). But
   items 3 and 4 below were already my stated soft spots, and [1.1] landed in exactly
   that area, so weight them accordingly.

1. **Paper 1 is topically adjacent to list item 2-1** ("Rate Monotonic vs. EDF: Judgment
   Day"). It is a different paper by different authors twenty-odd years earlier, and the
   brief explicitly offers it, so I judged it in bounds — but a strict reading of "do not
   pick a paper merely adjacent to one on the list" could go the other way. I mitigated
   by critiquing the 1973 paper on its own terms (cost model, assumption A3) rather than
   rehearsing the RM-vs-EDF comparison that 2-1 is about. If the validator disagrees,
   the cheapest substitution is Ghodsi et al., *Dominant Resource Fairness* (NSDI 2011),
   free from usenix.org.
2. **A quotation that contradicted my prior.** Liu & Layland's conclusion reads "**None**
   of our analytic work would remain valid under this circumstance". I expected "All",
   which is what the sentence's logic seems to want, and I only trusted "None" after
   reading it off the 300 dpi scan (`text/ll_p16_crop.png`). If the validator has a
   cleaner copy of the paper and it reads "All", my sentence "conceding that without
   periodicity 'None of our analytic work would remain valid'" needs rewording — but the
   surrounding point (that A1/A4 are reopened and A3 is not) survives either way.
3. **"Energy waste is proportional" as a criticism.** *(Round 1 wording of this item is
   what became defect [1.1] — the narrow grep.)* Now re-checked with `grep -i power`,
   which finds eleven mentions, none a measurement; the validator also confirmed by
   inspecting every figure caption and table that no power figure, axis or table exists.
   I consider the surviving claim solid. Residual risk: I still have not rendered every
   page of that paper as an image, so a power number drawn inside a figure body (rather
   than in a caption or axis label) could in principle have escaped both of us.
4. **The Shinjuku ring-3 criticism.** I assert the ring 3 → ring 0 crossings "would recur
   on every preemption" at a 5 µs quantum. That is my inference from the design, not
   something the paper states or measures; the paper only gives the 84-cycle transition
   cost. If a validator reads §3.6 as implying the crossing happens less often, the
   quantitative force of my point drops, though the core objection — that §4 was measured
   in ring 0 and the safe configuration was never re-measured — is directly supported by
   the paper's own sentence at §3.1.
5. **History claims.** EEVDF/6.6 and `sched_ext`/6.12 I verified by search today and am
   confident in. For UINTR I deliberately say only that the hardware "shipped … in
   Sapphire Rapids" and make **no** claim about mainline Linux support, because the
   sources I found said that support was still unmerged and I did not want to assert a
   current status I could not pin down.
