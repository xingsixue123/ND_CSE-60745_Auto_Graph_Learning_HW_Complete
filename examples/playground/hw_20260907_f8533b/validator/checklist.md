# Master validator checklist — hw_20260907_f8533b

Assignment: CSE 60321 Advanced Computer Architecture, Spring 2026, Homework 2 (100 pts).
specs.md instruction: **skip Problem 5** (45 pts); answered scope is Problems 1–4 = 55 pts.

---

## Round 1 — 2026-09-08

Verdict: **PASS** (with minor defects noted)

### What I did

Rather than trust `problems.json`, I enumerated the questions myself from the
assignment's own rendered pages (`ingest/pages/Homework_2/page_00N.png` + `.txt`),
then diffed my list against the answered document. I re-derived every numeric answer
from the problem statements with an independent script before reading the master's
arithmetic, and read the final PDF through both channels (9 page renders + extracted
text).

Channel reconciliation (R7): the ingest manifest reports `n_images = 0` on all 9
assignment pages, and my own read of the page renders confirms it — the only graphics
are ruled vector tables and the black/gray section-header bars. No question in this
assignment refers to a figure, so there is no figure channel to reconcile and the text
channel is complete. Where text extraction mangled the layout (Table 1/Table 2 of
Problem 2 came out as loose column headers followed by loose values), I read the values
off the page render instead: 30 bits / 2 GB / 64 KB / 4 Bytes. Both channels agree.

### Coverage — my own enumeration vs. what was answered

| Question | Pts | Answered? | Where in main.pdf |
|---|---|---|---|
| P1 A (3 T/F statements) | 3 | yes, all three | p.1–2 |
| P1 B (tag/index/offset) | 6 | yes | p.2 |
| P1 C (max initial memory access time, ns) | 10 | yes | p.2–3 |
| P1 D (AMAT with 32-B bus, CCs) | 2 | yes | p.3 |
| P2 A (fill Table 2) | 2 | yes | p.4 |
| P2 B (PTE count + page-table size) | 4 | yes | p.4 |
| P2 C (≥1 pro, ≥1 con) | 4 | yes (2 + 2) | p.4 |
| P3 A (best/worst case ns) | 2 | yes, both blanks | p.5 |
| P3 B (min prediction accuracy) | 6 | yes | p.5–6 |
| P4 A (three schemes) | 8 | yes, all three | p.6–7 |
| P4 B (two integer blanks) | 4 | yes, both | p.7–8 |
| P4 C (L1 vs L2 + reasons) | 4 | yes | p.8–9 |
| P5 A–F | 45 | intentionally omitted | declared on p.1 |

Points cross-check: 3+6+10+2 = 21 (P1); 2+4+4 = 10 (P2); 2+6 = 8 (P3); 8+4+4 = 16 (P4).
Total answered 55; omitted 45; 55+45 = 100, matching the assignment header. No sub-part
is missing, including the multi-blank questions (P1 D, P3 A two blanks, P4 B two blanks)
which are the usual place sub-parts get dropped.

specs.md compliance: P5 is recorded under `uncovered` in problems.json with a reason,
and the final document states the omission exactly once, in the boxed scope note on
page 1. Both requirements met. Assignment front-matter requirement "clearly indicate
which question an answer is for" is met — every answer sits under a
`Problem N` / `Question X (n points)` heading.

### Correctness — independent recomputation

Recomputed with exact rational arithmetic, from the problem statements, without
reading the submitted derivations first. Every value matches.

- P1 B: offset log2(128) = **7**; blocks 2^19/2^7 = 4096; sets 4096/4 = 2^10 → index
  **10**; tag 64−10−7 = **47**. Sums to 64. ✔
- P1 C: P_L3 = M+70 (8 transfers, 7 additional). 1+0.05[10+0.4(50+0.2(M+70))] ≤ 4
  ⟹ M ≤ 305 CC; at 2.0 GHz (0.5 ns/CC) → **152.5 ns**. ✔ Bound is tight (AMAT = 4
  exactly at M = 305), which the submission also verifies.
- P1 D: 4 transfers, 3 additional → P_L3 = 335; P_L2 = 117; P_L1 = 56.8;
  AMAT = **3.84 CC**. ✔ Cross-checked by the differential: Δ = 0.05·0.4·0.2·(−40)
  = −0.16, and 4 − 0.16 = 3.84. Carrying M = 305 CC forward from C is the only
  sensible reading of "assuming the same local miss rates in Question C".
- P2 A: offset **16**, VPN **14**, total **30**. ✔
- P2 B: 2^14 = **16,384 entries**, 2^14 × 4 B = 2^16 B = **64 KB**. ✔ The 2 GB physical
  memory size is a distractor and the answer correctly says so.
