# S1：文字與語言表示的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：`papers/tts-history/` 中 T1-01 至 T7-05，共 35 篇
- 分析單位：論文對文字輸入、語言特徵、發音、跨語言能力及失敗案例所提出的命題
- 判決限制：本文只能判斷「35 篇內是否形成殘餘問題」，不能據此宣稱整個 TTS 領域存在 novelty gap

## 1. 問題與範圍框線

### 核心問題

> 從規則式系統到大規模提示式模型，文字被轉換成何種語言表示；減少人工前端是否同時保留發音正確性、跨語言能力與分布外穩健性？

### 納入

- text normalization、grapheme、character、phoneme 與 linguistic features；
- pronunciation、罕見詞、姓名、語言特定音系規則；
- multilingual／cross-lingual text conditioning；
- 文字表示對內容正確性、對齊與泛化的影響。

### 排除

- 純說話者相似度，歸入 S6；
- 純波形 decoder 品質，歸入 S4；
- 一般資料規模效應，除非直接改變文字／發音覆蓋，否則歸入 S7。

## 2. 判決規則

令 `C` 為 35 篇封閉語料，`T` 為待驗證命題。本文只在下列條件同時成立時，標記 **Supported closed-corpus gap**：

1. `T` 對文字到語音映射有實質影響；
2. `C` 中至少有一篇提供問題、失敗或互斥取捨的直接證據；
3. `C` 中沒有論文在條件匹配下充分驗證解法；
4. 此結論被限定為 `C` 內，不外推到未搜尋的文獻。

若只有第 3 項，則判為 **Search lead only**，避免把「選樣未收錄」誤判為研究缺口。

## 3. 證據地圖

| 時期／論文 | 可抽取命題 | 證據狀態 | 對本範圍的意義 |
|---|---|---|---|
| T1-02 YorkTalk | 規則式 TTS 的問題包含音系表示與規則組織，不只是低階聲學控制 | Verified | 文字表示從一開始就是獨立瓶頸 |
| T1-03 Korean TTS | 韓語系統需要語言特定文字處理、音高、能量、時長規則與 demisyllable database | Verified | 一種語言的規則不能無條件泛化到另一種語言 |
| T2-05 Multisyn | open-domain unit selection 仍受 pronunciation variation、語料覆蓋與前端標註影響 | Verified | 真人片段沒有消除文字／發音覆蓋問題 |
| T3-01–T3-05 | HMM-SPSS 依賴高維 context-dependent linguistic features 與 decision-tree clustering | Verified | 語言知識被顯式編碼後再交給統計模型 |
| T4-01 Zen DNN | DNN 改善 linguistic-to-acoustic mapping，但保留人工 linguistic features | Verified | 神經網路替換回歸器，不等於移除前端 |
| T5-02 Tacotron | character-to-spectrogram 減少 phoneme aligner 與手工 linguistic features | Verified | 文字表示開始由資料學習 |
| T5-03 Deep Voice 3 | phoneme input 改善罕見詞與發音控制；attention 仍需位置／單調限制 | Verified | character 與 phoneme 表示存在可控制性取捨 |
| T5-04 Tacotron 2 | 錯誤仍集中於誤發音、姓名、異常韻律與 out-of-domain 文字 | Verified | 端到端學習沒有證明長尾發音已解決 |
| T7-02 VALL-E | 使用 phoneme condition 加 acoustic prompt；跨口音覆蓋仍有限 | Verified | 大規模 codec LM 仍保留顯式語言內容介面 |
| T7-03 Voicebox | 支援跨語言生成，但資料主要為 audiobook／read speech | Verified | 多語能力不等於所有語域、口音皆被覆蓋 |
| T7-05 MaskGCT | 英中資料與 VQ semantic codec 改善中英文內容建模，但未形成全面的文字表示比較 | Verified | semantic token 是新介面，並未消除輸入表示選擇 |

## 4. 命題鏈

### 命題 A：人工語言知識逐步減少

1. T1 直接以語言特定規則控制發音與聲學參數。
2. T3/T4 將這些知識改寫為 context-dependent linguistic features。
3. Tacotron 類系統直接從 character 或 phoneme 學習 spectrogram。
4. T7 將文字條件與 learned semantic／acoustic representation 結合。

**推論 A1（Inference）**

> 人工前端不是一次被移除，而是從顯式規則移到 phonemizer、文字 encoder、預訓練表示或訓練資料覆蓋中。

此推論否定「end-to-end 等於不再需要語言表示設計」。

### 命題 B：降低前端工程不蘊含發音問題消失

