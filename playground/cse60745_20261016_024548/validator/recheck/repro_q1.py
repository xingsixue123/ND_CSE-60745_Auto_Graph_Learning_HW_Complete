import torch
torch.set_num_threads(8)
from gt_framework import *
from solution import LapPETransformer, SPDAttention
run_graph_task("LapPE + SPD", LapPETransformer(attention_cls=SPDAttention))
