from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.io import wavfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KLSYN_ROOT = PROJECT_ROOT / "vendor" / "klsyn"
sys.path.insert(0, str(KLSYN_ROOT))

from klsyn import klatt_wrap, klpfile  # noqa: E402
from phonemes import DEMO_TEXT, base_phone, phone_spec, stress, text_to_phones  # noqa: E402


FRAME_MS = 5
SAMPLE_RATE = 16_000
RULE_FRAME_MS = 10
RULE_CONTROLS = PROJECT_ROOT / "config" / "stage1_rule_frontend_frames.csv"
VOWELS = {"IY", "IH", "EH", "AE", "AH", "ER", "AY", "OW"}
SONORANTS = {"W", "R", "L", "M", "N"}
FRICATIVES = {"F", "V", "TH", "DH", "S", "Z", "SH", "HH"}
STOPS = {"P", "B", "T", "D", "K", "G"}


def _frame_count(seconds: float) -> int:
    return max(1, int(round(seconds * 1000 / FRAME_MS)))


def _noise_amplitudes(phone: str, level: int) -> tuple[int, int, int, int, int, int, int]:
    """Return af/a2..a6/ab in Klatt's dB-like controls."""
    base = base_phone(phone)
    if level <= 0:
        return (0, 0, 0, 0, 0, 0, 0)
    if base in {"S", "Z"}:
        return (level, 0, 18, 38, 58, 62, 18)
    if base in {"SH", "JH"}:
        return (level, 0, 47, 58, 52, 46, 18)
    if base in {"F", "V", "TH", "DH"}:
        return (level, 37, 42, 43, 42, 38, 38)
    if base in {"T", "D"}:
        return (level, 0, 10, 28, 51, 57, 35)
    if base in {"K", "G"}:
        return (level, 0, 42, 51, 42, 34, 38)
    return (level, 30, 38, 45, 43, 38, 48)


def _db_envelope(level: int, gain: float) -> int:
    """Apply a linear envelope to one of Klatt's dB-like amplitude controls."""
    if level <= 0 or gain <= 0.01:
        return 0
    return max(0, int(round(level + 20.0 * np.log10(min(1.0, gain)))))


def _formant_target(phone: str, position: float) -> np.ndarray:
    """Return a formant target, including the movement in English diphthongs."""
    base = base_phone(phone)
    start = np.asarray(phone_spec(phone).formants, dtype=float)
    # Unstressed AH is a reduced schwa in this sentence (the/reverend/
    # gentleman's/journal), not the full stressed STRUT vowel used by AH1.
    if base == "AH" and stress(phone) == 0:
        return np.asarray((500.0, 1500.0, 2500.0))
    if base == "AY":
        end = np.asarray((320.0, 2250.0, 2850.0))
        amount = np.clip((position - 0.30) / 0.65, 0.0, 1.0)
        return start + (end - start) * amount
    if base == "OW":
        end = np.asarray((350.0, 800.0, 2200.0))
        amount = np.clip((position - 0.35) / 0.60, 0.0, 1.0)
        return start + (end - start) * amount
    return start


def _is_voiced(phone: str) -> bool:
    return phone != "sil" and phone_spec(phone).voiced > 0.0


