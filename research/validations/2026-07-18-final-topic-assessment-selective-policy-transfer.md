# 最終題目認定：未知生成器下輕量 ADD 的 Selective-Policy Transfer

日期：2026-07-18  
模式：Validate + Decide  
評估對象：`discussions/legacy/2026-07-18-thesis-plan-v2.md`  
判定：**題目方向 GO；實驗規格 CONDITIONAL GO**  
權限狀態：供作者與 Claude 統整；尚未寫入 `DECISIONS.md`，未解鎖下載、pilot 或訓練

## 1. Inquiry

本評估決定：plan v2 是否已足以成為碩士論文的最終工作題目，以及正式定題前還有哪些會影響有效性、novelty 或可執行性的必要修正。

### 固定問題框架

- **科學問題**：模型輕量化後，由 source-dev 決定並凍結的 accept/abstain/classification policy，在 lineage-disjoint unseen generators 上能否保留？
- **主要 stakeholder**：記者／事實查核者的本機初篩；棄權後升級人工或帶外查核。
- **分析單位**：完整語音訊息；泛化單位為 generator family。
- **threat model**：未知生成器造成的自然 distribution shift；本論文不涵蓋 adaptive attack、partial deepfake、真人使用者成效或身分驗證。
- **貢獻 bar**：忠實 baseline replication + external-validity test + 由失效診斷導出的增量方法；只有 H2 打贏強 rank-changing baseline 才主張方法貢獻。
- **邊界**：一人一年、單張 RTX 4090、不訓練 foundation model、不用 target labels 調參、不依賴 human-subject study。

## 2. Final determination

### 2.1 題目方向：GO

建議固定題目：

> **未知生成器下輕量音訊深偽偵測器的選擇性策略轉移**  
> **Selective-Policy Transfer of Lightweight Audio Deepfake Detectors under Unseen Generators**

理由：

1. **Verified：部署 estimand 合理。** 真實 ADD 不能用 target test labels 重選 EER threshold；ICWSM 2026 已顯示預設門檻比 test-derived threshold 更符合部署，且效能可大幅下降。
2. **Inference：殘餘 gap 可守但很窄。** 已查前作分別涵蓋 lightweight ADD、calibrated ADD、calibration/uncertainty-aware KD、AURC 與 selective classification under shift；在已記錄搜尋範圍內，尚未找到同時研究 `lightweight ADD × lineage-disjoint unseen generators × source-frozen selective-policy transfer` 的工作。
3. **Verified：v2 已修正 H1b 的核心邏輯。** TS／正斜率 binary Platt 對 scalar score 為單調轉換；在相同 source rank constraint 下重選 threshold 時，不能改變 primary ranking policy，適合作 control，不適合作 repair gate。
4. **Inference：一年範圍可行。** 一個 teacher、一至兩個 lightweight transformations、一個 confirmatory holdout、一個 H2 mechanism 的範圍合理，且有明確 early-stop sequence。
5. **Verified：replication-plus-extension 是正當的研究貢獻型態。** 但本校的行政／口試門檻仍須指導教授確認，不能由文獻或 agent 代替。

### 2.2 實驗規格：CONDITIONAL GO

目前不能直接解鎖 confirmatory experiment，因為存在一個 hard blocker 與四項設計規格缺口。它們不否決研究問題，但若不修會破壞 confirmatory validity 或使 H1a/H1b 混淆。

## 3. Evidence map

