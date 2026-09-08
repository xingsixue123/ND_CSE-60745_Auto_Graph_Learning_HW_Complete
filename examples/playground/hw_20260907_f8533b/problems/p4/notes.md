# p4 — notes

## Channel reconciliation (R7)
- `page_005.txt` — full prose, matches `problem.md` verbatim.
- `page_005.png` — verified by cropping the two numeric-dense paragraphs out of the
  source PDF at 5x (`crops/qA_l.png`, `qA_r.png`, `qB_l.png`, `qB_r.png`) and reading
  those, rather than the downscaled whole page. All constants confirmed:
  64-Byte block / 1MB / 110 / 90 / 10 / 30% (A); 32 KB / 32-Byte / 27 / 4 / 20% (B).
- Figure channel — `manifest.json` reports `n_images = 0` for all 9 pages, and
  `page.get_images(full=True)` on page 5 returns `[]`. There is genuinely no figure.
  Nothing rests on an unread image.
- No discrepancy between the brief and the page.

## What it needs
**plain + code.** No diagram (nothing asks to plot/draw/show). The credit is in the
derivations; code is used only to check the weighted sum in A(2) and the inverse
solve in B, both of which are easy to slip. Code stays out of `answer.tex`.

## Interpretation decision (the one real judgement call)
"With critical-word first, it takes 110 CCs to get the first word from memory" is read
as a **flat** cost: under CWF the requested word is delivered first and that delivery
costs 110 CCs, whatever the word's position in the block. The alternative reading
(CWF is a no-op when the requested word already is word 0, so 90 CCs in that case)
gives 0.3*90+0.7*110 = 104 CCs in A(3).

The flat reading is confirmed independently by Question B: B demands "the most
appropriate **integers**". With the flat reading B's second blank is exactly 10%;
with the mixed reading it is 17.5%, not an integer. So the flat reading is the
intended one, and A and B are consistent under it.

## Environment finding worth propagating (not in env.md)
`\begin{itemize}` **does not compile on this machine** with the default Computer Modern
fonts. The bullet resolves to a TS1-encoded glyph, pdfTeX tries to build the bitmap font
`tcrm1095` via mktexpk, and that write fails because `~/.TinyTeX/texmf-var` is read-only:

    !pdfTeX error: pdflatex (file tcrm1095): Font tcrm1095 at 600 not found

`enumerate` and `description` are unaffected (verified: `build/e_*.tex`).
`\usepackage{lmodern}` fixes `itemize` outright (verified: `build/d_lmodern_fix.tex`).
Mitigation taken on both fronts: this fragment uses `description`/`enumerate` and no
`itemize`, so it compiles even under a bare CM preamble, **and** `lmodern` is requested
in `preamble.txt` so the master document is protected if another problem uses `itemize`.

## Plan
1. n_words = block / 8 for each level.
2. A: three schemes; only (2) is a genuine expectation.
3. B: back-solve x from the given 20% early-restart reduction, then compute blank 2.
4. C: verdict driven by the percentages A and B produce, not textbook recital.
