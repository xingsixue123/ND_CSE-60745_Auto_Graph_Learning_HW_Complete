#!/usr/bin/env python3
"""Cross-problem checks that no single worker validator can perform.

Each worker validator sees exactly one problem's brief, so it is structurally blind
to anything that spans problems: a label defined in two fragments, two workers
reporting slightly different values for the same quantity, a figure referenced but
delivered to the wrong directory.  Those are the defects that survive every per-problem
audit and then break the master's compile or contradict each other in the final PDF.

It is also an *uncorrelated* check.  A worker and its validator share the same
`context_worker.md`, so they can make the same mistake together.  This script is
mechanical and shares nothing with them.

    python3 crosscheck.py [<job_id>]

Exits non-zero if any blocking problem is found.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PLAYGROUND, OUTPUT = ROOT / "playground", ROOT / "output"

FORBIDDEN = [r"\\documentclass", r"\\usepackage", r"\\begin\{document\}",
             r"\\end\{document\}"]


def latest_job() -> str:
    jobs = sorted((p for p in PLAYGROUND.iterdir()
                   if p.is_dir() and (p / "state.json").is_file()),
                  key=lambda p: p.stat().st_mtime)
    if not jobs:
        sys.exit("no job found")
    return jobs[-1].name


def norm_num(s: str) -> str:
    """LaTeX writes 26{,}728 and 26,728 for the same number."""
    return re.sub(r"[{},\s]", "", s)


def main():
    jid = sys.argv[1] if len(sys.argv) > 1 else latest_job()
    job, out = PLAYGROUND / jid, OUTPUT / jid
    print(f"cross-check: {jid}\n")
    blocking, warnings = [], []

    pj = job / "problems.json"
    problems = json.loads(pj.read_text())["problems"] if pj.is_file() else []
    pids = [p["id"] for p in problems] or [d.name for d in sorted(out.iterdir())
                                           if d.is_dir() and d.name != "final"]
    # A problem still running has no deliverable yet -- that is not a defect.
    state = json.loads((job / "state.json").read_text())
    status = {k: v["status"] for k, v in state.get("problems", {}).items()}
    pending = [p for p in pids if status.get(p) not in ("done", None)
               or not (out / p / "answer.tex").is_file() and status.get(p) != "done"]
    pending = [p for p in pids if status.get(p) != "done"]
    if pending:
        print(f"skipping {', '.join(pending)} -- not finished "
              f"({', '.join(status.get(p, 'not started') for p in pending)})\n")
    pids = [p for p in pids if p not in pending]

    # ---------- points coverage ----------
    if problems:
        total = sum(p.get("points", 0) for p in problems)
        print(f"points declared across {len(problems)} problem(s): {total}")
        if total != 100:
            warnings.append(f"points sum to {total}, not 100 -- confirm against the "
                            "assignment's stated total")

    # ---------- per-problem fragment checks ----------
    labels = defaultdict(list)      # label -> [pid, ...]
    numbers = defaultdict(set)      # pid -> {normalized numbers}
    preamble = defaultdict(list)    # line -> [pid, ...]

    for pid in pids:
        tex = out / pid / "answer.tex"
        if not tex.is_file():
            blocking.append(f"{pid}: no answer.tex in {out/pid}")
            continue
        body = tex.read_text()

        for pat in FORBIDDEN:
            if re.search(pat, body):
                blocking.append(f"{pid}: answer.tex contains {pat} "
                                "-- it is a fragment (rule R5)")

        for m in re.finditer(r"\\label\{([^}]+)\}", body):
            labels[m.group(1)].append(pid)
            if not m.group(1).startswith(pid + ":"):
                blocking.append(f"{pid}: label '{m.group(1)}' is not namespaced "
                                f"'{pid}:...' (rule R5) -- will collide on assembly")

        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", body):
            fig = m.group(1)
            if fig.startswith("/"):
                blocking.append(f"{pid}: figure referenced by absolute path: {fig}")
            elif not (out / pid / fig).is_file():
                blocking.append(f"{pid}: references {fig}, missing from {out/pid}")

        for m in re.finditer(r"\b\d{1,3}(?:\{,\}|,)?\d{3,}\b|\b\d{4,}\b", body):
            numbers[pid].add(norm_num(m.group(0)))

        pre = out / pid / "preamble.txt"
        if pre.is_file():
            for line in pre.read_text().splitlines():
                if line.strip():
                    preamble[line.strip()].append(pid)

    # ---------- label collisions ----------
    dupes = {k: v for k, v in labels.items() if len(v) > 1}
    print(f"labels defined: {len(labels)}   collisions: {len(dupes)}")
    for k, v in dupes.items():
        blocking.append(f"label '{k}' defined in {', '.join(v)} -- duplicate label "
                        "breaks the final compile")

    # ---------- near-miss numbers across problems ----------
    print("\nshared quantities across problems:")
    allnums = defaultdict(list)
    for pid, ns in numbers.items():
        for n in ns:
            allnums[n].append(pid)
    shared = {n: p for n, p in allnums.items() if len(set(p)) > 1}
    for n in sorted(shared, key=lambda x: -len(x)):
        print(f"  {n:>12}  agreed by {', '.join(sorted(set(shared[n])))}")
    if not shared:
        print("  (none -- problems report disjoint quantities)")

    ints = sorted({int(n) for ns in numbers.values() for n in ns
                   if n.isdigit() and len(n) >= 4})
    for a, b in zip(ints, ints[1:]):
        if 0 < b - a <= max(2, a * 0.0005):
            pa = sorted({p for p, ns in numbers.items() if str(a) in ns})
            pb = sorted({p for p, ns in numbers.items() if str(b) in ns})
            if set(pa) != set(pb):
                warnings.append(
                    f"near-miss values {a} ({','.join(pa)}) vs {b} ({','.join(pb)}) "
                    "-- possible disagreement about the same quantity")

    # ---------- merged preamble ----------
    print(f"\nmerged preamble ({len(preamble)} distinct lines):")
    for line, who in sorted(preamble.items()):
        tag = f"  [{', '.join(sorted(set(who)))}]" if len(set(who)) > 1 else ""
        print(f"  {line}{tag}")

    # ---------- report ----------
    print()
    for w in warnings:
        print(f"WARNING: {w}")
    for b in blocking:
        print(f"BLOCKING: {b}")
    if not blocking:
        print(f"\nCROSS-CHECK OK ({len(warnings)} warning(s))")
        return 0
    print(f"\nCROSS-CHECK FAILED: {len(blocking)} blocking problem(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
