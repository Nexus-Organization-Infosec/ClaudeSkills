param(
    [int]$Threshold = 80,          # session ceiling (0 = don't bound the session limit)
    [int]$WeeklyThreshold = 0,     # weekly ceiling (0 = don't bound the weekly limit)
    [string]$StatusFile = "$env:TEMP\claude_work_until_limit_status.txt",
    [int]$IntervalSeconds = 300,
    [int]$PerCallTimeoutSeconds = 120,
    [switch]$Once   # take a single fresh reading, write the status file, and exit
)

# Background usage monitor for the work-until-limit skill.
# Repeatedly asks the Claude CLI for current usage, parses a percentage,
# renders a text bar, and writes a status file the skill polls between work
# chunks. When usage >= Threshold it writes STOP=1 and exits (so it stops
# burning quota once the ceiling is reached).
#
# NOTE: `claude -p "/usage"` is itself a CLI call and may consume quota, so the
# default poll interval is deliberately slow (5 min). Faster polling means the
# monitor eats more of the very budget it is watching.

$ErrorActionPreference = "Continue"

function Get-UsageText {
    param([int]$TimeoutSec)
    # Run the CLI in a job so a hung call can't freeze the monitor forever.
    # Set UTF-8 inside the job so the ·/— characters in the usage text aren't mangled.
    $job = Start-Job -ScriptBlock {
        try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
        claude -p "/usage" 2>&1 | Out-String
    }
    if (Wait-Job $job -Timeout $TimeoutSec) {
        $out = Receive-Job $job
        Remove-Job $job -Force
        return $out
    } else {
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -Force -ErrorAction SilentlyContinue
        return $null
    }
}

function Write-Status {
    param([string]$Status, [int]$Percent, [int]$Session, [int]$Week, [int]$Stop, [string]$Bar, [string]$Raw,
          [int]$SessionResetMin = -1, [int]$WeekResetMin = -1, [string]$SessionReset = "", [string]$WeekReset = "")
    $lines = @(
        "STATUS=$Status",
        "PERCENT=$Percent",
        "SESSION=$Session",
        "WEEK=$Week",
        "THRESHOLD=$Threshold",
        "WEEKLYTHRESHOLD=$WeeklyThreshold",
        "SESSION_RESET_MIN=$SessionResetMin",
        "WEEK_RESET_MIN=$WeekResetMin",
        "SESSION_RESET=$SessionReset",
        "WEEK_RESET=$WeekReset",
        "STOP=$Stop",
        "BAR=$Bar",
        "UPDATED=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
        "---RAW---",
        $Raw
    )
    # Write atomically via a temp file + move so the skill never reads a half-written file.
    $tmp = "$StatusFile.tmp"
    Set-Content -Path $tmp -Value ($lines -join "`r`n") -Encoding UTF8
    Move-Item -Path $tmp -Destination $StatusFile -Force
}

function Get-MinutesUntil {
    # Parse a reset time like "Jul 12, 4:29am" or "Jul 14, 5pm" and return whole
    # minutes from now. Returns -1 if unparseable. Uses ParseExact with uppercased
    # AM/PM — lenient [datetime]::Parse silently mis-reads this format (it ignores a
    # lowercase "pm" and can land on the wrong year). The /usage lines carry the date,
    # so the result is right for both the soon (session) and days-away (weekly) resets.
    param([string]$s)
    if ([string]::IsNullOrWhiteSpace($s)) { return -1 }
    $ci = [System.Globalization.CultureInfo]::GetCultureInfo('en-US')
    $t = [regex]::Replace($s.Trim(), '(?i)\s*(am|pm)', { param($m) $m.Groups[1].Value.ToUpper() })
    $formats = @('MMM d, h:mmtt','MMM d, htt','MMM dd, h:mmtt','MMM dd, htt')
    $dt = [datetime]::MinValue; $ok = $false
    foreach ($f in $formats) {
        try { $dt = [datetime]::ParseExact($t, $f, $ci, [System.Globalization.DateTimeStyles]::AssumeLocal); $ok = $true; break } catch {}
    }
    if (-not $ok) { return -1 }
    $now = Get-Date
    if ($dt -lt $now.AddHours(-1)) { $dt = $dt.AddYears(1) }  # year-boundary guard
    return [int][math]::Round(($dt - $now).TotalMinutes)
}

