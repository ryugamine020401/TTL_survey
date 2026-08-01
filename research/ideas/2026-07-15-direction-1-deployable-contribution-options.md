# 方向 #1 的可部署方法貢獻：給 Claude 的比較與審查提案

日期：2026-07-15  
模式：Explore + Validate + Compare  
狀態：候選提案，尚未定題；pilot 與實作維持暫停

## 1. Inquiry

作者補充的真正目標不是只完成一篇 threshold measurement thesis，而是：

> 更深入理解 audio deepfake detection，讓偵測更容易部署、更能被一般大眾使用，從而降低 deepfake audio 帶來的風險。

本稿要回答：方向 #1 能否在保留 selective prediction／abstention 核心的同時，形成一個比「固定 `(q+t)` 量測」更具方法或系統貢獻、又能在一年內完成的題目？

本稿也把 Claude 已提出的 **D1-C：generator-shift-aware conformal selective risk** 納入同一比較，而不是預設它已勝出。

### Problem contract

- **主要 stakeholder**：需要低成本或離線檢查 voice message 的一般使用者、事實查核者或小型組織。
- **分析與決策單位**：一則完整語音訊息。
- **輸出動作**：`疑似合成 / 無法判定 / 未發現合成證據`；最後一項不得表示「已驗證真人」。
- **核心 threat model**：完整合成語音、未見生成器，加上一種常見 codec/channel；不含 live voice conversion、partial deepfake、自適應白箱攻擊及真人身分驗證。
- **可主張價值**：降低運算與隱私門檻，並降低 fake message 被高信心放行的比例。
- **不主張**：沒有真實使用者或介入研究時，不宣稱已降低詐騙率、受騙率或全社會風險。

## 2. Bottom line

**Inference（信心中等）：方向 #1 並非只能做 measurement。至少有三種可形成方法／系統貢獻的版本，其中目前最貼近作者部署願景的是 D1-P「selective-risk-preserving compression」。**

measurement-only protocol 仍有價值，但應退為診斷與評估骨架。論文的主要 contribution owner 可以改成：

1. 壓縮或量化如何破壞 detector 的 uncertainty ranking 與 threshold transfer；
2. 一個在相同資源預算下盡量保留 selective reliability 的 distillation 方法；
3. 一個誠實三態輸出的離線 reference deployment。

這個結論仍是候選判斷。最重要的 **Unknown** 是：audio deepfake 的 compression／distillation 文獻是否已直接最佳化或評估 AURC、selective risk、calibration 及 source-fixed abstention-threshold transfer。

## 3. Evidence map

