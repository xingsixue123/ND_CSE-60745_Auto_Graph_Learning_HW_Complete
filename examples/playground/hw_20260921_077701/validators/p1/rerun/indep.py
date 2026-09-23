from collections import deque
T={1:(1,10),2:(2,4),3:(3,1),4:(4,6)}
def run(arrivals_first):
    rem={i:T[i][1] for i in T}; q=deque(); tl=[]; prev=None
    for t in range(30):
        if not arrivals_first and prev is not None: q.append(prev); prev=None
        for i in sorted(T, key=lambda i:(T[i][0],i)):
            if T[i][0]==t: q.append(i)
        if arrivals_first and prev is not None: q.append(prev); prev=None
        if not q: tl.append(None); continue
        c=q.popleft(); tl.append(c); rem[c]-=1
        if rem[c]>0: prev=c
        if not any(rem.values()): break
    return tl
for lbl,af in (("RR arrivals-first",True),("RR preempted-first",False)):
    tl=run(af)
    comp={}
    for t,w in enumerate(tl):
        if w is not None: comp[w]=t+1
    print(f"{lbl:22}", " ".join("--" if x is None else f"T{x}" for x in tl))
    print(" "*22, "C:", {f"T{i}":comp[i] for i in sorted(comp)})
