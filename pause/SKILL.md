---
name: pause
description: Enter "away mode" — the user is stepping away from the machine and will NOT be responding to messages for a while. While away mode is active, do not start any test, task, build, backtest, download, or command expected to run longer than about a minute; the user isn't there to monitor it, answer a mid-run question, or catch it going wrong. Use whenever the user invokes /pause or says anything like "I'm heading out", "going afk", "won't be at my desk for a bit", "stepping away, don't kick off anything big", or "I won't be responding for a while". Keep doing short, safe work; defer the long-running work until the user returns and runs the [[continue]] skill. Do not use /pause and /continue in the same message — they are opposite actions and only one applies right now.
---

# Pause — Away Mode

> **Skill restriction — not compatible with `/continue`.** Pausing (stepping away) and continuing (coming back) are opposite actions; only one applies at any given moment. Never run both in the same message or turn. If the user's message contains cues for both, stop and ask which they mean rather than guessing.

The user is leaving the keyboard and won't answer messages for a while. Everything about how you work has to change to fit that one fact: **there is no one there to watch a long process, approve its next step, or stop it if it goes wrong.** So the rule for the duration of away mode is simple — don't launch anything big and unattended.

## The core rule

While away mode is active, **do not start any operation you expect to run longer than roughly one minute.** In particular:

- Full test suites, `RUN_*.bat` batch runs, regression sweeps
- Backtests, robustness/destruction runs, multi-year data crunches, generator sweeps
- Large downloads, big builds, `npm install`, dependency resolution
- Anything that streams for minutes, or that would normally prompt "this is still running…"

Short, self-contained steps are fine and encouraged — reading and editing files, small greps, quick single-file scripts, a single fast command. The test is runtime and attendance, not importance: a one-line fix is fine; a 20-minute backtest is not, however useful it would be.

**When unsure how long something takes, treat it as long and defer it.** Under-guessing is the expensive mistake here — a big run fired off into an empty room is exactly what this mode exists to prevent.

## What to do instead

1. **Keep making progress on the short stuff.** Anything that finishes in well under a minute and doesn't need the user's input, go ahead and do it. Away mode is not "stop working" — it's "don't start anything big."

2. **When you hit a step that needs a long-running operation, stop at its edge.** Do all the prep (write the script, stage the config, line up the command) but don't pull the trigger. Note it as deferred.

3. **Record what you're deferring** in `.claude/pause-state.md` in the current project directory (create the `.claude/` folder if needed). `/continue` reads exactly this path when the user is back, so keep the name and location. Keep it lean:

   ```markdown
   # Away mode — deferred until user returns
   Entered: <date from your context>

   ## Goal
   <what the user asked for, in full — a fresh session won't remember this chat>

   ## Done while away
   - <short steps already completed>

   ## Deferred long-running tasks (run these on /continue)
   - <the exact command / test / task, ready to run, WITH an estimated runtime — e.g. "RUN_ROBUSTNESS.bat (≈8 min)" or "python backtests/destruction.py (≈15 min)">
   <!-- Always include a rough time estimate per task, so on return the user can prioritize which to actually run given how long they have. -->
   <!-- If unsure of a runtime, say so ("unknown, likely several min") rather than omitting it. -->


   ## Notes
   <decisions, gotchas, literal paths and commands the resumer would otherwise re-derive>
   ```

4. **If the ONLY remaining work is long-running**, there's nothing safe left to do — write the checkpoint, tell the user what's waiting, and stop rather than launching it anyway.

5. **Confirm in a sentence or two**: what you got done, and what's queued for when they're back. Don't recite the whole file.

## What not to do

- Don't rationalize firing off one big run "because it'll probably be fine" — the user explicitly left so they wouldn't have to babysit it.
- Don't kill or wait on something already running in the background; just note in the checkpoint that it's still going and unfinished.
- Don't write a vague checkpoint — a fresh session with no memory of this chat has to be able to run the deferred tasks from this file alone, so record literal commands and paths.
