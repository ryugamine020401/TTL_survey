# S6：說話者身份、適應與零樣本複製的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：說話者身份如何進入系統、需要多少資料，以及身份條件與其他聲學屬性的關係
- 判決限制：本文件不直接判定冒用防禦；安全外部性歸入 S10

## 1. 問題與範圍框線

### 核心問題

> TTS 如何從固定聲音、少量調適演進到數秒 prompt 的零樣本聲音生成；現有證據是否能把 timbre identity 與口音、韻律、情緒和 channel 分開？

### 納入

- speaker-dependent parameters／database；
- average voice、speaker adaptation；
- speaker embedding、d-vector、speaker encoder；
- acoustic prompt、in-context voice conditioning；
- seen／unseen speaker similarity；
- prompt 長度、資料需求與身份泛化。

### 排除

- 不涉及身份的韻律控制，歸入 S5；
- 資料量的一般 scaling，歸入 S7；
- consent、impersonation、provenance 與 spoofing，歸入 S10。

## 2. 操作性定義

本文將「身份條件成功」拆為：

```text
TimbreSimilarity
∧ IdentityConsistencyAcrossTexts
∧ GeneralizationToUnseenSpeaker
∧ RobustnessAcrossAccentProsodyChannel
∧ ContentFaithfulness
```

單一 speaker-verification score 不足以證明五項都成立。

## 3. 證據地圖

| 時期／論文 | 身份進入方式 | 直接結果或限制 | 狀態 |
|---|---|---|---|
| T1-01 Klatt | 重寫聲源、formant 與控制參數 | 可人工模擬聲音，但需專家調整 | Verified |
| T2-01–T2-05 | 每位 speaker 建立專屬錄音資料庫 | 身份細節真實，但換 speaker 等於重建 corpus | Verified |
| T3-04 Yamagishi | average voice＋CSMAPLR／MAP 等 adaptation | 約數分鐘／百句可調適，且能使用不完美資料 | Verified |
| T3-05 SPSS Review | speaker adaptation／interpolation | 彈性與小 footprint 是 SPSS 優勢 | Verified |
| T5-03 Deep Voice 3 | multispeaker conditioning | 可擴展到大量 speaker，但 noisy data 降低品質 | Verified |
| T5-05 Jia | speaker-verification encoder 的 d-vector | 數秒未轉錄語音 zero-shot；unseen speaker similarity 下降 | Verified |
| T5-05 Jia | speaker encoder 使用大量且多樣 speaker 資料 | encoder data diversity 對泛化關鍵 | Verified |
| T5-05 Jia | 身份、口音與 prosody | 無法完全解耦；合成聲仍可被 verifier 區分 | Verified |
| T6-02 Glow-TTS | multispeaker condition＋flow | 可控制 speaker、pitch 與 speed | Verified |
| T6-03 HiFi-GAN | waveform model 對 unseen speaker | 提供 decoder 層的未見 speaker 泛化證據 | Verified |
| T6-05 VITS | multispeaker latent／decoder | VCTK 上接近 ground truth MOS，但非任意 speaker prompt | Verified |
| T7-01 AudioLM | 3 秒 acoustic prompt | 延續未見 speaker 與聲學環境 | Verified |
| T7-02 VALL-E | 3 秒 enrolled recording | zero-shot identity、環境與情緒保留；口音覆蓋有限 | Verified |
| T7-03 Voicebox | reference speech infilling／prompt | zero-shot 多語與 style transfer；屬性不能任意拆分 | Verified |
| T7-04 NaturalSpeech 2 | speech prompt＋continuous latent | zero-shot speech／singing；資料域仍有限 | Verified |
| T7-05 MaskGCT | prompt＋semantic／acoustic tokens | 英中大型資料下接近真人的相似度與可懂度 | Verified |

## 4. 歷史命題鏈

### 命題 A：取得一個新聲音的成本顯著下降

```text
專家重設參數／重錄 corpus
→ 數分鐘 speaker adaptation
→ 數秒 reference embedding
→ 數秒 acoustic prompt、零參數更新
```

**Verified**

35 篇共同支持此方向性變化，但沒有在相同任務上量化完整成本曲線。

### 命題 B：低資料成本不蘊含身份表示純化

1. Jia 顯示數秒 reference 可產生未見 speaker。
2. 同篇指出 accent、prosody 與 identity 不完全解耦。
3. VALL-E、AudioLM 顯示 prompt 也攜帶環境與情緒。
4. Voicebox 明示 prompt 屬性不能任意拆分。

