#!/bin/sh
# Build a test document from OUT_preamble.txt + the generated answer.tex, exactly as the
# master will: preamble lines then \input{answer.tex}.
set -e
D="$1"
{ printf '%s\n' '\documentclass[11pt]{article}'
  printf '%s\n' '\usepackage[margin=1in]{geometry}'
  cat OUT_preamble.txt
  printf '%s\n' '\begin{document}'
  printf '%s\n' '\input{answer.tex}'
  printf '%s\n' '\end{document}'
} > "$D/wrapper.tex"
