"""Generic Russian GTA 6 short builder.  python3 vbuild.py <cfg>   (cfg_<name>.py next to this file)
Shots: 'S:<material path>:<start>:<TY|XC|FULL>' stream footage (gameplay box cropped, blurred fill),
       'I:<screenshot name>' official screenshot pan.  Several shots per line split its time."""
import importlib, json, os, subprocess, sys
sys.path.insert(0, '/home/user/bd'); import build
name = sys.argv[1]; C = importlib.import_module(f'cfg_{name}')
D0 = f'/home/user/viral/{name}'; os.makedirs(D0, exist_ok=True); os.chdir(D0)
M = '/home/user/stream/material'; IMG = '/home/user/viral/img'
BOX = {'TY': (880, 780), 'XC': (340, 1190), 'FULL': (0, 1920)}
FPS, PAUSE = 30, 0.35
lines = C.LINES
for i, l in enumerate(lines):
    p = f'v{i:02d}.mp3'
    if os.path.exists(p + '.txt') and open(p + '.txt').read() == l: continue
    build.tts(l, p, '+22%'); open(p + '.txt', 'w').write(l)
W = [build.split_words(json.load(open(f'v{i:02d}.mp3.json'))) for i in range(len(lines))]
starts, t = [], 0.0
for i, w in enumerate(W): starts.append(t); t += 0.2 + w[-1]['s'] + w[-1]['d'] + PAUSE
TOT = t + 0.8; vs = [s + 0.2 for s in starts]; ends = starts[1:] + [TOT]

parts, credits, k = [], [], 0
for i, shots in enumerate(C.SHOTS):
    a, b = round(starts[i] * FPS), round(ends[i] * FPS); cuts = [a + round((b - a) * j / len(shots)) for j in range(len(shots) + 1)]
    for j, s in enumerate(shots):
        n = cuts[j + 1] - cuts[j]; d = n / FPS; out = f'shot{k:02d}.mp4'; f = s.split(':')
        if f[0] == 'S':
            y, h = BOX[f[3]]
            vf = (f"crop=1080:{h}:0:{y},split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.25:saturation=1.2[bg];"
                  f"[b]scale=1080:-2,zoompan=z='1.0+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x{h}:fps={FPS}[fg];[bg][fg]overlay=0:(H-h)/2-40,setsar=1,format=yuv420p")
            if f[3] == 'FULL': vf = f"zoompan=z='1.0+0.05*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},setsar=1,format=yuv420p"
            inp = ['-ss', f[2], '-i', f'{M}/{f[1]}.mp4']; who = 'tyrone' if '_ty_' in f[1] or f[3] == 'TY' else 'xcoldcut'; credits.append((cuts[j] / FPS, cuts[j + 1] / FPS, f'кадры: @{who}'))
        elif f[0] == 'V':   # landscape video: enlarged centre band over a blurred fill
            vf = (f"split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=28:2,eq=brightness=-0.25:saturation=1.2[bg];"
                  f"[b]scale=-2:820:flags=lanczos,crop=1080:820,zoompan=z='1.0+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x820:fps={FPS}[fg];[bg][fg]overlay=0:(H-h)/2-40,unsharp=5:5:0.6,setsar=1,format=yuv420p")
            inp = ['-ss', f[2], '-i', f'/home/user/viral/src/{f[1]}']; credits.append((cuts[j] / FPS, cuts[j + 1] / FPS, 'кадры: трейлер Rockstar Games'))
        else:
            x = f"(iw-1080)*{'t/' + str(d) if k % 2 == 0 else '(1-t/' + str(d) + ')'}"
            vf = f"scale=-2:2050:flags=lanczos,crop=1080:1920:x='{x}':y='(ih-1920)/2',setsar=1,fps={FPS},format=yuv420p"
            inp = ['-loop', '1', '-framerate', str(FPS), '-i', f'{IMG}/{f[1]}.jpg']; credits.append((cuts[j] / FPS, cuts[j + 1] / FPS, 'скриншоты: Rockstar Games'))
        if not os.environ.get('AUDIO_ONLY'): subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *inp, '-t', f'{d:.3f}', '-filter_complex', vf, '-frames:v', str(n), '-r', str(FPS), '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', out], check=True)
        parts.append(out); k += 1
open('shots.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
if not os.environ.get('AUDIO_ONLY'): subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'shots.txt', '-c', 'copy', 'joined.mp4'], check=True)

