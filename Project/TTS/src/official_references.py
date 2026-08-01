from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

from audio_utils import canonicalize_wav, inspect_wav


REFERENCES = {
    4: {
        "filename": "stage4_neural_spss_merlin.wav",
        "url": "https://speechresearch.github.io/audio/fastspeech/audio/merlin/1.wav",
        "model": "Merlin neural statistical parametric speech synthesis",
        "text": "I will quote an extract from the reverend gentleman's own journal.",
        "page": "https://speechresearch.github.io/fastspeech/",
    },
    5: {
        "filename": "stage5_autoregressive_tacotron2.wav",
        "url": "https://speechresearch.github.io/audio/fastspeech/audio/tacotron2/1.wav",
        "model": "Tacotron 2 autoregressive end-to-end TTS",
        "text": "I will quote an extract from the reverend gentleman's own journal.",
        "page": "https://speechresearch.github.io/fastspeech/",
    },
    6: {
        "filename": "stage6_parallel_fastspeech.wav",
        "url": "https://speechresearch.github.io/audio/fastspeech/audio/na/1.wav",
        "model": "FastSpeech parallel non-autoregressive TTS",
        "text": "I will quote an extract from the reverend gentleman's own journal.",
        "page": "https://speechresearch.github.io/fastspeech/",
    },
    7: {
        "filename": "stage7_codec_lm_valle.wav",
        "url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2023/06/ibrispeech_809_conti_infer_valle.vocos_.0.wav",
        "model": "VALL-E neural codec language model, Vocos reconstruction",
        "text": "They moved thereafter cautiously about the hut groping before and about them to find something to show that Warrenton had fulfilled his mission.",
        "page": "https://www.microsoft.com/en-us/research/project/vall-e-x/vall-e/",
    },
}


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "TTS-history-demo/1.0"})
    temporary = destination.with_suffix(destination.suffix + ".part")
    with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    converted = destination.with_suffix(destination.suffix + ".converted")
    canonicalize_wav(temporary, converted)
    if float(inspect_wav(converted)["duration_seconds"]) <= 0:
        raise RuntimeError(f"Downloaded invalid WAV: {url}")
    converted.replace(destination)
    temporary.unlink(missing_ok=True)


def materialize_all(output_dir: Path, refresh: bool = False) -> list[Path]:
    paths: list[Path] = []
    for stage in sorted(REFERENCES):
        item = REFERENCES[stage]
        path = output_dir / str(item["filename"])
        if refresh or not path.exists():
            download(str(item["url"]), path)
        paths.append(path)
    return paths
