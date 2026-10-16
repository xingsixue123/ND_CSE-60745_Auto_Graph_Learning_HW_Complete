#!/bin/bash
# Assemble the workers' fragments into output/<job>/final/.
# Builds in PLAYGROUND (playground/.../assemble/build) so that no .aux/.log/.fls
# can ever land in FINAL_DIR (R4); only the allowed deliverables are copied across.
set -euo pipefail
JOB=hw_20261008_5ae5f8
ROOT=/home/xing/project/auto_hw_complete
OUT=$ROOT/output/$JOB
FINAL=$OUT/final
BUILD=$ROOT/playground/$JOB/assemble/build
PIDS="$*"                      # e.g. "p1 p2 p3 p4 p5", in assignment order

rm -rf "$BUILD"; mkdir -p "$BUILD"

# --- merge preambles, de-duplicated, order-preserving -----------------------
: > "$BUILD/preamble.tex"
for pid in $PIDS; do
  [ -f "$OUT/$pid/preamble.txt" ] || continue
  cat "$OUT/$pid/preamble.txt"
done | grep -E '^\s*\\(usepackage|usetikzlibrary)' | sed 's/[[:space:]]*$//' | awk '!seen[$0]++' \
     > "$BUILD/preamble.tex"

# --- copy fragments and figures --------------------------------------------
for pid in $PIDS; do
  cp "$OUT/$pid/answer.tex" "$BUILD/$pid.tex"
  shopt -s nullglob
  for f in "$OUT/$pid"/fig_*.pdf; do cp "$f" "$BUILD/"; done
  if [ -d "$OUT/$pid/assets" ]; then mkdir -p "$BUILD/assets"; cp -r "$OUT/$pid/assets/." "$BUILD/assets/"; fi
  shopt -u nullglob
done

# --- main.tex ---------------------------------------------------------------
{
  echo '\documentclass[11pt,a4paper]{article}'
  echo '\usepackage[utf8]{inputenc}'
  echo '\usepackage{lmodern}'
  echo '\usepackage[T1]{fontenc}'
  echo '\usepackage{amsmath}'
  echo '\usepackage{amssymb}'
  echo '\usepackage{graphicx}'
  echo '\usepackage[margin=1in]{geometry}'
  echo '\input{preamble.tex}'
  echo '\usepackage[hidelinks]{hyperref}'
  echo ''
  echo '\title{Operating Systems --- Homework 3}'
  echo '\date{}'
  echo ''
  echo '\begin{document}'
  echo '\maketitle'
  echo '\vspace{-3em}'
  for pid in $PIDS; do echo "\\input{$pid.tex}"; done
  echo '\end{document}'
} > "$BUILD/main.tex"

# --- compile ----------------------------------------------------------------
cd "$BUILD"
ENGINE=pdflatex
if grep -qE '\\usepackage(\[[^]]*\])?\{ctex\}|\\setCJK' preamble.tex *.tex 2>/dev/null; then
  ENGINE=xelatex
fi
echo "engine: $ENGINE"
latexmk -$( [ "$ENGINE" = xelatex ] && echo xelatex || echo pdf ) \
        -interaction=nonstopmode -halt-on-error main.tex

# --- publish only the allowed files ----------------------------------------
rm -rf "$FINAL"; mkdir -p "$FINAL"
cp "$BUILD/main.tex" "$BUILD/preamble.tex" "$BUILD/main.pdf" "$FINAL/"
for pid in $PIDS; do cp "$BUILD/$pid.tex" "$FINAL/"; done
shopt -s nullglob
for f in "$BUILD"/fig_*.pdf; do cp "$f" "$FINAL/"; done
[ -d "$BUILD/assets" ] && cp -r "$BUILD/assets" "$FINAL/"
shopt -u nullglob

python3 "$ROOT/framework/tools/lint_output.py" "$FINAL" --final
pdfinfo "$FINAL/main.pdf" | grep -E '^Pages'
