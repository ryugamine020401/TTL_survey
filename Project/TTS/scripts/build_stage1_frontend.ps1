$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$sourceRoot = Join-Path $projectRoot "vendor\soloud"
$speechRoot = Join-Path $sourceRoot "src\audiosource\speech"
$patch = Join-Path $projectRoot "patches\soloud-frame-dump.patch"
$adapter = Join-Path $projectRoot "src\native\stage1_rule_frontend.cpp"
$outputDir = Join-Path $projectRoot ".tools\local\stage1"
$bash = Join-Path $projectRoot ".tools\cygwin64\bin\bash.exe"

if (-not (Test-Path $speechRoot)) {
    throw "Missing SoLoud source. Run .\scripts\setup_sources.ps1 first."
}
if (-not (Select-String -LiteralPath (Join-Path $speechRoot "klatt.cpp") -Pattern "gFrameDump" -Quiet)) {
    git -C $sourceRoot apply $patch
    if ($LASTEXITCODE -ne 0) { throw "Could not apply the Stage 1 frontend patch." }
}

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

function Convert-ToCygwinPath([string]$Path) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    $drive = $resolved.Substring(0, 1).ToLowerInvariant()
    return "/cygdrive/$drive/" + ($resolved.Substring(3) -replace "\\", "/")
}

$speechPosix = Convert-ToCygwinPath $speechRoot
$adapterPosix = Convert-ToCygwinPath $adapter
$outputPosix = Convert-ToCygwinPath (Join-Path $outputDir "stage1_rule_frontend.exe")

& $bash -lc "cd '$speechPosix' && g++ -O2 -std=c++11 -I. '$adapterPosix' darray.cpp resonator.cpp klatt.cpp tts.cpp -o '$outputPosix'"
if ($LASTEXITCODE -ne 0) { throw "Stage 1 rule frontend compilation failed." }

Write-Output "Stage 1 rule frontend is ready: $outputDir"
