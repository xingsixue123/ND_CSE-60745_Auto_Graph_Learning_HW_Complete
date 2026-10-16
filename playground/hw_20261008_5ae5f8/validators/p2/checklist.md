# p2 — Ex. 3.2 (10 pts) — validator checklist

Note: `rerun/` and `vbuild/` in this directory are leftovers from the validator run
that was killed at ~03:01. No checklist was written then, so this is round 1.

## Round 1
Verdict: FAIL

### What I verified (passing)

- **Brief vs. source.** Compared programmatically, not by eye: the brief's
  "transcribed verbatim" block, unwrapped and whitespace-normalised, is byte-equal to
  line 5 of `input/os_hw_3_problems.md`. No discrepancy; the worker's claim holds.
- **R7 channels.** Genuinely inapplicable, and verifiable as such rather than taken on
  the worker's word: `ingest/manifest.json` records `os_hw_3_problems.md` as
  `kind: text_document` with **no `pages` key at all**, and
  `ingest/pages/os_hw_3_problems/` contains only `alltext.txt` — no PNG, no
  `page_*_fig_*`. I re-ran the worker's substitute check,
  `diff ingest/pages/os_hw_3_problems/alltext.txt input/os_hw_3_problems.md` →
  identical. Nothing in the answer rests on an unread figure.
- **Numbers are real.** Re-ran both worker scripts from copies in `run/`; output
  matches `answer.tex`. Then re-derived every quoted figure myself in SI units in
  `run/indep.py`, sharing no code with the worker: area 1.68e5 mm², side 409.878 mm,
  2.3767 wafers, round trip 2.7344 ns, 10.9376 cycles @ 4 GHz. **Exact match** to all
  seven values quoted in the answer, including "about 2.4 wafers", "0.41 m",
  "at least 2.7 ns" and "eleven clock cycles".
- **Citations checked against sources, not just asserted.** 0.021 µm² is confirmed as
  the TSMC N5 high-density 6T SRAM cell (WikiChip/SemiWiki, ISSCC 2020). L1/L2/L3 at
  "roughly 4, 14 and 40 cycles" is confirmed mid-range — Skylake measures 4/12/41.
- **Needs classification.** `plain` is right: "why or why not", no show/draw/plot. No
  figure invented to pad. Supporting magnitudes were computed rather than asserted,
  which is the correct handling.
- **Answers the question asked.** Verdict committed in the first word ("No."), then
  justified. The "intermediate devices" half is answered explicitly in the closing
  paragraph (front it with a small fast array = build the hierarchy inside it).
- **R8 length.** 363 words by my count (worker claims 368; tokenisation difference),
  against a 300–380 target. In range. 0 em-dashes; the single `--` is an en-dash in
  "size--speed".
- **R5 / namespacing.** No `\documentclass`, `\usepackage`, `\begin{document}`,
  `\end{document}`, `\input` or `\include`. No labels, refs, figures or macros are
  defined at all, so there is nothing that can collide with another problem.
- **Compile.** `pdflatex` on the fragment inside a minimal wrapper (amsmath, amssymb,
  graphicx, geometry): rc=0, 1 page, **0** overfull/underfull boxes, no warnings, no
  undefined references. I rendered it at 110 dpi and read the page: it sets cleanly
  and every number on the page matches the script output.
- **OUTPUT clean.** `lint_output.py` → `OUTPUT LINT OK`, rc=0. `answer.tex` only.
- **R3 downloads.** `downloads.md` present, records "(nothing installed)". Accurate:
  both scripts are pure stdlib arithmetic, no venv, no pip, no clones.

### Defects

- [1.1] `answer.tex` line 10–11 calls the **high-density** SRAM cell the **fastest**
  one: "Take the fastest cell actually manufacturable, a high-density 6T SRAM bit at
  $0.021\,\mu\mathrm{m}^2$". The HD cell is the *densest*, not the fastest — the same
  WikiChip/SemiWiki N5 source the worker cites also lists a **high-performance SRAM
  variant at 0.025 µm²**, which is the faster flavour. The question's premise is
  literally "the fastest materials available", so this is the one sentence a grader
  checks against the premise, and as written it is false.
  Direction of the error is conservative — 0.021 understates area, hence understates
  the latency floor — so no conclusion or downstream number is wrong.
  Cheapest correct fix is to relabel, not to recompute: e.g. "the densest cell in
  production ... (the faster high-performance flavour is larger still, which only
  makes the array bigger)". That keeps all seven verified numbers intact and makes the
  lower-bound framing explicit. If instead the worker switches to 0.025 µm², the
  numbers become 2.0e5 mm², 447 mm side, 2.98 ns, ~12 cycles, 2.8 wafers — all of
  which must then be re-run and re-quoted consistently.
  | `OUTPUT/answer.tex` line 10–11 | severity: minor

- [1.2] The area cross-check is presented as independent corroboration when it is
  circular. `crosscheck_area.py` lines 5–9 and the "Cross-check of the area" section of
  `submission.md` claim the two routes "share only the process node" and that the 0.7%
  agreement shows "the area does not rest on my efficiency assumption". It does rest on
  it: the published ~32 Mib/mm² top-down figure is itself derived from the same
  0.021 µm² cell by assuming ~30% assist-circuit overhead (WikiChip states exactly
  that), which is the worker's own 70% efficiency constant. Agreeing to 0.7% is close
  to arithmetic identity, not independent confirmation.
  No delivered number is affected — `answer.tex` quotes the cells-only 1.68e5 mm²,
  which carries no efficiency assumption at all — so this is a defect in the
  verification narrative, not in the answer. Fix by restating it honestly (the
  cross-check confirms internal consistency with the published density, and the quoted
  figure is assumption-free because it is cells-only).
  | `crosscheck_area.py` lines 5–9, `submission.md` "Cross-check of the area"
  | severity: minor

