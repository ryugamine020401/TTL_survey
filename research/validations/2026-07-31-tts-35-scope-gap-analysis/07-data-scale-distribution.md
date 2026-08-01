# S7：資料規模、品質與分布覆蓋的封閉語料缺口推導

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：35 篇 TTS 技術史封閉語料
- 分析單位：訓練資料量、品質、多樣性與測試分布如何影響自然度、泛化及失敗邊界
- 判決限制：35 篇不是資料集或 scaling-law 系統性回顧

## 1. 問題與範圍框線

### 核心問題

> TTS 的能力提升有多少來自方法、有多少來自資料規模與覆蓋；大量資料是否真正解決跨語言、口音、風格、說話者與真實場景泛化？

### 納入

- corpus size、speaker count、language／accent；
- read speech、audiobook、conversation、singing；
- clean、noisy、in-the-wild、cross-domain；
- speaker encoder data diversity；
- low-resource adaptation；
- data quality、coverage、training／test overlap；
- scaling 造成的能力與限制。

### 排除

- 純模型容量，除非與資料效應混淆；
- 文字表示本身，歸入 S1；
- 只討論身份 prompt 的因素，歸入 S6。

## 2. 邏輯模型

觀察到的系統表現可寫成：

```text
Performance =
f(Method, DataQuantity, DataQuality, DataDiversity,
  Compute, EvaluationDistribution)
```

若論文同時增加資料與更換方法，就不能只把結果歸因於方法。

## 3. 證據地圖

| 時期／論文 | 資料命題 | 直接結果或限制 | 狀態 |
|---|---|---|---|
| T1-03 Korean TTS | 語言特定規則與 demisyllable database | 跨語言需要重建語言知識與資料 | Verified |
| T2-01–T2-05 | 品質依賴錄音資料庫覆蓋 | out-of-domain、pronunciation、prosody 與 bad joins 是弱點 | Verified |
| T3-04 Yamagishi | average voice 可用少量、不完美、跨域資料調適 | unit selection 在大量乾淨同域較強，跨域下降更劇烈 | Verified |
| T3-05 SPSS Review | SPSS 支援小模型、多語、適應與不一致資料 | 品質仍受 acoustic model／vocoder 限制 | Verified |
| T5-03 Deep Voice 3 | 大規模多 speaker 資料 | noisy LibriSpeech 音質明顯下降 | Verified |
| T5-04 Tacotron 2 | 單 speaker 錄音室資料達高 MOS | names、異常文字與 OOD coverage 仍失敗 | Verified |
| T5-05 Jia | 大量、多樣 speaker encoder data | 對 unseen speaker 泛化關鍵；相似度仍下降 | Verified |
| T6-03 HiFi-GAN | 測試 unseen speaker | 提供 waveform 泛化局部證據 | Verified |
| T6-05 VITS | LJ／VCTK | 在有限 benchmark 接近 ground truth，不等於開放域已解決 | Verified |
| T7-01 AudioLM | 大規模無文字標註音訊 | 支援未見 speaker continuation | Verified |
| T7-02 VALL-E | 約 60K 小時半監督資料 | 3 秒 zero-shot；口音與資料覆蓋仍有限 | Verified |
| T7-03 Voicebox | 約 50K–60K 小時、多語 | audiobook／read speech 偏差與 prompt 屬性限制 | Verified |
| T7-04 NaturalSpeech 2 | 約 44K 小時 speech、較少 singing | audiobook coverage、僅少量 singing data 是限制 | Verified |
| T7-05 MaskGCT | 英中約 100K 小時 | 英中能力強，不能外推所有語言與語域 | Verified |

## 4. 命題推導

### 命題 A：每一代的失敗邊界都由資料覆蓋決定

- 規則式：知識與語言規則覆蓋；
- unit selection：候選片段與組合覆蓋；
- SPSS：訓練 context 與 speaker adaptation；
- end-to-end：paired text–speech 與 speaker diversity；
- prompt model：大規模資料中的語言、口音、風格與環境覆蓋。

**Inference**

> 模型把「缺少規則」轉化成「缺少訓練分布」，但沒有取消 coverage 問題。

### 命題 B：更多資料不蘊含任意分布泛化

```text
LargeDataset(x)
∧ HighInDomainPerformance(x)
↛
GeneralizesToAllAccentsStylesChannels(x)
```

