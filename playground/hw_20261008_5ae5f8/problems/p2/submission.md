# p2 — Ex. 3.2 (10 pts) — submission (round 2)

## Response to validator round 1 (VERDICT: FAIL)

Two minor defects were raised. **I checked both myself and accepted both.** Neither
changed a number or the conclusion. Nothing is disputed this round.

### [1.1] "fastest cell" mislabelled the high-density cell — FIXED in the deliverable

The answer read "Take the fastest cell actually manufacturable, a high-density 6T SRAM
bit at $0.021\,\mu\mathrm{m}^2$". The HD cell is the *densest*, not the *fastest*.
I confirmed this from the very source I had already cited in round 1, which states that
N5 offers "a high-performance cell at 0.025 µm² and a high-density cell at 0.021 µm²".
The sentence was false, and it sat at the hinge of a question whose premise is
literally "the fastest materials available".

I took the recommended **relabel** rather than switching to 0.025 µm², for a
substantive reason rather than to avoid a re-run: the argument needs a **lower bound**
on physical size. The densest cell gives the smallest array and therefore the smallest
crossing time, so quoting it concedes the maximum possible ground to the question's
premise. Switching to the HP cell would have made the numbers *larger* and the answer
rhetorically stronger (2.0e5 mm², 447 mm, 2.98 ns, ~12 cycles — computed, not
asserted), which is precisely why it would have been the weaker choice.

The replacement makes the lower-bound logic explicit instead of leaving it implicit:

> Take the densest cell in production, a 6T SRAM bit at $0.021\,\mu\mathrm{m}^2$; the
> faster high-performance variant is larger at $0.025\,\mu\mathrm{m}^2$, so this keeps
> the bound conservative.

All seven previously verified numbers are preserved untouched.

The same conflation was also present in `calc_size_latency.py` — in the
`SRAM_BITCELL_UM2` comment block and in two printed strings. Corrected there as well,
so the error does not survive anywhere. Verified label-only: every numeric token in the
script's output is identical before and after.

### [1.2] Cross-check described as independent when it is circular — FIXED in playground docs

The validator is right, and I verified the circularity arithmetically rather than
taking its word. Inverting both routes to an effective per-bit area:

    bottom-up : 0.021 / 0.70       = 0.0300 um^2/bit
    top-down  : 1e6 / (32 * 2^20)  = 0.0298 um^2/bit     ratio 1.0066

Same cell, same ~30% overhead — the published ~32 Mib/mm² density is itself derived
from the 0.021 µm² cell by assuming that overhead, which is my own 70% efficiency
constant. The 0.7% residual is 1 MiB vs 1e6 rounding. It was never corroboration, and
my round-1 claim that the routes "share only the process node" was wrong.

`crosscheck_area.py` is rewritten to say so in its own docstring and to **print the
inversion above**, so the circularity is visible in the output rather than buried. What
the check legitimately establishes is narrower and is now stated as exactly that: my
70% constant matches the industry convention.

**No delivered number is affected.** `answer.tex` quotes the cells-only 1.68e5 mm²,
which is just (bits × cell area) and carries no efficiency assumption at all. That
choice was already right; what was wrong was the claim I made *about* the check.

### Length consequence

The [1.1] fix added ~13 words and pushed the answer to 382 by my tokeniser, over the
380 ceiling. I cut "and no choice of material moves that floor" from the end of that
paragraph: the new HP-variant sentence now carries that point concretely, so the clause
had become an abstract restatement of what preceded it (the R8 "summarising your own
answer" pattern). Now **374** by my method, ~369 by the validator's (which runs ~5
lower).

## What the problem asked

> Ex. 3.2 | (10 pts) Memory hierarchy is given by the speed of memory devices and the
> size of the devices along the hierarchy. What if we build a giant memory device made
> of the fastest materials available that is as big as some terabytes? Would that
> eliminate the need for having intermediate memory devices as in memory hierarchy?
> Why or why not?

A yes/no question where the marks sit in the justification, not the verdict.

**Brief vs. source: no disagreement.** The brief's "transcribed verbatim" block matches
line 5 of `input/os_hw_3_problems.md` word for word.

**On R7.** The source is a text file, not a PDF, so two of the three channels do not
exist rather than having been skipped: the manifest records it as `kind: text_document`
with no `pages` key, and the pages dir holds only `alltext.txt`. In place of a
cross-channel reconciliation I ran a byte-level diff of the ingested text against the
original (`diff ... # no output`). This question refers to no figure; nothing in the
answer rests on one.

## What I decided it needed

**plain**, with supporting magnitudes computed rather than asserted. No diagram: the
question says "why or why not", not show/draw/plot, and the brief sets `needs: plain`.
Not a `code` problem either, but "do not state a number you did not compute" applies
regardless, so the magnitudes went through a script. The code is support, not the
deliverable.

## What I did

Argued **no**: the question's premise fails, because access time is set by material
*and* size, and at terabyte scale size dominates. Three arguments, each sufficient
alone (R8: three, not six).

1. **Capacity itself costs latency.** A read must physically cross the array; the
   crossing time is bounded below by the array's linear dimension, which grows as
   sqrt(C). Quantified.
2. **Already visible with the material held constant.** L1/L2/L3 are all SRAM on the
   same die at the same node and still answer in roughly 4/14/40 cycles. Only capacity
   differs. This is the load-bearing point: the hierarchy is not an artifact of mixing
   cheap-slow with expensive-fast materials. I attribute that spread to RC delay,
   decoder depth and sense-amp resolution, **not** to the speed of light, which is
   negligible at those sizes (0.001 ns at 32 KB, §2 of the script).
3. **Power and heat.** The fastest cells are the leakiest; a terabyte cannot be powered
   or cooled as one block, and spreading it out re-pays (1).

