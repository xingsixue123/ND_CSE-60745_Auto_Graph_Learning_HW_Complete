import torch
from gt_framework import *
from solution import LapPETransformer, SPDAttention, SparseSPDAttention
from hybrid_layer import HybridGTLayer, HybridGT

# shrink ZINC so this is quick, but run the real code paths
for s in ZINC_GRAPHS: ZINC_GRAPHS[s] = ZINC_GRAPHS[s][:300]

print("--- cell 14 ---"); run_graph_task("LapPE + SPD", LapPETransformer(attention_cls=SPDAttention), epochs=1)
print("--- cell 18 ---"); run_graph_task("sparse: LapPE + SPD", LapPETransformer(attention_cls=SparseSPDAttention), epochs=1)
print("--- cell 22 ---"); run_graph_task("hybrid GT", HybridGT(), epochs=1)

def lastfm_model(a): return LapPETransformer(attention_cls=a, dim=32, heads=2, layers=2,
                                             out_dim=N_COUNTRIES, num_atom_types=0, graph_level=False)
print("--- cell 19 ---")
benchmark_step("full: LapPE + SPD", lastfm_model(SPDAttention))
benchmark_step("sparse: LapPE + SPD", lastfm_model(SparseSPDAttention))
run_node_task("sparse: LapPE + SPD", lastfm_model(SparseSPDAttention), epochs=5)
print("ALL CELLS RAN")