def _make_handcrafted_tracks(text: str) -> dict[str, list[int]]:
    phones = text_to_phones(text)
    tracks = {name: [] for name in (
        "f0", "av", "F1", "b1", "F2", "b2", "F3", "b3", "F4", "b4",
        "F5", "b5", "ah", "af", "a2", "a3", "a4", "a5", "a6", "ab", "an", "oq",
    )}

    segments: list[tuple[str, int]] = [("sil", _frame_count(0.13))]
    for phone in phones:
        if phone == "|":
            segments.append(("sil", _frame_count(0.065)))
        else:
            duration = phone_spec(phone).duration * 0.90
            if stress(phone) == 1 and base_phone(phone) in VOWELS:
                duration *= 1.12
            elif stress(phone) == 2 and base_phone(phone) in VOWELS:
                duration *= 1.06
            segments.append((phone, _frame_count(duration)))
    segments.append(("sil", _frame_count(0.18)))

    total_frames = sum(length for _, length in segments)
    current_formants = np.array((500.0, 1500.0, 2500.0))
    elapsed = 0

    for segment_index, (phone, length) in enumerate(segments):
        previous_phone = segments[segment_index - 1][0] if segment_index else "sil"
        next_phone = segments[segment_index + 1][0] if segment_index + 1 < len(segments) else "sil"
        if phone == "sil":
            target_formants = current_formants
            spec = None
        else:
            spec = phone_spec(phone)
            target_formants = _formant_target(phone, 1.0)

        for local_index in range(length):
            sentence_pos = elapsed / max(1, total_frames - 1)
            local_position = local_index / max(1, length - 1)
            if spec is None:
                formants = current_formants
            else:
                phone_target = _formant_target(phone, local_position)
                transition = min(1.0, (local_index + 1) / max(1.0, length * 0.28))
                formants = current_formants + (phone_target - current_formants) * transition
                if next_phone != "sil" and local_position > 0.78:
                    next_target = _formant_target(next_phone, 0.0)
                    next_amount = (local_position - 0.78) / 0.22
                    formants += (next_target - formants) * next_amount * 0.45

            if spec is None:
                av = ah = af_level = 0
                noise = (0, 0, 0, 0, 0, 0, 0)
                f0 = int(round(128 - 18 * sentence_pos))
                bandwidths = (90, 120, 170)
                oq = 40
            else:
                base = base_phone(phone)
                onset_gain = 1.0 if _is_voiced(previous_phone) else min(1.0, (local_index + 1) / 3.0)
                offset_gain = 1.0 if _is_voiced(next_phone) else min(1.0, (length - local_index) / 3.0)
                voice_gain = min(onset_gain, offset_gain)
                closure = base in STOPS and local_position < 0.48
                burst = base in STOPS and 0.48 <= local_position < 0.76
                affricate_closure = base == "JH" and local_position < 0.28

                if base in VOWELS:
                    av = _db_envelope(61, voice_gain)
                elif base in SONORANTS:
                    av = _db_envelope(56 if base in {"M", "N"} else 58, voice_gain)
                elif base in {"V", "DH", "Z"}:
                    av = _db_envelope(50, voice_gain)
                elif base in {"B", "D", "G"}:
                    av = 39 if closure else _db_envelope(51, offset_gain)
                elif base == "JH":
                    av = 35 if affricate_closure else _db_envelope(49, offset_gain)
                else:
                    av = 0

                ah = 0
                if base in STOPS:
                    release = local_position >= 0.48
                    af_level = 61 if burst else (48 if release and base in {"P", "T", "K"} else 0)
                    if release and base in {"P", "T", "K"}:
                        ah = 50
                elif base == "JH":
                    af_level = 0 if affricate_closure else _db_envelope(57, min(1.0, (local_index + 1) / 3.0))
                elif base in FRICATIVES:
                    noise_gain = min(1.0, (local_index + 1) / 3.0, (length - local_index) / 3.0)
                    af_level = _db_envelope(61 if base in {"S", "SH"} else 58, noise_gain)
                else:
                    af_level = 0
                noise = _noise_amplitudes(phone, af_level)
                f0 = int(round(128 - 18 * sentence_pos + (8 if stress(phone) == 1 else 3 if stress(phone) == 2 else 0)))
                bandwidths = tuple(int(round(value)) for value in spec.bandwidths)
                # At this male F0, OQ values near 50 ask the original KLSYN core
                # for a glottal-open interval longer than its supported maximum.
                oq = 38 if spec.voiced else 45

            tracks["f0"].append(f0)
            tracks["av"].append(av)
            tracks["F1"].append(int(round(formants[0])))
            tracks["b1"].append(bandwidths[0])
            tracks["F2"].append(int(round(formants[1])))
            tracks["b2"].append(bandwidths[1])
            tracks["F3"].append(int(round(formants[2])))
            tracks["b3"].append(bandwidths[2])
            tracks["F4"].append(3400)
            tracks["b4"].append(220)
            tracks["F5"].append(4300)
            tracks["b5"].append(300)
            tracks["ah"].append(ah)
            tracks["af"].append(noise[0])
            tracks["a2"].append(noise[1])
            tracks["a3"].append(noise[2])
            tracks["a4"].append(noise[3])
            tracks["a5"].append(noise[4])
            tracks["a6"].append(noise[5])
            tracks["ab"].append(noise[6])
            tracks["an"].append(48 if spec is not None and base_phone(phone) in {"M", "N"} else 0)
            tracks["oq"].append(oq)
            elapsed += 1

        current_formants = target_formants

    return tracks


