# S4：波形生成與聲碼器的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：從聲學表示或 latent 產生最終 waveform 的機制、品質、速度、泛化及失真
- 判決限制：生成論文選樣不等於完整 neural vocoder survey

## 1. 問題與範圍框線

### 核心問題

> 當上游已提供聲學條件後，哪種 waveform renderer 能在高保真、低延遲、跨說話者／跨領域與可部署性間取得可驗證的平衡？

### 納入

- formant synthesizer、source-filter renderer；
- traditional parametric vocoder；
- Griffin–Lim；
- WaveNet 類 autoregressive neural vocoder；
- GAN、flow、diffusion waveform generation；
- waveform decoder、codec decoder；
- decoder artifacts、速度、模型大小、unseen speaker 泛化。

### 排除

- 上游文字表示，歸入 S1；
- mel、token、latent 本身的資訊充分性，歸入 S3；
- waveform artifact 是否可被偵測器利用，主要歸入 S10。

## 2. 充分解法的條件

```text
HighFidelity
∧ LowLatency
∧ StableTraining
∧ CrossSpeakerAndDomainGeneralization
∧ SmallDeploymentCost
```

任何只在單一說話者、單一 mel 分布或單一硬體上成立的結果，都不能推出普遍 decoder 優勢。

## 3. 證據地圖

| 論文 | 波形機制 | 直接結果／限制 | 狀態 |
|---|---|---|---|
| T1-01 Klatt | cascade／parallel formant synthesizer | 可解釋可控，但自然度受參數與理論限制 | Verified |
| T1-05 Pearson | formant＋真人 waveform components | 混合真人成分改善結果，反映純 formant 上限 | Verified |
| T3-05 SPSS Review | parametric vocoder | vocoder 被列為 SPSS 三大退化來源之一 | Verified |
| T4-01 Zen DNN | 傳統 MLPG／vocoder pipeline | DNN 改善 acoustic mapping，仍受既有 renderer 限制 | Verified |
| T5-01 WaveNet | sample-level autoregressive waveform model | 高 MOS；sample-by-sample 推論極慢 | Verified |
| T5-02 Tacotron | Griffin–Lim | text-to-spectrogram 可行，但 waveform artifacts 明確 | Verified |
| T5-04 Tacotron 2 | mel-conditioned WaveNet | ablation 顯示 WaveNet 顯著優於 Griffin–Lim | Verified |
| T6-03 HiFi-GAN | convolutional GAN＋multi-period／scale discriminators | 高品質、快速、小模型，並測 unseen speaker | Verified |
| T6-04 DiffWave | iterative denoising diffusion | 品質可匹配 WaveNet且較快，但仍慢於強 flow vocoder | Verified |
| T6-05 VITS | HiFi-GAN-style decoder 與 acoustic latent 聯合訓練 | 減少兩階段 mismatch，接近 ground truth MOS | Verified |
| T7-01／T7-02 | SoundStream／EnCodec decoder | 支援 token LM 與高保真重建，但帶入 codec 失真與多層 token | Verified |
| T7-03 Voicebox | mel＋HiFi-GAN | 晚期通用模型仍使用可分離 waveform decoder | Verified |
| T7-04 NaturalSpeech 2 | codec encoder／decoder＋latent diffusion | 以 continuous latent 避免長離散 token；多步推論仍有限制 | Verified |
| T7-05 MaskGCT | acoustic codec decoder | decoder 依賴多層 acoustic token 品質 | Verified |

## 4. 命題推導

### 命題 A：waveform renderer 可成為完整系統的品質天花板

1. HMM／DNN-SPSS 即使改善 acoustic model，仍反覆指出 vocoder artifacts。
2. Tacotron 與 Tacotron 2 的主要差異之一是 Griffin–Lim 與 WaveNet。
3. Tacotron 2 的 ablation 直接支持 WaveNet 對結果的貢獻。

因此：

```text
ImprovedAcousticModel ↛ HighWaveformQuality
HighWaveformQuality requires AdequateRenderer
```

### 命題 B：高保真、低延遲與部署成本形成多目標取捨

- WaveNet：高品質、低平行性；
- HiFi-GAN：高平行性與小 footprint，但依賴 adversarial training 與 discriminator bias；
- DiffWave：穩定生成且品質高，但需多步反向過程；
- codec decoder：壓縮與通用 token 介面，但品質受 tokenizer／codebook／decoder 共同限制。

```text
BestQualityUnderOneCondition
↛
BestQualityLatencyRobustnessUnderAllConditions
```

