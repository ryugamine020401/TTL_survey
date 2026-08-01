# 壓縮與 selective reliability 的前作定位：Q1–Q3 全文查證

日期：2026-07-18  
模式：Validate  
對應 handoff：`2026-07-18-0010-priorart-positioning-search`  
決策用途：判定 narrowed D1-P 的 H2 是否仍可主張方法貢獻，並回填四層 novelty 表

## 1. Inquiry

### 問題

1. **Q1（現象）**：壓縮是否會在 accuracy／AUROC 大致不變時，破壞 calibration、uncertainty、OOD detection 或 selective prediction？
2. **Q2（方法；H2 生死線）**：是否已有保留或修復 calibration／uncertainty／selective reliability 的壓縮或蒸餾方法？
3. **Q3（指標）**：是否已有用 selective risk、risk–coverage、AURC 或固定門檻失效來評估壓縮／蒸餾，而非只看 accuracy、EER 與 latency？

### 單位、威脅模型與 contribution 判準

- 單位是 **full／teacher 與 lightweight／student detector pair**，不是只比較兩個任意架構。
- 目標威脅模型是 source generator 上訓練及凍結決策規則，部署到 **lineage-disjoint unseen generator family**；target holdout 不得用於選 layer、temperature、`q`、`t` 或 preprocessing。
- 只有「通用 calibration-aware KD」以外、且針對 **external selective-policy transfer** 的非平凡機制，才可能是 H2 方法 novelty；把既有方法直接套到 ADD，先視為 application novelty。
- 本輪不重新查 DK-CAST、FTDKD、DOC-KD、Pascu／FADEL 或 2026 edge/browser ADD；其已核實結果沿用 `2026-07-17-d1p-d1c-literature-gates.md`。

## 2. Bottom line

| 問題 | 裁決 | 信心 | 對 D1-P／H2 的直接影響 |
|---|---|---:|---|
| **Q1** | **Partially：現象已在若干壓縮設定出現，但不是跨壓縮法的既定定律。** | 中高 | 不能宣稱普遍「壓縮必然傷可靠性」；可把它寫成 ADD 中待檢驗、可被否證的 H1。量化 LLM 有支持證據，pruning 與量化 BNN 有反證。 |
| **Q2** | **Verified-known：廣義方法已存在；因此 broad H2 method novelty = Refuted。** | 高 | `calibrated outputs distillation`、`uncertainty matching/distillation`、`calibration-aware compression` 都不是新方法類別。H2 若存活，只能是 ADD-specific、針對 unseen-generator external selective-risk transfer，且必須勝過既有 calibration/uncertainty transfer baseline。 |
| **Q3** | **Partially：AURC／risk–coverage 評估 KD 已知；matched discrimination + source-fixed external threshold transfer 未見直接命中。** | 高（前半）／中（後半） | 不能把 AURC、eAURC 或 risk–coverage 稱為本研究提出。可保留的小型 measurement contribution 是：資源與 discrimination matched、source-fixed `(q,t)`、lineage-disjoint target、generator-macro asymmetric leakage。 |

**總結判定：** H2 沒有被整體殺死，但其主張必須由「提出 reliability-aware distillation」縮成：

> 在 ADD 的未見生成器外部轉移下，既有 lightweight transformation 與 calibration／uncertainty-transfer 方法能否保住 source-frozen selective policy；若不能，一個針對 generator-group transfer 的方法能否在相同 discrimination 與部署預算下，降低 generator-macro confident-real leakage？

這仍是 **Open-in-search-scope**，不是 verified gap。若 H2 只是 teacher soft targets、temperature、ECE loss、uncertainty vector matching、AURC reporting 或 source-dev recalibration 的組合，方法 novelty 不成立。

## 3. 搜尋方法與範圍

搜尋日：2026-07-17 至 2026-07-18（Asia/Taipei）。

### 系統與來源

- 一般網頁／學術檢索，用於發現候選與 citation chaining；
- 全文與出版狀態優先核對：CVF Open Access、PMLR、NeurIPS proceedings、ACL Anthology、ISCA Archive、OpenReview／arXiv 作者稿、出版社 DOI 紀錄；
- 最終技術判定只依檢查過的論文全文或官方 proceedings 頁，不以搜尋摘要作為唯一證據。

### Query families

