$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$projectRoot\scripts\generate_comparable.ps1" @args
