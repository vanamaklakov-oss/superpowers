"""Breakdown Shorts builder.  python3 build.py tts|spec|post <video|all>
tts:  narrate each scene (ru-RU-DmitryNeural via edge-tts), keep word timings
spec: lay scenes on the timeline, resolve word cues to frames, write the film spec + host page
post: music bed + narration mix (ducked), TikTok-style captions, mux onto the rendered film"""
import asyncio, json, math, os, re, ssl, subprocess, sys, time, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scripts import VIDEOS

ENGINE = "/home/user/gta6-explainer"; OUT = "/home/user"; HERE = os.path.dirname(os.path.abspath(__file__))
VOICE, FPS, LEAD, TAIL, BOOST = "ru-RU-DmitryNeural", 30, 6, 8, 18
norm = lambda s: re.sub(r"[^\w]", "", s.lower().replace("ё", "е"))

def tts(text, out, rate, pitch="+2Hz"):
    import edge_tts, edge_tts.communicate as c
    c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    variants = [(rate, pitch)] + [(f"{int(rate.rstrip('%')) + dr:+d}%", f"{int(pitch.rstrip('Hz')) + dp:+d}Hz") for dr, dp in [(1, 0), (-1, 1), (2, -1), (0, 2), (-2, 0), (3, 1)]]
    async def go():
        com = edge_tts.Communicate(text, voice=VOICE, rate=variants[k % len(variants)][0], pitch=variants[k % len(variants)][1], boundary="WordBoundary"); words = []
        with open(out, "wb") as f:
            async for ch in com.stream():
                if ch["type"] == "audio": f.write(ch["data"])
                elif ch["type"] == "WordBoundary": words.append({"w": ch["text"], "s": ch["offset"] / 1e7, "d": ch["duration"] / 1e7})
        return words
    for k in range(14):
        try:
            w = asyncio.run(go())
            if w: json.dump(w, open(out + ".json", "w"), ensure_ascii=False); return w
        except Exception as e: err = e
        time.sleep(4 + (k % 4) * 2)
    # the service refuses some whole texts but takes their sentences: narrate one by one, then join
    parts = [p for p in re.split(r"(?<=[.!?])\s+", text) if p]
    if len(parts) < 2: raise RuntimeError(f"tts failed: {text[:40]}")
    words, files, off = [], [], 0.0
    for i, p in enumerate(parts):
        pf = f"{out}.part{i}.mp3"; pw = tts(p, pf, rate, pitch); files.append(pf)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", pf], capture_output=True, text=True).stdout)
        words += [dict(x, s=x["s"] + off) for x in pw]; off += dur
    lst = out + ".list"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    json.dump(words, open(out + ".json", "w"), ensure_ascii=False); return words

def vdir(v): d = f"{HERE}/vo/{v}"; os.makedirs(d, exist_ok=True); return d

def stage_tts(v):
    for i, sc in enumerate(VIDEOS[v]["scenes"]):
        p = f"{vdir(v)}/s{i}.mp3"
        rate = f"{int(sc.get('rate', '+4%').rstrip('%')) + BOOST:+d}%"; key = sc["say"] + "|" + rate
        if os.path.exists(p + ".json") and os.path.exists(p + ".txt") and open(p + ".txt").read() == key: continue
        tts(sc["say"], p, rate); open(f"{p}.txt", "w").write(key); print(v, i, "ok", flush=True)

def split_words(ws):   # the service sometimes fuses two words ("6700 или"): split them, sharing the time by length
    out = []
    for x in ws:
        parts = x["w"].split()
        if len(parts) < 2: out.append(x); continue
        tot = sum(len(p) for p in parts); t = x["s"]
        for p in parts: d = x["d"] * len(p) / tot; out.append(dict(w=p, s=t, d=d)); t += d
    return out

def timeline(v):
    at, rows = 0, []
    for i, sc in enumerate(VIDEOS[v]["scenes"]):
        w = split_words(json.load(open(f"{vdir(v)}/s{i}.mp3.json"))); end = w[-1]["s"] + w[-1]["d"]
        vs = at + (8 if i == 0 else LEAD); b = vs + math.ceil(end * FPS) + TAIL
        rows.append(dict(a=at, b=b, vs=vs, words=w)); at = b
    return rows, at + 30

