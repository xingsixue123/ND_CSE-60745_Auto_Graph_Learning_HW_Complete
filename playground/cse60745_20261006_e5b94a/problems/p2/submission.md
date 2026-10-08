# p2 — Q4: R-GCN Implementation (6 pts)


## Round 1 — what the validator found, and what I changed

**[1.1] major — accepted, and it was my error.** `answer.tex` asserted that pooling helps
because "averaging *within* the two ≈400-degree listening relations smooths the users
flat". I did not take this on trust; I reproduced it (`run/ablation.py`, `run/ablation.log`):

- *Control first.* Variant A of my ablation is the per-relation normalisation, and its
  forward output is **bit-identical** to the delivered layer (max abs diff 0.000e+00), so
  A/B/C/D are a like-for-like comparison of the delivered code.
- *What pooling actually rescales*, measured as $|N_r(i)|/c_i$ over nodes with
  $|N_r(i)|>0$: `listens` **1.0000**, `listened_by` **0.9785**, `friend` **0.0451**
  (22.1× down-weighting). Pooling barely touches the listening relations — my stated
  mechanism had the wrong target, and as the validator noted it predicts the wrong sign,
  since under pooling the supposedly-flat listening terms dominate *more*.
- *Ablation*, 4 variants × 3 seeds through the frozen harness (val MRR):
  **A per-relation 0.1809** (control; tracks the delivered five-run mean 0.190),
  **B pooled everywhere 0.3053**, **C `friend` pooled only 0.3253**,
  **D listening pooled only 0.2465**. C alone exceeds B. The gain is the down-weighting
  of the sparse `friend` relation, exactly as the validator said. My ordering matches
  theirs (they got 0.1895 / 0.2957 / 0.3294 / 0.2388 — same conclusion, different
  `X_HETERO` draw).

The closing aside now states the mechanism the data supports, with the measured scale
factors and variant C's number in it. I also checked *why* down-weighting `friend` helps
rather than leaving it unexplained: `run/leak_check.py` shows **all 19,464 training
positives are exactly the relation-0 edges, and 0 of the 4,171 val and 4,171 test
positives are** — relation 0 hands the model its own training labels. That is in the
answer as a single clause, and it is measured, not surmised.

**[1.2] minor — fixed.** The loose "smooths *the users* flat" premise (relation 1
aggregates into artists, not users) is gone entirely with the rewrite; no claim about
which node type each listening relation smooths now appears.

**[1.3] minor — considered, deliberately unchanged.** The table reports run 1, which in
this batch is the maximum of five. The rule "run 1" was fixed before any value was seen
and the previous batch had run 1 as the *weakest*; switching to, say, the median *after*
seeing that run 1 came out high would be a post-hoc rule change, which I judge worse
practice than a fixed rule with disclosure. The 0.190 ± 0.020 spread is printed in the
sentence immediately below the table, which now also says "read the table with that
spread". Raised here so the decision is visible rather than silent.

**[1.4] minor — fixed.** The "crosscheck passes" claim is corrected below to say what
`crosscheck.py` actually reports for an in-flight problem.

**Also tightened (not a reported defect).** The validator was right that
`run/verify_fidelity.py` only tested line *membership in a set*, which would pass a
reordered cell or a deleted duplicate. It now does a **contiguous-block** comparison and
checks the two cut cells are exact prefixes (`run/verify_fidelity.log`).

## What the problem asked

Complete `MyRGCNConv()` (notebook cell 27) — "the basic version of R-GCN", with edge
type labels supplied in `edge_type` — and implement all four of `__init__`,
`reset_parameters`, `forward`, `message`, per the docx preamble (rendered page 2) and
cell 24.

**Channel reconciliation (R7).** All three channels agree; there is nothing to flag.

- `ingest/pages/CSE 60745_Fall 2026_HW3-Part(A)/page_003.txt` and `page_003.png`
  (rendered page 3; its footer reads "Page 2 of 4" because of the cover page) carry Q4
  verbatim and identically.
- `page_002_fig_01.png` (727×525, the only embedded figure in the document) is the
  `MyGCNConv` skeleton screenshot. I read it at native resolution; it matches notebook
  cell 16 comment-for-comment, confirming the four-method template my layer follows.
  It is on page 2, not my page, and nothing in my answer depends on reading a figure.
