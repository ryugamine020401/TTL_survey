# D4 計畫書：詐騙情境條件下語音深偽偵測的評估效度審計

> 撰寫日期：2026-07-23。本文為碩士論文候選方向 D4 之完整計畫書。所有 novelty 主張採 bounded wording，僅指「在本文記錄之搜尋範圍（2026-07-23）內未找到直接同題先作」，不等於證明不存在。引用僅列經查證之來源；查證依據見 `research/validations/2026-07-23-five-directions-contributions-rq-metrics-audit.md`。

---

## 1. 題目

- **中文**：《詐騙情境條件下語音深偽偵測的評估效度審計：一個繁體中文評測協定》
- **英文**：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Evaluation Protocol*

---

## 2. 研究背景

語音深偽（audio deepfake）已成為電信詐騙的實用工具：攻擊者可用開源 TTS/VC 在數秒內合成帶情緒的語音，冒充親友或權威機構向受害者施壓。為對抗此威脅，學界發展了一系列被動式深偽偵測器（如 AASIST [7]、以 wav2vec2 XLS-R [9] 自監督表徵為前端的 SSL-AASIST 變體），並在 ASVspoof、In-the-Wild 等公開基準上以 EER 與 fixed-FPR recall 回報成績。

然而這些成績單的**評測條件**與**詐騙現場條件**之間存在系統性落差。公開基準的 fake 多為錄音室朗讀、中性韻律、完整長句、乾淨或單一模擬通道；真正到達受害者耳朵的，卻是三秒左右、帶哭腔或急迫命令、走過電話編解碼通道、且承載「詐騙話術語意」的短音訊。2025 世代開源情緒 TTS（如 CosyVoice 2 [10]、F5-TTS [11]）已能可信地生成台灣國語的情緒語音，使此落差在 2026 年具實務急迫性。本計畫在**繁體中文（zh-TW／台灣國語）**這一特定語言脈絡下，量測並分解此評估效度落差。

---

## 3. 問題與痛點

現行語音深偽偵測基準的成績單，是用**錄音室朗讀長句**在**乾淨或單一通道**下考出的；廠商據此宣稱「能防詐」。但這種成績可能對**詐騙現場的三秒音訊**系統性高估其偵測能力。痛點有三：

1. **素材真實性樂觀偏差**：基準 fake 的長句、中性韻律、乾淨通道與詐騙現場的短句、情緒韻律、電話通道不匹配，成績單可能無法外推到部署現場。
2. **條件軸未受控地交纏**：時長、情緒、通道、話術語意等條件在既有研究中多半各自被單獨探討，缺少一個**受控 crossed 設計**去估計它們的**主效應與交互項**——尤其「詐騙話術語意／語用是否讓 TTS 露餡」與其他軸的交互，缺乏受控分解。
3. **品質與效度混淆**：情緒／短句 TTS 的合成品質本身可能較低；若不對品質做協變量調整，落差有多少來自「偵測器對現場失效」、有多少來自「較差的合成品質恰好較易被抓」，無法分離。

---

## 4. 研究動機

本計畫的動機是**評估誠實性**：在任何機構把某偵測器部署為反詐防線之前，其成績單應先在接近詐騙現場的條件下被審計。放棄「受騙率」作為因變數（因硬約束不做真人實測），改以**可計算、可複現、不需真人的機器事實**——固定 FPR（≤1%）下的 recall——作為因變數。本計畫不宣稱能救任何受害者；它量的是**評測條件與現場條件之間的落差總量、落差的因子結構，以及在品質 proxy 調整後仍殘餘的關聯**，作為「日後宣稱能防詐的偵測器需先通過的一關」的門檻證據。

---

## 5. 先前研究統整（誠實對照）

**各佔一軸的相鄰先作（非「全部單軸」的空白，而是各軸皆已有先作、僅其受控 crossed 交集未見）：**

