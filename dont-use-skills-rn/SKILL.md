---
name: dont-use-skills-rn
description: Turn the skills layer OFF. Stop applying any previously active skill mode, and stop auto-reaching for skills based on what a message looks like — for this message and every message after it. Behave like plain default Claude with no skills. Use whenever the user invokes /dont-use-skills-rn or says "stop using skills", "don't apply your skills", "skills off", "ignore your skills for now", or "no skills right now". Stays in force until the user turns it back on. The ONLY exception is an explicit slash invocation: if the user types /somename, run that one skill for that request.
---

# Don't Use Skills Right Now

Switch the skills layer off. From this message onward, until the user lifts it, act like default Claude with no skills in play.

## What this means

- **Drop every standing skill mode.** Anything a previous message turned on stops now: `careful`, `no-internet`, `stay-here`, `mask`, `no-talk`, `work-until-limit`, away mode from `pause`, and any other. None of them apply anymore.
- **Stop auto-applying skills.** Normally a skill kicks in when a request looks like it fits. Not now. Even if a message clearly matches a skill, do not reach for it. Just handle the request with your normal default behavior.
- **This covers this message and all later ones.** Past messages that invoked skills no longer count. Do not carry any skill behavior forward.

## The one exception: an explicit slash invocation

If the user explicitly types a skill with a leading slash (for example `/fix`, `/research`, `/careful`), that is a deliberate override. Run that one skill for that request, exactly as asked. An explicit `/name` always wins.

After that, this "skills off" state stays in force for the following messages. The single explicit call was a one-off, unless the skill they invoked is itself a standing mode they just chose to turn on again (in which case honor that skill's own on/off rules).

## Turning it back on

The user lifts it: "use skills again", "skills back on", or similar. Until they do, the baseline is skill-free.

## Notes

- This only silences the skills layer. It does not change your core tools, your normal helpfulness, or any safety rule. It just stops skills from auto-triggering and stops old skill modes from lingering.
- If you are unsure whether something counts as "using a skill," lean toward not using it. The whole point is a clean, skill-free default until the user says otherwise or types a `/`.
