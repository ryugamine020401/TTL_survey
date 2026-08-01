# S2：文字—語音對齊與時長的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：`papers/tts-history/` 中 35 篇 TTS 論文
- 分析單位：文字與語音時間軸如何對應，以及對齊機制對完整性、韻律、速度與控制的影響
- 判決限制：只判斷封閉語料中的證據缺口

## 1. 問題與範圍框線

### 核心問題

> 當文字序列遠短於語音訊號時，系統如何決定每個語言單位的開始、結束與時長；不同解法是否同時取得內容完整性、韻律多樣性、可控性與效率？

### 納入

- 規則時長、HMM／HSMM state duration；
- attention、位置限制、monotonic constraints；
- teacher attention、forced alignment、duration predictor、length regulator；
- MAS、stochastic duration、總長度預測與 masked generation；
- 漏字、重複、跳字、長句穩健性與時長控制。

### 排除

- 與對齊無關的 decoder 音質，歸入 S4；
- 一般 GPU 延遲，除非延遲由逐步對齊或時長生成造成，否則歸入 S8；
- 韻律內容本身歸入 S5，本範圍只處理對齊機制如何限制韻律。

## 2. 邏輯判準

在本範圍中，完整解法至少必須同時證明：

```text
ContentCompleteness
∧ AlignmentStability
∧ ProsodicAdequacy
∧ Controllability
∧ AcceptableLatency
```

只改善其中一項，不等於「對齊問題已解決」。

## 3. 證據地圖

| 論文 | 對齊／時長機制 | 直接結果或限制 | 狀態 |
|---|---|---|---|
| T1-03 Korean TTS | 語言特定 duration rules | 可控制，但需要大量語言規則 | Verified |
| T2-03 Hunt & Black | 由目標單元與 Viterbi 路徑隱含時序 | 保留真人片段，受資料庫覆蓋與接點限制 | Verified |
| T3-01 Yoshimura | HMM 同時建模 spectrum、pitch、duration | 統一時長與聲學模型 | Verified |
| T3-02 Tokuda | HMM 狀態序列＋動態特徵參數生成 | 產生整句平滑軌跡 | Verified |
| T5-02 Tacotron | soft attention 自動學 character–frame alignment | 減少外部 aligner，但 attention 可能失敗 | Verified |
| T5-03 Deep Voice 3 | positional encoding／monotonic constraints | 緩解 repeat／skip，未證明完全消除 | Verified |
| T5-04 Tacotron 2 | location-sensitive attention | 高自然度；仍有誤發音與異常韻律 | Verified |
| T6-01 FastSpeech | teacher attention → duration predictor → length regulator | 困難句穩定且快速，但依賴 teacher／蒸餾 | Verified |
| T6-02 Glow-TTS | flow＋Monotonic Alignment Search | 內生對齊、長句較穩、可控速度 | Verified |
| T6-05 VITS | MAS＋stochastic duration predictor | 單階段生成並補回部分韻律變異 | Verified |
| T7-02 VALL-E | codec LM 隱式產生長度與第一層 AR token | 零樣本能力高，仍有 AR 漏字／重複 | Verified |
| T7-04 NaturalSpeech 2 | 顯式 duration／pitch prior＋latent diffusion | 避免長離散 AR，仍有多步延遲 | Verified |
| T7-05 MaskGCT | 不用 phone-level alignment；預測／指定總長度後 masked generation | 提供另一種路線，但不是零時序假設 | Verified |

## 4. 跨時期命題推導

### 命題 A：每一代都需要某種時序約束

```text
TextLength << WaveformLength
→ TTS 必須引入 AlignmentOrDurationMechanism
```

證據從規則時長、HMM 狀態、attention、duration predictor、MAS 到總長度預測連續存在。

**Inference**

> 「alignment-free」通常只表示沒有 phoneme-level 外部對齊標註，不表示模型不需要任何長度或單調性假設。

因此不能由 MaskGCT 的無 phone-level alignment 推出「時長問題消失」。

### 命題 B：隱式 attention 提高彈性，但失敗會破壞內容完整性

1. Tacotron 將對齊交給 attention 學習。
2. Deep Voice 3 需要加入位置及單調限制。
3. FastSpeech 直接以漏字／重複和速度為前代問題。
4. VALL-E 的 AR token generation 再次回報漏字／重複。

```text
ImplicitSequentialAlignment
→ FlexibleConditioning
∧ RiskOfAccumulatedAlignmentFailure
```

此式是語料支持的趨勢，不是對所有 attention 系統的普遍定律。

