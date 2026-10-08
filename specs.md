inputdir: `input/`

outputdir: `output/`

<!--
Paths are relative to the repository root; the master is also given them as
absolute paths in its runtime facts, so this file does not have to repeat them.

Anything else worth telling the master goes here: a submission format the course
requires, a preferred library, a question to skip, a deadline. It can stay this
short -- see the examples/ directory for real ones.
-->

We are working on **HW3 Part (A): GNNs Hands-on Practice**, 30 points, five
questions worth 6 points each.

**The authoritative question list is the Word file**,
`input/CSE 60745_Fall 2026_HW3-Part(A).docx`. All three of its pages are this
assignment: page 1 is the cover, pages 2-3 are Q1 through Q5. It states
requirements the notebook does not, for example that Q2 should use
`torch_geometric.utils.softmax`, that Q4 wants the basic version of R-GCN, and
that in Q5 an 8-hop receptive field is not the same thing as an 8-layer GNN.

**The scaffolding to complete is the notebook**, `input/Practice3_pyg_basics.ipynb`.
Five cells are marked TODO and are the whole of the work: `MyGCNConv`,
`MyGATConv`, `MyGINConv`, `MyRGCNConv` and `MyDeepConv`. `MySAGEConv` earlier in
the notebook is a completed example of exactly the same pattern, so read it before
writing any of the five. The notebook also says to run the GraphSAGE demo end to
end first, "so that a failure later is yours and not the framework's" -- do that.

The assignment says to use Google Colab. Ignore that and run locally. Build a venv
and install `torch_geometric`, `gensim`, `pandas`, `scikit-learn` and `scipy`;
`torch` is already present. PyG 2.3 and later is a pure-Python wheel, so
`torch-scatter` and `torch-sparse` are not needed, as the notebook's own setup cell
notes.

Q5 asks you to look into the literature on over-smoothing before implementing. Cite
what you actually use, and follow R9 below when you do.

---

## Rules for workers

**Master: copy this whole section verbatim into every `problem.md` you write.**
Workers and worker validators never see this file; the brief is the only channel
that reaches both of them.

These are not style preferences. They are defects. A worker that breaks one has
not finished, and a validator that passes one has not done its job.

### R8 — Answer the question asked, at the length it deserves

Write the shortest answer that earns full marks, then stop. Concrete targets,
measured from a previous assignment after a careful human edit:

| question | target |
|---|---|
| a 5-point short answer | about 190 words; up to 290 if it has several sub-parts |
| a 10-point paper summary and critique | about 550 words |

Left alone, an answer comes out **1.5 to 2 times** these lengths. That is the
failure mode to watch for in yourself. The excess is never new substance; it is
always one of these four:

- **exhaustive enumeration** — four examples where the question needs one, six
  hardware mechanisms where three carry the argument;
- **summarising your own answer** — a closing sentence that restates the opening
  one. If a paragraph begins "so the model is X" and ends "the model is therefore
  X", delete the ending;
- **explaining the significance of your own answer** — the question asked *where*
  the magic number is stored, not why that location is efficient;
- **stating what you are about to do** — "the three binding times are worth
  naming", "it is worth noting that".

Em-dashes are a symptom rather than a cause, but they mark the places to look:
one every 70 words means the sentences are being extended rather than ended.

**Validator: count the words.** Compare against the target above and against what
the problem is worth. Over target by more than a quarter, with no sub-part that
justifies it, is a defect to be reported and fixed, at severity major. Do not pass
an answer because it is correct if it is also twice as long as it needs to be.

### R9 — Read past the quotation

When you quote or cite a source, read the sentences that follow the quote before
you build an argument on it. Stop at the quote and you will write a criticism the
source already answers, or attribute to an author a claim they did not make.

Both of these happened in a previous assignment and both were findable with one
grep by the person marking it:

- A paper was criticised for raising a security problem and leaving it there. The
  next sentence of the paper proposed two countermeasures. (The real criticism was
  available and stronger: one countermeasure reintroduced the central authority the
  design existed to remove, and the other was justified only "on a system that
  assumes no malicious processes".)
- A paper's closing section was described as claiming a system succeeded because
  it had no predefined objectives. It says nothing of the sort; it says the authors
  were grateful never to have had to satisfy someone else's requirements. The
  critique was aimed at an invented claim.

So: quote the source, then say what the source does next with it. Never assert that
an author "leaves the problem there", "never asks", or "does not address" something
without having read to the end of that discussion.

**Validator: for every quotation and every characterisation of what a source says
or fails to say, open the source and read the surrounding passage yourself.** A
quotation that is verbatim can still be used to support a claim the source
contradicts two sentences later. Confirming the words exist is not the check;
confirming the argument survives the context is.
