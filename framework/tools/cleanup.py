#!/usr/bin/env python3
"""Remove a finished job's artifacts.

Workers install everything inside their own playground and record each install in
`downloads.md` (rule R3), so deleting the job directories reclaims it all. This script
shows you what was installed before it deletes anything.

    python3 cleanup.py --list
    python3 cleanup.py <job_id> [--yes] [--keep-output]
"""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PLAYGROUND = ROOT / "playground"
OUTPUT = ROOT / "output"


def jobs():
    return sorted(p for p in PLAYGROUND.iterdir()
                  if p.is_dir() and (p / "state.json").is_file())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--keep-output", action="store_true")
    a = ap.parse_args()

    if a.list or not a.job:
        for j in jobs():
            size = sum(f.stat().st_size for f in j.rglob("*") if f.is_file())
            print(f"{j.name:32s} {size/1e6:8.1f} MB   playground")
            o = OUTPUT / j.name
            if o.is_dir():
                osize = sum(f.stat().st_size for f in o.rglob("*") if f.is_file())
                print(f"{'':32s} {osize/1e6:8.1f} MB   output")
        return

    job = PLAYGROUND / a.job
    if not job.is_dir():
        sys.exit(f"no such job: {a.job}")

    downloads = sorted(job.rglob("downloads.md"))
    if downloads:
        print("Recorded installs for this job:\n")
        for d in downloads:
            print(f"--- {d.relative_to(job)} ---")
            print(d.read_text().strip() or "(empty)")
            print()
    else:
        print("No downloads.md found -- either nothing was installed, "
              "or a worker skipped rule R3.\n")

    targets = [job] + ([] if a.keep_output else [OUTPUT / a.job])
    targets = [t for t in targets if t.exists()]
    print("Will delete:")
    for t in targets:
        print(f"  {t}")
    if not a.yes:
        if input("\nproceed? [y/N] ").strip().lower() != "y":
            sys.exit("aborted")
    for t in targets:
        shutil.rmtree(t)
        print(f"removed {t}")


if __name__ == "__main__":
    main()
