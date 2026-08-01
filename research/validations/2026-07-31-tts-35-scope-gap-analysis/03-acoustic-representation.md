# S3：聲學表示與資訊瓶頸的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：文字與波形之間的中介表示，以及表示對內容、音色、韻律、效率與可生成性的限制
- 判決限制：不把語料中的路線競爭直接解讀成完整領域缺口

## 1. 問題與範圍框線

### 核心問題

> TTS 模型應預測什麼表示，才能同時容易學習、保留必要資訊、支援高品質重建，並維持可控制與可擴展的序列長度？

### 納入

- formant／source parameters；
- 真人 speech units；
- spectrum、mel-cepstrum、F0、aperiodicity、duration；
- mel／linear spectrogram；
- raw waveform；
- flow／VAE continuous latent；
- semantic tokens、codec tokens、continuous codec latent；
- 表示中的內容、說話者、韻律、情緒、環境資訊。

### 排除

- decoder 架構本身，歸入 S4；
- 對齊取得方法，歸入 S2；
- speaker prompt 是否取得同意，歸入 S10。

## 2. 完整表示的判準

對本分析而言，一個表示 `R` 的充分性不是只有「能重建聲音」，至少包含：

```text
ContentFidelity(R)
∧ SpeakerFidelity(R)
∧ ProsodyFidelity(R)
∧ AcousticFidelity(R)
∧ Generatability(R)
∧ EfficientSequenceLength(R)
```

任何表示都可能在其中幾項較強、其他項較弱。

## 3. 證據地圖

| 時期／論文 | 核心表示 | 直接證據或限制 | 狀態 |
|---|---|---|---|
| T1-01 Klatt | formant、F0、聲源與濾波參數 | 高度可解釋與可控，但資訊由專家選定 | Verified |
| T1-05 Pearson | formant parameters＋真人 waveform components | 真人波形成分改善可懂度／自然度，顯示純參數化會丟失資訊 | Verified |
| T2-01–T2-05 | 真人錄音單元 | 局部細節完整；品質受覆蓋與接點限制 | Verified |
| T3-01–T3-05 | spectrum、F0、duration 等 vocoder parameters | 可生成、可調適，但 over-smoothing 與 vocoder artifacts 明確 | Verified |
| T4-01–T4-05 | 同類聲學參數，由 DNN／RNN 預測 | 更強模型仍受輸出空間和 vocoder 上限限制 | Verified |
| T5-01 WaveNet | raw waveform samples | 高音質但序列極長、逐 sample 生成慢 | Verified |
| T5-02 Tacotron | mel＋linear spectrogram | 減少手工特徵，但 Griffin-Lim 重建受限 | Verified |
| T5-04 Tacotron 2 | mel spectrogram | mel 作為緊湊介面，配合 WaveNet 可達高 MOS | Verified |
| T6-02 Glow-TTS | invertible flow latent／mel | 可做 likelihood 與平行生成，但受 invertibility 架構限制 | Verified |
| T6-05 VITS | posterior latent＋flow prior | 高解析 posterior 與 prior flow 對品質重要 | Verified |
| T7-01 AudioLM | semantic tokens＋coarse/fine acoustic tokens | semantic token 保長期結構；acoustic token 保 speaker／環境與重建 | Verified |
| T7-02 VALL-E | 八層 EnCodec tokens | 支援 codec LM 與 prompt cloning，但長離散序列有 AR 問題 | Verified |
| T7-03 Voicebox | mel／continuous flow state | 避免逐 token AR，支援 infilling 與多任務 | Verified |
| T7-04 NaturalSpeech 2 | continuous codec latent | 明確批評多層離散 token 的長序列與細節損失 | Verified |
| T7-05 MaskGCT | VQ semantic＋12 層 acoustic tokens | VQ 優於 k-means，主張改良 tokenizer＋masked NAR 可保留離散路線 | Verified |

## 4. 命題鏈

### 命題 A：表示選擇會建立不可逆的資訊上限

1. Pearson 的混合系統顯示，只調聲學參數不等於保留真人波形中的全部可感知資訊。
2. HMM／DNN-SPSS 的 over-smoothing 表明條件平均與參數空間會移除細節。
3. Tacotron 2 顯示同一 mel 介面搭配更強 waveform model 可大幅改善品質。
4. T7 再將資訊分成 semantic、acoustic、speaker／environment 或 continuous latent。

**Inference**

```text
若資訊在表示 R 中被移除，
則任意 decoder D 都無法由 R 唯一恢復該資訊。
```

這是資訊瓶頸推論；它不表示所有可感知差異都能以現有指標量到。

### 命題 B：可壓縮、可生成與可重建是不同目標

- raw waveform 容量高，但序列極長；
- mel 較緊湊且容易條件生成，但需 decoder 補回相位與細節；
- codec tokens 便於語言模型化，但層數與序列長度增加；
- continuous latent 避免離散量化，卻通常需 diffusion／flow 反覆生成。

