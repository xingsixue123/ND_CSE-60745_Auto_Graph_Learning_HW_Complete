## Results

Every value below is in `answer.tex`. `PY = ../../.venv-gt/bin/python`, run from PLAYGROUND.

### Table 1 — ZINC, 30 epochs, dense attention (`PY run_zinc_q1.py` -> `logs/zinc_q1.log`)

| row | val MAE | test MAE | best epoch |
|---|---|---|---|
| none: plain attention | 0.6472 | 0.7013 | 18 |
| demo: centrality + CN | 0.4629 | 0.4957 | 27 |
| LapPE only | 0.6205 | 0.6575 | 30 |
| SPD only | 0.5373 | 0.5614 | 29 |
| LapPE + SPD (cell 14) | 0.5160 | 0.5496 | 30 |

### Table 2 — ZINC masking strategies (`PY run_zinc_q2.py` -> `logs/zinc_q2.log`; seeds 1 and 2 from `PY run_seeds.py <s>` -> `logs/zinc_seed{1,2}.log`; pair counts from `logs/zinc_pair_counts.json`)

| strategy | pairs/graph | % of n² | val MAE | test MAE | test, seed 1 | test, seed 2 | 3-seed mean ± half-range |
|---|---|---|---|---|---|---|---|
| local | 73.0 | 13.1 | 0.4918 | 0.5048 | 0.5313 | 0.5073 | 0.5145 ± 0.0133 |
| local+virtual | 120.4 | 21.6 | 0.4791 | 0.5047 | 0.5049 | 0.5181 | 0.5092 ± 0.0067 |
| 2-hop ball+virtual **(submitted)** | 189.2 | 34.0 | 0.4293 | 0.4677 | 0.4951 | 0.5098 | 0.4909 ± 0.0211 |
| local+expander+virtual | 200.2 | 35.9 | 0.5179 | 0.5551 | 0.5810 | 0.5761 | 0.5708 ± 0.0129 |
| local+expander8+virtual | 266.4 | 47.8 | 0.5213 | 0.5554 | 0.5792 | 0.5620 | 0.5655 ± 0.0119 |
| full attention | 556.8 | 100.0 | 0.5160 | 0.5496 | 0.5651 | 0.5696 | 0.5614 ± 0.0100 |

### Table 3 — LastFM (`PY run_timing2.py` -> `logs/lastfm_timing2.log` for pairs and seconds, 8 threads, best of 7 steps; `PY run_lastfm_final.py` -> `logs/lastfm_final.log` for micro-F1)

| strategy | pairs attended | one step (s) | val micro-F1 | test micro-F1 |
|---|---|---|---|---|
| full: LapPE + SPD | 58,125,376 | 5.23 | not trained | not trained |
| local | 63,236 | 0.03 | 0.8152 | 0.7893 |
| local+virtual | 78,485 | 0.04 | 0.8073 | 0.7826 |
| 2-hop ball+virtual **(submitted)** | 804,349 | 0.33 | 0.8100 | 0.7827 |
| local+expander+virtual | 108,965 | 0.05 | 0.7929 | 0.7678 |
| local+expander8+virtual | 139,417 | 0.06 | 0.7733 | 0.7607 |

### Ablations quoted in the Q1 prose

| ablation | dataset | metric | value | reference | source |
|---|---|---|---|---|---|
| no sqrt(n) scaling | ZINC | test MAE | 0.5449 | 0.5496 | `run_ablation.py` -> `logs/zinc_ablation.log` |
| no sign flip | ZINC | test MAE | 0.5999 | 0.5496 | `run_ablation.py` -> `logs/zinc_ablation.log` |
| no sqrt(n) scaling | LastFM | test micro-F1 | 0.7319 | 0.7827 | `run_lastfm_final.py` -> `logs/lastfm_final.log` |
| sign flip forced on | LastFM | test micro-F1 | 0.6546 | 0.7827 | `run_lastfm_final.py` -> `logs/lastfm_final.log` |

### Other numbers in the text

- sparse attention reproduces dense attention on a complete pair set to **7.45e-08** (`test_solution.py` check 5, `logs/test_solution.log`).
- cell 18 against the final code, three identical repeats at 8 threads (`run_cell18.py` -> `logs/zinc_cell18.log`): val 0.4318, 0.4418, 0.4418; test 0.4715, 0.4766, 0.4766. Reference row measured before the rename and the sign-flip change: 0.4293 / 0.4677. The spread across identical repeats (0.0051 on test) is run-to-run non-determinism in `index_add_`, not a change in the model.
- ZINC: 12000 graphs, n from 9 to 37, every graph one connected component; LastFM: one component, unscaled LapPE channel RMS 0.01145 = 1/sqrt(7624) (`verify_facts.py` -> `logs/verify_facts.log`).
- LastFM SPD histogram (0..8 hops, none unreachable) is in `logs/lastfm.log`.
