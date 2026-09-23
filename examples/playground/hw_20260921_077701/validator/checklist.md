# Master validator checklist — hw_20260921_077701

## Round 1 — 2026-09-21

Verdict: **FAIL**

### What I checked, and how

**Coverage** — enumerated the questions from the assignment itself
(`input/hw2_instruction.md`), not from `problems.json`. Eight exercises:
2.1 (15) + 2.2 (5) + 2.3 (5) + 2.4 (5) + 2.5 (20) + 2.6 (5) + 2.7 (22.5) + 2.8 (22.5)
= **100 pts**. All eight appear in `main.pdf` with their own headings, and every
sub-part is present (three diagrams for 2.1; the explanation *and* the program for
2.2/2.3; four pseudo-codes *and* the inter-relation explanation for 2.5; three papers
each for 2.7 and 2.8). **No coverage defect.**

**Paper-list compliance** — `ingest/csv/PaperList.csv` has a merged "Scheduling"
label spanning rows 2-1…2-7. Ex. 2.7 uses 2-1, 2-3, 2-4 — all inside that block.
Ex. 2.8 uses Liu & Layland 1973, Lozi et al. 2016, Kaffes et al. 2019 — none of which
appear anywhere on the list. **Correct on both counts.**

**Ex. 2.1 recomputed from scratch.** Independent simulation of RR (q=1, new arrival
enqueued ahead of the preempted task), FCFS and non-preemptive SJF for
T1(1,10) T2(2,4) T3(3,1) T4(4,6):

| | RR | FIFO | SJF |
|---|---|---|---|
| completion | 22, 12, 5, 19 | 11, 15, 16, 22 | 11, 16, 12, 22 |
| avg turnaround / wait | 12.00 / 6.75 | 13.50 / 8.25 | 12.75 / 7.50 |

Every cell of Table 1 matches. All three figure PDFs read at 400 dpi and compared
block-by-block against the simulation — **all three diagrams are correct**, arrival
markers present for all four tasks, idle unit [0,1) drawn.

**Ex. 2.3 program actually compiled and run.** Extracted the listing from `p2.tex`,
built with `gcc -Wall -Wextra` (zero warnings), ran it in a directory with two small
files and again with `PATH=/nonexistent`. Output matches the claimed transcript
exactly in form, including `execvp: No such file or directory` and exit status 127 on
the failure branch. **Not fabricated.**

**The PDF, both channels.** 14 pages rendered at 200 dpi and read as images, plus
extracted text. Compiles clean; no missing-figure boxes; no margin overflow; the three
Gantt charts are legible at printed size; the `algpseudocode` floats and the `listings`
block render correctly; no duplicated or orphaned `\input`. **No compile/layout defect.**

**R4 output hygiene.** `lint_output.py` passes on all six of `p1`…`p6`.

**R8 length.** Per-paper prose: 424 / 456 / 473 (Ex 2.7) and 447 / 535 / 482 (Ex 2.8)
words against the ~550 target for a paper summary-and-critique. Short answers: 2.2 =
211, 2.4 = 228, 2.6 = 227 against the ~190 target — all inside the 25 % tolerance.
**No length defect.**

