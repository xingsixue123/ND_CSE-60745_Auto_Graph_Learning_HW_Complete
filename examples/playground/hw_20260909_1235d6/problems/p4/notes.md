# p4 — Ex 1.0 notes

## What the problem needs

**plain only.** No diagram, no code. The question asks to search for three papers,
read them, summarize and critically judge, >= 1/3 page each. There is nothing to compute
and nothing to plot. The only "work product" beyond prose is that the papers had to be
really downloaded and really read.

## Verification of the brief against ground truth

`input/hw_questions.md` line 41 matches the brief **verbatim**, including the odd `Ex. 1.0`
label. No discrepancy. Source is a plain `.md` (manifest: `kind: text_document`, no rendered
pages, no figures), so the three-channel PDF reconciliation of R7 does not apply to the
assignment itself — I read the original input file directly.

Exclusion boundary independently re-verified two ways:
- `ingest/csv/PaperList.csv`: row `1-1` carries `OS History and Architecture`, rows 1-2..1-11
  blank (merged cell), row `2-1` starts `Scheduling`.
- `ingest/pages/PaperList/page_001.png`: the green colour band covers exactly 1-1..1-11 and
  a new (blue) band starts at 2-1.
So the off-limits group is exactly 1-1 .. 1-11. Confirmed.

## Papers chosen (all found by WebSearch, none on the supplied list)

1. Corbató & Vyssotsky, "Introduction and Overview of the Multics System", AFIPS FJCC 1965
2. Accetta et al., "Mach: A New Kernel Foundation for UNIX Development", USENIX Summer 1986
3. Baumann et al., "The Multikernel: A New OS Architecture for Scalable Multicore Systems", SOSP 2009

Argument running through the set: three successive answers to *what may the OS assume about
the machine underneath, and where should OS function live?* — one maximal system on symmetric
shared memory (1965) -> decompose it into a minimal kernel plus user-level servers (1986) ->
abandon shared memory as the organising assumption altogether (2009).

Judgment call to flag: PaperList **3-3** is "The Multics Virtual Memory: Concepts and Design"
(Bensoussan et al. 1972), which is a *different paper* by *different authors* on a different
subject, and it sits in the **Memory Management** group, not the excluded OS History and
Architecture group. My paper 1 is the 1965 Corbató & Vyssotsky system overview. I judged this
not to be double-dipping. Recorded here so the validator can disagree.

## Reading channels used

All three PDFs: full `pdftotext` extraction read end to end. In addition, for the Multikernel
paper the graphs/tables do not survive text extraction (columns interleave, curves vanish), so
Figures 6 and 7 and Tables 2/3 were rendered at 150 dpi with `pdftoppm`, cropped and upscaled
4x LANCZOS, and read visually. That is where the per-figure numbers below come from.
`file` misreports page counts on these PDFs (6/8/6); `pdfinfo` is right: **10 / 16 / 20**
pages. (I first wrote 8 for the Multics PDF — that was `file`'s number leaking through,
because my `pdfinfo | head -12` had truncated before reaching the `Pages:` line for that
file. Corrected in validator round 1, defect 1.3.)

## Verified numbers

Multics (1965) — a *prospectus*, written before the system ran; six companion FJCC papers.
- Zero measurements. Everything future tense.
- Only quantitative claim: "a few hundred" simultaneous users, from "simple scaling of
  processor and memory speed", immediately hedged as "hazardous to predict any firm numbers".
