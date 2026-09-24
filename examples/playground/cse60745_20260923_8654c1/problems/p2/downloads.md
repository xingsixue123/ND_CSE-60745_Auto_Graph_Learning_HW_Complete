# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- (nothing installed)

Nothing was downloaded and no package was installed for p2. Everything used here was
already present and is recorded in the job-level
`playground/cse60745_20260923_8654c1/downloads.md`:

- shared venv | installed by the job setup (gensim 4.4.0, numpy, scipy, pandas, scikit-learn, networkx, matplotlib) | `playground/cse60745_20260923_8654c1/venv` | interpreter for every script here
- LastFM-Asia task data | downloaded by the job setup | `playground/cse60745_20260923_8654c1/data`, reached via the symlink `problems/p2/data` | `task3/hetero_stats.json` and `task3/user_artist.csv.gz` are the Task-4 inputs
- p1's finished code | `cp` from the read-only `problems/p1/`, not a download | `problems/p2/scaffold.py`, `problems/p2/impl.py` | reused byte-identically (sha256 verified) so the Task 3 / Task 4 comparison is valid

Local scratch dirs created here, no network involved: `.mplcache` (MPLCONFIGDIR),
`tex_test/` (LaTeX compile check), `__pycache__/`.