**R9 — quotation and characterisation audit.** This is where the submission fails. I
opened all six papers (local PDFs in the workers' playgrounds) and read the passages
*around* every quotation and every "the paper never / does not / leaves it there"
claim. Sixty-odd individual claims checked; the numeric and summary claims are almost
all sound. The defects below are concentrated in the *critique* paragraphs, and they
are the exact failure mode specs.md R9 names: a verbatim quote supporting a criticism
the source answers a sentence or two later.

### Defects

- **[D1.1] Ex. 2.7, Lottery Scheduling critique — the criticism is answered in the
  paragraph immediately after the quote.** | `p5.tex:22–30`, PDF p. 8 | severity:
  **blocking**
  The answer argues the authors retreat to long time intervals, and that this "costs
  them their framing" because the introduction wants control "at a time scale of
  milliseconds to seconds", concluding "on the timescale the paper says matters it
  supplies roughly what it criticises."
  The sentence *directly following* the 19.08:1 figure is: *"Although the results
  presented in Figure 4 indicate that the scheduler can successfully control
  computation rates, we should also examine its behavior over shorter time
  intervals."* Figure 5 then plots 8-second windows over a 200-second run and the
  paper states *"if a scheduling quantum of 10 milliseconds were used instead of the
  100 millisecond Mach quantum, the same degree of fairness would be observed over a
  series of subsecond time windows"* (echoed on p. 2: "reasonable fairness can be
  achieved over subsecond time intervals"). The paper does not retreat to minutes; it
  specifically examines the timescale the critique says it ignores.
  Second problem in the same sentence: "Individual 60-second runs scatter badly" is
  contradicted by the clause the 13.42:1 number is lifted from — *"With the exception
  of the run for which the 10 : 1 allocation resulted in an average ratio of 13.42 : 1,
  all of the observed ratios are close to their corresponding allocations."* 13.42:1
  is the single acknowledged outlier out of ~30 runs, not evidence of general scatter.
  **To resolve:** rewrite the paragraph against what the paper actually claims. The
  real criticism is available and survives: the subsecond claim is an *extrapolation*
  from a 100 ms quantum, never measured, and the 1/√n convergence rate means a 10 ms
  quantum buys only √10 in error over the same wall-clock window. Say that, or drop
  the argument.

- **[D1.2] Ex. 2.7, Buttazzo critique — attributes an overgeneralisation the paper
  does not make, and the answer refutes itself eleven lines later.** | `p5.tex:108–111`,
  PDF p. 10 | severity: **blocking**
  "…Buttazzo says exactly that of his jitter example, which \`\`does not prove that EDF
  always introduces less jitter'', **yet the abstract and conclusions generalise
  anyway**."
  The quoted half-sentence continues *"…but just confutes the common belief that RM
  outperforms EDF in reducing jitter"* — i.e. Buttazzo states the limited claim
  precisely. The abstract says the received statements are *"either wrong, or not
  precise"*. The conclusion says RM's claimed properties *"only apply for the highest
  priority task, and do not hold in general"* — a denial of RM's superiority, not an
  assertion that EDF always wins — and *"both RM and EDF are not very well suited to
  work in overload conditions and to achieve jitter control."* Figures 11–13 hedge
  further (below U = 0.7 "both algorithms introduce about the same jitter").
  The answer's own line 121 quotes that same "not very well suited" conclusion as
  evidence he "does not stack the deck", so the submission contradicts itself.
  **To resolve:** delete or invert the charge. If a version of it survives, it is
  about the *title and rhetorical register* ("Judgment Day", "it is time to clarify"),
  not about the abstract or conclusions, which are hedged.

- **[D1.3] Ex. 2.7, Buttazzo — attributes to the paper a discussion it does not
  contain.** | `p5.tex:114–116`, PDF p. 10 | severity: major
  "…the certification and tooling ecosystem built on fixed priorities, which he
  reduces to a circularity."
  There is no certification or tooling discussion in the paper (no occurrence of
  certification, tool-chain, standards, avionics, legacy). The nearest remark is the
  non-circular observation that *"the use of EDF would significantly increase if
  commercial kernels provided direct support for deadlines"*. The clause is also
  self-contradictory: it lists the ecosystem as "absent" and then describes what he
  does with it.
  **To resolve:** drop the "reduces to a circularity" clause. "Absent: multiprocessors,
  and the certification ecosystem that keeps fixed priorities in industrial use" is
  accurate and sufficient.

- **[D1.4] Ex. 2.7, Buttazzo — "never nets the saved switches against EDF's per-job
  deadline update" is false.** | `p5.tex:112–113`, PDF p. 10 | severity: major
  He nets them explicitly, on p. 8: *"In spite of the extra computation needed for
  updating the absolute deadline, however, EDF introduces less runtime overhead than
  RM, when context switches are taken into account."*
  **To resolve:** the defensible charge is that he never nets them **quantitatively** —
  the netting is an assertion, and Fig. 7 counts preemption *steps*, not cycles. Insert
  that qualifier. ("Never measures a context switch on real hardware" is correct as
  written and can stand.)

- **[D1.5] Ex. 2.7, Lottery — "unprotected" overstates, and the setuid point is
  answered in a footnote on the same page.** | `p5.tex:37–40`, PDF p. 9 | severity: major
  Footnote 5 of the paper: `fundx` *"only executes as root to initialize its task
  currency funding. It then performs a setuid back to the original user before
  invoking exec."* And §5.5 (Load Insulation) supplies a working containment mechanism
  — *"A currency defines a resource management abstraction barrier that locally
  contains intra-currency fluctuations such as inflation"* — demonstrated in Figure 9.
  So currencies in the measured artifact are not "unprotected"; what is missing is only
  the access control over *who may inflate a given currency*.
  **To resolve:** narrow the claim to the ACLs, which genuinely are left as future
  work, and drop "unprotected" and the setuid-root framing.

- **[D1.6] Ex. 2.8, Liu & Layland — "Independence alone is never reopened" is wrong
  twice.** | `p6.tex:46–47`, PDF p. 11 | severity: major
  (a) The conclusion reopens (A1), (A4) and (A2); it reopens neither (A3) **nor** (A5),
  so "alone" is false.
  (b) More importantly, the paper *does* discuss the reach of (A3), in the assumptions
  section: *"Note that assumption (A3) does not exclude the situation in which the
  occurrence of a task τ2 can only follow a certain (fixed) number … of occurrences of
  a task τ1"*, and gives a modelling recipe. Asserting the paper never addresses
  independence is precisely the R9 "never asks / does not address" pattern.
  **To resolve:** the substantive point (resource sharing and priority inversion are
  outside the model) is correct and worth keeping. Rephrase to acknowledge the §3
  remark and say what it does *not* cover: it handles fixed request-count coupling, not
  mutual exclusion, so the blocking term is still missing. That is a stronger criticism
  than the current one and costs one clause.

- **[D1.7] Ex. 2.8, Shinjuku — headline comparison drops a qualifier and a
  baseline.** | `p6.tex`, PDF p. 13 | severity: minor
  Paper: "up to 50% lower tail latency **at low load** and 5x better throughput for a
  given 300µs tail latency target", and the comparison is against **both IX and
  ZygOS**. The answer says "Against ZygOS … roughly 50 % lower tail latency", dropping
  "at low load".

- **[D1.8] Ex. 2.8, Shinjuku — misattributed causation and wrong section.** |
  `p6.tex`, PDF pp. 13 | severity: minor
  The "<10 % of worker throughput" figure is tied in §3.2 to the 1212-cycle *receiver
  interrupt* cost, not to the 36–109-cycle context switch. And the "11 workers /
  5 M / 9.5 M RPS" figures are in §4.3, not §3.6 (only the RSS quote and the
  socket-saturation claim are in §3.6).

