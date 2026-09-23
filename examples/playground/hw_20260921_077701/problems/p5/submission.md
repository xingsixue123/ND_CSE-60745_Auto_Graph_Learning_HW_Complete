# p5 — Ex. 2.7 submission

## What the problem asked

> Ex. 2.7 | (22.5pts) Pick three papers from 'Scheduling' in the paper list. Read,
> summarize, and critically judge them. Write at least 1/3 page for each paper's
> summarization and judgment. (7.5pts for each paper)

I checked this against ground truth rather than trusting the brief. The assignment is a
markdown file, `input/hw2_instruction.md`; the question is line 34 and matches the brief's
transcription **verbatim**. The Scheduling group is 2-1…2-7, confirmed two independent ways:
the merged-cell run in `ingest/csv/PaperList.csv`, and the colour band in
`ingest/pages/PaperList/page_001.png`, where 2-1…2-7 share one blue band distinct from the
green 1-x above and orange 3-x below. **No discrepancy between the brief and the source.**

One small correction to the brief, not to the assignment. The brief says the load-bearing
material for lottery scheduling includes "its own admission about response-time variability."
The lottery paper does not admit this as a weakness. It *states* the geometric variance
$\sigma_n^2 = (1-p)/p^2$ in §2.2 as a neutral property and never flags it as a cost; turning
it into a criticism is what the **stride** paper does (§5.3). I therefore did not attribute
an admission to the lottery paper that it does not make. I used its real hedges instead
(the convergence-over-longer-intervals reply, and "the measured differences are not very
significant" on overhead).

## What I decided it needed

**plain**, only. No code and no diagram: nothing is computed and nothing is drawn. Every
number in `answer.tex` is quoted from one of the three papers, which I downloaded and read
in full. The "code" I wrote is verification-only (`verify_quotes.py`), not part of the answer.

## What I did

Downloaded all three PDFs (the brief's trio: 2-3 Lottery, 2-4 Stride, 2-1 Buttazzo — no
substitutions) and read each end to end from the extracted text, not from abstracts or prior
knowledge. For each paper I wrote a Summary and a Critical judgment.

Because R9 is the expensive failure mode here, I explicitly hunted for places where I might
criticise something the paper already answers, and recorded each one in `notes.md` under
"R9 traps checked" before drafting. Three claims I deliberately did **not** make:

- *Not* "the lottery paper ignores the danger of ticket inflation." It doesn't — §3.2 says
  inflation "should in general be disallowed", §3.3 proposes currencies plus an ACL on who
  may inflate, and §4.7 says a complete system should protect currencies with ACLs or
  Unix permissions. The valid, narrower criticism I made instead: the ACL is proposed but
  unimplemented, and the artifact they actually measured ships setuid-root commands.
- *Not* "Buttazzo ignores RM's advantages." He grants RM the $O(1)$ ready queue (§2), grants
  that PDC costs more steps on average than RTA when $D<T$ (§4), grants RM's overrun
  containment (§5.2), and concludes RM's real advantage is implementation simplicity (§8).
  I say so explicitly in the answer.
- *Not* "Buttazzo overclaims from his jitter counterexample." He disclaims it himself in §6.
  The valid criticism is that the abstract and conclusions generalise past the local hedges.

The sharpest criticism in the answer is an internal contradiction I found by reading the
lottery paper's own framing against its own results: §1 says interactive systems need control
"at a time scale of milliseconds to seconds", §7 dismisses fair-share schedulers for achieving
fairness only "on a time scale of minutes", and §5.1's best accuracy number ($19.08\!:\!1$ for
a $20\!:\!1$ allocation) is a **three-minute** average. Both quotes verified verbatim.

The second is that the whole lottery-vs-stride comparison in paper 2-4 is **simulation only**.
I read §6 end to end to confirm: the Linux prototypes are measured against the ideal ratio and
against stock Linux, never against a lottery-scheduled kernel.

## Intermediate steps and code

Paths relative to PLAYGROUND.

| path | what it does |
|---|---|
| `papers/*.pdf` | the three papers as downloaded (see `downloads.md` for URLs) |
| `papers/*.txt` | `pdftotext -layout` extraction — **readable but column-interleaved** |
| `papers/*_flow.txt` | plain `pdftotext` (reading order) — use this for substring search |
| `verify_quotes.py` | re-checks all 60 quotations and numbers in `answer.tex` against the papers |
| `papers/fig12_cap*.png` | crops of stride.pdf p.15 used to confirm the Fig. 12 values by eye |
| `notes.md` | per-paper evidence table with section numbers; R9 trap list |
| `build/` | scratch compile of `answer.tex` inside a wrapper document |

Reproduce the verification:

    cd PLAYGROUND && python3 verify_quotes.py     # exits 0; prints 60/60 verified

Reproduce the compile:

    cd PLAYGROUND/build && pdflatex -interaction=nonstopmode test.tex   # 3 pages, no errors

**Extraction gotcha worth knowing if you re-check me.** `pdftotext -layout` on these
two-column papers interleaves the columns, so a sentence that wraps a line comes out split by
text from the other column and a naive `grep` for a quotation fails even though the quotation
is genuine. Four of my quotes failed that way on the first pass. Use `papers/*_flow.txt`
(plain `pdftotext`) and undo end-of-line hyphenation, which is what `verify_quotes.py` does.

## Results

No computed values — every number is quoted. All 60 verified by `verify_quotes.py` (exit 0).
The load-bearing ones, with source section:

