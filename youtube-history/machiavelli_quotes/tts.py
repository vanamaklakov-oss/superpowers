"""Narrate the quote videos sentence by sentence with ru-RU-DmitryNeural, slower and lower. vo/<id>/NN.mp3 + .json"""
import asyncio, ssl, json, os, sys, time
import edge_tts, edge_tts.communicate as c
from script import VIDEOS
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
HERE = os.path.dirname(os.path.abspath(__file__))
RATE, PITCH = -6, -8
def say(text, out):
    for dr, dp in [(0,0),(1,0),(-1,1),(2,-1),(0,2),(-2,0),(3,1),(1,2),(-3,-1),(4,0),(2,3),(-4,2),(5,-2),(0,-3)]:
        async def go():
            com = edge_tts.Communicate(text, voice="ru-RU-DmitryNeural", rate=f"{RATE+dr:+d}%", pitch=f"{PITCH+dp:+d}Hz", boundary="WordBoundary"); ws=[]
            with open(out,"wb") as f:
                async for ch in com.stream():
                    if ch["type"]=="audio": f.write(ch["data"])
                    elif ch["type"]=="WordBoundary": ws.append({"w":ch["text"],"s":ch["offset"]/1e7,"d":ch["duration"]/1e7})
            return ws
        try:
            ws = asyncio.run(go())
            if ws and os.path.getsize(out) > 2000: return ws
        except Exception: print("retry", file=sys.stderr); time.sleep(1.5)
    raise RuntimeError("tts failed: " + text)
for vid, (_, _, sents) in VIDEOS.items():
    d = f"{HERE}/vo/{vid}"; os.makedirs(d, exist_ok=True)
    for i, s in enumerate(sents):
        out = f"{d}/{i:02d}.mp3"
        if os.path.exists(out+".json") and json.load(open(out+".json"))["text"] == s: continue
        ws = say(s, out); json.dump({"text": s, "words": ws}, open(out+".json","w"), ensure_ascii=False); print(vid, i, "ok", flush=True)
