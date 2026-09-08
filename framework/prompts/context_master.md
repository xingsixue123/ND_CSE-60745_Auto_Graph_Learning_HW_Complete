# Shared context — master level

You and your counterpart (the master agent and the master validator) are given this
same section. Neither of you knows anything about the homework that the other does
not. Where you differ is your job, described in the section after this one.

## What this system does

A homework assignment lands in `input/`. It has to come back out of `output/` as a
compiled PDF of answers. Between those two points:

1. The **master agent** reads the assignment and cuts it into independent problems.
   Problems that depend on each other (a part (b) that uses the graph built in part
   (a), a proof that reuses a lemma from earlier in the same question) are **not**
   split — they go to one worker as a single unit. Splitting related subproblems is
   the main way this pipeline produces incoherent answers.
2. For each problem the master writes a self-contained problem statement into that
   problem's playground, including a pointer to where it lives in the assignment
   (rendered PDF page index and the surrounding text), and spawns a **worker agent**.
3. Each worker is audited by its own **worker validator** in a loop until the
   validator passes it or the round cap is hit. Workers are spawned **one at a time**;
   a new problem is not started until the previous one is finished.
4. The master assembles the workers' LaTeX fragments into one document, compiles it,
   and submits it to the **master validator**.
5. The master validator either passes it — and the job is done — or returns a defect
   list, and the master goes round again.

## Directory layout

    input/                       the assignment and its data. READ-ONLY, always.
    specs.md                     user-written notes about this assignment.
    playground/<job>/            scratch space for this run.
      ingest/                    normalized assignment: per-page PNGs + text
      problems/<pid>/            one worker's scratch space
      validator/                 the master validator's scratch space
      logs/                      run logs
    output/<job>/
      <pid>/                     one worker's deliverable
      final/                     the assembled answer document

## Reading the assignment

The assignment has already been normalized for you by `framework/ingest.py`. In
`playground/<job>/ingest/` you will find, for each document:

    pages/<docname>/page_001.png          rendered page image (200 dpi)
    pages/<docname>/page_001.txt          text extracted from that page
    pages/<docname>/page_001_fig_01.png   an embedded figure, native resolution
    pages/<docname>/alltext.txt           all text, page-delimited
    pages/<docname>/manifest.json         page count and per-page figure list

You must read **all three** channels and reconcile them (rule R7). This is not
ceremony. In a Word-derived assignment the figures are embedded images, so a question
saying "create the following graph" is *unanswerable* from the text — the graph is
only in the image. And the whole-page render is downscaled when you read it, so the
node labels in that graph are unreadable there too: the figure files are the only
channel that actually carries figure content. `manifest.json` tells you which pages
have figures.

When you write a problem brief, say explicitly which figure file the worker needs.
A worker that has to discover for itself that its question depends on an image will
sometimes answer from the text and be confidently wrong.

The **rendered page index** (1-based, from the PNG filenames) is the only page
coordinate you may use. It frequently disagrees with the page number printed in the
document's own footer, because cover pages offset the numbering. Cite the rendered
index.

## The problem manifest

The master writes `playground/<job>/problems.json` and keeps it current. It is the
contract between the two of you — the validator checks coverage against it rather
than re-deriving the problem list by eye:

    {
      "problems": [
        {
          "id": "p1",
          "title": "Q1 Graph Creation",
          "points": 15,
          "rendered_pages": [2],
          "anchor_text": "Q1: Graph Creation (15 pts)",
          "input_files": ["graph-1.txt"],
          "subparts": ["visualize the graph"],
          "needs": ["code", "diagram"],
          "grouped_with_reason": "..."   // only when several questions were merged
        }
      ],
      "uncovered": []    // anything in the assignment deliberately not assigned, with why
    }

`needs` is one or more of `plain`, `code`, `diagram`. A question asking for a
computed number needs `code`; a question asking to "show"/"visualize"/"plot" needs
`diagram`; a derivation or explanation is `plain`.

## What "done" means

The job is done when the master validator says it is done, and at no other time.
A compiled PDF is not evidence of correctness, and neither is the master's opinion.
