---
name: laptop-mode
description: Guard an unplugged laptop during a long/autonomous run — watch the battery, and when it drops to a threshold (default 20%), stop working and shut the PC down cleanly before it dies. Reads the battery with a PowerShell command; monitors more and more often as the charge falls (it drops fast near the end). Invoked as "laptop-mode" (shut down at 20%) or "laptop-mode N" (e.g. "laptop-mode 10" shuts down at 10%). Use whenever the user invokes /laptop-mode or says "I'm on battery, shut down before it dies", "watch the battery and power off at X%", or runs an autonomous session on an unplugged laptop. Pairs with [[shutdown-when-done]] for the actual power-off.
---

# Laptop Mode

The user is running on battery and doesn't want the laptop to die mid-work (losing state, or just powering off dirty). This mode watches the charge during the run and, when it hits the threshold, **stops working and shuts down cleanly** — a graceful power-off you control, instead of a hard drain to 0%.

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

- Laptop-mode is a **safety bound layered on top of the actual work** (e.g. a [[work-until-limit]] run, an [[ultragoal]], a [[loop]]). Whichever limit trips first wins: if the battery hits the threshold before the usage ceiling, the battery shutdown fires; if usage/clock ends the run first, that ends it. Fold the battery read into the same per-chunk boundary where you take other readings.
- With [[shutdown-when-done]] it's a natural pair — laptop-mode decides *when* (battery threshold), shutdown-when-done does the *how* (summary + power off).
- Respects [[no-talk]] (monitor quietly; only speak up at the threshold or if the battery can't be read).

## Notes

- Only shuts down on the **battery** threshold — if the user plugs in and the charge climbs back up, cancel the imminent shutdown and keep working; note that you're back on AC.
- Don't confuse `BatteryStatus` with charge: a high `BatteryStatus` number is a *state code*, not a percentage. The percentage is always `EstimatedChargeRemaining`.