function New-Bar {
    param([int]$Percent)
    $cells = 20
    $filled = [math]::Round($Percent / 100.0 * $cells)
    if ($filled -lt 0) { $filled = 0 }
    if ($filled -gt $cells) { $filled = $cells }
    return "[" + ("#" * $filled) + ("-" * ($cells - $filled)) + "] $Percent%"
}

while ($true) {
    $raw = Get-UsageText -TimeoutSec $PerCallTimeoutSeconds

    if ($null -eq $raw -or $raw.Trim() -eq "") {
        Write-Status -Status "TIMEOUT" -Percent 0 -Session -1 -Week -1 -Stop 0 -Bar "(no response)" -Raw "CLI call timed out or returned nothing."
    }
    else {
        # Parse ONLY the two limit lines, e.g.:
        #   "Current session: 71% used ..."
        #   "Current week (all models): 61% used ..."
        # The output also contains breakdown stats ("96% of your usage was at >150k
        # context", "Top skills: /x 1%") — those must NOT be mistaken for the limit,
        # so a naive max-of-all-percents is wrong. Match the labelled lines only.
        $session = -1
        $week = -1
        $ms = [regex]::Match($raw, 'Current session:\s*(\d{1,3})\s*%')
        if ($ms.Success) { $session = [int]$ms.Groups[1].Value }
        $mw = [regex]::Match($raw, 'Current week[^:\r\n]*:\s*(\d{1,3})\s*%')
        if ($mw.Success) { $week = [int]$mw.Groups[1].Value }

        # Reset times: "... resets Jul 12, 4:29am (Europe/Berlin)" on each limit line.
        $sessReset = ""; $weekReset = ""
        $msr = [regex]::Match($raw, 'Current session:[^\r\n]*?resets\s*([^\(\r\n]+?)\s*\(')
        if ($msr.Success) { $sessReset = $msr.Groups[1].Value.Trim() }
        $mwr = [regex]::Match($raw, 'Current week[^\r\n]*?resets\s*([^\(\r\n]+?)\s*\(')
        if ($mwr.Success) { $weekReset = $mwr.Groups[1].Value.Trim() }
        $sessMin = Get-MinutesUntil $sessReset
        $weekMin = Get-MinutesUntil $weekReset

        $cands = @()
        if ($session -ge 0) { $cands += $session }
        if ($week -ge 0) { $cands += $week }

        if ($cands.Count -gt 0) {
            $used = ($cands | Measure-Object -Maximum).Maximum
            $bar = New-Bar -Percent $used
            # Stop if EITHER bounded limit reaches its own ceiling. A threshold of 0
            # means that limit isn't bounded (e.g. weekly-only runs leave session at 0).
            $stop = 0
            if ($Threshold -gt 0 -and $session -ge 0 -and $session -ge $Threshold) { $stop = 1 }
            if ($WeeklyThreshold -gt 0 -and $week -ge 0 -and $week -ge $WeeklyThreshold) { $stop = 1 }
            Write-Status -Status "OK" -Percent $used -Session $session -Week $week -Stop $stop -Bar $bar -Raw $raw `
                -SessionResetMin $sessMin -WeekResetMin $weekMin -SessionReset $sessReset -WeekReset $weekReset
            if ($stop -eq 1) { break }   # ceiling reached: stop polling, stop spending quota
        }
        else {
            # CLI answered but neither limit line was found — don't invent a number.
            Write-Status -Status "UNKNOWN" -Percent 0 -Session -1 -Week -1 -Stop 0 -Bar "(limit lines not found)" -Raw $raw
        }
    }

    if ($Once) { break }   # single-reading mode: one check and out
    Start-Sleep -Seconds $IntervalSeconds
}
