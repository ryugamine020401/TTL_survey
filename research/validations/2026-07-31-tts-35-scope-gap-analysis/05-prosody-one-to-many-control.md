# S5：一對多映射、韻律與可控性的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：文字未指定的語速、F0、停頓、情緒、風格與隨機變異如何被建模和評估
- 判決限制：不把未收錄的 prosody 專題論文視為不存在

## 1. 問題與範圍框線

### 核心問題

> 同一句文字對應許多合法語音；系統如何在自然多樣性、使用者控制、內容忠實度與重現性之間取得可驗證的平衡？

### 納入

- duration、F0、energy、pause、rhythm；
- prosody、style、emotion、expressiveness；
- global variance、mixture density；
- stochastic duration、VAE／flow／diffusion sampling；
- acoustic prompt 中的韻律與環境；
- diversity、controllability、condition fidelity。

### 排除

- 純 speaker timbre，歸入 S6；
- 純 alignment completeness，歸入 S2；
- 純音質與 decoder artifacts，歸入 S4。

## 2. 形式化目標

文字 `X` 通常不足以唯一決定語音 `Y`：

```text
P(Y | X) 不是單點分布
```

因此完整方法不能只使平均輸出自然，還應處理：

```text
Diversity(Y|X)
∧ ControlAccuracy(Y, c)
∧ ContentFaithfulness(Y, X)
∧ Naturalness(Y)
```

其中 `c` 是目標韻律、情緒、語速或風格條件。

## 3. 證據地圖

| 論文 | 一對多／控制機制 | 直接證據或限制 | 狀態 |
|---|---|---|---|
| T1-01 Klatt | 明確控制 F0、時長、formant 與聲源 | 可解釋，但控制軌跡需專家提供 | Verified |
| T1-03 Korean TTS | 規則指定 stress、pitch、energy、duration | 語言特定且規則成本高 | Verified |
| T2-01–T2-05 | 從資料庫選取單一路徑 | 保留錄音韻律，但受 corpus coverage 與 target cost 限制 | Verified |
| T3-03 GV | 以 global variance 修正 ML 軌跡過度平滑 | 補回全句變異，但不是完整條件分布 | Verified |
| T3-04 Speaker-adaptive HMM | 可做風格／speaker 調適 | 彈性高，但平均化與 vocoder 限制仍在 | Verified |
| T4-02 DMDN | GMM mean／variance／weight 表達多模態 | 特別改善 F0 與自然度 | Verified |
| T5-04 Tacotron 2 | AR attention 隱式生成韻律 | 高平均自然度，仍有異常韻律與 OOD 錯誤 | Verified |
| T5-05 Jia | d-vector 條件化未見 speaker | 口音與 prosody 無法完全和身份解耦 | Verified |
| T6-02 Glow-TTS | flow latent，並可控制 pitch／speed | 提供變異與控制，但可逆架構有限制 | Verified |
| T6-04 DiffWave | 從隨機噪音生成 | 有隨機性，不等於有語義可控韻律 | Verified |
| T6-05 VITS | stochastic duration＋latent sampling | ablation 支持隨機時長改善韻律多樣性 | Verified |
| T7-01 AudioLM | prompt 延續長期結構、speaker 與環境 | prompt 將多種屬性混在一起 | Verified |
| T7-02 VALL-E | sampling 產生多樣輸出並保留情緒／環境 | AR 仍可能內容失敗；控制維度未完全分離 | Verified |
| T7-03 Voicebox | flow matching＋diverse sampling＋style transfer | prompt 屬性不能任意拆分 | Verified |
| T7-04 NaturalSpeech 2 | prompt＋pitch／duration prior＋latent diffusion | 強零樣本表現；資料與多步推論有限制 | Verified |
| T7-05 MaskGCT | masked iterative sampling＋總長度控制 | 提供平行多樣生成，但未建立完整 factor control | Verified |

## 4. 跨時期推導

### 命題 A：確定性平均會降低變異

1. HMM ML trajectory 和 DNN MSE 傾向條件平均。
2. GV 嘗試補回全句變異。
3. DMDN 以 mixture 表達多峰分布。
4. flow、VAE、diffusion、codec LM 與 masked generation 以 latent 或 sampling 明確建模多種輸出。

```text
DeterministicPointEstimate(Y|X)
→ RiskOfConditionalAveraging
```

這不是說所有 deterministic 模型都必然不自然，而是說文字欠定造成的變異不能由單一均值完整表達。