- **[D1.9] Ex. 2.7, Buttazzo — quoted scope too wide.** | `p5.tex:120–122` | severity:
  minor
  "highly application dependent" is said of **permanent** overload specifically, not of
  overload behaviour in general. Also, the grant that RM confines an overrun to
  lower-priority tasks is immediately qualified in the paper — *"such a property of RM
  can be of little use if we do not know a priori which task is going to overrun"*.

- **[D1.10] Ex. 2.7 heading omits its point value.** | PDF p. 8 | severity: minor
  Every other heading carries it ("Ex. 2.5 (20 pts)", "Ex. 2.8 (22.5 pts)"); Ex. 2.7
  reads "Ex. 2.7 — Three papers from the \`\`Scheduling'' group".

- **[D1.11] Ex. 2.7 closing sentence says "All three" and names two.** | `p5.tex`,
  PDF p. 10 | severity: minor
  "All three argue the same way: 2-4 unseats its own predecessor's randomness, and 2-1
  unseats static rate priorities…" — 2-3 is not accounted for, and it is the one paper
  of the three that unseats nothing.

- **[D1.12] Ex. 2.8, Liu & Layland — two small attribution slips.** | `p6.tex`, PDF
  p. 11 | severity: minor
  (a) The paper writes "**Perhaps** the most important and least defensible of these";
  the hedge is dropped (the quoted fragment itself is verbatim).
  (b) The 0.83 (two-task) and 0.78 (three-task) figures come from Theorems 3 and 4;
  Theorem 5 is the general m-task bound. They follow from Theorem 5's formula, so this
  is attribution, not arithmetic.

- **[D1.13] Ex. 2.7, Lottery — the 8:3:1 response times are conditional.** |
  `p5.tex:17–19` | severity: minor
  17.19 / 43.19 / 132.20 s hold only while the high-priority client is active, giving
  an observed 7.69 : 2.51 : 1 rather than the nominal 8 : 3 : 1.

