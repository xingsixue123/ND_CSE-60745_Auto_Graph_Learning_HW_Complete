"""Emit the Results section of submission.md: every computed value in answer.tex with the
command and log file it came from."""
import json

L = []
add = L.append
S = "2-hop ball+virtual"

q1 = json.load(open("logs/zinc_q1_results.json"))
q2 = json.load(open("logs/zinc_q2_results.json"))
abl = json.load(open("logs/zinc_ablation_results.json"))
counts = json.load(open("logs/zinc_pair_counts.json"))
lf = json.load(open("logs/lastfm_final_results.json"))
rep = json.load(open("logs/zinc_cell18_results.json"))["repeats"]
seeds = {sd: json.load(open(f"logs/zinc_seed{sd}_results.json")) for sd in (1, 2)}

add("## Results\n")
add("Every value below is in `answer.tex`. `PY = ../../.venv-gt/bin/python`, run from "
    "PLAYGROUND.\n")
add("### Table 1 — ZINC, 30 epochs, dense attention (`PY run_zinc_q1.py` -> `logs/zinc_q1.log`)\n")
add("| row | val MAE | test MAE | best epoch |")
add("|---|---|---|---|")
for k in ["none: plain attention", "demo: centrality + CN", "LapPE only", "SPD only",
          "LapPE + SPD (cell 14)"]:
    r = q1[k]
    add(f"| {k} | {r['val']:.4f} | {r['test']:.4f} | {r['epoch']} |")

add("\n### Table 2 — ZINC masking strategies "
    "(`PY run_zinc_q2.py` -> `logs/zinc_q2.log`; seeds 1 and 2 from `PY run_seeds.py <s>` -> "
    "`logs/zinc_seed{1,2}.log`; pair counts from `logs/zinc_pair_counts.json`)\n")
add("| strategy | pairs/graph | % of n² | val MAE | test MAE | test, seed 1 | test, seed 2 | 3-seed mean ± half-range |")
add("|---|---|---|---|---|---|---|---|")
for k in ["local", "local+virtual", "2-hop ball+virtual", "local+expander+virtual",
          "local+expander8+virtual"]:
    r, c = q2[f"sparse: {k}"], counts[k]
    v = [r["test"]] + [seeds[sd][f"sparse: {k}"]["test"] for sd in (1, 2)]
    mark = " **(submitted)**" if k == S else ""
    add(f"| {k}{mark} | {c['pairs']:.1f} | {100 * c['pairs'] / c['full']:.1f} | {r['val']:.4f} | "
        f"{r['test']:.4f} | {v[1]:.4f} | {v[2]:.4f} | {sum(v) / 3:.4f} ± {(max(v) - min(v)) / 2:.4f} |")
r = q1["LapPE + SPD (cell 14)"]
v = [r["test"]] + [seeds[sd]["full attention"]["test"] for sd in (1, 2)]
add(f"| full attention | {counts['local']['full']:.1f} | 100.0 | {r['val']:.4f} | {r['test']:.4f} | "
    f"{v[1]:.4f} | {v[2]:.4f} | {sum(v) / 3:.4f} ± {(max(v) - min(v)) / 2:.4f} |")

add("\n### Table 3 — LastFM (`PY run_timing2.py` -> `logs/lastfm_timing2.log` for pairs and "
    "seconds, 8 threads, best of 7 steps; `PY run_lastfm_final.py` -> `logs/lastfm_final.log` "
    "for micro-F1)\n")
add("| strategy | pairs attended | one step (s) | val micro-F1 | test micro-F1 |")
add("|---|---|---|---|---|")
bench = {}
import re
for line in open("logs/lastfm_timing2.log"):
    m = re.match(r"^(\S.*?)\s{2,}pairs attended\s+([\d,]+) \| one step\s+([\d.]+)s", line)
    if m:
        bench.setdefault(m.group(1).strip(),                      # keep the best-of-7
                         (int(m.group(2).replace(",", "")), float(m.group(3))))
for key in ["full: LapPE + SPD", "sparse: local", "sparse: local+virtual",
            "sparse: 2-hop ball+virtual", "sparse: local+expander+virtual",
            "sparse: local+expander8+virtual"]:
    p_, sec = bench[key]
    name = key.replace("sparse: ", "")
    f1 = lf.get(name)
    mark = " **(submitted)**" if name == S else ""
    add(f"| {name}{mark} | {p_:,} | {sec:.2f} | "
        + (f"{f1['val']:.4f} | {f1['test']:.4f} |" if f1 else "not trained | not trained |"))

add("\n### Ablations quoted in the Q1 prose\n")
add("| ablation | dataset | metric | value | reference | source |")
add("|---|---|---|---|---|---|")
base = q1["LapPE + SPD (cell 14)"]
add(f"| no sqrt(n) scaling | ZINC | test MAE | {abl['ablation: no sqrt(n) scaling']['test']:.4f} | "
    f"{base['test']:.4f} | `run_ablation.py` -> `logs/zinc_ablation.log` |")
add(f"| no sign flip | ZINC | test MAE | {abl['ablation: no sign flip']['test']:.4f} | "
    f"{base['test']:.4f} | `run_ablation.py` -> `logs/zinc_ablation.log` |")
add(f"| no sqrt(n) scaling | LastFM | test micro-F1 | {lf['ablation: no sqrt(n) scaling']['test']:.4f} | "
    f"{lf[S]['test']:.4f} | `run_lastfm_final.py` -> `logs/lastfm_final.log` |")
add(f"| sign flip forced on | LastFM | test micro-F1 | {lf['ablation: sign flip forced on']['test']:.4f} | "
    f"{lf[S]['test']:.4f} | `run_lastfm_final.py` -> `logs/lastfm_final.log` |")

add("\n### Other numbers in the text\n")
v = [r["test"] for r in rep]
w = [r["val"] for r in rep]
q2b = json.load(open("logs/zinc_q2_results.json"))["sparse: 2-hop ball+virtual"]
add(f"- sparse attention reproduces dense attention on a complete pair set to **7.45e-08** "
    f"(`test_solution.py` check 5, `logs/test_solution.log`).")
add(f"- cell 18 against the final code, three identical repeats at 8 threads "
    f"(`run_cell18.py` -> `logs/zinc_cell18.log`): val "
    + ", ".join(f"{x:.4f}" for x in w) + "; test " + ", ".join(f"{x:.4f}" for x in v)
    + f". Reference row measured before the rename and the sign-flip change: "
      f"{q2b['val']:.4f} / {q2b['test']:.4f}. The spread across identical repeats "
      f"({max(v) - min(v):.4f} on test) is run-to-run non-determinism in `index_add_`, "
      f"not a change in the model.")
add(f"- ZINC: 12000 graphs, n from 9 to 37, every graph one connected component; LastFM: one "
    f"component, unscaled LapPE channel RMS 0.01145 = 1/sqrt(7624) "
    f"(`verify_facts.py` -> `logs/verify_facts.log`).")
add(f"- LastFM SPD histogram (0..8 hops, none unreachable) is in `logs/lastfm.log`.")

open("results_section.md", "w").write("\n".join(L) + "\n")
print("\n".join(L[:12]))
print("...\nwrote results_section.md")
