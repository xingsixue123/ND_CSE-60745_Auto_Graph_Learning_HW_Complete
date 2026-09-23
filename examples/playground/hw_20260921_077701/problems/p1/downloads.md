# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- (nothing installed)

Everything used was already on the machine: `python3` (conda base) for the simulator,
`~/miniconda3/envs/py311/bin/python` (matplotlib 3.10.8) for the figures, and TinyTeX
for the test compile. Matplotlib's cache was pointed at `./.mplcache` inside this
playground via `MPLCONFIGDIR` because `~/.config/matplotlib` is read-only; that is a
cache directory, not an install, and it can simply be deleted with the playground.

