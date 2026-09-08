# p4 — submission

## What the problem asked

Problem 4 (16 pts), rendered page 5 of `Homework_2.pdf`. Critical-word first (CWF) and
early restart (ER) as miss-penalty reductions, with a word of 8 Bytes throughout.

- **A (8 pts)** — L2, 64-Byte block, first word 90 CCs without CWF, 10 CCs per additional
  word, 110 CCs for the critical word with CWF; P(first word) = 30%, the other words
  equally likely. Give the average miss service time under (1) neither, (2) ER only,
  (3) both, with the calculation process.
- **B (4 pts)** — L1, 32-Byte block, CWF first word 27 CCs, 4 CCs per additional word,
  uniform reference probability. Fill two integer blanks: the non-CWF first-word latency,
  and the % reduction from applying both. The given fact "ER alone reduces 20%" is what
  pins the first blank.
- **C (4 pts)** — Is CWF+ER more important for L1 or L2? Verdict + at least one reason +
  the factors driving relative importance. Hint says any consistent answer is accepted.

**Brief vs. page: no discrepancy.** The master's transcription matches the page verbatim.

**R7 three-channel reconciliation.**
1. Text — `ingest/.../page_005.txt`, read in full; matches the brief word for word.
2. Page image — I did *not* rely on the downscaled whole-page render. I cropped the two
   numeric-dense paragraphs straight out of the source PDF at 5x and read those
   (`crops/qA_l.png`, `crops/qA_r.png`, `crops/qB_l.png`, `crops/qB_r.png`). Every
   constant confirmed visually: 1MB / 64-Byte / 110 / 90 / 10 / 30% (A) and
   32 KB / 32-Byte / 27 / 4 / 20% (B).
3. Figures — **there are none, and I verified that rather than assuming it.**
   `manifest.json` reports `n_images = 0` for all 9 pages, and `page.get_images(full=True)`
   on page 5 returns `[]`. Nothing in this answer rests on an unread image.

## What I decided it needed

**plain + code.** No diagram: nothing asks to plot, draw, show or visualize, and there is
no data worth a figure. The marks are in the derivations, so `answer.tex` carries the
derivations and no code. Code was used only to check the arithmetic — the weighted sum in
A(2) and the inverse solve in B are both easy to slip — using exact `Fraction`/`sympy`
rationals so rounding cannot mask an error.

## What I did

Reduced all three schemes to one small model: with $n = B/8$ words per block, word $i$
arrives at $t_1 + i\,t_x$ without reordering, so "neither" $= t_1+(n-1)t_x$, "ER only"
$= \sum_i p_i (t_1+i t_x)$, "both" $= t_c$ flat. Then instantiated it per level. For B I
inverted the model: expressed both times as functions of the unknown first-word latency
$x$, set $(T_\text{none}-T_\text{ER})/T_\text{none} = 20\%$, and solved for $x$. For C I
put A's and B's percentage savings side by side and let the verdict follow from them.

**The one real judgement call**, and how I settled it: "with critical-word first it takes
110 CCs to get the first word" could mean a flat 110 CCs always, or 110 only when the
requested word is not already word 0 (CWF being a no-op in that case). I took the flat
reading. It is confirmed independently by Question B, which demands *integer* blanks: the
flat reading gives exactly 10%, the alternative gives 17.5%. So B validates the
interpretation used in A. This cross-check is printed by `solve.py`.

## Intermediate steps and code

Paths relative to PLAYGROUND.

- `solve.py` — the only script that produces results. Exact rational arithmetic; asserts
  that the probabilities sum to 1, that B's back-solve returns an integer, and that B's
  closed-form ER mean equals an explicit per-word average. Reproduces **every** number in
  `answer.tex`. Run: `python3 solve.py`.
- `notes.md` — channel reconciliation, the interpretation decision, and an environment
  finding (below).
- `crops/*.png` — 5x crops of page 5's two numeric paragraphs, used for channel 2.
- `build/` — LaTeX scratch: `f_withpre.tex` / `f_nopre.tex` are the two compile checks,
  `r*.png` the rendered pages I inspected, `b_*/c_*/d_*/e_*` the font-bug bisection.

## Results

Every computed value in `answer.tex`, all from `python3 solve.py`:

