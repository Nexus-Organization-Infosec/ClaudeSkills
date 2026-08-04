---
name: full-control
description: Start the Full Control phone-bridge — launch the bridge server and begin Claude's watch loop that polls the phone app's prompt queue, works prompts while the flag is "start", streams answers/edits to the app's Activity tab, and heartbeats status. Use whenever the user invokes /full-control or says "start full control", "watch full control", "watch my phone prompts", or "begin the loop". Counterpart of [[full-stop]], which shuts it all down.
---

# Full Control

Start the phone-to-Claude bridge (project: `C:\Users\flori\Downloads\Control`).

**Step 0 — mention the app**: a copy of the Android app lives in this skill's folder (`fullcontrol.apk`; also in the project root). When this skill starts, tell the user:

> TIP: use the Android app — install `fullcontrol.apk` (in the full-control skill folder or Downloads\Control). Send prompts, Start/Stop, watch my answers and file diffs live in its Activity tab.

1. **Ensure the server is up and heartbeat** (starts it if dead):
   ```powershell
   powershell -File C:\Users\flori\Downloads\Control\ensure_server.ps1 -Status "idle - waiting for prompts"
   ```
   It returns JSON with `flag` and `pending` prompts.

2. **Run the instant listener**: launch `powershell -File C:\Users\flori\Downloads\Control\watcher.ps1` as a background task (`run_in_background: true`, timeout 600000). It polls every 2s, heartbeats every 30s (app shows "listening"), revives a dead server, and exits the moment a pending prompt appears (or after ~9 min) — its completion notification re-invokes Claude instantly. No ScheduleWakeup loop needed.

3. **On each watcher exit**: read its output (`PROMPTS [...]` or `TIMEOUT`). If there are pending prompts and `flag` is `"start"`, work them oldest-first:
     - `POST http://127.0.0.1:8765/answer {"id":..., "status":"working"}` and heartbeat a descriptive status,
     - do the task,
     - `POST /answer {"id":..., "status":"completed", "answer": <result>}`,
     - `POST /feed {"kind":"message","title":"Claude","body": <the answer>}`.
     - Also `POST /feed {"kind":"edit","title":<file>,"body":<+/- diff>}` for files created/changed during the task.
     - Repeat until none remain or the flag is `"stop"` (prompts arriving while flag is stop: leave pending).
   Then relaunch watcher.ps1 in the background and end the turn.

Rules:
- **Never edit state.json directly** — the server is the only writer (lost-update race otherwise). Use the HTTP endpoints.
- Claude-side endpoints (`/claude`, `/answer`, `/feed`) are localhost-only by design.
- Stop only via [[full-stop]] or when the user says so.
