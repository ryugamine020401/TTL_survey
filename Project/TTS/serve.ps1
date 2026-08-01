param(
    [int]$Port = 8000,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot ".venv-f5\Scripts\python.exe"
$app = Join-Path $projectRoot "src\local_app.py"

if (-not (Test-Path $python)) {
    throw "The interactive environment is missing. Run .\scripts\setup_interactive.ps1 first."
}

$arguments = @($app, "--host", "127.0.0.1", "--port", "$Port")
if ($NoBrowser) { $arguments += "--no-browser" }

Write-Output "Local TTS website: http://127.0.0.1:$Port"
Write-Output "Press Ctrl+C to stop the server."
& $python @arguments
