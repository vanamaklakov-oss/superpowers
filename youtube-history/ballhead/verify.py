"""Transcribe a project's narration with faster-whisper and print it next to the script: python3 ballhead/verify.py <dir>"""
import sys, os, subprocess, importlib.util, numpy as np
from faster_whisper import WhisperModel
d = os.path.abspath(sys.argv[1]); s = importlib.util.spec_from_file_location("s", f"{d}/script.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
model = WhisperModel("small", device="cpu", compute_type="int8")
for n, text, *_ in m.SCENES:
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{d}/vo/{n:02d}.mp3", "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    got = " ".join(x.text.strip() for x in model.transcribe(a, language="ru")[0])
    print(f"{n:02d} SCRIPT: {text}\n   HEARD:  {got}")
