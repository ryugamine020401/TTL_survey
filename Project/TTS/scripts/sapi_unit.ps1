param(
    [Parameter(Mandatory = $true)][string]$Text,
    [Parameter(Mandatory = $true)][string]$Output,
    [string]$Voice = "Microsoft Zira Desktop"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Speech

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $available = $synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
    if ($available -contains $Voice) {
        $synth.SelectVoice($Voice)
    }
    $synth.Rate = -1
    $synth.Volume = 100
    $synth.SetOutputToWaveFile($Output)
    $synth.Speak($Text)
}
finally {
    $synth.Dispose()
}

