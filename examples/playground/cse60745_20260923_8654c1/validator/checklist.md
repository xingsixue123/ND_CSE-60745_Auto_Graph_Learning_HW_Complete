# Master validator checklist — job cse60745_20260923_8654c1

## Round 1 — 2026-09-23

Verdict: PASS (with three minor defects noted)

### What the assignment actually asks (enumerated from the source, not from problems.json)

Slide deck `CSE60745-Hands-on_HW2-Part(B)-1.pdf`, read through all three channels
(text, page PNG, extracted figures). Rendered pages 1–6 are HW1 recap, excluded by
specs.md. Rendered page 7 is the section divider "HW2-Part(B): 30 pts / Practice I".
Page 8 states the deliverable; page 9 is the pipeline demo figure (no new requirement —
it suggests dot-product scoring and a softmax classifier, both of which the submission
uses); page 10 marks Practice II **Optional**; page 11 states Task 4 and points at the
notebook; page 12 is a thank-you slide. The figures on pages 8, 9 and 11 were opened
and carry no requirement absent from the text.

specs.md: the real problem definitions are in `graph_embedding-1.ipynb`. Read in full.
The assignment is therefore:

| # | requirement | source | answered? |
|---|---|---|---|
| a | TODO 1 `sample_walks` | nb §3 | yes, p1 Listing 1 |
| b | TODO 2 `train_embedding` | nb §3 | yes, p1 Listing 2 |
| c | TODO 3a `LinkPredictor.fit/.score` | nb §4 | yes, p1 Listing 3 |
| d | TODO 3b `CountryClassifier.fit/.predict` | nb §4 | yes, p1 Listing 4 |
| e | reproduce DeepWalk and node2vec | nb §3 header, slide p8 | yes (DeepWalk + 3 (p,q) settings) |
| f | test own sampling ideas | nb §3, slide p8 | yes (RWR, deg-corrected, triadic) |
| g | `comparison_table()` across strategies | nb §6 | yes, Table 1 (+Table 4) |
| h | "which downstream task does each help, is one embedding best for both" | nb §6 | yes, §1.4 |
| i | Task 4 metapath2vec, ≥2 schemas, same fixed downstream models, combined table | nb §§7–8 (**optional**) | yes, §2, Table 4 |

Points: Task 3 = the whole 30 pts, and it is fully answered. Nothing uncovered.

### What I verified, and how