def stage_spec(v):
    V = VIDEOS[v]; rows, N = timeline(v); rows[-1]["b"] = N; scenes = []
    for sc, r in zip(V["scenes"], rows):
        idx = 0
        def cue(c):
            nonlocal idx
            if isinstance(c, int): return r["vs"] + c
            for j in range(idx, len(r["words"])):
                if norm(r["words"][j]["w"]).startswith(norm(c)): idx = j; return r["vs"] + round(r["words"][j]["s"] * FPS) - 2
            raise KeyError(f"{v}: cue '{c}' not spoken in: {sc['say']}")
        items = []
        for it in sc["items"]:
            it = json.loads(json.dumps(it))
            if "cue" in it: it["cue"] = cue(it["cue"])
            if "markCue" in it: it["markCue"] = cue(it["markCue"])
            for key in ("pills", "rows"):
                for p in it.get(key, []): p["cue"] = cue(p["cue"])
            items.append(it)
        scenes.append(dict(a=r["a"], b=r["b"], items=items))
    spec = dict(title=V["title"], N=N, pal=V["pal"], scenes=scenes)
    json.dump(spec, open(f"{ENGINE}/src/canvas-core/bd-{v}.json", "w"), ensure_ascii=False)
    open(f"{ENGINE}/src/canvas-core/bd{v}.ts", "w").write(f'import spec from "./bd-{v}.json";\nimport {{ makeFilm, type Spec }} from "./bd";\nexport const bd{v} = makeFilm(spec as unknown as Spec);\n')
    open(f"{ENGINE}/src/hosts/page-bd{v}.ts", "w").write(f'import {{ bd{v} }} from "../canvas-core/bd{v}";\nimport {{ mountFilm }} from "./page";\nmountFilm(bd{v});\n')
    print(v, "frames", N, f"({N / FPS:.1f}s)", "scenes", len(scenes))

def bed(path, tot, swish, seed):
    SR = 48000; N = int(SR * tot); L = np.zeros(N); R = np.zeros(N); rg = np.random.default_rng(seed)
    def add(s, t, g=1.0, pan=0.0):
        i = int(t * SR); n = min(len(s), N - i)
        if n > 0: L[i:i + n] += s[:n] * g * (1 - max(0, pan)); R[i:i + n] += s[:n] * g * (1 + min(0, pan))
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    def lp(x, a):
        y = np.empty_like(x); s = 0.0
        for k in range(len(x)): s = a * s + (1 - a) * x[k]; y[k] = s
        return y
    def pluck(m, d, v):
        t = np.arange(int(SR * d)) / SR; f = hz(m)
        return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6)) * np.exp(-t * 2.4) * np.minimum(1, t * 400) * v
    B = 0.5; progs = [[[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]], [[62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 70], [57, 61, 64, 67]]]
    prog = progs[seed % 2]
    for b in range(int(tot / (4 * B)) + 1):
        t0 = b * 4 * B; ch = prog[b % 4]
        for q in range(8): add(pluck(ch[q % 4] + 12 + (12 if q in (3, 6) else 0), 0.9, 0.055), t0 + q * B / 2, 1, 0.35 * (1 if q % 2 else -1))
        add(pluck(ch[0] - 12, 1.8, 0.2), t0); add(pluck(ch[0] - 12, 0.9, 0.12), t0 + 2.5 * B)
        for q in range(4):
            k = np.arange(int(SR * 0.28)) / SR; kick = np.sin(2 * np.pi * np.cumsum(48 + 70 * np.exp(-k * 32)) / SR) * np.exp(-k * 10)
            if q in (0, 2): add(kick, t0 + q * B, 0.42)
            if q in (1, 3):
                s = np.arange(int(SR * 0.16)) / SR; sn = rg.standard_normal(len(s)) * np.exp(-s * 26); add(sn - lp(sn, 0.85), t0 + q * B, 0.09)
            h = np.arange(int(SR * 0.035)) / SR; hat = rg.standard_normal(len(h)) * np.exp(-h * 100); add(hat - lp(hat, 0.5), t0 + q * B + B / 2, 0.05, 0.4)
    for t in swish:
        n = int(SR * 0.4); tt = np.arange(n) / SR; x = rg.standard_normal(n); x = lp(x, 0.6) - lp(x, 0.97); add(x * np.sin(np.pi * tt / 0.4) ** 1.5 * 0.45, t - 0.15)
        p = np.arange(int(SR * 0.12)) / SR; add(np.sin(2 * np.pi * np.cumsum(500 + 900 * p / 0.12) / SR) * np.exp(-p * 25) * 0.12, t + 0.05)   # a little pop as the scene lands
    fade = np.ones(N); i = int((tot - 2) * SR); fade[i:] = np.linspace(1, 0, N - i); L *= fade; R *= fade
    o = np.stack([L, R], 1); o /= np.max(np.abs(o)) * 1.15
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((o * 32767).astype("<i2").tobytes())

