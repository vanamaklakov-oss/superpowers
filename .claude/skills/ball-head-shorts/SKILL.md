---
name: ball-head-shorts
description: Make a history Short in the "ball-head characters in a 3D world" style (as on viral history-twist channels): cartoon ball-head people with stick limbs over rich 3D-render scenes, very fast cuts, one word of caption at a time, a story with a twist. Use when the user asks for this style, a "как у Архивариуса" video, or a short with ball-head / round-head characters.
---

# Ball-head history Shorts

Learned from a frame-by-frame read (30 fps) of a viral reference (69 s, 394x854, English, "the railroad gaps" story).
Measured: 214 words in 65 s (~197 wpm, fast), ~30 shots, median shot 0.8 s (long shots only for dialogue),
81 % of frames have visible motion, 6 % are static.

## The look
- **Characters**: a white ball head with no outline shading, two dot or short-line eyes, a small mouth line; eyebrows
  do the acting (angry = slanted, surprised = raised, worried = sweat drop). Body is a coloured costume shape
  (waistcoat, coat, uniform) with thin black stick arms and legs. Hats define who is who (flat cap = young
  engineer, bowler = boss, top hat = rich man, peaked cap = conductor). Same costume and hat in every shot.
- **Emotion gags**: the head fills with colour from the chin up (purple = rage), steam puffs from the head,
  sweat drop, big gritted teeth, eyes go wide with a tiny pupil.
- **World**: detailed 3D-render-looking scenes (canyon, rails, station, carriage interior, newspaper), warm
  saturated light, strong perspective; characters are flat 2D cut-outs standing in that world.
- **Captions**: ONE word at a time, white, bold, thin dark outline, centred at ~60 % height, changes exactly on
  the spoken word. No yellow two-line style here.

## The motion (what moves every second)
- Camera never stops: slow push-ins on dialogue, fast dolly/fly-throughs along rails, whip-pans between shots.
- Characters: small idle bob and lean, blinking, brows move on the key word, arms gesture; head colour fills
  over ~10 frames for rage.
- Story beats get a physical action (train drives in, rail kicks sideways, newspaper slaps onto screen).

## The story
Hook in the first 2 s with the absurd-sounding act ("He sawed gaps into every rail"), then: rivals, mockery,
public humiliation, a time skip ("Then summer comes"), the hidden reason pays off, the rival's disaster.
Titles that worked on Russian channels: "Самая гениальная ловушка в истории", "Он попросил X и разорил Y",
"Самый издевательский суд в истории". Facts are checked like every other video in youtube-history/.

## How we build it here (no copying of anyone's characters)
1. Script: 12–20 sentences, 45–65 s, twist structure above; fact-check and cite sources in script.py.
2. Backgrounds and camera moves: Grok image + "Make video" prompts (one combined prompt per shot), no people
   in them, 9:16, "3D animated film render, warm saturated light, strong perspective, no text".
3. Characters: our own ball-head rig drawn in code (youtube-history/ballhead/rig.py), composited over the
   clips with idle bob, blink, brow/mouth poses, rage fill, steam, sweat; same costume per character.
4. Narration ru-RU-DmitryNeural at +18 % (fast, like the reference), one-word captions, no music unless asked.
