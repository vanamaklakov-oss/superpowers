# GTA 6 in 40 seconds: chalkboard explainer (US)
Made with anidoodle (github.com/alexgreensh/anidoodle, Apache-2.0).
1. `node <anidoodle>/skills/anidoodle/engine/tools/scaffold.mjs ~/gta6-explainer --film explainer --format 9x16 --duration 40`, `npm install`
2. Copy `explainer.ts` to `src/canvas-core/explainer.ts`, then `node tools/render.mjs explainer --out out/explainer.mp4`
3. Narration: `lines.txt` via `../tools/etts_words.py` (en-US-AndrewNeural, +8%, +6Hz) into `vo/v1..v8.mp3`; offsets 0.3/5.1/9.4/15.6/21.75/26.75/32.25/35.75 s
4. `bed.py` writes the music bed and eraser swishes; `caps.py` writes the TikTok-style captions; mix and mux with ffmpeg (sidechain duck, loudnorm -14).
Facts: release Nov 19 2026 on PS5 and Xbox Series X|S, PC later; delays 2025 -> May 26 2026 -> Nov 19 2026; trailer 1: about 93M views in 24 h (record for a non-music video); YouTube 24-hour launch stream from midnight ET Nov 19.
