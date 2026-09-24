"""Every 0.NNNN in answer.tex must be traceable to a generated artefact."""
import re, pathlib
ans = pathlib.Path("/home/xing/project/auto_hw_complete/output/cse60745_20260923_8654c1/p1/answer.tex").read_text()
src = "\n".join(pathlib.Path(p).read_text() for p in
                ["tables.tex", "check_claims.out", "control_random.out", "run_all.log"])
nums = sorted(set(re.findall(r"0\.\d{4}", ans)))
missing = [n for n in nums if n not in src]
print(f"{len(nums)} distinct 4-dp numbers in answer.tex; {len(missing)} not found in artefacts")
for n in missing:
    ctx = [l.strip() for l in ans.splitlines() if n in l]
    print("  MISSING", n, "|", ctx[0][:110] if ctx else "")
