from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from audio_utils import inspect_wav
from official_references import REFERENCES, materialize_all
from phonemes import DEMO_TEXT
from stage1_formant import generate as generate_stage1
from stage2_concatenative import generate as generate_stage2
from stage3_hmm_spss import generate as generate_stage3
from verify_outputs import EXPECTED, verify


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one audible WAV for each of seven TTS eras.")
    parser.add_argument("--refresh", action="store_true", help="Re-download official model samples.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "output"
    cache = root / "cache"
    output.mkdir(parents=True, exist_ok=True)

    print("[1/7] Rule/formant synthesis (local)")
    generate_stage1(output / EXPECTED[0], DEMO_TEXT)

    print("[2/7] Waveform-unit concatenation (local)")
    generate_stage2(
        output / EXPECTED[1],
        cache / "stage2_units",
        root / "scripts" / "sapi_unit.ps1",
        DEMO_TEXT,
    )

    print("[3/7] HMM-style statistical parametric synthesis (local demonstrator)")
    generate_stage3(output / EXPECTED[2], DEMO_TEXT)

    print("[4-7/7] Materialising official model outputs")
    materialize_all(output, refresh=args.refresh)

    checks = verify(output)
    stages = [
        {
            "stage": 1,
            "era": "Rule/formant synthesis",
            "file": EXPECTED[0],
            "mode": "local_technique_reproduction",
            "model": "Compact source-filter/formant synthesizer written for this demo",
            "text": DEMO_TEXT,
            "claim_limit": "Illustrates the mechanism; it is not the original 1980 Klatt implementation.",
        },
        {
            "stage": 2,
            "era": "Concatenative synthesis",
            "file": EXPECTED[1],
            "mode": "local_technique_reproduction",
            "model": "Word-unit waveform inventory plus concatenation and short cross-fades",
            "text": DEMO_TEXT,
            "claim_limit": "The inventory is bootstrapped with Windows SAPI, not a historical Festival/Multisyn corpus.",
        },
        {
            "stage": 3,
            "era": "HMM statistical parametric synthesis",
            "file": EXPECTED[2],
            "mode": "local_pedagogical_proxy",
            "model": "Five-state duration model, smoothed acoustic means, compact source-filter renderer",
            "text": DEMO_TEXT,
            "claim_limit": "Mechanism-level demonstrator; not trained HTS and not suitable for quality benchmarking.",
        },
    ]
    for stage in sorted(REFERENCES):
        reference = REFERENCES[stage]
        stages.append(
            {
                "stage": stage,
                "era": {
                    4: "Neural statistical parametric synthesis",
                    5: "Autoregressive end-to-end TTS",
                    6: "Parallel/non-autoregressive TTS",
                    7: "Codec language model / zero-shot TTS",
                }[stage],
                "file": reference["filename"],
                "mode": "official_author_model_output",
                "model": reference["model"],
                "text": reference["text"],
                "source_page": reference["page"],
                "source_audio": reference["url"],
                "claim_limit": "Published demonstration audio; this project does not run the original model checkpoint locally.",
            }
        )

    by_name = {item["path"]: item for item in checks}
    for stage in stages:
        stage["audio"] = by_name[str(stage["file"])]

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "common_text_stages_1_to_6": DEMO_TEXT,
        "all_outputs_verified": True,
        "comparison_warning": (
            "These files form a historical listening exhibit, not a controlled benchmark. "
            "Stages differ in speakers, training data, vocoders, and generation provenance."
        ),
        "stages": stages,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Verified {len(checks)}/7 WAV files. Manifest: {output / 'manifest.json'}")


if __name__ == "__main__":
    main()

