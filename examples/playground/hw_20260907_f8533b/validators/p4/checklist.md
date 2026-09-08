# p4 — validator checklist

## Round 1
Verdict: PASS

### What I verified (independently, not by reading the worker's reasoning)

**Ground truth (R7, all three channels).**
1. *Text* — read `ingest/pages/Homework_2/page_005.txt` in full. Matches the master's
   brief verbatim; no transcription discrepancy.
2. *Page image* — did NOT trust the downscaled whole-page render. Cropped the Question A
   setup (`Rect(50,60,560,240)`) and the Question B paragraph (`Rect(50,448,560,600)`)
   out of the source PDF at 5x myself (`vA2.png`, `vB.png`) and read them. Confirmed:
   A = 1MB / 64-Byte block / 110 / 90 / 10 / 30%; B = 32 KB / 32-Byte block / 27 / 4 / 20%;
   shared "a word is 8 Bytes wide". Every constant the worker used is right.
3. *Figures* — verified there are none rather than accepting `n_images = 0`.
   `get_images(full=True)` returns `[]` on all 9 pages. Page 5 has 14 vector drawings, so
   I enumerated their geometry: all are thin horizontal rules (full-width header bars at
   y=54/143/434/611, plus the underline under "on average", plus the two fill-in-the-blank
   rules at [352.6,534.8,413.7,535.6] and [90.7,572.7,151.9,573.5]). No figure content.
   Nothing in the answer rests on an unread image.

**Numbers — recomputed independently in `indep.py`, written from the page text rather
than from the worker's model, then compared against a re-run of the worker's `solve.py`.**
All agree exactly:

| Claim | Independent result | Match |
|---|---|---|
| A: n = 64/8 | 8 words | yes |
| A(1) neither = 90+7(10) | 160 CCs | yes |
| A(2) ER only = 0.3(90)+0.1(910) | 118 CCs | yes |
| A(3) both | 110 CCs | yes |
| A savings | 26.25% / 31.25% | yes |
| B: n = 32/8 | 4 words | yes |
| B blank 1 | 18 CCs | yes |
| B blank 2 | 10% | yes |
| C: uniform-L2 counterfactual | 125 CCs, 21.875% | yes |
| C: CWF surcharge 20/160, 9/30 | 12.5% / 30% | yes |
| C: free-CWF ceiling 70/160, 12/30 | 43.75% / 40% | yes |
| C: break-even 50/3 | 16.67 → "above ~16:1" | yes |

For B I deliberately avoided the worker's method: instead of a sympy solve I brute-forced
every integer x in [1,2000) against the exact rational condition. x = 18 is the **unique**
solution. The decomposition in C factor 3 is also exact, not a coincidence:
43.75 − 12.5 = 31.25 and 40 − 30 = 10.

**The one interpretation risk, checked rather than accepted.** "With critical-word first
it takes 110 CCs to get the first word" could mean flat-110, or 110 only when the
requested word is not already word 0. The worker took flat. I confirmed its
cross-check independently: under the mixed reading B's second blank is 17.5%, and B
demands *integers*, so the flat reading is the intended one. Note the cross-check is
sound because B's first blank (18) is derived from the ER-only 20% and is therefore
independent of the CWF interpretation. Flat is also the textbook-standard reading.
Verdict: not a defect. The assumption is stated in `answer.tex` where it is used
(lines 75–76), which is the right amount of disclosure for a homework submission.

**Work actually done.** `needs: plain + code`. Code exists, runs, and reproduces every
number in `answer.tex`; no figure was required and none is claimed. No fabricated values —
every number in the answer traces to script output.

**LaTeX / R5.** No `\documentclass`, `\usepackage`, or `document` environment. All three
labels namespaced (`p4:eq:none`, `p4:eq:er`, `p4:eq:both`); no other labels, no figures,
no macros, so no collision surface. Subsections per Question A/B/C, satisfying the
assignment front matter ("clearly indicate which question an answer is for").
Compiled myself in two minimal wrappers: with the full `preamble.txt` and with a bare
`amsmath`+`booktabs` one. Both exit 0, 3 pages, **zero** errors, zero undefined
references, zero overfull/underfull boxes. Rendered all 3 pages to PNG and read them:
both tables and all boxed answers are legible and correctly aligned.

**R4 / R3.** `lint_output.py` exits 0; OUTPUT holds only `answer.tex` + `preamble.txt`.
All scratch (`build/`, `crops/`, `solve.py`) is correctly confined to PLAYGROUND.
`downloads.md` present and correctly records "(nothing installed)" — I confirmed no venv,
no pip cache, no clone in the playground.

**Worker's environment finding — independently reproduced.** I compiled a bare
`\begin{itemize}` document under default Computer Modern: it fails with
`!pdfTeX error: pdflatex (file tcrm1000): Font tcrm1000 at 600 not found`, because
`~/.TinyTeX/texmf-var` is read-only. The claim is real, correctly diagnosed, and the
worker's double mitigation (fragment avoids `itemize`; `lmodern` requested in
`preamble.txt` to protect the master) is the right response. Worth propagating —
this is not in `env.md`.

### Defects
None blocking, major, or minor that require action.

### Non-blocking observations (recorded, no action required)
- `enumitem` and `lmodern` in `preamble.txt` are not strictly needed by this fragment
  (I confirmed it compiles without them). Harmless — `lmodern` is deliberate defensive
  cover for the `itemize` bug above, and the master de-duplicates preambles.
- The worker's three self-declared low-confidence points were each examined and none is
  a defect: (1) the flat-CWF reading is confirmed by B's integrality; (2) C's factor-5
  miss-frequency caveat is explicitly scoped to "per miss, which is what this problem
  measures" and quantified, so it does not violate the hint's consistency requirement —
  it strengthens the answer; (3) the page-break gap was an artefact of the worker's test
  wrapper and does not appear in mine.

### Resolved since last round
n/a — first round.

### Still outstanding
Nothing.
