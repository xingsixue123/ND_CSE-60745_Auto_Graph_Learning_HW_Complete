#!/usr/bin/env python3
"""Enforce rule R4: an OUTPUT dir is a clean deliverable, not a workspace.

    python3 lint_output.py <OUTPUT_DIR> [--worker | --final]

Exits 0 if clean, 1 with a list of offenders otherwise.
"""
import argparse
import re
import sys
from pathlib import Path

WORKER_ALLOWED = [
    re.compile(r"^answer\.tex$"),
    re.compile(r"^preamble\.txt$"),
    re.compile(r"^fig_[A-Za-z0-9_]+\.pdf$"),
    re.compile(r"^assets/.+$"),
]
FINAL_ALLOWED = [
    re.compile(r"^main\.tex$"),
    re.compile(r"^main\.pdf$"),
    re.compile(r"^preamble\.tex$"),
    re.compile(r"^p[0-9A-Za-z_]+\.tex$"),
    re.compile(r"^fig_[A-Za-z0-9_]+\.pdf$"),
    re.compile(r"^assets/.+$"),
]
FORBIDDEN_HINT = {
    ".aux": "LaTeX build artefact", ".log": "build/run log", ".out": "LaTeX artefact",
    ".fls": "latexmk artefact", ".fdb_latexmk": "latexmk artefact",
    ".synctex.gz": "LaTeX artefact", ".py": "code belongs in PLAYGROUND",
    ".ipynb": "notebook belongs in PLAYGROUND", ".csv": "intermediate data",
    ".json": "intermediate data", ".png": "use a PDF figure instead",
    ".txt": "only preamble.txt is allowed here",
}


def lint(outdir: Path, allowed) -> list[str]:
    problems = []
    if not outdir.is_dir():
        return [f"{outdir} does not exist"]
    for path in sorted(outdir.rglob("*")):
        if path.is_dir():
            if path.name not in ("assets",) and not str(path.relative_to(outdir)).startswith("assets/"):
                problems.append(f"unexpected directory: {path.relative_to(outdir)}/")
            continue
        rel = str(path.relative_to(outdir))
        if any(rx.match(rel) for rx in allowed):
            continue
        hint = FORBIDDEN_HINT.get(path.suffix, "not an allowed deliverable")
        problems.append(f"{rel}  ({hint})")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--worker", action="store_true", default=True)
    g.add_argument("--final", action="store_true")
    a = ap.parse_args()

    outdir = Path(a.outdir)
    allowed = FINAL_ALLOWED if a.final else WORKER_ALLOWED
    problems = lint(outdir, allowed)

    required = "main.tex" if a.final else "answer.tex"
    if not (outdir / required).is_file():
        problems.insert(0, f"MISSING REQUIRED FILE: {required}")

    if problems:
        print(f"OUTPUT LINT FAILED ({len(problems)} problem(s)) in {outdir}:")
        for p in problems:
            print(f"  - {p}")
        print("\nMove intermediates into your PLAYGROUND. See rules.md R4.")
        sys.exit(1)
    print(f"OUTPUT LINT OK: {outdir}")


if __name__ == "__main__":
    main()
