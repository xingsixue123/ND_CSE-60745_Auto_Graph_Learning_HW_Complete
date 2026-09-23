# p5 notes — Ex. 2.7, three "Scheduling" papers

## Ground truth check
- Assignment text is `input/hw2_instruction.md` line 34. Verbatim match with the brief. No discrepancy.
- Paper list: CSV `ingest/csv/PaperList.csv` confirms 2-1..2-7 under merged `Scheduling` topic.
  `ingest/pages/PaperList/page_001.png` independently confirms: 2-1..2-7 share one blue colour band,
  distinct from 1-x (green) and 3-x (orange). Two channels agree. Brief's table is correct.

## What this needs
**plain** only. No code, no diagram. The question asks to read/summarize/critically judge.
Nothing is computed; every number in the answer is quoted from a paper I downloaded and read.

## Plan
Write about 2-3 (Lottery), 2-4 (Stride), 2-1 (Buttazzo RM vs EDF), per the brief.
Each: Summary + Critical judgment, ~400-450 words. Target total 1250-1400 (R8).

## Load-bearing numbers, with paper + section

### 2-3 Lottery (papers/lottery.txt)
- p=t/T; coefficient of variation sqrt((1-p)/np) -> accuracy improves as sqrt(n)   [Sec 2.2]
- Mach 3.0 MK82, 25MHz MIPS DECStation 5000/125, 100 ms quantum                    [Sec 4]
- Compensation ticket: fraction f -> inflate by 1/f. Example 400 base units, f=1/5
  -> compensation ticket 1600, total 2000                                          [Sec 3.4, 4.5]
- Fig 4: 10:1 run observed 13.42:1; 20:1 over three minutes -> 19.08:1              [Sec 5.1]
- Fig 5: 2:1 -> 25378 and 12619 iter/s = 2.01:1                                     [Sec 5.1]
- Fig 7: 8:3:1 DB clients, response times 17.19 / 43.19 / 132.20 s (7.69:2.51:1);
  after high-pri exits 44.17 and 15.18 s = 2.91:1; std dev < 7% of average          [Sec 5.3]
- Fig 9: currencies insulate: aggregate A:B = 1.01:1 before B3, 1.00:1 after        [Sec 5.5]
- Fig 11: mutex, A:B = 2:1 -> 763 vs 423 acquisitions = 1.80:1; mean waits 450 ms
  vs 948 ms = 1:2.11                                                                [Sec 6.1]
- Overhead: 3 Dhrystone -> 2.7% fewer iterations; 8 tasks -> 0.8% slower; "the
  measured differences are not very significant" (std dev ~ effect size).
  DB server 1.7% FASTER (1155.5 s -> 1135.5 s), std dev < 0.1%, "significant";
  footnote 9 attributes it to cache/TLB locality.                                   [Sec 5.6]
- "efficient lottery scheduling does not pose any challenging problems"             [Sec 5.6]
- Sec 1: interactive systems need control "at a time scale of milliseconds to seconds"
- Sec 7: fair share schedulers criticised for fairness "on a time scale of minutes"
  ^^ THIS IS THE SHARPEST CRITIQUE: the 20:1 headline number needs a 3-minute average.

### R9 traps checked for 2-3 (do NOT claim these are ignored)
- Inflation danger: Sec 3.2 says inflation "should be disallowed" in general; Sec 3.3
  proposes currencies + an ACL on who may inflate. Sec 4.7 says "A complete lottery
  scheduling system should protect currencies by using access control lists or
  Unix-style permissions". So they DO address it — but only as future work; the measured
  prototype's commands are setuid root and unprotected. Phrase accordingly.
