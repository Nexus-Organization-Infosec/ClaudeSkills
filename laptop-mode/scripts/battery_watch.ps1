param(
    [string]$StatusFile = "$env:TEMP\laptop_battery_status.txt",
    [int]$IntervalSeconds = 20
)

# Background battery watcher for the /laptop-mode skill.
# Runs FOREVER (until Claude stops it) and writes the current battery state to a
# status file every few seconds, atomically. Claude launches this in the
# background when the laptop is on AC (BatteryStatus 2), then reads the status
# file with an instant non-blocking peek at each work boundary — so it never
# inline-polls the battery and never blocks. When ONAC flips 1 -> 0 (unplugged)
# or the charge starts falling, Claude switches to active threshold monitoring.
#
# Status file fields:
#   CHARGE   EstimatedChargeRemaining (0-100, or -1 if unreadable)
#   STATUS   raw Win32_Battery BatteryStatus (2 = on AC, 1 = discharging)
#   ONAC     1 if on AC (STATUS=2), 0 if discharging, -1 if unknown
#   UPDATED  timestamp

$ErrorActionPreference = "Continue"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

function Write-State {
    param([int]$Charge, [int]$Status, [int]$OnAc, [string]$Note)
    $lines = @(
        "CHARGE=$Charge",
        "STATUS=$Status",
        "ONAC=$OnAc",
        "NOTE=$Note",
        "UPDATED=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    )
    $tmp = "$StatusFile.tmp"
    Set-Content -Path $tmp -Value ($lines -join "`r`n") -Encoding UTF8
    Move-Item -Path $tmp -Destination $StatusFile -Force
}

while ($true) {
    try {
        $b = Get-CimInstance Win32_Battery -ErrorAction Stop | Select-Object -First 1
        if ($b) {
            $charge = [int]$b.EstimatedChargeRemaining
            $status = [int]$b.BatteryStatus
            $onac = if ($status -eq 2) { 1 } else { 0 }
            Write-State -Charge $charge -Status $status -OnAc $onac -Note "ok"
        } else {
            Write-State -Charge -1 -Status -1 -OnAc -1 -Note "no battery object (desktop/VM?)"
        }
    } catch {
        Write-State -Charge -1 -Status -1 -OnAc -1 -Note "read error"
    }
    Start-Sleep -Seconds $IntervalSeconds
}
