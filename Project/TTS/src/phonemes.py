from __future__ import annotations

import re
from dataclasses import dataclass


DEMO_TEXT = "I will quote an extract from the reverend gentleman's own journal."


LEXICON = {
    "i": ["AY1"],
    "will": ["W", "IH1", "L"],
    "quote": ["K", "W", "OW1", "T"],
    "an": ["AE1", "N"],
    "extract": ["EH1", "K", "S", "T", "R", "AE2", "K", "T"],
    "from": ["F", "R", "AH1", "M"],
    "the": ["DH", "AH0"],
    "reverend": ["R", "EH1", "V", "ER0", "AH0", "N", "D"],
    "gentleman's": ["JH", "EH1", "N", "T", "AH0", "L", "M", "AH0", "N", "Z"],
    "own": ["OW1", "N"],
    "journal": ["JH", "ER1", "N", "AH0", "L"],
}


@dataclass(frozen=True)
class PhoneSpec:
    formants: tuple[float, float, float]
    bandwidths: tuple[float, float, float] = (90.0, 120.0, 170.0)
    voiced: float = 1.0
    noise: float = 0.0
    duration: float = 0.09


VOWELS = {
    "IY": PhoneSpec((300, 2300, 3000), duration=0.105),
    "IH": PhoneSpec((390, 1990, 2550), duration=0.085),
    "EH": PhoneSpec((530, 1840, 2480), duration=0.09),
    "AE": PhoneSpec((660, 1720, 2410), duration=0.11),
    "AH": PhoneSpec((640, 1190, 2390), duration=0.085),
    "ER": PhoneSpec((490, 1350, 1690), duration=0.105),
    "AY": PhoneSpec((700, 1200, 2500), duration=0.16),
    "OW": PhoneSpec((500, 900, 2450), duration=0.15),
}

SONORANTS = {
    "W": PhoneSpec((350, 800, 2200), duration=0.07),
    "R": PhoneSpec((420, 1250, 1650), duration=0.075),
    "L": PhoneSpec((400, 1200, 2600), duration=0.075),
    "M": PhoneSpec((250, 1000, 2100), bandwidths=(130, 180, 220), duration=0.075),
    "N": PhoneSpec((300, 1450, 2200), bandwidths=(140, 180, 230), duration=0.07),
}

FRICATIVES = {
    "F": (0.75, 0.085),
    "V": (0.42, 0.075),
    "TH": (0.60, 0.075),
    "DH": (0.35, 0.065),
    "S": (1.00, 0.095),
    "Z": (0.72, 0.085),
    "SH": (0.90, 0.10),
    "HH": (0.50, 0.07),
}

STOPS = {
    "P": (False, 0.07),
    "B": (True, 0.065),
    "T": (False, 0.065),
    "D": (True, 0.06),
    "K": (False, 0.075),
    "G": (True, 0.07),
}


def base_phone(phone: str) -> str:
    return re.sub(r"\d", "", phone)


def stress(phone: str) -> int:
    match = re.search(r"(\d)", phone)
    return int(match.group(1)) if match else 0


def text_to_phones(text: str) -> list[str]:
    words = re.findall(r"[a-z']+", text.lower())
    unknown = [word for word in words if word not in LEXICON]
    if unknown:
        raise ValueError(
            "The local historical demonstrators use a fixed lexicon. "
            f"Unsupported words: {', '.join(unknown)}"
        )
    phones: list[str] = []
    for word_index, word in enumerate(words):
        if word_index:
            phones.append("|")
        phones.extend(LEXICON[word])
    return phones


def phone_spec(phone: str) -> PhoneSpec:
    base = base_phone(phone)
    if base in VOWELS:
        return VOWELS[base]
    if base in SONORANTS:
        return SONORANTS[base]
    if base in FRICATIVES:
        noise, duration = FRICATIVES[base]
        voiced = 0.35 if base in {"V", "DH", "Z"} else 0.0
        # Keep F3 below the fixed F4 (3400 Hz).  The older 4200-Hz value made
        # the cascade cross formants during transitions and could overload it.
        return PhoneSpec((900, 2800, 3100), voiced=voiced, noise=noise, duration=duration)
    if base in STOPS:
        voiced, duration = STOPS[base]
        return PhoneSpec((500, 1700, 3000), voiced=0.25 if voiced else 0.0, noise=0.8, duration=duration)
    if base == "JH":
        return PhoneSpec((500, 1900, 3000), voiced=0.3, noise=0.85, duration=0.11)
    raise ValueError(f"No acoustic specification for phoneme: {phone}")
