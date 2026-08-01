# 步驟 08：TTS 世代轉折與單篇代表論文

日期：2026-07-26  
狀態：已確認的分期之精簡版；步驟 09 補入 2013 橋接世代  
上一步：`07-TTS技術分期邏輯.md`

## 本步問題

如何讓 TTS 時間軸的每一個世代只保留一篇代表論文，同時清楚說明「為什麼這項轉變足以開啟新世代」？

## 表示方法

不再把年代寫成精確、互不重疊的統治區間，而改用：

```text
世代起點年份
→ 代表論文
→ 上一代的核心做法
→ 被改變的核心環節
→ 為什麼形成新世代
```

原因是新舊方法會長期共存。「起點年份」代表新生成典範出現，不代表舊方法在該年消失。

代表論文的選擇標準：

1. 改變完整 TTS pipeline 的核心生成方式，而不只是改善單一指標；
2. 能清楚區別上一代與下一代；
3. 有可查證的原始論文與出版年份；
4. 一個世代只保留一篇，其他重要論文之後放在延伸閱讀，不進主時間軸。

**代表論文不等於該年代唯一重要或絕對最流行的論文。**

## TTS 六個世代（原精簡版）

> 後續查證顯示，2000–2017 之間不應視為單一 HMM 階段。步驟 09 已補入 2013 Neural Statistical Parametric 橋接世代，正式時間軸目前共有七個節點。

### 世代 0：1980 — Rule／Formant Synthesis

**代表論文**

