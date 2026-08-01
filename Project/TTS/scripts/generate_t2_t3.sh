#!/usr/bin/env bash
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

ROOT="/cygdrive/d/tts-history-build"
TEXT="$ROOT/config/comparison_text.txt"
OUTPUT="$ROOT/output/comparable"
FLITE="$ROOT/.tools/local/flite/bin/flite.exe"
FLITE_HTS="$ROOT/.tools/local/flite_hts_engine/bin/flite_hts_engine.exe"
HTS_VOICE="$ROOT/vendor/hts_voice_cmu_us_arctic_slt-1.06/cmu_us_arctic_slt.htsvoice"

mkdir -p "$OUTPUT"

"$FLITE" -voice kal16 "$TEXT" "$OUTPUT/stage2_author_flite_diphone.wav"
"$FLITE_HTS" -m "$HTS_VOICE" -o "$OUTPUT/stage3_author_hts.wav" "$TEXT"

test -s "$OUTPUT/stage2_author_flite_diphone.wav"
test -s "$OUTPUT/stage3_author_hts.wav"
echo "T2 and T3 generated from the shared text."

