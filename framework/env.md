# Machine capability sheet  (verified 2026-09-07 — trust this over your priors)

You are on a Linux box (Debian, kernel 6.1) with **no root**. Everything below was
tested by hand on this exact machine. If something here contradicts what you expect,
this file is right.

## LaTeX — WORKS

TinyTeX / TeX Live 2026 on PATH: `pdflatex`, `xelatex`, `lualatex`, `latexmk`, `tlmgr`.

Verified compiling: `pdflatex`, `latexmk -pdf`, `xelatex` with `ctex` (Chinese), and
`\includegraphics` of a matplotlib-produced `.pdf`.

Installed and available: amsmath, amssymb, amsthm, graphicx, geometry, booktabs,
listings, hyperref, xcolor, float, enumitem, siunitx, tikz, pgfplots, caption,
subcaption, algorithm, algorithmicx (algpseudocode), algorithm2e, bm, physics,
mathtools, standalone, adjustbox, wrapfig, multirow, fancyhdr, titlesec, microtype,
ulem, cancel, tcolorbox, longtable, threeparttable, soul, framed, fvextra,
ctex + xeCJK + fandol (Chinese).

**`tlmgr install` DOES NOT WORK from inside the sandbox** — `~/.TinyTeX` is mounted
read-only. If you need a package that is not in the list above, do not try to install
it. Rewrite the LaTeX to use what is available, and record the substitution in your
notes. Prefer the packages listed above; they cover essentially all homework needs.

Chinese text requires `xelatex` (not `pdflatex`) plus `\usepackage[UTF8]{ctex}`.
`\mathbb` etc. still need `\usepackage{amssymb}` — ctex does not pull it in.

## Reading a PDF — THREE channels, and the trap in each

`poppler` is installed (`pdftoppm`, `pdftotext`, `pdfinfo` on PATH, wrapped for their
conda libraries), so the **Read tool works directly on a `.pdf`** with a `pages`
argument. `pymupdf` is also available (`import pymupdf`). ImageMagick is still
MISSING — do not call `convert`.

`framework/tools/pdf_pages.py` pre-renders everything into three channels:

    page_001.png          the whole page, rendered at 200 dpi
    page_001.txt          text extracted from that page
    page_001_fig_01.png   an embedded figure at its NATIVE resolution
    alltext.txt           all text, page-delimited

**Each channel fails in its own way, and the failures are not obvious:**

1. **Text** silently drops every figure. A question saying "create the following
   graph" leaves a blank gap in the text — not an error, just absence. It also
   mangles reading order in headers and tables (a date can come out as `Mon` /
   `day,` / `09/1` / `4` across four lines).
2. **The whole-page image** carries figures, but the Read tool downscales it. On a
   1241x1754 page render, 8pt node labels in a graph become unreadable — you will be
   able to see *that* there is a figure and not *what it says*. Answering from a
   downscaled page render is guessing.
3. **The extracted figure files** (`page_00N_fig_NN.*`) are the fix: each embedded
   figure written out at the resolution it was authored at. **When a question refers
   to a figure, read that file.** If a figure is still too small to read, crop and
   upscale it with PIL (4x LANCZOS) and read it again — do not squint and guess.

Cross-check across channels rather than trusting one. Worked example from this
assignment: the figure file shows node 0 joined to 1, 4 and 5; the text of the *next*
question says "remove node 1, edge (0, 4) and edge (0, 5)", which independently
confirms two of those three edges. That is what a cross-check looks like — text
corroborating an image, or contradicting it and telling you to look harder.

## Word / PowerPoint / Excel input — via LibreOffice

`soffice` is on PATH (LibreOffice 26.2.6, installed root-free in `~/local`).
Convert anything to PDF first, then read the PDF with pymupdf:

    soffice --headless --norestore -env:UserInstallation=file://$PWD/.loprofile \
            --convert-to pdf --outdir <outdir> <input.doc>

The `-env:UserInstallation` pointing at a **writable** dir is required; without it
LibreOffice tries to write a profile into `$HOME` and fails in the sandbox.

WARNING: the rendered PDF's page index does not necessarily match the page numbers
printed in the document footer (cover pages offset them). Always cite the **rendered
page index** (1-based, as produced by pdf_pages.py) when pointing at a location.

WARNING: `.doc`/`.docx` figures are embedded images. Extracting text alone silently
drops them. Always look at the page PNGs too.

WARNING: a **spreadsheet** rendered to PDF extracts column-major -- every value in
column A, then every value in column B -- so rows come apart and values get
mis-associated. `ingest.py` also exports spreadsheets to CSV (`ingest/csv/<name>.csv`);
use that, not the PDF text.

WARNING: CSV export **flattens merged cells**. A category or group label that spanned
several rows in the spreadsheet appears only on the first of them, and the rest are
blank. A blank cell under a filled one usually means the value above spans down --
so counting rows whose cell literally contains a label will undercount the group,
often badly. Check whether the blanks form a contiguous run, and cross-check against
any other column that encodes the grouping (an ID prefix, a numbering scheme).

## Python

- `python3` = conda base 3.12: has numpy, sympy, torch, pymupdf, PIL, networkx.
  **No matplotlib, no scipy, no pandas, no sklearn.**
- `~/miniconda3/envs/py311/bin/python` has matplotlib 3.10.8, numpy, scipy,
  pandas. Use it for plotting if you do not want to build your own venv. If that
  path does not exist, find an equivalent with `conda env list` and check it with
  `<python> -c "import matplotlib, scipy, pandas"` before relying on it -- do not
  assume this line is still true of the machine you are on.
- `conda create` and `conda install` DO NOT WORK (read-only `~/miniconda3`).
- `pip install` into the base env DOES NOT WORK. Make your own venv inside your
  playground instead:

      python3 -m venv .venv
      PIP_CACHE_DIR=$PWD/.pipcache ./.venv/bin/pip install <pkgs>

  `~/.cache/pip` is read-only, hence `PIP_CACHE_DIR`.

## Network — unrestricted

Full outbound internet. `pip`, `curl`, `wget`, `git clone`, WebSearch, WebFetch all
work. You may download anything you need.

## Other tools present

`git`, `curl`, `wget`, `tar`, `xz`, `gs` (ghostscript), `java` 21, `bwrap`, `socat`,
`soffice`, `pdftoppm`, `pdftotext`, `pdfinfo`.
MISSING: docker, podman, imagemagick, pandoc, antiword.
