---
name: read-skills-again
description: Force a fresh re-read of the actual SKILL.md files from disk, even when you think you already know what the skills do. Open and read the real files in the skills folder rather than relying on the short descriptions in the menu or your memory of them — the skills change often, and your cached understanding drifts or is stale. Use whenever the user invokes /read-skills-again or says "re-read your skills", "read the skills again", "you're not following the skill, read it", "refresh the skills", or after the skills have been edited. Read the current text, then apply it.
---

# Read Skills Again

Stop and **actually re-read the skill files from disk.** Not the one-line descriptions in the skills menu, not your memory of what a skill "does" — open the real `SKILL.md` files and read the current text. Your recollection of a skill is a summary, and summaries go stale: these skills are edited constantly (new rules, new banned rationalizations, new arguments, new steps), so what you *think* the skill says is very likely out of date. The whole point of this skill is to defeat "I already know this one."

## Why this exists

- The menu descriptions are short triggers, not the full instructions — the real behavior lives in the body of each `SKILL.md`.
- Skills get patched often. A rule you're sure about may have been tightened, reversed, or replaced since you last read it.
- "I already know what /work-until-limit does" is exactly the assumption that makes you miss the new mantra, the new banned excuses, the enforced mode, etc. Re-read means re-read.

## What to do

1. **Determine which skills to re-read.**
   - If the user named one or more (`/read-skills-again work-until-limit swarm`), read those.
   - If they named none, re-read the skills **relevant to the current task or run** — the ones you're about to use or are already operating under. If a run is active (e.g. `work-until-limit`, `swarm`, `control`), those are first priority.
   - "Read the skills again" with no context and no active task → re-read the ones you most recently claimed to be applying.

2. **Open the actual files and read them fully.** They live in the skills directory, one folder per skill:
   `C:/Users/flori/.claude/skills/<name>/SKILL.md`
   Use the Read tool on each file. Read the **whole** body, not just the frontmatter — the rules that matter are in the steps, notes, and banned-reasons sections. If a skill has bundled `references/` or `scripts/`, glance at those too when they're relevant.

3. **Notice what changed.** Actively compare against what you assumed. Call out to yourself (briefly) anything that's different from your prior understanding — a new argument, a new rule, a new forbidden rationalization — so you actually apply the current version, not the remembered one.

4. **Then apply the current text.** Continue the task under what the file *actually says now*. If re-reading revealed you were about to do something the updated skill forbids, correct course.

## Notes

- This is cheap insurance against drift — a few file reads to make sure you're running the real, current instructions rather than a stale mental copy.
- Especially worth it right after the user says the skills were edited, or when your behavior seems to contradict what a skill should do ("you're not following it — read it again").
- Respects [[no-talk]] (re-read silently, then just act correctly). Pairs with everything — it doesn't change *what* you do, only ensures you're using the up-to-date rules for it.
- Don't fake it: actually call Read on the files. "I've refreshed my understanding" without opening them is the exact behavior this skill exists to stop.
