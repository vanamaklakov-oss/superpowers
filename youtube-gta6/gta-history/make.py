import json, subprocess, numpy as np, wave, re, sys
sys.path.insert(0, '/home/user/bd'); import build
FPS = 30; PAUSE = 0.35; LEAD = 0.25
lines = [l.strip() for l in open('lines.txt', encoding='utf-8') if l.strip()]
W = [build.split_words(json.load(open(f'v{i:02d}.mp3.json'))) for i in range(len(lines))]
starts, t = [], 0.0
for i, w in enumerate(W):
    starts.append(t); t += (LEAD if i == 0 else 0) + w[-1]['s'] + w[-1]['d'] + PAUSE
TOT = t + 1.2
vs = [s + (LEAD if i == 0 else 0) for i, s in enumerate(starts)]          # when each line's audio begins
bounds = [round(s * FPS) for s in starts] + [round(TOT * FPS)]
# ---- video: one Ken Burns move per image
moves = ["in", "down", "out", "up", "in_top", "out", "down", "in", "up", "out", "in_top", "up", "in", "out"]
def zexpr(m, n):
    p = f"(on/{n})"
    if m == "in": return f"z='1+0.13*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
    if m == "out": return f"z='1.15-0.13*{p}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'"
    if m == "down": return f"z='1.14':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*{p}'"
    if m == "up": return f"z='1.14':x='iw/2-iw/zoom/2':y='(ih-ih/zoom)*(1-{p})'"
    if m == "in_top": return f"z='1+0.15*{p}':x='iw/2-iw/zoom/2':y='(ih/2-ih/zoom/2)*0.4'"
parts = []
for i in range(len(lines)):
    n = bounds[i + 1] - bounds[i]
    out = f'clip{i:02d}.mp4'
    vf = f"scale=2160:3840:flags=lanczos,zoompan={zexpr(moves[i], n)}:d={n}:s=1080x1920:fps={FPS},setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-loop', '1', '-i', f'img/{i:02d}.jpg', '-vf', vf, '-frames:v', str(n), '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', out], check=True)
    parts.append(out)
open('clips.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'clips.txt', '-c', 'copy', 'joined.mp4'], check=True)
# ---- captions: one word at a time, centre, yellow-green with a black outline
def tt(x): return '%d:%02d:%05.2f' % (x // 3600, (x % 3600) // 60, x % 60)
ev = []
for i, w in enumerate(W):
    toks = [x for x in lines[i].replace('—', ' ').split() if re.search(r'\w', x)]; j = 0; seq = []
    for x in w:
        while j < len(toks) and build.norm(toks[j]) != build.norm(x['w']): j += 1
        word = toks[j] if j < len(toks) else x['w']; j += 1
        seq.append((re.sub(r'[«»".,:?!]', '', word).upper(), vs[i] + x['s'], vs[i] + x['s'] + x['d']))
    for k, (s, a, e) in enumerate(seq):
        b = seq[k + 1][1] if k + 1 < len(seq) else e + 0.25
        ev.append(f"Dialogue: 0,{tt(a)},{tt(b)},W,,0,0,0,,{{\\fscx112\\fscy112\\t(0,90,\\fscx100\\fscy100)}}{s}")
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Inter Display Black,96,&H004AF0E4,&H004AF0E4,&H00000000,&HAA000000,0,0,0,0,96,100,1,0,1,8,6,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('words.ass', 'w').write(hdr + '\n'.join(e.replace(',W,,0,0,0,,', ',W,,0,0,0,,{\\pos(540,1240)}', 1) for e in ev) + '\n')
# ---- score: drone, strings, a low hit on every cut
SR = 48000; N = int(SR * TOT); L = np.zeros(N); R = np.zeros(N); rg = np.random.default_rng(5)
def add(x, at, g=1.0, pan=0.0):
    a = int(at * SR); n = min(len(x), N - a)
    if n > 0: L[a:a + n] += x[:n] * g * (1 - max(0, pan)); R[a:a + n] += x[:n] * g * (1 + min(0, pan))
hz = lambda m: 440 * 2 ** ((m - 69) / 12); tt_ = np.arange(N) / SR
drone = (np.sin(2 * np.pi * hz(38) * tt_) + 0.5 * np.sin(2 * np.pi * hz(45) * tt_ + 0.3 * np.sin(tt_ * 0.7))) * (0.6 + 0.4 * np.sin(tt_ * 0.35)) * 0.12
L += drone; R += drone
prog = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 48, 52]]
for k in range(int(TOT / 4) + 1):
    ch = prog[k % 4]; d = 4.4; t2 = np.arange(int(SR * d)) / SR; env = np.minimum(1, t2 / 1.5) * np.minimum(1, (d - t2) / 1.2)
    for m in ch:
        for det in (-0.004, 0.004):
            ph = (t2 * hz(m + 12) * (1 + det)) % 1; saw = 2 * ph - 1
            sm = np.convolve(saw, np.ones(24) / 24, 'same'); add(sm * env * 0.035, k * 4, 1, det * 60)
for c in bounds[1:-1]:
    tm = c / FPS; t3 = np.arange(int(SR * 1.2)) / SR
    hit = np.sin(2 * np.pi * np.cumsum(40 + 50 * np.exp(-t3 * 18)) / SR) * np.exp(-t3 * 4.5); add(hit, tm, 0.55)
    nz = rg.standard_normal(len(t3)) * np.exp(-t3 * 9); add(np.convolve(nz, np.ones(40) / 40, 'same'), tm, 0.25)
fade = np.ones(N); a = int((TOT - 2) * SR); fade[a:] = np.linspace(1, 0, N - a); L *= fade; R *= fade
o = np.stack([L, R], 1); o /= np.max(np.abs(o)) * 1.1
with wave.open('score.wav', 'wb') as wv: wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((o * 32767).astype('<i2').tobytes())
ins = ['-i', 'score.wav']; fc = []
for i in range(len(lines)):
    ins += ['-i', f'v{i:02d}.mp3']; ms = int(vs[i] * 1000); fc.append(f'[{i + 1}]aresample=48000,adelay={ms}|{ms}[a{i}]')
fc = ';'.join(fc) + ';' + ''.join(f'[a{i}]' for i in range(len(lines))) + f'amix=inputs={len(lines)}:normalize=0,aformat=channel_layouts=stereo,highpass=f=70,equalizer=f=180:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3,aecho=0.8:0.5:40:0.12,apad,atrim=0:{TOT},volume=1.3,asplit[vo][sc];[0]volume=0.6[mu];[mu][sc]sidechaincompress=threshold=0.01:ratio=7:attack=15:release=400[d];[d][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5'
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *ins, '-filter_complex', fc, '-ar', '48000', 'mix.wav'], check=True)
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', 'joined.mp4', '-i', 'mix.wav', '-vf', "noise=alls=7:allf=t,vignette=PI/4.2,subtitles=words.ass", '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', '/home/user/gta_history_ru.mp4'], check=True)
print('done', round(TOT, 1), 's')
