from __future__ import annotations

import hashlib
import math
import struct
import wave
from array import array
from pathlib import Path
from typing import Iterable


def clamp16(value: float) -> int:
    return max(-32768, min(32767, int(round(value))))


def normalize(samples: Iterable[float], peak: float = 0.92) -> array:
    values = list(samples)
    if not values:
        return array("h")
    maximum = max(abs(value) for value in values)
    if maximum <= 1e-12:
        return array("h", [0] * len(values))
    scale = peak * 32767.0 / maximum
    return array("h", (clamp16(value * scale) for value in values))


def write_mono_wav(path: Path, samples: Iterable[float], sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = normalize(samples)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def write_pcm16_wav(path: Path, samples: Iterable[int], sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = array("h", (clamp16(value) for value in samples))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm.tobytes())


def decode_riff_wave(path: Path) -> tuple[int, list[int]]:
    """Decode common PCM and IEEE-float WAV variants to mono PCM16 values."""
    payload = path.read_bytes()
    if len(payload) < 12 or payload[:4] != b"RIFF" or payload[8:12] != b"WAVE":
        raise ValueError(f"Not a RIFF/WAVE file: {path}")

    fmt: bytes | None = None
    data: bytes | None = None
    offset = 12
    while offset + 8 <= len(payload):
        chunk_id = payload[offset : offset + 4]
        chunk_size = struct.unpack_from("<I", payload, offset + 4)[0]
        chunk = payload[offset + 8 : offset + 8 + chunk_size]
        if chunk_id == b"fmt ":
            fmt = chunk
        elif chunk_id == b"data":
            data = chunk
        offset += 8 + chunk_size + (chunk_size & 1)

    if fmt is None or data is None or len(fmt) < 16:
        raise ValueError(f"WAV is missing fmt or data chunk: {path}")
    format_tag, channels, sample_rate, _, block_align, bits = struct.unpack_from("<HHIIHH", fmt, 0)
    if format_tag == 0xFFFE and len(fmt) >= 26:
        format_tag = struct.unpack_from("<H", fmt, 24)[0]
    if channels < 1 or block_align < 1:
        raise ValueError(f"Invalid WAV layout: {path}")

    frame_count = len(data) // block_align
    mono: list[int] = []
    bytes_per_sample = bits // 8
    for frame_index in range(frame_count):
        channel_values: list[float] = []
        frame_offset = frame_index * block_align
        for channel in range(channels):
            sample_offset = frame_offset + channel * bytes_per_sample
            if format_tag == 3 and bits == 32:
                value = struct.unpack_from("<f", data, sample_offset)[0] * 32767.0
            elif format_tag == 1 and bits == 16:
                value = float(struct.unpack_from("<h", data, sample_offset)[0])
            elif format_tag == 1 and bits == 24:
                raw = int.from_bytes(data[sample_offset : sample_offset + 3], "little", signed=False)
                if raw & 0x800000:
                    raw -= 1 << 24
                value = raw / 256.0
            elif format_tag == 1 and bits == 32:
                value = struct.unpack_from("<i", data, sample_offset)[0] / 65536.0
            else:
                raise ValueError(f"Unsupported WAV format tag={format_tag}, bits={bits}: {path}")
            channel_values.append(value)
        mono.append(clamp16(sum(channel_values) / len(channel_values)))
    return sample_rate, mono


def canonicalize_wav(source: Path, destination: Path) -> None:
    sample_rate, samples = decode_riff_wave(source)
    write_pcm16_wav(destination, samples, sample_rate)


def read_pcm16_mono(path: Path) -> tuple[int, array]:
    with wave.open(str(path), "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2:
            raise ValueError(f"Expected 16-bit mono PCM: {path}")
        sample_rate = wav.getframerate()
        data = array("h")
        data.frombytes(wav.readframes(wav.getnframes()))
    return sample_rate, data


def concatenate_pcm16(
    clips: list[array], sample_rate: int, pause_ms: int = 28, crossfade_ms: int = 8
) -> array:
    if not clips:
        return array("h")
    pause = array("h", [0] * int(sample_rate * pause_ms / 1000))
    fade_count = int(sample_rate * crossfade_ms / 1000)
    output = array("h", clips[0])
    for clip in clips[1:]:
        if fade_count > 0 and len(output) >= fade_count and len(clip) >= fade_count:
            for index in range(fade_count):
                alpha = index / max(1, fade_count - 1)
                left = output[-fade_count + index]
                right = clip[index]
                output[-fade_count + index] = clamp16((1.0 - alpha) * left + alpha * right)
            output.extend(pause)
            output.extend(clip[fade_count:])
        else:
            output.extend(pause)
            output.extend(clip)
    return output


def inspect_wav(path: Path) -> dict[str, object]:
    with wave.open(str(path), "rb") as wav:
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frames = wav.getnframes()
        compression = wav.getcomptype()
        raw = wav.readframes(frames)

    if sample_width == 2:
        pcm = array("h")
        pcm.frombytes(raw)
        if pcm:
            peak = max(abs(value) for value in pcm) / 32768.0
            rms = math.sqrt(sum(value * value for value in pcm) / len(pcm)) / 32768.0
        else:
            peak = rms = 0.0
    else:
        peak = rms = None

    return {
        "path": path.name,
        "channels": channels,
        "sample_width_bytes": sample_width,
        "sample_rate_hz": sample_rate,
        "frames": frames,
        "duration_seconds": round(frames / sample_rate, 3) if sample_rate else 0.0,
        "compression": compression,
        "peak": round(peak, 6) if peak is not None else None,
        "rms": round(rms, 6) if rms is not None else None,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
