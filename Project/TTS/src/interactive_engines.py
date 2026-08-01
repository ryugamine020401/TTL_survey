from __future__ import annotations

import gc
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.io import wavfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "interactive"
CACHE_ROOT = PROJECT_ROOT / ".cache"
TORCH_HOME = CACHE_ROOT / "torch"
HF_HOME = CACHE_ROOT / "huggingface"
TARGET_RMS = 0.065
ENGINE_VERSION = "interactive-v1"

os.environ["TORCH_HOME"] = str(TORCH_HOME)
os.environ["HF_HOME"] = str(HF_HOME)


@dataclass(frozen=True)
class StageDefinition:
    stage: int
    era: str
    model: str
    method: str
    note: str
    gpu: bool


STAGES = (
    StageDefinition(1, "Rule / Formant", "KLSYN + rsynth rules", "規則產生聲學控制參數，再由共振峰合成器產生波形。", "原始 KLSYN C 波形核心；任意文字前端使用 rsynth 衍生規則。", False),
    StageDefinition(2, "Concatenative", "Flite kal16 diphone", "從錄製好的雙音素單元中選取片段並串接。", "FestVox 官方 Flite 與 kal16 voice。", False),
    StageDefinition(3, "HMM-based SPSS", "Flite + HTS engine", "HMM 預測聲學參數，再由 vocoder 合成語音。", "HTS 官方 engine 與 CMU ARCTIC SLT voice。", False),
    StageDefinition(4, "Neural parametric bridge", "Tacotron 2 + Griffin–Lim", "神經網路預測頻譜參數，使用傳統迭代 vocoder 還原波形。", "可任意文字的本機橋接展示；不是完整 Merlin voice。", True),
    StageDefinition(5, "Autoregressive E2E", "Tacotron 2 + WaveRNN", "自回歸聲學模型逐步產生頻譜，再由神經 vocoder 產生語音。", "PyTorch Audio 官方 LJSpeech checkpoint。", True),
    StageDefinition(6, "Parallel / Non-AR", "FastPitch + HiFi-GAN", "平行預測時長、音高與頻譜，再由神經 vocoder 產生語音。", "NVIDIA 官方 FastPitch 與 HiFi-GAN checkpoint。", True),
    StageDefinition(7, "Prompt-based", "F5-TTS v1 Base", "以參考語音作為 prompt，透過 flow-matching 生成指定文字。", "SWivid 官方 F5-TTS checkpoint；參考聲線來自 Stage 3。", True),
)

STAGE_BY_ID = {item.stage: item for item in STAGES}


def stage_catalog() -> list[dict[str, object]]:
    return [asdict(item) for item in STAGES]


def validate_text(text: str) -> str:
    text = " ".join(text.strip().split())
    if not text:
        raise ValueError("請輸入要朗讀的英文文字。")
    if len(text) > 300:
        raise ValueError("第一版每次最多 300 個字元。")
    if not text.isascii():
        raise ValueError("七階段共同比較目前只支援英文與 ASCII 標點。")
    if not re.search(r"[A-Za-z]", text):
        raise ValueError("文字中至少需要一個英文字母。")
    return text


def cache_path(stage: int, text: str) -> Path:
    digest = hashlib.sha256(f"{ENGINE_VERSION}|{stage}|{text}".encode("utf-8")).hexdigest()[:20]
    return OUTPUT_ROOT / f"stage{stage}" / f"{digest}.wav"


def inspect_audio(path: Path) -> dict[str, object]:
    sample_rate, data = wavfile.read(path)
    frames = int(data.shape[0])
    return {
        "sample_rate": int(sample_rate),
        "duration_seconds": round(frames / float(sample_rate), 3),
        "bytes": path.stat().st_size,
    }


def _to_float_audio(data: np.ndarray) -> np.ndarray:
    if data.ndim == 2:
        data = data.astype(np.float64).mean(axis=1)
    if np.issubdtype(data.dtype, np.integer):
        scale = float(max(abs(np.iinfo(data.dtype).min), np.iinfo(data.dtype).max))
        return data.astype(np.float64) / scale
    return data.astype(np.float64)


