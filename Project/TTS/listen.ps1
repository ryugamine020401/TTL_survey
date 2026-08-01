param(
    [int]$Port = 8000,
    [switch]$NoBrowser,
    [switch]$NoWait
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot ".venv-f5\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "The interactive environment is missing. Run .\scripts\setup_interactive.ps1 first."
}

if (-not $NoWait) {
    $serveArguments = @("-Port", "$Port")
    if ($NoBrowser) { $serveArguments += "-NoBrowser" }
    & (Join-Path $projectRoot "serve.ps1") @serveArguments
    exit $LASTEXITCODE
}

$server = Start-Process -FilePath $python `
    -ArgumentList "local_app.py", "--host", "127.0.0.1", "--port", "$Port", "--no-browser" `
    -WorkingDirectory (Join-Path $projectRoot "src") `
    -WindowStyle Hidden `
    -PassThru

try {
    $url = "http://127.0.0.1:$Port"
    $ready = $false
    foreach ($attempt in 1..30) {
        Start-Sleep -Milliseconds 250
        try {
            Invoke-WebRequest -UseBasicParsing "$url/api/health" | Out-Null
            $ready = $true
            break
        } catch {
            if ($server.HasExited) { break }
        }
    }
    if (-not $ready) { throw "The local TTS server failed to start." }
    Write-Output "Local TTS server test passed: $url"
} finally {
    if (-not $server.HasExited) { Stop-Process -Id $server.Id }
}