- **時長 × 通道**："Hi!" [1]（ICASSP 2026）同時研究超短音訊（0.5–4 秒固定截斷）的 utterance duration 與通訊通道退化對偵測的影響。故「短音訊」與「通道劣化」本身**並非空白**。
- **情緒（中英情緒 VC）**：EmoFake [2]（CCL 2024）已研究英文／中文的情緒語音轉換與其對偵測的影響。故「情緒韻律」軸**已有先作**。
- **電詐音訊-文本語意**：TeleAntiFraud-28k [3] 已處理電信詐騙的音訊-文本語意資料。故「詐騙語意」在音訊-文本層面**已有先作**。
- **中文電詐深偽含通道條件**：CFSDD [4] 之資料卡明示中文語音深偽、電信詐騙、benign real vs fraudulent fake，並含 clean／noise／noise-suppression／codec 測試條件（其同行評審狀態與確切方言組成仍待確認）。故「中文電詐深偽」與「通道條件」**已有先作**。

**評測效度與品質配對相關工作：** UTMOS [5]（Interspeech 2022）為 MOS 預測模型，ECAPA-TDNN [8]（Interspeech 2020）為語者身分嵌入；兩者常被用作合成品質／語者相似度的 proxy。惟 UTMOS 的 OOD 泛化有限，且已有 score-preserving 攻擊 [6] 展示可在維持 UTMOS 分數的同時降低人類感知品質——故 proxy 配對只能支持「殘餘關聯」而非因果解耦（詳見 §7、§9）。

**殘餘缺口（bounded）：** 在本文記錄之搜尋範圍內，未找到將 **zh-TW × 詐騙話術語意 × 時長 × 情緒 × 通道**以**受控 crossed 因子設計 + mixed-effects 交互項估計**同時分解的直接同題先作。上述各軸雖各有相鄰先作，但其受控交互分解構成本計畫的目標缺口。此為 dataset-context intersection 的可繼續驗證缺口，**不主張**四軸各自無先作，亦不主張「詐騙語意變數零先作」。

---

## 6. 研究問題（RQ）

- **RQ1（落差總量）**：從標準朗讀條件到詐騙情境條件，固定 FPR（≤1%）下的 recall 落差總量有多大？
- **RQ2（主效應與交互項）**：zh-TW 話術語意、時長、情緒、通道四軸的**主效應**與**預先選定的交互項**效應量各為何（以 mixed-effects 估計，含 generator／speaker／sentence 隨機效應）？
- **RQ3（proxy 調整後殘餘）**：以 UTMOS 與 ECAPA proxy 調整合成品質與語者相似度後，偵測器誤差與話術語意／情緒／時長／通道之間的**殘餘關聯**還剩多少？
- **RQ4（外部效度）**：在 zh-CN 對照臂（SpeechFake ZH [12]／CFAD [13]）上，落差方向是否一致，以佐證落差非單一 zh-TW 腔調 artifact（僅對照切片，標為外部效度限制，不升為主軸）？

---

## 7. 方法論

**核心方法：受控析因的評估落差量測。** 在一份自建的 zh-TW 詐騙情境刺激上，量現成 **frozen** 偵測器的 fixed-FPR（≤1%）recall，用同一批前向做因子分解與品質配對——全程零訓練、零人工聽測、全機器計算。方法物件有四：

1. **自建 zh-TW 詐騙情境刺激**：以公開反詐話術（約 165 條刑事局／165 反詐公開話術）去識別化改寫成受控刺激，並配對中性文本對照臂，控制 lexical content。以 2 家 2025 世代開源情緒 TTS（CosyVoice 2 [10]、F5-TTS [11]；GPT-SoVITS／OpenVoice v2 為備選）自建生成。**因無合法可散布之音訊本體，本計畫產出稱 evaluation protocol／manifest（配方＋checksum），不稱可重用 corpus**（見 §8.2 與 §12 倫理）。
2. **四軸 crossed 因子設計**：話術語意（詐騙 vs 中性對照）× 時長（短句 ~3s vs 標準長句）× 情緒（3 層，如中性／急迫命令／哭腔）× 通道（offline codec 條件）。各 cell 由**同一組文本、同一組 speaker、同一組 generator** crossed 產生，以避免軸效應與 generator／speaker／lexical content 混淆。
3. **frozen 偵測器**：AASIST [7] + 以 XLS-R [9] 為前端的 SSL-AASIST（公開權重）；退路降為 2 套（AASIST + RawNet2 現成 checkpoint），全程不自行重訓。
4. **offline codec 通道**：以 CPU 端 codec（如 clean／CELP 類 AMR-WB／neural codec 類 EnCodec）自足施加，不接任何真實通道 rig。
5. **UTMOS + ECAPA proxy**：以 UTMOS [5] 預測 MOS、ECAPA-TDNN [8] 計算語者相似度，作為合成品質與語者身分的**協變量**（機器計算）。
6. **mixed-effects／hierarchical 分析**：因同句／同語者／同生成器產生重複結構，以 mixed-effects（線性混合模型，fixed effects＝四軸與交互項，random effects＝generator／speaker／sentence）估計效應量與交互項；**不**以 cell-wise 獨立檢定處理相依樣本。

