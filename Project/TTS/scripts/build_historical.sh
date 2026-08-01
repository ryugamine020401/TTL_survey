#!/usr/bin/env bash
set -euxo pipefail

# When Cygwin bash is launched from PowerShell it inherits the Windows PATH.
export PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

if [[ -d /cygdrive/d/tts-history-build ]]; then
  # The official Makefiles do not quote install prefixes. A project-local
  # Windows junction provides the same files through a no-space build path.
  ROOT="/cygdrive/d/tts-history-build"
else
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi
VENDOR="$ROOT/vendor"
PREFIX="$ROOT/.tools/local"
JOBS="${NUMBER_OF_PROCESSORS:-4}"

mkdir -p "$PREFIX"

echo "[T2] Building Alan W. Black's official Flite source"
cd "$VENDOR/flite"
# The official Windows checkout stores executable build scripts with CRLF.
# Cygwin's shell requires LF; this changes line endings only, not program logic.
find . -path './.git' -prune -o -type f -perm /111 -exec sed -i 's/\r$//' {} +
./configure --prefix="$PREFIX/flite"
# Flite's generated voice list has an undeclared dependency; the first build
# must be serial or parallel make can race before flite_voice_list.c exists.
make
make install

echo "[T3] Building the HTS Working Group's official hts_engine API"
cd "$VENDOR/hts_engine_API-1.10"
if [[ ! -f config.status ]]; then
  ./configure --prefix="$PREFIX/hts_engine"
fi
make -j"$JOBS"
make install

echo "[T3] Building the HTS Working Group's official Flite+hts_engine"
cd "$VENDOR/flite+hts_engine-1.07"
if [[ ! -f config.status ]]; then
  ./configure \
    --prefix="$PREFIX/flite_hts_engine" \
    --with-hts-engine-header-path="$PREFIX/hts_engine/include" \
    --with-hts-engine-library-path="$PREFIX/hts_engine/lib"
fi
make -j"$JOBS"
make install

echo "Historical engines built successfully."
echo "Flite: $PREFIX/flite/bin/flite.exe"
echo "Flite+HTS: $PREFIX/flite_hts_engine/bin/flite_hts_engine.exe"
