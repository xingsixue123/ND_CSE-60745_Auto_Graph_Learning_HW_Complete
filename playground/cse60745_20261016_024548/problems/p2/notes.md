# p2 — Q3 Hybrid Graph Transformer — plan

## What the problem needs
- **code** (required): implement `HybridGTLayer`, actually run cell 22 on ZINC, report real MAE.
- **plain** (required): ~400 words of prose stating the design and justifying the combination rule.
- **diagram**: optional. Decide after results; a clean table may be enough. Candidate: bar chart of the ablation.

## Design (to be validated by experiment)
GraphGPS-style layer, both branches on the same input, summed in parallel.
- Local branch: GINE from scratch (sum aggregation, bond-type embedding inside the message,
  (1+eps)*x + sum ReLU(x_j + e_ij), then a 2-layer MLP). Sum aggregation because ZINC is a
  counting/substructure task (GIN); bond type enters the message, not the aggregation.
- Global branch: masked multi-head self attention over `to_dense_batch(x, batch)` so a node
  can only attend inside its own molecule. Same algebra as the framework's `Attention`.
- Fusion: residual + LayerNorm per branch, sum, then residual FFN + LayerNorm.
  (GraphGPS uses BatchNorm; LayerNorm matches the framework's TransformerBlock and does not
  depend on batch composition.)

## Experiments (every number from a real run, logged)
baselines: plain GraphTransformer; demo CentralityTransformer+CNAttention.
main: HybridGT (cell 22, verbatim).
ablations: local-only, global-only  (do the two branches both matter?)
combination-rule ablation: sequential (local then global), gated sum  (why parallel sum?)

## Hard constraints to check explicitly
- attention must not cross molecules -> verify with an explicit test, not by eye.
- bond ids in ZINC are {1,2,3}; embedding sized 4 ([0,4) per the docstring).
- do not edit gt_framework.py; do not touch Q1/Q2 classes.
