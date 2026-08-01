# TTS 35 篇封閉語料：十個範圍的研究缺口推導索引

- 日期：2026-07-31
- 研究模式：Synthesize + Validate
- 證據宇宙：`papers/tts-history/` 中 T1-01 至 T7-05，共 35 篇
- 目的：以一致的邏輯規則，判斷十個分析範圍在此封閉語料中是否形成殘餘問題
- 重要限制：本分析不是完整 novelty search；任何結論在外部搜尋前都不能寫成「整個領域沒有研究」

## 1. 共同推論流程

每份文件都使用下列流程：

```text
定義範圍與排除條件
→ 抽取原子命題
→ 建立跨時期證據鏈
→ 檢查非蘊含、矛盾、缺少聯合驗證與量詞越界
→ 尋找反例與已存在方法
→ 判定 closed-corpus gap / search lead / no-gap
→ 設定外部驗證與停止條件
```

原子命題格式：

```text
在條件 C 下，
方法 M 相較基準 B，
改善結果 R，
但沒有驗證條件 U。
```

## 2. 判決類別

| 判決 | 含義 |
|---|---|
| **Verified** | 可由 35 篇原始論文直接支持 |
| **Inference** | 由多篇命題合理推導，但不是單篇論文的直接宣稱 |
| **Supported closed-corpus gap** | 35 篇中有問題／張力證據，但沒有條件匹配的充分解法 |
| **Search lead only** | 只是 35 篇沒有覆蓋；需要外部搜尋，不能稱為缺口 |
| **No-gap verdict** | 指定問題在此語料中已有方法或證據，不保留為缺口 |
| **Unknown** | 證據不足或比較條件不相容 |

## 3. 十份分析

| 範圍 | 文件 | 主要 closed-corpus 結論 | 明確 no-gap 結論 |
|---|---|---|---|
| S1 文字與語言表示 | [01](01-text-linguistic-representation.md) | 不同輸入表示對長尾發音／跨語言穩健性的受控歸因不足 | 端到端文字輸入、多語 TTS 已存在 |
| S2 對齊與時長 | [02](02-alignment-duration.md) | 缺少穩健性—韻律—控制—延遲的 matched comparison；failure 定義不一致 | attention 以外的解法已存在 |
| S3 聲學表示 | [03](03-acoustic-representation.md) | discrete token／continuous latent／mel 缺少條件匹配比較；屬性可分離性不足 | 三類表示都已存在 |
| S4 波形生成 | [04](04-waveform-generation-vocoders.md) | decoder 家族缺少共同 conditioning 與成本下的比較 | 高品質、快速 neural vocoder 已存在 |
| S5 一對多與韻律 | [05](05-prosody-one-to-many-control.md) | diversity—quality—control—content 缺少共同評估；prompt 屬性糾纏 | 多樣生成與韻律控制已存在 |
| S6 說話者身份 | [06](06-speaker-identity-zero-shot.md) | 身份與 accent／prosody／channel 可分離性不足；prompt 泛化曲線不足 | 少量調適與 zero-shot cloning 已存在 |
| S7 資料與分布 | [07](07-data-scale-distribution.md) | quantity／quality／diversity 因果混淆；缺少共同跨分布壓力矩陣 | 大規模 TTS 與少量調適已存在 |
| S8 整合與效率 | [08](08-system-integration-efficiency-reliability.md) | 缺少多目標 Pareto benchmark；模組化／joint training 維護性未測 | fast／NAR／single-stage TTS 已存在 |
| S9 評估與歸因 | [09](09-evaluation-measurement-attribution.md) | 缺少多構念、子群、尾端風險與完整 factor attribution | 主觀與客觀評估均已存在 |
| S10 安全與來源 | [10](10-safety-provenance-detection.md) | same-generator detector 未建立跨生成器／通道／laundering 保證；provenance 證據不足 | 合成偵測與濫用討論已存在 |

## 4. 跨範圍重複項的分流

十個範圍並非互斥，因此以下問題只保留一個主要歸屬：

| 交集問題 | 主要文件 | 其他文件中的角色 |
|---|---|---|
| prompt 中 timbre、accent、prosody、channel 糾纏 | S6 | S3 談表示承載；S5 談韻律控制 |
| alignment 穩定與韻律多樣性 | S2 | S5 談一對多結果 |
| discrete vs. continuous | S3 | S8 談推論成本；S9 談比較效度 |
| model improvement vs. data scale | S7 | S9 談因果歸因 |
| decoder artifact 與 detector shortcut | S10 | S4 提供 waveform 來源 |
| OOD／channel shift | S7 | S10 在安全威脅模型下重新限定 |

## 5. 整體推論結果

### 已能由 35 篇支持

1. 方法不是匱乏點：十個範圍中，多數基本解法已存在。
2. 主要殘餘問題集中在：
   - 條件不匹配造成的不可歸因；
   - 多目標只分開量測、沒有聯合約束；
   - benchmark 結果被過度外推到語言、speaker、channel 或 attacker；
   - prompt 與 learned representation 將多種屬性糾纏；
   - 生成論文內的安全證據多為封閉世界。
3. 「有一個模型做到」與「該問題已在開放條件解決」不是同一命題。

### 不能由 35 篇推出

1. 不能宣稱任何候選是首次或 field-level gap。
2. 不能用跨論文 MOS／WER／similarity 直接排名系統。
3. 不能把沒有收錄 detection、watermark、HCI 或 production systems 論文視為那些領域沒有研究。
4. 不能因十個範圍都出現 closed-corpus gap，就推論十個範圍都有 thesis novelty。

## 6. 為何十個範圍都有 closed-corpus gap

這個結果需要特別紅隊檢查。35 篇是為了呈現七個 TTS 技術趨勢而選，不是為十個問題做均衡、系統性抽樣。因此：

```text
每個範圍都有未回答問題
可能來自：
  真正殘餘問題
  ∨ 歷史選樣偏差
  ∨ 評估論文未被納入
  ∨ 後續工作不在 35 篇中
```

所以每份文件都加入外部搜尋與停止條件。若搜尋找到充分解法，正確結論應是縮小或取消缺口，而不是保護原先推論。

## 7. 下一步驗證順序

若目的是建立完整領域知識圖，下一步可以依序：

1. 為每個 `Supported closed-corpus gap` 建立查詢字典與同義詞。
2. 搜尋原始論文、正式 proceedings、作者 repository 與 benchmark。
3. 記錄最接近工作、出版狀態、資料、條件與未涵蓋範圍。
4. 先嘗試反駁候選缺口。
5. 只有未被反駁者才進入 thesis feasibility、資料、計算與貢獻評估。

## 8. 證據來源

- [TTS 七大技術趨勢與 35 篇核心文獻](../../syntheses/2026-07-27-tts-seven-technical-trends-35-papers.md)
- [TTS 35 篇封閉語料精讀綜述](../../syntheses/2026-07-27-tts-history-closed-corpus-synthesis.md)
- 原始 PDF：`papers/tts-history/T1-01` 至 `T7-05`

## 9. 專案狀態影響

這組文件建立候選驗證樹，但沒有選定 thesis 題目，也不修改 `PROJECT.md` 或 `DECISIONS.md`。外部驗證工作應反映到 `TASKS.md`。
