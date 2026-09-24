import json, numpy as np, pandas as pd, networkx as nx
from pathlib import Path
D = Path("/home/xing/project/auto_hw_complete/playground/cse60745_20260923_8654c1/data")
stats = json.loads((D/"task1/split_stats.json").read_text())
print("split_stats:", stats)
n_users = stats["n_nodes"]
splits = {n: pd.read_csv(D/f"task1/lp_{n}.csv") for n in ("train","val","test")}
te = pd.read_csv(D/"task1/lp_graph_obs.csv")[["src","dst"]]
G = nx.Graph(); G.add_nodes_from(range(n_users), type="U"); G.add_edges_from(te.itertuples(index=False,name=None))
deg = dict(G.degree())
n_iso = sum(1 for _,d in G.degree() if d==0)
print(f"n_users {n_users} edges {G.number_of_edges()} iso {n_iso} meandeg {np.mean(list(deg.values())):.4f} maxdeg {max(deg.values())} comps {nx.number_connected_components(G)}")
for name,df in splits.items():
    nq = int(df.label.sum()); print(name, nq, len(df)//nq)
country = (pd.read_csv(D/"task2/node_country.csv").set_index("node_id")["country"].reindex(range(n_users)).to_numpy())
split = pd.read_csv(D/"task3/country_split.csv").set_index("node_id")["split"]
cs = {n: np.flatnonzero((split==n).to_numpy()) for n in ("train","val","test")}
print("classes", len(set(country)), {k:len(v) for k,v in cs.items()})
vc = pd.Series(country).value_counts()
print("largest class", vc.iloc[0], "smallest", vc.iloc[-1])
ctest = country[cs["test"]]
print("majority rate on test", pd.Series(ctest).value_counts().iloc[0]/len(ctest))
# smallest class in train split
ctr = pd.Series(country[cs["train"]]).value_counts()
print("smallest-class count in train:", ctr.get(vc.index[-1], 0))
# degree buckets for test/val positives
bins=(0,1,2,4,8,16,np.inf)
for name in ("val","test"):
    df=splits[name]; pos=df[df.label==1]
    b=pd.cut(pos["src"].map(deg), bins=list(bins), right=False)
    print(name, "bucket sizes", b.value_counts().sort_index().tolist())
# hetero
hs = json.loads((D/"task3/hetero_stats.json").read_text()); print("hetero_stats", hs)
ua = pd.read_csv(D/"task3/user_artist.csv.gz")
print("ua edges", len(ua), "users with >=1 artist", ua["user"].nunique())
per = ua.groupby("user").size()
print("artists per user median", per.median(), "max", per.max())
iso = [u for u,d in G.degree() if d==0]
covered = set(ua["user"].unique())
print("cold users with >=1 artist", sum(1 for u in iso if u in covered), "/", len(iso))
print("median artists of cold users", per.reindex(iso).dropna().median())
postest = splits["test"][splits["test"].label==1]
coldsrc = postest[postest["src"].map(deg)==0]["src"]
print("cold test queries", len(coldsrc), "covered", sum(1 for u in coldsrc if u in covered))
art_deg = ua.groupby("artist").size()
print("artist popularity median", art_deg.median(), "n artists", art_deg.nunique(), len(art_deg))
H_nodes = n_users + hs["n_artists"]; print("H nodes", H_nodes, "H edges", G.number_of_edges()+len(ua))