- `(compression OR pruning OR quantization OR knowledge distillation) AND (calibration OR uncertainty OR OOD OR selective prediction)`
- `(calibration-preserving OR uncertainty-preserving OR calibration transfer OR uncertainty matching) AND (distillation OR compression)`
- `(risk-coverage OR AURC OR selective risk OR abstention) AND (distillation OR pruning OR quantization)`
- 上述詞族再分別加入 `speech`、`audio`、`ASR`、`speaker verification`、`acoustic event detection`、`audio deepfake`、`anti-spoofing`
- 精確殘餘檢索：`matched accuracy/AUROC`、`fixed threshold`、`threshold transfer`、`external calibration transfer` 與 compression/KD 的組合

### 邊界與限制

- 主要涵蓋 2018–2026 的 classification、vision、NLP/LLM、audio/speech；較早的 Bayesian dark knowledge 只作 lineage lead，未納入核心裁決。
- 未取得 Scopus／Web of Science 的完整索引匯出，也未做付費資料庫的系統性 review；因此所有否定結果均為 `no inspected hit`。
- `matched discrimination` 在前作中常只代表同表比較或相近 accuracy，少有統計 equivalence test；本輪沒有把「數字看似接近」提升為嚴格 matched claim。
- 2026 文獻仍快速增加；投稿前需重跑 exact-intersection 與 citation-forward search。

## 4. Q1：壓縮在辨識力近似維持時是否傷可靠性？

### 4.1 支持證據

