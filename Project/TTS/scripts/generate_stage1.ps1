$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$env:PYTHONPATH = (Join-Path $projectRoot "vendor\klsyn") + ";" + (Join-Path $projectRoot "src")

& $python (Join-Path $projectRoot "src\generate_stage1_klsyn.py")
if ($LASTEXITCODE -ne 0) {
    throw "Stage 1 KLSYN generation failed with exit code $LASTEXITCODE"
}
