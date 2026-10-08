# p1 — HW3-Part(A), Q1 / Q2 / Q3 / Q5

## What the problem asked

Complete four `MessagePassing` subclasses from the Practice-3 notebook — `MyGCNConv`
(Q1), `MyGATConv` (Q2), `MyGINConv` (Q3), `MyDeepConv` (Q5) — implementing
`__init__`, `reset_parameters`, `forward` and `message` in each, run them on the LastFM
Asia friend-recommendation task with the notebook's frozen harness, and report real
val/test MRR and Hit@1. Q5 additionally asks for a layer that "stays useful with an
8-hop receptive field", with the explicit hint that **8 hops is not 8 layers**.
Deliverables: one `answer.tex` fragment with four sections, one results table, one
figure. Q4 (R-GCN) is another worker's and is untouched.

**Channel reconciliation (R7).** All three channels read and agreed:
- `page_002.txt` / `page_003.txt` carry the Q1–Q5 statements;
- `page_002.png` / `page_003.png` show the same text and nothing extra (the footer on
  rendered page 3 says "Page 2 of 4" — the cover page offsets it, as the brief warned);
- `page_002_fig_01.png` (727x525, the document's only embedded figure) read at native
  resolution: it is a screenshot of the `MyGCNConv` stub. I compared it line by line
  against notebook cell 15 and they are identical, which confirms the brief's claim
  rather than taking it on trust. No new information is in the figure.

**Where the brief and the source differ.** One discrepancy, cosmetic: the brief numbers
notebook cells 1-indexed ("cell 16" for the GCN stub, "cell 32" for the Q5 run). The
`.ipynb` is 0-indexed — GCN stub = cell 15, GAT = 18, GIN = 21, `MyDeepConv` = 30, the
Q5 run = 31, 32 cells total. Content identical; only the convention differs. I use
0-indexed numbers throughout. Nothing else in the brief conflicted with the page.

## What I decided it needed

**All three: plain + code + diagram.**
- *code* — the question type is "complete these functions", so the listings are the
  answer, and every reported number comes from an actual training run.
- *plain* — ~150–200 words per question justifying the implementation decisions the
  notebook's formulas do not fix (aggregation, self-loops, head layout, MLP shape).
- *diagram* — `fig_p1_depth.pdf`, test MRR against receptive-field depth, which is the
  evidence for the Q5 claim. Without it "stays useful" is an assertion.

## What I did

Ported the notebook's frozen harness verbatim into `run/common.py` (cells 2, 4, 6, 8,
10, 11) and **ran the GraphSAGE demo first**, as cell 12 instructs, before writing any
of my own layers. Its data stats reproduce the brief's measured facts exactly (7,624
nodes; 19,464 / 23,635 undirected edges; 666 isolated; 19,464 / 4,171 / 4,171 queries).

Then wrote the four layers in `run/layers.py` and, before training anything, **checked
each against PyG's own reference implementation with the parameters copied across**
(`run/test_layers.py`). `MyGCNConv` vs `GCNConv`, `MyGATConv` vs `GATConv`, `MyGINConv`
vs `GINConv`, and `MyDeepConv`'s propagation vs `APPNP` all agree to **0.0 in floating
point**; `MyGCNConv` also matches a hand-computed 4-node graph including an isolated
node. This is what makes the layers trustworthy independently of how well they score.

For Q5 I used **APPNP-style decoupled propagation**: a 2-layer MLP, then `K`
personalised-PageRank steps `Z <- (1-a) A_hat Z + a H` inside a *single* layer. One
`propagate` is one hop, so `K=8` at `n_layers=1` is exactly 8 hops — which is the
structural point the question is making, and `n_layers` in cell 31 is set to 1
accordingly. `alpha=0.3` was chosen **on validation MRR only**, over a 9-point
(alpha, dropout) grid and then a 7-point alpha refinement that confirms a plateau
(val 0.733–0.737 for alpha in [0.25, 0.5], falling to 0.699 at 0.20).

I read both cited papers in full rather than from the abstract (R9). Li, Han & Wu's
Theorem 1 and — importantly — their actual proposed remedy (co-training with a
random-walk model, plus self-training, keeping the GCN *shallow*) are characterised
correctly in the answer; I explicitly do **not** claim they leave the problem
undiagnosed or unaddressed.