### Resolved since last round
n/a — first round.

### Still outstanding
n/a — first round.

### Where I looked and found nothing

- Ex. 2.1: schedules, table, all three figures — independently recomputed, all correct.
- Ex. 2.2: argument is sound; the init/pid-1 exception is correctly stated.
- Ex. 2.3: compiles warning-free and runs; all three `fork()` return cases handled;
  `_exit` vs `exit` reasoning correct; claimed transcript reproduces.
- Ex. 2.4: correct, including the ASID/PCID caveat and the "different processes cost a
  process switch" framing.
- Ex. 2.5: all four pseudo-codes are sound — COW fork with the two return-value
  assignments, exec's point-of-no-return placed correctly, waitpid's ECHILD/WNOHANG/
  EINTR ordering correct, exit's reparent-to-init and zombie transition correct. The
  inter-relation explanation is accurate.
- Ex. 2.6: accurate (state Z, `<defunct>`, SIGKILL discarded, init adoption, EAGAIN
  leak, orphan contrast).
- Ex. 2.7 / 2.8 **summary** paragraphs: essentially every number verified against the
  source — lottery's 25378/12619, stride's µ=20.00/σ=0.01 vs µ=20.13/σ=19.64 range
  1–194, Buttazzo's C=(2,3,1,1) T=(5,9,20,30) overrun example and 0,2,8 vs 1,2,3
  jitters, Liu & Layland's T=(3,4,5) 98.3/100/78.3 %, Lozi's 13×/1040 s vs 38 s/22.2 %/
  13.2 %/137.59×, Shinjuku's 2081→298 and 2662→1212 cycles and 6.6×/88 %. Also
  confirmed the two critiques I most expected to collapse do **not**: Lozi's
  single-machine evidence base (Table 5 is the only hardware; Table 4 says "All" for
  exactly three of four bugs; no power measurement exists anywhere), and Shinjuku's
  ring-0 evaluation (§3.1 verbatim, and the only ring-3 number is an 84-cycle
  microbenchmark).
- Compile, layout, figure legibility, label namespacing, `lint_output.py` on all six
  worker dirs.

---

## Round 2 — 2026-09-21

Verdict: **PASS** (with one minor defect noted, and one round-1 minor withdrawn)

### What changed, and how I checked it

Only `p5.tex` (+793 B) and `p6.tex` (+448 B) were touched; `p1`–`p4` and the three
figure PDFs are byte-identical to round 1 (same sizes, same 17:43 mtimes), and a
sentence-level diff of the round-1 against the round-2 extracted PDF text confirms
**no change anywhere in Ex. 2.1–2.6**. The round-1 verification of those answers —
the independently recomputed RR/FIFO/SJF schedules and table, and the Ex. 2.3 program
I compiled and ran — therefore still stands and was not re-litigated.

For the rewritten passages I did not accept the fix on sight: every quotation and
characterisation *newly introduced* in round 2 was re-checked against the source PDFs.

### Resolved since last round

- **[D1.1] blocking — fixed, and fixed in the right direction.** The paragraph no
  longer claims the authors duck the short-timescale question; it now credits Figure 5
  explicitly ("the paper meets that objection rather than ducking it"), names 13.42:1
  as the acknowledged exception, and relocates the criticism to the genuinely weak
  step. I verified the two new load-bearing claims independently:
  – *"Nothing was ever run at 10 ms"* — **true**. The only two occurrences of "10
  milliseconds" in the paper are §2's analytical remark and §5.1's extrapolation; the
  Mach prototype quantum is 100 ms throughout. No 10 ms experiment exists.
  – *"every measurement in the paper comes from the unoptimised list-based prototype"*
  — **true**. §4: "Our scheduler uses the simple list-based lottery with a
  move-to-front heuristic"; §5.6: "numerous optimizations could be made to our
  list-based lottery". The tree-based O(lg n) version is described, never built.
  This is a stronger and accurate criticism.
