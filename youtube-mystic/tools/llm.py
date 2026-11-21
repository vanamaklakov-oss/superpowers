#!/usr/bin/env python3
# Вызов FreeLLMAPI (OpenAI-совместимый): python3 llm.py "вопрос" [модель=auto]. Сначала запустить tools/freellm.sh.
import json, os, sys, urllib.request
S = os.environ.get("S", "/tmp/freellm")
def ask(prompt, model="auto", system=None):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    req = urllib.request.Request("http://localhost:3001/v1/chat/completions", json.dumps({"model": model, "messages": msgs}).encode(),
                                 {"Authorization": "Bearer " + open(f"{S}/unified.key").read().strip(), "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180)); return d["choices"][0]["message"]["content"], d.get("model")
if __name__ == "__main__":
    out, m = ask(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "auto"); print(f"[{m}]\n{out}")
