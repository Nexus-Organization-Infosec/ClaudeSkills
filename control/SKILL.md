---
name: control
description: An addon (best paired with [[work-until-limit]], but works for any long/autonomous run) that gives the user a physical red STOP button — a small CustomTkinter window launched by a bundled Python script. When the user presses STOP, Claude finishes the CURRENT task and then cleanly ends its turn, instead of the user hard-interrupting mid-action with Esc. The user resumes anytime by typing /continue or literally any message. Use whenever the user invokes /control, or asks for a "stop button", "graceful stop", or "let me pause you without cutting you off mid-task". Launch the button on the first /control of the session.
---

# Control — graceful STOP button

During a long or autonomous run (e.g. [[work-until-limit]], [[ultragoal]], a [[map]] execution), the normal way to stop Claude is Esc — but that interrupts *mid-action*, possibly leaving a half-written edit or an abandoned command. `/control` gives the user a gentler lever: a single red STOP button that asks Claude to **finish what it's doing and then stop**, so the user keeps full control without cutting Claude off messily.

The mechanism is a flag file: the button writes it, Claude checks it between tasks, and stops gracefully when it appears.

## The two files (short paths)

Everything runs through two short files in the project's `.claude/` folder — kept short on purpose so the commands to touch them aren't unwieldy:

- **`.claude/stop`** — the stop flag. The button creates it; you check and delete it.
- **`.claude/status`** — Claude's state, shown in the button window. You write `working` or `stopped` into it.

**Always use the short RELATIVE path — never the full absolute path.** The Bash tool's working directory is already the project root, so `.claude/stop` resolves on its own. Writing out `C:/Users/.../Trader.../.claude/stop` is what made earlier checks unwieldy; don't.

The one command you run at every task boundary is just the check:

```bash
[ -f .claude/stop ]&&echo STOP||echo go
```

`go` = keep working; `STOP` = the user pressed it, go to Step 3. That's it — no status ping needed, because the window shows green "working" by default whenever it's open. Other one-liners:

| Action | Command |
|---|---|
| clear the stop flag | `rm -f .claude/stop` |
| mark yourself stopped | `echo stopped > .claude/status` |

## Step 0: Mention the Android app

This skill folder contains `stopbutton.apk` — a phone version of the STOP button (one red button; it POSTs `/ctlstop` to the Full Control bridge on port 8765, which creates `.claude/stop` in `C:\Users\flori\Downloads\Control`). On the first `/control` of the session, tell the user:

> TIP: use the Android STOP button app too — `stopbutton.apk` (in this skill's folder or in Downloads\Control). Same graceful stop from your phone; needs the bridge server running (`python server.py` in Downloads\Control).

Caveat: the phone flag lands in the Control project's `.claude/stop`. If the controlled session runs in a DIFFERENT project, also check that path at task boundaries (`[ -f "C:/Users/flori/Downloads/Control/.claude/stop" ]`) and clear it there after stopping.

## Step 1: Launch the button (first `/control` of the session)

On the first `/control`, make sure `.claude/` exists, then start the bundled GUI as a background task (Bash tool, run in background):

```bash
pythonw C:/Users/flori/.claude/skills/control/scripts/control_panel.py .claude/stop .claude/status
```

- Use `pythonw` (no console window) if available; plain `python` also works.
- The window shows a tiny status line ("● working" green by default; flips to "■ stopped" grey only on stop) above one red **STOP** button (CustomTkinter styled; falls back to plain tkinter if customtkinter isn't installed). No status ping is needed — it's green while open.
- **Don't relaunch it** if it's already running this session. Note it *closes itself* after a STOP (see Step 3), so when you resume a controlled run, relaunch it to get the button back.
- Tell the user the button is up: press STOP to have Claude wrap up the current task and pause; resume anytime with `/continue` or any message.

## Step 2: Check the flag between tasks

While `/control` is active this session, **between tasks/chunks** — not mid-action — run the check at each boundary:

```bash
[ -f .claude/stop ]&&echo STOP||echo go
```

`go` → keep going; `STOP` → go to Step 3. If you're also running `work-until-limit`, fold it into the same per-chunk checkpoint where you take the usage reading. Checking between tasks (never mid-edit, mid-command) is the whole point — it's what makes the stop *graceful* rather than an interrupt.

### A stop flag is authoritative — NEVER dismiss it as "stale" to keep working

If `.claude/stop` (or the phone flag path) exists, it means STOP was pressed. Honor it — go to Step 3. You do **not** get to decide the flag is "old," "stale," "left over," or "probably not meant for this run" and clear it so you can keep going. That is a fabricated justification for ignoring a real stop the user pressed, and it is banned. Inventing staleness to override the button defeats the entire safety mechanism.

- **A present flag means stop, full stop.** The default reading of a stop flag is always "the user wants me to stop," never "this is probably outdated."
- **The only time you clear the flag is:** (a) as part of honoring the stop in Step 3, or (b) when the user has, in the current message, **explicitly and unambiguously** resumed (typed `/continue`, or clearly said keep going) — and even then, if a stop flag is sitting there, you first **tell the user it's set and confirm they want to resume through it** rather than silently wiping it. A new message that re-invokes a work skill is not automatically permission to erase a pending STOP — the user may have pressed the button and *then* typed, meaning "stop," not "resume."
- **If in doubt, ask — do not clear-and-continue.** "There's a STOP flag set at <path>; do you want me to resume past it or stay stopped?" is the correct move. Clearing it on your own theory of staleness is never correct.
- This applies to the phone flag in the Control project path too: a flag there is a real press, not noise to sweep away.

## Step 3: When STOP was pressed (`.claude/stop` exists)

1. **Finish the current task cleanly** — complete the step in flight (don't abandon a half-applied edit or a running command), leaving the work in a consistent, resumable state. Do not start a new task.
2. **Clear the flag:** `rm -f .claude/stop`. (The window already shows "task stopped" and closes itself after a 10-second countdown — you don't need to kill it. Deleting the flag prevents a later continue from instantly re-triggering a stop.)
3. **End your turn** with a short status: what was just finished, where things stand, and that the user can resume with `/continue` or any message. Then stop — hand control back and wait.

## Step 4: Resuming

The user resumes by typing `/continue` (see the [[continue]] skill) or simply writing anything to keep going. Pick up exactly where you left off — the current task was finished before stopping, so continue with the next one. Since the window closed itself on the stop, **relaunch it** (Step 1) if the resumed run should still be controllable.

## Notes

- **Cooperative, not a kill switch.** The graceful STOP is honored *between* tasks, so there can be a short delay while the current task wraps up — that's intended. For an instant hard stop the user still has Esc; `/control` is the clean alternative to it.
- **The window self-closes** 10 seconds after STOP (showing "task stopped. closing python UI in N seconds"), so each stop ends with a clean shutdown of the panel — relaunch on the next controlled run.
- **A tiny status line** above the button shows green "working" by default the whole time the window is open, and the window itself flips to "task stopped" on a press — so you don't *need* to write `.claude/status` during a run at all.
- **Optional: show what's running.** If you write a short task label into `.claude/status` at the start of each chunk (e.g. `echo "Fixing panic broadcast" > .claude/status`), the window displays it as the current activity — so the user can see *what* they'd be interrupting before they hit STOP. Keep it to a few words. Writing `working` (or nothing) shows the plain green default; `stopped` shows grey. This is a nice-to-have, not required — the short flag check in Step 2 stands on its own.
- **One button only**, by design — no other controls in the window.
- **Composes** with `work-until-limit` (stop a long quota-bounded run on demand), `ultragoal`, and `map`. It is not one of the mutually-exclusive pairs.
