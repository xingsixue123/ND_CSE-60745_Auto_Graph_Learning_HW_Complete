# Evidence: every quoted number / phrase, with its source location

Text files: `text/<paper>.txt` produced by `pdftotext -layout papers/<paper>.pdf`.
Line numbers below are lines in those .txt files. Paper page numbers are the
printed page numbers.

## Paper 1 — Liu & Layland, JACM 20(1), Jan 1973, pp. 46–61
File `text/liu_layland_1973.txt`. Scanned PDF; every quotation below was
**re-checked against the 300 dpi page render** (`text/ll_p15-15.png`,
`text/ll_p16-16.png`, crops `ll_p15_crop.png`, `ll_p15_crop2.png`, `ll_p16_crop.png`)
because OCR of a 1973 scan is unreliable.

| claim | source |
|---|---|
| (A1)–(A5) assumption list | L109–120 (p. 48) |
| Thm 1 "A critical instant for any task occurs whenever the task is requested simultaneously with requests for all higher priority tasks." | L172–173 (p. 49) |
| Thm 2, rate-monotonic optimal among fixed priority | L279–280 (p. 51) |
| Thm 3, two tasks, $U=2(2^{1/2}-1)\approx0.83$ | L323–324, L368 (pp. 51–52) |
| Thm 5, $U=m(2^{1/m}-1)$; $m=3\Rightarrow0.78$; large $m\to\ln 2$ | L474–480 (pp. 53–54) |
| Thm 7, EDF feasible iff $\sum C_i/T_i\le 1$ | L582–584 (p. 56) |
| §6 "the practical costs of switching between tasks must still be counted" | L508 (p. 55) |
| A4 hedge: "the bookkeeping time necessary to request a successor and the costs of preemptions can be taken into account" | L131–133 (p. 48) |
| §9 example $T=(3,4,5)$, $C_1=C_2=1$: mixed $U=98.3\%$; EDF $C_3=2.0833$, 100%; RM $C_3\le1$, $U=78.3\%$ | L772–781 (p. 60). **The example is in §9 ("Comparison and Comment"), not §8** — §8 (L687) states the mixed algorithm, §9 (L769) evaluates it. Round 1's answer.tex attributed the example to §8; fixed in round 2. Arithmetic check: $1/3+1/4+2/5=0.9833$; $1/3+1/4+1/5=0.7833$; $1-1/3-1/4=0.41\overline{6}$, $\times5=2.08\overline{3}$. All three reconcile. |
| "Although a closed form expression for the least upper bound to processor utilization has not been found for the mixed scheduling algorithm, this example strongly suggests that the bound is considerably less restrictive ... may thus be appropriate for many applications." | L782–786 (p. 60); **verified in `ll_p15_crop2.png`** |
| "Perhaps the most important and least defensible of these are (A1) ... and (A4)" | L791–793 (p. 60); **verified in `ll_p15_crop2.png`** |
| "None of our analytic work would remain valid under this circumstance, and a severe bound on processor utilization could well be imposed by the task aperiodicity." | L805–806 (p. 61); **verified in `ll_p16_crop.png`**. NB: I initially expected "All of our analytic work"; the page image is unambiguous that it reads "None". |
| §10 re-opens (A1), (A4), (A2) but never (A3) | L790–813 (pp. 60–61); grep for "(A3)" in the file returns only L113 (the statement of the assumption) and L126. |

History claims: Sha, Rajkumar & Lehoczky, *Priority Inheritance Protocols*, IEEE
Trans. Computers 39(9), 1990 — adds a blocking term for shared resources. Mars
Pathfinder 1997 priority-inversion resets. Both standard, widely documented.

## Paper 2 — Lozi et al., EuroSys 2016 (HAL open-access copy, hal-01295194)
File `text/lozi_eurosys16.txt`.

