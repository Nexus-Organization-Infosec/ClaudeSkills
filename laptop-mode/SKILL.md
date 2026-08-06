---
name: laptop-mode
description: A BACKGROUND battery safety net for a long/autonomous run — NOT a task in itself. It quietly watches the charge while you keep doing the real work, and only if the battery falls to a threshold (default 20%) does it stop and shut the PC down cleanly before it dies. Never becomes the focus: the actual job (a work-until-limit run, an improve loop, a build) stays the focus; laptop-mode just guards it as an emergency fallback. Reads the battery with a PowerShell command; monitors more often as the charge falls (it drops fast near the end). Invoked as "laptop-mode" (guard at 20%) or "laptop-mode N" (e.g. "laptop-mode 10"). Use whenever the user invokes /laptop-mode or says "I'm on battery, shut down before it dies", "watch the battery in the background", or runs an autonomous session unplugged. Pairs with [[shutdown-when-done]] for the actual power-off.
---

# Laptop Mode

The user is running on battery and doesn't want the laptop to die mid-work (losing state, or just powering off dirty). This mode watches the charge during the run and, when it hits the threshold, **stops working and shuts down cleanly** — a graceful power-off you control, instead of a hard drain to 0%.

## CRITICAL: laptop-mode is a BACKGROUND SAFETY NET — never the focus

Laptop-mode is **not the task.** It is a guard that sits quietly in the background of whatever the *real* work is (a [[work-until-limit]] run, an [[improve]] loop, a build) and only fires if the battery actually runs low. The single most common mistake — the one that prompted this rule — is treating laptop-mode as the main job: announcing "I'll monitor the battery and shut down at 20%" and *centering the session on that*, instead of doing the actual work the user asked for.

- **Keep doing the real work.** If the user invoked laptop-mode alongside other skills (e.g. "`/improve` … `/work-until-limit 90` `/shutdown-when-done` `/laptop-mode`"), the **actual task is the improve / work-until-limit 90 run** — that's what you spend the session doing. Laptop-mode just guards it. Do not stop, slow down, or reframe the session around the battery.
- **The battery guard lives in the background.** On AC, the watcher process (below) does the watching — you don't narrate it or think about it; you work. It only surfaces if the battery is unplugged and falls to the threshold.
- **Keep it in "back of mind," don't foreground it.** Fold the battery check into the same boundary where you already take other readings; a one-line mention only if something changes (unplugged, or nearing the threshold). The planned end of the run is still whatever the *real* bound is (the 90% usage ceiling, the goal, etc.) — the battery threshold is an **emergency fallback** that pre-empts it only if the charge would otherwise die first.
- **Whichever bound trips first wins, but the battery one is the fallback, not the plan.** If usage hits 90% first, that ends the run normally. The battery shutdown is only there for the case where the charge would run out before the planned end. Treat it as insurance, not the objective.

So when laptop-mode is combined with a work run: **go do the work run.** Start the watcher, then get straight into the actual task and keep at it — the battery guard takes care of itself.

## Read the battery with this command

Always read the real charge with PowerShell (not a guess):

```powershell
Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus
```

- **`EstimatedChargeRemaining`** — the percent charge (0–100). This is the number you compare to the threshold.
- **`BatteryStatus`** — power state. **`2` = plugged in / on AC** (charging or maintained); **`1` = discharging (on battery)**. Only count down toward shutdown when it's **discharging**; if it's on AC, the battery isn't draining toward the threshold — relax (see below).
- If the command returns nothing / no battery object, this is a desktop or the battery isn't visible — tell the user laptop-mode doesn't apply here and don't pretend to monitor.

## The threshold

- **`laptop-mode`** (no number) → shut down at **20%**.
- **`laptop-mode N`** → shut down at **N%** (e.g. `laptop-mode 10` → 10%). Pin the number; don't drift off it.

## How to monitor — check MORE often as it falls (it drops fast near the end)

Battery percentage is not linear — it falls slowly up high and **plummets near the bottom**, so a stale reading can jump right past your threshold to a dead battery. So the lower it gets, the more often you check (per [[no-waiting]], these are quick boundary checks between work chunks, never a blocking sleep-loop):