def _make_rule_tracks() -> dict[str, list[int]]:
    """Convert rsynth-derived 10 ms rule controls to KLSYN's 5 ms tracks."""
    source = np.loadtxt(RULE_CONTROLS, delimiter=",")
    if source.ndim != 2 or source.shape[1] != 40:
        raise ValueError(f"Unexpected Stage 1 control table shape: {source.shape}")

    source_times = np.arange(len(source), dtype=float) * RULE_FRAME_MS
    output_times = np.arange(0.0, source_times[-1] + 0.1, FRAME_MS)

    def interpolate(column: int, scale: float = 1.0, minimum: int = 0) -> list[int]:
        values = np.interp(output_times, source_times, source[:, column] * scale)
        return np.maximum(minimum, np.rint(values)).astype(int).tolist()

    tracks = {
        "f0": interpolate(0, 0.1),
        "av": interpolate(1),
        "F1": interpolate(2, minimum=200),
        "b1": interpolate(3, minimum=40),
        "F2": interpolate(4, minimum=550),
        "b2": interpolate(5, minimum=40),
        "F3": interpolate(6, minimum=1200),
        "b3": interpolate(7, minimum=40),
        "F4": interpolate(8, minimum=1200),
        "b4": interpolate(9, minimum=40),
        "F5": interpolate(10, minimum=1200),
        "b5": interpolate(11, minimum=40),
        "f6": interpolate(12, minimum=1200),
        "b6": interpolate(13, minimum=40),
        "fz": interpolate(14, minimum=248),
        "bz": interpolate(15, minimum=40),
        "fp": interpolate(16, minimum=248),
        "bp": interpolate(17, minimum=40),
        "ah": interpolate(18),
        "oq": [35] * len(output_times),
        "at": interpolate(20),
        "tl": interpolate(21),
        "af": interpolate(22),
        "sk": interpolate(23),
        "a1": interpolate(24),
        "p1": interpolate(25, minimum=40),
        "a2": interpolate(26),
        "p2": interpolate(27, minimum=40),
        "a3": interpolate(28),
        "p3": interpolate(29, minimum=40),
        "a4": interpolate(30),
        "p4": interpolate(31, minimum=40),
        "a5": interpolate(32),
        "p5": interpolate(33, minimum=40),
        "a6": interpolate(34),
        "p6": interpolate(35, minimum=40),
        "an": interpolate(36),
        "ab": interpolate(37),
        "ap": interpolate(38),
    }
    return tracks


def _make_tracks(text: str) -> dict[str, list[int]]:
    if text.strip() == DEMO_TEXT:
        return _make_rule_tracks()
    return _make_handcrafted_tracks(text)


def generate(text: str, output: Path, parameter_output: Path) -> None:
    tracks = _make_tracks(text)
    duration_ms = len(tracks["f0"]) * FRAME_MS
    if duration_ms > 5000:
        raise ValueError(f"KLSYN's original duration limit is 5000 ms; got {duration_ms} ms")

    params: dict[str, int | list[int]] = {
        "sr": SAMPLE_RATE,
        "nf": 5,
        "du": duration_ms,
        "ss": 1,
        "ui": FRAME_MS,
        "rs": 1,
        "g0": 55,
        "agc": 0,
    }
    params.update(tracks)

    synth = klatt_wrap.synthesizer()
    synth.set_params(params)
    audio, sample_rate = synth.synthesize()
    if audio.size == 0 or int(np.max(np.abs(audio.astype(np.int32)))) == 0:
        raise RuntimeError("KLSYN produced an empty or silent waveform")

    output.parent.mkdir(parents=True, exist_ok=True)
    parameter_output.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(output, sample_rate, audio)
    comments = {
        "header": (
            "# Generated comparison controls for Dennis Klatt's KLSYN core.\n"
            f"# Text: {text}\n"
            "# The fixed-sentence rule controls are derived from rsynth/SoLoud element rules.\n"
            "# Waveform synthesis is performed by the original KLSYN C core.\n"
        ),
        "constant": {},
        "varied": [],
    }
    klpfile.write(parameter_output, synth=synth, comments=comments)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default=DEMO_TEXT)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "output" / "comparable" / "stage1_author_klsyn.wav",
    )
    parser.add_argument(
        "--parameters",
        type=Path,
        default=PROJECT_ROOT / "output" / "comparable" / "stage1_author_klsyn.klp",
    )
    args = parser.parse_args()
    generate(args.text, args.output, args.parameters)
    print(args.output)


if __name__ == "__main__":
    main()
