import pickle, pprint, sys
for p in ["../../problems/p2/results_hetero.pkl",
          "../../problems/p2/results_control.pkl",
          "../../problems/p1/results_full.pkl",
          "../../problems/p1/results_seeds.pkl"]:
    try:
        d = pickle.load(open(p,"rb"))
    except Exception as e:
        print(p, "ERR", e); continue
    print("="*70); print(p, type(d))
    if isinstance(d, dict):
        ks=list(d.keys()); print("keys:", ks[:12], "..." if len(ks)>12 else "", "n=",len(ks))
        k0=ks[0]; print("sample key:", repr(k0)); print("sample val type:", type(d[k0]))
        pprint.pprint(d[k0], depth=3, compact=True)
    else:
        print(repr(d)[:2000])