## Intermediate steps and code

All paths relative to PLAYGROUND. Run everything with `./.venv/bin/python` from `run/`,
with `MPLCONFIGDIR=$PWD/.mplcache`.

| file | what it does |
|---|---|
| `run/common.py` | the notebook's frozen harness, ported verbatim; caches node2vec X |
| `run/layers.py` | **the four layers** — the source the answer's listings come from |
| `run/demo_sage.py` | step 1: the GraphSAGE demo end to end (cell 13) |
| `run/test_layers.py` | correctness vs PyG's `GCNConv`/`GATConv`/`GINConv`/`APPNP` |
| `run/run_all.py` | **the main table and the depth sweep** |
| `run/tune_deep.py`, `run/tune_alpha.py` | Q5 (alpha, dropout) selection on val MRR |
| `run/sweep_seeds.py` | the depth sweep over seeds 0/1/2 — the figure's data |
| `run/seeds_all.py` | all six table rows over seeds 0/1/2 (stability evidence) |
| `run/robustness.py` | repeat-at-seed-0 + 3-seed check on the three headline rows |
| `run/gin_probe.py` | the degree-vs-norm measurement quoted in Q3 |
| `run/make_fig.py` | writes `fig_p1_depth.pdf` into OUTPUT |
| `run/build_notebook.py` | writes `Practice3_pyg_basics_completed.ipynb` |
| `run/exec_notebook.py` | executes that notebook end to end (Q4 cells skipped) |
| `Practice3_pyg_basics_completed.ipynb` | the completed notebook (kept out of OUTPUT per R4) |
| `run/logs/*.json`, `run/logs/*.log` | the raw console output behind every number |

**Which command reproduces which number**

- every row of the results table, and the single-seed depth sweep → `python run_all.py`
  (writes `run/logs/results.json`; console in `run/logs/run_all.log`)
- the figure's data (3 seeds per depth) → `python sweep_seeds.py` → `logs/sweep_seeds.json`
- the figure itself → `python make_fig.py`
- the alpha plateau quoted in Q5 → `python tune_alpha.py` → `logs/tune_alpha.json`
- the Q3 degree/norm numbers → `python gin_probe.py`
- the layer-correctness claim → `python test_layers.py` (prints `ALL CHECKS PASSED`)

## Results

All table numbers are seed 0 (the harness default) on the cached node2vec features,
from `run/logs/results.json`:

| row | val MRR | val Hit@1 | test MRR | test Hit@1 |
|---|---|---|---|---|
| GraphSAGE (demo, control) | 0.6243 | 0.4682 | 0.6281 | 0.4666 |
| GCN, 2 layers (Q1) | 0.7263 | 0.6085 | 0.7379 | 0.6253 |
| GAT (Q2) | 0.6210 | 0.4479 | 0.6365 | 0.4678 |
| GIN (Q3) | 0.4433 | 0.2870 | 0.4417 | 0.2793 |
| GCN, 8 layers | 0.3754 | 0.2208 | 0.3919 | 0.2318 |
| MyDeepConv, 8 hops, 1 layer (Q5) | 0.7376 | 0.6262 | 0.7492 | 0.6421 |

Figure data, test MRR, mean over seeds 0/1/2 (`run/logs/sweep_seeds.json`):

| hops | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| `MyGCNConv` (= n_layers) | 0.7244 | 0.5370 | 0.4036 | 0.3972 |
| `MyDeepConv` (= K, 1 layer) | 0.7248 | 0.7255 | 0.7257 | 0.7253 |

Other computed claims in `answer.tex`:
- parameter counts 8,320 (GCN-2 and MyDeepConv) and 33,280 (GCN-8) — `logs/results.json`, `params` field.
- alpha plateau: val MRR 0.7370/0.7371/0.7358/0.7372/0.7330 at alpha 0.25/0.30/0.35/0.40/0.50, and 0.6992 at 0.20 — `logs/tune_alpha.json`.
- Q3 degree coupling: corr(log degree, log ||z||) 0.868 (GIN) vs 0.632 (GCN); top/bottom degree-decile norm ratio 22.9x vs 2.07x — `run/gin_probe.py`. **Measured at initialisation**, on an untrained model; the answer says "at initialisation".
- "45% of its test MRR": 0.7244 -> 0.3972 is a 45.2% drop.

