@echo off
rem Shows the Claude toast notification, then schedules shutdown.
rem Optional first argument = delay in seconds (default 60).
set DELAY=%1
if "%DELAY%"=="" set DELAY=60
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0notify.ps1" -Message "All tasks finished - shutting down in %DELAY% seconds. Run 'shutdown -a' to cancel."
shutdown -s -t %DELAY% -c "Claude done. Cancel: shutdown -a"
