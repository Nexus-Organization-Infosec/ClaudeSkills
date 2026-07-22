param(
    [int]$SessionCeiling = 50,        # stop when session usage >= this (0 = don't bound session)
    [int]$WeeklyCeiling  = 0,         # stop when weekly usage  >= this (0 = don't bound weekly)
    [string]$Task        = "",        # the first-turn task prompt (what to work on)
    [string]$TaskFile    = "",        # ...or a file whose contents are the first-turn prompt
    [string]$ProjectDir  = (Get-Location).Path,
    [string]$PermissionMode = "acceptEdits",  # headless permission mode; "bypassPermissions" for full autonomy
    [int]$UsageTimeoutSec = 120,      # per /usage call timeout
    [int]$MaxUnreadable   = 3,        # consecutive unreadable meter reads before giving up (valid stop)
    [int]$MaxCrashes      = 5,        # consecutive claude crashes before giving up
    [switch]$ShutdownWhenDone,        # power off the PC once the ceiling is reached
    [switch]$DryRun                   # DEMO: never call claude, never shut down; simulate a rising meter so you can watch the loop drive to the ceiling at zero cost
)

# In dry-run we simulate the meter climbing so the whole control flow can be
# observed (loop -> read -> re-invoke -> ceiling -> shutdown) without spending
# any quota or touching the real CLI. Starts a bit below nothing so the first
# read is small, then climbs ~11% per turn.
$script:DryMeter = 3

# ============================================================================
#  work-until-limit ENFORCER  (external control loop)
#
#  WHY THIS EXISTS: the work-until-limit SKILL is behavioral text, and the model
#  can always talk itself into stopping early ("diminishing returns", "pacing",
#  "everything needs your decision"...). This script removes that choice. It is
#  the PARENT process: it launches Claude as a headless CHILD (`claude -p`),
#  reads the REAL usage meter after each turn, and if usage is still below the
#  ceiling it re-invokes Claude (`claude -c`, continuing the same conversation)
#  with a "keep going" prompt. Stopping early is not a state the model can reach,
#  because the model does not own the loop -- this script does.
#
#  Claude cannot decline to run this, because Claude does not run it: YOU launch
#  it (double-click the .bat), and it runs Claude. If a Claude turn crashes or
#  exits early, the loop just relaunches it. The only things that end the run are
#  the three legitimate conditions: (1) a ceiling is reached, (2) the meter is
#  unreadable N times in a row, or (3) YOU stop it (Ctrl+C, or a stop flag).
#
#  HONEST LIMITS (read these):
#   * Enforcement applies ONLY to runs started THROUGH this wrapper. Typing the
#     skill in a normal interactive session is NOT enforced -- launch via the
#     .bat to get the guarantee.
#   * This drives the `claude` CLI you're logged into. Each turn and each /usage
#     check spends quota (that's the point -- it's spending up to the ceiling).
#   * If YOU kill this window, sleep the machine, or lose network, the loop ends.
#     Nothing can enforce against the operator turning it off -- the guarantee is
#     only that *the model* can't end it early.
#   * `claude -c` continues the most recent conversation in ProjectDir, which is
#     how context carries across turns. Don't run two enforcers in one dir.
# ============================================================================

$ErrorActionPreference = "Continue"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$StopFlag = Join-Path $ProjectDir ".claude\wul_stop.flag"
$LogFile  = Join-Path $ProjectDir ".claude\wul_enforce.log"
try { New-Item -ItemType Directory -Force -Path (Join-Path $ProjectDir ".claude") | Out-Null } catch {}

function Log {
    param([string]$msg)
    $line = "[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $msg
    Write-Host $line -ForegroundColor Cyan
    try { Add-Content -Path $LogFile -Value $line -Encoding UTF8 } catch {}
}

