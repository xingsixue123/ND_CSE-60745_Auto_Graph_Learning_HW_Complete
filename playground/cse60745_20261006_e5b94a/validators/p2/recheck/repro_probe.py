"""Why do two runs of the notebook give different metrics? Isolate it to X_HETERO,
then attribute: gensim Word2Vec's `workers` (thread race) vs PYTHONHASHSEED (gensim
seeds each word's initial vector from hash(word + str(seed))).
"""
import hashlib, os, sys, numpy as np, torch
import rgcn_run as R

workers = int(sys.argv[1])
def feats():
    import random, time
    from gensim.models import Word2Vec
    # same walks as cell 26 (random.Random is deterministic), only `workers` varies
    import types
    src = R.metapath2vec_features.__code__
    return R.metapath2vec_features(R.HETERO, schema="UAU")

if workers == 1:
    # monkeypatch the Word2Vec constructor used inside cell 26 to workers=1
    import gensim.models
    _W = gensim.models.Word2Vec
    class W1(_W):
        def __init__(self, *a, **k):
            k["workers"] = 1
            super().__init__(*a, **k)
    import rgcn_run
    rgcn_run.Word2Vec = W1

X = feats()
h = hashlib.sha256(X.numpy().tobytes()).hexdigest()[:16]
print(f"PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED','<unset>')} workers={workers} "
      f"X_HETERO sha256[:16]={h}")
