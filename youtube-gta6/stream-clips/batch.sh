#!/bin/bash
cd /home/user/stream
for f in "$@"; do python3 highlights.py $f.mp4 4 > $f.log 2>&1; done
echo done > batch.done