**因果與 proxy 侷限的明確界線：** UTMOS 為 MOS 預測、ECAPA 為語者 proxy；兩者配對後最多能主張「在兩個 proxy 接近後仍有殘餘關聯」，**不能識別**「控制 TTS 品質後的偵測器現場失效」的因果量。UTMOS OOD 泛化有限且存在 score-preserving 攻擊 [6]。因此本計畫**不主張**「已排除低品質 TTS confounding」，僅主張 proxy 調整後殘餘關聯是否存在。

---

## 8. 實驗

### 8.1 設計、因子與 level

crossed 因子設計，四個 fixed factor：

| 軸 | Levels | 說明 |
|---|---|---|
| 話術語意 | 2：詐騙話術 / 中性對照 | 配對文本，控制 lexical content |
| 時長 | 2：短句 (~3s) / 標準長句 | 標準長句為對照 |
| 情緒 | 3：中性 / 急迫命令 / 哭腔 | 情緒可控 TTS 生成 |
| 通道 | 3：clean / CELP / neural codec | offline codec，逐格可控 |

Random effects：generator（2 家）、speaker、sentence（text item）。因變數：各 cell 的 TPR@FPR≤1%（recall）。主要 crossed cell 數 = 2×2×3×3 = 36（×偵測器 ×generator 為重複結構，納入隨機效應）。

### 8.2 資料集

- **自建 zh-TW 刺激（主）**：~165 條公開反詐話術去識別化改寫 + 配對中性文本；以 CosyVoice 2 [10]、F5-TTS [11] 生成 ~2–3 萬筆 fake；real 類取自公開 zh 真人語音。**僅發配方＋checksum，不散布合成詐騙語音本體。**
- **2025 情緒 TTS**：CosyVoice 2 [10]、F5-TTS [11]（GitHub／HF 開源 checkpoint；GPT-SoVITS／OpenVoice v2 備選）。月 0–1 硬 go/no-go 驗其情緒可控性。
- **zh-CN 對照臂（RQ4，僅對照）**：SpeechFake 開源部（ZH）[12]、CFAD [13]，抽樣佐證落差非單一腔調 artifact；**明標腔調為 zh-CN、屬外部效度限制，不升主軸**。
- **frozen 偵測器 checkpoint**：AASIST [7] 官方權重、XLS-R [9] 前端 SSL-AASIST 公開權重；退路 AASIST + RawNet2。皆 ASVspoof19 LA 訓練權重，**不重訓**。

### 8.3 參數、因子 level 與 GPU-h（≈180）

- 通道：offline codec 自足（CPU，近 0 GPU-h）。品質協變量：UTMOS + ECAPA（機器計算）。
- **GPU-h 結帳單（≈180，含 2.5× 重跑）**：S0 feasibility 8 + TTS 生成 75 + 通道施加 25 + 品質標註 18 + 主實驗析因前向 22 + 緩衝 25 ≈ **180**（悲觀含條件重訓約 190–315，用不到單張 RTX 4090 一年上限的 ~19%）。算力為全場最寬鬆；瓶頸是日曆（約 21–33 人週）與情緒 zh-TW TTS 取得性。
- **一年時程**：
  - 月 0–1：feasibility spike + **情緒 zh-TW TTS 硬 go/no-go 關卡**（不可用即切 crash-path B 三軸析因，不拖到月 8）+ 確認 XLS-R backend checkpoint 可得性。
  - 月 2–4：協定建構（生成 + 通道 + 品質標註）→ 保底：一份可重現的詐騙情境 ADD 評測協定。
  - 月 5–7：主實驗（RQ1 落差矩陣）→ 半篇 audit。
  - 月 8–10：多因子析因 + 品質 proxy 調整（RQ2、RQ3）+ zh-CN 對照（RQ4）。
  - 月 10–12：輕量發布（配方 + checksum，不散布合成詐騙語音本體）+ 寫作。