## Deliverables

- `OUTPUT/answer.tex` — four `\section*`s (Q1, Q2, Q3, Q5), gap left for Q4, one results
  table (`\label{p1:tab:results}`), one figure (`\label{p1:fig:depth}`), hand-written
  `thebibliography` with two entries (`p1:li2018`, `p1:appnp`). Style is
  `p1pystyle`, colours `p1kw`/`p1str`/`p1cmt`; no macros defined. No `\ref` is used
  anywhere, so the unnumbered `\section*`s cannot produce a bad cross-reference.
- `OUTPUT/fig_p1_depth.pdf` — vector, 5.4x3.5in, referenced by bare filename.
- `OUTPUT/preamble.txt` — `amsmath`, `listings`, `xcolor`, `booktabs`, `graphicx`, `float`.
- `python3 framework/tools/lint_output.py <OUTPUT>` → **OUTPUT LINT OK**.
- Compile-tested in `texcheck/`: `latexmk -pdf` exits 0, **no errors, no undefined
  references, no overfull or underfull boxes**, 5 pages. I rendered it and looked at it.

## Where I am least confident

1. **Absolute numbers are not reproducible across feature draws, and this is the most
   important caveat.** The notebook's node2vec step calls
   `gensim.models.Word2Vec(..., workers=4)`, which is non-deterministic regardless of
   `seed=0`. Re-running the notebook from scratch gave a *different* feature matrix and
   noticeably different scores (GAT 0.6952 vs my 0.6365; MyDeepConv 0.7283 vs 0.7492;
   GCN-8 0.3911 vs 0.3919). I therefore computed X once and cached it so all six rows
   share identical inputs, and the answer states the caveat. **A validator re-running
   `run_all.py` with `run/cache/x_node2vec.pt` present will reproduce my table; one who
   deletes the cache, or runs the notebook, will not.** The *ordering* is stable across
   3 seeds and 2 independent feature draws; the absolute values are not.
2. **GAT is the least stable row** (3-seed range 0.5867–0.7000, from `logs/seeds_all.json`).
   Seed 0 lands at 0.6365, near the bottom of that range; on the notebook's independent
   feature draw the same code reached 0.6952 by training to epoch 193 instead of
   stopping at epoch 3. The reported figure is real but pessimistic, and I did not tune
   GAT (the harness's lr/patience are frozen).
3. **MyDeepConv does not beat the 2-layer GCN**, it matches it (3-seed means 0.7254 vs
   0.7244). The defensible claim — and the one the answer makes — is that it is *flat in
   depth* where GCN collapses. I deliberately did not phrase it as a win.
4. **`alpha=0.3` was selected on validation**, which is legitimate, but it is still
   selection: the plateau is wide (0.25–0.5) so the choice is not fragile, yet there is
   a sharp cliff just below it (0.699 at alpha=0.2), and I do not have a principled
   account of why the cliff sits exactly there. The nearby configurations early-stop at
   epoch ~5 rather than training to ~135, so it looks like an optimisation effect rather
   than a property of the operator — but I did not prove that.
5. **The Q3 degree/norm explanation is measured at initialisation**, not after training,
   so it is evidence about the operator's inductive bias rather than a full account of
   why GIN scores 0.44. The answer hedges it as "the likely reason" and gives the
   numbers; it does not claim to be the proven cause.
6. **Head count for GAT (8) is my choice**, not the assignment's. `out_channels=64` is
   divisible by it so each head gets 8 features; the code falls back to 1 head if a
   future `out_channels` is not divisible, which silently changes the model rather than
   erroring. That fallback is untested in a real run.
7. The completed notebook runs cells 0–22 and 28–31. **Cells 23–27 are Q4's and are left
   exactly as shipped**, so a top-to-bottom run of the whole notebook will raise
   `NotImplementedError` at cell 26 (`MyRGCNConv`). That is by design — Q4 is not mine —
   but it means "the notebook runs" is true only for my cells.