def captions(v, rows, path):
    V = VIDEOS[v]; t = lambda x: "%d:%02d:%05.2f" % (x // 3600, (x % 3600) // 60, x % 60); out = []
    for sc, r in zip(V["scenes"], rows):
        keys = set()
        for it in sc["items"]:
            for s in [it.get("text", ""), it.get("sub", "")] + [p["text"] for p in it.get("pills", [])] + [x["text"] for x in it.get("rows", [])]: keys |= {norm(x) for x in s.split()}
        toks = sc["say"].split(); j = 0; words = []
        for x in r["words"]:
            while j < len(toks) and norm(toks[j]) != norm(x["w"]): j += 1
            words.append((toks[j] if j < len(toks) else x["w"], x["s"], x["s"] + x["d"])); j += 1
        chunks, cur = [], []
        for wd in words:
            if wd[0] in ("—", "-"): continue
            cur.append(wd)
            if len(cur) == 3 or wd[0][-1] in ".,:?!—»" or (len(cur) == 2 and len(cur[0][0] + cur[1][0]) > 16): chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        st = r["vs"] / FPS
        for i, c in enumerate(chunks):
            a = st + c[0][1]; b = st + (chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + 0.3)
            txt = " ".join(("{\\c&H0000E1FF&}" + s.upper() + "{\\c&HFFFFFF&}") if (norm(s) in keys or re.search(r"\d", s)) else s.upper() for s, _, _ in c)
            out.append(f"Dialogue: 0,{t(a)},{t(b)},Cap,,0,0,0,,{{\\fscx118\\fscy118\\t(0,110,\\fscx100\\fscy100)}}" + txt)
    hdr = "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Cap,Inter Display Black,80,&H00FFFFFF,&H00FFFFFF,&H00331D1D,&H99331D1D,0,0,0,0,100,100,1,0,1,9,5,2,60,60,300,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    open(path, "w").write(hdr + "\n".join(out) + "\n")

def stage_post(v):
    rows, N = timeline(v); d = vdir(v); tot = N / FPS
    bed(f"{d}/bed.wav", tot, [r["a"] / FPS for r in rows[1:]], seed=sum(map(ord, v)))
    ins = ["-i", f"{d}/bed.wav"]; fc = []
    for i, r in enumerate(rows):
        ins += ["-i", f"{d}/s{i}.mp3"]; ms = int(r["vs"] / FPS * 1000); fc.append(f"[{i + 1}]aresample=48000,adelay={ms}|{ms}[a{i + 1}]")
    n = len(rows)
    fc = ";".join(fc) + ";" + "".join(f"[a{i}]" for i in range(1, n + 1)) + f"amix=inputs={n}:normalize=0,aformat=channel_layouts=stereo,highpass=f=80,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3,aecho=0.85:0.4:28:0.08,apad,atrim=0:{tot},volume=1.3,asplit[vo][sc];[0]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.01:ratio=8:attack=15:release=400[duck];[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5"
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-ar", "48000", f"{d}/mix.wav"], check=True)
    captions(v, rows, f"{d}/caps.ass")
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", f"{ENGINE}/out/bd{v}.mp4", "-i", f"{d}/mix.wav", "-vf", f"subtitles={d}/caps.ass", "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{OUT}/gta6_ru_{v}.mp4"], check=True)
    print(v, "->", f"{OUT}/gta6_ru_{v}.mp4")

if __name__ == "__main__":
    stage, which = sys.argv[1], sys.argv[2]
    for v in (VIDEOS if which == "all" else [which]): {"tts": stage_tts, "spec": stage_spec, "post": stage_post}[stage](v)