- Response-time variance: the paper STATES sigma_n^2 = (1-p)/p^2 (Sec 2.2) but does not
  flag it as a defect. Do not claim they "admit" it is a weakness — the stride paper is
  what turns it into a criticism. (Brief said "its own admission about response-time
  variability"; that is not quite what the paper does. Noted in submission.md.)
- Overhead: they do NOT overclaim naively; they explicitly say the differences are not
  significant. The critique is about the closing sentence, not the measurements.

### 2-4 Stride (papers/stride.txt)
- stride = stride1/tickets; run min pass, pass += stride; O(lg nc) with priority queue [Sec 2.1]
- partial quantum: pass += f*stride; join/leave via remain vs global pass; ticket change
  rescales remain by stride'/stride                                                 [Sec 2.2-2.4]
- lottery abs+rel error O(sqrt(na)); stride pairwise relative error <= 1 quantum,
  independent of na; but absolute error still O(nc) for skew                        [Sec 2, 5.1]
- 101 clients at 100:1:...:1 -> standard stride absolute error 50; hierarchical
  simulated max absolute error 4.5; bound O(lg nc)                                  [Sec 4, 4.1]
- Fig 12: 19:1, 1M allocations, 1-ticket client: lottery mu=20.13 sigma=19.64, range
  1..194 quanta; stride mu=20.00 sigma=0.01. "three orders of magnitude smaller"     [Sec 5.3]
- Fig 11: 7:3, 3-ticket client: lottery mu=3.33 sigma=2.79; stride mu=3.33 sigma=0.47;
  max response time 39 (lottery) vs 4 (stride)                                       [Sec 5.3]
- Fig 13: 8 clients 7:1..1: ordinary stride sigma=2.45, hierarchical sigma=1.07; max
  absolute error 4 vs 1.5                                                            [Sec 5.4]
- Linux 1.1.50, 25MHz i486 Thinkpad 350C, 100 ms quantum, <300 lines each prototype   [Sec 6]
- CPU: within 1% of ideal for ratios 1..10; 20:1 -> 19.94..20.04; 50:1 -> 49.93..50.44;
  Fig 15: 3:1 -> 2409.18 and 802.89 iter/s = 3.001:1                                 [Sec 6.1]
- Overhead vs stock Linux: 1,2,4,8 arith procs, always < 0.2% fewer iterations        [Sec 6.1]
- ADMISSION: "neither the standard Linux scheduler nor our prototype stride scheduler
  are particularly efficient"; prototype does a LINEAR SCAN, not O(lg nc)             [Sec 6.1]
- ADMISSION: CPU prototype did NOT implement ticket transfers or currencies            [Sec 6.1]
- Network: ttcp UDP within 5%; 20:1 -> 18.51..18.77:1 (systematically low).
  Footnote 9: they decreased a hard-coded ttcp delay constant; without it "observed
  throughput ratios were consistently lower than specified"                           [Sec 6.2]
- ADMISSION: core algorithm "nearly identical" to VirtualClock / WFQ / PGPS, found
  after independent development                                                       [Sec 7.1]
- ADMISSION (conclusion): "lottery scheduling is conceptually simpler ... stride
  scheduling requires careful state updates for dynamic changes, while lottery
  scheduling is effectively stateless"                                                [Sec 8]
- KEY CRITIQUE: Section 5 (the whole lottery-vs-stride comparison) is SIMULATION ONLY.
  Section 6's prototypes are measured against the ideal ratio and against stock Linux,
  never against a lottery-scheduled kernel. Verified by reading Sec 6 end to end.

### 2-1 Buttazzo (papers/buttazzo.txt)
- Five misconceptions listed in abstract + Sec 1                                      [Abstract, Sec 1]
- Priority levels "typically, not greater than 256"; EDF would need 2^32 queues; RM
  gets O(1) insertion with one FIFO per level. Native impl: only the sort key differs  [Sec 2]
- Preemption sim: 1000 independent sims x 1000 time units, periods uniform [10,100],
  U = 0.9 (Fig 2). Fig 3: 10 tasks, load 0.5..0.95. RM preemptions rise ~linearly with
  load; EDF falls at high load (longer job with earliest deadline pushes a task past an
  arrival, Fig 4)                                                                     [Sec 3]
- RM bound n(2^(1/n)-1) -> ln 2 ~= 0.69; EDF U<=1 iff; Lehoczky statistical ~88%;
  hyperbolic bound prod(Ui+1) <= 2, acceptance ratio improved "up to a limit of sqrt2"  [Sec 4]
- Harmonic myth: T=4,8,12, C=2 each -> U=11/12~=0.917 is the ceiling; ALL PAIRS must be
  harmonic (T3=16 -> U=1.00)                                                          [Sec 4]
- Exact test: O(n) for EDF when D=T; pseudo-polynomial for RM. When D<T both pseudo-poly
  and "in the average, the PDC requires more computational steps"  <-- concession       [Sec 4]
- Permanent overload: Cervin Thm 1, EDF rescales to Ti*U. Example U=4/8+6/12+5/20=1.25
  -> T = 10,15,25; in 120 units tau1 runs 12x, tau2 8x, tau3 4.8x. RM may block low-pri  [Sec 5.1]
- CONCESSION: "both the behaviors of RM and EDF are predictable, but, deciding which one
  is better is highly application dependent"                                           [Sec 5.1]
- Transient overload: C=2,3,1,1; T=5,9,20,30; overrun 1.5 on first two jobs of tau1
  -> tau2 misses, not tau4. "The situation is not better under EDF."                   [Sec 5.2]
- CONCESSION: under RM an overrun in tau_i cannot make HIGHER priority tasks miss;
  under EDF any task could. He then says this "can be of little use if we do not know
  a priori which task is going to overrun" and points to resource reservation.          [Sec 5.2]
- Jitter: C=2,3,2; T=6,8,12 -> RM jitter 0,2,8; EDF 1,2,3. I/O latency RM 2,5,7;
  EDF 2,3,2. Cervin Thm 2: EDF I/O latency <= RM for every task                        [Sec 6]
- Jitter sim: 10 tasks, periods uniform [10,200]; below load 0.7 both about the same     [Sec 6]
- CONCESSION: "this example does not prove that EDF always introduces less jitter than
  RM, but just confutes the common belief"                                             [Sec 6]
- Aperiodic: Tia et al. Thms 3 & 4 (no fixed-priority algorithm minimizes aperiodic
  response time); TB(1) dominates the Slack Stealer at Up=0.85; aperiodic utilization
  bound (2-sqrt2)~=0.586 for DM vs 1 for EDF (Abdelzaher 2004)                          [Sec 7.2]
- Resource reservation: Mercer capacity reserves under RM; Abeni-Buttazzo Constant
  Bandwidth Server under EDF                                                            [Sec 7.3]
- CONCESSION (conclusion): "both RM and EDF are not very well suited to work in overload
  conditions and to achieve jitter control"; "the real advantage of RM ... is its simpler
  implementation in commercial kernels"                                                 [Sec 8]

### R9 traps checked for 2-1 (do NOT claim these are ignored)
- Do NOT say he ignores RM's advantages: Sec 2 grants RM O(1) insertion, Sec 4 grants PDC
  is costlier on average when D<T, Sec 5.1 says overload preference is app-dependent,
  Sec 5.2 grants RM's containment property, Sec 8 grants RM's implementation advantage.
- Do NOT say he overclaims the jitter example: he explicitly disclaims it (Sec 6).
  The valid criticism is that the ABSTRACT and CONCLUSIONS generalise more strongly
  than the local hedges.
- The genuinely open gap: Sec 3 counts preemptions, never measures a context-switch cost,
  and never nets that against EDF's per-job deadline update. Verified — Sec 3 is entirely
  preemption counts. Also: no multiprocessor discussion anywhere in the paper.

## History claims (checkable, stated conservatively)
- Linux CFS (2007) and EEVDF (merged 6.6, 2023) both pick the minimum virtual-time task
  and advance it — structurally stride's rule. No production kernel adopted lottery draws.
- Linux SCHED_DEADLINE (merged 3.14, 2014) implements EDF + the Constant Bandwidth Server,
  i.e. exactly the Abeni-Buttazzo reservation mechanism of Buttazzo Sec 7.3.