| Claim in answer.tex | Value | Source |
|---|---|---|
| A: words per block | 8 | `64/8` |
| A(1) neither | **160 CCs** | `90 + 7*10` |
| A(2) early restart only | **118 CCs** | `0.30*90 + 0.10*910 = 27+91` |
| A(3) both | **110 CCs** | flat $t_c$ |
| A: saving, ER only | 26.25% | `42/160` |
| A: saving, both | 31.25% | `50/160` |
| B: words per block | 4 | `32/8` |
| B: **blank 1** | **18 CCs** | sympy solve of `6/(x+12)=0.20` |
| B: derived $T_\text{none}$, $T_\text{ER}$ | 30, 24 CCs | `x+12`, `x+6` |
| B: **blank 2** | **10%** | `(30-27)/30` |
| C: L2 uniform-distribution counterfactual | 125 CCs, 21.875% | expectation with $p_i=1/8$ |
| C: CWF surcharge, L2 / L1 | 20 CC (12.5%) / 9 CC (30%) | `t_c - t_1` over block time |
| C: ceiling if CWF were free | 43.75% / 40% | `(n-1)t_x / T_none` |
| C: absolute saving | 50 CCs / 3 CCs | `160-110`, `30-27` |
| C: break-even miss ratio | ~16:1 | `50/3` |

**Question C verdict: more important for L2**, driven by 31.25% vs 10%, plus the sharper
point that at L1 CWF actively *hurts* (ER alone 24 CCs → 27 CCs with CWF added), because
its 9 CC surcharge exceeds the 6 CC ER had saved, whereas at L2 it improves 118 → 110.

## Deliverables

- `OUTPUT/p4/answer.tex` — fragment, starts at `\section`; no documentclass/usepackage/
  document env. Subsections for A, B, C as the assignment's front matter requires. All
  three equation labels namespaced (`p4:eq:none`, `p4:eq:er`, `p4:eq:both`).
- `OUTPUT/p4/preamble.txt` — `lmodern`, `amsmath`, `booktabs`, `enumitem`.
- No figures (none required).

**Verification of the deliverable, not just of the maths:** `lint_output.py` passes
(exit 0). The fragment was compiled twice to a real PDF — once with my `preamble.txt` and
once *without* `lmodern` — both with 0 errors and 0 undefined references, and I read the
rendered pages to check the two tables and the boxed answers are legible and aligned.

**Environment finding the validator may want to propagate:** `\begin{itemize}` does not
compile on this machine under default Computer Modern. The bullet needs a TS1 glyph,
pdfTeX tries to generate bitmap font `tcrm1095`, and the write fails because
`~/.TinyTeX/texmf-var` is read-only — a fatal "Font tcrm1095 at 600 not found", no PDF.
`enumerate` and `description` are unaffected; `\usepackage{lmodern}` fixes `itemize`.
I hit this, bisected it (`build/c_*`, `build/d_*`, `build/e_*`), and covered it twice:
this fragment uses no `itemize`, so it compiles even under a bare CM preamble, and
`lmodern` is in `preamble.txt` to protect the master if another problem uses one.
This is not in `env.md`.

## Where I am least confident

1. **The flat-cost reading of CWF in A(3)** is the load-bearing assumption. I believe the
   integrality cross-check from B settles it, but if a grader intended CWF to be a no-op
   when the requested word is already word 0, A(3) becomes
   $0.3(90)+0.7(110) = 104$ CCs, and A's "both" saving becomes 35%. A(1) and A(2) are
   unaffected either way, and C's verdict would only strengthen. I state the flat
   assumption in the answer where it is used, but I did not enumerate the alternative in
   `answer.tex` — I judged that hedging would read as indecision on a homework
   submission. Reasonable people could want it mentioned.
2. **Question C is a judgement question**, so "L2" is not provably right — the hint says
   only that it must be consistent. My factor 5 openly concedes that miss *frequency* is
   the one thing that could tip it the other way, and quantifies the ~16:1 break-even.
   That ratio is genuinely reachable in real machines (L1 MPKI usually far exceeds L2
   MPKI), so someone could argue L1 from a full-AMAT angle. I kept the verdict anchored
   to the per-miss latency reduction, which is what the problem actually computes, and
   flagged the caveat rather than hiding it. If the validator thinks naming that caveat
   weakens internal consistency, it is a one-paragraph change — but I think an honest
   boundary is worth more than a tidier-looking argument.
3. **Presentation, not correctness:** in my standalone test compile a page break leaves a
   gap above "(3) Both..." on page 2. That is an artefact of my test wrapper's geometry;
   the master's document will flow differently, and I deliberately added no manual page
   breaks, since those would be actively harmful once the fragment is assembled.
