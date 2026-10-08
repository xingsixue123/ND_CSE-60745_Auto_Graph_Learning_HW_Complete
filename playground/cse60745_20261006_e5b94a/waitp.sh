#!/bin/bash
# Block (no `sleep`) until the fw.py driver process exits, or until $1 seconds elapse.
secs="${1:-540}"
pid=$(pgrep -f "^python3 .*framework/fw\.py (spawn-worker|respawn-worker|submit)" | head -1)
if [ -z "$pid" ]; then
  echo "DRIVER NOT RUNNING"
else
  timeout "$secs" tail -f --pid="$pid" /dev/null
  if kill -0 "$pid" 2>/dev/null; then echo "DRIVER STILL RUNNING (pid $pid) after ${secs}s"
  else echo "DRIVER EXITED"; fi
fi
python3 /home/xing/project/auto_hw_complete/framework/fw.py status | tail -4
echo "--- run.log ---"; tail -4 logs/run.log
echo "--- heartbeat ---"; tail -2 logs/heartbeat.log 2>/dev/null
