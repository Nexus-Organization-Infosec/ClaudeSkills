@echo off
rem Play the completion chime over the default speakers (synchronously).
powershell.exe -NoProfile -Command "(New-Object Media.SoundPlayer '%~dp0..\assets\claude_done.wav').PlaySync()"