```text
ShortPromptSuccess
↛
PureSpeakerIdentityRepresentation
```

### 命題 C：seen-speaker 表現不能外推 unseen／cross-domain speaker

```text
HighSimilarity(seen speaker, matched domain)
↛
HighSimilarity(unseen speaker, new accent/style/channel)
```

Jia 的 unseen similarity 下降與晚期論文的資料覆蓋限制直接支持此警告。

## 5. 候選缺口推導

### G1：身份、口音、韻律、情緒與 channel 缺少因果分離評估

**前提**

- 多篇工作成功複製整體聲音；
- 至少 Jia 與 Voicebox 直接報告屬性糾纏；
- VALL-E／AudioLM 顯示 prompt 會保留環境與情緒，這既是能力也是混淆；
- 35 篇沒有完整的 swap／counterfactual evaluation。

**推導**

```text
Prompt A 與 B 同時在 timbre、accent、prosody、channel 不同
輸出也不同
→ 無法將輸出身份差異歸因於單一因素
```

**判決：Supported closed-corpus gap（causal／measurement gap）**

### G2：prompt 長度、品質與跨域身份泛化的聯合曲線不足

**前提**

- 3 秒 prompt 成為代表性設定；
- Jia 顯示資料多樣性與 unseen speaker 差異重要；
- 晚期模型的資料域、speaker encoder、codec 與規模同時改變。

**缺失命題**

```text
IdentityPerformance =
f(prompt duration, prompt SNR/channel, accent match,
  text match, speaker rarity, training exposure)
```

35 篇沒有把這些因素做完整 factorial 或 response-surface 分析。

**判決：Supported closed-corpus gap（evaluation／coverage gap）**

### G3：speaker similarity 指標是否等同人類身份判斷

語料使用 verifier score 與主觀相似度，但不同系統、模型與條件不一致。

**判決：Search lead only**

此題需要 speaker verification、perception 與 deepfake 文獻，不可只靠 35 篇 TTS 論文判定。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「沒有少量資料 speaker adaptation」 | 拒絕 | Yamagishi 已建立數分鐘調適 |
| 「沒有 zero-shot voice cloning」 | 拒絕 | Jia、VALL-E、Voicebox、NaturalSpeech 2、MaskGCT 均有相關證據 |
| 「3 秒是一般性的最小充分長度」 | Unknown | 代表性設定不是普遍下界 |
| 「高 speaker-verifier score 等於人類無法分辨」 | 不成立 | 指標與人類判斷不是同一命題 |
| 「prompt 只攜帶 timbre」 | 拒絕 | 多篇證據顯示也攜帶 accent、prosody、emotion、environment |

## 7. 最終判決

- **Verified：** 新 speaker 所需資料與調適成本從專屬 corpus 降到數秒 prompt。
- **No-gap verdict：** zero-shot cloning 與少量 speaker adaptation 已存在，因此不能把「實現零樣本聲音」當研究缺口。
- **Supported closed-corpus gap：** 身份與 accent／prosody／emotion／channel 的因果可分離性不足。
- **Supported closed-corpus gap：** prompt 長度、品質、speaker rarity 與跨域條件的聯合泛化曲線不足。
- **Search lead only：** verifier 指標與人類身份判斷的一致性。

## 8. 下一個最小驗證步驟

1. 搜尋 zero-shot TTS speaker disentanglement、prompt duration ablation、cross-domain speaker similarity。
2. 優先找同一 speaker 在多種 accent／emotion／channel 條件下的 paired data。
3. 查驗是否做過 identity-preserving attribute swap，而非只報整體 similarity。
4. 若已有跨模型、跨語言、跨通道的 factorial evaluation，取消 G1/G2。

**停止條件**

> 若現有文獻已分別操弄 timbre、accent、prosody、emotion、channel 與 prompt duration，並以人類及 calibrated verifier 共同評估 unseen speaker，則本範圍不得主張上述缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T3-04、T3-05、T5-03、T5-05、T6-02、T6-03、T6-05、T7-01 至 T7-05

## 10. 專案狀態影響

不修改 `PROJECT.md` 或 `DECISIONS.md`。G1、G2 可作為 audio deepfake threat-model 的生成能力節點，但不是尚未驗證的 thesis gap。
