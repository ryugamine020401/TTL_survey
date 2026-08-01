# Codex 對碩論計畫 v1 的驗證：現實門檻、H1b 單調性與 replication-plus-extension

日期：2026-07-18  
模式：Validate + Compare  
狀態：供 Claude red-team；未經作者裁定，不代表題目或計畫已變更

## 1. Inquiry

本文件回答兩個問題：

1. `discussions/2026-07-18-thesis-plan-v1.md` 的悲觀 novelty 判斷，以及 source-dev 凍結 operating point 後部署到未知 generator 的設定，是否有文獻與數學依據？
2. 若廣義方法 novelty 已被前作壓縮，能否把論文主軸改成「忠實重現最近方法、在更現實的 ADD 情境驗證其邊界，再提出有診斷依據的增量改良」？

範圍限於計畫書 v1 的研究設計與貢獻定位；不授權下載資料、訓練模型、改寫 `DECISIONS.md`，也不直接改動計畫書 v1。

## 2. Bottom line

1. **Verified：source-frozen threshold／policy 是合理的現實部署 proxy。** 真實系統不能用 target test labels 重選 EER threshold；ICWSM 2026 已在 ADD 中明確指出預設門檻比 test-derived EER threshold 更符合部署，且實測性能明顯下降。
2. **Verified：廣義 calibration-aware KD、calibrated ADD、lightweight ADD KD 均已有直接前作。** 因此不能把「校準蒸餾」或「輕量 ADD 的可靠性」泛稱為全新方法題；剩餘 gap 只可能位於 `lightweight ADD × lineage-disjoint unseen generators × source-frozen selective-policy transfer` 的窄交集。
3. **Inference（高信心、待補 score 公式）：目前 H1b 可能退化成近乎由設計保證的結果。** 若 temperature scaling／binary Platt 只是對同一 scalar logit 做嚴格單調轉換，而每個模型又在轉換後依同一 source-dev operating constraint 重選自己的 `(q_m,t_m)`，則 source 與 target 上的接受／分類集合通常不變。TS/Platt 修不好 primary leakage，未必是實證發現，而可能是數學等價。
4. **Recommendation：可改成 replication-plus-extension，而且比強求「從零發明」更穩健。** 但最低可守版本不是「把別人的方法套到 ADD」，而是「忠實重現最近 baseline → 在未見生成器的 external policy transfer 下發現並診斷失效 → 加入能改變 correctness ordering／selection behavior 的最小機制 → 以 matched discrimination 與資源預算做消融驗證」。

## 3. Evidence map

| 命題 | 原始／官方證據 | 狀態 | 對計畫的含義 |
|---|---|---|---|
| 部署門檻必須預先決定 | Schäfer & Steinebach, ICWSM 2026：指出 EER threshold 使用 test scores；預設 threshold 才接近 real-world，ITW F1 可由 91.35% 降至 64.65% | **Verified** | H1a 的 external fixed-policy 問題合理，但「預設門檻 ADD 評估」本身已非全新 |
| IID post-hoc calibration 在 shift 下可能不足 | Ovadia et al., NeurIPS 2019：IID validation 的 TS 在較強 shift 下落後 uncertainty-aware 方法，部分設定甚至傷害 Brier | **Verified** | 支持研究 source-only calibration 的外部轉移邊界，但不保證 ADD 或壓縮後一定失效 |
| TS 是單一正溫度 logit rescaling | Guo et al., ICML 2017：`z/T, T>0`；不改 argmax/class prediction | **Verified** | 對 binary scalar score 為 order-preserving；不能期待它修正排序型 selective 指標 |
| calibration transfer via KD 已存在 | Hebbalaguppe et al., ACCV 2024, KD(C) | **Verified** | H2 不能只叫 calibration-aware KD |
| calibrated、跨資料集 ADD 已存在 | Pascu et al., Interspeech 2024 | **Verified** | full-model ADD calibration/generalization 層已知 |
| lightweight、confidence/codec-aware ADD KD 已存在 | DK-CAST, Discover Computing 2025；另有 FTDKD 等 | **Verified** | paired clean↔codec consistency、confidence-weighted loss 等機制有撞題風險 |
| replication/generalizability study 可構成研究貢獻 | NeurIPS MLRC 2026 官方徵稿明列 rigorous replication、new-setting generalizability、negative/partial reproduction | **Verified（社群層）** | 支持 replication-plus-extension 的科學正當性；不等於保證本校碩論行政門檻 |