### 8.4 預期結果與表骨架（皆標「預期／推估」，不捏造數值）

**表 A（RQ1，預期）落差矩陣骨架**——每格填 TPR@FPR≤1%，`Δ` = 詐騙情境 − 標準朗讀：

| 條件 | AASIST | SSL-AASIST |
|---|---|---|
| 標準朗讀長句·clean（基準） | `r₀` | `r₀'` |
| 詐騙話術·短句·情緒·CELP | `r₁` | `r₁'` |
| 詐騙話術·短句·情緒·neural codec | `r₂` | `r₂'` |
| **落差 Δ = 基準 − 現場** | `Δ ≥ 0（預期）` | `Δ' ≥ 0（預期）` |

**預期／推估（方向性假設，非數值）**：H1 預期 `Δ > 0`（現場條件下 recall 系統性低於標準朗讀）。依據為 in-domain vs out-of-domain 與壓縮通道劣化已有文獻支撐，故落差為正的方向性推論較穩健；**具體數值待實測，不於計畫書階段給出**。

**表 B（RQ2，預期）mixed-effects 效應量骨架**——每列填 fixed-effect 估計與 95% CI：

| 效應項 | 估計（預期方向） | 備註 |
|---|---|---|
| 話術語意（主效應） | `β₁`（預期 <0，降 recall） | 單軸前作未直接量 |
| 時長（短句） | `β₂`（預期 <0） | 與 "Hi!" [1] 方向相容 |
| 情緒 | `β₃`（預期 <0） | 與 EmoFake [2] 相容 |
| 通道（neural codec） | `β₄`（預期 <0） | 與通道劣化文獻相容 |
| 語意 × 情緒（交互） | `β₁₃`（預期 ≠0，符號待估） | **本計畫目標交互項** |
| 語意 × 通道（交互） | `β₁₄`（預期符號待估） | 目標交互項 |

**表 C（RQ3，預期）proxy 調整前後殘餘骨架**：

| 模型 | 語意軸關聯 | 情緒軸關聯 |
|---|---|---|
| 未調整 | `a₀` | `b₀` |
| + UTMOS 協變量 | `a₁`（預期 |a₁|≤|a₀|） | `b₁` |
| + UTMOS + ECAPA 協變量 | `a₂`（**殘餘關聯**） | `b₂` |

**預期措辭**：若 proxy 調整後殘餘關聯 `a₂` 顯著非零，僅可主張「偵測器誤差與話術語意之關聯在 UTMOS/ECAPA proxy 調整後仍存在」，**不主張**「已排除低品質 TTS confounding」或因果品質解耦。

---

## 9. 結果分析與討論

**主情境（交互項顯著）**：若 RQ2 顯示語意 × 情緒或語意 × 通道交互項顯著，則落差不可由單軸主效應加總解釋，支持「受控 crossed 交互分解」的貢獻；並於 RQ3 報告 proxy 調整後殘餘關聯的量級。

**null 情境（交互不顯著）**：若所有交互項在 mixed-effects 下不顯著（效應量估計含 0），則主張**降為**「四軸主效應可加、無顯著交互」的負結果——這仍是有用的評測效度發現（表示可用單軸修正外推），且 RQ1 落差矩陣本身已獨立成篇。若 RQ1 落差本身很小（H0），則轉為「現行 benchmark 對詐騙情境的代表性驗證」之可發表否證。

