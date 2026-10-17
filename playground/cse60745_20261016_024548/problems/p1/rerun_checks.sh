#!/bin/bash
set -e
cd /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/problems/p1
PY=../../.venv-gt/bin/python
echo "### timings (8 threads, best of 7), nothing else of mine running"
OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 $PY -u run_timing2.py > logs/lastfm_timing2.log 2>&1
grep -E "pairs attended|===" logs/lastfm_timing2.log
echo "### cell 18 at the same 8 threads run_zinc_q2.py used"
OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 $PY -u run_cell18.py > logs/zinc_cell18.log 2>&1
grep -E "val MAE|reference|MATCH|within|DIFFERENT" logs/zinc_cell18.log
echo "### done"