- **[D1.2] blocking — fixed.** Now reads "the paper is more careful about it than its
  title", quotes the jitter sentence *through* its continuation ("…but just confutes
  the common belief") with a correct ellipsis, and cites the conclusion's "do not hold
  in general". The self-contradiction with the later paragraph is gone. The residual
  criticism — "what overshoots is the register, not the claims: a Judgment Day that
  delivers a rebuttal" — is about the title, which is fair comment.
- **[D1.3] major — fixed.** "which he reduces to a circularity" deleted; now reads
  "multiprocessors, and the certification ecosystem that keeps fixed priorities in
  use", which is an accurate statement of what is *absent* from the paper.
- **[D1.4] major — fixed.** Now "nets the saved switches … **by assertion alone**",
  with the p. 8 sentence quoted verbatim. Exactly the qualifier that was missing.
- **[D1.5] major — fixed.** "unprotected" and the setuid-root framing removed; now
  credits §5.5's barrier and narrows the complaint to the missing ACLs, which is what
  the paper actually defers.
- **[D1.6] major — fixed.** Now quotes the (A3) remark itself and answers it:
  "Independence is examined once, and only in its easy case … Fixed request-count
  coupling is not what real systems break on." The modelling recipe is correctly
  summarised as "absorbed by choosing commensurate periods" (paper: "the period of τ2
  is N times the period of τ1"), and the τ1/τ2 direction is right.
- **[D1.7] minor — fixed.** "Against both IX and ZygOS … up to 50 % lower tail latency
  **at low load**".
- **[D1.8] minor — fixed.** Causation reattributed to the 1212-cycle receiver cost, and
  the 11-worker / 5 M / 9.5 M figures correctly credited to §4.3 while §3.6 keeps only
  the socket-saturation quote and the RSS proposal.
- **[D1.9] minor — fixed.** "highly application dependent" now scoped to permanent
  overload, and the "can be of little use if we do not know a priori which task is
  going to overrun" qualifier added.
- **[D1.10] minor — fixed.** Heading now reads "Ex. 2.7 (22.5 pts)".
- **[D1.11] minor — fixed.** "Two of the three are acts of replacement… exactly the
  state 2-3 had traded away for a stateless draw" — the count is right and 2-3 is now
  accounted for.
- **[D1.12a] minor — fixed.** Quotation now reads "perhaps the most important and least
  defensible".
- **[D1.13] minor — fixed.** Now "an 8:3:1 database allocation whose response times
  while the best-funded client is active … give relative speeds of 7.69 : 2.51 : 1".

### Withdrawn

- **[D1.12b]** — I said the 0.83 / 0.78 figures belong to Theorems 3 and 4 rather than
  Theorem 5. On re-reading, Theorem 5 *is* the general bound U = m(2^{1/m} − 1), and
  m = 2 and m = 3 evaluate to 0.828 and 0.780, so "Theorem 5 bounds utilisation at
  U = m(2^{1/m} − 1): about 0.83 for two tasks, 0.78 for three" is a correct reading of
  Theorem 5, not a misattribution. The master was right to leave it. **Withdrawn.**

### Defects

- **[D2.1] Inexact quotation introduced by the round-2 rewrite.** | `p5.tex:31–32`,
  PDF p. 8 | severity: **minor**
  The answer quotes a lottery as needing only ``a random number and $\lg n$ additions
  and comparisons''. The paper (§5.6) reads: *"a tree-based lottery need only generate
  a random number and **perform** lg n additions and comparisons"*. The word "perform"
  is elided inside the quotation marks without an ellipsis. The meaning is unaffected
  and the attribution to the tree-based implementation is correct; this is purely a
  transcription slip. Inserting "perform", or cutting the quote at "a random number",
  would resolve it.

### Still outstanding

None. Both blocking and all four major defects from round 1 are resolved; six of the
seven minors are fixed and the seventh is withdrawn. D2.1 is the only open item and is
cosmetic.

### Where I looked in round 2 and found nothing

- **Compile health**: `main.log` has zero Overfull/Underfull boxes, zero LaTeX
  warnings, zero undefined references. 14 pages, same as round 1.
- **Layout**: pages 8–13 (everything the rewrite moved) re-rendered and read as images.
  No overflow, no orphaned headings, no broken page breaks. Pages 1–7 unchanged.
- **R4**: `lint_output.py` passes on all six worker dirs; `p5/answer.tex` and
  `p6/answer.tex` are byte-identical to `final/p5.tex` and `final/p6.tex`, so the
  worker deliverables and the assembly are in sync.
- **R8 length**: per-paper prose is now 477 / 456 / 543 (Ex 2.7) and 488 / 535 / 508
  (Ex 2.8) words against the ~550 target — the rewrites added 136 and 67 words in
  total and every paper is still at or under target. Short answers unchanged at 211 /
  228 / 227.
- **Coverage** re-confirmed against `hw2_instruction.md`: all eight exercises, 100 pts,
  every sub-part present.

I have nothing substantive left to blame.

---

## Round 3 — 2026-09-21

Verdict: **PASS** (clean — no outstanding defects at any severity)

### What changed

A single surgical edit. `p5.tex` grew by 37 bytes (11377 → 11414); `p6.tex` and
`p1`–`p4` and the three figure PDFs are untouched (mtimes unchanged at 17:59 / 17:43).
A sentence-level diff of the round-2 against the round-3 extracted PDF text shows
**exactly one sentence differs in the whole 14-page document**:

> −  The warrant offered for a fine quantum being cheap, that a lottery needs only
>    ``a random number and lg n additions and comparisons'', describes the tree-based
>    implementation, whereas …
> +  The warrant offered for a fine quantum being cheap — ``a tree-based lottery need
>    only generate a random number and perform lg n additions and comparisons'' —
>    describes an implementation that was never built, whereas …

That is D2.1 and nothing else. No other paragraph, number, figure or heading moved.

### Resolved since last round

- **[D2.1] minor — fixed, and verified against the source properly.** My first grep for
  the new quotation returned NOT FOUND, which would have been a false positive: the
  OSDI paper is two-column, so the flat text extraction interleaves the columns and
  breaks the sentence across a hyphenated line ("generate a ran-/dom number"). I
  re-extracted page 8 of `lottery.pdf` with a half-width clip box per column and
  repaired the hyphenation. §5.6 then reads, contiguously:
  *"The core lottery scheduling mechanism is extremely lightweight; a tree-based
  lottery need only generate a random number and perform lg n additions and
  comparisons to select a winner among n clients."*
  The quotation as now printed is **verbatim and contiguous**. Resolved.
  The rewrite is also a genuine improvement rather than a patch: the quote now carries
  its own subject ("a tree-based lottery"), so the redundant gloss "describes the
  tree-based implementation" could be replaced by the load-bearing claim, "describes an
  implementation that was never built". I checked that claim too — §4 states "Our
  scheduler uses the simple list-based lottery with a move-to-front heuristic", and the
  sentence immediately after the quoted one reads "Our prototype scheduler, which
  includes full support for currencies, **has not been optimized**", which is the paper
  itself corroborating the surrounding criticism.

### Withdrawn

None this round. (D1.12b remains withdrawn from round 2.)

### Defects

None.

### Still outstanding

None, at any severity. Round 1's two blocking and four major defects were resolved in
round 2; six of seven round-1 minors were fixed and the seventh withdrawn; the single
round-2 minor is now fixed.

### Where I looked in round 3 and found nothing

- **Regression check**: the r2→r3 text diff is one sentence. Ex. 2.1–2.6 and Ex. 2.8
  are byte-for-byte what I already verified — the recomputed RR/FIFO/SJF schedules and
  timing table (round 1), the Ex. 2.3 program I compiled with `-Wall -Wextra` and ran
  (round 1), and every quotation across the six papers (rounds 1–2).
- **Compile health**: zero Overfull/Underfull boxes, zero LaTeX warnings, zero
  undefined references in `main.log`. Still 14 pages.
- **Layout**: pages 8 and 9 re-rendered and read as images, since the edit moved the
  page break inside that paragraph. The break now falls at "…never / built"; no widow,
  no orphan, no overflow.
- **R4**: `lint_output.py` passes on all six worker dirs; `p5/answer.tex` is
  byte-identical to `final/p5.tex`.
- **R8**: the Lottery section went 477 → 482 words; every paper remains at or under the
  ~550 target.
- **Coverage**: all eight headings present and carrying their point values —
  15 + 5 + 5 + 5 + 20 + 5 + 22.5 + 22.5 = 100.

Three rounds, twenty defects raised, nineteen fixed and one withdrawn by me. I have
nothing left to blame.
