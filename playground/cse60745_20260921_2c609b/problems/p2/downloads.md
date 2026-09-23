# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- HGB node-classification data (DBLP, IMDB, ACM, Freebase) | downloaded as zips from the Google Drive IDs declared in PyG's `hgb_dataset.py`, by a research subagent | `/tmp/hgbdata/` (389 MB) | the HGB paper publishes only dataset *totals*, never a per-node-type breakdown; the breakdown in the answer's statistics table was derived from these files and checked against the published totals by `verify_hgb.py`

**Rule R3 note / deviation.** The 389 MB HGB download landed in `/tmp/hgbdata/`, i.e. **outside
this PLAYGROUND**, because a background research subagent fetched it there before I could direct
it. I am recording it here rather than silently leaving it. I did not relocate it (size) and did
not delete it (it is not mine to destroy, and `/tmp` is the system scratch that gets cleaned
anyway). To keep the derivation reproducible without the bulk data I copied the four small
schema files into `hgb_info/` inside the playground, and `hgb_verify_output.txt` holds the full
recomputation. If the 389 MB must be cleaned up, `rm -rf /tmp/hgbdata` is the whole of it.

No other installs. No Python venv was created; no `pip`/`tlmgr` install was performed. All LaTeX
packages used (`tikz`, `booktabs`, `amsmath`, `amssymb`, `array`, `multirow`) were already
present in the system TinyTeX. Other research was read-only web fetching (arXiv, OGB docs, DBLP).

**Session 2 update (resume session).** Nothing new was downloaded or installed. `/tmp/hgbdata`
**no longer exists** — it was cleaned up between sessions, so the R3 deviation noted above is
already resolved and there is nothing left to remove. The consequence is that `verify_hgb.py`
can no longer be re-run; `check_invariants.py` was added to keep the numeric claims checkable
without it. The `longtable` package listed above was never actually used and is not in
`preamble.txt`.

