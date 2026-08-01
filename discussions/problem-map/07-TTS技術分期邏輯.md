# 步驟 07：TTS 技術分期的邏輯

日期：2026-07-26  
狀態：分期已確認；單篇代表論文與年代邊界由步驟 08 精簡修正  
上一步：`06-TTS與VC雙主軸.md`

## 本步問題

TTS 的歷史應依什麼技術轉折分期，才不會把模型元件、生成能力與完整 TTS 架構混為一談？

## 結論

TTS 時間軸使用兩層資訊：

### 主時間軸：生成機制

觀察文字如何被轉換成最終波形：

```text
文字
→ 語言／音素表示
→ 時長與對齊
→ 聲學表示
→ 波形
```

當其中的主要表示方式、對齊方法或生成方式改變，才構成新的歷史階段。

### 次要標記：能力變化

以下能力標在年代旁邊，但不單獨構成年代：

- 自然度與可懂度；
- 推論速度；
- 漏字、重複與長文本穩定性；
- 單說話者、多說話者與 speaker adaptation；
- zero-shot voice cloning；
- 多語、情緒、韻律與 streaming；
- 訓練資料與模型規模。

## 為什麼必須分成兩層

- **WaveNet、HiFi-GAN** 主要解決波形生成／vocoder，不等於完整的 text-to-speech pipeline。
- **Zero-shot cloning** 是系統能力，可以由 speaker encoder、codec language model、diffusion 或 flow matching 等不同架構實現。
- **Robustness** 必須說明是哪種 failure mode，例如漏字、重複、錯誤對齊、長文本失敗或 noisy prompt；不能只寫「更穩健」。

## 第一版 TTS 分期

> 年代邊界表示研究重心改變，不代表舊方法立即消失。部分技術在前一階段末期已出現，之後才成為重要研究路線。

### T0. 1990 年以前：Rule／Formant Synthesis 前史

- 由人工語音規則預測控制 formant synthesizer 的聲學參數。
- 可控制但機械感明顯；與現代資料驅動 deepfake 的直接關係較弱。
- 本問題地圖只保留一個背景節點，不展開完整機械語音史。

### T1. 1990–2004：Concatenative／Unit Selection

- 從真人語料庫選擇並串接語音片段。
- 代表入口：
  - **1990 — Takeda et al., _On the unit search criteria and algorithms for speech synthesis using non-uniform units_**
- 主流證據：
  - 2000 年研究指出 concatenative synthesis 已是商業 TTS 的主導技術。
  - Zen et al. 2009 回顧指出 unit-selection synthesis 主導了先前十年的 speech synthesis。
- 主要限制：依賴大型指定說話者語料庫，跨說話者與風格控制困難，可能出現拼接不連續。

來源：

