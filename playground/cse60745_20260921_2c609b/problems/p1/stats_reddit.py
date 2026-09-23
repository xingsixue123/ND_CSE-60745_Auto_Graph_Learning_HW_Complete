"""Reddit is a ~1.5 GB download, so it gets its own script and its own run."""
import os
from stats import summarize, ROOT
from torch_geometric.datasets import Reddit

ds = Reddit(root=f"{ROOT}/Reddit")
r = summarize("Reddit (GraphSAGE)", ds[0], ds.num_classes)
print(r)
