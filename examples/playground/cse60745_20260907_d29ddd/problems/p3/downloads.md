# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- (nothing installed)

No venv, no pip, no downloads were needed. Everything was computed with
interpreters already present on the machine:

- `/home/xing/miniconda3/envs/py311/bin/python` — networkx 3.3 + scipy 1.16.3 +
  numpy 2.2.6. Used for everything that needs scipy
  (`eigenvector_centrality_numpy`, `katz_centrality_numpy`, `eigsh`, `spsolve`).
- `python3` (conda base) — networkx 3.6.1 + numpy 2.5.2, no scipy. Used only to
  re-run the pure-Python calls as a networkx-version cross-check.

The problem brief suggested a venv might be necessary because base python3 lacks
scipy; it turned out py311 already has networkx as well, so no install was
required.
