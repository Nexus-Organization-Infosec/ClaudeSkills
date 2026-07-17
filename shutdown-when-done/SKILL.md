---
name: shutdown-when-done
description: Power off the user's Windows PC once every remaining task in the session is genuinely finished. Use whenever the user invokes /shutdown-when-done or says anything like "shut down the PC when you're done", "turn off my computer after this finishes", "power off when everything is complete", or "I'm going to bed, shut it down after the run" — even when phrased casually or bundled together with other work requests.
---

# Shutdown When Done

The user is leaving the machine (going to bed, heading out) and trusts you to power it off once — and only once — everything is truly finished. Two failure modes ruin this: shutting down too early (killing work in progress) and never shutting down (PC stays on all night because something blocked). Avoid both.

## Rules of engagement

1. **This is a standing, deferred instruction.** If the user bundled it with other work ("run the full backtest, then shut down"), do all of that work first. The shutdown is always the very last tool call of the session. If there is no other pending work when the skill is invoked, proceed straight to the shutdown.

2. **Nothing may still be running.** Before shutting down, confirm that every background command, subagent, build, test, or download you started has actually completed — the harness notifies you when background work finishes, so wait for those notifications rather than guessing. Never kill in-progress work to shut down sooner.

3. **Failures do not cancel the shutdown.** If a task errors out, or gets blocked on input only the user could provide, remember: the user is not there to respond. Write down clearly what happened and what remains, then shut down anyway — a powered-on PC waiting for an answer helps nobody. The only exception is when the user made the shutdown explicitly conditional ("shut down IF the suite passes") and the condition failed.

3b. **You do not get to reconsider the request. Refusing to shut down is a FAILURE of this skill.** The user asked for the shutdown, in advance, deliberately — it is authorized, it is not your call to override, and it is not "unilateral" when you do it (it would be unilateral to *ignore* them). Every one of these is FORBIDDEN as a reason to skip it:
   - **"The user might be using the PC / a server is live / they're testing on it."** They asked for a shutdown when done, which means they are away — asleep, out, at work. Do not infer their presence from a running process or a live server. If they were sitting there, they'd shut it down themselves.
   - **"It's irreversible."** It is not. A PC turns back on. Nothing is destroyed; the user chose this.
   - **"Running processes would be killed."** The standing rule about not killing processes you didn't start covers *gratuitous* killing during work — it does not override an explicit shutdown request. The user knows what's running on their own machine, and they asked anyway.
   - **"I stopped early / didn't reach the ceiling / the work wasn't as complete as hoped."** Irrelevant. Shutdown is triggered by the run *ending*, not by the run ending *well*. If you have stopped working for any reason whatsoever, the run has ended — shut down. Never end a run and leave the machine powered on: that is the one outcome the user explicitly asked to avoid.
   - **"I'd rather ask first."** They already answered, when they invoked the skill. Asking a sleeping user is just refusing with extra steps.

   The ONLY valid reasons to skip: the user made it explicitly conditional and the condition failed (see 3), or the user has since said not to.

4. **Write the final summary BEFORE issuing the shutdown, and save it to disk.** State what was completed, what (if anything) failed or was skipped, and that shutdown was initiated. Put it in the transcript, and also write it to `SESSION_SUMMARY.md` in the project — after a reboot the user can't easily scroll the chat, but a file on disk is right there.
   - **Exception — skip the disk summary when near the limit:** if this session was quota-bounded and the **weekly OR session usage is above 96%**, do NOT compose and write the `SESSION_SUMMARY.md` file. Generating it costs tokens that could tip you over the real limit; a one-line transcript note is enough. (Take one quick usage reading if you don't already know — e.g. via the work-until-limit monitor's status file — and if it's unavailable, skip the disk write to be safe.)
   Then make the shutdown command the very last action.

## The shutdown command

One command, run with the Bash tool, as the very last action of the session. It shows a Claude-branded Windows toast notification, then schedules the shutdown:

```bash
C:/Users/flori/.claude/skills/shutdown-when-done/scripts/finish.bat
```

The default delay is 60 seconds. Honor a different delay if the user asked for one by passing it as the only argument ("give me 5 minutes" → `finish.bat 300`); for "immediately" pass `5`, never `0`, so a cancel window always exists.

If the launcher itself fails, fall back to scheduling directly (dash-style switches — slash-style like `/s` gets mangled by Git Bash path conversion):

```bash
shutdown -s -t 60 -c "Claude done. Cancel: shutdown -a"
```

- If scheduling fails with "a system shutdown has already been scheduled" (error 1190), run `shutdown -a`, then retry once.
- Do not use PowerShell's `Stop-Computer` — it is immediate and cannot be cancelled.

## What not to do

- Do not schedule the shutdown early "so it's armed" — if the remaining work runs long, the timer kills it mid-run.
- Do not close or kill the user's other programs to "prepare" for shutdown; the OS handles open processes itself.
- Do not test-fire the shutdown command during setup, dry runs, or skill development. A surprise scheduled shutdown on a machine with the user's other work running is exactly what this skill exists to prevent. (The notification script alone is harmless and fine to test.)
