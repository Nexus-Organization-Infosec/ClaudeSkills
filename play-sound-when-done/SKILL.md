---
name: play-sound-when-done
description: Play a short, friendly chime over the speakers once the session's work is finished, so the user knows to look back without watching the screen. A standing, deferred instruction — do all the requested work first, then play the sound as the final action. Use whenever the user invokes /play-sound-when-done or says "beep when you're done", "play a sound when finished", "make a noise when the task completes", or "let me know with a sound". Pairs with long/autonomous runs.
---

# Play Sound When Done

The user wants an audible "I'm done" so they can step away and come back when they hear it. This is a standing, deferred instruction: **do all the requested work first, then play the chime as the very last action** before handing back.

## What to do

1. **Finish the actual work.** If the user bundled this with other requests ("do X, then play a sound"), complete X first. The sound signals completion, so it only makes sense once you're genuinely done and about to hand back.
2. **Play the chime** (Bash tool). It's a warm completion sound bundled with the skill, played synchronously over the default speakers:

   ```bash
   C:/Users/flori/.claude/skills/play-sound-when-done/scripts/play.bat
   ```

3. That's it — then give your normal wrap-up. Play the sound **once**, at the end, not between steps.

## Details

- The sound is `assets/claude_done.wav` — a soft ascending major arpeggio with a bell-like decay, deliberately gentle so it's pleasant, not startling.
- **To change it:** edit the note list in `scripts/make_sound.py` and re-run `python .../make_sound.py` to regenerate the WAV.
- Plays through the **default output device** at the system volume — if the user hears nothing, that's a muted/zero-volume or wrong-output-device issue on their side, not the skill.

## Composing with other skills

- With **`/shutdown-when-done`**: play the chime **before** the shutdown finale — once the machine powers off there are no speakers. (Though a chime moments before a shutdown that's about to happen anyway is often redundant; use judgment.)
- With **`/work-until-limit`**, **`/ultragoal`**, **`/improve N`**: play once when the whole run ends, not per chunk/round.
- Not mutually exclusive with anything.