| Claim / issue | Primary or authoritative evidence | Status | Consequence |
|---|---|---|---|
| 預設 threshold 是真實 ADD 部署問題 | Schäfer & Steinebach, ICWSM 2026 | **Verified** | 支持 source-frozen policy estimand；但 preset-threshold ADD evaluation 本身已非全新 |
| calibration/KD/lightweight ADD 各層已有前作 | KD(C) ACCV 2024；Pascu Interspeech 2024；DK-CAST 2025；既有 Q1–Q3 validation | **Verified** | novelty 只能主張窄交集，不可泛稱首次可靠性壓縮 |
| generic selective classification under shift 已有 rank-changing/post-hoc score baselines | Liang, Peng & Sun, TMLR 2024：margin scores，並比較 Energy、KNN、ViM、SIRC 等 | **Verified** | H1b 必須納入強 generic baseline；feature-space selector 本身不是新方法空白 |
| matched accuracy 後 selective degradation 可能消失 | Cattelan & Silva, NeurIPS 2023 workshop：84 ImageNet classifiers；修正 confidence estimator 後 selective performance 幾乎由 accuracy 決定，shift drop 可由 accuracy drop 解釋 | **Verified contradicting evidence** | H1a 可能為 null；早停 gate 必須保留，不預設現象存在 |
| ASVspoof 5 不允許 MLS/LibriLight-derived model，因與 evaluation data overlap | ASVspoof 5 official Phase-2 Evaluation Plan | **Verified** | checkpoint pretraining lineage 是 confirmatory blocker |
| 官方 XLS-R checkpoint 的 pretraining data 包含 MLS | Meta `facebook/wav2vec2-xls-r-300m` model card；XLS-R paper | **Verified** | plan v2 的 XLS-R teacher 與 ASVspoof 5 confirmatory holdout 組合不可直接採用 |
| ASVspoof 5 資料與 protocol 已公開，約 142.3 GB | Official Zenodo record 14498691 | **Verified** | 資料可取得；下載仍需作者授權，lineage/shortcut audit 仍未完成 |

## 4. Hard blocker：XLS-R × ASVspoof 5 upstream overlap

Plan v2 暫定 `XLS-R + AASIST/linear head` 為 teacher，ASVspoof 5 eval 為 confirmatory holdout。這個組合目前不可接受：

- ASVspoof 5 官方 evaluation plan 說明 MLS English 與 evaluation data 有 overlap，禁止 MLS、LibriLight 及其衍生 pretrained models；
- 同一文件明確允許 LibriSpeech 及其衍生資源；
- Meta 官方 XLS-R-300M model card 列出 MLS 為 pretraining corpus。

即使本研究不是 challenge submission，這仍是 representation pretraining 看過 evaluation upstream speech/speakers 的實質 contamination 風險，與 `lineage-disjoint holdout` 主張衝突。

### 解除條件

在下列方案中擇一並記錄：

1. 改用 pretraining lineage 可證明符合 ASVspoof 5 要求的 checkpoint，例如明確為 LibriSpeech-only 的 speech SSL backbone；或
2. 改 confirmatory holdout，並對新 holdout 重新做 generator、speaker、content、pretraining-corpus lineage audit；或
3. 若保留 XLS-R，只能把 ASVspoof 5 結果降為 contaminated/exploratory sensitivity，不能作 confirmatory evidence。

Lineage manifest 必須增加一欄：`backbone pretraining corpora → holdout upstream speaker/utterance overlap`。

## 5. 定題前必修的四項規格

### R1. 分開 H1a baseline selector 與 H1b repair

Plan v2 §5.1 已把 rank-changing feature-space `u(x)` 放入 primary policy，§4/§5.4 又把 feature-space selector 當 H1b repair，形成 treatment contamination。

建議：

- **H1a base policy**：預先定義普通 decision-margin selector，例如 `u0(x)=|s(x)-t_m|`；
- **H1b repair**：才加入 `u1(x)=h(s(x),z_student(x))` 的 rank-changing score；
- `z_student` 必須由部署中的 lightweight student 取得。若 selector 在 inference 需要完整 teacher／XLS-R，便不符合 edge estimand；
- selector 的 parameters、CPU latency、RAM 與 model size 必須計入 deployment budget。

### R2. 讓風險上限 `alpha` 真正由 source policy 約束

目前 `t` 由 FPR/cost 選、`q` 由 coverage 選，但 `Delta_transfer = L_CR^macro(holdout)-alpha` 又把 `alpha` 稱為預設風險上限。若 source fitting 沒有約束 `L_CR <= alpha`，該 promise 不成立。

推薦規格：

```text
(q_m, t_m) = argmax Coverage_dev(q,t)
subject to UCB_{1-delta}[L_CR,dev(q,t)] <= alpha
           and FPR_real,dev(q,t) <= beta
```

若有限樣本下無可行 policy，應輸出「無法承諾」而不是硬選 threshold。另一個可行版本是固定 source coverage `C0` 後只比較 target leakage，但那就不應稱 `alpha` 為已承諾風險上限。