tt = lambda x: '%d:%02d:%05.2f' % (x // 3600, (x % 3600) // 60, x % 60)
bgr = lambda c: '&H00%s%s%s&' % (c[5:7], c[3:5], c[1:3])
pop = '{\\fscx40\\fscy40\\t(0,160,\\fscx112\\fscy112)\\t(160,260,\\fscx100\\fscy100)}'
ev = []
def D(a, b, st, tx, layer=1): ev.append(f'Dialogue: {layer},{tt(a)},{tt(b)},{st},,0,0,0,,{tx}')
last = len(lines) - 1
for i in range(len(lines)):
    big, col, pill = C.TITLES[i]
    if pill: D(starts[i] + 0.05, ends[i], 'Pill', '{\\fad(150,0)}' + pill)
    b1, _, b2 = big.partition('|')
    D(starts[i] + 0.05, ends[i], 'Big', pop + f'{{\\4c{bgr(col)}}}' + b1)
    if b2: D(starts[i] + 0.3, ends[i], 'Big2', pop + '{\\c&H004DD8FF&}' + b2)
for a, b, tx in credits: D(a, b, 'Credit', tx, 0)
keys = {build.norm(x) for x in C.KEYS.split()}
for i, w in enumerate(W):
    toks = lines[i].split(); j = 0; seq = []
    for x in w:
        while j < len(toks) and build.norm(toks[j]) != build.norm(x['w']): j += 1
        seq.append((toks[j] if j < len(toks) else x['w'], x['s'], x['s'] + x['d'])); j += 1
    chunks, cur = [], []
    for s in seq:
        if s[0] in ('—', '-'): continue
        cur.append(s)
        if len(cur) == 3 or s[0][-1] in '.,:?!—»': chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for c_i, c in enumerate(chunks):
        a = vs[i] + c[0][1]; b = vs[i] + (chunks[c_i + 1][0][1] if c_i + 1 < len(chunks) else c[-1][2] + 0.3)
        txt = ' '.join(('{\\c&H0000E1FF&}' + s.upper() + '{\\c&HFFFFFF&}') if build.norm(s) in keys else s.upper() for s, _, _ in c)
        D(a, b, 'Cap', '{\\fscx116\\fscy116\\t(0,110,\\fscx100\\fscy100)}' + txt, 0)
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Big,Inter Display Black,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00D84FFF,0,0,0,0,100,100,2,0,1,11,9,8,50,50,300,1
Style: Big2,Inter Display Black,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,11,9,8,50,50,440,1
Style: Pill,Inter Display Black,46,&H00FFFFFF,&H00FFFFFF,&H00141414,&H00141414,0,0,0,0,100,100,3,0,3,14,0,8,50,50,200,1
Style: Cap,Inter Display Black,76,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,1,0,1,9,5,2,60,60,300,1
Style: Credit,Inter Display Black,30,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,3,0,3,40,40,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open('titles.ass', 'w').write(hdr + '\n'.join(ev) + '\n')
MUSIC = getattr(C, 'MUSIC', False)   # default: voice only, no background music
if MUSIC: build.bed('bed.wav', TOT, starts[1:], seed=C.SEED)
ins = ['-i', 'bed.wav'] if MUSIC else ['-f', 'lavfi', '-t', f'{TOT}', '-i', 'anullsrc=r=48000:cl=stereo']; fc = []
for i in range(len(lines)):
    ins += ['-i', f'v{i:02d}.mp3']; ms = int(vs[i] * 1000); fc.append(f'[{i + 1}]aresample=48000,adelay={ms}|{ms}[a{i}]')
n = len(lines)
vo = ';'.join(fc) + ';' + ''.join(f'[a{i}]' for i in range(n)) + f'amix=inputs={n}:normalize=0,aformat=channel_layouts=stereo,highpass=f=80,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3,aecho=0.85:0.4:28:0.08,apad,atrim=0:{TOT},volume=1.3'
fc = (vo + ',asplit[vo][sc];[0]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.01:ratio=8:attack=15:release=400[d];[d][vo]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5') if MUSIC else (vo + ',loudnorm=I=-14:TP=-1.5')
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', *ins, '-filter_complex', fc, '-ar', '48000', 'mix.wav'], check=True)
if os.environ.get('AUDIO_ONLY'):   # re-mix sound only, keep the rendered picture
    o = f'/home/user/gta6_{name}_ru.mp4'; subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', o, '-i', 'mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', o + '.tmp.mp4'], check=True)
    os.replace(o + '.tmp.mp4', o); print('audio', o); sys.exit()
vf = "drawbox=x=0:y=0:w=1080:h=560:color=black@0.25:t=fill,eq=saturation=1.12:contrast=1.04,subtitles=titles.ass"
out = f'/home/user/gta6_{name}_ru.mp4'
subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-i', 'joined.mp4', '-i', 'mix.wav', '-vf', vf, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-maxrate', '6M', '-bufsize', '12M', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
print('done', out, round(TOT, 1), 's')