- Segments: up to ~1/4 million segments per user, each up to ~1/4 million words. Dual page
  size 64 or 1024 words. Execute-only descriptor bit. No master processor ("the supervisor
  does not have a special processor"). Processors reach I/O only via memory "mailboxes".
- ASCII: 128 codes, 95 printing graphics. Batch = the n=0 terminal case.
- Conclusion sentence: plans "are not unattainable"; expecting the initial system to meet all
  requirements would be "presumptuous".

Mach (1986) — design + status report as of April 1986.
- **The entire quantitative evaluation is one number**: touching newly allocated memory on a
  MicroVAX II costs "less than 0.7 milliseconds per 1024 bytes" vs "approximately 1.2
  milliseconds for 4.3BSD". `fork` called "substantially faster" with **no figure**.
- Says explicitly: "extensive performance comparisons with other systems have not yet been
  done"; performance "appears to be in line with 4.3BSD".
- Threads (the lead feature) NOT yet implemented — "expected by Summer 1986".
- Figure 6 caption: the UNIX compatibility box "still executes in kernel state".
- Design thesis quote: "The actual system running on any particular machine is a function of
  its servers rather than its kernel."
- MD page size on VAX 512 B; MI page size a boot-time power-of-two multiple. VAX page tables
  vs RT/PC inverted page table. 24 MB COW message example.

Multikernel (2009) — much the strongest evaluation of the three.
- Fig 3: 1 core update <30 cycles; 16 cores on same data ~12,000 *extra* cycles/update. Single
  RPC server does 2x the updates/sec of all 16 shared-memory threads combined.
- Table 1 (LRPC, same-core): 845 / 757 / 1463 / 1549 cycles = 318 / 270 / 585 / 774 ns on
  2x4 Intel / 2x2 AMD / 4x4 AMD / 8x4 AMD. (Arithmetic checks against the stated clocks:
  845/2.66=318, 757/2.8=270, 1463/2.5=585, 1549/2.0=774. Consistent.)
- Table 2 (URPC, read visually): 180 cycles (shared cache, 2x4 Intel, 11.97 msgs/kcycle) up to
  618 cycles (two-hop, 8x4 AMD, 2.75 msgs/kcycle).
- **Table 3 (read visually)**: URPC 450 cycles / 3.42 msgs/kcycle / 9 Icache + 8 Dcache lines;
  L4 IPC 424 cycles / 2.36 msgs/kcycle / 25 Icache + 13 Dcache lines.
  => URPC latency is *worse* than L4's; the wins are throughput and cache footprint.
- **Fig 6 (read visually)**, TLB shootdown protocol baselines at 32 cores: Broadcast ~13.8k
  cycles, Unicast ~12.7k, Multicast ~4.8k, NUMA-aware multicast ~3.1k (from ~1.3k at 2 cores).
- **Fig 7 (read visually)**, end-to-end unmap latency. CORRECTED in round 1 — see below.
  At 32 cores: Barrelfish ~17.5k cycles, Linux 2.6.26 ~29.5k, Windows Server 2008 R2 ~46k.
  At 2 cores: **Barrelfish ~10.3k, Linux ~5.2k, Windows ~5.8k**. Barrelfish is FLAT from 2 to
  ~5 cores, then rises gently. Growth 2->32 cores: Barrelfish 1.7x, Linux 5.7x, Windows 7.9x.
  Barrelfish crosses below Windows ~5 cores and below Linux ~12-13 cores.
  Cross-reading Fig 6 vs Fig 7: baseline messaging ~3.1k of an end-to-end ~17.5k, so >4/5 of
  the operation is Barrelfish's own monitor LRPC + marshaling + unoptimized thread dispatch.

  > **ERRATUM (validator round 1, defect 1.1).** My first pass recorded "(Barrelfish ~5.5k,
  > Linux ~5k, Windows ~10k)" at the 2-core end. That was wrong: I swapped Barrelfish and
  > Windows at the left edge. The ~5.2k point belongs to Linux and the ~10.3k flat line is
  > Barrelfish. Cause: I read Fig 7 from a 150 dpi render where the three markers at x=2 are
  > only a few pixels apart and the legend glyphs (+ / square / *) are not resolvable. At
  > 300 dpi they separate cleanly. **Lesson: for a marker-identity question, re-render at
  > higher dpi rather than upscaling a low-dpi crop — LANCZOS cannot recover glyph identity
  > that was never sampled.** The error inverted the conclusion in the deliverable: I had
  > written that the multikernel "reduced the constant", when in fact it roughly DOUBLED the
  > constant (10.3k vs Linux's 5.2k) and bought a flatter slope. The corrected reading is
  > also the one consistent with the paper's own concession at multikernel_sosp2009.txt:1128
  > that monitor RPC "adds a constant overhead ... of several thousand cycles" which is
  > "constant as the number of cores increases".
  > Verified crops: `papers/fig7_hi.png` (300 dpi full), `papers/fig7_leftedge.png`
  > (x in [2,10]), `papers/fig7_mid.png` (x in [9,23], shows the Linux crossover).
- Table 4, IP loopback on 2x2 AMD: 2154 vs 1823 Mbit/s; 21 vs 77 Dcache misses/packet;
  HT dwords/packet 467 vs 657 (src->sink) and 188 vs 550 (sink->src).
- GbE UDP echo: 951.7 Mbit/s vs Linux 951 Mbit/s (both near card saturation).
- Static 4.1 kB web page: 18697 req/s (640 Mbit/s) vs lighttpd/Linux 8924 req/s (316 Mbit/s)
  = 2.10x. But Barrelfish's e1000 driver has no TSO/checksum/scatter-gather offload while
  those were *enabled* for Linux.
- SQLite TPC-W SELECT: 3417 req/s (17.1 Mbit/s), bottlenecked at the SQLite core.
- CPU driver: 7135 lines C + 337 lines asm, 54 kB text, 370 kB static data.
- IPI/context-switch cost C ~6000 cycles; x86-64 TLB invalidate 95-320 cycles; IPI trap ~800.
- Candid admissions to quote: "it would be wrong to draw any quantitative conclusions from our
  large-scale benchmarks"; capabilities "in hindsight, this was a mistake ... unnecessarily
  complex, and no more efficient than scalable per-processor memory managers"; network stack
  "very much a placeholder"; homogeneous x86-64 only, "does not represent a truly
  heterogeneous environment"; CPU driver/monitor split "not optimal for performance", adds
  "several thousand cycles"; "the complete system is a failure unit".
- Fig 4 = spectrum of sharing/locking disciplines; mainstream OSes "moving towards the
  center", multikernel sits at "the extreme right".

## Caveat on the figure readings

Figures 6 and 7 report no data table, so the cycle counts above are read off the plotted
curves after 4x upscaling. They are good to roughly the nearest 1k cycles, and I write them
with "~" in the answer. The qualitative orderings (Barrelfish < Linux < Windows at 32 cores;
NUMA-aware multicast flattest) are unambiguous.

## Historical context used in the judgments

Not from these three PDFs — standard history, used to say what was vindicated/refuted:
Bell Labs left Multics in 1969 and UNIX followed as a reaction to its scale; x86-64 largely
abolished segmentation; Mach 3.0's user-space UNIX server was slow, Chen & Bershad (1993)
attributed the loss to memory-system behaviour rather than message path length, and Liedtke's
L4 line of work argued the cost was an implementation artefact and cut IPC by roughly an order
of magnitude; XNU (macOS/iOS) is Mach-derived; Barrelfish stayed a research vehicle while
Linux/Windows absorbed NUMA and core asymmetry with percpu data, RCU and sharding.
Liedtke's "On µ-Kernel Construction" is list paper 1-8 — cited only as one sentence of
historical context, NOT written about as one of my three papers, and not in my reference list.

## House style to match (from the brief's description of Ex 1.9)

`\section*{Ex.\ 1.0 --- ...}`, intro naming the three and why together, one `\subsection*` per
paper with run-in bold `Summary.` / `Critical judgment.`, a short comparative subsection, then
a References subsection as an enumerate with `[1] [2] [3]` custom labels. Namespace any label
`p4:`. LaTeX quotes `` '' throughout, never ASCII `"`.
