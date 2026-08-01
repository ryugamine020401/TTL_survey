# S9：評估、量測效度與因果歸因的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：論文用何種指標支持何種主張，以及指標、比較與 ablation 是否足以推出結論
- 判決限制：這是對 35 篇證據結構的分析，不是完整 speech evaluation survey

## 1. 問題與範圍框線

### 核心問題

> TTS 論文使用的 MOS、WER、speaker similarity、prosody、FSD、速度與 ablation，是否真的量到它們聲稱改善的能力，並足以歸因到指定方法？

### 納入

- intelligibility、naturalness、MOS／CMOS；
- spectral distance、F0、duration、WER；
- speaker similarity、人類偏好；
- prosody、FSD、偵測、速度；
- baseline matching、ablation、統計檢定；
- 跨論文可比較性、human-level claim。

### 排除

- 單純提出新 metric 但不討論其構念；
- 具體資料 coverage 問題歸入 S7；
- detection 的威脅模型歸入 S10。

## 2. 推論有效性的最低條件

論文由觀察結果 `R` 推出方法主張 `M causes improvement`，至少需要：

```text
ValidConstructMeasure
∧ MatchedBaseline
∧ ControlledConfounders
∧ AdequateSampleAndStatistics
∧ ScopeMatchedConclusion
```

缺一項時，結論需縮限，而不是自動判為錯誤。

## 3. 證據地圖

| 論文／時期 | 主要評估形式 | 可支持與不可支持的命題 | 狀態 |
|---|---|---|---|
| T1 系列 | 可懂度、個別聲學或規則展示 | 支持可產生可懂語音；不足以比較現代自然度 | Verified |
| T2 系列 | unit cost、接點與聽測 | 支持局部自然與搜尋改進；受 corpus／系統差異影響 | Verified |
| T3-01 | 架構與客觀結果，正式主觀評估不足 | 支持可統一建模；自然度結論較弱 | Verified |
| T3-03 GV | 針對 over-smoothing 的參數與聽測 | 提供機制導向證據 | Verified |
| T3-05 Review | 統整 SPSS 與 unit selection 優缺點 | 支持穩定性—最佳樣本自然度的取捨 | Verified |
| T4-01 Zen DNN | 相同模型大小、主觀比較 | 支持 DNN mapping 的局部改進 | Verified |
| T4-02 DMDN | 多模態輸出、F0 與自然度 | 支持 MSE／單峰限制的修正 | Verified |
| T4-03 vs. T4-05 | dynamic features／MLPG 結論不一致 | 顯示 recipe、資料與架構會改變結論 | Verified |
| T5-04 Tacotron 2 | MOS＋WaveNet／Griffin–Lim ablation | 支持 decoder 對品質的貢獻；不能外推所有資料域 | Verified |
| T5-05 Jia | naturalness＋speaker similarity／verifier | 支持 zero-shot；同時顯示 unseen identity gap | Verified |
| T6-01 FastSpeech | MOS、speed、repeat／skip 困難句 | 支持效率／完整性改善；teacher 與蒸餾是混淆因素 | Verified |
| T6-03 HiFi-GAN | MOS、速度、ablation、unseen speaker | 證據相對完整，但仍限指定 conditioning 與資料 | Verified |
| T6-05 VITS | MOS＋component ablation | 支持 prior flow／posterior／stochastic duration 的局部作用 | Verified |
| T7 系列 | WER、speaker similarity、MOS／CMOS、prosody、FSD、speed、detectability | 多維評估增加，但資料、prompt、baseline 不一致 | Verified |

## 4. 邏輯推導

### 命題 A：自然度不是單一可完全觀察構念

```text
Naturalness ≠ Intelligibility
Naturalness ≠ SpeakerSimilarity
Naturalness ≠ ProsodyAppropriateness
Naturalness ≠ ContentReliability
```

MOS 可能同時受上述因素影響，因此高 MOS 不能單獨證明每一項皆已解決。

### 命題 B：跨論文 MOS 不具天然可比性

35 篇的聽者、語料、音量正規化、sample rate、reference、baseline、問句與統計方法不同。

```text
MOS_A > MOS_B
且 Protocol_A ≠ Protocol_B
↛
System_A > System_B
```

### 命題 C：完整系統改進不等於單一機制因果效果

晚期工作經常同時改變：

```text
Data + Representation + Architecture + Objective
+ Decoder + Compute + Evaluation
```

若沒有 matched ablation，整體結果只能支持「整套系統在該條件表現較好」，不能支持每個元件都是原因。

