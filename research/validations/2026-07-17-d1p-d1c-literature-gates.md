# D1-P 與 D1-C commit gates：輕量化下的 selective reliability 與 conformal prior art

日期：2026-07-17  
模式：Validate + Compare  
狀態：文獻 gate 已完成到可做暫定選題；不是「無前作」或最終 novelty 證明  
對應 handoff：`2026-07-15-2205-reply-4-candidates`、`2026-07-15-2015-pathA-conformal-commit-gate`

## 1. 問題與裁決

本輪回答兩個問題：

1. **D1-P gate**：DK-CAST 及其 ADD knowledge-distillation／lightweight lineage，是否已評估壓縮後的 calibration、AURC、error ranking、risk–coverage 或 source-fixed abstention-threshold transfer？
2. **D1-C P1/P2 gate**：conformal prediction／conformal risk control 是否已直接用於 audio deepfake detection（ADD）；相鄰的 shift-aware、group-aware、selective conformal 方法是否已占據方法貢獻？

### Bottom line

- **D1-P：KEEP，但必須再縮窄。** 在本輪檢查的 ADD 輕量化全文中，沒有找到聯合評估「模型變小後，selective risk 與固定拒答門檻能否轉移到未知生成器」的直接前作。可是 2026 年已有 ADD 瀏覽器外掛，DK-CAST 也已宣稱 distillation 保留 confidence；因此不能主張「第一個輕量／edge／大眾外掛」或「第一個保留 confidence」。可守的 residual gap 是 **lightweight transformation 是否保留可操作的 selective reliability，以及如何在相同資源預算下修復它**。
- **D1-C P1：在本輪搜尋範圍內，未找到直接的學術 ADD conformal-selective paper。** 這是 `no inspected hit`，不是證明文獻不存在。
- **D1-C P2：generic 方法空間已有強碰撞。** Selective Conformal Risk Control、SCoRE，以及 covariate-shift conformal 已處理 selective risk、一般 bounded loss 或帶假設的 shift。若只把它套到 ADD，很可能是 domain application；若宣稱 source-only 對任意未知生成器仍 distribution-free，則主張不可守。D1-C 應降為 baseline／敏感度分析，不作目前的主論文貢獻。
- **綜合排序維持 Claude 的裁決：D1-P > D1-C > D1-M > D1-G。** 作者已明確說明目標是更容易部署、讓一般人較可使用，因此 Claude 所指出的「deployment intent 尚未確定」也已解除。

## 2. 搜尋方法與限制

搜尋日：2026-07-17。

### D1-P 範圍

