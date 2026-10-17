"""Run one named experiment. Usage: run_exp.py <name> [seed] [epochs]"""
import sys, torch
torch.set_num_threads(int(__import__("os").environ.get("NTHREADS", "4")))
import gt_framework
from gt_framework import *
from gt_framework import _prepare   # star-import skips underscore names
from hybrid_layer import HybridGTLayer, HybridGT
from variants import (LocalOnlyLayer, GlobalOnlyLayer, SequentialLayer,
                      GatedLayer, AblationGT)

EXPERIMENTS = {
    # baselines, straight from gt_framework (item 5 of the brief)
    "baseline-plain":  lambda: ("baseline: plain transformer", GraphTransformer()),
    "baseline-demo":   lambda: ("baseline: centrality + CN", CentralityTransformer(attention_cls=CNAttention)),
    # the answer: notebook cell 22, verbatim
    "hybrid":          lambda: ("hybrid GT", HybridGT()),
    # ablations: does each branch matter?
    "local-only":      lambda: ("ablation: local branch only", AblationGT(LocalOnlyLayer)),
    "global-only":     lambda: ("ablation: global branch only", AblationGT(GlobalOnlyLayer)),
    # ablations: does the combination rule matter?
    "sequential":      lambda: ("combination: sequential", AblationGT(SequentialLayer)),
    "gated":           lambda: ("combination: gated", AblationGT(GatedLayer)),
}


def active_params(name):
    """Parameters that actually receive a gradient (an ablation inherits modules it never calls)."""
    _, probe = EXPERIMENTS[name]()
    graphs = ZINC_GRAPHS["train"][:8]
    node_fn, pair_fn, pairs_fn = _prepare(probe, graphs)
    probe(make_batch(graphs, node_fn, pair_fn, pairs_fn)).sum().backward()
    total = sum(p.numel() for p in probe.parameters())
    used = sum(p.numel() for p in probe.parameters() if p.grad is not None)
    return total, used


name = sys.argv[1]
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
epochs = int(sys.argv[3]) if len(sys.argv) > 3 else gt_framework.EPOCHS_ZINC
gt_framework.RANDOM_SEED = seed      # read by _reset() and by run_graph_task()'s batch order
n_total, n_params = active_params(name)
label, model = EXPERIMENTS[name]()
print(f"### experiment={name} seed={seed} epochs={epochs} label={label!r} "
      f"params_active={n_params} params_allocated={n_total}", flush=True)
best = run_graph_task(label, model, epochs=epochs)
print(f"### result {name} seed={seed} epochs={epochs} val={best['val']:.4f} "
      f"test={best['test']:.4f} epoch={best['epoch']} params={n_params}", flush=True)