- Notebook cell 24 supplies the formula
  $h_i' = W_0 h_i + \sum_{r} \sum_{j \in N_r(i)} \frac{1}{c_{i,r}} W_r h_j$ and the
  three relations; cell 1's table and cell 24 both ask for all four methods.

**Where the brief and a source disagree — one place, and it matters.** The brief says
"$c_{i,r}$ is a problem-specific normalisation constant; **the paper's default choice is
$|N_r(i)|$**". That is only half the story, and R9 ("read past the quotation") is
exactly what catches it. I downloaded Schlichtkrull et al. (arXiv:1703.06103v4,
`refs/rgcn_1703.06103.pdf`):

- §2.1 Eq. (2): "$c_{i,r}$ is a problem-specific normalization constant that can either
  be learned or chosen in advance (such as $c_{i,r} = |N_i^r|$)." — an *example*, not a
  default.
- §5.2 (**link prediction**, which is our task): "We found a normalization constant
  defined as $c_{i,r} = c_i = \sum_r |N_i^r|$ — in other words, applied across relation
  types – to work best."

So the paper's own link-prediction experiments used the *pooled* constant, not the
per-relation one. I still implemented $c_{i,r}=|N_r(i)|$ (reasons below), but I say in
`answer.tex` that Eq. (2) only *offers* it, I attribute the pooled constant correctly to
the link-prediction experiments, and I report its measured score here. I did **not**
write "the paper's default".

I also checked §2.2 before calling the two decompositions optional regularisers: the
section is titled "Regularization" and reads "we introduce two separate methods for
regularizing the weights of R-GCN-layers: basis- and block-diagonal-decomposition".

## What I decided it needed

**code** (required and primary — the question names functions to complete, and the brief
overrides the usual "no code listing" rule) + **plain** (a short justification).
**No diagram**: nothing in Q4 says show/plot/draw, the brief forbids inventing one, and
I did not produce one.

## What I did

Reproduced the notebook's cells as a plain script, wrote `MyRGCNConv`, and ran the frozen
harness.

Design: `aggr="mean"` — which *is* the $1/c_{i,r}$ factor with $c_{i,r}=|N_r(i)|$;
`self.root = nn.Linear(in, out, bias=True)` is $W_0$; `self.rel[r] =
nn.Linear(in, out, bias=False)` is $W_r$, one full matrix per relation with no basis and
no block-diagonal decomposition. `forward` slices `edge_index` by `edge_type` and calls
`propagate` once per relation subset, so `edge_type` never has to enter `propagate` and
the stub's `message(self, x_j)` signature is untouched. $W_r$ is applied **before**
propagating (legal because $c_{i,r}$ is independent of $j$ and $W_r$ is linear), and
`size=(n, n)` is passed so relation 0 — whose edges touch only the 7,624 users — still
returns all 15,466 rows.

Three independent correctness checks, not just "it runs":

1. **Brute force.** `run/sanity_check.py` lifts the class out of `run/rgcn_run.py` by
   AST (so it tests the exact delivered source) and compares against a Python-loop
   reference on a toy 6-node, 2-relation graph: max abs difference 5.96e-08. It also
   checks the isolated node equals $W_0 h_i$ exactly, that a relation with zero edges is
   skipped, that `size=(N,N)` is honoured, that `reset_parameters()` is safe twice,
   parameter count $(R+1)\cdot\text{in}\cdot\text{out}+\text{out}$, and that gradients
   reach every $W_r$.
2. **PyG's own layer, on the real graph.** `run/check_vs_pyg.py` copies my weights into
   `torch_geometric.nn.RGCNConv(..., aggr="mean", num_bases=None)` and compares
   forward passes on the full 6,067,650-edge graph: **max abs difference 4.17e-07**.
3. **PyG's layer through the same frozen harness**: val MRR 0.2076 / test 0.2084,
   inside my layer's own run-to-run spread (0.190 ± 0.020 / 0.182 ± 0.023). The weak
   metric is therefore the task, not the implementation.

