import pickle, numpy as np
H = pickle.load(open("../../problems/p2/results_hetero.pkl","rb"))
C = pickle.load(open("../../problems/p2/results_control.pkl","rb"))
P0= pickle.load(open("../../problems/p1/results_full.pkl","rb"))
PS= pickle.load(open("../../problems/p1/results_seeds.pkl","rb"))

def row(r):
    s=r["summary"]; c=r["country"]
    def g(k,alt):
        return s[k] if k in s and s[k] is not None else alt
    return dict(
      vH1=s["lp_val_hit@1"], vMRR=s["lp_val_MRR"],
      tH1=s["lp_test_hit@1"], tMRR=s["lp_test_MRR"],
      vmi=c.loc["val","micro_f1"], vma=c.loc["val","macro_f1"],
      tmi=c.loc["test","micro_f1"], tma=c.loc["test","macro_f1"],
      cold=r["lp"]["test"][1].iloc[0]["hit_at_1"],
    )
def summ(rows):
    ks=rows[0].keys()
    m={k:np.mean([r[k] for r in rows]) for k in ks}
    sd={k:np.std([r[k] for r in rows],ddof=1) for k in ks}
    return m,sd

COLS=["vH1","vMRR","tH1","tMRR","vmi","vma","tmi","tma","cold"]
out={}
# control: summary may be empty -> recompute
def row_ctrl(r):
    c=r["country"]; lp=r["lp"]
    def agg(split):
        df=lp[split][1]
        n=df["n_queries"]; 
        return (df["hit_at_1"]*n).sum()/n.sum(), (df["MRR"]*n).sum()/n.sum()
    vH,vM=agg("val"); tH,tM=agg("test")
    return dict(vH1=vH,vMRR=vM,tH1=tH,tMRR=tM,
        vmi=c.loc["val","micro_f1"],vma=c.loc["val","macro_f1"],
        tmi=c.loc["test","micro_f1"],tma=c.loc["test","macro_f1"],
        cold=lp["test"][1].iloc[0]["hit_at_1"])

# sanity: does weighted-bucket agg reproduce summary for a hetero row?
r=H["metapath U-U-U-A-U|seed0"]
print("agg-vs-summary check:", row_ctrl(r)["tH1"], r["summary"]["lp_test_hit@1"])

p1names={"DeepWalk":"deepwalk","node2vec p=1,q=0.5":"node2vec p=1 q=0.5",
 "node2vec p=1,q=2":"node2vec p=1 q=2","node2vec p=q=0.25":"node2vec p=0.25 q=0.25",
 "RWR r=0.15":"rwr r=0.15","deg-corrected a=1":"degcorr a=1","triadic":"triadic"}
for disp,k in p1names.items():
    rows=[row(P0[k]), row(PS[f"{k} | seed1"]), row(PS[f"{k} | seed2"])]
    out[disp]=summ(rows)
out["control DeepWalk x22"]=summ([row_ctrl(C[f"deepwalk x22|seed{s}"]) for s in (0,1,2)])
for disp,k in [("type-blind DeepWalk on H","hetero-deepwalk"),
  ("metapath U-A-U","metapath U-A-U"),("metapath U-U-A-U","metapath U-U-A-U"),
  ("metapath U-U-U-A-U","metapath U-U-U-A-U"),("U-A-U rare a=1","U-A-U rare-artist a=1")]:
    out[disp]=summ([row(H[f"{k}|seed{s}"]) for s in (0,1,2)])

hdr=f"{'config':28s}"+"".join(f"{c:>8s}" for c in COLS)
print(hdr); print("-"*len(hdr))
for k,(m,sd) in out.items():
    print(f"{k:28s}"+"".join(f"{m[c]:8.4f}" for c in COLS))
print("\n--- within-config sd ---")
for k,(m,sd) in out.items():
    print(f"{k:28s}"+"".join(f"{sd[c]:8.4f}" for c in COLS))
print("\nmean sd over 13 rows:")
for c in COLS:
    print(f"  {c}: {np.mean([sd[c] for m,sd in out.values()]):.4f}   (n rows={len(out)})")
