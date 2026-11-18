#!/bin/bash
# Narrate, verify and build videos q6..q15, then commit. Logs to out/batch2.log
cd "$(dirname "$0")"
for k in 1 2 3; do python3 tts.py 2>&1 | grep -v retry; done
python3 - <<'PY'
import json,subprocess,numpy as np,difflib,re,glob
from faster_whisper import WhisperModel
m=WhisperModel('small',device='cpu',compute_type='int8')
norm=lambda s: re.sub(r'[^а-яё ]','',s.lower().replace('ё','е'))
for n in range(6,16):
  for f in sorted(glob.glob(f'vo/q{n}/*.mp3')):
    j=json.load(open(f+'.json'))
    a=np.frombuffer(subprocess.check_output(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-']),np.int16).astype(np.float32)/32768
    got=''.join(x.text for x in m.transcribe(a,language='ru')[0]); r=difflib.SequenceMatcher(None,norm(j['text']),norm(got)).ratio()
    if r<0.85: print('CHECK',f,round(r,2),'|',got, flush=True)
print('verify done', flush=True)
PY
python3 build.py q6 q7 q8 q9 q10 q11 q12 q13 q14 q15
cd ../.. && git add youtube-history && git commit -qm "Machiavelli quotes: ten more videos (q6-q15), verified quotes, narration

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LZn1gvfKzyGAVymJLobXNu" ; (git push -q 2>&1 || (git pull -q --rebase && git push -q)); echo ALLDONE