Harness untouched, and mechanically so: `run/build_runner.py` *generates*
`run/rgcn_run.py` by splicing the notebook's cells straight out of the `.ipynb`, and
`run/verify_fidelity.py` re-checks every line of cells 5, 11, 12, 25, 26 and 28 against
the original — 0 mismatches. The only edits are the two stated cuts (cell 7's trailing
`X = node2vec_features(...)`, and cell 28's bare `train_and_eval_hetero("R-GCN")` call
moving under `__main__`).

## Intermediate steps and code

All paths relative to PLAYGROUND. Interpreter is `./.venv/bin/python`; run from `run/`.

| path | what it does |
|---|---|
| `run/my_rgcn_conv.py` | **the answer itself** — the `MyRGCNConv` class, nothing else |
| `run/build_runner.py` → `run/rgcn_run.py` | assembles the runnable script by splicing the notebook's cells 3, 5, 7, 11, 12, 25, 26, 28 **verbatim out of the original `.ipynb`** and inserting `my_rgcn_conv.py` as cell 27. Two cuts only, both named in its docstring. `answer.tex`'s listing is extracted from `rgcn_run.py` by AST. |
| `run/verify_fidelity.py` → `run/verify_fidelity.log` | proves the splice by **contiguous-block** comparison: cells 3, 5, 11, 12, 25, 26 byte-identical to the `.ipynb`, cells 7 and 28 exact prefixes with only the declared cuts |
| `run/sanity_check.py` → `run/sanity_check.log` | unit checks vs. a brute-force reference (check 1 above) |
| `run/check_vs_pyg.py` → `run/check_vs_pyg.log` | equivalence with `torch_geometric.nn.RGCNConv`, that layer through the harness, and 5 torch-seeds of mine in one process |
| `run/diagnose.py` → `run/diagnose.log` | random/no-GNN baselines, 50-epoch val curve with no early stopping, per-relation contribution norms |
| `run/diagnose2.py` → `run/diagnose2.log` | within-process determinism, 1-thread determinism, the pooled $c_i=\sum_r\|N_r(i)\|$ variant, and the score-collapse measurement |
| `run/ablation.py` → `run/ablation.log` | **round 1**: the $\|N_r(i)\|/c_i$ rescaling and the 4-variant × 3-seed ablation, with variant A asserted bit-identical to the delivered layer |
| `run/leak_check.py` → `run/leak_check.log` | **round 1**: shows the training positives are exactly the relation-0 edges |
| `run/degrees.py` → `run/degrees.log` | exact per-relation $\|N_r(i)\|=0$ counts and mean degrees |
| `run/repro_probe.py` → `run/repro_probe.log` | isolates the cross-process nondeterminism to `Word2Vec(workers=4)` |
| `run/make_notebook.py` | writes `Practice3_pyg_basics_p2_completed.ipynb` (cell 27 replaced, nothing else touched) |
| `gen_answer.py` | builds `OUTPUT/answer.tex`: pulls the class source out of `run/rgcn_run.py` by AST and every number out of a `.log`, so the fragment cannot drift |
| `texcheck/` | `pdflatex` smoke test of the fragment inside a 5-section wrapper |
| `refs/rgcn_1703.06103.pdf` | the R-GCN paper, for the R9 check |

**Reproducing each number**

    cd run
    python3 build_runner.py                  # regenerate rgcn_run.py from the .ipynb
    ../.venv/bin/python verify_fidelity.py   # 0 harness lines altered
    ../.venv/bin/python rgcn_run.py          # the headline table (RESULT_JSON line)
    ../.venv/bin/python sanity_check.py      # 5.96e-08 brute-force agreement
    ../.venv/bin/python check_vs_pyg.py      # 4.2e-07 vs RGCNConv; PyG val MRR 0.208
    ../.venv/bin/python diagnose2.py         # pooled-c_i MRRs; the ln2 collapse
    ../.venv/bin/python ablation.py          # the rescaling factors and A/B/C/D
    ../.venv/bin/python leak_check.py        # train positives == relation-0 edges
    ../.venv/bin/python degrees.py           # the |N_r(i)|=0 counts
    python3 ../gen_answer.py                 # rebuilds OUTPUT/answer.tex from the logs