**Independent bit-exact reproduction** (my own copy of the code in
`validator/repro/`, same venv, nothing reused from the workers' output artefacts):

- Task 3 `deepwalk` seed 0 → 0.6039 / 0.7226 / 0.6023 / 0.7214 / 0.7575 / 0.7647 /
  0.6817. Identical to `results_comparison.csv` to 4 dp on all 13 columns.
- Task 3 `triadic` seed 0 → 0.6037 / 0.7213 / 0.6044 / 0.7227 / 0.7628 / 0.7663 /
  0.6956. Identical on all 13 columns.
- Task 4 `metapath U-U-U-A-U` seed 0 → 0.6234 / 0.7437 / 0.6145 / 0.7358 / 0.7969 /
  0.7896 / 0.6383, and 148,000 walks. Identical to `results_hetero.csv` on all 13.
- `corpus_size.py` re-run: every walk/token count in §2.2 reproduces exactly
  (U-A-U 152,930 walks / 6,117,200 tokens = −0.1% vs DeepWalk ×22; U-U-U-A-U
  4,068,117 tokens, ×15 control +2.6%).
- `test_sampler.py` re-run: meta-path walks are type-correct (social-step fraction
  0.000 / 0.334 / 0.509 for UAU / UUAU / UUUAU), and the rare-artist claim
  "median visited-artist popularity 613 → 204.5" reproduces exactly.
- `typeblind_steps.py` re-run: type-blind walk on H takes a social step 0.72% of the
  time over 31,122 steps — exactly as claimed.
- `cold_start_stats.py` re-run: 647/666 cold users have ≥1 artist (97.1%), median 334
  artists; 209/216 cold test sources covered (96.8%); U-A-U one-step reach median
  7,307 of 7,623 vs social 2-hop median 61.

**Recomputed from the raw data by my own script** (`validator/check_data.py`):
7,624 users; 19,464 observed edges; 666 isolated; mean degree 5.1060; max 153; 734
components; 4,171 × 21 val/test queries; 18 countries, 763/763/6,098 split; largest
class 1,572, smallest 16 with exactly 2 in the training split; test majority rate
0.2063; test degree buckets 216/266/469/842/939/1439 and val 213/261/524/842/973/1358
(both sum to 4,171); N_ARTISTS 7,842; 3,014,361 user–artist edges; 7,451 users with
≥1 artist; artists per user median 400 (over all 7,624 users, exactly as the notebook's
table says) max 944; artist popularity median 205; H = 15,466 nodes / 3,033,825 edges.
Every one of these appears in the answer and every one is right.

**Recomputed the derived statistics** from the stored per-run artefacts, independently
of `make_tables.py`: all noise floors and spread/noise ratios in Table 1
(7.0 / 6.0 / 4.1 / 4.2 / 1.3 / 5.4 / 1.7 / 3.9 ×) are correct to the displayed
precision; Table 2's three breakdown rows, Table 3's 42 cells, Table 4's control rows
(×15: 0.6110/0.7267/0.6118/0.7269/0.7650/0.6678/0.7601/0.6764; ×22:
0.6170/0.7298/0.6179/0.7292/0.7623/0.6643/0.7624/0.6852) and Table 5's ×15 column all
match. The cold-bucket instability claim (21 runs, range 0.0139–0.1065; DeepWalk
0.0833/0.0231/0.0278) is exact. The random-Z control (test Hit@1 0.0671, MRR 0.2009,
country micro-F1 0.1340) is exact, and chance MRR = H_21/21 = 0.1736 is right.

**Load-bearing interpretive claim spot-checked**: "country is an extremely assortative
label". 87.5% of observed edges join same-country users against 11.9% expected at
random. Supported.

**The PDF itself** (read through both channels — 14 rendered pages plus extracted text,
and pages 1, 4, 5, 6, 11, 12, 13, 14 opened as images at 300 dpi). Recompiled from
`final/` myself: exit 0, 14 pages, **zero** overfull boxes, no multiply-defined labels,
no undefined references, 3 cosmetic underfull hboxes. All four figures render (vector,
no missing-file boxes) and are legible at printed size; I checked each against the table
it plots and they agree. The 9-column Tables 1 and 4 sit inside the margins. Equations
and listings typeset correctly.

**Assembly and compliance.** `final/p1.tex` and `final/p2.tex` are byte-identical to the
workers' `answer.tex`. No `\documentclass` / `\begin{document}` / `\usepackage` in
either fragment. Every label is namespaced (`p1:`/`p2:`), the two `\lstdefinestyle`
names are namespaced, figures are referenced by bare filename, `preamble.tex` is the
correct de-duplicated union (9 packages). `lint_output.py` passes on `output/p1` and
`output/p2`. It fails on `output/final`, but that is expected and not a defect: R4
governs worker deliverable dirs, and `final/` is by design the assembled document
(`main.tex`, `main.pdf`, the fragments and the merged preamble); no logs, aux files or
scratch artefacts are present there. `downloads.md` records the venv, gensim, the other
wheels and the dataset download.

### Defects

- [1.1] Rendered page 1, §1.1: "Seven rules are compared:" introduces a table with only
  **five** rows — node2vec's three (p,q) settings are collapsed into a single row, so
  the seven of Table 1 are configurations, not listed transition rules. A reader
  counting rows finds five. Resolution: "five transition rules, seven configurations",
  or give node2vec three rows. | severity: minor
- [1.2] Table 1 caption (page 4) describes its columns as "The scalar metrics of
  `comparison_table()`", and Table 4's caption (page 11) as "The notebook's
  `comparison_table()`". The `val ma-F1` column is not one of them:
  `run_experiment` records only `country_val_microF1`, `country_test_microF1` and
  `country_test_macroF1`. The column is correctly measured (I verified all seven values
  and its 0.0077 noise floor against `evaluate_country`'s own frames) and §1.4 makes a
  good argument out of it — only the stated provenance is loose. Resolution: one clause
  saying val macro-F1 is read off `evaluate_country`, not the summary row. | severity: minor
- [1.3] Redundancy across the assembled document: Table 4 (page 11) reprints all seven
  Task 3 rows already given in Table 1 (page 4) — 56 numbers appear twice. The notebook
  explicitly asks for Task 4 to be compared "in the same `comparison_table()`", so this
  is defensible and I am **not** asking for it to be removed; recorded so the redundancy
  is a decision on the record rather than an oversight. | severity: minor

### Where I looked and found nothing

- Coverage against the assignment enumerated from the source: no missing question, no
  missing sub-part, no missing metric (Hit@1, MRR, micro-F1, macro-F1, per-source-degree
  breakdown all present for both splits).
- Fabricated or drifted numbers: three full runs reproduced bit-exactly and every other
  cell traced to a stored per-run artefact. I did not find a single number in the
  document that disagrees with what the code produces.
- Method soundness: the notebook's scaffolding (sections 1, 2, 5) is byte-verbatim;
  `impl.py` and `scaffold.py` are sha256-identical between p1 and p2, so Task 4's claim
  to reuse Task 3's trainer and both downstream models unchanged is literally true; the
  downstream models are held fixed across every row as the notebook demands; the
  node2vec rejection sampler is correct; C-selection on validation is disclosed and the
  argument is rested on the held-out columns.
- Altitude: the four code listings are the TODO implementations the assignment asks for,
  trimmed to the author's own code; no debugging output, no duplicated figure, no
  five-page derivation of a one-line answer.

### Resolved since last round
(none — first round)

### Still outstanding
[1.1], [1.2], [1.3] — all minor. Passing with them noted, per the severity rule.

---

## Round 2 — 2026-09-23

Verdict: FAIL

### What changed since round 1

The master fixed two of the three minor defects and left the third by explicit,
well-reasoned decision (master.log `[SUBMIT 2 decision]`). Diffing the shipped PDF's
text against my round-1 copy shows **exactly three hunks changed and nothing else** —
no number anywhere in the document moved, and all four figure PDFs are byte-identical
(md5 unchanged across `final/`, `p1/`, `p2/` and my round-1 snapshot). So the whole of
round 1's correctness verification — three bit-exact pipeline reproductions, every
dataset statistic, all eight noise-floor and spread/noise ratios, every table cell
traced to a stored artefact — carries over unchanged and did not need re-running.

I re-verified the three edits are themselves correct:

- [1.1] now reads "Five transition rules are compared, giving the seven configurations
  of Table 1 (node2vec is run at three (p,q) settings)". Correct: the five rules are
  uniform/DeepWalk, node2vec, RWR, deg-corrected, triadic, and Table 1 has seven rows.
- [1.2] p1's prose and caption and p2's Table 4 caption all now state that the
  validation macro-F1 column is not recorded by `run_experiment`. Correct — I confirmed
  in round 1 that `run_experiment`'s summary row carries only `country_val_microF1`,
  `country_test_microF1` and `country_test_macroF1`.
- [1.3] left as is, with reasoning I accept and had already said I was not objecting to.

Recompiled `final/` myself: rc=0, still 14 pages, **zero** overfull boxes, no
multiply-defined labels, no undefined references. Rendered and looked at the three pages
that changed (1, 4, 11): all three set cleanly, nothing reflowed badly, Tables 1 and 4
still sit inside the margins and are numerically unchanged.

### Defects

- [2.1] **The round-2 fixes exist only in `final/`; the worker deliverables still carry
  the defective text.** `output/.../final/p1.tex` and `output/.../p1/answer.tex` now
  differ in 3 hunks, and `final/p2.tex` vs `p2/answer.tex` in 1 hunk — precisely the
  [1.1] and [1.2] wording. `p1/answer.tex:18` still reads "Seven rules are compared:"
  and `p1/answer.tex:227` / `p2/answer.tex:178` still carry the undisclosed
  `comparison_table()` captions. This is not a stylistic quibble:

  * `output/<pid>/answer.tex` is a deliverable in its own right under the OUTPUT layout,
    and the two copies of the same answer now contradict each other, with the
    defective one sitting in the directory that looks authoritative.
  * `final/` is by construction assembled *from* those fragments. Any re-assembly —
    which is what the master does at the start of every submission round — silently
    reverts both round-2 fixes. The regression is live, not hypothetical.
  * It is a deviation from the master's own practice, which is why I read it as an
    oversight rather than a decision: the two *earlier* post-PASS edits (p1's
    "$3$--$20\times$" bucket-ratio fix and the cold-tie coherence sentence) were
    propagated correctly and `p1/answer.tex` matches `final/p1.tex` on both.

  Resolution: copy `final/p1.tex` → `output/.../p1/answer.tex` and `final/p2.tex` →
  `output/.../p2/answer.tex` (or make the edits there and re-assemble), then confirm
  `diff` is empty for both pairs and that `final/main.pdf` recompiles to the same 14
  pages. No substantive work is needed — the wording fixes are already correct and I
  have verified them; only the propagation is missing. | severity: **major**

### Where I looked and found nothing new

- Numbers, tables, figures, coverage: unchanged from round 1 and still correct. The
  text diff of the shipped PDF is confined to the three intended wording hunks.
- `lint_output.py` still passes on `output/p1` and `output/p2`; figures still
  byte-identical and referenced by bare filename; all labels still namespaced; no
  `\documentclass`/`\usepackage`/`\begin{document}` in either fragment.
- The master's decision to resubmit rather than ship post-PASS edits unchecked was the
  right call and I want it on the record as such — the defect below is about where the
  edits landed, not about making them.

### Resolved since last round

- [1.1] **fixed in the assembled document, verified** — but see [2.1]: not fixed in
  `output/p1/answer.tex`.
- [1.2] **fixed in the assembled document, verified** — but see [2.1]: not fixed in
  `output/p1/answer.tex` or `output/p2/answer.tex`.
- [1.3] **withdrawn.** I recorded it in round 1 without asking for a change and the
  master's justification (the notebook itself asks for Task 4 to be compared against
  Task 3 "in the same `comparison_table()`", and stripping the rows would make p2's
  table unreadable standalone) is correct. Closed, not carried forward.

### Still outstanding

[2.1] major. [1.1] and [1.2] remain open in the worker deliverables until [2.1] is
resolved; they are closed in `final/`.

---

## Round 3 — 2026-09-23

Verdict: PASS

### What changed since round 2

Only the location of already-validated text. The master copied `final/p1.tex` and
`final/p2.tex` back over the worker deliverables and recompiled. All four `.tex` sources
in `final/` are **byte-identical to the round-2 versions I already validated**
(`p1.tex`, `p2.tex`, `main.tex`, `preamble.tex` all diff-clean against my round-2
snapshot), and the shipped `main.pdf`'s extracted text is **identical to round 2's**
with no differences at all. So no number, table, figure or sentence moved, and round 1's
correctness verification — the three bit-exact pipeline reproductions, every dataset
statistic, all eight noise-floor and spread/noise ratios, every table cell traced to a
stored artefact — carries over untouched. Nothing warranted re-running the experiments.

### [2.1] — resolved and verified

- `diff final/p1.tex output/p1/answer.tex` → empty. `diff final/p2.tex
  output/p2/answer.tex` → empty. The two copies of each answer now agree.
- **The merge went the right way.** I checked the direction rather than just the
  equality: the surviving text is the *fixed* wording ("Five transition rules are
  compared, giving the seven configurations…", and both disclosed `comparison_table()`
  captions), not a revert to the round-1 phrasing. [1.1] and [1.2] are now closed in the
  worker deliverables as well as in `final/`.
- **I proved the idempotence claim myself** rather than taking the master's log for it,
  since that is the property whose absence caused the defect: re-assembling from the
  worker deliverables into a scratch dir reproduces `final/` exactly — `p1.tex` and
  `p2.tex` come back identical, and I independently re-derived `preamble.tex` as the
  de-duplicated union of `p1/preamble.txt` and `p2/preamble.txt` (9 packages, exact
  match). A future re-assembly can no longer silently revert anything.
- All four figure PDFs are md5-identical between each `<pid>/` dir and `final/`
  (2 copies each, no third variant anywhere).

### Independent checks this round

- **Rebuilt the document myself** from the shipped sources: rc=0, 14 pages, zero
  overfull boxes, no multiply-defined labels, no undefined references — and the text of
  my rebuild is identical to the shipped `main.pdf`, so the shipped PDF really is the
  product of the shipped sources and not a stale artefact.
- Rendered and read page 1 of the shipped PDF: the corrected sentence sets cleanly above
  the five-row rule table, which is exactly what the fix was for.
- `lint_output.py` OK on `output/p1` and `output/p2`. Full inventory of the OUTPUT tree:
  17 files, every one of them an allowed deliverable — no `.aux`/`.log`/`.out`, no
  scratch images, no code, no intermediates anywhere.
- R5 re-checked on both fragments: no `\documentclass`, `\usepackage` or
  `\begin{document}`.

### Defects

None.

### Resolved since last round

- [2.1] **major — fixed and verified**, by equality, by direction of the merge, and by
  independently reproducing the assembly. The master also added the idempotence check to
  its own procedure, which addresses the root cause rather than just this instance.

### Still outstanding

Nothing. [1.1] and [1.2] closed everywhere; [1.3] withdrawn in round 2; [2.1] closed.

### Closing assessment

Over three rounds I reproduced three full experiment runs bit-exactly (Task 3 DeepWalk
and triadic at seed 0, Task 4 metapath U-U-U-A-U at seed 0, all 13 columns each),
recomputed every dataset statistic and every derived ratio from the raw data, re-ran the
corpus accounting, the sampler type-correctness gates, the rare-artist popularity
measurement, the type-blind step probe and the cold-start coverage, checked the one
load-bearing interpretive claim (country assortativity: 87.5% of edges same-country vs
11.9% at chance), and read the compiled document through both channels. Coverage is
complete against the assignment as I enumerated it from the source: all four notebook
TODOs, DeepWalk, node2vec at three settings, three original sampling strategies, the
comparison table, the per-source-degree breakdown, the "which task does each strategy
help" analysis, and the optional Task 4 with two-plus meta-path schemas and budget
controls. I did not find a number in the document that disagrees with what the code
produces. I have nothing substantive left to blame.