**2-3 Lottery** — 2:1 Dhrystone → 25378 vs 12619 iter/s (2.01:1) §5.1 · 10:1 observed at
13.42:1 §5.1 · 20:1 → 19.08:1 over three minutes §5.1 · 8:3:1 DB response times 17.19 /
43.19 / 132.20 s §5.3 · currency insulation 1.01:1 → 1.00:1 §5.5 · overhead 2.7% / 0.8%
slower and 1.7% faster §5.6 · Mach 3.0, 25 MHz MIPS DECStation 5000/125, 100 ms quantum §4.

**2-4 Stride** — lottery error $O(\sqrt{n_a})$ vs stride pairwise relative error ≤ 1 quantum
§2, §5.1 · 101 clients at 100:1:…:1 → absolute error 50, hierarchical 4.5 §4 · Fig. 12
1-ticket client: stride μ=20.00 σ=0.01 vs lottery μ=20.13 σ=19.64, range 1–194 quanta §5.3 ·
CPU within 1% of ideal, 3:1 → 3.001:1 (2409.18 / 802.89 iter/s) §6.1 · UDP within 5% §6.2 ·
under 300 lines each §6.1 · overhead < 0.2% §6.1.

*Caveat on the Fig. 12 numbers:* `pdftotext` renders the Computer Modern math decimal point
as `:`, so these extract as "20:13". I confirmed all four by eye from the rendered page
(`papers/fig12_cap2.png`), and they are internally consistent — σ ratio 19.64/0.01 ≈ 2000 is
the "three orders of magnitude" the text claims, and μ=20 is the expected wait for a 1-ticket
client at 19:1.

**2-1 Buttazzo** — ≤ 256 priority levels, RM $O(1)$ insertion §2 · preemption simulations at
U=0.9, periods uniform [10,100] §3 · RM $\ln 2 \approx 0.69$ vs EDF exact $O(n)$ at $U\le1$ §4 ·
permanent overload rescaling $T_iU$, example U=1.25 §5.1 · transient overload C=(2,3,1,1),
T=(5,9,20,30), 1.5-unit overrun, τ2 misses not τ4 §5.2 · jitters 0,2,8 (RM) vs 1,2,3 (EDF) §6.

**Two history claims** (not from the papers; general OS knowledge, flagged so you can check):
Linux CFS and its EEVDF successor both pick the minimum-virtual-time task and advance it by a
weight-scaled increment, structurally stride's rule, and no production kernel shipped lottery
scheduling; and Linux `SCHED_DEADLINE` (merged 3.14, 2014) implements EDF together with the
Constant Bandwidth Server, i.e. the Abeni–Buttazzo mechanism of Buttazzo §7.3.

## Deliverables

- `OUTPUT/answer.tex` — the fragment. No `\documentclass` / `\usepackage` / `document` env
  (checked). Labels: none defined, so no namespacing collisions possible. No figures.
- No `preamble.txt`: the fragment needs only `amsmath`/`amssymb`-level math that a homework
  master document will already have, plus `\texttt`, `\emph`, `enumerate`. Nothing exotic.
- No `fig_p5_*.pdf`: this problem is plain prose, no diagram required.
- `lint_output.py` on OUTPUT: **OK**, exit 0. OUTPUT contains `answer.tex` only.

**Length (R8).** Target is 400–450 words per 7.5-point paper, 1250–1400 total.
Measured: 465 (2-3) / 486 (2-4) / 484 (2-1) + 35 (closing comparative sentence) = **1470**
excluding references. That is 5% over the total ceiling and ~8% over per paper, well inside
the "more than a quarter over is a defect" threshold. I cut it down from a 1752-word first
draft; em-dashes went from 25 to 4. Compiles to 3 pages, so each paper comfortably clears the
assignment's own "at least 1/3 page" floor.

## Where I am least confident

1. **The two history claims are the only assertions not verified against a primary source.**
   I am confident in both, but I did not open the Linux source or the CFS/EEVDF/SCHED_DEADLINE
   commit history to confirm. If you want them airtight, they need checking; if you'd rather
   they came out, the arguments around them stand without them.
2. **"No production kernel ever shipped the lottery"** is the weakest sentence in the answer.
   It is a negative existential over all production kernels, which I cannot actually prove.
   I believe it is right for mainstream general-purpose kernels; I would soften it to
   "no mainstream kernel adopted it" without argument if you think it overreaches.
3. **The multiprocessor criticism of Buttazzo.** I claim the paper never discusses
   multiprocessors. I read all 22 pages and saw none, and the task model in §1 is explicitly
   uniprocessor, but this is an absence claim and absence claims are what R9 punishes. It is
   the one "he does not address X" statement I left in; if you find a multiprocessor passage,
   that sentence is a defect and should go.
4. **"The abstract and conclusions generalise anyway"** (Buttazzo critique) is my reading of
   tone, not a quotation. The abstract does say EDF "significantly improves system's
   performance" while §6 disclaims the jitter example, so I think the tension is real, but a
   reader could call it a fair summary rather than an overreach.
5. **Figure content.** I read the three papers from text plus targeted page renders. Two
   Buttazzo figures (Fig. 2 and Fig. 3, preemption counts vs. task count and vs. load) are
   pure graphs whose numeric values I did **not** read off the axes. I described only their
   qualitative shape — "rising roughly linearly with load under RM while falling under EDF" —
   which the surrounding prose states in words (§3). I did not assert any number from them.