## Results

Every figure in `answer.tex`, with its source. All logs were regenerated after the final
rebuild of `run/rgcn_run.py`, so no number below predates the delivered source.

| claim in answer.tex | value | where it came from |
|---|---|---|
| selected epoch | 13 | `run/rgcn_run.log` (= `rgcn_run_1.log`), `RESULT_JSON` |
| val MRR / Hit@1 | 0.2291 / 0.0782 | same line |
| test MRR / Hit@1 | 0.2229 / 0.0714 | same line |
| val MRR over five runs | 0.190 ± 0.020 | `rgcn_run_1..5.log`, population sd, computed in `gen_answer.py` |
| test MRR over five runs | 0.182 ± 0.023 | same |
| random-tie-breaking baseline MRR 0.174 | 0.1736 | $H_{21}/21$, a closed form; also printed by `diagnose.py` |
| PyG `RGCNConv` val MRR 0.208 | 0.2076 | `check_vs_pyg.log`, `PYG_RESULT_JSON` |
| agreement with `RGCNConv`: $4\times10^{-7}$ | 4.172e-07 | `check_vs_pyg.log` |
| 6,067,650 edges; 15,466 nodes; 3,014,361 messages | — | `rgcn_run.log` header |
| "all 15,466 nodes have $\|N_r(i)\|=0$ for some $r$" | 15466 of 15466 | `degrees.log` |
| "the dense relations" (context for the scale factors) | mean degrees 384.4 and 404.6 vs `friend` 5.6 | `degrees.log` |
| pooled $c_i$ val MRR 0.305 | variant B, 3 seeds → 0.3053 | `ablation.log` (corroborated independently at 0.2864 by `diagnose2.log` part (c), a different process) |
| "leaves their scale at ×1.00, ×0.98" | `listens` 1.0000, `listened_by` 0.9785 | `ablation.log` |
| "dividing the sparse `friend` term by 22" | 0.0451 mean ratio = 22.1× | `ablation.log` |
| "whose edges *are* the training positives" | 19,464 of 19,464 train positives are relation-0 edges; 0 of 4,171 val and 0 of 4,171 test | `leak_check.py` |
| `friend` pooled alone val MRR 0.325 | variant C, 3 seeds → 0.3253 | `ablation.log` |
| "training loss settles at $\ln 2$" | 0.69310 vs $\ln 2$ = 0.69315 | `diagnose2.log` part (d) |
| "dot-product scores collapsed towards zero" | val score sd 1.93e-03, mean embedding row norm 0.156 | `diagnose2.log` part (d) |

Context not quoted in `answer.tex` but worth the validator's attention: the raw
metapath2vec features scored by plain dot product give val MRR 0.1695 / test 0.1671
(`diagnose.log`) — *below* the 0.1736 chance line. The input features carry almost no
friend-prediction signal through a dot product, which is the real reason this question's
numbers are weak.

**Which run is "the" run, and why the numbers move.** Run 1 of five is reported — a rule
fixed before looking at values, not the best of five. (An earlier batch, before the
`build_runner.py` rebuild, had run 1 as the *weakest* of its five; this batch has it as
the strongest. I did not swap either time, and the five-run spread is printed next to the
table in `answer.tex` precisely so a single draw cannot mislead.)

Three separate sources of variation, measured rather than assumed:

1. **Across processes — large, and the one that matters.** Cell 26 trains gensim
   `Word2Vec` with `workers=4`. `run/repro_probe.log`: `X_HETERO` hashes differently in
   two processes at `workers=4` (with `PYTHONHASHSEED` both unset *and* pinned to 0), and
   **identically** at `workers=1`. This is the notebook's own code, not mine, and it hits
   Q1–Q3 the same way (cell 7 also uses `workers=4`).
2. **Within one process, 16 torch threads — tiny.** `diagnose2.log` part (a): two seed-0
   runs give val MRR 0.1933 and 0.1932. Multithreaded CPU scatter-reduce sums floats in a
   nondeterministic order.
3. **Within one process, `torch.set_num_threads(1)` — none.** Part (b): the two runs are
   identical to every digit printed.

## Deliverables

