from __future__ import annotations

import re
import subprocess
import wave
from array import array
from pathlib import Path

from audio_utils import concatenate_pcm16
from phonemes import DEMO_TEXT


def trim_silence(samples: array, threshold: int = 180, pad: int = 180) -> array:
    active = [index for index, value in enumerate(samples) if abs(value) >= threshold]
    if not active:
        return samples
    start = max(0, active[0] - pad)
    end = min(len(samples), active[-1] + pad + 1)
    return array("h", samples[start:end])


def generate(path: Path, cache_dir: Path, script: Path, text: str = DEMO_TEXT) -> None:
    words = re.findall(r"[A-Za-z']+", text)
    cache_dir.mkdir(parents=True, exist_ok=True)
    clips: list[array] = []
    sample_rate: int | None = None

    for index, word in enumerate(words):
        unit_path = cache_dir / f"{index:02d}_{word.lower().replace(chr(39), '')}.wav"
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                "-Text",
                word,
                "-Output",
                str(unit_path),
            ],
            check=True,
        )
        with wave.open(str(unit_path), "rb") as wav:
            if wav.getnchannels() != 1 or wav.getsampwidth() != 2:
                raise RuntimeError(f"Unexpected SAPI WAV format: {unit_path}")
            if sample_rate is None:
                sample_rate = wav.getframerate()
            elif sample_rate != wav.getframerate():
                raise RuntimeError("SAPI unit sample rates do not match")
            pcm = array("h")
            pcm.frombytes(wav.readframes(wav.getnframes()))
            clips.append(trim_silence(pcm))

    assert sample_rate is not None
    joined = concatenate_pcm16(clips, sample_rate, pause_ms=22, crossfade_ms=6)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(joined.tobytes())


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    generate(
        root / "output" / "stage2_concatenative.wav",
        root / "cache" / "stage2_units",
        root / "scripts" / "sapi_unit.ps1",
    )

