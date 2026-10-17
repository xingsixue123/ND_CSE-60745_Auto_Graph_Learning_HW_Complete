#!/bin/bash
# After the ZINC seed runs: point SparseSPDAttention at the winning pair set, make the sign
# flip conditional, prove both are inert where it matters, then re-measure LastFM and timings.
set -e
cd /home/xing/project/auto_hw_complete/playground/cse60745_20261016_024548/problems/p1
PY=../../.venv-gt/bin/python

echo "### 1. switch the submitted pair set + conditional sign flip"
python3 switch_submitted.py
python3 apply_flip_fix.py

echo "### 2. the pair sets measured in Table 2 are unchanged by the rename"
OMP_NUM_THREADS=8 $PY -u verify_switch.py 2>&1 | grep -vE "Warning|warn|^  masks" | tee logs/verify_switch.log

echo "### 3. the full test suite, against the final solution.py"
OMP_NUM_THREADS=8 $PY -u test_solution.py > logs/test_solution.log 2>&1
grep -cE "^  PASS" logs/test_solution.log | xargs echo "checks passed:"
tail -1 logs/test_solution.log

echo "### 4. clean timings on an idle machine (Table 3)"
OMP_NUM_THREADS=32 MKL_NUM_THREADS=32 $PY -u run_timing.py > logs/lastfm_timing.log 2>&1
grep "pairs attended" logs/lastfm_timing.log

echo "### 5. LastFM with the final code, and ZINC cell 18, in parallel"
OMP_NUM_THREADS=10 MKL_NUM_THREADS=10 nohup $PY -u run_lastfm_final.py > logs/lastfm_final.log 2>&1 &
OMP_NUM_THREADS=16 MKL_NUM_THREADS=16 nohup $PY -u run_cell18.py > logs/zinc_cell18.log 2>&1 &
wait
echo "### done"
grep -hE "micro-F1" logs/lastfm_final.log
grep -hE "MAE|MATCH|DIFFERENT|reference" logs/zinc_cell18.log
