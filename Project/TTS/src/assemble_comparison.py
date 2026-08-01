from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly

from audio_utils import inspect_wav
from official_references import REFERENCES, download
from phonemes import DEMO_TEXT


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "output" / "comparable"
PLAYBACK_DIR = RAW_DIR / "playback"
TARGET_SAMPLE_RATE = 24_000
TARGET_RMS = 0.065

RAW_FILES = {
    1: "stage1_author_klsyn.wav",
    2: "stage2_author_flite_diphone.wav",
    3: "stage3_author_hts.wav",
    4: "stage4_official_merlin.wav",
    5: "stage5_official_tacotron2.wav",
    6: "stage6_official_fastspeech.wav",
    7: "stage7_local_f5_prompt.wav",
}

PLAYBACK_FILES = {
    stage: f"stage{stage}_comparison.wav" for stage in range(1, 8)
}


def _load_mono(path: Path) -> tuple[int, np.ndarray]:
    sample_rate, data = wavfile.read(path)
    if data.ndim == 2:
        data = data.astype(np.float64).mean(axis=1)
    if np.issubdtype(data.dtype, np.integer):
        maximum = float(max(abs(np.iinfo(data.dtype).min), np.iinfo(data.dtype).max))
        audio = data.astype(np.float64) / maximum
    else:
        audio = data.astype(np.float64)
    return int(sample_rate), audio