- P3 A: best **1 ns**, worst 1 + 1.1 = **2.1 ns**. ✔
- P3 B: baseline 1.1 + 0.01·50 = 1.6 ns; wp 2.6 − 1.1a ≤ 0.95·1.6 = 1.52
  ⟹ a ≥ 1.08/1.1 = **54/55 = 98.1818…%**. ✔
- P4 A: n = 8 words. Neither 90+70 = **160 CC**; early restart 0.3·90 + 0.1·910
  = **118 CC**; both = **110 CC**. ✔ Also verified the submission's side-claim that a
  uniform 1/8 distribution would give 125 CC. ✔
- P4 B: n = 4, T_none = x+12, T_ER = x+6; 6/(x+12) = 0.20 ⟹ **x = 18 CC**;
  (30−27)/30 = **10%**. ✔ Both blanks are integers, as the question demands.
- P4 C: verdict "more important for L2" with consistent supporting numbers
  (43.75% vs 40% ceiling; 12.5% vs 30% CWF surcharge; 31.25% vs 10% net). I checked
  each of these arithmetically and the 16:1 break-even claim (50/3 = 16.67). The hint
  allows any consistent answer; this one is internally consistent and correct.

### The PDF itself

- Compiles. `build/main.log` (299 lines) contains **zero** Overfull, Underfull,
  Warning, or Undefined-reference messages. 9 pages, letter size, pdfTeX 1.40.29.
- `final/main.pdf` is byte-identical to `build/main.pdf`, and all five `.tex` sources
  in `final/` md5-match the ones actually compiled — the delivered PDF is not stale
  relative to the delivered sources.
- Read all 9 rendered pages. No margin overflow, no runaway math, no missing-file
  boxes (there are no figures), no `??` in the extracted text, no duplicated or
  orphaned sections from a bad `\input`. Section order is P1→P2→P3→P4.
- Preamble merge is correct and de-duplicated: the union of the four workers'
  `preamble.txt` files is {lmodern, amsmath, amssymb, booktabs, float, enumitem},
  which is exactly `final/preamble.tex`.
- Labels are namespaced per R5 (`p1:eq:amat`, `p3:eq:wp`, `p4:eq:none`, …); I found no
  collisions, consistent with the clean log.
- Master's edits to the worker fragments were limited to section titles plus one table
  caption (diffed all four); no content was altered in assembly.

### Defects

- [D1.1] **minor** — Altitude. Problem 4 Question C is worth 4 points and asks for a
  verdict plus reasons; the answer runs to roughly a page and a half with a comparison
  table and five enumerated factors (`final/p4.tex:133–191`, PDF pp.8–9). Item 5 in
  particular introduces a full-AMAT miss-frequency caveat that argues partly against
  the stated verdict. It is not wrong and the hint does ask "what factors", plural, but
  it is longer than the question warrants. Would be resolved by trimming to two or
  three factors. Not grounds for failing.
- [D1.2] **minor** — Presentation of the P3 B answer. The headline boxed value is
  `≈ 98.19%` (rounded up), whereas the exact threshold is 54/55 = 98.1818…%. A grader
  keying on "98.18%" may pause. Mitigated: the exact fraction 54/55 and the reason for
  rounding up (98.18% would give 1.52002 ns and miss the budget) are both stated
  immediately, and the check at a = 54/55 is shown. No action strictly required.

### Considered and withdrawn

- `python3 framework/tools/lint_output.py output/hw_20260907_f8533b/final` exits with
  8 complaints (no `answer.tex`; `main.tex`, `main.pdf`, `p1–p4.tex`, `preamble.tex`
  "not an allowed deliverable"). I am **not** recording this as a defect. R4's file
  whitelist governs the per-problem worker deliverable directories, which is where the
  linter is pointed by the worker rules; `final/` is by construction the assembled
  document plus its sources. The four worker dirs `p1/`–`p4/` each contain exactly
  `answer.tex` + `preamble.txt` and each pass the linter cleanly, and `final/` carries
  no `.aux`/`.log`/`.fls`/`.fdb_latexmk` scratch — those were correctly left in
  `playground/.../build/`. Nothing to fix.

### Where I looked and found nothing

Coverage diff against my own question enumeration; independent recomputation of all 13
numeric answers; both PDF channels across all 9 pages; the LaTeX log for silent layout
failures; source/PDF staleness; preamble merge; label namespacing; worker-fragment
diffs; specs.md's three P5 requirements. No blocking or major defect survived.

### Resolved since last round

(none — first round)

### Still outstanding

D1.1, D1.2 — both minor, both recorded, neither blocking.
