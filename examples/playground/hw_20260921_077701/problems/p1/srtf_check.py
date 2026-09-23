# scratch: only to verify the one sentence about the preemptive variant (SRTF)
TASKS = {1:(1,10), 2:(2,4), 3:(3,1), 4:(4,6)}
left = {i: TASKS[i][1] for i in TASKS}
tl = []
for t in range(40):
    ready = [i for i in TASKS if TASKS[i][0] <= t and left[i] > 0]
    if not ready:
        tl.append(None); continue
    cur = min(ready, key=lambda i: (left[i], i))
    left[cur] -= 1
    tl.append(cur)
    if all(v == 0 for v in left.values()):
        break
print("SRTF:", " ".join("--" if w is None else f"T{w}" for w in tl))
