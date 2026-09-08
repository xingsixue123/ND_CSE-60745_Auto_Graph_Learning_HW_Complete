# p1 — notes

## Channel reconciliation (R7)
- `page_001.txt` / `page_002.txt`: full text of the setup + Questions A–D.
- `page_001.png` / `page_002.png`: rendered pages. Page 2 read directly (large type, legible).
  Page 1 setup bullets read via 2x LANCZOS upscaled crops (`work/crop_setup_top.png`,
  `work/crop_setup_bot.png`) because the Read tool downscales the full page.
- Figure channel: `manifest.json` reports `n_images = 0` for every page and `figures: []`.
  There is genuinely no figure file to read; the upscaled crop is the substitute. Nothing
  in this problem depends on an image.
- Result: text, render and brief agree verbatim. No discrepancy between `problem.md` and
  the assignment page.

## What this needs
**plain + code.** Four questions: A is qualitative True/False; B is an address-split
derivation; C is an inequality solved for the initial memory access time; D is a single
AMAT evaluation. No diagram is required or implied (no "plot"/"draw"/"show" verbs).
"code" = verify the arithmetic of B/C/D in python before writing it down; the code itself
must NOT appear in answer.tex.

## Conventions fixed by the statement
The hint "cache miss penalty is an additional cost **on top of** the hit time" fixes the
nested AMAT model:

    AMAT      = HT_L1 + MR_L1 * P_L1
    P_L1      = HT_L2 + MR_L2 * P_L2
    P_L2      = HT_L3 + MR_L3 * P_L3
    P_L3      = M + 10 * (additional transfers)

with HT_L1 = 1, HT_L2 = 10, HT_L3 = 50 CC, and M = initial main memory access time.
The "initial time ... accounts for a single transfer", so for a 128 B block on a 16 B bus
there are 8 transfers of which **7** are additional -> P_L3 = M + 70 CC. Do not
double-count the first transfer.
Rates given are *local* miss rates, which is exactly what the nested form consumes.
Clock 2.0 GHz -> 1 CC = 0.5 ns.

## Plan
- A: verdict + one clause each. (1) F, (2) T, (3) F.
- B: offset from 128 B block (byte addressable -> 7 bits, the 64-bit word size does not
  shrink it); sets = 512KB/(128B*4) = 1024 -> 10 index bits; tag = 64-10-7 = 47.
- C: solve 1 + 0.05(10 + 0.4(50 + 0.2(M+70))) <= 4 for M, convert to ns.
- D: carry forward M from C, bus 32 B -> 4 transfers -> 3 additional -> P_L3 = M + 30;
  evaluate AMAT in CCs.
- Verify all of B/C/D with `verify.py` (exact rational arithmetic via `fractions`).
