---
name: full-stop
description: Shut down the Full Control phone-bridge completely — end Claude's watch loop, stop the bridge server (server.py started via ensure_server.ps1), and mark Claude offline in the app. Use whenever the user invokes /full-stop or says "stop full control", "stop the watch loop", "shut down the bridge/server", or "stop the ps1". Counterpart of [[full-control]], which starts everything.
---

# Full Stop

Cleanly shut down the Full Control system (project: `C:\Users\flori\Downloads\Control`).

Do these steps in order:

1. **Mark Claude offline in the app** (best effort, before killing the server):
   ```powershell
   Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/claude -Body '{"status":"offline - watch loop stopped"}' -ContentType application/json
   ```
   Ignore errors if the server is already down.

2. **Stop the bridge server** (the python process running server.py — this is what ensure_server.ps1 keeps alive):
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name like 'python%'" | Where-Object {$_.CommandLine -match 'server\.py'} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false }
   ```

3. **Stop the listener**: kill any running watcher process and don't relaunch it:
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name like 'powershell%'" | Where-Object {$_.CommandLine -match 'watcher\.ps1'} | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -Confirm:$false }
   ```
   Also TaskStop the background watcher task if one is tracked in this session, and if a ScheduleWakeup loop is running, call `ScheduleWakeup` with `stop: true`.

4. **Confirm to the user**: loop ended, server stopped (the phone app will show "PC unreachable"). Note that `/full-control` (or asking to "watch full control" again) brings it all back.

Do NOT delete state.json — queued prompts survive for the next start.