| Work | 全文所見 | 證據狀態 | 能支持到哪裡 |
|---|---|---|---|
| [Zhong et al., *Quantized Can Still Be Calibrated*, ACL 2025](https://aclanthology.org/2025.acl-long.1473/) | 比較 7B 級 full-precision 與 4-bit BNB/GPTQ LLM；作者指出量化模型通常維持可比 accuracy，但 48 個 calibration-error 比較中 41 個（85%）較差，並提出 soft-prompt post-calibration 修復。 | **Verified** | 最接近 Q1 的已出版支持：quantization 可在任務能力大致保留時造成 calibration gap。但任務是生成式 multiple-choice QA，未做 AUROC-matched 或 selective policy transfer。 |
| [DistilDoc, ICDAR 2024](https://arxiv.org/pdf/2406.08226)（正式 DOI `10.1007/978-3-031-70546-5_12`） | 對 base→small/tiny KD 同時報 ACC、ECE、AURC；相近 ACC 的 KD 方法可有不同 AURC/ECE，且 covariate-shift RVL-CDIP-N 上 KD 的 ranking 與 ID 不一致。 | **Verified** | 證明壓縮後 accuracy 不能替代 confidence ranking／calibration 評估，並直接把 AURC 放進 KD benchmark；不證明壓縮必然使 reliability 變差。 |
| [Wang & Zhang, *Calibration Bottleneck*, ICML 2024](https://proceedings.mlr.press/v235/wang24cm.html) | 顯示頂層 representation 過度壓縮會降低可校準性。 | **Verified-adjacent** | 提供 representation-compression 的機制性動機，但不是 pruning／quantization／small-student 的直接比較，不能單獨回答 Q1。 |

### 4.2 反證與邊界

| Work | 全文所見 | 證據狀態 | 對 H1 的約束 |
|---|---|---|---|
| [Mitra et al., CVPRW 2024](https://openaccess.thecvf.com/content/CVPR2024W/SAIAD/papers/Mitra_Investigating_Calibration_and_Corruption_Robustness_of_Post-hoc_Pruned_Perception_CNNs_CVPRW_2024_paper.pdf) | 三類 post-hoc pruning、CIFAR-10、多個 CNN；在 accuracy 尚保持的範圍，ECE 多為相近或更低，natural corruption 下也未見 pruning 額外傷 calibration。 | **Verified contradiction** | 直接否定「pruning 普遍傷 calibration」。結果限於單資料集、ECE、特定 pruning 與 corruption，不排除 ADD external transfer 失效。 |
| [Krishnamoorthi et al., *Quantization of Bayesian Neural Networks...*, UDL workshop 2021](https://www.gatsby.ucl.ac.uk/~balaji/udl2021/accepted-papers/UDL2021-paper-039.pdf) | CIFAR-10 BNN FP32→INT8：accuracy 91.00→90.87，ECE 1.523→2.001；作者基於多指標與 corruption 實驗判定無顯著 accuracy 或 uncertainty-quality degradation，最高 7.1× size reduction。 | **Verified contradiction（低出版層級）** | 量化是否傷 uncertainty 取決於模型家族與表示；單一小數差不能當可靠性損害證明。 |
| [Cui et al., BN3, CVPR 2021](https://openaccess.thecvf.com/content/CVPR2021/papers/Cui_Bayesian_Nested_Neural_Networks_for_Uncertainty_Calibration_and_Adaptive_Compression_CVPR_2021_paper.pdf) | 共同學習可調寬度 subnet 與 Bayesian uncertainty；以 accuracy、ECE、OOD AUPR 評估，在各寬度優於 deterministic nested net。 | **Verified boundary** | 壓縮與可靠性可以共同優化；因此 H1 必須是 empirical gate，不能被寫成先驗事實。 |

### 4.3 Q1 verdict

**Partially（中高信心）。** 已知的是「accuracy／task performance 不足以推知壓縮後 calibration 或 confidence ranking」，以及部分量化設定確有 calibration gap；未知且被反證約束的是「壓縮本身會普遍傷可靠性」。

因此 D1-P 的現象主張應寫成 **Hypothesis**：

> H1：對至少一種可重現的 ADD lightweight transformation，在 lineage-disjoint unseen-generator holdout 上，即使 AUROC/EER 與部署預算 matched，source-fixed selective policy 的 generator-macro confident-real leakage 仍顯著高於 full model。

不能寫成「我們把一般領域已確立的定律首次搬到 ADD」；較準確的是「前作顯示結果依壓縮法與模型而異，ADD 的特定外部轉移尚待測量」。

## 5. Q2：保住可靠性的壓縮／蒸餾方法是否已存在？

### 5.1 直接碰撞

| Work | 方法與評估 | Publication status | Collision with H2 |
|---|---|---|---|
| [Hebbalaguppe et al., *Calibration Transfer via Knowledge Distillation*, ACCV 2024](https://openaccess.thecvf.com/content/ACCV2024/papers/Hebbalaguppe_Calibration_Transfer_via_Knowledge_Distillation_ACCV_2024_paper.pdf) | 先以 adaptive/dynamic calibration 訓練 teacher，再以 KD(C) 產生較小 WRN/MobileNet／DistilBERT student；同報 Top-1、ECE/SCE/ACE，展示 accuracy 近似時 calibration 可大幅改善。 | **Published conference paper** | 直接占據 `calibrated-teacher → calibrated compact student`。H2 不能只是蒸餾 calibrated logits 或調 temperature。 |
| [Mishra et al., *Distilling Calibrated Student from an Uncalibrated Teacher*, 2023](https://arxiv.org/pdf/2302.11472) | 將 Cutout/Mixup/CutMix 與 KD 結合；VGG/ResNet teacher 到 MobileNet/VGG student，在 CIFAR/CINIC/TinyImageNet 報 accuracy、ECE、OE，並在 CIFAR-100C 測 corruption。 | **Preprint；後續版本有 IEEE TAI DOI `10.1109/TAI.2025.3605902`** | 直接占據 `uncalibrated teacher → calibrated student without accuracy sacrifice`；資料增強 + KD 不是 H2 新機制。 |
| [Zhong et al., ACL 2025](https://aclanthology.org/2025.acl-long.1473/) | 對 quantized LLM 用 soft-prompt tuning 最小化 calibration upper bound，修復量化造成的 gap。 | **Published long paper** | 占據 calibration-aware post-compression repair；H2 必須與 source-dev post-calibration 明確比較。 |
| [Cui et al., BN3, CVPR 2021](https://openaccess.thecvf.com/content/CVPR2021/papers/Cui_Bayesian_Nested_Neural_Networks_for_Uncertainty_Calibration_and_Adaptive_Compression_CVPR_2021_paper.pdf) | 以 variational nested dropout 共同產生 uncertainty-calibrated subnets，測 accuracy、ECE、OOD AUPR。 | **Published conference paper** | 占據 joint adaptive compression + uncertainty/OOD quality；即使不是 KD，也排除「首個考慮可靠性的壓縮方法」。 |
| [Ryabinin et al., *Scaling Ensemble Distribution Distillation...*, NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/2f4ccb0f7a84f335affb418aee08a6df-Abstract.html) | 把 ensemble predictive distribution 蒸餾成單模型，保留 total/knowledge uncertainty；ImageNet 與 LibriSpeech 上測 calibration/OOD ROC-AUC。ASR 的 knowledge uncertainty 未完整追上 ensemble，作者保留負結果。 | **Published conference paper** | 直接占據 uncertainty-preserving ensemble compression，且已有 speech/OOD 實驗；「蒸餾 uncertainty」本身不新。 |
| [Kim et al., *Multi-Domain KD via Uncertainty-Matching for E2E ASR*, Interspeech 2021](https://www.isca-archive.org/interspeech_2021/kim21g_interspeech.html) | teacher/student 額外輸出 token-level aleatoric variance，以 normalized MSE 蒸餾 uncertainty；WSJ small/tiny students 只以 WER 驗證，未測 calibration、OOD 或 selective risk。 | **Published conference paper** | 音訊／speech 中已明確有 `uncertainty-matching KD for limited-capacity students`。這是 H2 必須引用的最近機制碰撞，但其 evaluation 沒驗證 uncertainty 是否真的被保留。 |
| [Guo et al., RepL4NLP 2021](https://aclanthology.org/2021.repl4nlp-1.29/) | 把 KD 視為 student uncertainty matching，設計無額外 inference cost 的 recalibration，測 GLUE ID/OOD calibration。 | **Published workshop paper** | 占據 calibration transfer under OOD 的一般敘事；雖然主要是同規模模型，不足以單獨回答 compression。 |

另有 [Malinin et al., Ensemble Distribution Distillation, ICLR 2020](https://openreview.net/forum?id=BygSP6Vtvr) 與 [Gurau et al., Dropout Distillation, 2018 preprint](https://arxiv.org/abs/1809.10562) 形成更早的 uncertainty-distillation lineage。後者明言 student 與 teacher 同架構，壓縮的是 MC-dropout 的多次推論成本而非參數量。

### 5.2 Q2 verdict 與 H2 生死線

**「是否已有方法？」= Verified-known（高信心）。**  
**「H2 作為廣義 reliability-aware compression/KD 是否新？」= Refuted。**

H2 只有以下 residual 可能存活：

1. **對象特定**：ADD binary/asymmetric harm，主要風險是 fake 被高信心放成 real，而非一般 top-1 ECE。
2. **轉移特定**：不是 ID calibration，而是 source-frozen `(q,t)` 到 lineage-disjoint unseen generator 的 external selective-policy transfer。
3. **比較特定**：在相同 student architecture、資料、CPU/RAM/latency 與 AUROC/EER 容忍區間內，勝過 ordinary KD、ordinary KD + source-dev recalibration，以及至少一個 calibration/uncertainty-transfer baseline。
4. **機制特定**：loss 需明確針對 generator-group transfer 的 error ranking／asymmetric leakage，而非重命名 ECE、teacher entropy 或 soft-target KL。

若做不到第 4 點，H2 應降為 **ADD application + evaluation contribution**；這仍可能是有用碩論，但不能以新通用蒸餾方法定位。

## 6. Q3：selective-risk 比較軸是否已有前作？

### 6.1 已知部分

| Work | 已用的比較軸 | 與本提案的差異 |
|---|---|---|
| [Gurau et al., Dropout Distillation, 2018](https://www.robots.ox.ac.uk/~mobile/Papers/wip_gurau_ddn.pdf) | 對 distilled single-pass model 畫 risk–coverage curve，以 confidence threshold sweep 比較 baseline、MC-10/100、DDN。 | 同架構、ID CIFAR-10；不是小參數 student，不做 discrimination matching 或 source→target threshold transfer。 |
| [Niu et al., *Respecting Transfer Gap in KD*, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/file/89b0e466b46292ce0bfe53618aadd3de-Abstract-Conference.html) | KD／self-distillation 同報 Top-1/Top-5、ECE、AURC；IPWD 在多架構降低 AURC。 | AURC 已是 KD evaluation 先例；主實驗是 ID classification，未凍結 source threshold 到外部 shift。 |
| [DistilDoc, ICDAR 2024](https://arxiv.org/pdf/2406.08226) | 小型 KD students 同報 ACC、ECE、AURC，另在 covariate-shift RVL-CDIP-N 評估。 | 是最接近「compressed student + AURC + shift」的前作；仍以 target set 上的 AURC 評估，沒有 source-fixed operating point 或 matched-discrimination protocol。 |
| [Xu et al., *KD with a Precise Teacher and Prediction with Abstention*, ICPR 2020](https://doi.org/10.1109/ICPR48806.2021.9412696) | 論文題目與方法直接把 KD 與 abstention／risk–coverage 連結。 | 進一步排除「首個把 KD 與拒答放在一起」；本輪可取得 proceedings metadata／簡報，未取得可全文重現所有設定的作者 PDF，因此不把它作唯一裁決依據。 |

因此以下主張都 **不可守**：

- 第一個用 risk–coverage／AURC 評估 knowledge distillation；
- 第一個把 KD 與 abstention 放在一起；
- 第一個同時報 accuracy 和 calibration／selective metric 的 compact student。

### 6.2 仍未見直接命中的 protocol

在本輪全文與 exact-query 範圍內，未見一篇工作同時做到：

1. teacher/student 的部署預算 matched；
2. AUROC/EER 以預先定義 tolerance 或 equivalence test 做 discrimination matched；
3. `q`（abstention）和 `t`（class decision）只由 source dev 決定並凍結；
4. 在 lineage-disjoint external target 不重調 score scale 或 threshold；
5. 報 generator-macro 的 **confident-real leakage** 與 fixed-policy violation。

這是 **Open-in-search-scope（中信心）**，屬 evaluation/deployment gap，不是新 selective metric。

### 6.3 指標設計修正

`08-positioning-and-comparison-metric.md` 寫「同 AUROC / eAURC（排序能力）」需要修正：

- **不能把 eAURC 同時當 matching variable 與主要 outcome。** 這會把要比較的 selective reliability 先行配平，形成 circular comparison。
- 建議 matching 只用：model/latency/RAM budget + AUROC（或 EER）equivalence tolerance；eAURC/error-AUROC 留作 secondary selective-ranking outcome。
- risk–coverage/AURC 是 **target score sweep**；它回答 ranking quality，但不回答 source threshold 是否可部署轉移。
- source-fixed `(q,t)` leakage 是 **operating-point transfer**；它是本題的主要 outcome。兩者必須分開報告。
- ECE/Brier/NLL 衡量 probability quality，不能替代 error ranking；temperature scaling可改善 ECE但通常不改 score ranking，因此必须把 `ordinary KD + source-dev recalibration` 保留為致命 baseline。

## 7. 回填四層 novelty 表

| 層 | 我們的主張 | 前作狀態（本輪回填） | 最接近前作 | 誠實 novelty 定位 |
|---|---|---|---|---|
| **現象層**：壓縮在辨識力近似不變時仍破壞 uncertainty/calibration/selective behavior | 在 ADD 觀察到 | **Partially**：量化 LLM 有直接支持；DistilDoc 顯示 ACC 與 AURC/ECE 可脫鉤；但 pruning 與 quantized BNN 有無傷甚至改善的反證。 | Zhong ACL 2025；DistilDoc ICDAR 2024；反證 Mitra CVPRW 2024、QBNN workshop 2021 | **不主張通用新現象。** 可主張在 ADD unseen-generator external policy transfer 的預註冊 measurement。 |
| **設定層**：輕量／edge ADD | 壓縮 ADD detector | **Verified-known** | DK-CAST、FTDKD、DOC-KD、One-Class KD、2026 edge/browser ADD（沿用先前 gate） | **不在此層。** |
| **可靠性層**：ADD selective reliability | 衡量拒答與 reliability | **Verified-known（泛稱）** | Pascu／FADEL full-model reliability；先前 gate 已核對 | **不在「ADD reliability」泛稱。** |
| **交集 + 方法層**：lightweight ADD × unseen-generator external selective-policy transfer × preservation method | H2 核心 | **Partially**：generic calibrated/uncertainty-preserving compression 已知，speech uncertainty-matching KD 也已知；但 exact ADD + lineage-disjoint + source-fixed `(q,t)` + generator-macro leakage 未見直接命中。 | KD(C) ACCV 2024；BN3 CVPR 2021；EnD² NeurIPS 2021；Kim Interspeech 2021；Q3 的 Niu/DistilDoc | **只在窄交集可能成立。** 若方法只是既有 KD(C)/uncertainty matching 的 ADD 套用，降為 application novelty；若提出並驗證 external selective-risk transfer 的 ADD-specific 機制，才可能保留方法貢獻。 |

一句可守的 positioning：

> Prior work has shown that compression can alter calibration in some settings, has developed calibration- and uncertainty-aware distillation methods, and has evaluated distilled models with AURC. Within our documented search scope, however, we found no work that tests whether a source-frozen abstention/classification policy survives lightweight audio-deepfake transformation on lineage-disjoint unseen generators, or develops an ADD-specific method for that external selective-risk transfer.

## 8. Red-team findings

1. **H2 最大碰撞不是 ADD KD，而是 generic calibration/uncertainty transfer。** 不加入 KD(C)、uncertainty matching 或等價 baseline，reviewer 可合理認定重造輪子。
2. **H1 不是已知真理。** pruning/BNN 反證表示 H1 很可能依 transformation、score head、teacher calibration 與 shift 而變；兩週 gate 必須允許完整否證。
3. **AURC 不新，也不等於 threshold transfer。** 若論文只報 eAURC 優勢，measurement novelty 仍不足。
4. **匹配設計可能 circular。** 不能 match eAURC 再宣稱 selective-risk 改善；AUROC/EER matching 也需預先定 tolerance，不能事後挑 checkpoint/layer。
5. **方法可能只學 source calibration。** source 上改善 ECE/AURC 不保證 unseen generator 的 ordering 或 threshold scale；若 H2 不優於 source-dev recalibration，應殺死「新 loss 必要性」。
6. **跨 generator 的 group surrogate 可能洩漏 threat model。** 若用 leave-one-generator-out 設計 loss，confirmatory target 必須是訓練與 meta-validation 都未見的 lineage，且 generator labels 的可用性要符合部署主張。

## 9. Validation contract

### 下一個最小步驟

在不解除 pilot 暫停的前提下，把 H1/H2 protocol 增補以下 preregistration 條款：

1. 只以 deployment budget + AUROC/EER tolerance 做 matching；eAURC 不作 matching variable。
2. H1 primary：source-fixed `(q,t)` 的 generator-macro confident-real leakage；secondary：eAURC、error-AUROC、Brier/NLL/ECE、AUROC/EER。
3. H2 最低 baselines：ordinary KD；ordinary KD + source-dev temperature/vector recalibration；calibrated-teacher KD（KD(C)-style）；若輸出結構可行，再加 uncertainty-target matching。所有 baseline 使用同 student、資料與 tuning budget。
4. H2 method 在 H1 通過後才定義；禁止用 confirmatory unseen-generator holdout 選 loss 或超參數。

### Success signal

- H1：至少一個預先指定 transformation 在 discrimination equivalence 成立時，external fixed-policy leakage 有穩健、跨 generator 的惡化，而非單一 dataset artifact。
- H2：在相同預算、同 AUROC/EER tolerance 下，對至少兩個 lineage-disjoint generator groups 同時勝過 `ordinary KD + recalibration` 與 calibrated/uncertainty-transfer baseline；改善主要出現在 fixed-policy leakage，而非只在 ECE。

### Kill／narrow condition

- matched discrimination 後沒有 H1 degradation：**kill H2**。
- degradation 由 teacher 本身在 target 失效或 dataset shortcut 解釋：**kill compression interpretation**。
- KD(C)／uncertainty matching／recalibration 已達同等結果：**kill new-method claim**，保留 replication/evaluation thesis。
- 只有 target-tuned threshold 才改善：**kill external-transfer claim**。

### Pivot

若 broad H2 被 baseline 吃掉，轉為：

> 一個可重現的 ADD compression reliability benchmark，系統比較 ordinary KD、calibration transfer、uncertainty matching 與 post-hoc recalibration 在 source-fixed policy 下的失效邊界。

有力負結果是：不同 compression families 並不一致地傷 reliability，且哪種 source-only repair 能／不能跨 generator 轉移；但是否足以作碩論主貢獻仍需 advisor 明確判斷。

## 10. Project-state impact

- 依 handoff authority boundary，**未修改** `PROJECT.md`、`TASKS.md`、`DECISIONS.md`，也未解除 pilot 暫停。
- `TASKS.md` 現有「H1 先於 H2」方向不需改；若作者／advisor 接受本輪定位，下一次可把 H2 baseline 明確加入 KD(C)-style 與 uncertainty-matching，但本輪不越權更新。
- `DECISIONS.md` 不應變更：本輪縮窄 novelty，未選定最終 thesis direction。

