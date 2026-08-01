# S8：系統整合、效率與可靠性的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：模組化／端到端、AR／NAR、兩階段／單階段對延遲、穩定、可診斷與部署成本的影響
- 判決限制：論文中的硬體與實作不同，不做速度數字的直接排名

## 1. 問題與範圍框線

### 核心問題

> TTS 系統如何在音質、速度、內容完整性、訓練穩定性、模組可替換性與部署成本間取捨；端到端或非自回歸是否真正提高整體可靠性？

### 納入

- modular、two-stage、single-stage、joint training；
- autoregressive、non-autoregressive、iterative parallel；
- latency、RTF、throughput、streaming、model footprint；
- exposure bias、repeat／skip、long-form failure；
- external aligner／teacher dependency；
- 可重現工具鏈、模組替換與錯誤定位。

### 排除

- 純自然度構念，歸入 S9；
- 純 decoder 比較，歸入 S4；
- 資料 coverage，歸入 S7。

## 2. 多目標定義

部署可用性至少是：

```text
Utility =
Quality
× ContentReliability
× Throughput
× ResourceFeasibility
× Reproducibility
```

這不是數值公式，而是邏輯上的合取：任一必要條件失敗，都可能使完整系統不可用。

## 3. 證據地圖

| 論文 | 系統整合／效率命題 | 直接結果或限制 | 狀態 |
|---|---|---|---|
| T2-03 Hunt & Black | Viterbi 搜尋完整 unit path | 可形式化搜尋，成本受資料庫與候選規模影響 | Verified |
| T3-05 SPSS Review | 小 footprint、穩定、可調適 | 音質受 over-smoothing／vocoder 限制 | Verified |
| T4-03 BLSTM | 使用前後全文 context | 品質改善，但整句非串流且成本較高 | Verified |
| T4-04 Low-Latency LSTM | 單向 LSTM＋recurrent output | 避免 utterance-level MLPG，支援低延遲 | Verified |
| T4-05 Merlin | 模組化開源 DNN/RNN SPSS toolkit | 促進可重現；也揭示 recipe 會改變結論 | Verified |
| T5-01 WaveNet | sample-level AR | 品質高但推論慢 | Verified |
| T5-02／T5-04 | attention AR spectrogram generation | 減少人工 pipeline；有 alignment failure 與逐幀成本 | Verified |
| T5-03 Deep Voice 3 | fully convolutional attention | 改善訓練速度與擴展性，仍需 attention constraints | Verified |
| T6-01 FastSpeech | feed-forward NAR＋distillation | 大幅加速並降低 repeat／skip；依賴 teacher | Verified |
| T6-02 Glow-TTS | flow＋MAS | 移除外部 aligner，平行且長句較穩 | Verified |
| T6-03 HiFi-GAN | parallel GAN vocoder | 快速、小 footprint、CPU/GPU 可部署 | Verified |
| T6-04 DiffWave | iterative parallel diffusion | 比 WaveNet 快，但多步生成仍有成本 | Verified |
| T6-05 VITS | single-stage joint training | 減少 acoustic model／vocoder mismatch | Verified |
| T7-02 VALL-E | 第一層 AR、其餘 NAR | 規模化 token generation，但 AR 完整性與成本仍存在 | Verified |
| T7-03 Voicebox | NAR flow matching | 報告相對快速並統一多任務 | Verified |
| T7-04 NaturalSpeech 2 | latent diffusion | 避免長 token AR，但多步 solver 有延遲 | Verified |
| T7-05 MaskGCT | iterative masked NAR | 無逐 token AR，仍需多輪 T2S／S2A 解碼 | Verified |

## 4. 命題推導

### 命題 A：非自回歸不等於常數時間

```text
NARAcrossSequence
↛
SinglePassGeneration
```

FastSpeech 可單次平行產生 mel；flow 需 invertible transformation；diffusion、flow matching、masked generation 可能需要多個 solver／refinement steps。

### 命題 B：端到端不等於沒有模組

```text
Tacotron → spectrogram predictor + waveform reconstruction
Tacotron 2 → text-to-mel + WaveNet
VITS → prior/posterior/flow/duration/GAN components jointly trained
VALL-E/MaskGCT → tokenizer + token models + codec decoder
```

