$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

& (Join-Path $projectRoot "scripts\generate_stage1.ps1")
& (Join-Path $projectRoot "scripts\generate_t2_t3.ps1")
& (Join-Path $projectRoot "scripts\generate_stage7.ps1")

$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$arguments = @(Join-Path $projectRoot "src\assemble_comparison.py")
if ($args -contains "--refresh") { $arguments += "--refresh" }
& $python @arguments
if ($LASTEXITCODE -ne 0) { throw "Final comparison assembly failed." }
