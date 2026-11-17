import asyncio, ssl, sys, json
import edge_tts, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
voice, text, out, rate, pitch = sys.argv[1:6]
async def main():
    com = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch, boundary="WordBoundary")
    words=[]
    with open(out,'wb') as f:
        async for ch in com.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"]=="WordBoundary": words.append({"w":ch["text"],"s":ch["offset"]/1e7,"d":ch["duration"]/1e7})
    json.dump(words, open(out+'.json','w'), ensure_ascii=False)
asyncio.run(main())
