# TTS 評測向度分類 / A Taxonomy of TTS Evaluation Dimensions

> 本檔為同一份內容的中英兩版。中文版在前，英文版在後（[English version](#english-version)）。

---

# 中文版

## 1. 為什麼原本的清單需要重新分層

原始的八項清單是**可用的檢查表，但不是好的向度集**，因為這八項不在同一個抽象層級上：

- 「可懂度」「自然度」「相似度」「可控性」是**對一個輸出樣本**可以直接評的性質。
- 「穩定性」不是新的性質，而是上述性質在**分佈尾端**的讀數（同一個 WER，看的是 P95 而不是平均）。
- 「泛化／資料效率」同樣不是新的性質，而是上述性質在**訓練分佈之外**的讀數。
- 「延遲／模型大小」與音檔內容無關，是**取得上述性質所付出的代價**。
- 「安全」不是系統的性質，而是系統 × 使用情境 × 對手的性質，而且**方向相反**：其他向度越好，此向度風險越高。

把它們平行列成八點，會誤導成「八個可以各自加分的項目」。實際上它們是**四個層級**，而且後三層是前一層的函數。

**分層依據（三個問題）：**

| 問題 | 分出的層級 |
|---|---|
| 評測對象是單一樣本，還是輸出分佈？ | A 層 vs B 層 |
| 評測需要參考音訊／條件輸入嗎？ | A 層內部的子軸 |
| 評測的是音訊、系統，還是社會後果？ | A/B 層 vs C 層 vs D 層 |

---

## 2. 建議的向度結構：4 層 / 6 軸

```
A. 輸出品質（樣本層級，可對單一 utterance 評分）
   A1 可懂度與文字忠實度      —— 說對字了嗎？
   A2 自然度與訊號品質        —— 聽起來像真人錄的嗎？
   A3 條件符合度              —— 符合被要求的條件嗎？
        A3a 參考驅動（隱式條件）：說話者／口音／情緒／韻律／錄音環境相似度
        A3b 標籤驅動（顯式條件）：時長／語速／F0／停頓／風格可控性

B. 可靠性（分佈層級，A 軸的不同統計量／不同分佈讀數）
   B1 穩定性        —— A 軸的「尾端」：最差的 1% 有多差、失敗率多高
   B2 泛化與資料效率 —— A 軸的「域外」：未見說話者、跨語言、跨領域、低資源

C. 系統成本（與音訊內容無關）
   C1 效率與部署    —— 延遲、吞吐量、參數量、記憶體、裝置端可行性

D. 社會技術（系統 × 情境 × 對手，方向與 A–C 相反）
   D1 安全、濫用與可偵測性 —— 冒用聲音、詐騙、合成語音偵測、浮水印、同意機制
```

**最重要的一個合併與一個拆分：**

1. **合併：** 「相似度」與「可控制性」應是**同一軸的兩種形態**（A3）。兩者都在問「輸出是否符合被指定的條件」，差別只在條件的表示法是參考音訊（隱式）還是數值／標籤（顯式），指標形式同樣是「條件與輸出之間的距離」。分成兩軸會讓 zero-shot 音色複製與風格控制看起來像兩種不同能力，但它們共用同一個 conditioning 機制，且常常此消彼長。
2. **拆分：** 「穩定性」應明確標記為 **A 軸的尾端統計**，不可與 A 軸平均值並列。一個系統的平均 MOS 4.3 但每 200 句崩潰一次，和平均 MOS 4.1 但零崩潰，在單一清單上無法比較；在 A×B 矩陣上則一目了然。

因此**報告形式應是矩陣，不是清單**：A 軸為列、B 條件（域內／尾端／域外）為欄，C 標在表頭作為預算，D 獨立成節。

---

## 3. 各向度定義、指標與陷阱

### A1 可懂度與文字忠實度

| 項目 | 內容 |
|---|---|
| 問題 | 輸出是否忠實傳達輸入文字？ |
| 子項 | 音素正確性、破音字／多音字、數字與縮寫正規化（TN）、外來語與混語、插入／刪除（幻覺、漏字） |
| 常用指標 | ASR 轉寫後的 WER／CER、音素錯誤率、intelligibility MOS、多音字準確率、TN／G2P 準確率 |
| 陷阱 | ASR 本身有偏誤：對合成語音、口音、低資源語言的 WER 不等於人類可懂度；WER 低也可能是輸出過度「標準化」而喪失自然度 |

### A2 自然度與訊號品質

| 項目 | 內容 |
|---|---|
| 問題 | 聽起來像真人在真實環境中錄的嗎？ |
| 子項 | 韻律自然度、音段品質、雜訊／偽影（金屬聲、嗡鳴、斷點）、頻寬與取樣率 |
| 常用指標 | MOS／CMOS（主觀）、UTMOS／NISQA／DNSMOS（無參考自動）、PESQ／ViSQOL（有參考，僅適用於重建任務） |
| 陷阱 | MOS 跨論文不可比（受評分者、指示語、樣本池影響），只能用同批 listening test 內比較；自動 MOS 預測器在其訓練分佈外會失效；「自然度」與「與參考相似」常被受試者混為一談，必須分開設題（MOS vs SMOS） |

### A3 條件符合度

**A3a 參考驅動（相似度）**

| 項目 | 內容 |
|---|---|
| 問題 | 輸出是否符合參考音訊隱含的條件？ |
| 子項 | 說話者音色、口音、情緒、韻律風格、錄音／通道環境 |
| 常用指標 | SMOS（主觀）、說話者嵌入餘弦相似度 SECS（WavLM／ECAPA）、口音分類正確率、情緒分類正確率或情緒嵌入相似度、F0 RMSE／相關係數、時長相關係數、DTW 距離、通道匹配（RT60 誤差、SNR 匹配） |
| 陷阱 | 說話者相似度與**編碼器選擇高度相關**，不同 encoder 排序可能反轉；SECS 高不代表人耳覺得像；環境相似度容易被忽略，但是決定「像不像同一段錄音」的關鍵；相似度提高常以音質下降為代價 |

**A3b 標籤驅動（可控制性）**

| 項目 | 內容 |
|---|---|
| 問題 | 給定明確的控制目標，輸出是否照做？ |
| 子項 | 總時長、語速、F0 平移／範圍、停頓位置與長度、強調、風格／情緒強度 |
| 常用指標 | 控制誤差（目標 vs 實測：duration error、rate error、F0 shift 誤差、停頓位置命中率）、控制範圍（可達區間）、解耦度（改動一個屬性時其他屬性的漂移量） |
| 陷阱 | 只報「能控制」而不報**控制範圍與解耦度**，是最常見的高估；在極端控制值下自然度與可懂度會塌陷，必須報告 quality-vs-control 曲線而非單點 |

### B1 穩定性

| 項目 | 內容 |
|---|---|
| 問題 | 最差的情況有多差？多久壞一次？ |
| 子項 | 漏字、重複、提前截斷、長句漂移、無限延長、隨機種子敏感度、對抗性輸入（超長句、純數字、標點異常、混語、空白） |
| 常用指標 | 失敗率（每 N 句）、WER 的 P95／P99（而非平均）、重複／截斷偵測率、長篇合成的品質漂移曲線、跨種子變異數 |
| 陷阱 | **絕不可用平均值代表穩定性**；測試集若只有乾淨短句，穩定性數字沒有意義；自迴歸模型與非自迴歸模型的失敗模式不同，需分別設計探測輸入 |

### B2 泛化與資料效率

| 項目 | 內容 |
|---|---|
| 問題 | 離開訓練分佈後，A 軸還剩多少？ |
| 子項 | 未見說話者、未見語言／口音、跨領域（朗讀 vs 自發口語）、跨錄音條件、低資源語言、few-shot 所需秒數 |
| 常用指標 | 同一組 A 軸指標，但分「域內／域外」兩欄報告；資料量-效能曲線；enrollment 秒數-相似度曲線 |
| 陷阱 | 「unseen speaker」若與訓練集同一個語料庫，仍是域內；跨資料集才算；資料效率必須報告**曲線**，單點「只要 3 秒」不可比 |

### C1 效率與部署

| 項目 | 內容 |
|---|---|
| 問題 | 達到上述品質要付多少代價？ |
| 子項 | 首包延遲（TTFB）、即時率 RTF、串流吞吐量、參數量、記憶體峰值、量化後表現、裝置端功耗與熱 |
| 常用指標 | 上述數值 **＋ 明確的硬體與批次設定**；量化前後的 A 軸對照 |
| 陷阱 | 效率數字若未綁定品質即無意義，應報告「在 X 延遲預算下的 A 軸表現」；串流與離線的品質不同，不可互相引用 |

### D1 安全、濫用與可偵測性

| 項目 | 內容 |
|---|---|
| 問題 | 這個能力被誤用時會造成什麼？能否被驗證或撤銷？ |
| 子項 | 未經同意的聲音冒用、語音詐騙與社交工程、繞過聲紋驗證（ASV spoofing）、合成語音偵測、來源證明與浮水印、同意與授權機制 |
| 常用指標 | 偵測器在該系統輸出上的 EER／min-tDCF（未見生成器條件下）、ASV 攻擊成功率、浮水印在壓縮／重錄／變速下的存活率與不可感知性、對抗性洗白後的殘存偵測率 |
| 陷阱 | **這一軸與 A–C 反向**：A2、A3a 越好，D1 風險越高，因此不可與其他軸加總成單一分數；偵測器在**已見生成器**上的表現嚴重高估實際能力，必須以未見生成器／未見通道評估；浮水印的保證（來源證明）與被動偵測的保證（真偽判斷）不同，不可互相替代 |

---

## 4. 向度之間的權衡（不可獨立最佳化）

| 權衡 | 說明 |
|---|---|
| A1 ↔ A2 | 追求低 WER 易導致過度標準化的平板韻律；追求表現力易增加誤讀 |
| A3a ↔ A2 | 複製含雜訊／混響的參考音訊時，相似度與音質直接衝突（要像就得複製雜訊） |
| A3b ↔ A2 | 控制值越極端，自然度越差 |
| A3a ↔ A3b | 強參考條件會壓縮顯式控制的可達範圍（解耦不足） |
| B1 ↔ A2 | 高表現力／高隨機性的取樣策略提高自然度上限，但抬高尾端失敗率 |
| C1 ↔ 全部 | 蒸餾、量化、非自迴歸化通常先犧牲 A3b 與 B1，其次才是 A2 |
| D1 ↔ A2/A3a/B2 | **正向能力即風險**：越自然、越像、越能泛化到未見說話者，冒用與詐騙門檻越低，偵測越難 |

---

## 5. 最小報告集（避免只報有利數字）

一份可信的 TTS 評測至少應包含：

1. **A1／A2／A3** 各一個主觀指標與一個客觀指標，主觀部分明確區分 MOS 與 SMOS 題目。
2. **B1**：失敗率與 WER 的 P95，且測試集包含刻意的困難輸入。
3. **B2**：至少一組**跨資料集**的未見說話者結果，與域內結果並列。
4. **C1**：硬體、批次、串流／離線設定，以及「在該延遲預算下」的 A 軸數值。
5. **D1**：至少說明資料來源同意狀態、是否加浮水印，以及輸出在公開偵測器上的可偵測性。
6. 明列**未測項目**，而非留白。

---

## 6. 與音訊深偽研究的接點（本專案相關）

在深偽偵測／來源驗證的研究裡，這個分類的用法會反轉：A、B、C 是**對手能力的描述**，D 是**防禦方的評測面**。具體而言：

- A2／A3a 決定攻擊的**可信度上限**（人類是否會上當）。
- B1 決定攻擊的**可用率**（對手要重試幾次才能拿到一句可用的音檔）——這也是被低估的偵測線索：失敗樣本不會被送出，因此野外樣本的分佈是被對手篩選過的。
- B2 與 C1 共同決定攻擊的**規模與成本**（能否即時、能否在裝置端、需要多少目標音訊）。
- D1 是防禦方的實際評測面，且必須在**未見生成器、未見通道、經壓縮與洗白**的條件下報告，否則會系統性高估。

換言之，威脅模型應明確指出對手在 A–C 上位於哪個點，D 的評測條件才有意義。

---
---

<a id="english-version"></a>

# English Version

## 1. Why the original list needs re-layering

The original eight-item list is **a usable checklist but a poor set of axes**, because the items do not sit at the same level of abstraction:

- Intelligibility, naturalness, similarity, and controllability are properties evaluable **on a single output sample**.
- Robustness is not a new property — it is a reading of the above properties **in the tail of the distribution** (the same WER, read at P95 instead of the mean).
- Generalization / data efficiency is likewise not a new property — it is a reading of the above properties **outside the training distribution**.
- Latency and model size are independent of audio content; they are **the price paid** for the properties above.
- Safety is not a property of the system but of system × context × adversary, and it runs **in the opposite direction**: the better the other axes, the higher the risk on this one.

Listing all eight in parallel implies "eight items you can independently score points on." In reality they form **four tiers**, and the later tiers are functions of the earlier ones.

**Basis for the layering (three questions):**

| Question | Separates |
|---|---|
| Is the unit of evaluation a single sample or the output distribution? | Tier A vs Tier B |
| Does evaluation require a reference / conditioning input? | Sub-axes within Tier A |
| Is the object of evaluation the audio, the system, or the social consequence? | A/B vs C vs D |

---

## 2. Proposed structure: 4 tiers / 6 axes

```
A. Output quality (per-sample; scorable on a single utterance)
   A1 Intelligibility & text fidelity   — did it say the right words?
   A2 Naturalness & signal quality      — does it sound like a real recording?
   A3 Conditional conformance           — does it match what was asked for?
        A3a Reference-driven (implicit): speaker / accent / emotion / prosody /
            recording-environment similarity
        A3b Label-driven (explicit): duration / rate / F0 / pause / style control

B. Reliability (distribution-level; different statistics or distributions of A)
   B1 Robustness            — the tail of A: how bad is the worst 1%, how often it breaks
   B2 Generalization & data efficiency — A out of domain: unseen speakers,
      cross-lingual, cross-domain, low-resource

C. System cost (independent of audio content)
   C1 Efficiency & deployment — latency, throughput, parameters, memory, on-device

D. Sociotechnical (system × context × adversary; direction opposite to A–C)
   D1 Safety, misuse & detectability — voice impersonation, fraud, synthetic-speech
      detection, watermarking, consent
```

**The one merge and the one split that matter most:**

1. **Merge:** similarity and controllability should be **two forms of one axis** (A3). Both ask whether the output conforms to a specified condition; they differ only in how the condition is expressed — reference audio (implicit) versus a value or label (explicit) — and both are measured as a distance between condition and output. Splitting them makes zero-shot voice cloning and style control look like different capabilities, when they share one conditioning mechanism and routinely trade off against each other.
2. **Split:** robustness must be labelled explicitly as **a tail statistic of A**, never listed alongside A's means. A system with mean MOS 4.3 that collapses once every 200 utterances cannot be compared against mean MOS 4.1 with zero collapses on a flat list; on an A×B matrix the difference is immediate.

Consequently, **results should be reported as a matrix, not a list**: A axes as rows, B conditions (in-domain / tail / out-of-domain) as columns, C stated in the header as the budget, D in its own section.

---

## 3. Definitions, metrics, and pitfalls

### A1 Intelligibility & text fidelity

| Item | Content |
|---|---|
| Question | Does the output faithfully convey the input text? |
| Sub-items | Phonetic correctness, heteronyms/polyphones, number and abbreviation normalization (TN), loanwords and code-switching, insertions/deletions (hallucination, skipping) |
| Metrics | WER/CER via ASR transcription, phoneme error rate, intelligibility MOS, polyphone accuracy, TN/G2P accuracy |
| Pitfalls | The ASR itself is biased: its WER on synthetic speech, accents, and low-resource languages is not human intelligibility. A low WER can also mean the output was over-normalized at the cost of naturalness. |

### A2 Naturalness & signal quality

| Item | Content |
|---|---|
| Question | Does it sound like a human recorded in a real environment? |
| Sub-items | Prosodic naturalness, segmental quality, noise/artifacts (metallic timbre, buzz, discontinuities), bandwidth and sample rate |
| Metrics | MOS/CMOS (subjective); UTMOS/NISQA/DNSMOS (no-reference automatic); PESQ/ViSQOL (reference-based, valid only for reconstruction tasks) |
| Pitfalls | MOS is not comparable across papers (rater pool, instructions, sample pool); only within-test comparisons are valid. Automatic MOS predictors fail outside their training distribution. Listeners conflate "natural" with "similar to the reference" unless MOS and SMOS are asked as separate questions. |

### A3 Conditional conformance

**A3a Reference-driven (similarity)**

| Item | Content |
|---|---|
| Question | Does the output match the conditions implied by the reference audio? |
| Sub-items | Speaker timbre, accent, emotion, prosodic style, recording/channel environment |
| Metrics | SMOS (subjective); speaker-embedding cosine similarity SECS (WavLM/ECAPA); accent and emotion classification accuracy or embedding similarity; F0 RMSE/correlation; duration correlation; DTW distance; channel match (RT60 error, SNR match) |
| Pitfalls | Speaker similarity is **highly encoder-dependent** — rankings can invert across encoders. High SECS does not imply perceived similarity. Environment similarity is routinely ignored yet largely determines whether two clips sound like the same recording. Similarity gains often cost signal quality. |

**A3b Label-driven (controllability)**

| Item | Content |
|---|---|
| Question | Given an explicit control target, does the output comply? |
| Sub-items | Total duration, speaking rate, F0 shift/range, pause placement and length, emphasis, style/emotion intensity |
| Metrics | Control error (target vs measured: duration, rate, F0 shift, pause-position hit rate); control range (attainable interval); disentanglement (drift in other attributes when one is changed) |
| Pitfalls | Reporting "it is controllable" without **range and disentanglement** is the most common overstatement. Naturalness and intelligibility collapse at extreme control values, so report a quality-vs-control curve, not a single point. |

### B1 Robustness

| Item | Content |
|---|---|
| Question | How bad is the worst case, and how often does it occur? |
| Sub-items | Skipping, repetition, early truncation, long-form drift, runaway generation, seed sensitivity, adversarial inputs (very long sentences, bare digits, unusual punctuation, code-switching, empty input) |
| Metrics | Failure rate per N utterances; P95/P99 of WER (not the mean); repetition/truncation detection rate; quality-drift curve over long-form synthesis; cross-seed variance |
| Pitfalls | **Never represent robustness by a mean.** A test set of clean short sentences makes the number meaningless. Autoregressive and non-autoregressive models fail differently and need separately designed probe inputs. |

### B2 Generalization & data efficiency

| Item | Content |
|---|---|
| Question | How much of axis A survives outside the training distribution? |
| Sub-items | Unseen speakers, unseen languages/accents, cross-domain (read vs spontaneous), cross-recording-condition, low-resource languages, seconds of enrollment needed for few-shot |
| Metrics | The same A-axis metrics, reported in separate in-domain / out-of-domain columns; data-volume-vs-performance curves; enrollment-seconds-vs-similarity curves |
| Pitfalls | "Unseen speaker" drawn from the same corpus as training is still in-domain; only cross-corpus counts. Data efficiency must be reported as a **curve** — a single "only 3 seconds needed" claim is not comparable. |

### C1 Efficiency & deployment

| Item | Content |
|---|---|
| Question | What does the above quality cost? |
| Sub-items | Time-to-first-byte, real-time factor, streaming throughput, parameter count, peak memory, post-quantization behavior, on-device power and thermals |
| Metrics | The above numbers **plus explicit hardware and batch settings**; A-axis before/after quantization |
| Pitfalls | Efficiency numbers are meaningless unless bound to quality — report "A-axis performance under an X latency budget." Streaming and offline quality differ and must not be cited for each other. |

### D1 Safety, misuse & detectability

| Item | Content |
|---|---|
| Question | What happens when this capability is misused, and can it be verified or revoked? |
| Sub-items | Non-consensual voice impersonation, voice fraud and social engineering, bypassing speaker verification (ASV spoofing), synthetic-speech detection, provenance and watermarking, consent and authorization |
| Metrics | Detector EER / min-tDCF on this system's output **under unseen-generator conditions**; ASV attack success rate; watermark survival under compression, re-recording, and time-stretching, plus imperceptibility; residual detection rate after adversarial laundering |
| Pitfalls | **This axis runs opposite to A–C**: better A2 and A3a mean higher D1 risk, so it cannot be summed into a single overall score. Detector performance on **seen generators** severely overstates real capability; evaluate on unseen generators and unseen channels. Watermarking guarantees provenance while passive detection guarantees a real/fake judgment — they are not substitutes. |

---

## 4. Trade-offs (the axes cannot be optimized independently)

| Trade-off | Explanation |
|---|---|
| A1 ↔ A2 | Chasing low WER produces over-normalized, flat prosody; chasing expressiveness raises mispronunciation |
| A3a ↔ A2 | Cloning a noisy or reverberant reference puts similarity in direct conflict with signal quality — sounding alike means reproducing the noise |
| A3b ↔ A2 | The more extreme the control value, the worse the naturalness |
| A3a ↔ A3b | Strong reference conditioning compresses the attainable range of explicit control (weak disentanglement) |
| B1 ↔ A2 | Expressive, high-entropy sampling raises the naturalness ceiling and the tail failure rate together |
| C1 ↔ all | Distillation, quantization, and non-autoregressive redesign typically sacrifice A3b and B1 first, A2 second |
| D1 ↔ A2/A3a/B2 | **Capability is the risk**: the more natural, the more similar, the better it generalizes to unseen speakers, the lower the bar for impersonation and fraud and the harder detection becomes |

---

## 5. Minimum reporting set (to prevent selective reporting)

A credible TTS evaluation should include at least:

1. **A1 / A2 / A3**: one subjective and one objective metric each, with MOS and SMOS asked as distinct questions.
2. **B1**: failure rate and P95 WER, on a test set that deliberately includes hard inputs.
3. **B2**: at least one **cross-corpus** unseen-speaker result, reported next to the in-domain result.
4. **C1**: hardware, batch, and streaming/offline settings, plus A-axis numbers *at that latency budget*.
5. **D1**: at minimum, the consent status of the training data, whether output is watermarked, and detectability under a public detector.
6. An explicit list of **what was not measured**, rather than silence.

---

## 6. Connection to audio-deepfake research (relevant to this project)

In deepfake detection and provenance research the taxonomy inverts: A, B, and C describe **adversary capability**, while D is **the defender's evaluation surface**. Specifically:

- A2 / A3a set the **credibility ceiling** of an attack (whether a human is fooled).
- B1 sets the attack's **yield** (how many retries before the adversary obtains one usable utterance). This is an underused detection cue: failed samples are never sent, so in-the-wild samples are a distribution already filtered by the adversary.
- B2 and C1 jointly set the attack's **scale and cost** (real-time or not, on-device or not, how much target audio is required).
- D1 is the defender's actual evaluation surface, and must be reported under **unseen generators, unseen channels, and after compression and laundering** — otherwise it is systematically overstated.

In short, a threat model must state where the adversary sits on A–C before the evaluation conditions for D mean anything.
