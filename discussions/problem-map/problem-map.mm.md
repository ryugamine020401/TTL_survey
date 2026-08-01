---
markmap:
  colorFreezeLevel: 1
---

# Audio Deepfake Detection

## H1 歷史分支

- 問題：音訊偽造與其偵測問題，如何共同演變成今天的 Deepfake Audio Detection？

### A. Audio Deepfake 的發展

- 什麼樣的音訊偽造逐漸變得可能？
- 呈現順序：年份／歷史階段
- 分期依據：主流生成與修改技術發生轉折
- 每個階段：代表性方法＋代表論文＋相對前一階段的改變

#### A1. TTS 發展線

- 輸入：文字
- 輸出：新生成的語音內容
- 追蹤：生成機制、自然度、說話者控制、zero-shot cloning、效率與穩定性

##### 1980｜Rule／Formant

- 代表論文：Klatt (1980), *Software for a Cascade/Parallel Formant Synthesizer*
- 世代轉變：以人工規則控制聲學參數來合成波形

##### 1996｜Concatenative／Unit Selection

- 代表論文：Hunt & Black (1996), *Unit Selection in a Concatenative Speech Synthesis System Using a Large Speech Database*
- 世代轉變：從人工合成聲學細節，改為搜尋與重組真人錄音片段

##### 2000｜Statistical Parametric

- 代表論文：Tokuda et al. (2000), *Speech Parameter Generation Algorithms for HMM-Based Speech Synthesis*
- 世代轉變：從儲存與拼接波形，改為學習機率模型並產生聲學參數

##### 2013｜Neural Statistical Parametric（橋接世代）

- 代表論文：Zen et al. (2013), *Statistical Parametric Speech Synthesis Using Deep Neural Networks*
- 世代轉變：以 DNN 取代 HMM／decision-tree acoustic mapping
- 延續性：仍預測 acoustic parameters，並由獨立 vocoder 產生波形

##### 2017｜Neural End-to-End

- 代表論文：Wang et al. (2017), *Tacotron: Towards End-to-End Speech Synthesis*
- 世代轉變：從手工多階段 pipeline，改為字元到聲學表示的端到端學習

##### 2019｜Parallel／Non-Autoregressive

- 代表論文：Ren et al. (2019), *FastSpeech: Fast, Robust and Controllable Text to Speech*
- 世代轉變：從逐幀自回歸生成，改為明確時長與平行生成

##### 2023｜Codec LM／Large-scale Zero-shot

- 代表論文：Wang et al. (2023), *Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers*（VALL-E；arXiv）
- 世代轉變：從連續聲學特徵回歸，改為 codec-token language modeling 與聲音 prompt

#### A2. Voice Conversion 發展線

- 輸入：來源語音
- 輸出：保留內容、改變說話者或風格的語音
- 追蹤：映射方式、平行／非平行資料、any-to-any、zero-shot 與即時性

#### A3. 跨路線與邊界

- editing／inpainting／splicing／partial fake：描述修改方式，底層可使用 TTS、VC 或混合模型
- generalist speech model：可能同時支援 TTS、VC 與編輯，以跨線節點表示
- replay／codec／channel／laundering：不是生成主軸，留到 threat model 與共同演化層

### B. Detection 的發展

- 人們如何辨識、驗證與評估音訊偽造？

### C. 兩者的共同演化

- 新的偽造能力破壞了哪些偵測假設？
- Detection 如何回應？