- 從 [DK-CAST 正式全文](https://doi.org/10.1007/s10791-025-09746-4) 往後檢查引用與同題關鍵字，並往前檢查其 ADD KD／lightweight references。
- 全文或官方紀錄中特別檢索：`calibration`、`AURC`、`risk-coverage`、`selective`、`abstain`、`error ranking`、`confidence`、`fixed threshold`。
- 另檢索 2024–2026 ADD compression、KD、truncation、quantization、edge/browser deployment。

### D1-C 範圍

- 組合檢索 `conformal prediction`／`conformal risk control` 與 `audio deepfake`／`speech anti-spoofing`／`synthetic speech detection`。
- 相鄰範圍包括 selective conformal、general-risk control、covariate shift、unknown shift、group/subpopulation shift，以及 speech applications。

### 限制

- DK-CAST 於 2025-10-23 出版，resolved citation-forward 網路仍短；搜尋不到前向引用不能當作沒有前作。
- 部分 IEEE 頁面只能核對官方摘要／metadata；因此下表的否定措辭一律是「未在所檢查的全文或官方紀錄看見」，不是全稱否定。
- 2026 文獻仍快速增加；送出論文前必須更新一次 search log。

## 3. D1-P：DK-CAST full-text citation-forward gate

### 3.1 DK-CAST 實際做了什麼

[DK-CAST](https://doi.org/10.1007/s10791-025-09746-4) 是 Discover Computing 2025 已出版論文。它以 XLS-R teacher、compact audio-selective-transformer student、logit／embedding／phoneme distillation、codec-aware loss、MMD 與 center loss，處理 codec degradation 與輕量部署。

**Verified：**

- 報告 Accuracy、F1、Precision、Recall、EER 與 min t-DCF；hyperparameter 以 development EER 選擇。
- 報告 12.8M parameters、2.1 GFLOPs、desktop/mobile latency 與約 50 MB model size。
- loss 文字確實談到 teacher `confidence/uncertainty`、codec classifier confidence，以及 classification confidence preservation。
- 但全文沒有 AURC、risk–coverage、abstention、fixed abstention threshold transfer 或 calibration evaluation；score-distribution 圖也只顯示分離程度，沒有驗證機率校準或拒答後風險。

**Implication：** D1-P 不能說 DK-CAST 完全不碰 confidence；我們必須把 `confidence imitation` 與 `selective reliability verified under external transfer` 分開。前者已有，後者在本輪未見。

### 3.2 直接與相鄰 closest work

| Work | 已做內容 | 所見 metrics／protocol | 對 D1-P 的影響 |
|---|---|---|---|
| [DK-CAST, Discover Computing 2025](https://doi.org/10.1007/s10791-025-09746-4) | codec-aware tri-stream KD、compact student、resource evaluation | Accuracy/F1/EER/min t-DCF；loss 文字含 confidence | 直接占據 codec-aware lightweight KD；未見 selective-risk／fixed-threshold transfer |
| [FTDKD, IEEE/ACM TASLP 2024](https://doi.org/10.1109/TASLP.2024.3492796) | low-quality compressed ADD 的 frequency/time-domain KD | EER、min t-DCF | 占據 compressed-audio KD；未見 selective protocol |
| [One-Class KD, ICASSP 2024](https://arxiv.org/abs/2309.08285) | one-class objective + KD，改善 unseen attacks | 主要為 EER | 占據「KD + generalization」，未見 threshold-transfer evaluation |
| [DOC-KD, IEEE TMM 2024](https://doi.org/10.1109/TMM.2023.3321505) | lightweight one-class learning + KD | EER/minDCF 類 performance | 「lightweight + KD」不是新穎點 |
| [Frequency-mix KD, 2024 preprint](https://arxiv.org/abs/2406.09664) | frequency-mix knowledge distillation | EER/min t-DCF | 未見 selective/calibration protocol |
| [RawTFNet, 2025 preprint](https://arxiv.org/abs/2507.08227) | lightweight ADD architecture | EER／效率 | 小模型本身已擁擠 |
| [Lightweight Resolution-Aware ADD, 2026 preprint](https://arxiv.org/abs/2601.06560) | 159K parameters、低 GFLOPs | Accuracy/AUC/EER | 極小模型也不是 residual gap |
| [Detecting Audio Deepfakes on the Edge, 2026 preprint](https://arxiv.org/abs/2606.30780) | truncated XLS-R + logistic classifier、六個 OOD datasets、Chrome plugin | EER、latency、memory、parameters；binary output | 直接殺死「首個 browser/on-device/public detector」；全文未見 calibration/AURC/abstention/risk–coverage |
| [DeFakeQ, 2026 preprint](https://arxiv.org/abs/2604.08847) | edge deepfake quantization | 視覺 deepfake datasets；accuracy／efficiency | 是相鄰而非 ADD；禁止宣稱「first deepfake quantization」，但不直接填補 audio selective gap |

2026 browser-plugin paper 特別重要：它以 ASVspoof 2019 訓練、六個 OOD dataset 評估，layer 7 的 mean OOD EER 為 8.4%，並以約 101M parameters、單 CPU、瀏覽器內推論呈現部署價值。作者明確把 EER 稱為 threshold-free metric，外掛仍直接回傳 bona fide／spoof。全文未出現 `calibration`、`AURC`、`abstention`、`risk` 或 `coverage` 的方法或評估。

### 3.3 D1-P 可守與不可守的 novelty

**不可守：**

- 第一個 lightweight、on-device、privacy-preserving 或 browser ADD detector；
- 第一個用 KD／truncation／codec-aware loss 做 ADD；
- 第一個在 distillation 中傳遞 confidence；
- 第一個外部測試 lightweight ADD generalization。

**目前可作為待驗證 residual gap：**

> 現有 ADD 輕量化工作主要用 EER、AUC、accuracy、latency 與 memory 證明模型「仍能分」，但沒有驗證 source development 上凍結的分類／拒答規則，在 lightweight transformation 後是否仍能讓模型「知道何時不該判斷」，尤其是在真正未見 generator family 上。

這是 **Inference（中等信心）**，不是 first claim。它把兩條已有文獻線接成一個可否證問題：Pascu-style calibrated/rejection-aware frozen SSL 與 DK-CAST/browser-style lightweight ADD。

## 4. D1-C：P1/P2 conformal gate

### 4.1 P1：conformal 是否已直接進入 ADD？

**Result：No inspected direct academic hit（搜尋範圍內）。**

本輪沒有找到把 conformal prediction 或 conformal risk control 直接用在 ADD／speech anti-spoofing 的學術全文，並以 selective risk、abstention 或 unseen-generator transfer 為主要問題的工作。搜尋中有商業網站聲稱使用 conformal，但沒有足夠可驗證方法，不能視為 closest academic work。

**Interpretation：** 應用交集可能仍空，但「把 generic conformal 套到 ADD」最多先視為 domain application novelty，不能自動成為方法 novelty。

### 4.2 P2：相鄰 shift-aware／selective conformal 是否已占據方法空間？

| Work | 能保證什麼 | 關鍵假設／限制 | Collision |
|---|---|---|---|
| [Selective Conformal Risk Control, 2025/2026 preprint](https://arxiv.org/abs/2512.12844) | selective classification 下的 exact/PAC risk guarantees | exchangeability 等明示條件 | 直接占據 generic selective + conformal risk control |
| [SCoRE: Conformal Selective Prediction with General Risk Control, 2026 preprint](https://arxiv.org/abs/2603.24704) | arbitrary bounded risk 的 selective trust decisions；含 shift extensions | exchangeability；covariate shift 需 weights／doubly robust assumptions | 幾乎占據 generic「selective conformal general risk」方法敘事 |
| [Conformal Prediction Under Covariate Shift, NeurIPS 2019](https://proceedings.neurips.cc/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html) | covariate shift 下的 weighted conformal coverage | known／estimable likelihood ratio，常需 target covariates | shift robustness 並非無條件 |
| [Conformal prediction beyond exchangeability, AoS 2023](https://doi.org/10.1214/23-AOS2276) | nonexchangeable data 的 weighted guarantees／degradation characterization | 需設計 weights 或描述 departure | 不能推導 arbitrary unseen-generator source-only guarantee |
| [Audited Conformal Prediction under Unknown Distribution Shift, 2026 preprint](https://arxiv.org/abs/2606.14909) | unknown shift 下 auditing | 需要少量 labeled target data | 與 source-only 設定不同，但占據「unknown shift certificate」措辭 |
| [Confident and Adaptive Generative Speech Recognition via Risk Control, ICLR 2026](https://iclr.cc/virtual/2026/poster/10008472) | speech ASR 中 adaptive candidate/risk control | 任務是 ASR，不是 ADD/unseen generator | speech domain 也已有 risk-control application |

**Inference：** source data 完全相同時，可以構造兩個目標環境，讓新 generator 上的錯誤方向與風險相反；任何只看 source data 的程序在兩者輸出相同，因此不能同時對任意 target shift 提供非平凡的 sound guarantee。若要保證，必須縮限 shift set、觀察 target covariates／labels，或把輸出降格成 empirical warning。

### 4.3 D1-C verdict

- **作主方法：DEPRIORITIZE／NARROW。** 不使用 `distribution-free under unseen-generator shift` 或 `certificate`。
- **作 D1-P baseline：KEEP。** 在 exchangeable source calibration 上使用標準 conformal／risk-control baseline，並把外部 generator violation 誠實報告為 assumption failure，而不是把它包裝成保證。
- 只有在日後能提出可觀察、可檢驗、非 target-label-dependent 的 ADD-specific bounded-shift model，且超出 SCRC/SCoRE，才重新考慮 D1-C 為主題。

## 5. 兩案整合後的 thesis gate

### 推薦主軸

暫定題目：

> **未知生成器下輕量音訊深偽偵測器的選擇性可靠性與保留方法**  
> *Selective Reliability of Lightweight Audio Deepfake Detectors under Unseen Generators*

### H1-before-H2

1. **H1 audit（先做、便宜、可殺題）**：比較 full calibrated teacher 與一組 truncation／ordinary KD students；在 discrimination-matched 條件下，檢查 eAURC、error ranking、generator-macro confident-real leakage 與 source-fixed threshold violation。
2. **H2 method（只有 H1 成立才做）**：在相同 student architecture、資料與 latency 下，加入 selective-reliability-aware distillation／selection loss，測試能否修復上述退化。

`discrimination-matched` 是必要條件：若 student 只是整體 detector 變差，就不能把 selective-risk 變差解讀為獨立的 reliability failure。

### Kill / pivot

- 若 ordinary truncation 與 ordinary KD 在 matched discrimination 下都完整保留 selective behavior，**KILL H2**；不要為了做新 loss 製造問題。
- 若 teacher 在外部 holdout 接近隨機，**KILL compression interpretation**；那是 base detector generalization failure。
- 若 H1 成立但 H2 無增益，可考慮 measurement／evaluation thesis；是否足夠必須讓 advisor 判斷，不能預設負結果必然足以畢業。
- confirmatory holdout 若不能證明 generator-family disjoint，或差異可由 dataset shortcut 解釋，維持 pilot 暫停。

## 6. 下一個最小驗證步驟

在不開始 full pilot 的前提下，先做一個 **score-only H1 feasibility audit specification**：

- 一個 frozen SSL teacher；
- 一個可重現的 truncation family 作低成本 probe，ordinary KD 最多再一個；
- source dev 同時凍結 classification threshold `t` 與 abstention threshold `q`；
- 一個 lineage-audited unseen-generator holdout；
- primary risk：generator-macro confident-real leakage at fixed/matched coverage；
- secondary：eAURC、error-AUROC、Brier/NLL、AUROC/EER、CPU latency、RAM、model size；
- 禁止用 holdout 挑 layer、threshold、temperature 或 preprocessing。

送給學長的提案可以現在先送，但應標示為「暫定題目；H1 與 lineage gate 通過後才正式 commit」。

## 7. 未解問題

- 2026 browser-plugin code 與各 layer scores 是否足以直接重現 calibration／selective audit；
- teacher/student checkpoint、license、實際 CPU target 與可接受 latency；
- DFADD／ASVspoof 5 子集的 generator lineage、訓練資料與 vocoder overlap；
- primary stakeholder 最終是一般使用者、記者／查核者，或小型組織；三者的 review capacity 不同；
- H1 若只在一個 dataset 成立，是否為 generator effect 或 dataset shortcut。