| Claim / issue | Evidence | Status | Implication |
|---|---|---|---|
| ADD 的 uncertainty、rejection 與 calibration 不是空白 | [Pascu et al., Interspeech 2024](https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html)；[FADEL, ICASSP 2025](https://doi.org/10.1109/ICASSP49660.2025.10888053) | Verified，已出版 | 新題不能只是在既有 detector 上加 confidence threshold |
| 輕量化、knowledge distillation 與 codec-aware ADD 已存在 | [DK-CAST, Discover Computing 2025](https://doi.org/10.1007/s10791-025-09746-4) | Verified，已出版 | 「做一個小模型」本身不足；必須研究壓縮與 selective reliability 的交互 |
| 隱私友善 ADD 已有直接前作 | [SafeEar, CCS 2024](https://safeearweb.github.io/Project/files/SafeEar_CCS2024.pdf) | Verified，已出版 | 離線／隱私只能支撐 deployment value，不能單獨當 novelty |
| OOD routing 與 explanation 已用於 ADD | [ICLAD, Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.450/) | Verified，已出版 | generic「不確定就轉第二模型」已擁擠；低成本 guardrail 必須與昂貴 ALM routing 區分 |
| 泛化與新攻擊適應已有 meta/continual 路線 | [RWM, AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29929)；[ALDEN, ACM MM 2025](https://doi.org/10.1145/3746027.3754741) | Verified，已出版 | source pseudo-shift 方法須把貢獻限定為 selective-risk transfer，而非泛稱 generalization |
| ADD compression 是否保留 selective risk | 尚未完成 citation-forward full-text audit | Unknown | D1-P 的 novelty 生死線 |
| conformal 在 arbitrary unseen-generator shift 下能否保證風險 | 標準 conformal 的 exchangeability 與部署 shift 間存在假設衝突；P1/P2 尚在查 | Unknown / theoretical concern | D1-C 不能在查證前使用「distribution-free under generator shift」作既定賣點 |

## 4. 四個候選版本

### D1-C：Generator-shift-aware conformal selective risk（Claude 現有 Path A）

**RQ**：能否只用 source development generator families，建立在新 generator 上仍有意義的 selective-risk bound，或可靠判定何時不能給 bound？

**Hypothesis**：在明確限制的 shift set 或 generator-family model 下，group/worst-case conformal 程序比 pooled calibration 更少違反外部 selective-risk target。

**可能貢獻**：形式化程序、有限樣本性質，以及保證成立／拒絕成立的條件。

**主要風險**：

- unseen generator 不屬於已知 group 時，group-conditional coverage 不會自動外推；
- arbitrary distribution shift 下，source-only guarantee 可能在資訊上不可識別；
- 「方法失敗後開不可轉移證書」必須有正式定義、soundness 與可觀測條件，不能只把 violation detector 改名為 certificate；
- 對一般大眾的 deployability 幫助主要是 reliability，而非模型大小、延遲或隱私。

**Useful negative result**：清楚證明哪些 generator-shift assumptions 不足以支援 source-only selective guarantee；但若只有實證失敗而無形式或診斷增量，會退回 measurement thesis。

### D1-P：Selective-risk-preserving compression（Codex 首選）

暫定題名：

> *Selective-Risk-Preserving Compression for Deployable Audio Deepfake Detection under Unseen Generators*

**RQ1**：distillation 或 quantization 是否可能在保留 AUROC/EER 的同時，破壞 error ranking、calibration 或 source-fixed abstention-threshold transfer？

**RQ2**：在相同模型大小與推論延遲下，selective-risk-aware distillation 是否比 ordinary KD 更能保留 teacher 的 risk–coverage 行為？

**RQ3**：此效果在 attack-system-disjoint holdout 與一種常見 codec 條件下是否仍成立？

**Falsifiable hypotheses**：

- H1：普通壓縮造成的 discrimination loss 小於 selective-reliability loss；也就是 EER 看似維持，但 eAURC、class-conditional coverage 或 fixed-`(q+t)` violation 顯著惡化。
- H2：加入 correctness/error-ranking distillation 與 clean–codec selection-consistency 後，student 在相同資源預算與 matched coverage 下有較低的 generator-macro confident-real leakage。

**Proposed contribution**：

1. 壓縮前後 discrimination、ranking、calibration 與 threshold transfer 的分解式稽核；
2. 一個 selective-risk-aware distillation objective，而不是新增 backbone；
3. 一個低成本、離線、三態輸出的 reference implementation 與 deployment model card。

**Minimal method**：一個 frozen teacher、一個小型 student；ordinary KD 對比 `KD + error-ranking/selection loss + clean–codec consistency`。只選一種量化設定、一個 codec family 及一個 confirmatory holdout。

**Primary comparisons and metrics**：

- 相同 parameter count／latency：ordinary KD vs selective-risk-aware KD；
- AUROC/EER 只作 discrimination gate；
- primary：generator-macro `L_CR` at matched fake/overall coverage；
- secondary：eAURC、error-AUROC、Brier/NLL、source-fixed `(q+t)` violation；
- deployment：CPU latency、peak RAM、model size；energy 只在量測設備可靠時納入。

**Closest-work collision**：DK-CAST 已涵蓋 compression-aware KD、codec robustness 與 resource-constrained deployment；Pascu/FADEL 涵蓋 reliability/uncertainty。residual gap 只能是兩者交集中的非顯然問題：**壓縮是否破壞 selective reliability，以及如何在相同資源預算下保留它。**

**Failure / kill conditions**：

- 找到直接前作已在 ADD distillation/quantization 下最佳化並外部驗證 selective risk 或 fixed abstention transfer；
- ordinary KD 已完整保留所有 selective metrics，新增 loss 沒有穩定增益；
- teacher 在 holdout 接近隨機，使問題其實是 detector generalization 而非 compression；
- improvement 只來自較大 student、更多資料或不同 preprocessing；
- reference deployment 只是 demo，沒有量化資源與錯誤成本。

**Useful negative result**：即使 EER 保留，模型壓縮仍系統性破壞 threshold transfer；這可形成對 edge ADD 評估標準的具體修正建議。

**一年 minimum scope**：一個 teacher、一個 student architecture、ordinary vs proposed KD、兩個 precision/quantization points、一個主要 holdout、一個 codec family。不要同時做 mobile UI、使用者研究、多語大矩陣或六種 uncertainty methods。

### D1-M：Source-only meta-selective calibration

**RQ**：將 source generator families 輪流視為 pseudo-unseen domain，能否學到比 pooled development 更能轉移的 selector 或 score normalization？

**Hypothesis**：leave-one-generator-family-out episodic objective 能降低真正 unseen family 的 worst-generator selective risk。

**Minimal method**：在 frozen embeddings 上訓練一個小型 selection head，以 worst-generator／group-DRO selective objective 最佳化；不改 detector backbone。

**Residual gap**：不是新的 generalizable ADD，而是 source-only episodic training 對 abstention transfer 的影響。

**Risk**：與 ALDEN、RWM 以及 generic group-DRO/selective learning 的組合可能過於顯然；source generator diversity 也可能無法代理未來 shift。

**Useful negative result**：既有 generator families 的 pseudo-shift 無法預測新世代 generator 的 reliability failure。

### D1-G：Fail-closed deployment guardrail

**RQ**：能否利用無標籤 score/embedding drift、codec statistics 或 cheap detector disagreement，在 deployment environment 層級預警 source-fixed operating point 已不適用？

**Hypothesis**：多訊號 monitor 比任一單一 OOD score 更能召回會發生 risk violation 的 deployment batches。

**Contribution**：輸出 `green/yellow/red` 的環境層級 guardrail；red 時提高 abstention 或停用自動判斷。

**Risk**：unlabeled covariate drift 不等於 risk drift；單一使用者的一則訊息也缺少 batch。它只能是 alarm，不能宣稱 safety certification，較適合平台或查核 pipeline。

**Useful negative result**：在任意 generator shift 下，無標籤 drift 不能可靠識別 detector risk，界定 deployment monitoring 的限制。

## 5. 比較與 Codex 暫定建議

| Candidate | 主要貢獻 owner | 與作者願景的直接性 | 最大生死線 | 一年風險 |
|---|---|---|---|---|
| D1-C conformal | 形式方法／風險控制 | 中：改善可靠性，但不直接降低部署成本 | unseen shift 下的保證是否可識別、是否已有前作 | 中；方法小但理論責任重 |
| D1-P compression | ML 方法 + edge/system evaluation | **高：直接處理大小、延遲、離線與 reliability** | selective-risk-aware ADD compression 是否已被做過 | 中；需訓練 student，但範圍可控 |
| D1-M meta-selective | ML generalization method | 中高：增強 unseen-generator reliability | 與 meta-learning/group-DRO 前作是否只是顯然組合 | 中高 |
| D1-G guardrail | deployment safety mechanism | 中：平台適用，單筆大眾使用較弱 | label-free risk identifiability | 高；容易退成 drift benchmark |

**Codex 暫定推薦：D1-P > D1-C > D1-M > D1-G。**

理由不是 D1-P 已被證明較新，而是它的問題、方法與作者想要的部署價值在同一條因果鏈上：模型要小且離線，但壓縮不能讓拒答機制失真。D1-C 若能給出在明確 shift assumptions 下真正成立的新保證，科學性可能更強；但它目前對「arbitrary unseen generator」的保證措辭過度樂觀，也較少處理大眾部署的資源門檻。

不建議把 D1-C 與 D1-P 同時做成兩個主要方法。可以先讓兩者通過各自的 novelty/theory kill check，再由作者選一個 contribution owner；未選中的只能作 baseline 或 future work。

## 6. 請 Claude 獨立審查的問題

請不要只潤稿，請用反方立場回答：

1. **逐案裁決**：對 D1-C／D1-P／D1-M／D1-G 分別給 `KEEP / NARROW / KILL`，並指出最可能的直接撞題。
2. **正面比較 D1-C 與 D1-P**：哪一個有更清楚的 contribution owner？哪一個更貼近作者「易部署、一般大眾可用」的目標？
3. **攻擊 conformal claim**：在未知 generator 打破 exchangeability 時，Path A 究竟能保證什麼？若只能在已知 family 或 bounded shift 下成立，請重寫最窄可守的 RQ。若「不可轉移證書」沒有 soundness 定義，請直接否決該措辭。
4. **攻擊 compression novelty**：DK-CAST、其他 KD／quantization ADD 是否已報告 calibration、uncertainty ranking、AURC、risk–coverage 或固定 abstention threshold transfer？若有，D1-P 還剩什麼 residual gap？
5. **驗證 deployment chain**：small/offline + abstention 是否真的足以支撐面向大眾的技術貢獻？還缺哪些最低限度的 resource、privacy、decision-output 或 misuse 評估？
6. **砍 scope**：若只能保留一個 method、一個 student、一個 holdout 與一個 channel，Claude 會保留什麼？
7. **給出決策 gate**：列出能在不跑 full pilot 前 KILL D1-P 的最小文獻查證，以及若 D1-P 被殺，應回 D1-C 還是退出 #1。

期望 Claude 的回覆包含 closest-work matrix、strongest objection、可守的 RQ、最小一年 scope、useful negative result，以及最終排序。不要把 agent 共識當成 novelty 證據。

## 7. Validation contract

### 下一個最小步驟

在解除 pilot 暫停前，完成兩條平行但只讀的 commit gate：

1. **D1-P literature gate**：citation-forward 檢查 ADD compression、KD、quantization 與 lightweight deployment 全文，特別搜尋 calibration、AURC、selective prediction、abstention、risk–coverage、confidence preservation、fixed threshold transfer。
2. **D1-C theory/novelty gate**：完成既有 P1/P2，並要求每個保證寫出 exchangeability／shift-set／group observability assumptions。

### Strengthen signal

- D1-P：沒有 inspected direct work 聯合研究 ADD compression 與 external selective-risk transfer；初步結果顯示 EER 與 selective reliability 對壓縮反應不同。
- D1-C：能在 realistic、可檢驗且非 target-label-dependent 的 assumptions 下給出比 pooled conformal 更強的新性質。

### Kill or narrow

- 若 D1-P 已有直接等同方法與 protocol，KILL 或縮成獨立 replication，不能以新 loss 換名續命。
- 若 D1-C 只能對 source exchangeable data 給標準 conformal 保證，且 unseen-generator 部分只剩事後 violation，則縮回 baseline／measurement，不作主方法。
- 若所有 deployability 主張最終都依賴未規劃的 user study，技術主張改為 resource-constrained reliable detection，不宣稱 public-risk reduction。

### Pivot

- D1-P 方法失敗但壓縮明顯破壞 reliability：轉成 compression-induced reliability failure audit，加上評估標準與 model-card contribution；是否足以成 thesis 需作者／advisor裁定。
- D1-C 方法失敗且無形式負結果：不以「certificate」包裝，回到 D1-P 或退出 #1。

### Remaining unknowns

- DK-CAST 與其他 ADD KD/quantization 工作的完整 metric 與外部 transfer protocol；
- 可用 teacher/student checkpoint、授權與實際 CPU target；
- confirmatory holdout 的 generator lineage 與 family 數；
- 使用者實際裝置、可接受延遲、模型大小與 abstention capacity；
- conformal P1/P2 的 current closest work。

## 8. Project-state impact

- `DECISIONS.md`：不修改；作者尚未選 D1-C 或 D1-P。
- `PROJECT.md`：不修改；這是候選方向細化，不是已批准 scope。
- `TASKS.md`：本輪不修改；Claude 審查與兩條 commit gate 完成後，再由作者決定是否取代目前的 conformal-only gate。
- 實作與 pilot：維持暫停。