## 4. H1b 的條件性數學問題

假設模型產生 scalar score `s(x)`，校準器是嚴格遞增函數 `g`：

```text
s'(x) = g(s(x))
```

若 source-dev 依同一 operating constraint 選得原門檻 `tau`，校準後對應門檻為 `tau' = g(tau)`，則對任意 source 或 target 樣本：

```text
1[s'(x) >= tau'] = 1[s(x) >= tau]
```

因此，在下列條件同時成立時，接受集合、分類集合、coverage、confident-real leakage 與 risk violation 應完全或近乎完全相同：

- binary ADD，使用單一 logit／probability score；
- TS 的 `T>0`，或 Platt slope 為正；
- `q_m`、`t_m` 都在校準後依相同 source-dev constraint 重選；
- selection score 只是該 scalar score 或其單調函數；
- 沒有 ties、離散化或額外 input-dependent uncertainty。

TS/Platt 仍可能改變 NLL、Brier、ECE 和機率語意，但不能改善排序；AURC/eAURC 也不應改變。

### 尚未建立的關鍵資訊

計畫書尚未把 `q_m`、`t_m`、confidence/selection score 寫成公式。因此上述結論是**條件性推論**。Claude 應先檢查：

1. `t_m` 是由固定 source FPR/FNR/cost constraint 選，還是永遠固定在語意機率 `0.5`？
2. `q_m` 是 score quantile、`max(p,1-p)`、distance-to-`t_m`，還是另一個 correctness estimator？
3. calibrator 後是否真的重新選 `(q_m,t_m)`？
4. primary policy 是「相同 source risk/coverage constraint」還是「固定語意機率承諾，例如 estimated error ≤ 5%」？

若答案符合單調等價條件，Stage 0.3 不能再把 TS/Platt 的失敗當成 H2 空間證據，只能把它們列為 probability-calibration controls。

## 5. 兩種可守的主軸

### A. Selective-policy transfer（推薦）

- **RQ**：既有 calibration/uncertainty-aware KD 是否能在 lineage-disjoint unseen generators 上保留 source-only 決定的 selective policy？
- **baseline**：ordinary KD、KD(C) 類方法、ordinary KD + TS/Platt，以及至少一個能改變 instance ordering 的 source-only selector／correctness estimator。
- **增量方法**：selection-aware correctness ranking、selection-margin consistency、source proxy-group robust selector，或其他能改變樣本排序的方法。
- **primary**：generator-macro confident-real leakage / risk violation；AUROC/EER 與部署成本配平。
- **貢獻型態**：independent replication + external-validity gap + incremental method。
- **最大風險**：calibrated selective classification、uncertainty-matching KD、DK-CAST 已涵蓋相似機制；必須做 method closest-work gate。

### B. Semantic calibration transfer

- **RQ**：source-dev 學得的機率語意或 risk promise，經 lightweight transformation 後能否轉移到未知 generator？
- **policy**：使用固定語意門檻，例如只在 estimated error probability ≤ `delta` 時接受，而不是每個模型重新選等價 quantile。
- **primary**：target calibration/risk-promise violation；selective leakage 為部署結果。
- **優點**：TS/Platt 成為真正有意義的 trivial-repair baseline。
- **最大風險**：arbitrary unseen shift 下 source-only calibration 沒有一般保證；容易變成已知 calibration-under-shift 問題的 ADD application。

目前建議 A，因為它較貼近計畫原先的記者／事實查核者 triage 情境，也能保留 source-frozen policy 的現實意義。但標題應弱化 `Calibration Preservation`，改以 `Selective-Policy Transfer` 或 `Selective-Risk Preservation` 為核心。

## 6. 「仿效再改進」的最低貢獻合約

可接受的說法不是「我們仿效以前的方法」，而是：

> We independently replicate the closest calibration-aware distillation baselines, test their external validity under a source-frozen selective policy on lineage-disjoint unseen audio generators, diagnose why in-domain calibration does or does not translate into external selective-risk transfer, and evaluate a minimal selection-aware extension under matched discrimination and deployment budgets.

要守住 incremental contribution，至少必須同時滿足：

1. 最近方法被忠實重現，差異不是因 baseline 做弱或重現失敗；
2. 新 setting 不只是換資料集，而是改變一個有部署意義、前作未回答的 estimand；
3. 改良機制直接對應已診斷的 failure mode；
4. 有消融證明增益來自新增機制，而不是模型變大、更多資料、target tuning 或不同門檻；
5. 改良在 generator-family macro primary endpoint、matched AUROC/EER 與資源限制下仍成立；
6. 若最近方法已足夠，誠實降為 replication/audit，不事後重新命名 loss 製造 novelty。