- **On AC (`BatteryStatus 2`) → immediately launch the background watcher; do NOT inline-poll.** The instant a read shows `BatteryStatus 2`, start `scripts/battery_watch.ps1` as a **background task** (Bash tool, `run_in_background: true`) — it runs forever (until you stop it) and writes the live battery state to a status file every ~20s. Then keep working normally and just take an **instant non-blocking peek at the status file** at each boundary instead of running the CIM query yourself:

  Launch it in the background (`run_in_background: true`):
  ```bash
  powershell -NoProfile -ExecutionPolicy Bypass -File C:/Users/flori/.claude/skills/laptop-mode/scripts/battery_watch.ps1 -StatusFile .claude/battery-status.txt
  ```
  Then check it with an instant peek at each boundary:
  ```bash
  cat .claude/battery-status.txt   # read ONAC / CHARGE / STATUS
  ```
  While `ONAC=1`, the machine is on AC — keep working, glance at the file occasionally. **When `ONAC` flips to `0` (unplugged) or `CHARGE` starts falling**, switch to the active battery cadence below (and you can keep reading `CHARGE` from the watcher's file, which updates continuously). The watcher is backgrounded, so the wait-loop hook allows it and it never blocks you. **Stop it** (kill the background shell) when the run ends, when you power off, or if the user cancels laptop-mode — it's the one thing that "runs forever until Claude stops it."
- **Above ~40% and discharging** → check every several work chunks.
- **20%–40%** → check every chunk.
- **Under 20% (or within ~10 points of a low threshold like `laptop-mode 10`)** → check **very frequently — every short chunk**, and keep chunks small. This is the danger zone where it drops fast; a big chunk here can outrun your last reading.
- **Approaching the threshold with a fast drop** → don't wait for the exact number. If a reading is close to the threshold and falling quickly (e.g. it dropped several points since the last check), **shut down now** rather than risk the next read being well past it or the battery dying mid-shutdown. Better a few percent early than a hard power-loss.

When the user set a low threshold (19 or below), be *extra* vigilant as you near it — the lower the target, the faster the final descent and the less margin you have.

## When the charge hits the threshold → shut down cleanly

When `EstimatedChargeRemaining <= threshold` while discharging:

1. **Stop starting new work.** Don't begin another chunk.
2. **Shut down promptly via [[shutdown-when-done]].** A low battery is a hard deadline — write the session summary quickly (or skip the disk summary if it's *very* low and every second counts) and issue the shutdown, per that skill's sequence. Don't dawdle "finishing one more thing"; if the battery dies first you lose the shutdown *and* the work.
3. Tell the user plainly: battery hit the threshold, work paused, powering off — so if they see it later they know why.

The point of the threshold is to shut down *before* the battery forces it. Treat it as "shut down at or just above," never "keep going until slightly under."

## Composing with the run

- Laptop-mode is a **safety bound layered UNDER the actual work** (e.g. a [[work-until-limit]] run, an [[ultragoal]], a [[loop]]) — the work is the focus, the battery guard is the net. Whichever limit trips first wins: if the battery hits the threshold before the usage ceiling, the battery shutdown fires; if usage/clock ends the run first, that ends it normally. But the *planned* end is the work bound (e.g. 90% usage); the battery threshold is the emergency that only matters if the charge would die first. Fold the battery read into the same per-chunk boundary where you take other readings — quietly, without making it the topic.
- With [[shutdown-when-done]] it's a natural pair — laptop-mode decides *when* (battery threshold), shutdown-when-done does the *how* (summary + power off).
- Respects [[no-talk]] (monitor quietly; only speak up at the threshold or if the battery can't be read).

## Notes

- Only shuts down on the **battery** threshold — if the user plugs in and the charge climbs back up, cancel the imminent shutdown and keep working; note that you're back on AC.
- Don't confuse `BatteryStatus` with charge: a high `BatteryStatus` number is a *state code*, not a percentage. The percentage is always `EstimatedChargeRemaining`.
