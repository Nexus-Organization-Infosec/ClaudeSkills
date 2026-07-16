param(
    [string]$Src = (Get-Location).Path,
    [string]$BackupRoot = ""
)

# ---------------------------------------------------------------
#  Backs up a project into  <BackupRoot>\<PROJECT>_<timestamp>\
#  containing infos.txt plus a full copy of the project tree.
#  Default BackupRoot is a "BACKUP" folder next to the project
#  (its parent dir), so the copy never recurses into itself.
# ---------------------------------------------------------------

$ErrorActionPreference = "Stop"

$Src = (Resolve-Path $Src).Path
$name = Split-Path $Src -Leaf
if ([string]::IsNullOrWhiteSpace($BackupRoot)) {
    $BackupRoot = Join-Path (Split-Path $Src -Parent) "BACKUP"
}
$ts   = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$dest = Join-Path $BackupRoot ("{0}_{1}" -f $name, $ts)
New-Item -ItemType Directory -Force -Path $dest | Out-Null

Write-Output "Backing up:"
Write-Output "  from : $Src"
Write-Output "  to   : $dest"

# Copy the whole tree. /R:2 /W:1 so locked files (e.g. a browser profile)
# fail fast instead of hanging on robocopy's million-retry default.
# /XD excludes the backup root itself, in case it lives inside the project.
robocopy "$Src" "$dest" /E /R:2 /W:1 /XD "$BackupRoot" /NFL /NDL /NJH /NJS /NP /NC /NS | Out-Null
$rc = $LASTEXITCODE   # robocopy: 0-7 = success, 8+ = real failure

$files  = Get-ChildItem -Path $dest -Recurse -File -Force -ErrorAction SilentlyContinue
$count  = ($files | Measure-Object).Count
$sizeMB = if ($count -gt 0) { [math]::Round((($files | Measure-Object Length -Sum).Sum) / 1MB, 2) } else { 0 }

# Git info, if the source is a repo.
$gitInfo = "Not a git repository"
Push-Location $Src
try {
    $branch = (git rev-parse --abbrev-ref HEAD 2>$null)
    if ($branch) {
        $commit    = (git log -1 --format="%h  %s  (%ci)" 2>$null)
        $porcelain = (git status --porcelain 2>$null)
        if ($porcelain) { $tree = "dirty (uncommitted changes present)" } else { $tree = "clean" }
        $gitInfo = "Branch      : $branch`r`nLast commit : $commit`r`nWorking tree: $tree"
    }
} catch { }
Pop-Location

$warn = if ($rc -ge 8) { "`r`nWARNING: robocopy reported errors (code $rc) - some files may not have copied (locked/in use)." } else { "" }

$info = @"
PROJECT BACKUP
==============
Project name : $name
Backed up at : $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  [$([System.TimeZoneInfo]::Local.Id)]
Source path  : $Src
Backup path  : $dest

Machine      : $env:COMPUTERNAME
User         : $env:USERNAME
OS           : $([System.Environment]::OSVersion.VersionString)

Files copied : $count
Total size   : $sizeMB MB

Git
---
$gitInfo
$warn
"@

Set-Content -Path (Join-Path $dest "infos.txt") -Value $info -Encoding UTF8

Write-Output ""
Write-Output "Backup complete: $count files, $sizeMB MB"
Write-Output "  $dest"
if ($rc -ge 8) { Write-Output "  (robocopy code $rc - check infos.txt, some files may be locked)" }
