# Downloads and installs for this problem

One line per item: `- <name> | <how> | <path> | <why>`
If you install nothing, write `- (nothing installed)`.

- GraphGPS paper (arXiv:2205.12454) | `curl -sL -o refs/graphgps_2205.12454.pdf https://arxiv.org/pdf/2205.12454` | `refs/graphgps_2205.12454.pdf` | to quote the GPS layer equations (6)-(11) and the "preventing early smoothing" argument accurately (rule R9)
- ZINC subset + LastFM CSVs (copy, not a download) | `cp -r ../../shared/data .` | `data/` (384 MB) | `gt_framework.py` loads them at import time with relative paths
- gt_framework.py (copy, not a download) | `cp ../../shared/gt_framework.py .` | `gt_framework.py` | the notebook's framework code, unmodified
