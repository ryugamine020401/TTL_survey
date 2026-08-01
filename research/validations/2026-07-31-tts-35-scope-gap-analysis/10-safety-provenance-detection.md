# S10：濫用、安全、來源追溯與偵測的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：生成論文如何定義冒用風險、提出何種緩解方法，以及證據涵蓋何種威脅模型
- 判決限制：這 35 篇以 TTS 生成史為選樣，不是 audio deepfake detection、watermarking 或 provenance 的系統性回顧

## 1. 問題與範圍框線

### 核心問題

> 當 TTS 能以數秒 prompt 生成高相似度未見聲音時，35 篇中的安全證據是否足以支持「生成語音可被可靠辨識、取得有效同意並追溯來源」？

### 納入

- impersonation、spoofing、fraud、voice consent；
- synthetic-speech detection；
- same-generator／cross-generator detection；
- compression、resynthesis、channel、re-recording、laundering；
- watermark／fingerprint／provenance；
- reporting、release policy 與部署 safeguards；
- 專用偵測器與生成器共同評估。

### 排除

- 純生成自然度；
- speaker identity 技術本身歸入 S6；
- 一般資料偏差歸入 S7，除非直接影響安全保證。

## 2. 威脅模型

本範圍至少區分：

```text
A0：非惡意、原始模型輸出
A1：同模型輸出，經一般 codec／壓縮
A2：跨生成器、未見模型
A3：重錄、通訊通道、去噪或重新編碼
A4：刻意 laundering／artifact removal
A5：adaptive attacker 知道 detector／watermark
```

只在 A0 成功，不能推出 A1–A5 的安全性。

## 3. 證據地圖

| 論文 | 安全命題／緩解 | 直接證據與範圍 | 狀態 |
|---|---|---|---|
| T5-05 Jia | 明示可能無同意冒用聲音 | 驗證其合成聲容易與真聲區分；限該模型與當時品質 | Verified |
| T7-01 AudioLM | 承認 spoofing／impersonation 風險 | 訓練同模型專用 classifier；為避免 codec artifact shortcut，真聲也經 SoundStream | Verified |
| T7-01 AudioLM | 人類真偽辨識接近隨機，classifier 準確度高 | 證明人耳與同模型 detector 可分離；未證明跨模型／通道 | Verified |
| T7-02 VALL-E | 承認 spoofing／impersonation | 提到可以建立 detector；論文未提供通用偵測驗證 | Verified |
| T7-03 Voicebox | 承認 arbitrary-user style generation 的濫用 | 建立 binary classifier，比較 original／resynthesized 與 Voicebox-generated | Verified |
| T7-03 Voicebox | 計畫研究 artificial fingerprinting | 屬 future work，不是已驗證 provenance | Verified |
| T7-04 NaturalSpeech 2 | 實驗假設目標 speaker 同意 | 建議部署時加入 approval protocol 與 detector；未實作完整治理機制 | Verified |
| T7-05 MaskGCT | 承認 spoofing／impersonation | 假設使用者同意；主張需要 robust detector 與 misuse reporting system | Verified |
| T1–T4、T5-01–T5-04、T6 | 多數以生成方法與品質為主 | 未形成可比較的 security evaluation | Verified as corpus coverage |

## 4. 邏輯推導

### 命題 A：生成逼真與可偵測可以同時成立

AudioLM 顯示：

```text
HumanDiscrimination ≈ Chance
∧ SameGeneratorClassifierAccuracy is High
```

因此「人耳難辨」不蘊含「機器不可偵測」。

同樣地：

```text
SameGeneratorDetectable
↛
CrossGeneratorOrPostProcessedDetectable
```

### 命題 B：acknowledging risk 不等於 mitigating risk

Jia、VALL-E、NaturalSpeech 2、MaskGCT 都承認 impersonation／spoofing；但其行動從實驗 detector、建議 detector、假設 consent 到 future protocol 不等。

```text
RiskAcknowledged
↛
RiskMitigated
```

只有具體機制、威脅模型、測試與失敗條件才能支持 mitigation claim。

### 命題 C：同模型 detector 是封閉世界命題

AudioLM 與 Voicebox 的 detector 證據可形式化為：

```text
Train(generator = G)
∧ Test(generator = G, selected processing)
→ DetectableWithinTestedConditions(G)
```

不能改寫為：

```text
∀ generator, channel, laundering：Detectable
```

後者是未被證明的全稱命題。

### 命題 D：同意假設不是可執行的同意機制

NaturalSpeech 2 與 MaskGCT 假設使用者同意。這對研究倫理範圍有說明作用，但沒有證明部署系統能：

- 驗證 prompt speaker 身份；
- 驗證授權範圍與期限；
- 防止第三方上傳他人音訊；
- 撤銷或追蹤已生成內容。

## 5. 候選缺口推導

### G1：生成器內 detector 缺少跨生成器與真實轉換鏈評估

**前提**

- AudioLM、Voicebox 提供 same-generator detector 證據；
- VALL-E 等明示需要 detector；
- 35 篇沒有共同測試 unseen generator、通信 codec、重錄、去噪、laundering 與 adaptive attack。

