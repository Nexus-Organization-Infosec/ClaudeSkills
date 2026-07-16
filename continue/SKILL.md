---
name: continue
description: The user is back at the keyboard — resume work. This lifts the "away mode" set by /pause (long-running tasks are allowed again) and runs whatever was deferred, OR picks back up work that got cut off mid-stream (e.g. a usage limit was hit and the session stopped without warning). Use whenever the user invokes /continue or says anything like "I'm back", "keep going", "continue where you left off", "you got cut off, finish it", or "carry on". Always pair mentally with the [[pause]] skill, which writes the checkpoint this skill looks for. Do not use /pause and /continue in the same message — resuming and pausing are opposite actions and only one applies to the current moment.
---

# Continue

> **Skill restriction — not compatible with `/pause`.** Continuing (coming back) and pausing (stepping away) are opposite actions; only one applies at any given moment. Never run both in the same message or turn. If the user's message contains cues for both, stop and ask which they mean rather than guessing.

There are two distinct situations this skill has to cover, and the very first thing to do is figure out which one applies — the recovery paths are different.

**If a `work-until-limit` run was cut off, resume it toward the *remaining* budget.** If `.claude/wul-config`, `.claude/wul-banked`, and `.claude/wul-log` exist, a quota-bounded run was interrupted (a reset, a `/usage` glitch, or a cutoff). Read them and continue toward the ceiling using banked + current progress — do NOT restart toward the full ceiling. Only do this if the user asks to resume it; otherwise leave the files and treat their new message normally (per work-until-limit's "active only when invoked" rule).

**Before resuming in either case, confirm the baseline is healthy.** An interruption can leave a half-applied edit, a broken import, or a failing state behind. Run the project's quick tests or build first to check you're resuming from known-good ground — building new work on top of a broken interrupted state just compounds the mess. If the baseline is broken, fix that first, then continue.

## Step 1: Look for an explicit checkpoint

Check whether `.claude/pause-state.md` exists in the current project directory.

**If it exists**, the user went into away mode via /pause and is now back. Away mode is over — long-running tasks are allowed again. Read the file fully, then:
1. **Run the deferred long-running tasks** listed under "Deferred long-running tasks" — these are the big tests/builds/backtests that were held back precisely because they couldn't run unattended. Now that the user is present, execute them, in order. Before firing each one, glance at reality (the files it names, the task list) to confirm nothing already moved past it since the checkpoint was written; skip or adjust anything already handled rather than redoing it.
2. Then continue with whatever was left of the "Goal" beyond those deferred tasks.
3. Once the checkpointed work is truly done (or the user pauses again), delete `.claude/pause-state.md` so a stale checkpoint doesn't confuse a future /continue on unrelated work. If the user pauses again before finishing, follow the [[pause]] skill to rewrite it fresh.
4. Briefly tell the user what you're kicking off, in one sentence — they already know what was deferred.

## Step 2: No checkpoint file — infer an involuntary interruption

**If no checkpoint file exists**, the user is almost certainly invoking /continue because something stopped Claude without warning — most often a usage limit hit mid-task, sometimes a crash or connection drop. No checkpoint got written, so reconstruct from whatever evidence survives. Two cases, and it matters which you're in:

- **Same session continues** (the earlier conversation is still above you in context): the transcript is your best record. Re-read the last several turns — the final tool call and its result, whether it landed or was mid-flight, and the plan leading up to it.
- **Fresh session** (the cutoff forced a new conversation, so there's no history to read): the chat is gone, but the work left physical traces. Look at what actually changed — recently modified files, uncommitted edits in the working tree (`git status` / `git diff` where applicable), a persisted task list, half-written output files, the newest entries in any project logs. These survive session boundaries when the transcript doesn't.

In both cases, work in this order:
1. **Check the task list** (TaskList, if the harness's task tracking was in use) for anything `in_progress` or `pending` — the most reliable single signal of where things stopped, and it persists across sessions.
2. **Gather the evidence** appropriate to your case above.
3. **State your read before acting**: one or two sentences on what you believe was interrupted and what you'll do to finish it. This matters more than in the checkpoint case, because you're inferring, not reading a deliberate summary. Give the user room to correct you, but don't wait for a reply before proceeding unless the ambiguity is genuinely high — e.g. two plausible unfinished threads, or a fresh session where the traces are too thin to be sure. In that thin-evidence case, it's better to ask "here's the little I can reconstruct — what were we doing?" than to guess and act.
4. Resume from there — finish the interrupted step, then continue with whatever was left of the original task.

**If neither a checkpoint nor any sign of unfinished work exists** (the last turn looks fully wrapped up, nothing pending, no stray changes), say so plainly — tell the user nothing appears to be paused or interrupted, and ask what they'd like to continue.

## What not to do

- Don't silently restart a task from the beginning because reconstructing the exact interruption point felt easier than reading carefully — redone work wastes the time /continue exists to save.
- Don't leave a stale `.claude/pause-state.md` behind once its task is actually finished — the next /continue in this project should not resume something that's already done.
- Don't invoke both /pause and /continue in one message — if the user's message contains both cues, ask which one they mean rather than guessing.