### R3. 統一 matching 規格

H2 文字中的 `matched AUROC/eAURC` 與後文「eAURC 不作配平變數」矛盾。統一為：

> matched deployment budget + predeclared AUROC/EER equivalence tolerance；eAURC/error-AUROC 為 secondary outcome/diagnostic，不作 matching variable。

### R4. 預先限定 rank-changing baseline 與模型選擇規則

不能在 target holdout 上挑「最好的便宜 repair」。在 protocol 中預先限定一個小型 shortlist，所有超參數與 baseline 選擇只用 source train/dev；至少納入 TMLR 2024 generalized-SC 的強 generic score family 中適用於 binary ADD 的代表方法。

可考慮的 bounded set：

- normalized logit / decision-margin score；
- student-embedding Mahalanobis 或 ViM 類 score；
- confidence + OOD composite（SIRC 類）。

`cluster-conditional recalibration` 只有在 target inference 時能無標籤決定 cluster/router，且不使用 target labels 時才是合法 baseline。所有方法都要計算 deployment cost。

## 6. 必要文字修正

這些不是 blocker，但應由 Claude 統整進下一版：

1. 把「這把貢獻推向一片較少人碰的空間」改為 bounded wording；generic generalized selective classification 已直接研究 distribution shift。
2. 把 H1a 的「顯著高於」改為「高於預先定義的實質差異 `epsilon`，並報 paired family-level interval」。約 7 families 不適合以 utterance-level significance 支撐普遍性。
3. 區分「題目已固定」與「H2 mechanism 尚未固定」：H2 必須由 H1a diagnosis 導出並另過 closest-work gate。
4. `In-the-Wild` 沒有可信 generator lineage，只能 exploratory；不得用它通過 generator-macro confirmatory claim。

## 7. 修正後的假設骨架

### H1a — Base-policy transfer failure

在相同 source risk/coverage policy-fitting rule、matched discrimination tolerance 與部署預算下，ordinary lightweight student 使用預先定義的 base selector `u0`，其 unseen-generator family-macro `L_CR` 相對 teacher 增加至少實質差異 `epsilon`。

### H1b — Strong cheap-repair gate

只用 source train/dev 擬合、可在 student-side 廉價推論、且預先登記的 rank-changing selector `u1`，仍不能把 student 的 external policy transfer 修回 teacher/reference tolerance。TS/Platt 僅作 probability-calibration controls。

### H2 — Diagnosis-driven incremental method

若 H1a 成立且 H1b 失敗，才根據 family/error/representation diagnosis 定義一個 training-time or lightweight selection-aware mechanism；它必須在同一 student、同一 deployment budget 與 matched discrimination 下勝過 ordinary KD 及最強合法 H1b baseline，並通過 method closest-work gate。

## 8. Contribution contract

本題的可守貢獻不是「第一個研究 ADD reliability」，而是：

1. **replication contribution**：忠實重現最近的 lightweight/calibration-aware KD baselines；
2. **evaluation contribution**：建立 source-frozen、lineage-audited、generator-family macro 的 external selective-policy transfer protocol；
3. **diagnostic contribution**：區分 discrimination、score ordering、operating-point transfer 與 calibration 的失效來源；
4. **conditional incremental-method contribution**：只有 H2 打贏強 source-only rank-changing repair 才成立；
5. **useful negative result**：若 H1a null 或便宜 repair 足夠，留下對 edge ADD 評估規格的 bounded audit，但按作者設定不視為已達預期方法 bar。

## 9. Validation contract

### 下一個最小步驟

1. Claude 統整本評估與其獨立審查，產出不覆寫 v2 的 plan v3／consensus delta；
2. 選定一個 pretraining lineage 合格的 teacher checkpoint；
3. 把 `u0/u1/q/t/alpha/beta/delta/epsilon` 寫成 executable protocol；
4. 用 toy scores 驗證 base policy、TS/Platt invariance、rank-changing repair 與 joint policy fitting；
5. 完成 ASVspoof 5 generator + speaker/content + backbone-pretraining lineage manifest；
6. 指導教授確認 replication-plus-extension 與 conditional H2 的 thesis contribution bar。

