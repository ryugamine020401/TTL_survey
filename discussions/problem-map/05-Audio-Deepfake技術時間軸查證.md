# 步驟 05：Audio Deepfake 技術時間軸第一輪查證

日期：2026-07-26  
狀態：查證完成，分期待作者確認  
上一步：`04-年份主線與技術分期.md`

## 本步問題

依照「年份作為閱讀順序、技術轉折作為年代邊界」，`Audio Deepfake` 的生成與聲音轉換技術可以如何分期？

## 查證後的邏輯修正

不能把時間軸寫成「每年選一篇最佳論文」，原因有三個：

1. TTS 與 Voice Conversion 是平行發展的兩條技術線。
2. 自然度、說話者相似度、可懂度、速度與對齊穩定性不是同一項指標。
3. 各論文的資料集與聽測設計不同，結果不能直接跨論文排名。

年代邊界表示研究重心與新能力改變，不表示舊方法在該年後立即消失。

因此使用四種標籤：

- **主流典範**：有來源明確支持曾占主導或成為主流技術家族。
- **技術轉折代表**：提出後續反覆沿用的新技術方式。
- **當時高能力代表**：只在該論文的實驗範圍內有較強結果。
- **特定穩健性代表**：明確定義 failure mode 與 robustness 指標並改善；不外推成全面穩健。

## 第一版六段時間軸

```text
1990–2003  語料拼接／Unit Selection
2004–2015  統計參數式 TTS／GMM Voice Conversion
2016–2019  神經波形／端到端 TTS／零樣本模仿
2020–2021  高速 vocoder／對齊穩健／單階段生成
2022–2023  Codec Token／Audio LM／大型 zero-shot
2024–2025  Flow Matching 簡化／Masked Generation／Scaling
```

## 各段的閱讀入口

| 年份 | 論文 | 本時間軸中的地位 |
|---|---|---|
| 1990 | Takeda et al., _On the unit search criteria..._ | Unit selection 技術前史代表 |
| 2004 | Toda, _Overview of Voice Conversion_ | 明確稱 GMM-based VC 為當時最普遍方法 |
| 2009 | Zen et al., _Statistical Parametric Speech Synthesis_ | 證實 unit selection 曾主導前十年；HMM-TTS 重要回顧 |
| 2016 | van den Oord et al., _WaveNet_ | 神經 raw-waveform 生成轉折 |
| 2017 | Wang et al., _Tacotron_ | 端到端 text-to-spectrogram |
| 2018 | Shen et al., _Tacotron 2_ | 論文內自然度接近專業錄音 |
| 2018 | Jia et al., _Transfer Learning..._ | 數秒參考音訊合成未見說話者 |
| 2019 | Qian et al., _AutoVC_ | Zero-shot voice conversion |
| 2020 | Shen et al., _Non-Attentive Tacotron_ | 對齊 failure 的特定穩健性代表 |
| 2020 | Kong et al., _HiFi-GAN_ | 高傳真、高速 vocoder |
| 2021 | Kim et al., _VITS_ | 單階段平行 TTS |
| 2022 | Borsos et al., _AudioLM_ | Semantic + acoustic token LM |
| 2023 | Wang et al., _VALL-E_ | 3 秒 prompt 的大型 codec-LM TTS；arXiv |
| 2023 | Le et al., _Voicebox_ | Flow matching、多任務 speech infilling |
| 2023/2024 | Shen et al., _NaturalSpeech 2_ | Zero-shot diffusion；ICLR 2024 |
| 2024 | Eskimez et al., _E2 TTS_ | 簡化的 fully non-autoregressive flow TTS；SLT 2024 |
| 2024 | Du et al., _CosyVoice_ | LLM token + flow matching；work in progress |
| 2025 | Wang et al., _MaskGCT_ | Peer-reviewed masked codec transformer；ICLR 2025 |

完整論據、出版狀態、限制與來源：

- `../../research/syntheses/2026-07-26-audio-deepfake-generation-technology-timeline.md`

## 尚未寫入正式問題地圖的原因

步驟 04 已約定：年代分期需先由作者確認，才加入 `problem-map.mm.md`。因此本步保留為可修改的查證草案。

## 下一個單一問題

這六個年代是否成立，並且要不要在每個年代內把 **TTS** 與 **Voice Conversion** 畫成兩條平行泳道？
