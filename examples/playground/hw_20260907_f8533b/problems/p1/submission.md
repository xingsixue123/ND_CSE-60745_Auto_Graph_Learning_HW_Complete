# p1 — submission

## What the problem asked

CSE 60321 HW2, Problem 1 (21 pts), rendered pages 1–2. A three-level cache hierarchy on
a 2.0 GHz Xeon: 64KB L1-I, 64KB L1-D, 512KB unified L2, 8MB unified L3; 128 B blocks;
hit times 1 / 10 / 50 CC for L1 / L2 / L3; a 16-Byte processor-to-memory bus where the
L3 miss penalty is the initial memory access time (which itself covers the first
transfer) plus 10 CC per *additional* transfer.

- **A (3 pts)** — True/False on three statements.
- **B (6 pts)** — tag / index / offset split of a 64-bit physical address for the 4-way
  512KB L2, with the calculation process.
- **C (10 pts)** — with local miss rates 5% / 40% / 20%, find the maximum initial main
  memory access time such that AMAT ≤ 4 CC, answer **in nanoseconds**.
- **D (2 pts)** — same miss rates, bus widened to 32 Bytes, give the AMAT **in CCs**.

**Brief vs. assignment page: no discrepancy.** I checked all three channels per R7.
`page_001.txt` / `page_002.txt` match `problem.md`'s transcription verbatim, and the
page renders agree. The figure channel is genuinely empty — `ingest/manifest.json`
reports `n_images: 0` and `figures: []` for all 9 pages, so there is no
`page_00N_fig_NN` file to read. Because the Read tool downscales a 1275×1650 page, I did
not read `page_001.png` whole; I cropped the setup-bullet and Question-A regions and
upscaled 2× LANCZOS (`work/crop_setup_top.png`, `work/crop_setup_bot.png`) and read
those. Page 2 was legible read directly. Nothing in this problem depends on an image.

## What I decided it needed

**plain + code**, no diagram — matching the brief. Nothing here says plot/draw/show, and
there is no data to visualize. The "code" part is verification, not a deliverable: the
C bound and the D AMAT are easy to slip a factor on (the first-transfer double-count is
the obvious trap), so I recomputed everything in exact rational arithmetic rather than
trusting hand algebra. Per the brief, **no code appears in `answer.tex`.**

## What I did

Fixed the AMAT convention from the statement's hint ("miss penalty is an additional cost
on top of the hit time"): the nested model
`AMAT = HT_L1 + MR_L1·(HT_L2 + MR_L2·(HT_L3 + MR_L3·P_L3))`, stated explicitly in the
answer before it is used, since Question C's 10 points are for the derivation. Read the
bus model as: the initial access time `M` already covers the first 16-B transfer, so a
128-B block charges `10 × (128/16 − 1) = 70` CC of additional transfers, not 80.

- **A** — reasoned qualitatively; one clause of justification each, not padded.
- **B** — offset from the 128-B block (7 bits); explicitly argued that "Byte
  addressable" means the 64-bit word size does *not* shrink the offset, since the grader
  put that sentence in on purpose; sets = 512KB/(128 B × 4) = 1024 → 10 index bits; tag
  = 64 − 10 − 7 = 47. Checked the three sum to 64.
- **C** — unwound the inequality one level at a time to bound `P_L1`, `P_L2`, `P_L3`,
  then subtracted the 70 CC of additional-transfer cost to isolate `M`, then converted
  at 1 CC = 0.5 ns.
- **D** — carried `M = 305` CC forward (stated explicitly so the grader can follow),
  recomputed with 128/32 = 4 transfers → 3 additional → `P_L3 = 335` CC.
- Test-compiled the fragment in a throwaway wrapper **in the playground** and read all
  three rendered pages to proofread the output. Second `pdflatex` pass is warning-free.

## Intermediate steps and code

All paths relative to PLAYGROUND.

- `verify.py` — the only computational artifact. Exact `fractions.Fraction` arithmetic
  (no floating point) for B, C and D. Reproduces every number in the answer:
  **`python3 verify.py`**. It is self-checking, not just self-reporting:
  - asserts tag + index + offset == 64;
  - asserts the C bound by **back-substitution** — `amat(305, 16) == 4` exactly;
  - asserts the bound is **tight** — `amat(306, 16) > 4`;
  - asserts each cache size / set count is a power of two before taking a log.
- `notes.md` — the up-front decision record (needs, conventions, plan) written before
  solving.