- `OUTPUT/answer.tex` — one `\section`, `\label{p2:sec:rgcn}`, style `pTwoPyStyle`,
  colours `pTwoKw/pTwoCmt/pTwoStr/pTwoRule`. All `p2`-namespaced; no digits in control
  sequences; no macros defined. No `\documentclass`/`\usepackage`/`document`.
- `OUTPUT/preamble.txt` — `listings`, `xcolor`, `booktabs`, `amsmath`.
- No figures (`fig_p2_*.pdf` absent by design; see above).
- `lint_output.py` passes. `crosscheck.py` exits 0, but it prints
  `skipping p2 -- not finished (running)`, so it does **not** actually examine this
  problem's labels while the run is in flight — the earlier "0 collisions" wording
  overclaimed. The only label I define is `p2:sec:rgcn`, and the only other global names
  are `pTwoPyStyle` and `pTwoKw/Cmt/Str/Rule`; all are `p2`-namespaced, which I checked by
  hand (`grep` output in the Deliverables bullet above).
- `pdflatex` compiles the fragment inside a 5-section wrapper with **no** overfull or
  underfull boxes and 0 errors (`texcheck/compile.log`, rendered to
  `texcheck/pg-{1,2}.png`, which I looked at).
- Prose word count (listing and table excluded): **287**, printed by `gen_answer.py` (up 19 from round 1: the corrected mechanism carries three measurements the wrong one did not). R8's allowance for a multi-sub-part answer is 290.
- Not in OUTPUT, for the validator: `Practice3_pyg_basics_p2_completed.ipynb`.

## Where I am least confident

1. **The result sits at the chance line, and that is the honest answer.** Over five
   runs val MRR is 0.190 ± 0.020 against a 0.1736 random-tie-breaking baseline; individual
   draws land anywhere from 0.170 (below chance) to 0.229. I chased this rather than
   reporting it blind: training loss converges to $\ln 2$ with embedding row norms of
   0.156, i.e. the dot-product scorer collapses to ~0 and `evaluate_ranking` is then
   ranking tie-break noise. A grader may read a near-chance number as a broken layer. My
   defence is check 2 — agreement with PyG's `RGCNConv` to 4.2e-07 on the real graph —
   and check 3 — PyG's own layer scoring 0.2076 through the same harness, inside my own
   spread. If my validator can show the layer is wrong, both cross-checks have to be
   wrong too.
2. **$c_{i,r}=|N_r(i)|$ vs the pooled $c_i$.** The pooled constant scores much better
   here (0.305 vs 0.181 in the like-for-like ablation) *and* is what the paper used for
   link prediction — and round 1 showed the reason is that it suppresses the relation that
   leaks the training labels, which is a property of this split rather than of R-GCN. I
   still shipped the per-relation mean, because the notebook writes $c_{i,r}$ with an $r$
   subscript, the stub exposes a single `aggr=` slot, the brief directs it, and it is
   what `RGCNConv`'s documented default does. This is the one substantive judgement call
   in the answer; if the validator thinks the pooled constant is the better deliverable,
   it is a one-line change in `forward` and `diagnose2.py` already has the measurements.
3. **Bias on $W_0$.** The formula has no bias term. I put `bias=True` on the root linear
   (as `MySAGEConv` does and as `RGCNConv` does) and said so only implicitly, in the
   code. If a grader reads the formula strictly, that is an extra $\text{out}$
   parameters.
4. **Prose length.** 287 words, against R8's 290 allowance for an answer with several sub-parts (the validator counted 266 for round 1 and called it within target). It is closer to the ceiling than I would like. The
   brief asked for 150–190 words of justification covering four separate points plus a
   measured result; I judged the chance-baseline, irreproducibility and cross-check
   sentences to be load-bearing rather than padding, but they are the first things to cut.
5. **Every log was produced by a plain shell redirect from the script beside it**, so
   nothing here is transcribed by hand — but the baselines inside `run/diagnose.log`
   were measured in a *different* process from `run/rgcn_run.log`, hence a different
   `X_HETERO` draw. The one number I take from it and quote in `answer.tex` is the
   random-tie-breaking baseline $H_{21}/21 = 0.1736$, which is a closed form and does
   not depend on the draw.