1. Tacotron 顯示 character-to-spectrogram 可運作。
2. Deep Voice 3 顯示 phoneme input 對罕見詞與發音控制有益。
3. Tacotron 2 仍回報姓名、誤發音與 out-of-domain 錯誤。

形式化表示：

```text
EndToEnd(x) → LessManualFrontend(x)
LessManualFrontend(x) ↛ PronunciationSolved(x)
```

其中 `↛` 表示前件不足以推出後件。

### 命題 C：多語展示不蘊含跨語言一般化

1. T1-03 證明語言特定規則的重要性。
2. Voicebox 與 MaskGCT 展示多語或英中生成。
3. 晚期論文明示 audiobook、口音與語域覆蓋限制。

因此：

```text
EvaluatedOnMultipleLanguages(x)
↛
GeneralizesAcrossLanguagesAccentsAndDomains(x)
```

## 5. 候選缺口推導

### G1：輸入表示對長尾發音與跨語言穩健性的受控歸因不足

**前提**

- character、phoneme、人工 linguistic features 與 semantic representation 均在語料中出現；
- Deep Voice 3 與 Tacotron 2 提供「表示選擇會影響罕見詞與發音錯誤」的直接線索；
- T7 的資料、模型規模、decoder 與訓練目標同時改變。

**推導**

```text
存在多種輸入表示 R1...Rn
∧ 表示與發音／跨語言結果相關
∧ 35 篇中沒有在固定資料、模型容量與 decoder 下比較 R1...Rn
→ 無法把長尾或跨語言差異歸因於輸入表示本身
```

**判決：Supported closed-corpus gap（causal／evaluation gap）**

這個判決只代表 35 篇沒有完成受控歸因；外部搜尋可能找到已完成的比較。

### G2：模型對「不知道如何發音」的可觀察狀態未被建立

**前提**

- 多篇論文記錄誤發音與 out-of-domain 失敗；
- 35 篇主要輸出語音或品質分數，沒有把發音不確定性作為可校準、可拒絕的輸出。

**推導**

```text
存在發音失敗
∧ 系統仍必須輸出單一語音
∧ 語料中未評估 pronunciation uncertainty
→ 35 篇沒有證明系統能辨識自身的發音未知
```

**判決：Search lead only**

原因是這組語料為生成技術史選樣，未收錄相關研究不能證明領域缺口。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「端到端 TTS 沒有研究文字表示」 | 拒絕 | Tacotron、Deep Voice 3、VALL-E、MaskGCT 都明確設計文字／音素介面 |
| 「沒有人做多語 TTS」 | 拒絕 | Voicebox 與 MaskGCT 已提供多語證據 |
| 「phoneme 一定優於 character」 | Unknown | Deep Voice 3 提供特定條件證據，但沒有跨架構普遍比較 |
| 「semantic token 已解決跨語言問題」 | 拒絕 | 英中結果不能推出所有語言、口音及語域皆成立 |

## 7. 最終判決

- **Verified：** 文字表示從手工規則、context features、character／phoneme encoder 演進到與 learned semantic representation 結合。
- **Inference：** 人工語言知識沒有消失，而是轉移到 phonemizer、encoder、資料與預訓練表示。
- **Supported closed-corpus gap：** 缺少在控制資料、模型容量與 decoder 後，對不同文字表示之長尾發音、跨語言及跨語域穩健性的因果比較。
- **Search lead only：** 發音不確定性、選擇性輸出或拒絕機制。
- **No-gap verdict：** 「是否已存在端到端文字輸入」及「是否已存在多語生成」在本語料中沒有缺口。

## 8. 下一個最小驗證步驟

1. 對外搜尋 `grapheme vs phoneme TTS rare words pronunciation OOD multilingual` 等查詢族。
2. 優先找固定資料與 decoder 的受控比較，而非只比較不同完整系統。
3. 若已有跨模型、跨語言且受控的完整評估，縮小或取消 G1。
4. 若只找到平均 WER／MOS，保留「長尾發音與跨語域」的較窄版本。

**停止條件**

> 若外部文獻已在相同資料、相同 backbone／decoder 下，系統比較 character、phoneme 與 learned semantic input，並涵蓋長尾詞、多語與 OOD，則本範圍不再保留研究缺口。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：本專案 `papers/tts-history/T1-01` 至 `T7-05`

## 10. 專案狀態影響

本分析不改變 `PROJECT.md` 或 `DECISIONS.md`。G1、G2 在外部文獻驗證前只能作為後續搜尋節點。