### 命題 C：「端到端」沒有消除 waveform rendering

VITS 聯合訓練 acoustic latent 與 decoder；T7 又使用凍結或預訓練 codec decoder。即使端到端訓練，最後仍有將內部表示映射成 waveform 的生成機制。

**Inference**

> 問題從「是否有 vocoder」改為「renderer 是否與上游共同訓練、其表示是否固定，以及誤差如何跨模組傳遞」。

## 5. 候選缺口推導

### G1：主要 waveform generator 家族缺少匹配條件的品質—速度—泛化比較

**前提**

- WaveNet、GAN、diffusion、flow／codec decoder 均提供強結果；
- 評估資料、mel／latent condition、sample rate、硬體、模型大小及 real-time factor 不同；
- 35 篇不能直接用 MOS 或速度數字跨論文排序。

**推導**

```text
若 Conditioning、Data、Hardware、ModelSize 不相同，
則 ObservedDecoderDifference
不能唯一歸因於 DecoderFamily。
```

**判決：Supported closed-corpus gap（evaluation + causal gap）**

### G2：decoder 的跨上游分布泛化證據不足

**前提**

- HiFi-GAN 測試 unseen speaker，提供部分泛化證據；
- 多數完整 TTS 結果由訓練相容的 acoustic model 產生條件；
- 真實部署可能收到不同聲學模型、語言、speaker、錄音域產生的 mel／latent。

**推導**

```text
Renderer 在 matched upstream distribution 表現良好
↛
Renderer 對 unseen upstream model/domain 穩健
```

**判決：Search lead only**

35 篇不是以 universal vocoder 或跨上游泛化為主要選樣，未收錄不能直接建立 field gap。

### G3：單階段改善是否來自聯合訓練而非更強 decoder

VITS 的 ablation 支持多個組件，但沒有形成跨多架構的機制普遍性。

**判決：Supported closed-corpus gap（narrow causal gap）**

需要固定 decoder、latent 與資料，比較 separate training、joint fine-tuning 與 fully joint training。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「neural vocoder 尚未達高自然度」 | 拒絕 | WaveNet、Tacotron 2、HiFi-GAN、VITS 均提供高品質證據 |
| 「沒有快速 waveform generator」 | 拒絕 | HiFi-GAN 等已明確處理速度與部署 |
| 「GAN 一定優於 diffusion」 | Unknown | 比較條件不匹配 |
| 「codec decoder 已取代 mel vocoder」 | 拒絕 | Voicebox 等晚期系統仍採 mel＋HiFi-GAN |
| 「端到端表示完全沒有 decoder」 | 拒絕 | VITS 與 codec 模型仍存在 waveform decoder |

## 7. 最終判決

- **Verified：** waveform rendering 長期決定品質上限和推論成本。
- **Verified：** 高品質 AR、GAN、diffusion 與 codec decoder 路線都已存在。
- **Supported closed-corpus gap：** 缺少在共同 conditioning、資料、sample rate、硬體與模型預算下的多目標比較。
- **Supported closed-corpus gap：** 聯合訓練相對於 decoder 容量提升的獨立因果效果尚未普遍建立。
- **Search lead only：** decoder 對 unseen upstream model／domain 的泛化。
- **No-gap verdict：** 「是否已有高品質或快速 neural waveform generation」沒有缺口。

## 8. 下一個最小驗證步驟

1. 外部搜尋 universal vocoder、cross-model vocoder generalization、matched neural vocoder benchmark。
2. 只保留同 sample rate、同 mel extraction、同資料與同硬體或有正規化成本的比較。
3. 核對是否同時量測 MOS／CMOS、RTF、參數量、記憶體、unseen speaker／language。
4. 若已有完整 matched benchmark，取消 G1；若泛化只測 unseen speaker，G2 可縮小到 unseen upstream model／channel。

**停止條件**

> 若現有文獻已在共同 conditioning 與硬體預算下比較主要 decoder 家族，並涵蓋跨上游模型與分布泛化，則本範圍不得再保留上述缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T1-01、T1-05、T3-05、T4-01、T5-01、T5-02、T5-04、T6-03 至 T6-05、T7-01 至 T7-05

## 10. 專案狀態影響

不修改 `PROJECT.md` 或 `DECISIONS.md`。若 thesis 最終偏向偵測，G2 可轉為「不同 decoder artifact 是否造成 detector shortcut」的跨 S4×S10 驗證問題。
