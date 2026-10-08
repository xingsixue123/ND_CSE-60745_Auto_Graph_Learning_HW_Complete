# p1 — notes (updated after the work was done)

## Channel reconciliation (R7)
- `page_002.txt` / `page_003.txt`: the Q1–Q5 statements; match the brief.
- `page_002.png` / `page_003.png`: same text, nothing extra. Footer "Page 2 of 4" on
  rendered page 3 — cover page offsets by 1, as the brief warned.
- `page_002_fig_01.png` (727x525) read at native resolution: a screenshot of the
  `MyGCNConv` stub. Compared line by line against notebook cell 15 — identical.
  Confirmed for myself rather than taking the brief's word.
- DISCREPANCY (cosmetic): the brief cites notebook cells 1-indexed; the `.ipynb` is
  0-indexed (GCN stub 15, GAT 18, GIN 21, MyDeepConv 30, Q5 run 31; 32 cells).

## What this needed
plain + code + diagram. Decided before starting; unchanged.

## What actually happened (deviations from the original plan)
1. Ran GraphSAGE first (cell 12's instruction). Data stats reproduce the brief exactly.
2. Added a correctness-vs-PyG test (`test_layers.py`) that was NOT in the plan. It is
   the strongest evidence in the submission: all four layers agree with
   `GCNConv`/`GATConv`/`GINConv`/`APPNP` to 0.0 in floating point.
   It also caught that PyG's `GINConv` does not strip self-loops while mine does —
   the difference is confined to exactly the self-loop-carrying nodes, which is correct
   (the notebook's GIN formula is the OPEN neighbourhood).
3. Q5 = APPNP, as planned. But the planned alpha=0.1 scored only 0.6866 test MRR.
   Tuned (alpha, dropout) on VALIDATION MRR: alpha=0.3, no internal dropout, which sits
   on a plateau (0.25–0.5). Removed the dropout from the layer after checking
   `F.dropout(p=0)` is an exact no-op that does not touch the RNG, so the shipped code
   is numerically what was tuned.
4. Figure upgraded from single-run lines to 3-seed mean + min/max band, because the
   single-seed version made a claim the seeds did not fully support.
5. Caching node2vec X turned out to matter more than expected: `Word2Vec(workers=4)` is
   non-deterministic, and a fresh feature draw moves GAT by ~0.06 MRR. All rows share
   one cached X. This is the biggest reproducibility caveat and is flagged in both
   `answer.tex` and `submission.md`.

## Design decisions (as shipped)
- GCN: `aggr="add"`; `remove_self_loops` then `add_self_loops`; `degree` on
  `edge_index[1]`; W before `propagate`; bias after aggregation.
- GAT: `node_dim=0`; attention split into `att_src`/`att_dst`; self-loops before
  softmax; heads=8, head width `out_channels//heads`; `concat` is a constructor
  default (the layer cannot know it is last) with `concat=False` giving the
  averaging variant.
- GIN: `aggr="add"`; OPEN neighbourhood; MLP Linear-BN-ReLU-Linear; eps learnable,
  init 0; `reset_parameters` walks the Sequential's children.
- MyDeepConv: APPNP. K=8 steps in ONE layer => 8 hops at n_layers=1 (cell 31 set to 1).
  alpha=0.3. 8,320 params — same as GCN-2, a quarter of GCN-8.

## Verification done
- `test_layers.py` — ALL CHECKS PASSED (incl. reset_parameters twice).
- listings in `answer.tex` are byte-identical to `run/layers.py` and to the completed
  notebook's cells (checked programmatically).
- every number in `answer.tex` traced back to `run/logs/results.json` programmatically.
- `latexmk -pdf` in `texcheck/`: exit 0, no errors, no undefined refs, no overfull or
  underfull boxes, 5 pages; rendered to PNG and inspected.
- `lint_output.py` — OUTPUT LINT OK.