Dennis H. Klatt, **_Software for a Cascade/Parallel Formant Synthesizer_**, Journal of the Acoustical Society of America, 1980.  
DOI：[10.1121/1.383940](https://doi.org/10.1121/1.383940)

**上一代／當時的核心做法**

利用人工建立的語音規則與聲學知識，指定基頻、formant、頻寬與音源等參數，再由聲道模型合成波形。

**開啟新世代的轉變**

把人類發聲機制抽象成一套可程式控制的聲學參數模型，使電腦能根據規則產生任意語音，而不只是播放預先錄好的單字。

**為什麼獨立成一代**

這一代的核心是：

```text
人類知識與規則 → 聲學參數 → 合成波形
```

後續所有資料驅動方法，都是在回答「能否不要靠人工逐條寫規則」。

**主要限制**

需要大量專家知識；雖可控制，聲音通常具有明顯機械感。它是 TTS 技術前史，尚不是現代 deepfake 的主要來源。

---

### 世代 1：1996 — Concatenative／Unit Selection

**代表論文**

Andrew J. Hunt and Alan W. Black, **_Unit Selection in a Concatenative Speech Synthesis System Using a Large Speech Database_**, ICASSP 1996.  
原始論文：[University of Edinburgh Research Archive](https://era.ed.ac.uk/items/07a1382d-ac96-4894-8532-b6c8eac44aad)

**上一代的核心問題**

Rule／formant synthesis 必須用人工規則近似真人聲道與語音細節，難以產生自然的人聲質感。

**開啟新世代的轉變**

不再從零合成聲學細節，而是從大型真人語音庫中，依 target cost 與 concatenation cost 搜尋最合適的語音單元，再串接成新句子。

**為什麼形成新世代**

生成邏輯從：

```text
人工規則產生聲音
```

改成：

```text
從真人錄音資料庫搜尋並重組聲音
```

這使自然度大幅受益於真人錄音本身。2009 年的領域回顧指出，unit selection 主導了先前約十年的 speech synthesis。

**主要限制**

聲音受限於指定說話者語料庫；未涵蓋的音素環境、韻律或風格容易產生不自然拼接，建立新聲音需要重新錄製大型語料。

---

### 世代 2：2000 — Statistical Parametric／HMM-based TTS

**代表論文**

Keiichi Tokuda et al., **_Speech Parameter Generation Algorithms for HMM-Based Speech Synthesis_**, ICASSP 2000.  
DOI：[10.1109/ICASSP.2000.861820](https://doi.org/10.1109/ICASSP.2000.861820)  
作者保存的原始論文：[Nagoya Institute of Technology](https://www.sp.nitech.ac.jp/~tokuda/selected_pub/pdf/conference/tokuda_icassp2000.pdf)

**上一代的核心問題**

Unit selection 必須保存並搜尋大量真人片段；系統難以平滑控制說話者、音高、時長與風格，也受資料庫覆蓋率限制。

**開啟新世代的轉變**

以 HMM 學習文字條件下的頻譜、基頻與時長分布，再從模型產生完整聲學參數軌跡，最後交給 vocoder 重建波形。

**為什麼形成新世代**

生成邏輯從：

```text
搜尋並拼接現成波形
```

改成：

```text
從資料學得機率模型 → 預測聲學參數 → 生成新波形
```

聲音第一次主要儲存在「模型參數」而非「大量待拼接的錄音片段」中，因此更容易做 speaker adaptation、語速與聲學特徵控制。

**主要限制**

統計平均容易造成過度平滑，vocoder 也帶來明顯音色。2013 年 DNN acoustic model 雖改善 HMM mapping，但仍沿用「預測聲學參數→vocoder」的核心 pipeline，因此列為本世代內部演進，不另開一代。

**年代修正**

先前使用 2005 作為邊界過晚。HMM 統一建模在 1999 年已出現，核心 parameter-generation 論文發表於 2000 年，HTS toolkit 於 2002 年公開；因此把此世代起點修正為 **2000**。

---

### 世代 3：2017 — Neural End-to-End／Autoregressive TTS

**代表論文**

Yuxuan Wang et al., **_Tacotron: Towards End-to-End Speech Synthesis_**, Interspeech 2017.  
原始出版頁：[Google Research](https://research.google/pubs/tacotron-towards-end-to-end-speech-synthesis/)

**上一代的核心問題**

Statistical parametric TTS 仍需人工設計文字分析、語言特徵、duration、acoustic model 與 vocoder 介面；多階段系統容易累積誤差，輸出也受過度平滑限制。

**開啟新世代的轉變**

Tacotron 使用 sequence-to-sequence attention，直接從字元序列預測 spectrogram；訓練只需要配對的文字與音訊，不再依賴大量手工語言／聲學特徵設計。

**為什麼形成新世代**

生成邏輯從：

```text
人工設計特徵 + 分開訓練的多階段模型
```

改成：

```text
文字字元 → 單一神經網路學習對齊與聲學表示
```

核心突破不是「第一次使用神經網路」，而是把文字到聲學表示的 pipeline 端到端學習。Tacotron 在原論文中取得 MOS 3.82，優於其 production parametric baseline。

**主要限制**

自回歸生成速度慢；attention 對齊可能造成漏字、重複與長句失敗。WaveNet 2016 是重要的 neural waveform 前驅，但主要處理波形生成，因此不取代 Tacotron 作為完整 TTS 世代代表。

**年代修正**

先前以 2016–2018 表示整段神經轉折；現在主時間軸以完整 end-to-end TTS 的代表作 **Tacotron 2017** 作為世代起點。

---

### 世代 4：2019 — Parallel／Non-Autoregressive TTS

**代表論文**

Yi Ren et al., **_FastSpeech: Fast, Robust and Controllable Text to Speech_**, NeurIPS 2019.  
原始出版頁：[NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2019/hash/f63f65b503e22cb970527f23c9ad7db1-Abstract.html)

**上一代的核心問題**

Tacotron 類模型逐幀自回歸生成，推論慢；attention 可能對錯位置，造成漏字、重複或無法穩定處理困難句。

**開啟新世代的轉變**

FastSpeech 使用 feed-forward Transformer、duration predictor 與 length regulator，先決定每個音素的時長，再平行產生完整 spectrogram。

**為什麼形成新世代**

生成邏輯從：

```text
逐幀生成，下一幀依賴上一幀
```

改成：

```text
明確預測時長 → 所有聲學幀平行生成
```

這不只是加速技巧，也改變對齊方式。原論文在 LJSpeech 上報告：mel generation 相對 autoregressive Transformer TTS 加速 270 倍，並在其 50 個困難句測試中消除漏字與重複。

**主要限制**

第一代 FastSpeech 仍依賴 autoregressive teacher 提供 alignment，且音質、韻律與 robustness 證據限於其資料與測試。後續 Glow-TTS、VITS 等方法移除外部 aligner或整合單階段生成，但屬本世代的延伸。

---

### 世代 5：2023 — Codec Language Model／Large-scale Zero-shot TTS

**代表論文**

Chengyi Wang et al., **_Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers_（VALL-E）**, arXiv, 2023.  
官方研究頁：[Microsoft Research](https://www.microsoft.com/en-us/research/publication/neural-codec-language-models-are-zero-shot-text-to-speech-synthesizers/)

**上一代的核心問題**

前一代多半直接回歸連續 spectrogram，並為特定資料、語言或說話者設定訓練；要適應未見說話者，通常仍需額外 speaker encoder、微調或專門設計。

**開啟新世代的轉變**

VALL-E 先用 neural audio codec 把語音離散化為 tokens，再把 TTS 定義成 conditional language modeling。模型以 60K 小時資料預訓練，使用 3 秒未見說話者錄音作為 acoustic prompt。

**為什麼形成新世代**

生成邏輯從：

```text
文字 → 連續聲學特徵回歸
```

改成：

```text
文字 + 聲音提示 → 像語言模型一樣預測離散語音 tokens
```

這同時改變：

1. **語音表示**：連續 spectrogram → discrete codec tokens；
2. **訓練方式**：任務模型 → 大規模預訓練；
3. **說話者適應**：專門訓練／額外模組 → in-context acoustic prompt；
4. **能力**：數秒音訊即可對未見說話者合成個人化語音。

因此它比單純提高 MOS 更接近 foundation-style TTS 的世代轉折。

**主要限制**

VALL-E 的出版狀態是 **arXiv 預印本，不是 peer-reviewed conference paper**；原論文的 SOTA 結論也只適用於其比較設定。若時間軸日後限定只能使用 peer-reviewed 代表作，可改用較晚的 MaskGCT（ICLR 2025），但那代表此世代的成熟，而不是最早轉折。

**年代修正**

2022 AudioLM 是 codec-token audio language modeling 的重要前驅，但它不是以文字為輸入的 TTS 系統。因此 TTS 主時間軸從 **VALL-E 2023** 開始此世代，不從 2022 開始。

## 原精簡時間軸

| 世代起點 | 世代名稱 | 唯一代表論文 | 開創世代的核心轉變 |
|---|---|---|---|
| 1980 | Rule／Formant | Klatt (1980) | 人工規則控制聲學參數來合成波形 |
| 1996 | Unit Selection | Hunt & Black (1996) | 從合成聲學參數轉為搜尋、重組真人錄音 |
| 2000 | Statistical Parametric | Tokuda et al. (2000) | 從儲存波形轉為學習機率模型並產生聲學參數 |
| 2017 | Neural End-to-End | Tacotron (2017) | 從手工多階段 pipeline 轉為字元到聲學表示的端到端學習 |
| 2019 | Parallel／Non-AR | FastSpeech (2019) | 從逐幀生成轉為明確時長與平行生成 |
| 2023 | Codec LM／Large-scale Zero-shot | VALL-E (2023) | 從連續回歸轉為 codec-token LM 與聲音 prompt 的 in-context synthesis |

## 世代之間的因果鏈

```text
人工規則很難重現真人細節
→ 改用真人錄音片段

錄音片段難以控制、擴充與跨說話者
→ 改用統計模型產生聲學參數

統計 pipeline 手工階段多、輸出過度平滑
→ 改用端到端神經網路

自回歸神經網路慢且對齊不穩
→ 改用明確時長與平行生成

平行模型仍多為特定任務／說話者，聲學表示仍是連續回歸
→ 改用大規模 codec-token language model 與短聲音 prompt
```

## 證據狀態

- **Verified：** 六篇代表論文的書目、出版年份與各自提出的核心方法。
- **Verified：** Tacotron、FastSpeech 與 VALL-E 對上一代問題及本身方法轉變的描述。
- **Inference：** 將連續且重疊的 TTS 發展壓縮成六個教學用世代。
- **Unknown：** VALL-E 之後哪一個架構會長期成為主要典範；目前 codec LM、diffusion／flow 與 masked generation 仍在並行。

## 後續

步驟 09 查證 2000–2017 的演進並加入 2013 DNN-based statistical parametric 橋接世代。正式 Markmap 以步驟 09 的七節點版本為準。
