# Problem id: `p2`

**Course:** CSE 60321 -- Advanced Computer Architecture -- Spring 2026
**Assignment:** Homework 2
**This problem:** Problem 2, 10 points (Questions A, B, C)
**Location in the assignment:** rendered page **3** of
`playground/hw_20260907_f8533b/ingest/pages/Homework_2/` (`page_003.png`, `page_003.txt`).
The whole problem fits on that one page.
**Anchor text:** `Problem 2: (10 points)` / "Consider the following parameters of a
virtual memory system:"

**Figures:** none. The ingest manifest reports `n_images = 0` for every page of this
assignment. The two tables on this page are ruled vector tables, not images; both are
transcribed in full below, and both have been verified against `page_003.png`. (Table
text extraction flattens a table into one column per line, so trust the transcription
below and the page render over the raw `.txt`.)

**Namespacing (mandatory):** every LaTeX label, every figure filename and every macro
you define must carry the `p2` prefix — `\label{p2:tab:vaddr}`, `fig_p2_*.pdf`.
Unnamespaced labels collide with the other problems and break the master document's compile.

---

## Assignment-wide unit convention (stated on rendered page 1, applies here)

> Unit clarification: for all problems in this homework,
> 1TB = 2^10 GB, 1GB = 2^10 MB, 1MB = 2^10 KB, 1KB = 2^10 Bytes, 1 Byte = 8 bits.

This matters here: 2 GB = 2^31 Bytes and 64 KB = 2^16 Bytes exactly. No decimal-SI
interpretation.

---

## Shared setup (transcribed verbatim — applies to all three questions)

> Consider the following parameters of a virtual memory system:
>
> **Table 1: basic specifications of the system**
>
> | Virtual address | Physical memory size | Page size | PTE size |
> |---|---|---|---|
> | 30 bits | 2 GB | 64 KB | 4 Bytes |

---

## Question A (2 points) — transcribed verbatim

> **Fill in the table:**
>
> **Table 2: virtual address components**
>
> | Page offset / bits | Virtual page memory (VPN) / bits | Total / bits |
> |---|---|---|
> |  |  | 30 |

Only the `Total / bits` cell is pre-filled, with the value **30**. The other two cells
are blank and are what you must supply.

(The column header really does read "Virtual page memory (VPN)" in the original — that is
the assignment's own typo for *virtual page number*. Reproduce the header as printed;
do not silently correct it, and do not draw attention to it either.)

**Deliverable:** reproduce Table 2 in LaTeX with all three cells filled in, and add a
line or two showing where the page-offset width comes from. This is a 2-point fill-in,
so keep it tight — the table plus a sentence.

## Question B (4 points) — transcribed verbatim

> **How many page table entries (PTEs) are needed and how much physical memory is
> needed for storing the page table?** Direct answers are expected (e.g., 2^10 entries
> and 1 KB physical memory).

**Deliverable:** two direct answers, in the style the worked example sets — a power of
two for the entry count, and a size with a binary unit for the memory. The phrase
"Direct answers are expected" means do not write an essay; one short line of arithmetic
for each is appropriate and sufficient at 4 points.

Two things to be careful about. First, the number of PTEs in a single-level page table
is set by the size of the **virtual** address space, not the physical one — the 2 GB
physical memory size is not what indexes the table. Second, express the page table size
using the assignment's binary units (1 KB = 2^10 Bytes), matching the format of the
example given in the question.

## Question C (4 points) — transcribed verbatim

> **What are the pros and cons of increasing the page size?** Please provide at least 1
> pro and 1 con.

**Deliverable:** at least one pro and at least one con, clearly separated (a short
labelled list is the natural format). Two of each is a comfortable answer for 4 points;
do not write six.

Each item should be one or two sentences that actually name the mechanism, not just the
outcome — "fewer PTEs, so a smaller page table" is worth marks, "it is more efficient"
is not. You have just computed a page table size in Question B off a 64 KB page, so at
least one of your points can be grounded in that result; a good answer connects back to
it. Keep the pros and cons genuinely opposed (e.g. page table size / TLB reach on one
side, internal fragmentation and page-fault transfer cost on the other) rather than
listing two versions of the same effect.

---

## What to produce

- `OUTPUT/p2/answer.tex` — a LaTeX **fragment**: no `\documentclass`, no
  `\begin{document}`, no `\usepackage`. It starts at the section level. Extra packages
  go one per line in `OUTPUT/p2/preamble.txt` as literal `\usepackage{...}` lines.
  If you use `booktabs` for the tables, declare it there.
- Structure it as a section for Problem 2 with a clearly labelled subsection per
  question (A, B, C) — the assignment's front matter requires it: *"Please clearly
  indicate which question an answer is for in your submission."*
- Reproduce **Table 2** as a real LaTeX table (the question is literally "fill in the
  table"), with the same three column headers as the original and its caption
  "Table 2: virtual address components". Let LaTeX number the table itself rather than
  hard-coding the string "Table 2" into the caption body.
- **`needs`: plain.** The arithmetic here is exact powers of two and short enough to do
  by hand — but check it anyway before writing it down. **No code in `answer.tex`.**
  This is a homework submission: give the answers and the short justification a grader
  needs, and stop.
- No diagram is required for this problem.
