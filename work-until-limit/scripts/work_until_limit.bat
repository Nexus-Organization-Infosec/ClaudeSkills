@echo off
rem Launcher for the work-until-limit usage monitor.
rem Usage: work_until_limit.bat <sessionThreshold%%> [statusfile] [intervalSeconds] [weeklyThreshold%%]
rem   sessionThreshold - stop when the SESSION limit reaches this %% (0 = don't bound session; default 80)
rem   statusfile       - where to write the status the skill polls (default %%TEMP%%\claude_work_until_limit_status.txt)
rem   intervalSeconds  - seconds between usage checks (default 300; lower = more quota spent by the monitor itself)
rem   weeklyThreshold  - stop when the WEEKLY limit reaches this %% (0 = don't bound weekly; default 0)
setlocal
set THRESHOLD=%1
if "%THRESHOLD%"=="" set THRESHOLD=80
set STATUSFILE=%2
if "%STATUSFILE%"=="" set STATUSFILE=%TEMP%\claude_work_until_limit_status.txt
set INTERVAL=%3
if "%INTERVAL%"=="" set INTERVAL=300
set WEEKLY=%4
if "%WEEKLY%"=="" set WEEKLY=0
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0usage_monitor.ps1" -Threshold %THRESHOLD% -WeeklyThreshold %WEEKLY% -StatusFile "%STATUSFILE%" -IntervalSeconds %INTERVAL%
endlocal
