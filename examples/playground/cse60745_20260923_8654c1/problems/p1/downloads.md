# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- (nothing installed) | used only the pre-existing shared venv `playground/cse60745_20260923_8654c1/venv` and the pre-fetched dataset `playground/cse60745_20260923_8654c1/data`, both already recorded in the job-level `downloads.md` | — | no new package or download was needed
- data symlink | `ln -s ../../data data` | `problems/p1/data` -> `playground/cse60745_20260923_8654c1/data` | the notebook scaffolding hard-codes `Path("data/task1/...")`; read-only symlink, nothing written there

