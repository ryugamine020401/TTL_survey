$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$tools = Join-Path $projectRoot ".tools"
$cache = Join-Path $tools "cygwin-cache"
$cygwinRoot = Join-Path $tools "cygwin64"
$setup = Join-Path $tools "setup-x86_64.exe"

New-Item -ItemType Directory -Force -Path $tools, $cache, $cygwinRoot | Out-Null
if (-not (Test-Path $setup)) {
    Invoke-WebRequest -UseBasicParsing "https://cygwin.com/setup-x86_64.exe" -OutFile $setup
}

& $setup -q -B -n -N -d -R $cygwinRoot -l $cache `
    -s "https://mirrors.kernel.org/sourceware/cygwin/" `
    -P gcc-core,gcc-g++,mingw64-x86_64-gcc-core,mingw64-x86_64-gcc-g++,make,libunistring5,tar,bzip2,gzip,wget,git

if (-not (Test-Path (Join-Path $cygwinRoot "bin\bash.exe"))) {
    throw "Cygwin installation did not produce bash.exe"
}

Write-Output "Project-local Cygwin toolchain is ready: $cygwinRoot"