**推導**

```text
有 A0 證據
∧ 缺少 A1–A5 的共同證據
∧ 實際濫用可進行後處理與模型替換
→ 35 篇未建立部署範圍的 detector robustness
```

**判決：Supported closed-corpus gap（threat-model／evaluation gap）**

此判決不表示 detection 領域沒有相關研究；只表示生成語料本身沒有建立此保證。

### G2：被動偵測、主動標記與 provenance 未形成共同保證模型

**前提**

- Voicebox 把 fingerprinting 留作 future work；
- 其餘晚期論文主要建議 detector、consent 或 reporting；
- 沒有一篇在此語料中聯合定義 authenticity、source attribution、tamper survival 與 absence-of-mark 的意義。

**判決：Supported closed-corpus gap（provenance／deployment gap）**

仍需外部 watermark／C2PA／provenance 文獻驗證是否為 field gap。

### G3：speaker consent 的技術可執行性

**前提**

- 多篇只假設 consent；
- 沒有實作身份核驗、授權範圍、撤銷與稽核流程。

**判決：Search lead only**

此問題跨 usable security、privacy、policy 與 systems；生成論文未收錄不足以宣稱領域空白。

### G4：偵測器失效時的決策與不確定性

35 篇的 detector 多為二元分類結果，沒有處理 unknown generator、校準、棄權、risk–coverage 或錯誤代價。

**判決：Search lead only**

這可能連到 thesis 的 selective prediction，但必須另查現行 deepfake detection 文獻。

## 6. 支持與反面證據

| 命題 | 支持證據 | 限制／反面證據 |
|---|---|---|
| 高逼真輸出仍可被機器偵測 | AudioLM、Voicebox | 主要為 same-generator、特定 processing |
| 生成論文注意到濫用 | Jia、AudioLM、VALL-E、Voicebox、NS2、MaskGCT | 承認風險不等於已部署緩解 |
| codec artifact 可造成 shortcut | AudioLM 將真聲也經 SoundStream | 只控制一類 artifact，不涵蓋所有 generator/channel |
| 主動 fingerprint 可能有用 | Voicebox future work | 在本語料中未實作、未測 survival |
| consent 是必要條件 | NS2、MaskGCT | 只是假設，沒有 enforceable protocol |

## 7. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「35 篇完全沒有合成偵測」 | 拒絕 | AudioLM、Voicebox 有 detector 實驗，Jia 也測可區分性 |
| 「高自然度代表不可偵測」 | 拒絕 | AudioLM 提供直接反例 |
| 「same-generator detector 證明部署安全」 | 拒絕 | 量詞與威脅模型過度延伸 |
| 「沒有任何研究提到 consent」 | 拒絕 | NaturalSpeech 2、MaskGCT 明示同意假設 |
| 「這 35 篇證明整個領域沒有 watermark」 | 拒絕 | 生成史選樣不能代表 watermark／provenance 領域 |
| 「通用 detector 已被證明」 | No evidence | 沒有跨生成器、通道與 adaptive attack 的共同保證 |

## 8. 最終判決

- **Verified：** T5 後期至 T7 的論文逐步承認 impersonation／spoofing，部分工作提供 same-generator detector。
- **Verified：** 高人類逼真度與機器可偵測性可以同時成立。
- **Supported closed-corpus gap：** 生成器內偵測證據沒有建立跨生成器、通訊處理、laundering 與 adaptive attacker 的部署保證。
- **Supported closed-corpus gap：** 被動 detector、主動 fingerprint／watermark 與 provenance 缺少共同保證與生存性評估。
- **Search lead only：** enforceable consent、misuse reporting、detector uncertainty／abstention。
- **No-gap verdict：** 「是否有人提出合成偵測」及「是否有人注意濫用」在 35 篇內沒有缺口。

## 9. 下一個最小驗證步驟

1. 停止只使用 TTS 生成論文，改查 audio deepfake detection、ASVspoof、watermarking、provenance 的原始研究。
2. 建立查詢矩陣：

   ```text
   unseen generator
   × codec/transcode
   × re-recording/telephony
   × denoising/enhancement
   × adversarial laundering
   × calibration/abstention
   ```

3. 分開驗證：
   - detector 能否泛化；
   - watermark／fingerprint 能否存活；
   - provenance 缺失能否被正確解讀；
   - consent 能否被系統執行。
4. 搜尋最接近 G1/G2 的當前工作並記錄 publication status。

**停止／縮限條件**

> 若當前文獻已有公開、跨生成器、跨通道、含 laundering 與 adaptive attacker 的獨立評估，則取消或縮小 G1。若已有可驗證來源、能抵抗上述處理且明確處理 absence-of-mark 的 provenance 系統，則取消或縮小 G2。

## 10. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T5-05、T7-01、T7-02、T7-03、T7-04、T7-05

## 11. 專案狀態影響

本分析與現有五個 thesis candidate families 有直接關聯，但沒有核可任何方向，也不修改 `PROJECT.md` 或 `DECISIONS.md`。G1/G2 應進入外部驗證，而不是直接成為 thesis claim。