**proxy 侷限**：UTMOS 為 MOS 預測、非人類聽測；其 OOD 泛化有限且有 score-preserving 攻擊 [6]。故 RQ3 之殘餘關聯僅為 proxy 調整後殘餘，**不識別因果品質解耦**；本計畫全程無人工聽測，此為方法論的自覺限制而非可補齊的缺口。

**外部效度限制**：（1）結論限於已量測之 generator／speaker population，不外推至閉源商用 TTS 世代；（2）zh-CN 對照臂（RQ4）之腔調為 zh-CN，僅佐證方向一致性，不等同 zh-TW；（3）offline codec 非真實蜂巢／PSTN 通道，通道軸為受控代理；（4）產出為 evaluation protocol／manifest，其在雲端 TTS 版本或 preprocessing 改變後可能無法重建相同 bytes，故不宣稱可直接重用 corpus。

**退路可靠度**：核心假設（現場素材 ≠ 標準素材）幾乎不可能全滅；月 4 有自足協定、月 7 有半篇 audit。情緒 TTS 月 1 不可用或話術語意軸無效 → crash-path B 三軸析因（樣本層檢定力足，主效應由單軸前作幾乎保證存在）。XLS-R 取不到 → 降 2 套偵測器。

---

## 10. 總結

本計畫在繁體中文脈絡下，以 **zh-TW × 話術語意 × 時長 × 情緒 × 通道的 crossed 因子設計**、**mixed-effects 交互項估計**與 **UTMOS+ECAPA proxy 調整後殘餘關聯**三者為核心貢獻，審計現行語音深偽偵測成績單對詐騙情境的評估效度落差。它以機器可計算的 fixed-FPR recall 為因變數，一人一年、單張 RTX 4090、GPU-h≈180、不做真人實測即可完成，並在核心假設破裂時仍有多層可發表退路。

---

## 11. 未來展望

- 人工聽測（human MOS）以補 proxy 侷限、真正逼近因果品質解耦；
- 擴至閉源商用 TTS 世代與真實蜂巢／PSTN 通道以增外部效度；
- 若能建立合法可散布之凍結生成管線（凍結模型 + seed + 環境 + 授權 + deterministic pipeline），將 evaluation protocol 升級為可重用 corpus；
- 將受控交互分解方法轉移至其他語言／其他高風險情境（如金融客服、緊急求助）。

---

## 12. 參考文獻（僅列查證過之來源）

1. Y. Zhang et al. *"Hi!": Toward Efficient and Lightweight Deepfake Speech Detection in Real-World Communication Scenarios.* ICASSP 2026. arXiv:2601.19573.
2. Y. Zhao et al. *EmoFake: An Initial Dataset for Emotion Fake Audio Detection.* CCL 2024. https://aclanthology.org/2024.ccl-1.99/
3. *TeleAntiFraud-28k: An Audio-Text Slow-Thinking Dataset for Telecom Fraud Detection.* arXiv:2503.24115.
4. *CFSDD: Chinese Fraud Speech Deepfake Dataset* (dataset card). HuggingFace `Izzyzlin/CFSDD`. https://huggingface.co/datasets/Izzyzlin/CFSDD （同行評審狀態與方言組成待確認）
5. T. Saeki et al. *UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022.* Interspeech 2022. https://www.isca-archive.org/interspeech_2022/saeki22c_interspeech.html
6. *Score-Preserving Attacks on UTMOS.* arXiv:2606.31105.
7. J. Jung et al. *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks.* ICASSP 2022.
8. B. Desplanques, J. Thienpondt, K. Demuynck. *ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification.* Interspeech 2020, pp. 3830–3834. arXiv:2005.07143.
9. A. Babu et al. *XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale.* Interspeech 2022. arXiv:2111.09296.
10. Z. Du et al. *CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models.* 2024. arXiv:2412.10117.
11. Y. Chen et al. *F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching.* 2024. arXiv:2410.06885.
12. W. Huang et al. *SpeechFake: A Large-Scale Multilingual Speech Deepfake Dataset Incorporating Cutting-Edge Generation Methods.* ACL 2025. arXiv:2507.21463.
13. H. Ma et al. *CFAD: A Chinese Dataset for Fake Audio Detection.* Speech Communication, 2024. arXiv:2207.12308.