VALL-E、Voicebox、NaturalSpeech 2 的作者限制直接支持此非蘊含關係。

### 命題 C：方法與資料效應高度混淆

T7 相較 T5/T6 同時改變：

- 資料從數十／數百小時增加到數萬小時；
- speaker、語言及錄音條件增加；
- 模型容量與預訓練增加；
- 表示從 mel 轉為 codec／latent；
- 評估任務改為 zero-shot、多語與多任務。

因此不能由整體系統勝出推出某一單一架構因素是原因。

## 5. 候選缺口推導

### G1：資料數量、品質與多樣性的因果效應未被分離

**前提**

- 小資料適應、大規模預訓練與資料多樣性均被證明有用；
- 35 篇沒有固定架構後，對 quantity × quality × diversity 做完整 factorial comparison；
- 晚期結果常同時增加資料和模型。

**推導**

```text
若 Quantity、Quality、Diversity 同時變動，
則 improvement 無法唯一歸因於其中一項。
```

**判決：Supported closed-corpus gap（causal／scaling gap）**

### G2：跨分布能力缺少共同壓力測試矩陣

**缺失矩陣**

```text
Language × Accent × SpeakingStyle × Speaker
× Channel/Noise × TextDomain × PromptQuality
```

各論文涵蓋其中部分，但沒有共同 test matrix 與 macro-level 報告。

**判決：Supported closed-corpus gap（dataset／evaluation gap）**

### G3：訓練與測試重疊、speaker exposure 與資料 lineage

35 篇摘要與系統結果不足以建立現代大型語料的完整 lineage、deduplication 與 speaker exposure。

**判決：Search lead only**

這需要 dataset cards、訓練 manifest、作者 repository 與後續 audit，不可由生成結果推定。

## 6. 被拒絕的缺口說法

| 說法 | 判決 | 理由 |
|---|---|---|
| 「TTS 尚未使用大規模資料」 | 拒絕 | T7 已使用數萬至十萬小時 |
| 「更多資料一定提高所有能力」 | 拒絕 | 作者自述仍有口音、語域與情境覆蓋限制 |
| 「小資料無法做 speaker adaptation」 | 拒絕 | T3-04 已提供少量調適證據 |
| 「大模型結果完全來自架構」 | 不成立 | 資料、算力、表示與任務同步改變 |
| 「英中有效等於多語一般化」 | 拒絕 | 量詞超出測試範圍 |

## 7. 最終判決

- **Verified：** 資料規模從語言規則／專屬資料庫擴展到數萬至十萬小時預訓練。
- **Verified：** 大資料帶來 zero-shot 和多語能力，但論文明示 coverage 仍有限。
- **Supported closed-corpus gap：** quantity、quality、diversity 與 model scale 的因果效應未被充分分離。
- **Supported closed-corpus gap：** 缺少共同的跨語言、口音、風格、speaker、channel 與 prompt-quality 壓力測試矩陣。
- **Search lead only：** 大型訓練資料的 lineage、speaker exposure、去重與污染。
- **No-gap verdict：** 「是否已有大規模 TTS」及「是否有少量調適」沒有缺口。

## 8. 下一個最小驗證步驟

1. 搜尋 TTS data scaling law、data quality vs quantity、cross-domain zero-shot TTS benchmark。
2. 優先找固定模型、分層 subsampling 與 paired quality controls。
3. 核對是否使用 speaker／language／accent macro average，而不是只報 pooled score。
4. 對候選大型資料集查 dataset card、license、deduplication、speaker overlap 與可取得性。

**停止條件**

> 若外部文獻已在固定模型和算力下，系統分離資料量、品質、多樣性效應，並建立公開的跨分布壓力矩陣，則取消 G1/G2；若只有單一完整系統 scaling，仍不足以取消。

## 9. 證據來源

- [35 篇核心文獻清單](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：T2-01 至 T2-05、T3-04、T3-05、T5-03 至 T5-05、T6-03、T6-05、T7-01 至 T7-05

## 10. 專案狀態影響

不修改 `PROJECT.md` 或 `DECISIONS.md`。G2 與目前 thesis 的 distribution shift 問題高度相關，但必須再加入 detection 資料與威脅模型，不能由 TTS 生成語料直接轉成 detector gap。
