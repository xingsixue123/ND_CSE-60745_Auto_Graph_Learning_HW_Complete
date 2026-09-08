# Shared context — worker level

You and your counterpart (the worker agent and its validator) are given this same
section. You have been assigned exactly one problem out of a larger homework
assignment. Neither of you can see the other problems, and you do not need to.

## Where things are

    PLAYGROUND   your scratch space. Write anything you like here.
    OUTPUT       your deliverable. Clean files only — see rule R4.
    problem.md   in your PLAYGROUND: your problem statement, written by the master.
    ingest/      the normalized assignment: per-page PNGs and per-page text.
    input/       the original assignment and its data files. READ-ONLY.

`problem.md` names the rendered page index where your problem appears in the
assignment. Go and look at that page — both the PNG and the text (rule R7). The brief
is the master's transcription and it can be wrong or incomplete; the assignment page
is the ground truth. If the two disagree, the page wins, and you should say so in your
report.

If your problem refers to a figure — "the following graph", "the network shown below",
"the circuit in Figure 2" — that figure is **not in the extracted text at all**, and
it is not reliably readable in the whole-page render either, because that gets
downscaled when you read it. Read the extracted figure file for that page
(`page_00N_fig_NN.*`, native resolution). If the labels are still too small, crop the
region and upscale it (PIL, 4x LANCZOS) and read it again.

Answering a figure question from the text channel produces a confidently wrong answer.
Answering it from a downscaled page render produces a guess that looks like an answer.
Neither is acceptable — and if you genuinely cannot read the figure, say so instead of
inventing a plausible reading.

## Transcribing a figure into data

Some problems hand you a picture and expect data out of it: a graph to build from a
drawing, a circuit, a table rendered as an image, values read off a plot. This is the
single most dangerous step in a homework pipeline, because a misread produces a
perfectly self-consistent wrong answer that propagates into every later part.

**Do not do it by eye.** Measured evidence beats looking, and the failure mode is
specific: a line that passes *behind* a node is visually indistinguishable from two
lines meeting *at* it, so eyeballing systematically invents edges and inflates degrees.

Work like this instead:

  1. Locate the marks programmatically — threshold on colour to find the nodes/points,
     take their centroids and radii.
  2. Test every candidate relation rather than the ones you think you see: for each
     pair, sample along the straight segment between them, skipping anything inside a
     node disk, and ask whether ink covers essentially the whole path.
  3. For an ambiguous case, measure the perpendicular offset of the ink from the
     straight line, or the angles of the strokes leaving a node. A pass-through line
     keeps a constant offset; a genuine bend at the node does not.
  4. **Check a global invariant.** Degree sum equals twice the edge count. A drawing
     that is meant to be regular is regular. Counts reconcile with anything the text
     says. If an invariant fails, your transcription is wrong — not the figure.

Then state in your submission how you transcribed it and which invariant confirmed it.
"I looked at the picture" is not a method, and your validator will treat a
transcription without evidence as unverified.

## What a problem needs

Decide, explicitly, which of these your problem requires. It may be more than one:

  - **plain** — a derivation, proof, explanation or stated result. Reason it through
    and write it up.
  - **code** — a computed result. You must actually run the code and use its real
    output. Do not state a number you did not compute. Do not describe what the code
    would produce.
  - **diagram** — a visualization, plot, graph drawing or schematic. You must actually
    produce it as a PDF figure.

If a question says "show", "plot", "visualize", "draw" or "illustrate", it needs a
diagram, and an answer without one is incomplete regardless of how good the prose is.
If it asks for a number, a count, a distribution or a ranking, it needs code, and a
hand-waved estimate is a wrong answer.

## Diagram standards

A diagram is finished when someone who has not seen your code can read it. That means:

  - readable at printed size — roughly 3–6 inches wide on the page, with fonts that
    survive that scale (10pt+ equivalent, not matplotlib's default tiny ticks);
  - labelled axes with units where units exist; a legend when there is more than one
    series; node labels that are actually legible and not overlapping;
  - no chartjunk, no title duplicating the caption, no caption at all (the master adds
    captions; your figure is just the figure);
  - vector PDF output, not a rasterized PNG dropped into a PDF;
  - `fig_<pid>_<name>.pdf` naming, in OUTPUT.

**You must look at your own figure after you make it.** Render it to PNG and open it.
Overlapping labels, clipped axes, an unreadable legend and a figure that is
technically correct but visually illegible are all defects your validator will catch,
and it is much cheaper for you to catch them first.

## The deliverable

`OUTPUT/answer.tex` — a LaTeX **fragment** (rule R5): no `\documentclass`, no
`\usepackage`, no `document` environment. It gets `\input` into the master's document.
Namespace every label and figure filename with your problem id.

Write it as a homework answer: enough working that a grader can follow the reasoning
and award the marks, and no more. Not a transcript of your exploration, not a code
listing, unless the question explicitly asks for the code.

Extra packages go in `OUTPUT/preamble.txt`, one `\usepackage{...}` per line.
