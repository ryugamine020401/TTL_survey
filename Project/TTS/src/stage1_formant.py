from __future__ import annotations

import math
import random
from pathlib import Path

from audio_utils import write_mono_wav
from phonemes import DEMO_TEXT, FRICATIVES, STOPS, base_phone, phone_spec, stress, text_to_phones


SAMPLE_RATE = 22050


def envelope(index: int, count: int, edge: float = 0.12) -> float:
    if count <= 1:
        return 1.0
    position = index / (count - 1)
    return min(1.0, position / edge, (1.0 - position) / edge)


def voiced_segment(phone: str, duration: float, pitch: float, rng: random.Random) -> list[float]:
    spec = phone_spec(phone)
    count = max(1, int(duration * SAMPLE_RATE))
    result: list[float] = []
    harmonic_count = min(48, int((SAMPLE_RATE / 2) / pitch))
    base = base_phone(phone)
    for index in range(count):
        t = index / SAMPLE_RATE
        local_pitch = pitch * (1.0 - 0.025 * t / max(duration, 1e-6))
        value = 0.0
        for harmonic in range(1, harmonic_count + 1):
            frequency = harmonic * local_pitch
            resonance = 0.0
            for formant, bandwidth in zip(spec.formants, spec.bandwidths):
                resonance += 1.0 / (1.0 + ((frequency - formant) / bandwidth) ** 2)
            amplitude = (0.16 + resonance) / (harmonic ** 1.15)
            value += amplitude * math.sin(2.0 * math.pi * frequency * t)
        if spec.noise:
            value += spec.noise * 0.18 * rng.uniform(-1.0, 1.0)
        if base in {"M", "N"}:
            value *= 0.58
        result.append(value * envelope(index, count))
    return result


def noise_segment(phone: str, duration: float, rng: random.Random) -> list[float]:
    count = max(1, int(duration * SAMPLE_RATE))
    base = base_phone(phone)
    emphasis = FRICATIVES.get(base, (0.85, duration))[0]
    result: list[float] = []
    previous = 0.0
    for index in range(count):
        raw = rng.uniform(-1.0, 1.0)
        high_pass = raw - 0.82 * previous
        previous = raw
        value = emphasis * high_pass
        if base in {"F", "TH", "HH"}:
            value *= 0.55
        result.append(value * envelope(index, count, 0.18))
    return result


def stop_segment(phone: str, duration: float, pitch: float, rng: random.Random) -> list[float]:
    voiced, _ = STOPS.get(base_phone(phone), (False, duration))
    closure_count = int(duration * SAMPLE_RATE * 0.58)
    burst_count = max(1, int(duration * SAMPLE_RATE) - closure_count)
    result = [0.0] * closure_count
    if voiced:
        result = voiced_segment("AH0", closure_count / SAMPLE_RATE, pitch * 0.82, rng)
        result = [sample * 0.13 for sample in result]
    previous = 0.0
    for index in range(burst_count):
        raw = rng.uniform(-1.0, 1.0)
        burst = raw - previous
        previous = raw
        result.append(0.8 * burst * math.exp(-5.5 * index / burst_count))
    return result


def synthesize(text: str = DEMO_TEXT) -> list[float]:
    rng = random.Random(1980)
    phones = text_to_phones(text)
    output: list[float] = [0.0] * int(0.12 * SAMPLE_RATE)
    voiced_index = 0
    total_phones = sum(phone != "|" for phone in phones)
    for phone in phones:
        if phone == "|":
            output.extend([0.0] * int(0.045 * SAMPLE_RATE))
            continue
        spec = phone_spec(phone)
        accent = stress(phone)
        pitch = 118.0 + (13.0 if accent == 1 else 5.0 if accent == 2 else 0.0)
        pitch -= 16.0 * voiced_index / max(1, total_phones)
        voiced_index += 1
        base = base_phone(phone)
        duration = spec.duration * (1.18 if accent == 1 else 1.05 if accent == 2 else 1.0)
        if base in STOPS:
            segment = stop_segment(phone, duration, pitch, rng)
        elif base in FRICATIVES and spec.voiced == 0.0:
            segment = noise_segment(phone, duration, rng)
        else:
            segment = voiced_segment(phone, duration, pitch, rng)
        output.extend(segment)
    output.extend([0.0] * int(0.18 * SAMPLE_RATE))
    return output


def generate(path: Path, text: str = DEMO_TEXT) -> None:
    write_mono_wav(path, synthesize(text), SAMPLE_RATE)


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[1] / "output" / "stage1_rule_formant.wav")

