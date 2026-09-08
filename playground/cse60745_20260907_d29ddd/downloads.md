# Downloads and installs for this run (master level)

One line per item: `- <name> | <how> | <path> | <why>`

- (nothing installed)

No package was downloaded, pip-installed, cloned or otherwise fetched at the
master level, and no venv was created. Everything needed was already present on
the machine:

- `python3` (conda base) — networkx 3.6.1, numpy, PIL. Used to read the Q1 figure
  and to independently re-verify every worker's numbers.
- `/home/xing/miniconda3/envs/py311/bin/python` — networkx 3.3, scipy 1.16.3,
  matplotlib. Used for my own independent Q5 reference computation.
- `soffice`, `pdftoppm`, `pdfinfo`, `latexmk`/`pdflatex` — all pre-installed.

All three workers also reported `(nothing installed)` in their own
`problems/<pid>/downloads.md`.

Scratch produced inside the PLAYGROUND (working files, not installs):
- `scratch/` | figure-analysis scripts, upscaled figure crops, `*.npy` masks,
  `q5_check.py` (my independent Q5 reference), rendered page PNGs of the final PDF
- `scratch/doc2pdf/` + `scratch/.loprofile/` | my own LibreOffice re-conversion of
  the source `.doc`, used to confirm the assignment really is 3 pages despite its
  "Page 1 of 4" footer
- `logs/` | master log, per-spawn logs, LaTeX compile log