**Inference**

> 歷史方向是減少人工介面與跨模組 mismatch，而不是邏輯上消除所有模組。

### 命題 C：速度改善可能把依賴移到訓練或外部元件

FastSpeech inference 快，但 duration 來自 AR teacher 與 distillation；Glow-TTS 以 MAS 內生處理；晚期模型依賴 codec、ASR pseudo-label 或大規模預訓練。

```text
FastInference
↛
LowTotalSystemCost
```

完整成本還包括 teacher、pretraining、memory、tokenizer 與資料準備。

## 5. 候選缺口推導

### G1：品質—完整性—延遲—資源的共同 Pareto 評估不足

**前提**

- 各論文以不同硬體、sample rate、資料、模型大小及速度定義報告結果；
- MOS、RTF、mel-generation speed、end-to-end speed 不可直接互換；
- 某些 NAR 方法仍是 iterative generation。

**推導**

```text
只報 Quality 或單一 Speedup
不足以判定 DeploymentUtility
```

**判決：Supported closed-corpus gap（deployment／evaluation gap）**

### G2：模組化與 joint training 對錯誤定位、維護及跨模組替換的影響不足

**前提**

- Merlin 顯示模組化有可重現與替換價值；
- VITS 顯示 joint training 可降低 mismatch；
- T7 又回到多個預訓練模組；
- 35 篇主要測輸出品質與速度，沒有共同測試 fault localization、component swap、update cost。

**判決：Supported closed-corpus gap（systems／replication gap）**

### G3：真實串流、長內容與服務負載可靠性

T4-04 處理低延遲，T5/T6 處理 AR／NAR 速度，但 35 篇不是完整 production-systems corpus。

**判決：Search lead only**

不能因缺少 tail latency、concurrency、長時間 drift 就宣稱領域空白。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「沒有快速 TTS」 | 拒絕 | FastSpeech、Glow-TTS、HiFi-GAN、Voicebox 等直接處理效率 |
| 「NAR 一定只需一步」 | 拒絕 | diffusion、flow matching、masked generation 可多步迭代 |
| 「端到端沒有模組」 | 拒絕 | VITS 與 T7 均含明確子模組 |
| 「單階段一定更容易維護」 | Unknown | 35 篇沒有維護／替換實驗 |
| 「速度最高的論文就是最佳部署方案」 | 拒絕 | 硬體、品質、記憶體、完整性與總訓練成本未對齊 |

## 7. 最終判決

- **Verified：** AR 的逐步成本與 alignment failure 推動 NAR、flow、GAN、diffusion 及 masked generation。
- **Inference：** 效率問題被重新分配到 teacher、alignment、solver steps、tokenizer 與預訓練，而非完全消失。
- **Supported closed-corpus gap：** 缺少品質、完整性、延遲、記憶體、模型大小與總系統成本的共同 Pareto benchmark。
- **Supported closed-corpus gap：** modular vs. joint training 的可診斷、可替換與維護成本未被系統評估。
- **Search lead only：** production streaming、tail latency、併發與長期服務可靠性。
- **No-gap verdict：** 「是否存在快速／非自回歸／單階段 TTS」沒有缺口。

## 8. 下一個最小驗證步驟

1. 搜尋 standardized TTS efficiency benchmark、end-to-end latency、component swap、streaming reliability。
2. 將 preprocessing、speaker encoder、acoustic model、decoder、迭代步數納入端到端成本。
3. 尋找固定硬體與品質 constraint 下的 Pareto frontier，而非單一 speedup。
4. 若已有公開、可重現的共同 benchmark 且涵蓋系統維護性，取消 G1/G2。

**停止條件**

> 若當前工作已在共同硬體、品質與可靠性條件下量測主要架構，並實驗比較 component swap、fault isolation 和更新成本，則本範圍不得保留上述缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T3-05、T4-03 至 T4-05、T5-01 至 T5-04、T6-01 至 T6-05、T7-02 至 T7-05

## 10. 專案狀態影響

不改變專案方向。若後續 thesis 聚焦通訊場景，G1 可擴充真實 channel 的 end-to-end latency 與可靠性，但需要額外 systems 文獻。