# --- read + parse the real usage meter (reuses usage_monitor.ps1's regexes) ---
function Get-Usage {
    param([int]$TimeoutSec)
    if ($DryRun) {
        $script:DryMeter += 11
        return @{ Ok = $true; Session = [math]::Min($script:DryMeter, 100); Week = 0 }
    }
    $job = Start-Job -ScriptBlock {
        try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
        claude -p "/usage" 2>&1 | Out-String
    }
    $raw = $null
    if (Wait-Job $job -Timeout $TimeoutSec) { $raw = Receive-Job $job }
    else { Stop-Job $job -ErrorAction SilentlyContinue }
    Remove-Job $job -Force -ErrorAction SilentlyContinue

    if ([string]::IsNullOrWhiteSpace($raw)) { return @{ Ok = $false; Session = -1; Week = -1 } }
    $session = -1; $week = -1
    $ms = [regex]::Match($raw, 'Current session:\s*(\d{1,3})\s*%')
    if ($ms.Success) { $session = [int]$ms.Groups[1].Value }
    $mw = [regex]::Match($raw, 'Current week[^:\r\n]*:\s*(\d{1,3})\s*%')
    if ($mw.Success) { $week = [int]$mw.Groups[1].Value }
    if ($session -lt 0 -and $week -lt 0) { return @{ Ok = $false; Session = -1; Week = -1 } }
    return @{ Ok = $true; Session = $session; Week = $week }
}

function Ceiling-Reached {
    param($u)
    if ($SessionCeiling -gt 0 -and $u.Session -ge 0 -and $u.Session -ge $SessionCeiling) { return $true }
    if ($WeeklyCeiling  -gt 0 -and $u.Week    -ge 0 -and $u.Week    -ge $WeeklyCeiling)  { return $true }
    return $false
}

function Bar {
    param([int]$pct, [int]$ceil)
    if ($ceil -le 0) { $ceil = 100 }
    $cells = 20
    $filled = [math]::Round(($pct / [double]$ceil) * $cells)
    if ($filled -lt 0) { $filled = 0 }; if ($filled -gt $cells) { $filled = $cells }
    return "[" + ("#" * $filled) + ("-" * ($cells - $filled)) + "] $pct% of $ceil"
}

# --- resolve the first-turn task -------------------------------------------
if ($Task -eq "" -and $TaskFile -ne "" -and (Test-Path $TaskFile)) {
    $Task = Get-Content -Path $TaskFile -Raw
}
if ([string]::IsNullOrWhiteSpace($Task)) {
    $Task = "Work continuously on this project until told to stop: improve it, harden it, " +
            "add tests, fix bugs, extend features. Rotate across useful activities. Do NOT " +
            "stop on your own -- an external controller decides when the run ends."
}

Set-Location $ProjectDir
if (Test-Path $StopFlag) { Remove-Item $StopFlag -Force -ErrorAction SilentlyContinue }

$ceilDesc = @()
if ($SessionCeiling -gt 0) { $ceilDesc += "session $SessionCeiling%" }
if ($WeeklyCeiling  -gt 0) { $ceilDesc += "weekly $WeeklyCeiling%" }
Log "ENFORCER START | ceiling: $($ceilDesc -join ' / ') | dir: $ProjectDir | perm: $PermissionMode"

# baseline reading — if unreadable, DO NOT run blind. The #1 cause is being logged out.
$u = Get-Usage -TimeoutSec $UsageTimeoutSec
if (-not $u.Ok) {
    Log "baseline usage UNREADABLE. Retrying once in case of a transient hiccup..."
    Start-Sleep -Seconds 3
    $u = Get-Usage -TimeoutSec $UsageTimeoutSec
}
if (-not $u.Ok) {
    # Definitively check whether it's an auth problem (the usual cause).
    $loggedOut = $false
    try {
        $authRaw = (claude auth status 2>&1 | Out-String)
        if ($authRaw -match '"loggedIn"\s*:\s*false' -or $authRaw -match '"authMethod"\s*:\s*"none"') { $loggedOut = $true }
    } catch {}
    Log '======================================================================'
    if ($loggedOut) {
        Log '  NOT LOGGED IN - `claude auth status` reports loggedIn:false.'
        Log '  That is why the meter is unreadable.'
    } else {
        Log '  METER UNREADABLE - the Claude CLI is most likely NOT LOGGED IN.'
    }
    Log '  claude -p "/usage" is returning a cost stub with no percent lines.'
    Log ''
    Log '  FIX: authenticate, then relaunch this window:'
    Log '      claude auth login           (opens your browser to sign in)'
    Log '      claude setup-token          (long-lived token; best for unattended runs)'
    Log ''
    Log '  Refusing to run blind - without the meter I cannot know when to stop'
    Log '  or when to fire the shutdown, so I would burn quota uncontrolled.'
    Log '  (If you ARE logged in and it is still a stub, headless /usage may not'
    Log '   expose percentages in this CLI version - use a time-bound run instead.)'
    Log '======================================================================'
    return
}
Log ("baseline usage -> session {0}% / week {1}%" -f $u.Session, $u.Week)