- `work/crop_setup_top.png`, `work/crop_setup_bot.png`, `work/crop_qA.png` — 2×
  upscaled crops of `page_001.png` used to read the setup bullets (R7 channel 2).
- `work/wrap.tex`, `work/wrap.pdf`, `work/pg-{1,2,3}.png` — throwaway compile wrapper
  and page renders used to proofread the fragment. Playground only; not in OUTPUT.

## Results

Every value below comes from `python3 verify.py` and is reproduced by hand in the answer.

| Claim in `answer.tex` | Value | Source |
|---|---|---|
| B: block offset | **7 bits** (`log2 128`) | `verify.py`, Question B block |
| B: L2 blocks | 4096 (`2^19 / 2^7`) | same |
| B: L2 sets | 1024 = `2^10` (4096 / 4 ways) | same |
| B: index | **10 bits** | same |
| B: tag | **47 bits** (`64 − 10 − 7`) | same, asserted to sum to 64 |
| C: additional transfers, 16 B bus | 7 (`128/16 − 1`) | `verify.py`, Question C block |
| C: `P_L3 ≤` | 375 CC | same |
| C: `P_L2 ≤` | 125 CC | same |
| C: `P_L1 ≤` | 60 CC | same |
| C: **max initial memory access time** | **305 CC = 152.5 ns** | same; back-substitution gives AMAT exactly 4 CC |
| D: additional transfers, 32 B bus | 3 (`128/32 − 1`) | `verify.py`, Question D block |
| D: `P_L3` | 335 CC | same |
| D: `P_L2` | 117 CC | same |
| D: `P_L1` | 56.8 CC | same |
| D: **AMAT** | **3.84 CC** (exactly 96/25) = 1.92 ns | same |

Question A verdicts (qualitative, no computation): **(1) False, (2) True, (3) False.**

## Deliverables

- `OUTPUT/p1/answer.tex` — LaTeX fragment. Starts at `\section{Problem 1 (21 points)}`
  with a `\subsection*` per question A–D. No `\documentclass`, no `\usepackage`, no
  `document` environment (grep-checked). Both labels namespaced: `p1:eq:amat`,
  `p1:eq:pl3`.
- `OUTPUT/p1/preamble.txt` — `amsmath`, `amssymb`, `booktabs`.
- No figures (none required).
- `python3 framework/tools/lint_output.py output/hw_20260907_f8533b/p1` → **OUTPUT LINT OK**, exit 0.

## Where I am least confident

1. **Question A(2) is the weakest item.** The statement is about *cost*, and the
   intended reading is almost certainly cost-per-byte of the SRAM technology (L1 uses
   fast, low-density, heavily-ported cells; L3 uses dense, latency-tolerant ones), which
   makes it **True** — this is the standard textbook point. But "more expensive" is not
   defined in the question, and someone could argue *total* cost the other way, since the
   8 MB L3 occupies far more die area in absolute terms than 64 KB of L1. I answered the
   per-unit-capacity reading because the statement says "a certain amount ... the same
   amount", which explicitly holds capacity fixed. I think this is right, but it is a
   wording judgment, not a calculation.

2. **The first-transfer convention in Question C/D.** I read "the initial time required
   to access memory, which accounts for a single transfer" as meaning `M` covers transfer
   #1, giving 7 additional transfers on a 16 B bus (not 8). The brief agrees, and the
   phrase "for every *additional* transfer" supports it. If a grader instead intended 8
   × 10 = 80 CC, then C becomes `M ≤ 295` CC = 147.5 ns and D becomes 3.80 CC. I am
   fairly confident in my reading, but this is the single assumption the whole numeric
   answer pivots on, so it is worth an explicit look. I stated the convention in the
   answer so a grader can see which one I used.

3. **Question D's carried-forward `M`.** The question says only "the same local miss
   rates", not "the same memory access time". I used `M = 305` CC because it is the only
   value of `M` in play and the brief says the same; the resulting 3.84 CC is a clean
   number, which is weak corroboration that it is the intended path. If the intent were
   instead "re-solve for the new maximum `M` under a 4 CC budget", the answer would
   trivially be 4 CC, which would make the question pointless — so I am confident the
   carry-forward is right.

4. Not a correctness worry, but noting it: the AMAT model treats a single unified stream
   with one L1 miss rate, ignoring the split I-cache/D-cache. The question supplies one
   L1 miss rate, so that is clearly what is intended; there is no instruction/data mix
   given that would let anyone do otherwise.
