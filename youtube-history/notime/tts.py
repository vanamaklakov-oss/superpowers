"""Narrate each scene with ru-RU-DmitryNeural, sentence by sentence, keeping word timings.
Output: vo/NN.mp3 + vo/NN.json (words with start/duration, seconds)."""
import asyncio, ssl, json, os, re, subprocess, sys, time
import edge_tts, edge_tts.communicate as c
from script import SCENES

c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
HERE = os.path.dirname(os.path.abspath(__file__)); VO = f"{HERE}/vo"; os.makedirs(VO, exist_ok=True)
VOICE, RATE, PITCH = "ru-RU-DmitryNeural", 10, 2   # lively: rate +14%, pitch +6Hz

def say(text, out):
    tries = [(RATE + dr, PITCH + dp) for dr, dp in [(0, 0), (1, 0), (-1, 1), (2, -1), (0, 2), (-2, 0), (3, 1), (1, 2), (-3, -1), (4, 0), (2, 3), (-4, 2), (5, -2), (0, -3), (6, 1), (-5, 0)]]
    variants = [text, text.rstrip(".!?…"), text.rstrip(".!?…") + "!"]   # the service sometimes refuses a form; vary it
    for k, (r, p) in enumerate(tries * 2):
        t = variants[k % len(variants)]
        if k >= len(tries): time.sleep(4)                                    # second pass: give the service time
        async def go():
            com = edge_tts.Communicate(t, voice=VOICE, rate=f"{r:+d}%", pitch=f"{p:+d}Hz", boundary="WordBoundary"); ws = []
            with open(out, "wb") as f:
                async for ch in com.stream():
                    if ch["type"] == "audio": f.write(ch["data"])
                    elif ch["type"] == "WordBoundary": ws.append({"w": ch["text"], "s": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
            return ws
        try:
            ws = asyncio.run(go())
            if ws and os.path.getsize(out) > 2000: time.sleep(6); return ws   # be gentle with the service
        except Exception as e: print("retry", r, p, file=sys.stderr); time.sleep(1.5)
    raise RuntimeError(f"tts failed: {text}")

def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

for n, text, *_ in SCENES:
    out = f"{VO}/{n:02d}.mp3"
    if os.path.exists(out + ".json") and json.load(open(out + ".json")).get("text") == text: continue
    parts = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]; files, words, t = [], [], 0.0
    for i, s in enumerate(parts):
        pf = f"{VO}/{n:02d}.p{i}.mp3"; ws = say(s, pf); files.append(pf)
        words += [{**w, "s": w["s"] + t} for w in ws]; t += dur(pf)
    lst = f"{VO}/{n:02d}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    for f in files: os.remove(f)
    os.remove(lst)
    json.dump({"text": text, "dur": dur(out), "words": words}, open(out + ".json", "w"), ensure_ascii=False)
    print(n, "ok", round(dur(out), 2), flush=True)
