# Validator checklist — p2

## Round 1
Verdict: FAIL

### What I verified (passing)

- **Brief vs. ground truth (R7).** Read `page_003.txt` and `page_003.png` myself. Every
  value in the brief matches the page: 30-bit VA, 2 GB, 64 KB, 4 Bytes; Table 2 with
  only `Total / bits = 30` pre-filled; the "Virtual page memory (VPN)" header typo is
  genuine. Third channel: `ingest/pages/Homework_2/manifest.json` reports
  `n_images = 0, figures: []` for all 9 pages and `find` returns no `*fig*` files, so the
  figure channel is vacuously empty — nothing here rests on a figure. Unit convention
  confirmed independently at `page_001.txt` line 16-17 (1KB = 2^10 Bytes).
- **Numbers are real.** Re-ran the worker's `check.py` from my own dir — output matches
  the submission's results table exactly. Then re-derived everything independently with
  pure bit arithmetic (no `log2`, no worker code): offset 16, VPN 14, PTEs 2^14 = 16384,
  table 2^16 B = 64 KB. Extra cross-check the worker did not do: 2^30 B / 64 KB = 16384
  pages == PTE count. PPN = 15 bits, 32768 frames. The Question C claim (128 KB page ->
  13-bit VPN -> 32 KB table, i.e. halved) also verifies.
- **Correct interpretation.** Entry count is driven by the virtual address space; the
  2 GB physical size is correctly treated as a distractor.
- **Right kind of work.** `needs: plain`; no plot/draw/show verb anywhere in A/B/C, so no
  diagram is owed. No code in `answer.tex`. All three sub-parts answered, C with 2 pros +
  2 cons that name mechanisms and are genuinely opposed.
- **Table fidelity.** Renders with the original's three headers and 16 / 14 / 30; caption
  is LaTeX-numbered, not hard-coded as "Table 2", as the brief required.
- **R5/R4/R3.** No `\documentclass`/`\usepackage`/`document` env in `answer.tex`. Sole
  label `p2:tab:vaddr` is namespaced. No figures, no absolute paths.
  `lint_output.py` exits 0. `downloads.md` present and records "(nothing installed)".

### Defects

- **[1.1] `answer.tex` uses `\text{}` but `preamble.txt` never declares `amsmath`, so the
  fragment does not compile.** | `OUTPUT/p2/answer.tex` lines 4, 9, 34 (five `\text{}`
  uses); `OUTPUT/p2/preamble.txt` (declares only `booktabs`, `float`) | severity: **blocking**

  Compiling the shipped fragment in a minimal wrapper carrying exactly the two declared
  packages gives:

      ! Undefined control sequence.
      l.4 $64\text
                  { KB} = 2^{16}$ Bytes and $2\text{ GB} = 2^{31}$ Bytes.
      ! ==> Fatal error occurred, no output PDF file produced!

  `\text` comes from `amsmath`/`amstext`. Adding `\usepackage{amsmath}` and nothing else
  makes it compile clean (exit 0, 1 page, zero `!` lines), so this is the only missing
  declaration.

  Why the worker missed it: its own check wrapper
  `problems/p2/build/master.tex` line 3 loads `\usepackage{amsmath,amssymb}` — packages it
  did not put in `preamble.txt`. The build copy of `answer.tex` is byte-identical to the
  shipped one (`diff` clean), so the file is fine; the *compile check was invalid*
  because it was run against a richer preamble than the one declared. The submission's
  claim "pdflatex exits 0, one page, no errors" is true only of that private wrapper.

  The master merges and de-dupes `preamble.txt` lines from all problems. If no other
  problem happens to declare `amsmath`, the entire assembled document dies with a fatal
  error. Relying on a sibling problem to declare a package you need is not acceptable.

  Fix: add `\usepackage{amsmath}` to `OUTPUT/p2/preamble.txt`. (Alternative: drop the
  `\text{}` uses in favour of `\mathrm{}`/plain prose — but declaring the package is
  simpler and matches R5.)

- **[1.2] Results table in `submission.md` overstates its provenance.** |
  `problems/p2/submission.md` line 67 ("All from `python3 check.py`") vs. line 76 | severity: minor

  The row "C, pro 1: 128 KB page -> 13-bit VPN, table 32 KB" is not computed by
  `check.py`, which only ever evaluates the 64 KB case. I verified the number is correct
  independently, so this is a documentation defect, not a wrong answer — but a results
  table that attributes an uncomputed value to a script output is how fabricated numbers
  get laundered. Either extend `check.py` to sweep the page size or mark that row as
  hand-derived.