def make_playback_copy(source: Path, destination: Path) -> None:
    sample_rate, audio = _load_mono(source)
    if sample_rate != TARGET_SAMPLE_RATE:
        divisor = math.gcd(sample_rate, TARGET_SAMPLE_RATE)
        audio = resample_poly(audio, TARGET_SAMPLE_RATE // divisor, sample_rate // divisor)
    rms = float(np.sqrt(np.mean(audio * audio))) if audio.size else 0.0
    if rms <= 1e-8:
        raise RuntimeError(f"Silent source audio: {source}")
    gain = TARGET_RMS / rms
    peak = float(np.max(np.abs(audio)))
    if peak * gain > 0.95:
        gain = 0.95 / peak
    audio = np.clip(audio * gain, -1.0, 1.0)
    pcm = np.round(audio * 32767.0).astype(np.int16)
    destination.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(destination, TARGET_SAMPLE_RATE, pcm)


def materialize_official_middle_stages(refresh: bool) -> None:
    for stage in (4, 5, 6):
        source = PROJECT_ROOT / "output" / str(REFERENCES[stage]["filename"])
        target = RAW_DIR / RAW_FILES[stage]
        if refresh or not source.exists():
            download(str(REFERENCES[stage]["url"]), source)
        if refresh or not target.exists() or source.read_bytes() != target.read_bytes():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def build_manifest() -> dict[str, object]:
    metadata = {
        1: {
            "era": "Rule/formant synthesis",
            "model": "Dennis Klatt KLSYN C core via rsprouse/klsyn",
            "provenance": "local_original_author_core",
            "source_code": "https://github.com/rsprouse/klsyn",
            "source_revision": "30ea63c0480bdea7963568a9ffa2b0a3e5cd512b",
            "rule_frontend": "rsynth-derived element controls from SoLoud",
            "rule_frontend_source": "https://github.com/jarikomppa/soloud/tree/e82fd32c1f62183922f08c14c814a02b58db1873/src/audiosource/speech",
            "claim_limit": "The waveform core is Klatt's original code. The fixed-sentence acoustic controls use later rsynth-derived rules, not the unavailable complete MITalk front end. KLSYN has no learned speaker identity.",
        },
        2: {
            "era": "Concatenative synthesis",
            "model": "FestVox Flite kal16 diphone voice",
            "provenance": "local_author_official_code",
            "source_code": "https://github.com/festvox/flite",
            "source_revision": "6c9f20dc915b17f5619340069889db0aa007fcdc",
            "claim_limit": "Alan W. Black's official Flite implementation is used. Its kal16 diphone voice demonstrates concatenation, but is not the unreleased full Hunt & Black 1996 unit-selection experiment package.",
        },
        3: {
            "era": "HMM-based statistical parametric synthesis",
            "model": "Flite+hts_engine 1.07 with CMU ARCTIC SLT voice 1.06",
            "provenance": "local_official_team_code_and_voice",
            "source_code": "https://hts-engine.sourceforge.net/",
            "source_revision": "flite+hts_engine 1.07 / hts_engine API 1.10",
            "claim_limit": "Official HTS Working Group engine and distributed SLT voice; the project did not retrain the acoustic model.",
        },
        4: {
            "era": "Neural statistical parametric synthesis",
            "model": "Merlin neural SPSS",
            "provenance": "official_author_demo_output",
            "source_code": "https://github.com/CSTR-Edinburgh/merlin",
            "source_audio": REFERENCES[4]["url"],
            "source_page": REFERENCES[4]["page"],
            "claim_limit": "Author-published output for the exact test sentence; inference is not rerun locally.",
        },
        5: {
            "era": "Autoregressive end-to-end TTS",
            "model": "Tacotron 2",
            "provenance": "official_author_demo_output",
            "source_audio": REFERENCES[5]["url"],
            "source_page": REFERENCES[5]["page"],
            "claim_limit": "Author-published output for the exact test sentence; inference is not rerun locally.",
        },
        6: {
            "era": "Parallel/non-autoregressive TTS",
            "model": "FastSpeech",
            "provenance": "official_author_demo_output",
            "source_audio": REFERENCES[6]["url"],
            "source_page": REFERENCES[6]["page"],
            "claim_limit": "Author-published output for the exact test sentence; inference is not rerun locally.",
        },
        7: {
            "era": "Large-scale prompt-based TTS",
            "model": "F5-TTS v1 Base",
            "provenance": "local_official_code_and_checkpoint",
            "source_code": "https://github.com/SWivid/F5-TTS",
            "source_revision": "f5-tts 1.1.22 / model_1250000.safetensors",
            "prompt_audio": "reference/stage7_slt_reference.wav",
            "prompt_text": "This is a short reference sample for the modern synthesis system.",
            "claim_limit": "Prompt voice is synthetic CMU SLT from Stage 3; this controls voice more closely for Stage 3 and 7 but cannot impose one identity on all historical systems.",
        },
    }

    stages: list[dict[str, object]] = []
    for stage in range(1, 8):
        raw_path = RAW_DIR / RAW_FILES[stage]
        playback_path = PLAYBACK_DIR / PLAYBACK_FILES[stage]
        item = {
            "stage": stage,
            **metadata[stage],
            "text": DEMO_TEXT,
            "raw_file": str(raw_path.relative_to(RAW_DIR)).replace("\\", "/"),
            "playback_file": str(playback_path.relative_to(RAW_DIR)).replace("\\", "/"),
            "raw_audio": inspect_wav(raw_path),
            "playback_audio": inspect_wav(playback_path),
        }
        stages.append(item)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "comparison_text": DEMO_TEXT,
        "comparison_text_sha256": hashlib.sha256(DEMO_TEXT.encode("utf-8")).hexdigest(),
        "all_stages_use_exact_comparison_text": True,
        "playback_controls": {
            "language": "English",
            "channels": 1,
            "sample_width_bytes": 2,
            "sample_rate_hz": TARGET_SAMPLE_RATE,
            "target_whole_file_rms": TARGET_RMS,
        },
        "speaker_control": {
            "same_identity_across_all_stages": False,
            "reason": "Rule/formant KLSYN has no learned speaker identity and historical voices/checkpoints are not shared across all seven systems.",
            "best_effort": "Stages 3 and 7 share the CMU SLT voice source; Stages 4-6 are female author demos, while Stage 2 kal16 is male and Stage 1 is synthetic.",
        },
        "all_outputs_verified": True,
        "stages": stages,
    }


def verify_sources() -> None:
    errors = []
    for stage, filename in RAW_FILES.items():
        path = RAW_DIR / filename
        if not path.exists():
            errors.append(f"Stage {stage}: missing {path.name}")
            continue
        info = inspect_wav(path)
        if float(info["duration_seconds"]) < 0.5:
            errors.append(f"Stage {stage}: duration is too short")
        if info["rms"] is None or float(info["rms"]) < 0.001:
            errors.append(f"Stage {stage}: output is silent")
    if errors:
        raise RuntimeError("Comparison assembly failed:\n- " + "\n- ".join(errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    materialize_official_middle_stages(args.refresh)
    verify_sources()
    for stage in range(1, 8):
        make_playback_copy(
            RAW_DIR / RAW_FILES[stage],
            PLAYBACK_DIR / PLAYBACK_FILES[stage],
        )
    manifest = build_manifest()
    manifest_path = RAW_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Verified 7/7 raw outputs and 7/7 controlled playback copies: {manifest_path}")


if __name__ == "__main__":
    main()
