$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$bash = Join-Path $projectRoot ".tools\cygwin64\bin\bash.exe"
$script = "/cygdrive/" + $projectRoot.Substring(0, 1).ToLowerInvariant() + ($projectRoot.Substring(2) -replace "\\", "/") + "/scripts/generate_t2_t3.sh"

& $bash $script
if ($LASTEXITCODE -ne 0) {
    throw "T2/T3 generation failed with exit code $LASTEXITCODE"
}