### 命題 D：human-level 是帶量詞範圍的命題

正確形式：

```text
在資料集 D、任務 T、指標 M、prompt P 與 protocol E 下，
模型與 reference 的差異未達顯著或達指定門檻。
```

它不能推出任意語言、口音、長度、文本、speaker 或 channel 都達到真人。

## 5. 候選缺口推導

### G1：多構念聯合評估與失敗分解不足

**前提**

- T7 開始同時使用 WER、speaker similarity、prosody、FSD 等；
- 仍沒有跨 35 篇一致的內容、身份、韻律、音質、穩定性、效率共同 protocol；
- 平均分數可能掩蓋 generator／speaker／language／condition 子群失敗。

**判決：Supported closed-corpus gap（measurement／evaluation gap）**

### G2：大型完整系統的因果歸因不足

**前提**

- Tacotron 2、HiFi-GAN、VITS 提供有價值的 ablation；
- T7 系統規模更大、元件更多、資料與表示同時改變；
- 35 篇沒有形成跨系統共同的 factorized ablation standard。

**判決：Supported closed-corpus gap（causal attribution gap）**

### G3：平均品質之外的風險、尾端失敗與不確定性

35 篇主要報平均 MOS／WER／similarity，較少建立：

- per-condition worst case；
- failure probability；
- calibrated uncertainty；
- abstention／selective generation；
- fixed operating constraint。

**判決：Search lead only**

這與目前 thesis 的 uncertainty／selective prediction 方向相關，但此生成史語料不足以建立領域缺口。

## 6. 矛盾與負面證據

| 張力 | 證據 | 推論 |
|---|---|---|
| unit selection 最佳樣本自然 vs. SPSS 一致性 | T3-05 | 平均自然度與品質方差不是同一目標 |
| BLSTM 是否可移除 dynamic features／MLPG | T4-03、T4-05 | 結果受 recipe 與資料影響，不能形成普遍定律 |
| discrete token vs. continuous latent | T7-02、T7-04、T7-05 | 完整系統比較不足以歸因表示優劣 |
| AR 表現力 vs. NAR 穩健性 | T5、T6、T7 | 需要聯合而非單指標評估 |
| 接近真人 MOS vs. OOD／口音限制 | T5-04、T7 | benchmark 飽和不等於開放域問題解決 |

## 7. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「TTS 沒有主觀評估」 | 拒絕 | MOS／CMOS 與偏好測試廣泛存在 |
| 「TTS 沒有客觀指標」 | 拒絕 | WER、speaker similarity、F0、FSD、速度等均已使用 |
| 「只要 MOS 高就代表完全成功」 | 拒絕 | 構念與範圍都過度延伸 |
| 「任何 ablation 都能證明因果」 | 拒絕 | 需控制資料、訓練與交互作用 |
| 「不同論文的 MOS 可直接排名」 | 拒絕 | protocol 不匹配 |

## 8. 最終判決

- **Verified：** 評估已從可懂度／MOS 擴展到內容、身份、韻律、分布與效率多維指標。
- **Inference：** 指標增加不等於構念已被完整定義；晚期系統反而使歸因更困難。
- **Supported closed-corpus gap：** 缺少共同的多構念、子群與尾端失敗評估。
- **Supported closed-corpus gap：** 大型完整系統的 representation／data／architecture／decoder 因果歸因不足。
- **Search lead only：** calibrated uncertainty、selective generation 與 risk–coverage 評估。
- **No-gap verdict：** 「是否存在主觀或客觀 TTS 評估」沒有缺口。

## 9. 下一個最小驗證步驟

1. 搜尋 standardized TTS evaluation、multi-dimensional speech generation benchmark、MOS validity、failure-tail evaluation。
2. 查驗是否有 protocol 將內容、speaker、prosody、naturalness、robustness、latency 分開。
3. 查驗是否報告 macro／worst-group，而非只報 pooled average。
4. 對因果候選只接受 matched ablation 或 factorial design。

**停止條件**

> 若當前已有公開、跨模型、跨語言、跨條件的多構念 protocol，並包含尾端風險與系統性 factor attribution，則取消 G1/G2；若只是更多平均指標，不足以取消。

## 10. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：35 篇均涉及；關鍵反例為 T3-05、T4-03、T4-05、T5-04、T5-05、T6-01、T6-03、T6-05、T7-01 至 T7-05

## 11. 專案狀態影響

不改變 `PROJECT.md` 或 `DECISIONS.md`。G3 可成為後續 detection／uncertainty 文獻搜尋入口，但不能由本封閉語料直接認定為 thesis gap。
