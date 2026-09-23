#!/usr/bin/env python3
"""Simulator for Ex 2.1: RR(q=1), FIFO, SJF (non-preemptive) on
T1(1,10) T2(2,4) T3(3,1) T4(4,6).

Conventions (see notes.md):
  * discrete time, the CPU decides what to run at each integer instant t and runs
    that task over the slice [t, t+1);
  * a task with arrival time a is runnable at instant a;
  * FIFO / SJF are non-preemptive; SJF picks the smallest *total* execution time
    among arrived-and-unfinished tasks, ties broken by smaller index;
  * RR with q = 1: at an instant where a task arrives *and* the running task is
    preempted, the arriving task is enqueued first and the preempted task then
    goes to the tail.  Simultaneous arrivals enter in index order.
"""
import json

TASKS = {1: (1, 10), 2: (2, 4), 3: (3, 1), 4: (4, 6)}   # id -> (arrival, exec)
HORIZON = 100


def _stats(timeline):
    """timeline[t] is the task id running over [t, t+1), or None for idle."""
    comp, res = {}, {}
    for t, who in enumerate(timeline):
        if who is not None:
            comp[who] = t + 1
    for i, (a, e) in TASKS.items():
        turn = comp[i] - a
        res[i] = dict(arrival=a, burst=e, completion=comp[i],
                      turnaround=turn, waiting=turn - e)
    return res


def fifo():
    timeline = []
    remaining = dict(TASKS)
    done = set()
    t = 0
    while len(done) < len(TASKS):
        ready = sorted(i for i in TASKS
                       if i not in done and TASKS[i][0] <= t)
        if not ready:
            timeline.append(None)
            t += 1
            continue
        # arrival order, tie -> smaller index (sorted key does both)
        pick = min(ready, key=lambda i: (TASKS[i][0], i))
        for _ in range(TASKS[pick][1]):          # non-preemptive: run to completion
            timeline.append(pick)
            t += 1
        done.add(pick)
    return timeline


def sjf():
    timeline = []
    done = set()
    t = 0
    while len(done) < len(TASKS):
        ready = [i for i in TASKS if i not in done and TASKS[i][0] <= t]
        if not ready:
            timeline.append(None)
            t += 1
            continue
        pick = min(ready, key=lambda i: (TASKS[i][1], i))   # shortest total burst
        for _ in range(TASKS[pick][1]):
            timeline.append(pick)
            t += 1
        done.add(pick)
    return timeline


def rr(q=1):
    timeline = []
    left = {i: TASKS[i][1] for i in TASKS}
    queue = []
    running = None
    for t in range(HORIZON):
        # 1. tasks arriving at instant t are enqueued first ...
        for i in sorted(TASKS, key=lambda i: (TASKS[i][0], i)):
            if TASKS[i][0] == t:
                queue.append(i)
        # 2. ... then the task preempted at the end of the previous quantum
        if running is not None:
            queue.append(running)
            running = None
        if not queue:
            timeline.append(None)
            continue
        cur = queue.pop(0)
        for _ in range(q):
            timeline.append(cur)
            left[cur] -= 1
        if left[cur] > 0:
            running = cur          # goes to the tail at the next instant
        if all(v == 0 for v in left.values()):
            break
    return timeline


def check(name, timeline):
    assert timeline[0] is None, f"{name}: t=0 must be idle"
    assert timeline.count(None) == 1, f"{name}: expected exactly one idle unit"
    assert len(timeline) == 22, f"{name}: makespan {len(timeline)} != 22"
    for i, (a, e) in TASKS.items():
        assert timeline.count(i) == e, f"{name}: T{i} got {timeline.count(i)} != {e}"
        first = timeline.index(i)
        assert first >= a, f"{name}: T{i} ran before it arrived"


def compress(timeline):
    """[(who, start, end), ...] for the Gantt chart."""
    out = []
    for t, who in enumerate(timeline):
        if out and out[-1][0] == who and out[-1][2] == t:
            out[-1][2] = t + 1
        else:
            out.append([who, t, t + 1])
    return [tuple(b) for b in out]


def main():
    dump = {}
    for name, fn in (("RR", rr), ("FIFO", fifo), ("SJF", sjf)):
        tl = fn()
        check(name, tl)
        st = _stats(tl)
        blocks = compress(tl)
        dump[name] = dict(timeline=tl, blocks=blocks, stats=st)

        print(f"=== {name} ===")
        print("  t :", " ".join(f"{t:>2}" for t in range(len(tl))))
        print("  r :", " ".join(("--" if w is None else f"T{w}") for w in tl))
        print("  blocks:", ", ".join(
            ("idle" if w is None else f"T{w}") + f"[{s},{e})" for w, s, e in blocks))
        print(f"  {'task':<5}{'arr':>4}{'burst':>7}{'compl':>7}{'turn':>7}{'wait':>7}")
        for i in sorted(st):
            d = st[i]
            print(f"  T{i:<4}{d['arrival']:>4}{d['burst']:>7}{d['completion']:>7}"
                  f"{d['turnaround']:>7}{d['waiting']:>7}")
        n = len(TASKS)
        print(f"  avg turnaround = {sum(d['turnaround'] for d in st.values())}/{n}"
              f" = {sum(d['turnaround'] for d in st.values())/n:.2f}")
        print(f"  avg waiting    = {sum(d['waiting'] for d in st.values())}/{n}"
              f" = {sum(d['waiting'] for d in st.values())/n:.2f}")
        print()

    with open("schedules.json", "w") as f:
        json.dump(dump, f, indent=1)
    print("wrote schedules.json")


if __name__ == "__main__":
    main()
