$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$python = Join-Path $projectRoot ".venv-f5\Scripts\python.exe"
$cache = Join-Path $projectRoot "cache\stage6"
$env:HF_HOME = Join-Path $projectRoot ".cache\huggingface"
$env:TORCH_HOME = Join-Path $projectRoot ".cache\torch"

if (-not (Test-Path (Join-Path $projectRoot "vendor\soloud"))) {
    & (Join-Path $projectRoot "scripts\setup_sources.ps1")
}
if (-not (Test-Path (Join-Path $projectRoot ".tools\cygwin64\bin\bash.exe"))) {
    & (Join-Path $projectRoot "scripts\setup_historical_toolchain.ps1")
}
if (-not (Test-Path (Join-Path $projectRoot ".tools\local\flite\bin\flite.exe"))) {
    & (Join-Path $projectRoot "scripts\build_historical.ps1")
}
if (-not (Get-ChildItem (Join-Path $projectRoot "vendor\klsyn\klsyn") -Filter "klatt_wrap*.pyd" -ErrorAction SilentlyContinue)) {
    & (Join-Path $projectRoot "scripts\build_klsyn.ps1")
}
& (Join-Path $projectRoot "scripts\build_stage1_frontend.ps1")

if (-not (Test-Path $python)) {
    & (Join-Path $projectRoot "scripts\setup_stage7.ps1")
}
& $python -m pip install "fastapi==0.141.1" "uvicorn==0.35.0" "inflect==7.5.0" "Unidecode==1.4.0"
if ($LASTEXITCODE -ne 0) { throw "Could not install the local web dependencies." }

New-Item -ItemType Directory -Force -Path $cache | Out-Null
$heteronyms = Join-Path $cache "heteronyms"
$cmudict = Join-Path $cache "cmudict-0.7b"
if (-not (Test-Path $heteronyms)) {
    Invoke-WebRequest -UseBasicParsing `
        "https://raw.githubusercontent.com/NVIDIA/NeMo/263a30be71e859cee330e5925332009da3e5efbc/scripts/tts_dataset_files/heteronyms-052722" `
        -OutFile $heteronyms
}
if (-not (Test-Path $cmudict)) {
    Invoke-WebRequest -UseBasicParsing `
        "https://raw.githubusercontent.com/NVIDIA/NeMo/263a30be71e859cee330e5925332009da3e5efbc/scripts/tts_dataset_files/cmudict-0.7b_nv22.08" `
        -OutFile $cmudict
}

& $python (Join-Path $projectRoot "src\download_interactive_models.py")
if ($LASTEXITCODE -ne 0) { throw "Could not download the interactive TTS models." }

$reference = Join-Path $projectRoot "output\comparable\reference\stage7_slt_reference.wav"
if (-not (Test-Path $reference)) {
    $referenceText = Join-Path $projectRoot "cache\stage7_reference.txt"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $reference) | Out-Null
    Set-Content -LiteralPath $referenceText -Encoding ascii `
        -Value "This is a short reference sample for the modern synthesis system."
    $env:PATH = (Join-Path $projectRoot ".tools\cygwin64\bin") + ";" + $env:PATH
    & (Join-Path $projectRoot ".tools\local\flite_hts_engine\bin\flite_hts_engine.exe") `
        -m (Join-Path $projectRoot "vendor\hts_voice_cmu_us_arctic_slt-1.06\cmu_us_arctic_slt.htsvoice") `
        -o $reference $referenceText
    if ($LASTEXITCODE -ne 0) { throw "Could not generate the Stage 7 reference voice." }
}

Write-Output "Seven-stage interactive TTS setup is complete. Run .\serve.ps1"
