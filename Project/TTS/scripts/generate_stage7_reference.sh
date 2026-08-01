#!/usr/bin/env bash
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

ROOT="/cygdrive/d/tts-history-build"
TEXT="$ROOT/config/stage7_reference_text.txt"
OUTPUT="$ROOT/output/comparable/reference"
FLITE_HTS="$ROOT/.tools/local/flite_hts_engine/bin/flite_hts_engine.exe"
HTS_VOICE="$ROOT/vendor/hts_voice_cmu_us_arctic_slt-1.06/cmu_us_arctic_slt.htsvoice"

mkdir -p "$OUTPUT"
"$FLITE_HTS" -m "$HTS_VOICE" -o "$OUTPUT/stage7_slt_reference.wav" "$TEXT"
test -s "$OUTPUT/stage7_slt_reference.wav"
