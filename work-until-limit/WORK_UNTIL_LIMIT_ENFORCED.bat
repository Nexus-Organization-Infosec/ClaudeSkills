@echo off
setlocal
REM ==========================================================================
REM  work-until-limit ENFORCED launcher
REM
REM  Double-click this to run an ENFORCED work-until-limit session. Unlike
REM  typing the skill in a chat, this makes stopping-early impossible: this
REM  window is the parent loop, and it drives Claude as a child until the real
REM  usage meter hits your ceiling.
REM
REM  It asks for the ceiling, the working folder, and the task, then runs.
REM  Close the window (or Ctrl+C) to stop; that's the only operator-side stop.
REM ==========================================================================

title work-until-limit ENFORCED

set "SCRIPT=%~dp0scripts\wul_enforce.ps1"

echo(
echo  === work-until-limit ENFORCED ===
echo(

set "SESSION=50"
set /p SESSION=Session ceiling %% (stop when session usage reaches this) [50]:

set "WEEKLY=0"
set /p WEEKLY=Weekly ceiling %% (0 = don't bound weekly) [0]:

set "PDIR=%CD%"
set /p PDIR=Project folder to work in [%CD%]:

echo(
echo  Enter the task (what to work on). One line. Leave blank for a general
echo  "keep improving/hardening this project" run.
set "TASK="
set /p TASK=Task:

set "PERM=acceptEdits"
set /p PERM=Permission mode (acceptEdits / bypassPermissions) [acceptEdits]:

set "SD="
set /p SDANS=Shut down the PC when the ceiling is reached? (y/N):
if /i "%SDANS%"=="y" set "SD=-ShutdownWhenDone"

echo(
echo  Launching enforced run: session %SESSION%%%  weekly %WEEKLY%%%  dir "%PDIR%"
echo  (Ctrl+C in this window is the only way to stop it early.)
echo(

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" ^
  -SessionCeiling %SESSION% -WeeklyCeiling %WEEKLY% -ProjectDir "%PDIR%" ^
  -PermissionMode "%PERM%" -Task "%TASK%" %SD%

echo(
echo  === run ended ===
pause
endlocal
