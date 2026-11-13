param(
    [string]$TargetDir = "$env:USERPROFILE\.gemini\config\skills"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

foreach ($skill in @("informs-writing", "informs-zh-review")) {
    $src = Join-Path $RepoRoot $skill
    $dst = Join-Path $TargetDir $skill
    if (Test-Path $dst) {
        Remove-Item $dst -Recurse -Force
    }
    Copy-Item -Path $src -Destination $dst -Recurse -Force
    Get-ChildItem $dst -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "Installed $skill -> $dst"
}