### 命題 B：多樣性不等於可控制

```text
StochasticSampling → MultipleOutputs
MultipleOutputs ↛ UserSpecifiedProsody
```

DiffWave、VITS、VALL-E 等可產生變異，但若使用者無法指定哪個屬性變動，則只能證明 diversity，不能證明 controllability。

### 命題 C：prompt control 是聯合條件，不是因素控制

Jia、AudioLM、VALL-E、Voicebox 等證據顯示，參考音訊同時攜帶 timbre、accent、prosody、emotion、channel。

```text
PromptConditioning
→ JointAttributeTransfer
PromptConditioning
↛ IndependentAttributeControl
```

## 5. 候選缺口推導

### G1：自然度、多樣性、控制精度與內容忠實度未被聯合評估

**前提**

- 各時期分別以 GV、MDN、stochastic duration、flow／diffusion／LM sampling 處理變異；
- 不同論文使用 MOS、F0、speaker similarity、WER 或展示樣本；
- 提高 sampling diversity 可能同時提高內容或韻律失敗率。

**缺少的命題**

```text
在固定文字、speaker、資料與生成預算下，
同時量測：
  naturalness
  + diversity
  + target-control error
  + content error
  + run-to-run failure
```

**判決：Supported closed-corpus gap（evaluation／measurement gap）**

### G2：prompt 屬性的因果可分離性不足

**前提**

- prompt 可成功轉移多種屬性；
- Jia 與 Voicebox 直接指出身份、口音、prosody 或其他屬性無法完全解耦；
- 35 篇沒有系統性 factor intervention。

**推導**

```text
觀察到 prompt 相似
∧ prompt 同時改變多個因素
→ 無法知道輸出變化由哪個 prompt 因素造成
```

**判決：Supported closed-corpus gap（causal／representation gap）**

### G3：韻律適切性而非韻律相似度

現有證據多比較是否像 reference，較少回答「在新文字語義與對話情境下，韻律是否適切」。

**判決：Search lead only**

這 35 篇不是語用／對話 prosody 的完整選樣，不能直接建立領域缺口。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「TTS 沒有建模一對多」 | 拒絕 | DMDN、flow、VITS、diffusion、codec LM 與 masked generation 都已處理 |
| 「沒有韻律控制」 | 拒絕 | 規則控制、pitch／speed control、duration prior 及 prompt control 均已存在 |
| 「sampling 越多樣越好」 | 拒絕 | 多樣性可能犧牲內容忠實、控制與失敗率 |
| 「prompt 等同可分離控制」 | 拒絕 | 語料有直接負面證據 |
| 「MOS 高表示韻律問題已解決」 | 拒絕 | MOS 不單獨識別韻律適切性與條件忠實度 |

## 7. 最終判決

- **Verified：** 一對多問題從 GV／MDN 演進到 latent、stochastic duration、prompt 與 sampling。
- **Inference：** 領域把「平均聲音不自然」轉化為「多樣性與控制如何共存」，問題沒有消失。
- **Supported closed-corpus gap：** 缺少自然度—多樣性—控制—內容忠實度的共同操作化與 matched evaluation。
- **Supported closed-corpus gap：** prompt 中 speaker、accent、prosody、emotion、channel 的因果可分離性不足。
- **Search lead only：** 新文字／新對話情境中的韻律適切性。
- **No-gap verdict：** 「是否已有 stochastic／多樣生成或韻律控制方法」沒有缺口。

## 8. 下一個最小驗證步驟

1. 搜尋 TTS diversity–quality trade-off、prosody controllability benchmark、prompt disentanglement。
2. 只保留同時報告內容錯誤與控制結果的研究。
3. 尋找 swap intervention：固定 timbre 換 prosody、固定 prosody 換 accent／channel。
4. 若已有跨模型標準化多目標 benchmark，取消 G1；若已有充分因果干預，取消 G2。

**停止條件**

> 若外部文獻已在共同資料與模型條件下，聯合量測多樣性、自然度、控制、內容錯誤，並完成 prompt 屬性干預，則本範圍判為沒有殘餘缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T1-01、T1-03、T3-03、T3-04、T4-02、T5-04、T5-05、T6-02、T6-04、T6-05、T7-01 至 T7-05

## 10. 專案狀態影響

不修改專案狀態。G2 與 audio deepfake 的「voice identity 是否能與情緒／通道分離」直接相關，但仍需 detection／security 文獻驗證後才可轉成 thesis question。
