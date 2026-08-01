from __future__ import annotations

import gc
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
os.environ["TORCH_HOME"] = str(ROOT / ".cache/torch")
os.environ["HF_HOME"] = str(ROOT / ".cache/huggingface")


def release(*objects) -> None:
    del objects
    gc.collect()


def main() -> None:
    import torch
    import torchaudio
    from huggingface_hub import snapshot_download

    print("Stage 4: Tacotron 2 + Griffin-Lim")
    bundle4 = torchaudio.pipelines.TACOTRON2_GRIFFINLIM_CHAR_LJSPEECH
    release(bundle4.get_tacotron2(), bundle4.get_vocoder())

    print("Stage 5: Tacotron 2 + WaveRNN")
    bundle5 = torchaudio.pipelines.TACOTRON2_WAVERNN_CHAR_LJSPEECH
    release(bundle5.get_tacotron2(), bundle5.get_vocoder())

    print("Stage 6: NVIDIA FastPitch + HiFi-GAN")
    repo = "NVIDIA/DeepLearningExamples:torchhub"
    fastpitch, _ = torch.hub.load(repo, "nvidia_fastpitch", trust_repo=True)
    hifigan, _, denoiser = torch.hub.load(repo, "nvidia_hifigan", trust_repo=True)
    release(fastpitch, hifigan, denoiser)

    print("Stage 7: F5-TTS v1 Base")
    snapshot_download(
        repo_id="SWivid/F5-TTS",
        allow_patterns=["F5TTS_v1_Base/model_1250000.safetensors"],
        cache_dir=str(ROOT / ".cache/huggingface/hub"),
    )

    print("All interactive model files are stored inside Project/TTS/.cache.")


if __name__ == "__main__":
    main()
