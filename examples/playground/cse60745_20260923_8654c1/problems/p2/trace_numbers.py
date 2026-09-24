"""Audit: every 4-decimal number in answer.tex must appear in a generated artefact.

    ../../venv/bin/python trace_numbers.py
"""
import re
from pathlib import Path

ANS = Path("/home/xing/project/auto_hw_complete/output/cse60745_20260923_8654c1/p2/answer.tex").read_text()
SRC = "\n".join(Path(p).read_text() for p in
                ("tables.tex", "run_hetero.log", "control_budget.log", "results_hetero.csv"))

nums = sorted(set(re.findall(r"\d\.\d{4}", ANS)))
missing = [n for n in nums if n not in SRC]
print(f"{len(nums)} distinct 4-dp numbers in answer.tex; {len(nums)-len(missing)} traceable")
if missing:
    print("NOT found verbatim in an artefact (check each by hand):")
    for n in missing:
        ctx = re.search(r".{70}" + re.escape(n) + r".{40}", ANS, re.S)
        print(f"  {n}   ...{' '.join(ctx.group().split()) if ctx else ''}...")