- [Takeda et al., ICSLP 1990](https://www.isca-archive.org/icslp_1990/takeda90_icslp.html)
- [Zen, Tokuda, Black, 2009](https://pure.nitech.ac.jp/en/publications/statistical-parametric-speech-synthesis-2/)

### T2. 2005–2015：Statistical Parametric TTS，從 HMM 到 DNN

- 以統計模型預測頻譜、基頻與時長，再由 vocoder 重建波形。
- HMM 技術在 1990 年代末已成形，2002 年 HTS toolkit 公開；2009 年資料指出 HMM-based synthesis 在先前數年逐漸流行。
- 2013 年 DNN 取代 HMM decision-tree acoustic mapping，但整體「文字→聲學參數→vocoder」管線仍屬 statistical parametric paradigm，因此不另切一個年代。
- 代表入口：
  - **1999 — Yoshimura et al., _Simultaneous modeling of spectrum, pitch and duration in HMM-based speech synthesis_**
  - **2005 — Toda & Tokuda, _Speech parameter generation algorithm considering global variance..._**
  - **2013 — Zen, Senior, Schuster, _Statistical Parametric Speech Synthesis Using Deep Neural Networks_**
- 主要改善：較小資料量、可控制、容易做 speaker adaptation。
- 主要限制：過度平滑與 vocoder 音色，自然度通常落後大型 unit-selection。

來源：

- [Yoshimura et al., Eurospeech 1999](https://www.isca-archive.org/eurospeech_1999/yoshimura99_eurospeech.html)
- [Toda & Tokuda, Interspeech 2005](https://www.isca-archive.org/interspeech_2005/toda05b_interspeech.html)
- [Zen et al., ICASSP 2013](https://research.google/pubs/statistical-parametric-speech-synthesis-using-deep-neural-networks/)
- [HTS 發展與流行度，Zen et al. 2009](https://www.research.ed.ac.uk/en/publications/a01bb759-bbbc-46b4-b4ab-10dd3e699ca1/)

### T3. 2016–2018：Neural End-to-End、Autoregressive TTS

- 神經模型直接產生波形，或由文字端到端預測 mel spectrogram。
- 代表入口：
  - **2016 — WaveNet**：raw-waveform neural generation。
  - **2017 — Tacotron**：character-to-spectrogram end-to-end TTS。
  - **2018 — Tacotron 2**：Tacotron acoustic model + WaveNet vocoder。
- 能力支線：
  - **2018 — Jia et al.**：以數秒參考音訊對未見說話者合成，代表 zero-shot speaker cloning 能力出現。
- 主要改善：自然度大幅提高、減少手工 pipeline。
- 主要限制：自回歸推論慢；attention 可能漏字、重複或對齊失敗。

來源：

- [WaveNet, 2016](https://deepmind.google/blog/wavenet-a-generative-model-for-raw-audio/)
- [Tacotron, Interspeech 2017](https://research.google/pubs/tacotron-towards-end-to-end-speech-synthesis/)
- [Tacotron 2, ICASSP 2018](https://research.google/pubs/natural-tts-synthesis-by-conditioning-wavenet-on-mel-spectrogram-predictions/)
- [Jia et al., NeurIPS 2018](https://research.google/pubs/transfer-learning-from-speaker-verification-to-multispeaker-text-to-speech-synthesis/)

### T4. 2019–2021：Parallel／Non-Autoregressive 與 Single-stage TTS

- 研究焦點轉向平行生成、明確時長、穩定對齊與縮短兩階段 pipeline。
- 代表入口：
  - **2019 — FastSpeech**：平行 text-to-spectrogram、length regulator；在其 50 個困難句測試中消除漏字／重複，mel generation 相對 autoregressive Transformer TTS 加速 270 倍。
  - **2020 — Glow-TTS**：flow + monotonic alignment search，不需外部 autoregressive aligner。
  - **2020 — HiFi-GAN**：高速高傳真 vocoder；它是重要元件，不單獨代表完整 TTS 架構。
  - **2021 — VITS**：VAE + flow + adversarial learning，單階段、平行 end-to-end TTS。
- 主要改善：速度、對齊、長文本與部署可行性。
- 主要限制：品質、韻律、speaker generalization 與 robustness 證據仍高度依賴各自資料集。

來源：

- [FastSpeech, NeurIPS 2019](https://proceedings.neurips.cc/paper/2019/hash/f63f65b503e22cb970527f23c9ad7db1-Abstract.html)
- [Glow-TTS, NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/file/5c3b99e8f92532e5ad1556e53ceea00c-Paper.pdf)
- [HiFi-GAN, NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/hash/c5d736809766d46260d816d8dbc9eb44-Abstract.html)
- [VITS, ICML 2021](https://proceedings.mlr.press/v139/kim21f.html)

### T5. 2022–現在：Large-scale Zero-shot／Foundation-style TTS

- 大規模多說話者資料與短音訊 prompt 讓 zero-shot personalized TTS 成為核心設定。
- 這是一個系統能力與規模共同轉折的年代，內部至少有三條並行生成家族：
  1. **Codec-token autoregressive LM**
  2. **Diffusion／flow matching**
  3. **Masked non-autoregressive generation**
- 代表入口：
  - **2023 — VALL-E**：60K 小時、3 秒 prompt 的 neural-codec language model；arXiv。
  - **2023 預印本／2024 ICLR — NaturalSpeech 2**：codec latent + diffusion。
  - **2024 — E2 TTS**：簡化的 fully non-autoregressive flow-matching TTS；SLT 2024。
  - **2025 — MaskGCT**：masked generative codec transformer；ICLR 2025。
- 主要改善：zero-shot speaker similarity、多語、規模化與任務整合。
- 主要限制：不同模型與 benchmark 不可直接排名；目前沒有足夠證據把單一模型稱為 2022–現在全領域最流行或最穩健。

來源：

- [VALL-E, Microsoft Research 2023](https://www.microsoft.com/en-us/research/publication/neural-codec-language-models-are-zero-shot-text-to-speech-synthesizers/)
- [NaturalSpeech 2, ICLR 2024](https://www.microsoft.com/en-us/research/publication/naturalspeech-2-latent-diffusion-models-are-natural-and-zero-shot-speech-and-singing-synthesizers/)
- [E2 TTS, SLT 2024](https://arxiv.org/abs/2406.18009)
- [MaskGCT, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/74a31a3b862eb7f01defbbed8e5f0c69-Abstract-Conference.html)

## 壓縮後的 TTS 時間軸

```text
前史          Rule／Formant synthesis
1990–2004    Concatenative／Unit Selection
2005–2015    Statistical Parametric：HMM → DNN
2016–2018    Neural End-to-End／Autoregressive
2019–2021    Parallel／Non-Autoregressive／Single-stage
2022–現在     Large-scale Zero-shot／Foundation-style
```

## 證據狀態

- **Verified：** 各代表論文的年份、出版狀態與上述原論文內部結果。
- **Verified：** Unit selection 曾主導一段時期；HMM-based TTS 在 2000 年代逐漸流行。
- **Inference：** 將連續發展壓縮成上述五個主要年代加一個前史節點。
- **Unknown：** 2022 年後哪個單一架構家族具有跨語言、跨資料與跨任務的最高採用度或全面穩健性。

## 反證與限制

- HMM-TTS 在 1999 年已出現，因此 2005 是「研究重心轉移」的近似邊界，不是發明年份。
- Zero-shot speaker cloning 在 2018 年已出現，因此不能把 zero-shot 完全說成 2022 年才誕生；2022 年後的轉折是大規模化、短 prompt 與 foundation-style 系統化。
- WaveNet、HiFi-GAN 等 vocoder 對品質非常重要，但若只按照 vocoder 分期，會與 acoustic model 的發展混在一起。
- 現代模型可能跨越 TTS、VC 與 speech editing，T5 不是互斥的架構分類。

## 後續

作者已確認分期方向。步驟 08 改以「世代起點」呈現，並將每一代精簡為一篇真正改變核心生成方式的代表論文。