| claim | source |
|---|---|
| invariant "make sure that ready threads are scheduled on available cores" | L44–46 (abstract) |
| "Energy waste is proportional." | L71 (§1). |
| **no power measurement anywhere** (the load-bearing claim) | Correct, but my round-1 justification was not. I used `energy\|watt\|power consum\|joule`, which misses every bare use of "power". The right check is `grep -i power`, which returns **eleven** lines: L84–85 (footnote 1), L188 (§2.2), L263 (§2.2.1 "Power-related optimizations"), L446–451 (the §3.3 fix), L693 and L710/L717 (§5), L864 (a reference title). None is a measurement — no power figure, axis or table — so the claim stands, but round 1's answer.tex also said power was mentioned nowhere *else*, which is false. Fixed in round 2. |
| Group Imbalance: compares group *average* load; fix compares *minimum* | L330–341 (§3.1) |
| make 13% faster; NAS `lu` 13× faster with 60 threads + 4 R processes | L357–364 (§3.1) |
| Sched-Group Construction: groups $\{0,1,2,4,6\}$, $\{1,2,3,4,5,7\}$; nodes 1,2 in both | L371–388 (§3.2) |
| Table 1: `lu` 1040 s → 38 s, 27× | L381 |
| Overload-on-Wakeup fix gated: "we only enforce the new wakeup strategy if the system's power management policy does not allow cores to enter low-power states at all" | L444–452 region, §3.3 "The fix" |
| Table 2: TPC-H #18 55.9 s → 43.5 s (−22.2%); full TPC-H 542.9 s → 471.1 s (−13.2%); both fixes −22.6% / −14.2% | L474–480 |
| Missing Sched Domains: Table 3 `lu` 2196 s → 16 s, 137.59×; text "138× faster"; min slowdown 4× | L520, L538, L545 |
| Table 4 "Impacted applications: All" for 3 of 4 bugs | L588–604 |
| Table 4 "maximum measured performance impact": Group Imbalance 13×, Sched Group Construction 27×, **Overload-on-Wakeup 22 %**, Missing Sched Domains 138× | L588–604. So Overload-on-Wakeup is the *smallest* of the four, not the "highest-value fix" as round 1 claimed. It is the largest single contributor only on the TPC-H workload (−22.2 % vs −13.1 % for Group Imbalance, Table 2). Qualified in round 2. |
| Table 5 machine: 8 × 8-core Opteron 6272 (64 threads), 2.1 GHz, 512 GB DDR-3, HyperTransport 3.0 — **the only machine in the paper** | L547–556 |
| sanity checker S = 1 s, M = 100 ms, overhead < 0.5% at 10,000 threads | L644–652 |
| "less than 150 lines of code" | L710–711, and it sits in **§4.2 (visualisation tool)**, referring to that tool's kernel instrumentation only. The sanity checker's cost is reported separately in §4.1 (porting 3.17→4.3 "only required changing one line of code", L655–659). Round 1's answer.tex wrongly applied the 150 lines to both tools; fixed in round 2. |
| "All our fixes will be submitted to the kernel developers shortly." | L587 (footnote 6) |
| 4.3's new load metric "significantly reduces complexity of the code" but "we confirmed, using our tools, that the bug is still present" | L546–587 (§3.5) |
| §5 modular proposal: "We envision a scheduler that is a collection of modules: the core module and optimization modules" | L730–746 |
| "The takeaway is that new scheduler designs come and go." | L583–584 (§3.5) |
| "we will inevitably see new features and 'hacks' retrofitted into the source base" | L583–587 |
| **Direction of the history argument** | Round 1 said EEVDF and `sched_ext` are where "history contradicts the paper". Both are wrong. EEVDF replacing CFS is an *instance* of "new scheduler designs come and go", which the paper predicted; and `sched_ext` is the modular architecture §5 explicitly recommends. Both vindicate the paper. Rewritten in round 2, with the `sched_ext` match explicitly softened (it swaps a whole scheduler rather than advising an invariant-keeping core). |

History claims (verified by web search, 2026-09-21): EEVDF replaced CFS in Linux
6.6 (2023); sched_ext (BPF-defined scheduler class) mainlined in Linux 6.12 (2024).

## Paper 3 — Kaffes et al., Shinjuku, NSDI 2019
File `text/shinjuku_nsdi19.txt`.

| claim | source |
|---|---|
| IX = d-FCFS, ZygOS = c-FCFS by task stealing; both non-preemptive | L36–41, L67–72 (§1) |
| PS optimal for high-dispersion workloads (theory) | L93–97 |
| CFS target preemption latency 6 ms, minimum 0.75 ms | L279–281 (§3.1) |
| preempt every 5–15 µs | L276–281, L380–384 |
| Table 1 cycles: Linux signal 2084/2523/4950; vanilla IPI 2081/2662/4219; no exits 298/1212/1993 | L290–300 |
| receiver-side VM exit removal: −54%, 2662 → 1212 cycles | L326–330 |
| sender 298 cycles = 149 ns at 2 GHz | L344 |
| Table 2 context switch: swapcontext 985 (Linux) / 2290 (Dune); options used cost 36–109 cycles | L350–413 |
| 1212 cycles at 5 µs ⇒ "without wasting more than 10% of the workers' throughput" | L380–384. Check: 5 µs × 2.3 GHz = 11 500 cycles; 1212/11500 = 10.5%. Consistent. |
| MQ queue selection = max(queuing time / SLO), BVT-inspired | L419–434, Alg. 1 |
| Bimodal(99.5−0.5, 0.5−500): "up to 50% lower tail latency at low load and 5x better throughput for a given 300µs tail latency target" | L638–640 (§4.2) |
| multi-modal: "94% lower slowdown at low load and over 2x higer [sic] throughput" | L665–668 |
| RocksDB 99.5% GET / 0.5% SCAN(1000): "tail latency (88% decrease) and throughput (6.6x improvement)" vs ZygOS | L760–762 (§4.4) |
| single dispatcher near-linear to 11 workers; 5 M RPS / 9.5 M RPS with 1 / 2 dispatchers | L748–753 |
| **Fig. 7b/c use "short requests with 1µsec fixed service time to stress the dispatcher"** | L740–746 |
| scale-out plan: "each dispatcher thread handle a subset of the worker threads and steer requests to different dispatchers using the NIC RSS feature" | L474–478 (§3.6) |
| DoS: "one process could launch a denial-of-service attack on another process by issuing a large number of interrupts to a specific core" | L510–513 (§3.6) |
| countermeasure: "Future versions of Shinjuku will run application code in ring 3 ... eliminating this attack vector with very small overhead"; ring3→ring0→ring3 = 84 cycles | L514–520 |
| **but** "For the results in §4, we run applications in VMX non-root mode ring 0 to avoid the address space crossings between Shinjuku and the application code." | L324–328 (§3.1) |
| wish for "support for lightweight user-level interrupts [51]" | L331–333 |
| server: 2 × Intel E5-2658 @ 2.3 GHz, 128 GB, Intel 82599ES 10 GbE; Ubuntu 16.04 / kernel 4.4.0; 1920 connections | L560–588 |

History claim (verified by web search, 2026-09-21): Intel shipped user interrupts
(UINTR, `SENDUIPI`) in 4th-gen Xeon "Sapphire Rapids" — the hardware mechanism the
paper asks for. I deliberately do **not** claim mainline Linux merged UINTR support,
because as of the sources I found it had not.