### 解鎖 Phase 0 的訊號

- checkpoint lineage 無 holdout contamination；
- H1a/H1b treatment 層級不再重疊；
- source policy 確實滿足預設 risk/coverage rule；
- baseline shortlist 與所有 tuning data 已凍結；
- 作者授權小型資料下載與推論。

### Kill / narrow

- 找不到 lineage-clean teacher/holdout 組合；
- matched discrimination 後 H1a 無實質差異；
- 強 generic rank-changing repair 已足夠；
- H2 與最近 selective-classification／uncertainty-KD／ADD work 撞題；
- 需用 target labels 或完整 teacher inference 才能取得增益；
- generator families 或有效 clusters 不足以支持 bounded inference。

### Pivot

若方法空間消失，成果降為 replication/external audit，並回到其他候選方向比較；不得事後更名 loss 製造 novelty。

## 10. Proposed author-owned decision entry

以下文字僅供作者寫入 `DECISIONS.md`；Codex 不代寫決策檔：

> **2026-07-18 — Select selective-policy transfer for lightweight audio deepfake detection as the final working thesis direction.**  
> The thesis will test whether a source-frozen accept/abstain/classification policy survives lightweight model transformation on lineage-disjoint unseen generators. The intended contribution is a rigorous replication and external-validity protocol plus, only if H1a and H1b gates justify it, a diagnosis-driven incremental method that beats strong source-only rank-changing baselines under matched discrimination and deployment budgets. Human-subject evaluation, adaptive attacks, partial deepfakes, and foundation-model pretraining are excluded. Phase 0 remains gated on advisor approval, an executable policy specification, a lineage-clean teacher/holdout pair, and authorized data access.

## 11. Project-state impact

- **現在**：不更新 `PROJECT.md`／`TASKS.md`／`DECISIONS.md`，等待 Claude 統整與作者裁定。
- **作者正式接受後**：`PROJECT.md` 應把本題標為 selected direction；`TASKS.md` 應以 checkpoint-lineage、policy spec、baseline preregistration、Phase-0 environment 為 Now；`DECISIONS.md` 由作者加入上列或等價決策。
- **仍不授權**：142 GB ASVspoof 5 下載、full pilot、student/H2 training。

## 12. Search record and sources

查證日期：2026-07-18。搜尋系統：web search、官方 proceedings、TMLR/OpenReview、ASVspoof 官方網站／evaluation plan／Zenodo、Meta author-maintained model card。核心 query families：`audio deepfake fixed/preset threshold`、`selective classification distribution shift feature-space score`、`knowledge distillation reliability calibration`、`ASVspoof 5 MLS LibriLight pretrained model overlap`、`XLS-R pretraining MLS`。範圍限制：沒有宣稱全球首次；H2 尚未定義，因此 method-level novelty 仍是 Unknown，必須在 H1a diagnosis 後重查。

- Schäfer & Steinebach, ICWSM 2026: https://ojs.aaai.org/index.php/ICWSM/article/view/42803
- Guo et al., ICML 2017: https://proceedings.mlr.press/v70/guo17a.html
- Ovadia et al., NeurIPS 2019: https://proceedings.neurips.cc/paper_files/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html
- Hebbalaguppe et al., ACCV 2024: https://openaccess.thecvf.com/content/ACCV2024/html/Hebbalaguppe_Calibration_Transfer_via_Knowledge_Distillation_ACCV_2024_paper.html
- Pascu et al., Interspeech 2024: https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html
- Liang, Peng & Sun, TMLR 2024: https://openreview.net/pdf?id=dmxMGW6J7N
- Cattelan & Silva, NeurIPS 2023 workshop: https://nips.cc/virtual/2023/80532
- ASVspoof 5 official Phase-2 Evaluation Plan: https://www.asvspoof.org/file/ASVspoof5___Evaluation_Plan_Phase2.pdf
- ASVspoof 5 official Zenodo: https://zenodo.org/records/14498691
- Meta XLS-R-300M model card: https://huggingface.co/facebook/wav2vec2-xls-r-300m
- XLS-R paper: https://arxiv.org/abs/2111.09296