因此：

```text
EasyToReconstruct(R) ↛ EasyToGenerate(R)
EasyToGenerate(R) ↛ CompleteInformation(R)
Compact(R) ↛ PerceptuallySufficient(R)
```

### 命題 C：T7 內部存在可驗證的路線衝突

1. VALL-E：離散 codec token 讓 TTS 可改寫成 conditional language modeling。
2. NaturalSpeech 2：多層離散 token 造成長序列、量化細節損失與 AR error propagation。
3. MaskGCT：離散 token 的問題可由更佳 tokenizer 與 masked NAR 緩解。

三者不能直接形成邏輯矛盾，因為資料、模型、decoder 與訓練目標不同；但它們對「限制來自離散表示本身，還是來自生成方法」提出競爭解釋。

## 5. 候選缺口推導

### G1：離散 token、連續 latent 與 mel 表示缺少條件匹配的聯合比較

**前提**

- 三條路線都聲稱其表示有助於品質、穩定性或效率；
- 各完整系統同時更換資料量、模型規模、decoder、對齊及目標函數；
- 跨論文 MOS、WER、speaker similarity 與延遲不可直接排名。

**推導**

```text
Outcome = f(Representation, Generator, Decoder, Data, Compute, Evaluation)
各論文同時改變多個自變數
→ 不能將 Outcome 差異單獨歸因於 Representation
```

**判決：Supported closed-corpus gap（causal attribution gap）**

### G2：表示所承載屬性的可分離性不足

**前提**

- AudioLM 顯示 semantic 與 acoustic token 承載不同資訊；
- VALL-E prompt 可同時保留 speaker、環境、情緒；
- Voicebox 明示 prompt 屬性不能任意拆分；
- NaturalSpeech 2／MaskGCT 同樣以 prompt 或 token 混合多種條件。

**推導**

```text
PromptRepresentation = Content + Timbre + Accent + Prosody + Emotion + Channel
∧ 使用者常只想指定其中一部分
∧ 35 篇沒有建立完整的 factor-wise intervention
→ 表示的屬性可分離性未被充分驗證
```

**判決：Supported closed-corpus gap（representation + measurement gap）**

### G3：表示中的不可逆資訊損失是否可預測

語料提供個別重建或下游結果，但沒有建立「表示失真 → 特定感知／身份／偵測失敗」的一般預測模型。

**判決：Search lead only**

此問題可能超出 TTS 生成論文的原始任務，必須外部搜尋。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「沒有人比較離散與連續表示」 | 拒絕 | NaturalSpeech 2 明確提出對離散 token 的批評；MaskGCT 提供相反方向證據 |
| 「離散 token 一定較差」 | Unknown | MaskGCT 顯示 tokenizer 與生成方法會改變結論 |
| 「continuous latent 一定較慢」 | Unknown | 延遲也受 solver、步數、硬體與實作影響 |
| 「mel 已被淘汰」 | 拒絕 | Voicebox 等晚期工作仍使用連續聲學介面 |
| 「存在一個公認最佳表示」 | No evidence | 35 篇反而支持多目標取捨 |

## 7. 最終判決

- **Verified：** 表示從專家參數、真人片段、vocoder parameters、spectrogram 演進到 token／latent，但沒有單向收斂。
- **Inference：** 表示是 TTS 的可達上限與失敗型態之一，不只是工程介面。
- **Supported closed-corpus gap：** 缺少在固定資料、generator、decoder 與算力下，對離散 token、連續 latent、mel 的多目標比較。
- **Supported closed-corpus gap：** prompt／token／latent 中 timbre、accent、prosody、emotion、channel 的可分離性未被完整干預驗證。
- **No-gap verdict：** 「是否已有離散、連續及 spectrogram 表示」沒有缺口；缺的是可歸因比較，而不是新表示名稱。

## 8. 下一個最小驗證步驟

1. 搜尋 matched representation benchmark 與 neural codec ablation。
2. 優先找同資料、同參數量、同 decoder 或可互換 decoder 的研究。
3. 要求至少分別量測 content、speaker、prosody、environment、reconstruction、latency。
4. 若已有充分 matched comparison，取消 G1；若只有完整系統 leaderboard，G1 仍保留為較窄的因果歸因問題。

**停止條件**

> 若現有文獻已在相同訓練資料、算力、條件輸入和解碼預算下，對主要表示家族完成多維度評估及屬性干預，則本範圍判為沒有可保留缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T1-01、T1-05、T3-01 至 T3-05、T5-01、T5-02、T5-04、T6-02、T6-05、T7-01 至 T7-05

## 10. 專案狀態影響

不修改專案方向。G1、G2 是外部驗證候選，尚不能視為已成立的 thesis gap。