### Resolved since last round
(none — first round)

### Still outstanding
- [1.1] missing `\usepackage{amsmath}` in `preamble.txt` — blocking
- [1.2] provenance overstatement in `submission.md` results table — minor

---

## Round 2
Verdict: PASS

### Resolved since last round

- **[1.1] RESOLVED (was blocking).** `OUTPUT/p2/preamble.txt` now declares
  `\usepackage{amsmath}` alongside `booktabs` and `float`. Verified the way that
  matters: I generated the wrapper preamble by `cat`-ing the *shipped* `preamble.txt`
  (never hand-writing it), and the fragment compiles **exit 0, zero `!` lines, 1 page**.
  The only warning is the benign "Label(s) may have changed. Rerun to get
  cross-references right."

  I did not take the worker's word that the package set is now minimal-and-sufficient.
  I ran my own three-way negative control, dropping each declared package in turn:

      without amsmath   -> exit 1 | ! Undefined control sequence.  (l.4  $64\text)
      without booktabs  -> exit 1 | ! Undefined control sequence.  (l.17 \toprule)
      without float     -> exit 1 | ! LaTeX Error: Unknown float option `H'.

  All three fail, so every declared package is genuinely required and none is
  superfluous. Confirmed none of these failures was a spurious file-not-found: no
  `neg_*.log` contains "not found", and the `answer.tex` in my test dir is `diff`-clean
  against the shipped one.

- **[1.2] RESOLVED (was minor).** The worker made the claim true rather than softening
  it. `check.py` now computes the 128 KB case and asserts `size_c * 2 == size`, and
  additionally asserts the cross-check I had raised in round 1
  (`2**VA_BITS // PAGE == ptes`). I re-ran `check.py` from my own directory (exit 0) and
  `diff`-ed its stdout against the verbatim block quoted at `submission.md` lines 99-106:
  **byte-identical**. The results table's provenance column is now accurate row by row.

### Verified unchanged / still correct

- `answer.tex` is **byte-identical** to the round-1 file (`diff` clean against my
  archived copy), so the mathematics I verified independently in round 1 still stands:
  offset 16, VPN 14, 2^14 = 16384 PTEs, 2^16 B = 64 KB table, and the Question C
  128 KB -> 13-bit VPN -> 32 KB halving. No regression was introduced while fixing the
  preamble.
- Rendered the compiled PDF to PNG and read it. Table typesets 16 / 14 / 30 under the
  original's three headers, caption is LaTeX-numbered ("Table 1: virtual address
  components") rather than hard-coding "Table 2", A/B/C are clearly labelled, and the
  2 pros + 2 cons are all present and legible.
- `OUTPUT/` still holds exactly `answer.tex` + `preamble.txt`; `lint_output.py` exits 0.
- R5 clean: no `\documentclass`/`\usepackage`/`document` env in the fragment; sole label
  `p2:tab:vaddr` is namespaced; no figures, no absolute paths.
- `downloads.md` still correctly records "(nothing installed)" — nothing was installed
  this round either.

### Defects

- **[2.1] `build/neg.tex` is described in `submission.md` but does not exist.** |
  `problems/p2/submission.md` lines 64-65 ("I also added a negative control
  (`build/neg.tex`)") and line 88 (listed under "Intermediate steps and code") |
  severity: **minor (cosmetic — noted, not blocking)**

  `ls build/` returns only `answer.tex log.txt master.aux master.log master.pdf
  master.tex`, and `find` across the whole playground turns up no `neg.*` at all.

  I am flagging this rather than ignoring it because it is the same *class* of issue as
  [1.2]: describing an artifact in terms that overstate what is actually on disk. But it
  is not blocking, because the substantive claim the negative control was meant to
  support — that `amsmath` is genuinely required and that its absence produces exactly
  the round-1 fatal error — is true, and I verified it independently twice (round 1
  wrapper, and this round's `neg_amsmath.tex`, which reproduces the identical
  `l.4 $64\text` error). Nothing in the deliverable depends on this file.

  Also trivially stale, not worth a separate item: `downloads.md` still says "`booktabs`
  and `float` were already present" without mentioning `amsmath`. Nothing was installed,
  which is all R3 actually requires, so this is accurate where it counts.

### Still outstanding

- [2.1] missing `build/neg.tex` — minor, playground-only documentation, does not affect
  `OUTPUT`. Not worth another round.
