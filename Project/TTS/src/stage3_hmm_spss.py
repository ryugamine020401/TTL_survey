from __future__ import annotations

import math
import random
from pathlib import Path

from audio_utils import write_mono_wav
from phonemes import DEMO_TEXT, base_phone, phone_spec, stress, text_to_phones


SAMPLE_RATE = 22050
FRAME_SECONDS = 0.005
FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_SECONDS)


def moving_average(values: list[float], radius: int) -> list[float]:
    if not values:
        return []
    result: list[float] = []
    for index in range(len(values)):
        start = max(0, index - radius)
        end = min(len(values), index + radius + 1)
        result.append(sum(values[start:end]) / (end - start))
    return result


def build_state_trajectory(text: str) -> list[dict[str, float]]:
    frames: list[dict[str, float]] = []
    pitch_cursor = 0
    phones = text_to_phones(text)
    phone_total = sum(phone != "|" for phone in phones)
    for phone in phones:
        if phone == "|":
            for _ in range(8):
                frames.append({"f0": 0.0, "f1": 500, "f2": 1500, "f3": 2800, "voice": 0, "noise": 0})
            continue

        spec = phone_spec(phone)
        accent = stress(phone)
        duration = spec.duration * (1.12 if accent == 1 else 1.0)
        total_frames = max(5, round(duration / FRAME_SECONDS))
        # Five left-to-right HMM states with explicit mean durations.
        state_counts = [total_frames // 5] * 5
        for index in range(total_frames % 5):
            state_counts[index] += 1
        base_f0 = 120 + (10 if accent == 1 else 3 if accent == 2 else 0)
        base_f0 -= 14 * pitch_cursor / max(1, phone_total)
        pitch_cursor += 1

        for state, count in enumerate(state_counts):
            state_offset = (state - 2) / 2
            for _ in range(count):
                frames.append(
                    {
                        "f0": base_f0 + 1.5 * state_offset if spec.voiced else 0.0,
                        "f1": spec.formants[0] + 10 * state_offset,
                        "f2": spec.formants[1] + 18 * state_offset,
                        "f3": spec.formants[2] + 22 * state_offset,
                        "voice": spec.voiced,
                        "noise": spec.noise,
                    }
                )

    # MLPG-like continuity proxy: smooth means and shrink variance, reproducing
    # the characteristic over-smoothed trajectory of classical SPSS.
    for key, radius in (("f0", 4), ("f1", 7), ("f2", 7), ("f3", 7), ("voice", 2), ("noise", 2)):
        smoothed = moving_average([frame[key] for frame in frames], radius)
        for frame, value in zip(frames, smoothed):
            frame[key] = value
    means = {key: sum(frame[key] for frame in frames) / len(frames) for key in ("f1", "f2", "f3")}
    for frame in frames:
        for key in ("f1", "f2", "f3"):
            frame[key] = means[key] + 0.72 * (frame[key] - means[key])
    return frames


def render_trajectory(frames: list[dict[str, float]]) -> list[float]:
    rng = random.Random(2000)
    phase = 0.0
    previous_noise = 0.0
    output: list[float] = [0.0] * int(0.12 * SAMPLE_RATE)
    for frame in frames:
        f0 = max(75.0, frame["f0"]) if frame["voice"] > 0.04 else 0.0
        for sample_index in range(FRAME_SAMPLES):
            value = 0.0
            if f0:
                phase += 2.0 * math.pi * f0 / SAMPLE_RATE
                harmonic_count = min(34, int((SAMPLE_RATE / 2) / f0))
                for harmonic in range(1, harmonic_count + 1):
                    frequency = harmonic * f0
                    resonance = sum(
                        1.0 / (1.0 + ((frequency - frame[key]) / bandwidth) ** 2)
                        for key, bandwidth in (("f1", 150), ("f2", 190), ("f3", 240))
                    )
                    value += frame["voice"] * (0.12 + resonance) * math.sin(harmonic * phase) / (harmonic ** 1.28)
            if frame["noise"] > 0.01:
                raw = rng.uniform(-1.0, 1.0)
                value += frame["noise"] * 0.22 * (raw - 0.75 * previous_noise)
                previous_noise = raw
            # Quantisation is a compact stand-in for a low-dimensional vocoder parameter stream.
            output.append(round(value * 96.0) / 96.0)
    output.extend([0.0] * int(0.18 * SAMPLE_RATE))
    return output


def generate(path: Path, text: str = DEMO_TEXT) -> None:
    frames = build_state_trajectory(text)
    write_mono_wav(path, render_trajectory(frames), SAMPLE_RATE)


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[1] / "output" / "stage3_hmm_spss.wav")

