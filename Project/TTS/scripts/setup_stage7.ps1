$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venv = Join-Path $projectRoot ".venv-f5"
$python = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path $python)) {
    py -3.11 -m venv $venv
}

& $python -m pip install --upgrade pip
& $python -m pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 `
    --extra-index-url https://download.pytorch.org/whl/cu128
& $python -m pip install f5-tts==1.1.22

& $python -c "import torch; assert torch.cuda.is_available(); print(torch.cuda.get_device_name(0))"
if ($LASTEXITCODE -ne 0) { throw "Stage 7 CUDA environment is not ready." }
