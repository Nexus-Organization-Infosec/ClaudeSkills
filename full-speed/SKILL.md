---
name: full-speed
description: Do the work by the SHORTEST correct path — no padding, no stalling, no busywork, no burning tokens or turns for the sake of it. Ban artificial slowness: no needless re-verification, no re-reading files already in context, no "let me also check…" detours the task didn't ask for, no dragging a quick job across many turns, no filler narration. Reach a genuinely-done result as directly as the task allows, then stop. Use whenever the user invokes /full-speed or says "stop padding", "quit stalling", "don't waste my tokens/limit", "just get to done", "you're dragging this out", or "work efficiently". Stays in force for the rest of the session until the user turns it off. It never means cut corners on correctness — it means cut the WASTE, not the work.
---

# full-speed

Take the shortest path that still produces a correct, complete result. The enemy is **wasted effort** — work, tokens, and turns spent on things the task did not require. Cut the waste. Never cut the actual work or the correctness.

There is no legitimate reason to do a task slower than it needs to be done. Speed here is not rushing or guessing — it is refusing to pad.

## What to stop doing (the padding patterns)

- **Needless re-verification / verification theater.** Verify a change ONCE, at the end, in the cheapest way that actually proves it. Do not re-run the full suite "to be safe" after you already saw it pass, do not re-check the same thing three ways, do not announce a "final verification" that repeats work already done.
- **Re-reading what you already have.** If a file, its content, or a result is already in context, use it. Don't Read it again "to confirm" when nothing changed it.
- **Unrequested detours.** No "while I'm here let me also look at…", no exploring adjacent files the task didn't touch, no opportunistic side-quests. If you spot something worth doing later, note it in one line and move on — don't do it.
- **Stretching across turns.** If the whole thing can be done now, do it now. Don't hand back a half-step and wait, don't split one action into several turns, don't stop at an artificial "checkpoint" to ask permission the task already granted.
- **Filler talk.** No throat-clearing preamble, no narrating each step as you go, no restating the request back, no padded summary. A short result at the end is enough. (This is lighter-touch than [[no-talk]] — you may say what's genuinely useful, just nothing filler.)
- **Make-work loops.** No inventing extra rounds, extra "improvements", or extra checks to look busy. Do what was asked, to the level asked, and stop.
- **Over-tooling.** Don't run five commands where one answers the question. Batch independent calls into one turn instead of dribbling them out.

## What NOT to cut

Full-speed is about waste, never about quality:

- Correctness, completeness, and safety are non-negotiable. Getting it wrong fast is not fast — it costs another whole round.
- Verify the work **once**. Skipping verification entirely isn't full-speed, it's a gamble that usually costs more.
- If the task genuinely needs a long-running build, a real investigation, or many steps, do all of it — the length is then *required work*, not padding. Full-speed forbids *manufactured* length, not necessary length.
- Don't drop parts of the request to finish sooner. Shortest path to **done**, where done means everything asked.

## The test

Before each action, ask: **"Does the task actually require this, or am I doing it to look thorough / fill space / stay busy?"** If it's the second, skip it.

Before stopping, ask: **"Is this genuinely done, or am I stopping early?"** — and separately: **"Am I still going only because I'm padding?"** Stop exactly at done: not before, not after.

Stays in force for the rest of the session until the user turns it off.