def _write_normalized(path: Path, sample_rate: int, audio: np.ndarray) -> None:
    audio = _to_float_audio(np.asarray(audio))
    audio = np.nan_to_num(audio, nan=0.0, posinf=0.0, neginf=0.0)
    if audio.size < sample_rate // 10:
        raise RuntimeError("合成器輸出的音訊過短。")
    audio -= float(np.mean(audio))
    rms = float(np.sqrt(np.mean(audio * audio)))
    if rms <= 1e-7:
        raise RuntimeError("合成器輸出了靜音。")
    gain = TARGET_RMS / rms
    peak = float(np.max(np.abs(audio)))
    if peak * gain > 0.96:
        gain = 0.96 / peak
    pcm = np.clip(np.rint(audio * gain * 32767.0), -32768, 32767).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(path, sample_rate, pcm)


def _normalize_wav(source: Path, destination: Path) -> None:
    sample_rate, data = wavfile.read(source)
    _write_normalized(destination, int(sample_rate), data)


class InteractiveEngines:
    def __init__(self) -> None:
        self.root = PROJECT_ROOT
        self._loaded_stage: int | None = None
        self._loaded: tuple[object, ...] = ()

    def readiness(self) -> dict[int, dict[str, object]]:
        paths = {
            1: [self.root / ".tools/local/stage1/stage1_rule_frontend.exe", self.root / "vendor/klsyn/klsyn/klatt_wrap.cp311-win_amd64.pyd"],
            2: [self.root / ".tools/local/flite/bin/flite.exe"],
            3: [self.root / ".tools/local/flite_hts_engine/bin/flite_hts_engine.exe", self.root / "vendor/hts_voice_cmu_us_arctic_slt-1.06/cmu_us_arctic_slt.htsvoice"],
            4: [TORCH_HOME / "hub/checkpoints/tacotron2_english_characters_1500_epochs_ljspeech.pth"],
            5: [TORCH_HOME / "hub/checkpoints/tacotron2_english_characters_1500_epochs_wavernn_ljspeech.pth", TORCH_HOME / "hub/checkpoints/wavernn_10k_epochs_8bits_ljspeech.pth"],
            6: [TORCH_HOME / "checkpoints/nvidia_fastpitch_210824+cfg.pt", TORCH_HOME / "checkpoints/hifigan_gen_checkpoint_10000_ft.pt"],
            7: [self.root / ".venv-f5/Scripts/f5-tts_infer-cli.exe"],
        }
        result: dict[int, dict[str, object]] = {}
        for stage, required in paths.items():
            missing = [str(path.relative_to(self.root)) for path in required if not path.exists()]
            if stage == 7 and not list((HF_HOME / "hub/models--SWivid--F5-TTS/snapshots").glob("*/F5TTS_v1_Base/model_1250000.safetensors")):
                missing.append(".cache/huggingface/.../F5TTS_v1_Base/model_1250000.safetensors")
            result[stage] = {"ready": not missing, "missing": missing}
        return result

    def synthesize(self, stage: int, text: str, destination: Path) -> None:
        if stage not in STAGE_BY_ID:
            raise ValueError("未知的 TTS 階段。")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if stage == 1:
            self._stage1(text, destination)
        elif stage == 2:
            self._stage2(text, destination)
        elif stage == 3:
            self._stage3(text, destination)
        elif stage == 4:
            self._stage4(text, destination)
        elif stage == 5:
            self._stage5(text, destination)
        elif stage == 6:
            self._stage6(text, destination)
        else:
            self._stage7(text, destination)

    def _native_environment(self) -> dict[str, str]:
        env = os.environ.copy()
        cygwin_bin = self.root / ".tools/cygwin64/bin"
        env["PATH"] = str(cygwin_bin) + os.pathsep + env.get("PATH", "")
        return env

    def _run_native(self, arguments: list[str], timeout: int = 120) -> None:
        completed = subprocess.run(
            arguments,
            cwd=self.root,
            env=self._native_environment(),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if completed.returncode:
            message = (completed.stderr or completed.stdout).strip()[-1200:]
            raise RuntimeError(message or f"本機合成器結束碼：{completed.returncode}")

    @staticmethod
    def _to_cygwin_path(path: Path) -> str:
        resolved = path.resolve()
        drive = resolved.drive.rstrip(":").lower()
        remainder = resolved.as_posix()[2:]
        return f"/cygdrive/{drive}{remainder}"

    def _stage1(self, text: str, destination: Path) -> None:
        frontend = self.root / ".tools/local/stage1/stage1_rule_frontend.exe"
        jobs = self.root / "cache/jobs"
        jobs.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=jobs) as directory:
            job = Path(directory)
            text_path = job / "input.txt"
            control_path = job / "controls.csv"
            text_path.write_text(text, encoding="ascii")
            self._run_native([str(frontend), str(text_path), str(control_path)])
            controls = np.loadtxt(control_path, delimiter=",")
        tracks = self._klsyn_tracks(controls)
        audio = self._synthesize_klsyn_chunks(tracks)
        _write_normalized(destination, 16_000, audio)

    @staticmethod
    def _klsyn_tracks(source: np.ndarray) -> dict[str, np.ndarray]:
        if source.ndim != 2 or source.shape[1] != 40:
            raise RuntimeError(f"Stage 1 規則前端輸出格式錯誤：{source.shape}")
        source_times = np.arange(len(source), dtype=float) * 10.0
        output_times = np.arange(0.0, source_times[-1] + 0.1, 5.0)

        def interpolate(column: int, scale: float = 1.0, minimum: int = 0) -> np.ndarray:
            values = np.interp(output_times, source_times, source[:, column] * scale)
            return np.maximum(minimum, np.rint(values)).astype(int)

        f0 = interpolate(0, 0.1)
        open_samples = interpolate(19)
        period_samples = 11025.0 / np.maximum(f0, 60)
        oq = np.clip(np.rint(open_samples / period_samples * 100.0), 25, 45).astype(int)
        return {
            "f0": f0, "av": interpolate(1),
            "F1": interpolate(2, minimum=200), "b1": interpolate(3, minimum=40),
            "F2": interpolate(4, minimum=550), "b2": interpolate(5, minimum=40),
            "F3": interpolate(6, minimum=1200), "b3": interpolate(7, minimum=40),
            "F4": interpolate(8, minimum=1200), "b4": interpolate(9, minimum=40),
            "F5": interpolate(10, minimum=1200), "b5": interpolate(11, minimum=40),
            "f6": interpolate(12, minimum=1200), "b6": interpolate(13, minimum=40),
            "fz": interpolate(14, minimum=248), "bz": interpolate(15, minimum=40),
            "fp": interpolate(16, minimum=248), "bp": interpolate(17, minimum=40),
            "ah": interpolate(18), "oq": oq, "at": interpolate(20),
            "tl": interpolate(21), "af": interpolate(22), "sk": interpolate(23),
            "a1": interpolate(24), "p1": interpolate(25, minimum=40),
            "a2": interpolate(26), "p2": interpolate(27, minimum=40),
            "a3": interpolate(28), "p3": interpolate(29, minimum=40),
            "a4": interpolate(30), "p4": interpolate(31, minimum=40),
            "a5": interpolate(32), "p5": interpolate(33, minimum=40),
            "a6": interpolate(34), "p6": interpolate(35, minimum=40),
            "an": interpolate(36), "ab": interpolate(37), "ap": interpolate(38),
        }

    def _synthesize_klsyn_chunks(self, tracks: dict[str, np.ndarray]) -> np.ndarray:
        klsyn_root = self.root / "vendor/klsyn"
        if str(klsyn_root) not in sys.path:
            sys.path.insert(0, str(klsyn_root))
        from klsyn import klatt_wrap

        count = len(tracks["f0"])
        quiet = (tracks["av"] <= 2) & (tracks["af"] <= 2) & (tracks["ah"] <= 2) & (tracks["ap"] <= 2)
        ranges: list[tuple[int, int]] = []
        start = 0
        maximum = 950
        while count - start > maximum:
            candidates = np.flatnonzero(quiet[start + 650 : start + maximum]) + start + 650
            end = int(candidates[-1]) if candidates.size else start + maximum
            ranges.append((start, end))
            start = end
        ranges.append((start, count))

        chunks: list[np.ndarray] = []
        for start, end in ranges:
            params: dict[str, int | list[int]] = {
                "sr": 16_000, "nf": 5, "du": (end - start) * 5,
                "ss": 1, "ui": 5, "rs": 1, "g0": 55, "agc": 0,
            }
            params.update({name: values[start:end].tolist() for name, values in tracks.items()})
            synth = klatt_wrap.synthesizer()
            synth.set_params(params)
            chunk, _ = synth.synthesize()
            chunks.append(chunk)
        return np.concatenate(chunks)

    def _stage2(self, text: str, destination: Path) -> None:
        executable = self.root / ".tools/local/flite/bin/flite.exe"
        self._native_text_synthesis(
            text,
            destination,
            lambda text_path, raw_path: [
                str(self.root / ".tools/cygwin64/bin/bash.exe"),
                "-lc",
                'exec "$1" -voice kal16 -f "$2" -o "$3"',
                "tts-stage2",
                self._to_cygwin_path(executable),
                self._to_cygwin_path(text_path),
                self._to_cygwin_path(raw_path),
            ],
        )

    def _stage3(self, text: str, destination: Path) -> None:
        executable = self.root / ".tools/local/flite_hts_engine/bin/flite_hts_engine.exe"
        voice = self.root / "vendor/hts_voice_cmu_us_arctic_slt-1.06/cmu_us_arctic_slt.htsvoice"
        self._native_text_synthesis(
            text,
            destination,
            lambda text_path, raw_path: [
                str(self.root / ".tools/cygwin64/bin/bash.exe"),
                "-lc",
                'exec "$1" -m "$2" -o "$3" "$4"',
                "tts-stage3",
                self._to_cygwin_path(executable),
                self._to_cygwin_path(voice),
                self._to_cygwin_path(raw_path),
                self._to_cygwin_path(text_path),
            ],
        )

    def _native_text_synthesis(self, text: str, destination: Path, command) -> None:
        jobs = self.root / "cache/jobs"
        jobs.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=jobs) as directory:
            job = Path(directory)
            text_path = job / "input.txt"
            raw_path = job / "raw.wav"
            text_path.write_text(text, encoding="ascii")
            self._run_native(command(text_path, raw_path))
            _normalize_wav(raw_path, destination)

    def _unload_neural(self) -> None:
        self._loaded = ()
        self._loaded_stage = None
        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

    def _stage4(self, text: str, destination: Path) -> None:
        import torch
        import torchaudio
        if self._loaded_stage != 4:
            self._unload_neural()
            bundle = torchaudio.pipelines.TACOTRON2_GRIFFINLIM_CHAR_LJSPEECH
            processor = bundle.get_text_processor()
            model = bundle.get_tacotron2().to("cuda").eval()
            vocoder = bundle.get_vocoder().to("cpu")
            self._loaded = (processor, model, vocoder)
            self._loaded_stage = 4
        processor, model, vocoder = self._loaded
        processed, lengths = processor(text.lower())
        with torch.inference_mode():
            spectrogram, spec_lengths, _ = model.infer(processed.cuda(), lengths.cuda())
            waveform, _ = vocoder(spectrogram.cpu(), spec_lengths.cpu())
        _write_normalized(destination, vocoder.sample_rate, waveform[0].numpy())

    def _stage5(self, text: str, destination: Path) -> None:
        import torch
        import torchaudio
        if self._loaded_stage != 5:
            self._unload_neural()
            bundle = torchaudio.pipelines.TACOTRON2_WAVERNN_CHAR_LJSPEECH
            processor = bundle.get_text_processor()
            model = bundle.get_tacotron2().to("cuda").eval()
            # WaveRNN emits one sample at a time. On this Windows setup the many
            # tiny CUDA launches are substantially slower than a scripted CPU run.
            raw_vocoder = bundle.get_vocoder().to("cpu").eval()
            sample_rate = raw_vocoder.sample_rate
            vocoder = torch.jit.script(raw_vocoder)
            self._loaded = (processor, model, vocoder, sample_rate)
            self._loaded_stage = 5
        processor, model, vocoder, sample_rate = self._loaded
        processed, lengths = processor(text.lower())
        with torch.inference_mode():
            spectrogram, spec_lengths, _ = model.infer(processed.cuda(), lengths.cuda())
            waveform, waveform_lengths = vocoder(spectrogram.cpu(), spec_lengths.cpu())
        valid = min(int(waveform_lengths[0]), waveform.shape[-1])
        _write_normalized(destination, int(sample_rate), waveform[0, :valid].cpu().numpy())

    def _stage6(self, text: str, destination: Path) -> None:
        import torch
        if self._loaded_stage != 6:
            self._unload_neural()
            repo = "NVIDIA/DeepLearningExamples:torchhub"
            fastpitch, generator_config = torch.hub.load(repo, "nvidia_fastpitch", trust_repo=True)
            hifigan, vocoder_config, denoiser = torch.hub.load(repo, "nvidia_hifigan", trust_repo=True)
            processor = torch.hub.load(
                repo,
                "nvidia_textprocessing_utils",
                cmudict_path=str(self.root / "cache/stage6/cmudict-0.7b"),
                heteronyms_path=str(self.root / "cache/stage6/heteronyms"),
                trust_repo=True,
            )
            self._loaded = (
                fastpitch.cuda().eval(), hifigan.cuda().eval(), denoiser.cuda().eval(),
                processor, generator_config, vocoder_config,
            )
            self._loaded_stage = 6
        fastpitch, hifigan, denoiser, processor, _, vocoder_config = self._loaded
        batches = processor.prepare_input_sequence([text], batch_size=1)
        batch = batches[0]
        with torch.inference_mode():
            mel, _, *_ = fastpitch(
                batch["text"].cuda(), pace=1.0, speaker=0,
                pitch_tgt=None, pitch_transform=None,
            )
            waveform = hifigan(mel).float()
            waveform = denoiser(waveform.squeeze(1), 0.005).squeeze(1)
        _write_normalized(destination, int(vocoder_config["sampling_rate"]), waveform[0].cpu().numpy())

    def _stage7(self, text: str, destination: Path) -> None:
        self._unload_neural()
        reference = self.root / "output/comparable/reference/stage7_slt_reference.wav"
        reference_text = "This is a short reference sample for the modern synthesis system."
        if not reference.exists():
            self._stage3(reference_text, reference)
        cli = self.root / ".venv-f5/Scripts/f5-tts_infer-cli.exe"
        jobs = self.root / "cache/jobs"
        jobs.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=jobs) as directory:
            job = Path(directory)
            raw_path = job / "stage7.wav"
            env = os.environ.copy()
            env["HF_HOME"] = str(HF_HOME)
            env["TORCH_HOME"] = str(TORCH_HOME)
            completed = subprocess.run(
                [
                    str(cli), "--model", "F5TTS_v1_Base",
                    "--ref_audio", str(reference), "--ref_text", reference_text,
                    "--gen_text", text, "--output_dir", str(job),
                    "--output_file", raw_path.name, "--device", "cuda", "--nfe_step", "24",
                ],
                cwd=self.root, env=env, capture_output=True, text=True,
                timeout=600, check=False,
            )
            if completed.returncode or not raw_path.exists():
                message = (completed.stderr or completed.stdout).strip()[-1600:]
                raise RuntimeError(message or "F5-TTS 沒有產生音檔。")
            _normalize_wav(raw_path, destination)


def result_payload(stage: int, text: str, path: Path, cached: bool, elapsed: float) -> dict[str, object]:
    metadata = inspect_audio(path)
    return {
        "stage": stage,
        "text": text,
        "audio_url": f"/audio/stage{stage}/{path.name}",
        "cached": cached,
        "elapsed_seconds": round(elapsed, 2),
        **metadata,
    }
