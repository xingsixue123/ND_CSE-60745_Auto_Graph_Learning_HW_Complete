import json, time, urllib.request
from pathlib import Path
import numpy as np, pandas as pd, torch
from torch_geometric.utils import coalesce, degree, to_undirected
GITHUB_REPO="antman9914/CSE60745-Practice"; BRANCH="main"
REQUIRED={"data/task1":["split_stats.json","lp_graph_obs.csv","lp_train.csv","lp_val.csv","lp_test.csv"],
          "data/task3":["hetero_stats.json","user_artist.csv.gz"]}
t0=time.time()
for d,names in REQUIRED.items():
    Path(d).mkdir(parents=True,exist_ok=True)
    for name in names:
        p=Path(d)/name
        if not p.exists():
            urllib.request.urlretrieve(f"https://raw.githubusercontent.com/{GITHUB_REPO}/{BRANCH}/{d}/{name}",p)
print(f"download {time.time()-t0:.1f}s")
n=json.loads(Path("data/task1/split_stats.json").read_text())["n_nodes"]
def as_edge_index(df):
    e=df[["src","dst"]].to_numpy().T
    return coalesce(to_undirected(torch.from_numpy(e).long()),num_nodes=n)
train_edges=pd.read_csv("data/task1/lp_graph_obs.csv")
splits={s:pd.read_csv(f"data/task1/lp_{s}.csv") for s in ("train","val","test")}
val_pos=splits["val"].query("label == 1")[["src","dst"]]
tv=pd.concat([train_edges[["src","dst"]],val_pos],ignore_index=True)
EI=as_edge_index(train_edges); EITV=as_edge_index(tv)
print("nodes",n,"| EI_TRAIN",EI.size(1)//2,"undirected | isolated",int((degree(EI[1],n)==0).sum()))
print("EI_TRAINVAL",EITV.size(1)//2)
for s in ("train","val","test"):
    df=splits[s]; print(s,df["query_id"].nunique(),"queries",len(df),"pairs")
# evaluate_ranking smoke test under pandas 3
def evaluate_ranking(df,scores,seed=0):
    rng=np.random.default_rng(seed); d=df[["query_id","label"]].copy(); d["score"]=scores
    d["tiebreak"]=rng.random(len(d))
    d=d.sort_values(["query_id","score","tiebreak"],ascending=[True,False,True])
    d["rank"]=d.groupby("query_id").cumcount()+1
    pos=d.loc[d["label"]==1,["query_id","rank"]]
    return {"hit@1":float((pos["rank"]==1).mean()),"MRR":float((1.0/pos["rank"]).mean())}
print("rand eval", evaluate_ranking(splits["val"], np.random.default_rng(0).random(len(splits["val"]))))
t=time.time(); ua=pd.read_csv("data/task3/user_artist.csv.gz")
print("user_artist rows",len(ua),"cols",list(ua.columns),f"{time.time()-t:.1f}s")