### Not defects (raised and withdrawn)

- The worker's own flagged worry that the 2.7 ns figure reads as a latency estimate:
  the answer says "at least ... *in vacuum*" and "real on-chip wires are several times
  slower than $c$". Correctly framed as a floor. Withdrawn.
- "At least 2.7 ns" as a lower bound: the script takes the full side one-way and
  doubles it. Checked — for a controller at a corner with Manhattan routing the mean
  round-trip flight distance is also ≈2s, so the figure is simultaneously a fair
  average and a worst-case-ish bound. Legitimate. Withdrawn.
- Cost getting only one clause: the brief explicitly warns that a cost-only answer is
  a 5-point answer and directs the physical arguments. The answer grants the cost
  premise and wins on physics, which is the stronger reading. Correct call.
- The speed-of-light term being negligible at L1/L3 sizes (0.001 ns at 32 KB per the
  worker's own §2): the answer does **not** attribute the 4/14/40 spread to light; it
  attributes it to RC, decoder depth and sense-amp resolution. No overclaim.

### Resolved since last round
(none — first round)

### Still outstanding
- [1.1] minor — "fastest cell" mislabels the high-density cell, in `answer.tex`.
- [1.2] minor — circular cross-check described as independent, in playground docs.

## Round 2
Verdict: PASS

### Resolved since last round

- **[1.1] "fastest cell" mislabel — FIXED, verified.** `answer.tex` now reads "Take the
  densest cell in production, a 6T SRAM bit at $0.021\,\mu\mathrm{m}^2$; the faster
  high-performance variant is larger at $0.025\,\mu\mathrm{m}^2$, so this keeps the
  bound conservative." I confirmed the new figure at source rather than from the
  worker's say-so: TSMC N5 offers a high-density 6T cell at 0.021 µm² and a
  high-performance (a.k.a. high-current) cell at 0.025 µm². The statement is now true,
  and the fix is better than the minimum I asked for — it makes the lower-bound logic
  explicit on the page instead of leaving it implicit, which was the real weakness.
  The worker also propagated the correction into `calc_size_latency.py` (comment block
  plus two printed strings). I verified its "label-only" claim independently by
  extracting every numeric token from the r1 and r2 script outputs: 70 tokens each,
  **identical**. No number moved.
- **[1.2] Circular cross-check — FIXED, verified.** `crosscheck_area.py` is rewritten;
  its docstring now states plainly that the two routes are "the same assumption written
  two ways" and that the earlier independence claim was wrong, and it prints the
  inversion. I reproduced that inversion myself rather than trusting the printout:
  bottom-up 0.021/0.70 = 0.030000 µm²/bit vs top-down 1e6/(32·2²⁰) = 0.029802 µm²/bit,
  ratio 1.0066 — the circularity is real and is now stated correctly. The delivered
  figure remains the assumption-free cells-only 1.68e5 mm².

### Re-verified this round (not taken on trust)

- **Numbers.** Re-ran both scripts from copies in `run2/`. All seven quoted values
  unchanged and matching `answer.tex`; they were already re-derived independently in SI
  in round 1 (`run/indep.py`), and the r1-vs-r2 numeric-token diff confirms nothing
  drifted during the edit.
- **R8 length.** 368 words by my round-1 method (up 5 from 363, consistent with the
  worker's "+13 words, minus one clause"). Checked under a second, more generous
  tokenisation that splits math into separate tokens: 380 — exactly at the ceiling, not
  over. In range under every method I tried. 0 em-dashes; the single `--` is the
  en-dash in "size--speed".
- **The cut clause.** "and no choice of material moves that floor" was removed to stay
  under the ceiling. Checked that the point survives: it is now carried concretely by
  the new HD/HP sentence (the faster cell is *larger*, so it gives a worse floor) and
  again in paragraph 3 ("It reappears with the material held fixed."). The paragraph
  still ends on the direct refutation of the premise. Nothing was lost.
- **R5 / namespacing.** No `\documentclass`, `\usepackage`, `\begin{document}`,
  `\end{document}`, `\input`, `\include`. No labels, refs, figures or macros defined at
  all — nothing can collide.
- **Compile.** Fragment in a minimal wrapper (amsmath, amssymb, graphicx, geometry):
  rc=0, 1 page, **0** overfull/underfull boxes, no warnings, no undefined references.
  Rendered at 110 dpi and read it: sets cleanly, both cell figures render correctly,
  the new sentence reads properly in place.
- **OUTPUT clean.** `lint_output.py` → OK, rc=0. `answer.tex` only.
- **R3.** `downloads.md` still accurate: nothing installed, both scripts pure stdlib.

### Defects

(none)

### Nits — noted, not blocking, no fix required

- `downloads.md` says "Three WebSearch calls were made", a round-1 count that is now
  stale (round 2 made at least one more). R3 governs *installs*, the file correctly
  records "(nothing installed)", and the note itself says a search leaves nothing on
  disk. Cosmetic.
- "six transistors per bit with static current in each" is loose — the static draw is
  leakage, not a DC path through the cell. Qualitatively right and standard for an OS
  course; rewording would be churn.

### Still outstanding

(none)
