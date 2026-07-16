@echo off
rem Backup launcher. Usage: backup.bat "<project path>" ["<backup root>"]
rem With no args it backs up the current directory into a sibling BACKUP folder.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0backup.ps1" %*