Conclusion: front the giant device with a small fast array — build the hierarchy
*inside* it. Cost stops being the motive; the size/speed trade-off supplies one. Cost
gets one clause, per the brief's warning that a cost-only answer is a 5-point answer.

**Deliberately omitted** (R8, in `notes.md`): non-volatility (off-target, the question
says *intermediate* devices), decoder fan-out and banking (a restatement of 1, folded
in), locality as a fifth argument (one clause in the conclusion), wafer cost and yield.

## Intermediate steps and code

Paths relative to PLAYGROUND.

- `notes.md` — plan written before drafting, plus round-1 continuation and round-2
  defect-response sections.
- `calc_size_latency.py` — the only script producing numbers used in the answer. Pure
  stdlib arithmetic; nothing simulated or fitted. Run: `python3 calc_size_latency.py`.
- `crosscheck_area.py` — consistency check on the area, **rewritten this round** to
  state its own circularity. Run: `python3 crosscheck_area.py`.
- `build/` — compile test (`pdflatex test.tex`), `page-1.png` at 110 dpi which I looked
  at, and the previous revisions kept for diffing: `answer_r1.tex`,
  `calc_size_latency_r1.py`, `crosscheck_area_r1.py`, plus the before/after script
  output captures `calc_b2.txt` / `calc_a2.txt`.

## Results

Every computed value in `answer.tex`, with its source. **All unchanged from round 1**
(the [1.1] fix was a relabel, not a recomputation):

| claim in answer.tex | value | from |
|---|---|---|
| densest 6T SRAM bit cell | 0.021 um^2 | published TSMC N5 HD cell, verified by web search |
| faster HP variant, for contrast | 0.025 um^2 | same source; **new this round**, added by the [1.1] fix |
| cells in 1 TB | 8e12 | `calc_size_latency.py` §1 |
| area of those cells | 1.68e5 mm^2 | `calc_size_latency.py` §1 |
| "about 2.4 whole 300 mm wafers" | 2.3767 | `calc_size_latency.py` §1 |
| "some 0.41 m on a side" | 409.878 mm | `calc_size_latency.py` §1 |
| "at least 2.7 ns in vacuum" | 2.7344 ns | `calc_size_latency.py` §1 |
| "eleven clock cycles at 4 GHz" | 10.9376 | `calc_size_latency.py` §1 |
| L1/L2/L3 ~ 4/14/40 cycles | — | published figures for recent x86; stated as "roughly", not computed |

**Independent re-derivation**, re-run again this round in SI units sharing no code with
`calc_size_latency.py`: area 168000 mm², side 409.878 mm, 2.3767 wafers, 2.7344 ns,
10.9376 cycles @ 4 GHz. Exact match to all quoted values.

**Area cross-check** (`crosscheck_area.py`) — stated correctly this round: bottom-up
240,000 mm² vs top-down 238,419 mm², agreeing to 0.7%, but the two are **the same
assumption written twice** (0.0300 vs 0.0298 µm²/bit) and so are **not** mutual
corroboration. The figure quoted in the answer, 168,000 mm², is the bit-cells-only
number, assumption-free and smaller than both, which is what the lower-bound argument
needs.

**Length (R8).** 374 words by my method, against a 300–380 target. 0 em-dashes.

**Compile.** `pdflatex` rc=0, one page, **0** Overfull/Underfull boxes, no warnings, no
undefined references. Rendered `build/page-1.png` and read it: sets cleanly, every
number on the page matches script output, and the new HD/HP sentence reads correctly in
place.

## Deliverables

- `OUTPUT/answer.tex` — the fragment, starting at `\subsection*{Ex.~3.2 (10 pts)}`.
  No `\documentclass`, `\usepackage`, `\begin{document}`, `\end{document}`, `\input` or
  `\include` (checked programmatically).
- No `preamble.txt` — needs only `\sqrt`, `\times`, `\mathrm`, `\emph`.
- No figures, by design.
- `OUTPUT` contains `answer.tex` and nothing else; `lint_output.py` exits 0.

No labels, figures or macros are defined, so nothing can collide in the `p2:` namespace.

## Where I am least confident

1. **The L1/L2/L3 cycle counts (4/14/40) remain quoted, not measured.** The validator
   independently confirmed them as mid-range (Skylake 4/12/41), which strengthens this
   from round 1, but they are still a citation. The argument degrades gracefully: it
   needs only that the three differ by roughly an order of magnitude end to end. A
   residual nitpick a hostile reader could still raise: L3 latency includes ring/mesh
   transit, not purely array access, and some designs use a different SRAM flavour for
   L3 than L1 — so "on the same die at the same process node" is doing real work in
   that sentence. Neither breaks the point, since both remain consequences of size
   rather than material.
2. **"Fastest material available" is still interpreted as SRAM.** The [1.1] fix
   sharpened the HD-vs-HP distinction *within* SRAM, but the choice of SRAM as the
   stand-in for "fastest material" is unchanged and is still an interpretation. I think
   it survives: arguments (1) and (3) concern distance and power density and do not
   depend on the cell at all, and a smaller cell only shrinks the array without
   removing the sqrt(C) scaling.
3. **The speed-of-light figure is a floor, not a prediction.** The validator raised and
   withdrew this one, agreeing the framing ("at least ... *in vacuum*", "real on-chip
   wires are several times slower than $c$") is correct. I still flag it as the place a
   careless reader could misread the answer.
4. **The 300 mm wafer comparison is rhetorical.** The arithmetic is right, but nobody
   builds a 168,000 mm² monolithic die — which is the point, that it is not buildable
   as one block. It illustrates scale; it is not an engineering claim.
