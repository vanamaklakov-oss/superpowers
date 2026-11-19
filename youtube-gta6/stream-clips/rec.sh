#!/bin/bash
# rec.sh <channel> : record every broadcast of a TikTok channel for 3 hours (vertical FLV stream)
ch="$1"; cd /home/user/stream
END=$(( $(date +%s) + 3*3600 ))
while [ "$(date +%s)" -lt "$END" ]; do
  out="${ch}_$(date +%Y%m%d_%H%M%S).flv"
  timeout 3h python3 -m yt_dlp --no-playlist --no-part -f "flv-hd/flv-hd1/hls-hd/best" -o "$out" "https://www.tiktok.com/@${ch}/live" >> "yt_${ch}.log" 2>&1
  if [ -s "$out" ]; then echo "$(date '+%F %T') saved $out ($(du -h "$out" | cut -f1))" >> "watch_${ch}.log"; else rm -f "$out"; echo "$(date '+%F %T') offline" >> "watch_${ch}.log"; fi
  sleep 60
done
