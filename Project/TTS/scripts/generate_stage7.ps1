$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$bash = Join-Path $projectRoot ".tools\cygwin64\bin\bash.exe"
$cli = Join-Path $projectRoot ".venv-f5\Scripts\f5-tts_infer-cli.exe"
$referenceScript = "/cygdrive/" + $projectRoot.Substring(0, 1).ToLowerInvariant() + ($projectRoot.Substring(2) -replace "\\", "/") + "/scripts/generate_stage7_reference.sh"
$reference = Join-Path $projectRoot "output\comparable\reference\stage7_slt_reference.wav"
$output = Join-Path $projectRoot "output\comparable"
$env:HF_HOME = Join-Path $projectRoot ".cache\huggingface"
$env:TORCH_HOME = Join-Path $projectRoot ".cache\torch"

& $bash $referenceScript
if ($LASTEXITCODE -ne 0) { throw "Could not generate the SLT reference prompt." }

& $cli --model F5TTS_v1_Base `
    --ref_audio $reference `
    --ref_text "This is a short reference sample for the modern synthesis system." `
    --gen_text "I will quote an extract from the reverend gentleman's own journal." `
    --output_dir $output `
    --output_file "stage7_local_f5_prompt.wav" `
    --device cuda `
    --nfe_step 24
if ($LASTEXITCODE -ne 0) { throw "Stage 7 F5-TTS inference failed." }