if ($u.Ok -and (Ceiling-Reached $u)) {
    Log "Already at/over the ceiling before starting. Nothing to do."
    return
}

$turn = 0
$unreadable = 0
$crashes = 0
$firstTurn = $true

while ($true) {
    if (Test-Path $StopFlag) { Log "STOP flag found -> ending run (user interrupt)."; break }

    $turn++
    # Build the prompt. First turn = the task; later turns = a continue-and-keep-going nudge
    # that carries the live meter reading, so the model knows exactly where it stands.
    if ($firstTurn) {
        $prompt = $Task
        $args = @("-p", $prompt, "--permission-mode", $PermissionMode)
    } else {
        $sess = if ($u.Ok) { "$($u.Session)%" } else { "unknown" }
        $prompt =
            "[ENFORCED work-until-limit -- turn $turn] You are at session $sess against the " +
            "$SessionCeiling% ceiling" + $(if ($WeeklyCeiling -gt 0) { " (weekly ceiling $WeeklyCeiling%)" } else { "" }) + ". " +
            "You have NOT reached the ceiling, so keep working. This is an external control loop: " +
            "it re-prompts you until the real usage meter hits the ceiling, so stopping early is " +
            "impossible and pointless -- any 'I'll stop / pace / surface for a decision' reasoning is " +
            "overridden. Continue the previous task; if one activity is exhausted, switch to another " +
            "genuinely useful one (tests, bug hunt, security/red-team pass, hardening, docs, perf, next " +
            "feature). Park anything that truly needs my decision in a notes file and keep going on work " +
            "that doesn't. Do real, verified work this turn."
        $args = @("-c", "-p", $prompt, "--permission-mode", $PermissionMode)
    }

    Log ("--- turn {0} (claude {1}) ---" -f $turn, $(if ($firstTurn) { "-p" } else { "-c -p" }))
    if ($DryRun) {
        Log ("[DRYRUN] would invoke: claude {0}" -f ($args -join ' '))
        Start-Sleep -Seconds 1
        $code = 0
    } else {
        try {
            & claude @args 2>&1 | ForEach-Object { Write-Host $_ }
            $code = $LASTEXITCODE
        } catch {
            $code = 999
            Log "claude invocation threw: $($_.Exception.Message)"
        }
    }

    if ($code -ne 0) {
        $crashes++
        Log "claude exited with code $code (consecutive crashes: $crashes/$MaxCrashes)."
        if ($crashes -ge $MaxCrashes) { Log "Too many consecutive crashes -> stopping."; break }
        Start-Sleep -Seconds ([math]::Min(30, 5 * $crashes))
        # don't flip firstTurn on a crashed first turn -- retry the task fresh
        continue
    }
    $crashes = 0
    $firstTurn = $false

    # check the meter after the turn
    if (Test-Path $StopFlag) { Log "STOP flag found -> ending run (user interrupt)."; break }
    $u = Get-Usage -TimeoutSec $UsageTimeoutSec
    if (-not $u.Ok) {
        $unreadable++
        Log "usage meter unreadable ($unreadable/$MaxUnreadable)."
        if ($unreadable -ge $MaxUnreadable) {
            Log "Meter unreadable too many times -> stopping (a legitimate stop condition)."
            break
        }
        continue   # re-prompt without a fresh number rather than risk overrun-blind
    }
    $unreadable = 0
    Log ("after turn {0}: {1}" -f $turn, (Bar -pct $u.Session -ceil $SessionCeiling) +
         $(if ($WeeklyCeiling -gt 0) { "  |  week $($u.Week)% of $WeeklyCeiling" } else { "" }))

    if (Ceiling-Reached $u) {
        Log "*** CEILING REACHED (session $($u.Session)% / week $($u.Week)%). Run complete. ***"
        break
    }
}

Log "ENFORCER END."

if ($ShutdownWhenDone) {
    if ($DryRun) {
        Log "[DRYRUN] would power off now (shutdown /s /t 20). Nothing actually happens in dry-run."
    } else {
        Log "shutdownwhendone set -> powering off in 20s (Ctrl+C this window to cancel)."
        try { shutdown /s /t 20 /c "work-until-limit reached ceiling; shutting down." } catch { Log "shutdown failed: $($_.Exception.Message)" }
    }
}
