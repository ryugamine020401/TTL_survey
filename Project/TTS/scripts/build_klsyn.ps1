$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$cygwinBin = Join-Path $projectRoot ".tools\cygwin64\bin"
$gcc = Join-Path $cygwinBin "x86_64-w64-mingw32-gcc.exe"
$sourceDir = Join-Path $projectRoot "vendor\klsyn\klsyn"
$source = Join-Path $sourceDir "klatt_wrap.c"
$output = Join-Path $sourceDir "klatt_wrap.cp311-win_amd64.pyd"

if (-not (Test-Path $venvPython)) {
    py -3.11 -m venv (Join-Path $projectRoot ".venv")
}

$pythonHome = & $venvPython -c "import sys; print(sys.base_prefix)"
$pythonHome = $pythonHome.Trim()
$pythonInclude = Join-Path $pythonHome "Include"
$pythonLib = Join-Path $pythonHome "libs"

& $venvPython -m pip install "numpy>=2,<3" "scipy>=1.14,<2" "cython>=3,<4" "xlrd>=2,<3" "xlwt>=1,<2"
if ($LASTEXITCODE -ne 0) { throw "Could not install KLSYN Python dependencies." }

if (-not (Test-Path $gcc)) {
    throw "MinGW cross-compiler is missing. Run scripts/setup_historical_toolchain.ps1 first."
}

$numpyInclude = & $venvPython -c "import numpy; print(numpy.get_include())"
if ($LASTEXITCODE -ne 0) { throw "Could not locate NumPy headers." }

if (-not (Test-Path $source)) {
    Push-Location (Join-Path $projectRoot "vendor\klsyn")
    try {
        & $venvPython -m cython -3 "klsyn\klatt_wrap.pyx" -o "klsyn\klatt_wrap.c"
    } finally {
        Pop-Location
    }
    if ($LASTEXITCODE -ne 0) { throw "Cython could not generate klatt_wrap.c." }
}

$env:PATH = $cygwinBin + ";" + $env:PATH
Push-Location $sourceDir
try {
    & $gcc -shared -O2 -DMS_WIN64 "-I$pythonInclude" "-I$numpyInclude" `
        "klatt_wrap.c" "-L$pythonLib" -lpython311 -o $output
} finally {
    Pop-Location
}
if ($LASTEXITCODE -ne 0) { throw "KLSYN extension build failed." }

$env:PYTHONPATH = Join-Path $projectRoot "vendor\klsyn"
& $venvPython -c "import klsyn.klatt_wrap as k; print('KLSYN ready:', k.__file__)"
if ($LASTEXITCODE -ne 0) { throw "The compiled KLSYN extension could not be imported." }
