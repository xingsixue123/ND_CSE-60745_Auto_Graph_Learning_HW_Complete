import torch
torch.set_num_threads(8)
from gt_framework import *
from hybrid_layer import HybridGT
run_graph_task("hybrid GT", HybridGT())
