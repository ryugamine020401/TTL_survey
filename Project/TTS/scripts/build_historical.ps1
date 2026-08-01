$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$bash = Join-Path $projectRoot ".tools\cygwin64\bin\bash.exe"
$script = "/cygdrive/" + $projectRoot.Substring(0, 1).ToLowerInvariant() + ($projectRoot.Substring(2) -replace "\\", "/") + "/scripts/build_historical.sh"
$shortBuildPath = "D:\tts-history-build"

if (-not (Test-Path $shortBuildPath)) {
    New-Item -ItemType Junction -Path $shortBuildPath -Target $projectRoot | Out-Null
}

if (-not (Test-Path $bash)) {
    throw "Cygwin toolchain is missing. Run scripts/setup_historical_toolchain.ps1 first."
}

& $bash $script
if ($LASTEXITCODE -ne 0) {
    throw "Historical engine build failed with exit code $LASTEXITCODE"
}
