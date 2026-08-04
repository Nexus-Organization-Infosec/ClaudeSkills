---
name: sound-generator
description: Generate custom sound effects from a description — completion chimes, notification blips, alert/error buzzers, success jingles, UI clicks, short tones — as real WAV files, using a dependency-free Python synth. Describe the sound and it builds a note/waveform spec, renders the WAV, previews it, and iterates until it's right. Can install the result as the [[play-sound-when-done]] chime or save it anywhere for your app. Use whenever the user invokes /sound-generator or asks to "make a sound / chime / beep / jingle", "generate a notification sound", "create an alert tone", "design a sound effect", or "change the done-sound". Pure stdlib, no audio libraries or downloads needed.
---

# Sound Generator

Turn a description of a sound into a real, playable WAV. The engine is `scripts/gen_sound.py` — a small pure-stdlib synthesizer (no numpy, no audio libs, no downloads) that renders a JSON **spec** of notes and shaping into 16-bit stereo audio. Your job is to translate what the user wants into a good spec, render it, let them hear it, and refine.

This is the standalone, general version of the synth behind [[play-sound-when-done]] (which only makes its one fixed chime). Here the user designs any sound they want.

## Step 1: Understand the sound they want

Pin down the character before synthesizing:
- **Purpose** — completion chime, notification, error/alert, success jingle, button click, startup sound, a specific melody?
- **Feel** — warm/soft/pleasant, sharp/attention-grabbing, retro/8-bit, bright, muffled, urgent, playful?
- **Length** — a quick blip (~0.1–0.3s), a short jingle (~0.5–1s), or a longer chime (~1–2s)?
- **Where it goes** — install as the "done" chime, save into their app/project, or just save to a file?

If they were vague ("make a nice sound"), pick sensible defaults and iterate from their reaction — don't over-interrogate.

## Step 2: Build the spec

Write a JSON spec (a file, or pipe it on stdin). Full shape and every field are documented at the top of `scripts/gen_sound.py` — read it. The essentials:

```json
{
  "out": "path/to/sound.wav",
  "gain": 0.4,                 // final peak 0..1 — keep <=0.8 so it's not harsh
  "lowpass": 2200,             // optional: softens/muffles; omit for a bright sound
  "notes": [
    {"note": "C5", "start": 0.0, "dur": 1.0, "amp": 1.0, "wave": "bell", "decay": 0.45}
  ]
}
```

- **Pitch:** `"note": "C5"` (names C0–B8, `#`/`b` accidentals) or `"freq": 523.25`.
- **Timing:** `start` and `dur` in seconds. Overlap notes (later `start` < earlier note's end) for chords/ringing; space them out for a melody.
- **Waveform (`wave`):** `bell` (warm, harmonic — chimes), `sine` (pure/soft), `triangle` (mellow retro), `square`/`saw` (buzzy, 8-bit, alerts), `noise` (percussive clicks/hiss).
- **Envelope:** `attack` (fade-in s), `decay` (exp ring-out time — bigger rings longer; `0` = flat with a short release, good for blips).
- **Motion:** `vibrato` (Hz depth) + `vibrato_rate` for a wobble.

**Mapping feel → spec:**
- *Warm/pleasant chime* → `bell`, ascending arpeggio, overlapping, `decay` 0.4–0.5, `lowpass` ~2000–2500.
- *Notification blip* → one or two `square`/`sine` notes, `dur` ~0.09, small `decay`.
- *Error/alert* → low `saw`/`square`, two descending notes, `decay` 0.
- *Success jingle* → three rising notes (`triangle` then a `bell` on the last), short.
- *8-bit/retro* → `square`/`triangle`, no `lowpass`, short notes.

There are ready examples baked in — `python gen_sound.py --demo chime|alert|error|success --out x.wav` — copy one as a starting point and tweak.

## Step 3: Render and preview

Run the engine, then play it so the user hears it:

```bash
python C:/Users/flori/.claude/skills/sound-generator/scripts/gen_sound.py --spec spec.json --play
# or a quick built-in example:
python C:/Users/flori/.claude/skills/sound-generator/scripts/gen_sound.py --demo success --out out.wav --play
```

`--play` plays the WAV synchronously (Windows .NET SoundPlayer). If the user can't hear it, that's usually system volume / output device, not the file — confirm the WAV was written (the script prints the path and duration).

## Step 4: Iterate

Sound design is trial-and-error — expect a couple of passes. Adjust from their feedback:
- "too harsh/piercing" → lower `gain`, add/lower `lowpass`, switch `square`/`saw` → `bell`/`sine`.
- "too quiet" → raise `gain` (cap ~0.8).
- "too long / drags" → shorten `dur`, lower `decay`.
- "too plain" → add an overlapping higher note, a `bell` sparkle on top, or slight `vibrato`.
- "not attention-grabbing" → `square`/`saw`, higher pitch, repeat the blip.

Regenerate and replay until they're happy.

## Step 5: Place the result

- **Save to their app/project** — write the WAV where they want it and tell them the path.
- **Install as the done-chime** — if they want this to become the [[play-sound-when-done]] sound, render it to `C:/Users/flori/.claude/skills/play-sound-when-done/assets/claude_done.wav` (overwrites the default). Confirm before overwriting, and mention they can revert by re-running that skill's `make_sound.py`.
- **Just a file** — leave it at the chosen path and report where it is.

## Notes

- **Pure stdlib** — respects [[no-internet]] (no downloads), runs anywhere Python does.
- Output is 44.1 kHz 16-bit stereo WAV. For other formats (mp3/ogg) you'd need `ffmpeg` — mention it, don't assume it's installed.
- Keep sounds short and `gain` modest; a startling or clipping sound is worse than a quiet one.
- Pairs with [[play-sound-when-done]] (design its chime), and any project that needs UI/notification audio. Respects [[no-talk]] (just render + report the path) and [[quick-*]] (skip the interrogation, pick defaults, render).
