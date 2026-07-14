param(
    [string]$Title = "Claude Code",
    [string]$Message = "All tasks finished - shutting down in 60 seconds. Run 'shutdown -a' to cancel."
)

$ErrorActionPreference = "Stop"

# Primary: native WinRT toast — the real Windows notification popup (bottom-right,
# also lands in the Notification Center). Requires Windows PowerShell 5.1, which is
# why the skill invokes this script via powershell.exe rather than pwsh.
try {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $texts = $xml.GetElementsByTagName("text")
    $null = $texts.Item(0).AppendChild($xml.CreateTextNode($Title))
    $null = $texts.Item(1).AppendChild($xml.CreateTextNode($Message))
    $toast = New-Object Windows.UI.Notifications.ToastNotification($xml)

    # Send the toast under the Claude desktop app's identity so the popup shows
    # Claude's name and icon. Look it up dynamically (survives app updates),
    # fall back to the known AppID, then to PowerShell's as a last resort.
    $appId = $null
    try {
        $appId = (Get-StartApps | Where-Object { $_.Name -eq 'Claude' } | Select-Object -First 1).AppID
    } catch { }
    if (-not $appId) { $appId = 'Claude_pzs8sxrjxfjjc!Claude' }

    try {
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show($toast)
    } catch {
        $appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show($toast)
    }
    Start-Sleep -Seconds 1
    Write-Output "toast shown (winrt)"
    exit 0
} catch { }

# Fallback: tray balloon tip, which Windows 10/11 also renders as a toast.
# The process must stay alive while the balloon is visible, hence the sleep.
try {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    $ni = New-Object System.Windows.Forms.NotifyIcon
    $ni.Icon = [System.Drawing.SystemIcons]::Information
    $ni.BalloonTipTitle = $Title
    $ni.BalloonTipText = $Message
    $ni.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
    $ni.Visible = $true
    $ni.ShowBalloonTip(10000)
    Start-Sleep -Seconds 6
    $ni.Dispose()
    Write-Output "toast shown (balloon fallback)"
    exit 0
} catch {
    Write-Output "notification failed: $_"
    exit 1
}
