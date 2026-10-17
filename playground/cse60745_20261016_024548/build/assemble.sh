#!/bin/bash
# Assemble output/<job>/final from the workers' fragments, compile, lint.
# Builds in PLAYGROUND/build/compile so no .aux/.log ever lands in OUTPUT (rule R4).
set -euo pipefail
JOB=cse60745_20261016_024548
PG=/home/xing/project/auto_hw_complete/playground/$JOB
OUT=/home/xing/project/auto_hw_complete/output/$JOB
FINAL=$OUT/final
WORK=$PG/build/compile
PIDS="${*:-p1 p2}"

rm -rf "$WORK"; mkdir -p "$WORK" "$FINAL"

# fragments + figures
for p in $PIDS; do
    cp "$OUT/$p/answer.tex" "$WORK/$p.tex"
    shopt -s nullglob
    for f in "$OUT/$p"/fig_*.pdf; do cp "$f" "$WORK/"; done
    if [ -d "$OUT/$p/assets" ]; then mkdir -p "$WORK/assets"; cp -r "$OUT/$p/assets/." "$WORK/assets/"; fi
    shopt -u nullglob
done

# merged, de-duplicated preamble: master's own packages first, then the workers'
{
  echo "% packages required by the master's cover page and page furniture"
  printf '%s\n' \
    '\usepackage{lmodern}' \
    '\usepackage[T1]{fontenc}' \
    '\usepackage[utf8]{inputenc}' \
    '\usepackage[margin=1in]{geometry}' \
    '\usepackage{array}' \
    '\usepackage{fancyhdr}'
  echo "% packages requested by the workers (preamble.txt), de-duplicated"
  for p in $PIDS; do
      [ -f "$OUT/$p/preamble.txt" ] && cat "$OUT/$p/preamble.txt"
  done
  # hyperref last: loaded before float it duplicates every [H] float's PDF anchor
  echo "% hyperref last, as it must be"
  echo '\usepackage{hyperref}'
} | awk '/^%/ {print; next} NF==0 {next} !seen[$0]++' > "$WORK/preamble.tex"

{
  echo '\documentclass[11pt,a4paper]{article}'
  echo '\input{preamble.tex}'
  cat <<'TEX'
\pagestyle{fancy}
\fancyhf{}
\lhead{\small CSE 60745 (Fall 2026) -- HW3-Part(B)}
\rhead{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setcounter{secnumdepth}{0}   % the questions are already named Q1/Q2/Q3
\setlength{\parskip}{0.4em}
\setlength{\parindent}{0pt}
\hypersetup{hidelinks}
\begin{document}
TEX
  cat "$PG/build/cover.tex"
  for p in $PIDS; do echo "\\input{$p.tex}"; done
  echo '\end{document}'
} > "$WORK/main.tex"

cd "$WORK"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > latexmk.log 2>&1 || {
    echo "COMPILE FAILED -- tail of main.log:"; tail -40 main.log; exit 1; }

# ship only what R4 allows
rm -f "$FINAL"/*.tex "$FINAL"/*.pdf
cp "$WORK/main.tex" "$WORK/preamble.tex" "$WORK/main.pdf" "$FINAL/"
for p in $PIDS; do cp "$WORK/$p.tex" "$FINAL/"; done
shopt -s nullglob
for f in "$WORK"/fig_*.pdf; do cp "$f" "$FINAL/"; done
[ -d "$WORK/assets" ] && { mkdir -p "$FINAL/assets"; cp -r "$WORK/assets/." "$FINAL/assets/"; }
shopt -u nullglob

echo "pages: $(pdfinfo "$FINAL/main.pdf" | awk '/^Pages/{print $2}')"
grep -c "Overfull" "$WORK/main.log" || true
python3 /home/xing/project/auto_hw_complete/framework/tools/lint_output.py "$FINAL" --final
