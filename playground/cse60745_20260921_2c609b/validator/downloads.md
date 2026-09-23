# Downloads / installs — master validator, job cse60745_20260921_2c609b

All inside VALIDATOR_DIR (`playground/cse60745_20260921_2c609b/validator/`).

- python venv | `python3 -m venv .venv` | `validator/.venv` | host for the packages below
- torch (CPU wheel) | `PIP_CACHE_DIR=$PWD/.pipcache .venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu` | `validator/.venv` | dependency of torch_geometric
- torch_geometric | `PIP_CACHE_DIR=$PWD/.pipcache .venv/bin/pip install torch_geometric` | `validator/.venv` | load Planetoid/WebKB/WikipediaNetwork/Actor/Coauthor/Amazon/PPI to recompute the answer's Table 1 statistics
- scipy | `PIP_CACHE_DIR=$PWD/.pipcache .venv/bin/pip install scipy` | `validator/.venv` | required by torch_geometric to read the Planetoid/Coauthor/Amazon .npz files
- pip cache | side effect of the above | `validator/.pipcache` | `~/.cache/pip` is read-only
- benchmark datasets (Cora, CiteSeer, PubMed, WebKB, Chameleon, Squirrel, Actor, Coauthor CS/Physics, Amazon Computers/Photo, PPI) | auto-downloaded by torch_geometric loaders | `validator/data/` | ground truth for recomputing the submitted statistics
- LibreOffice profile + re-converted assignment PDF | `soffice --convert-to pdf` | `validator/recheck/` | independent re-conversion of the input .doc to check the page count against ingest
- rebuilt document + rendered pages | `latexmk`, `framework/tools/pdf_pages.py` | `validator/build/`, `validator/finalpages/`, `validator/zoom_*.png` | recompile the submission and read the PDF through both channels
