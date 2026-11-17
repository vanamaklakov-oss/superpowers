import asyncio, ssl, sys
import edge_tts, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
voice, text, out, rate, pitch = sys.argv[1:6]
asyncio.run(edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch).save(out))
