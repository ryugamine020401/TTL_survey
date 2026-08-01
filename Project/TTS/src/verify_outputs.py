from __future__ import annotations

import json
from pathlib import Path

from audio_utils import inspect_wav


EXPECTED = [
    "stage1_rule_formant.wav",
    "stage2_concatenative.wav",
    "stage3_hmm_spss.wav",
    "stage4_neural_spss_merlin.wav",
    "stage5_autoregressive_tacotron2.wav",
    "stage6_parallel_fastspeech.wav",
    "stage7_codec_lm_valle.wav",
]


def verify(output_dir: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    errors: list[str] = []
    for filename in EXPECTED:
        path = output_dir / filename
        if not path.exists():
            errors.append(f"missing: {filename}")
            continue
        try:
            info = inspect_wav(path)
        except Exception as exc:  # noqa: BLE001 - verification should report every bad artifact
            errors.append(f"invalid WAV {filename}: {exc}")
            continue
        if float(info["duration_seconds"]) < 0.5:
            errors.append(f"too short: {filename}")
        if info["rms"] is not None and float(info["rms"]) < 0.001:
            errors.append(f"effectively silent: {filename}")
        results.append(info)
    if errors:
        raise RuntimeError("Output verification failed:\n- " + "\n- ".join(errors))
    return results


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results = verify(root / "output")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

