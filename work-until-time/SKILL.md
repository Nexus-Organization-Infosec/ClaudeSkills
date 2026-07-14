---
name: work-until-time
description: Work continuously on the task at hand until a target clock time (German / Europe-Berlin time), then stop. A task already in progress when the time hits may finish, but work must NEVER run more than 5 minutes past the target — that's a hard ceiling. Invoked as "work-until-time <HH:MM> [shutdownwhendone]" — e.g. "work-until-time 11:30" works until 11:30 German time and stops; append "shutdownwhendone" to power off at the end. Use whenever the user invokes /work-until-time or says "work until <time>", "keep going until 11:30", or "stop at <clock time>". The time-bounded sibling of [[work-until-limit]].
---

# Work Until Time

Keep doing useful work until a target wall-clock time (German time), then stop cleanly. Simple idea, one firm rule: **a task in progress when the target hits can finish, but nothing may run more than 5 minutes past the target.** Target + 5 min is an absolute ceiling.

## Step 1: Parse the invocation

`work-until-time <HH:MM> [shutdownwhendone]`
- **`<HH:MM>`** — the target time, interpreted as **German time (Europe/Berlin)**. Accept `11:30`, `11:30pm`, "11:30 German time", etc.
- **`shutdownwhendone`** (optional) — run the [[shutdown-when-done]] finale when work stops.
- Compute the **hard ceiling = target + 5 minutes** (e.g. target 11:30 → hard stop 11:35). Never work past it.
- If the target has already passed today, don't silently assume tomorrow — confirm with the user which they meant.

Also decide **what to work on** — usually the task already in play; if there's none, ask.

**Pin the target and hard cap to a file so they can't drift.** Over a long run (many chunks, a possible context compaction), a target time held only in memory can slip. Record it once:

```bash
printf 'TARGET=%s\nHARDCAP=%s\n' <HH:MM> <HH:MM+5min> > .claude/wut-config
```

Read it back (`cat .claude/wut-config`) whenever you're deciding — the target is exactly what the user gave, never a remembered approximation.

## Step 2: Get the current German time (Windows-correct commands)

Check the clock with one of these. **Your machine is set to German time, so plain local `date` is correct and simplest:**

```bash
date '+%H:%M:%S'
```

For an explicit Europe/Berlin reading that's right even if the machine's clock isn't German, use PowerShell:

```bash
powershell.exe -NoProfile -Command "[System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow,'W. Europe Standard Time').ToString('HH:mm:ss')"
```

**Do NOT use `TZ='Europe/Berlin' date` in the Bash tool** — Git Bash on Windows mishandles it and returns the wrong time (observed 2 hours off). Use plain `date` or the PowerShell form above.

## Step 3: Work in bounded chunks, checking the clock between them

Loop:
1. **Read the current German time** (Step 2).
2. **Decide:**
   - **`now >= target`** → stop the loop. Do not start any new chunk. Go to Step 4.
   - **`now < target`** → do **one bounded chunk** of useful work. Keep chunks short — a few minutes each — so you can't accidentally sail past the ceiling.
   - Before starting a chunk you expect to be long, check there's room: if it could run past the **hard ceiling (target + 5 min)**, don't start it — do something smaller or stop.
3. **Optionally show the countdown** each chunk, e.g. `German time 11:22 — 8 min left (stop 11:30, hard cap 11:35)`.
4. Repeat.

### The 5-minute grace, precisely
- The grace exists only for a chunk **already running** when the target passes — it may finish, but **must not cross target + 5 min.**
- After the target, **start no new chunks.** Only let an in-flight one wrap up.
- Because chunks are kept short (~≤5 min), a chunk begun just before the target can't blow the ceiling. If any work is somehow approaching the hard cap, stop it there — the ceiling is not negotiable.

## Step 4: Stop cleanly

1. **Summarize** what you accomplished and the current time (note if you used part of the grace window).
2. **If `shutdownwhendone`** was in the invocation, run the `/shutdown-when-done` finale now (notification + scheduled shutdown) as the very last action. Otherwise hand the work back.

## Notes

- **Cooperative stop:** nothing interrupts you mid-action — the target is honored because you check the clock *between* chunks. So keep chunks short and check every time; that's what keeps you inside the ceiling.
- Composes with `/shutdown-when-done`, `/control` (STOP button), `/ultragoal`, and `/improve`. It's the time-bounded sibling of `/work-until-limit` (quota-bounded) — use whichever bound you want, or, if you ever want both, stop at whichever comes first.
- Respects `/no-talk`.
