# Downloads and installs for job hw_20260907_f8533b

**None.** Nothing was downloaded, cloned, pip-installed or otherwise fetched during this
run, so there is nothing here for the cleanup pass to remove outside the playground.

Everything needed was already on the machine: TinyTeX supplied every LaTeX package the
four workers asked for (lmodern, amsmath, amssymb, booktabs, float, enumitem), and the
conda base `python3` supplied PIL (figure-crop checks during ingest), sympy and
`fractions` (independent verification of the Problem 3 and Problem 4 arithmetic). No venv
was created and the network was not used.

Scratch directories created inside the playground, all safe to delete:

- `build/`  | latexmk working copy of the final document, plus its .aux/.log/.fls/.pdf |
  kept out of OUTPUT deliberately so no build artefact could ever land in `final/`
- `crops/`  | 2x-LANCZOS upscaled crops of rendered pages 1 and 5 | used to read numeric
  constants that the Read tool's downscaling of the full page render had made unreliable
