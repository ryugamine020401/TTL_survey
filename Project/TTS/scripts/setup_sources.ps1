$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$vendor = Join-Path $projectRoot "vendor"
$downloads = Join-Path $vendor "downloads"
New-Item -ItemType Directory -Force -Path $vendor, $downloads | Out-Null

function Get-GitSource {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$Revision,
        [Parameter(Mandatory = $true)][string]$Destination
    )
    if (Test-Path $Destination) {
        Write-Output "Using existing source: $Destination"
        return
    }
    git clone $Url $Destination
    if ($LASTEXITCODE -ne 0) { throw "Could not clone $Url" }
    git -C $Destination checkout --detach $Revision
    if ($LASTEXITCODE -ne 0) { throw "Could not select revision $Revision" }
}

function Get-TarSource {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$ArchiveName,
        [Parameter(Mandatory = $true)][string]$DirectoryName
    )
    $archive = Join-Path $downloads $ArchiveName
    $destination = Join-Path $vendor $DirectoryName
    if (Test-Path $destination) {
        Write-Output "Using existing source: $destination"
        return
    }
    if (-not (Test-Path $archive)) {
        Invoke-WebRequest -UseBasicParsing $Url -OutFile $archive
    }
    tar -xzf $archive -C $vendor
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $destination)) {
        throw "Could not extract $ArchiveName"
    }
}

Get-GitSource `
    -Url "https://github.com/rsprouse/klsyn.git" `
    -Revision "30ea63c0480bdea7963568a9ffa2b0a3e5cd512b" `
    -Destination (Join-Path $vendor "klsyn")

Get-GitSource `
    -Url "https://github.com/festvox/flite.git" `
    -Revision "6c9f20dc915b17f5619340069889db0aa007fcdc" `
    -Destination (Join-Path $vendor "flite")

Get-GitSource `
    -Url "https://github.com/jarikomppa/soloud.git" `
    -Revision "e82fd32c1f62183922f08c14c814a02b58db1873" `
    -Destination (Join-Path $vendor "soloud")

Get-TarSource `
    -Url "https://downloads.sourceforge.net/hts-engine/hts_engine_API-1.10.tar.gz" `
    -ArchiveName "hts_engine_API-1.10.tar.gz" `
    -DirectoryName "hts_engine_API-1.10"

Get-TarSource `
    -Url "https://downloads.sourceforge.net/hts-engine/flite%2Bhts_engine-1.07.tar.gz" `
    -ArchiveName "flite+hts_engine-1.07.tar.gz" `
    -DirectoryName "flite+hts_engine-1.07"

Get-TarSource `
    -Url "https://downloads.sourceforge.net/hts-engine/hts_voice_cmu_us_arctic_slt-1.06.tar.gz" `
    -ArchiveName "hts_voice_cmu_us_arctic_slt-1.06.tar.gz" `
    -DirectoryName "hts_voice_cmu_us_arctic_slt-1.06"

Write-Output "Historical TTS sources are ready."
