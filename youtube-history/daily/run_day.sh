#!/bin/bash
# narrate + build every video folder under daily/ that has no out/<slug>.mp4 yet
cd "$(dirname "$0")"
for d in d*_*/; do d=${d%/}; [ -f "$d/out/$d.mp4" ] && continue
  for k in 1 2 3; do python3 tts_one.py "$d" 2>&1 | grep -v retry; done
  python3 build_one.py "$d" 2>&1 | tail -1
done
echo ALLDONE