### 命題 C：顯式時長改善穩定性，但不自動保留一對多韻律

1. FastSpeech 以 deterministic duration 和 distillation 換取速度與完整性。
2. VITS 特別加入 stochastic duration predictor，以恢復平行模型的韻律多樣性。
3. NaturalSpeech 2 又加入 duration／pitch prior。

因此：

```text
ExplicitDuration → StabilityAndControl
ExplicitDuration ↛ ProsodicDiversity
```

第二式表示顯式時長不足以單獨推出韻律多樣性。

## 5. 候選缺口推導

### G1：對齊穩健性與韻律多樣性的聯合、受控比較不足

**前提**

- T5 論文顯示 attention 失敗；
- T6 論文顯示 duration／MAS 改善速度與穩健性；
- VITS 的 stochastic duration 顯示 deterministic duration 可能不足以建模變異；
- T7 又分成 AR 隱式長度、顯式 prior 與總長度 masked generation。

**缺失的聯合命題**

```text
同一資料、同一 speaker condition、同一 decoder、相近模型容量下：
比較 implicit attention、deterministic duration、stochastic duration、
MAS 與 total-length masked generation，
並同時量測 completeness、prosody diversity、control error 與 latency。
```

35 篇沒有完成此聯合控制。

**判決：Supported closed-corpus gap（evaluation + causal gap）**

### G2：對齊失敗的操作性定義跨論文不一致

**前提**

- 有的論文數 repeat／skip；
- 有的使用 WER；
- 有的用長句或困難句展示；
- 有的只報 MOS 或 attention 圖；
- 晚期 masked／diffusion 系統改變了失敗形式。

**推導**

```text
不同方法聲稱 alignment robustness
∧ robustness 的測量事件與測試集不一致
→ 無法跨方法判定「更穩健」是否為同一命題
```

**判決：Supported closed-corpus gap（measurement gap）**

### G3：完全不依賴細粒度對齊是否優於顯式時長

MaskGCT 提供實例，但只有單一路線且同時更換 tokenizer、資料規模與生成目標。

**判決：Search lead only**

目前只能說存在替代機制，不能由一篇完整系統比較推導其一般優勢。

## 6. 反證與被拒絕說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「沒有非 attention TTS」 | 拒絕 | FastSpeech、Glow-TTS、VITS、NaturalSpeech 2、MaskGCT 均提供替代方案 |
| 「顯式時長已完全解決對齊」 | 拒絕 | 它把問題轉為 duration accuracy、變異與外部／內生對齊來源 |
| 「MaskGCT 完全沒有時長模型」 | 拒絕 | 它仍預測或指定總長度 |
| 「AR 一定比 NAR 更有韻律」 | Unknown | 本語料有機制線索，但沒有控制所有混淆因子的普遍比較 |
| 「對齊研究沒有缺口」 | 不成立 | 解法存在，但聯合評估與測量一致性仍不足 |

## 7. 最終判決

- **Verified：** 對齊與時長沒有消失，只是不斷改變承擔模組。
- **Verified：** attention、顯式 duration、MAS、stochastic duration、顯式 prior 及總長度 masked generation 均已存在。
- **Supported closed-corpus gap：** 缺少對這些機制在相同條件下的穩健性—韻律—控制—延遲聯合比較。
- **Supported closed-corpus gap：** alignment failure／robustness 缺少跨方法一致的操作性定義。
- **No-gap verdict：** 「是否有 attention 之外的解法」在本語料內沒有缺口。

## 8. 下一個最小驗證步驟

1. 外部搜尋 classification：`TTS alignment robustness benchmark duration predictor attention MAS masked generation`。
2. 先找是否已有固定 backbone／decoder 的 alignment ablation。
3. 對每篇候選工作核對是否同時報告：
   - word/phone completeness；
   - duration error；
   - prosody diversity；
   - controllability；
   - latency。
4. 若已有完整 matched benchmark，取消 G1；若只比較 WER 或 MOS，保留較窄的聯合評估缺口。

**停止條件**

> 若當前文獻已在固定資料與生成器條件下，比較主要對齊家族並使用一致的完整性、韻律、控制和成本指標，則本範圍不得再主張殘餘缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T3-01、T3-02、T5-02 至 T5-04、T6-01、T6-02、T6-05、T7-02、T7-04、T7-05

## 10. 專案狀態影響

本分析不改變已核可方向。G1 與 G2 可加入後續外部搜尋，但在完成搜尋前不能寫成領域級研究缺口。
