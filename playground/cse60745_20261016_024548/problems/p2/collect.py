"""Aggregate every '### result' line in logs/ into the table that goes in answer.tex."""
import re, glob, statistics as st

rows = {}
for f in sorted(glob.glob("logs/*.log")):
    for line in open(f):
        m = re.match(r"### result (\S+) seed=(\d+) epochs=(\d+) val=([\d.]+) test=([\d.]+) "
                     r"epoch=(\d+) params=(\d+)", line)
        if m:
            name, seed, ep, val, test, be, pr = m.groups()
            rows.setdefault((name, int(ep)), []).append(
                dict(seed=int(seed), val=float(val), test=float(test),
                     best_epoch=int(be), params=int(pr)))

ORDER = ["baseline-plain", "baseline-demo", "global-only", "local-only",
         "sequential", "gated", "hybrid"]
for epochs in sorted({e for _, e in rows}):
    print(f"\n=== {epochs} epochs ===")
    print(f"{'experiment':16} {'n':>2} {'val mean':>9} {'val sd':>7} {'test mean':>10} "
          f"{'test sd':>8} {'test min':>9} {'test max':>9} {'best ep':>8} {'params':>8}")
    for name in ORDER:
        rs = rows.get((name, epochs))
        if not rs:
            continue
        rs.sort(key=lambda r: r["seed"])
        v = [r["val"] for r in rs]
        t = [r["test"] for r in rs]
        sd = (lambda a: st.stdev(a) if len(a) > 1 else 0.0)
        print(f"{name:16} {len(rs):2d} {st.mean(v):9.4f} {sd(v):7.4f} {st.mean(t):10.4f} "
              f"{sd(t):8.4f} {min(t):9.4f} {max(t):9.4f} "
              f"{','.join(str(r['best_epoch']) for r in rs):>8} {rs[0]['params']:8d}")
        print(f"{'':16}    seeds " + "  ".join(f"s{r['seed']}: {r['val']:.4f}/{r['test']:.4f}" for r in rs))
