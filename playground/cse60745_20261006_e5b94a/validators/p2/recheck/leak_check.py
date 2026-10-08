"""Context for why down-weighting `friend` helps: are the training positives the same
edges as relation 0? (Not asserted in answer.tex -- recorded for submission.md.)"""
import torch, rgcn_run as R
tr = R.SPLITS["train"]
pos = tr[tr["label"] == 1][["src", "dst"]].to_numpy()
pos = {tuple(sorted(p)) for p in pos.tolist()}
ei = R.EI_TRAIN
edges = {tuple(sorted((int(a), int(b)))) for a, b in zip(ei[0].tolist(), ei[1].tolist())}
print(f"train positives            {len(pos)}")
print(f"G_train undirected edges   {len(edges)}")
print(f"train positives that ARE a relation-0 edge: {len(pos & edges)} "
      f"({100 * len(pos & edges) / len(pos):.1f}%)")
for s in ("val", "test"):
    d = R.SPLITS[s]
    p = {tuple(sorted(x)) for x in d[d["label"] == 1][["src", "dst"]].to_numpy().tolist()}
    print(f"{s:5} positives that are a relation-0 edge: {len(p & edges)} of {len(p)}")
