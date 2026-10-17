#!/bin/sh
# One command: regenerate answer.tex from the code + logs, copy the figure and the
# preamble into OUTPUT, compile a test document, and lint OUTPUT.
set -e
P2=/home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/problems/p2
OUT=/home/xing/project/auto_hw_complete/output/cse60745_20261016_024548/p2
PY=/home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/.venv-gt/bin/python
cd "$P2"
$PY make_answer.py
cp fig/layer.pdf "$OUT/fig_p2_layer.pdf"
cp OUT_preamble.txt "$OUT/preamble.txt"
rm -rf build/check && mkdir -p build/check
cp "$OUT/answer.tex" "$OUT/fig_p2_layer.pdf" build/check/
./build/mkwrapper.sh build/check
( cd build/check && pdflatex -interaction=nonstopmode -halt-on-error wrapper.tex >/dev/null \
  && pdflatex -interaction=nonstopmode -halt-on-error wrapper.tex >/dev/null )
echo "compiled: $(pdfinfo build/check/wrapper.pdf | grep Pages)"
python3 wordcount.py "$OUT/answer.tex"
python3 /home/xing/project/auto_hw_complete/framework/tools/lint_output.py "$OUT"
echo "OUTPUT contents:"; ls -la "$OUT"
