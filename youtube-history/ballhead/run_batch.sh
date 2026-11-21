#!/bin/bash
# Build several ball-head projects end to end: backgrounds -> narration -> stills -> video. Usage: run_batch.sh dir...
cd "$(dirname "$0")/.."
for d in "$@"; do
  echo "=== $d"; python3 ballhead/genbgs.py "$d" || { echo "BGFAIL $d"; continue; }
  (cd "$d" && python3 tts.py && python3 build.py --stills && python3 build.py) || echo "FAIL $d"
  ls -la "$d/out/$d.mp4" 2>/dev/null
done
echo ALLDONE
