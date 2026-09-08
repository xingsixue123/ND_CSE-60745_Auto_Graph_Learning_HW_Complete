# p2 — notes

## Channel reconciliation (R7)

Problem is on rendered page 3 of `ingest/pages/Homework_2/`.

1. **Text** (`page_003.txt`) — flattens both tables to one cell per line, but all
   values are present and match the brief. Superscripts are lost: the worked example
   prints as "210 entries", which is `2^10`.
2. **Page render** (`page_003.png`) — read; both tables are ruled vector tables and
   fully legible at the downscaled size. Confirms Table 1 (30 bits / 2 GB / 64 KB /
   4 Bytes) and Table 2 (three headers, only `Total / bits` = 30 pre-filled). The
   render also resolves the superscript the text dropped: the example is "2^10 entries
   and 1 KB physical memory".
3. **Figure files** — none exist. `manifest.json` reports `n_images = 0` for all 9
   pages, so this channel is vacuously empty; there is no figure to misread. The
   tables are vector, not raster, which is why the render carries them cleanly.

No disagreement between the brief and the page. The brief's transcription is accurate,
including the "Virtual page memory (VPN)" header typo, which I reproduce as printed.

Unit convention from rendered page 1, item 4: 1 KB = 2^10 Bytes etc. So 64 KB = 2^16 B
and 2 GB = 2^31 B exactly. Binary, not decimal-SI.

Front matter item 1: "Please clearly indicate which question an answer is for" — hence
one subsection per question.

## What it needs

**plain.** No diagram is asked for (no "plot"/"draw"/"show"). The arithmetic is exact
powers of two, done by hand and cross-checked with `check.py`; per the brief, no code
goes in `answer.tex`.

## Arithmetic (verified by check.py)

- Page size 64 KB = 2^16 B  =>  page offset = **16 bits**
- VPN = 30 - 16 = **14 bits**   (invariant: 16 + 14 = 30 = stated total ✓)
- Single-level PT is indexed by the VPN, so #PTEs = 2^14 = **16384 entries**
  (the 2 GB *physical* size does not index the table — it is a distractor)
- PT size = 2^14 x 4 B = 2^16 B = **64 KB**
- Sanity: PPN = 31 - 16 = 15 bits, fits in a 4-byte PTE with room for flags ✓
- Coincidence worth not tripping over: the page table happens to be exactly one
  page (64 KB). That is a coincidence of these numbers, not a general rule.

## Plan

Section for Problem 2; subsections A, B, C. Table 2 as a real booktabs table with
LaTeX-numbered caption. C: 2 pros + 2 cons, each naming a mechanism, one grounded in
the 64 KB result from B, pros and cons genuinely opposed.
