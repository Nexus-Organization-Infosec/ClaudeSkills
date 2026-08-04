@echo off
setlocal enabledelayedexpansion
title Claude Skills Installer

rem ---------------------------------------------------------------
rem  Copies every skill folder next to this script into the current
rem  user's Claude skills directory. Works for any username because
rem  it uses %USERPROFILE% instead of a hardcoded path.
rem ---------------------------------------------------------------

set "SRC=%~dp0"
set "DEST=%USERPROFILE%\.claude\skills"

echo.
echo  Claude Skills Installer
echo  =======================
echo   From : %SRC%
echo   To   : %DEST%
echo.

if not exist "%DEST%" (
    mkdir "%DEST%" 2>nul
    if errorlevel 1 (
        echo  [!] Could not create "%DEST%"
        echo      Check permissions and try again.
        echo.
        pause
        exit /b 1
    )
    echo  [+] Created %DEST%
    echo.
)

set /a COUNT=0
set /a FAILED=0

for /d %%D in ("%SRC%*") do (
    set "NAME=%%~nxD"
    rem skip git internals and anything that is not a skill folder
    if /I not "!NAME!"==".git" if /I not "!NAME!"==".github" (
        if exist "%%~fD\SKILL.md" (
            robocopy "%%~fD" "%DEST%\!NAME!" /E /NFL /NDL /NJH /NJS /NP /NC /NS >nul
            if errorlevel 8 (
                echo  [!] FAILED  !NAME!
                set /a FAILED+=1
            ) else (
                echo  [+] !NAME!
                set /a COUNT+=1
            )
        )
    )
)

echo.
if !FAILED! GTR 0 (
    echo  Installed !COUNT! skills, !FAILED! failed.
) else (
    echo  Done. Installed !COUNT! skills.
)
echo.
echo  Start a new Claude Code session and type / to see them.
echo.
pause
endlocal