## 7. 請 Claude red-team 的具體問題

1. 依計畫 v1 可推定的 `q_m,t_m` 定義，Codex 的單調等價分析是否正確？請列出成立條件、反例與實際 pipeline 中會破壞等價的因素。
2. H1b 應如何改寫，才不是「TS 按設計必敗」？請至少提出一個最低成本、能改變 ordering 的 source-only repair baseline。
3. 在 A/B 兩個主軸中，哪個更能同時滿足：一人一年、RTX 4090、無 target-label tuning、方法貢獻、記者本機 triage？
4. replication-plus-extension 是否足以達到本計畫所要求的貢獻 bar？請區分：純 reproduction、application novelty、external-validity evidence、incremental method contribution。
5. 請再攻擊暫定 H2：correctness-ranking、selection-margin、paired clean↔codec selection consistency 是否已被 calibrated selective classification、uncertainty-aware KD、DK-CAST 或其他最近方法涵蓋？
6. 若同意修正，請提供計畫書 v1 的精確 redline 建議，至少涵蓋標題、摘要、RQ/H1b/H2、baselines、Stage 0.3、風險聲明；不要直接覆寫 v1。

## 8. Validation contract

- **下一個最小步驟**：在任何 pilot 前，用半頁數學規格明確定義 raw score、class decision、selection score、`q_m`、`t_m`、calibrator fit 與 threshold fit 的順序，並用一組玩具 logits 驗證 TS/Platt 前後 primary decisions 是否完全一致。
- **支持 A 的訊號**：單調校準不改 primary decisions；但一個 source-only、input-dependent correctness score 能在 held-out source proxy groups 改善 risk transfer，且最近 ADD/KD 前作沒有評估相同 external estimand。
- **kill／narrow**：最近方法已聯合涵蓋 ADD lightweight transformation、unseen-generator selective-policy transfer 與同型 selection-aware loss；或 ordinary KD/KD(C) 已保留 policy；或改良只能靠 target labels。
- **pivot**：若方法空間消失，將成果定位為嚴格 replication/external audit，並回到其他候選題比較，而不是硬宣稱方法 novelty。
- **剩餘未知**：`q_m,t_m` 精確公式、學校／指導教授對純 replication-extension 的碩論門檻、最接近 selection-aware distillation 的完整搜尋結果。

## 9. Project-state impact

目前不應改 `PROJECT.md`、`TASKS.md` 或 `DECISIONS.md`。先等待 Claude red-team 與作者裁定；若作者接受主軸 A 或 B，再建立 plan v2 並同步正式狀態。

## 10. Sources inspected

查證日期：2026-07-18。搜尋範圍：官方 proceedings／出版社頁與原論文；核心 query family 包含 `audio deepfake preset/fixed threshold`、`calibration transfer knowledge distillation`、`lightweight audio deepfake distillation confidence`、`temperature scaling monotonic ranking`、`selective classification distribution shift`、`replication generalizability contribution`。

- Schäfer & Steinebach, “Reality Check: Measuring Real-World Applicability of State-of-the-Art Audio Deepfake Detectors on Social Media Data,” ICWSM 2026: https://ojs.aaai.org/index.php/ICWSM/article/view/42803
- Ovadia et al., “Can You Trust Your Model's Uncertainty?,” NeurIPS 2019: https://proceedings.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html
- Guo et al., “On Calibration of Modern Neural Networks,” ICML 2017: https://proceedings.mlr.press/v70/guo17a.html
- Hebbalaguppe et al., “Calibration Transfer via Knowledge Distillation,” ACCV 2024: https://openaccess.thecvf.com/content/ACCV2024/html/Hebbalaguppe_Calibration_Transfer_via_Knowledge_Distillation_ACCV_2024_paper.html
- Pascu et al., “Towards generalisable and calibrated audio deepfake detection with self-supervised representations,” Interspeech 2024: https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html
- “Dynamic knowledge condensation with audio-selective transformer for audio deepfake detection,” Discover Computing 2025: https://link.springer.com/article/10.1007/s10791-025-09746-4
- NeurIPS MLRC 2026 official announcement: https://blog.neurips.cc/2026/05/04/mlrc-2026-reproducibility-as-an-official-track-at-neurips/

