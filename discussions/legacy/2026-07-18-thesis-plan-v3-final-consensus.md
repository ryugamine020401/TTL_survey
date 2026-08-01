# 碩士論文計畫 v3 — 最終共識文件

## 未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留
### Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators

日期：2026-07-18　狀態：**題目方向 GO；實驗規格 CONDITIONAL GO**（正式定題由作者寫入 DECISIONS.md；下載/pilot/訓練仍暫停）
整合來源：plan v2（`2026-07-18-thesis-plan-v2.md`）+ 外部審核確認（`2026-07-18-claude-confirm-external-review.md`）+ Codex 最終認定（`research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md`）+ Codex 資料集 delta（`research/validations/2026-07-18-dataset-recency-direct-access-gate-delta.md`）
> 不覆寫 v1/v2；本檔為最終共識。

---

## 0. v3 相對 v2 的變更（一覽）
1. **主 estimand 改為 teacher-relative double-difference `Δ_light`**（隔離「輕量化額外損失」與「teacher 自身失效」）。
2. **`α` 進 policy 建構**（UCB 約束）；`L_CR` 與 coverage 聯合約束（防「全棄權」作弊）。
3. **H1a base selector `u0` 與 H1b repair `u1` 分離**（R1，避免 treatment contamination）。
4. **硬 blocker：XLS-R × ASVspoof 5 的 MLS 預訓練重疊** → teacher backbone 必須換 lineage-clean（見 §6）。
5. **資料集免申請 hard gate（A/B/C）+ dataset role table + primary→fallback 切換 + protocol-first 下載順序**（見 §7）。
6. H2 不 pin 死機制、pin family+範圍、由 H1a 診斷導出、過 closest-work gate；matching 統一（R3）；In-the-Wild 僅 smoke test。

---

## 1. 最終題目與核心問題
**核心問題**：模型輕量化後，由 source-dev 決定並凍結的 accept/abstain/classification policy，在 documented lineage-disjoint unseen generators 上能否保留？若便宜的 source-only rank-changing 修法不足，能否用一個由失效診斷導出的機制保留它（不用 target labels、固定部署預算與辨識力容忍）？

**stakeholder**：記者/事實查核者的本機初篩；三態輸出（發現合成證據／未發現合成證據（≠已驗證真人）／證據不足棄權）。**threat model**：未知生成器的自然 shift；不涵蓋 adaptive attack、partial deepfake、真人成效、身分驗證。

## 2. 背景與動機（精簡，詳見 v2 §1–2 / survey）
deepfake 詐騙侵蝕信任 → 兩防線極限（被動偵測 generalization 崩、C2PA 只證未竄改）→ 部署缺口：輕量/edge ADD 只用 EER/AUC/延遲評估，沒人查輕量化是否破壞「該棄權時棄權」。動機鏈：大眾/記者本機安全使用 → 本機低成本 → 輕量 → 不能只看 EER → 研究凍結選擇策略守不守得住、能否保留。

## 3. 誠實 novelty 定位（bounded wording）
前作已分別涵蓋 lightweight ADD、calibrated ADD、calibration/uncertainty-aware KD、AURC、**以及 generic selective classification under shift 的 rank-changing/post-hoc score baselines（TMLR 2024）**。在已記錄搜尋範圍內，未見同時研究 `lightweight ADD × documented lineage-disjoint unseen generators × source-frozen selective-policy transfer` 者。**不主張「首次」、不宣稱「較少人碰的空間」**（generic SC under shift 已直接研究）；主張的是這個窄交集的預註冊量測 + 條件性方法。

## 4. 最終假設（kill sequence）
- **H1a — Base-policy transfer failure**：在相同 source risk/coverage policy-fitting rule、matched discrimination tolerance、部署預算下，ordinary lightweight student 用**預先定義的 base selector `u0(x)=|s(x)−t_m|`**，其 unseen-generator family-macro `Δ_light` 超過具部署意義的實質差異 `ε`（報 paired family-level interval，非 utterance-level p 值）。
- **H1b — Strong cheap-repair gate**：只用 source train/dev 擬合、可在 **student 端**廉價推論、預先登記的 rank-changing selector `u1`（shortlist 見 §11），**仍**無法把 external policy transfer 修回 teacher/reference 容忍。TS/Platt 僅作 probability-calibration control（已證 no-op）。
- **H2 — Diagnosis-driven incremental method（條件性）**：僅當 H1a 成立且 H1b 失敗，才依 family/error/representation 診斷定義一個 training-time 或輕量 selection-aware 機制；須在同 student、同預算、matched discrimination 下打贏 ordinary KD 與最強合法 H1b baseline，並過 method closest-work gate。

## 5. Policy 與 estimand 規格
- raw score `s(x)∈ℝ`；分類 `ŷ=1[s≥t_m]`。
- **H1a base selector**：`u0(x)=|s(x)−t_m|`（decision-margin，非 rank-changing）；`accept ⇔ u0≥q_m`。
- **H1b repair selector**：`u1(x)=h(s(x), z_student(x))`（rank-changing，`z_student` 取自**部署中的 student**，不得需要完整 teacher/XLS-R inference；selector 的參數/latency/RAM 計入部署預算）。**必須以 Kendall τ / accepted-set disagreement 實測確認 u1 真的改變 accepted set。**
- **α 進 policy（UCB 約束）**：
  ```
  (q_m,t_m) = argmax Coverage_dev(q,t)
  s.t.  UCB_{1-δ}[ L_CR,dev(q,t) ] ≤ α    (信賴上界，非點估計)
        FPR_real,dev(q,t) ≤ β
  ```
  有限樣本無可行 policy → 輸出「無法承諾」，不硬選門檻（no-feasible-policy fallback）。
- **防作弊**：primary endpoint 與 overall/fake/bona-fide coverage 與人工複核比例**聯合約束/報告**（否則「全棄權」也能低 leakage）。
- **主 comparative estimand（隔離輕量化額外損失）**：
  ```
  G_m = L_CR^target − L_CR^source     (每模型 transfer gap；source 分量用 held-out source 估)
  Δ_light = G_student − G_teacher       (輕量化額外退化；per-family 版 Δ_light,g，再 family-macro)
  ```
  並列報 per-family `G_student, G_teacher` 分量以求透明。
- **matching（統一 R3）**：配平只用 deployment budget + 預宣告 AUROC/EER equivalence tolerance；**eAURC/error-AUROC 為 secondary diagnostic，不作配平變數**。
- **擬合順序**（全部凍結後才碰 target）：model-train → selector-train（out-of-fold）→ policy-dev 擬合校準/selector/`(q_m,t_m)` → 凍結 → target。

## 6. 硬 Blocker：XLS-R × ASVspoof 5 上游重疊（必解）
ASVspoof 5 官方 Phase-2 evaluation plan 指出 **MLS English 與 eval data 重疊，禁用 MLS/LibriLight 及其衍生 pretrained model**；官方 XLS-R-300M model card 列 **MLS 為預訓練語料** → plan v2 的 `XLS-R teacher × ASVspoof 5 confirmatory` **不可直接用**（representation 已看過 eval 上游語者，與 lineage-disjoint 衝突）。

**解除條件（擇一並記錄）**：
1. 換 **pretraining lineage 合格的 backbone**（ASVspoof 5 明確允許 LibriSpeech 及衍生）——**候選待 Codex 查證預訓練語料**：wav2vec2-base（LibriSpeech-960）、HuBERT-base（LibriSpeech）等英語 LibriSpeech-only SSL（ASVspoof 5 為英語，英語 backbone 適用）；**不可假設 lineage，須逐一 audit**；或
2. 換 confirmatory holdout（對新 holdout 重做 generator/speaker/content/**backbone-pretraining** lineage audit）；或
3. 保留 XLS-R → ASVspoof 5 結果只能降為 **contaminated/exploratory sensitivity**，不作 confirmatory。
> lineage manifest 新增欄位：`backbone pretraining corpora → holdout upstream speaker/utterance overlap`。

## 7. 資料集：免申請 hard gate + role table + 切換 + 下載順序

### 7.1 存取分級（critical path 必須 A 級）
| 級 | 定義 | 角色 |
|---|---|---|
| **A direct** | 匿名/公開連結直接下載，無表單/審核/資格 | **critical path 必須用 A** |
| **B account-only** | 只需免費帳號/接受標準條款，無人工審核/等待 | 只作 optional/secondary，不得為唯一 confirmatory |
| **C approval/gated** | 需寄信/申請/資格/邀請/DUA，或 final labels 只給參賽者 | **排除於 critical path** |

**排序規則（作者硬限制）**：先過**效度 + pretraining/data-lineage** gate → critical path 必須**立即可取**（免人工核准）→ 再比發布時間/metadata/混淆/授權/容量/算力 → **只有前述相近才以較新者優先**。**新 ≠ 自動勝出。**

### 7.2 Dataset role table（v3 固定）
| 角色 | 資料集 | 存取 | 容量/授權 | 效度/風險 | 前置 gate |
|---|---|---|---|---|---|
| **source baseline / repro anchor** | ASVspoof 2019 LA（暫留；若要更新，另比較 ASVspoof5 train/dev→eval，但未審 split lineage 前不換） | A | ODC-By | attack 偏舊 | source↔target lineage 比較 |
| **primary confirmatory** | **ASVspoof 5 eval 預註冊 subset** | **A**（Zenodo 直接下載；寄信只適用於「產生 spoofed data」，非下載既有 corpus） | ~142.3GB / ODC-By 1.0 | protocol/metadata 完整 | **§6 backbone lineage-clean（hard blocker）** + generator/speaker/shortcut manifest |
| **newer direct-access fallback / secondary** | **XMAD-Bench**（EACL 2026） | **A**（GitHub/HF/Drive） | ~61.3GB | 很新、多語、split 明確；**但 cross-domain 同時改 language/real-source/speaker/generator → 因果混淆** | license + split-confounding + backbone-pretraining overlap audit（未過不升 primary） |
| **exploratory replication** | DFADD（pinned corrected release） | A | ~42.7GB / MIT | LJSpeech/VCTK source shortcut | 固定 revision + shortcut 控制；不作唯一 confirmatory |
| **plumbing only** | MLAAD-tiny | A | ~4.2GB / CC BY-NC 4.0 | prototyping/debug，代表性不足 | 僅 pipeline 驗證 |
| **不列 critical path** | 完整 MLAAD v9（B，帳號+real 拼接）；AUDETER（A 但 1.08TB、fake-only）；RADAR 2026/challenge-gated（C，資格/隱藏 labels） | — | — | 帳號摩擦/容量/資格 | 排除 |

### 7.3 Primary → Fallback 切換條件
- **ASVspoof 5 找不到 lineage-clean backbone**（§6 三方案皆不可）→ 切到**已完成 audit 的 XMAD-Bench**（或其他 A 級 holdout）；若仍保留 ASVspoof 5，只能降為 contaminated sensitivity。
- **XMAD-Bench license 或 cross-domain confounding 無法解決** → 維持 secondary，不升 primary。
- **任一候選變 C 級 / 公開連結失效 / license 改變** → **立即移出 critical path，切到已 audit 的 A 級候選，不等待申請**。
- **新資料集雖更新但 >1TB / 缺 real / 無可重現 protocol** → 不因「新」而納入。

### 7.4 明文 hard gate（寫入計畫）
> All datasets required for the preregistered critical path must be available by direct public download without manual application, eligibility review, invitation, DUA countersignature, or unreleased labels. Among datasets that pass access, license, lineage, confounding, and feasibility gates, prefer the most recent release. If a primary dataset's public link or license changes, switch to an already-audited direct-access candidate without waiting.

### 7.5 Protocol-first 最小下載順序（作者授權後才執行；目前不下載）
1. **只下載 protocol/metadata**，不下載 audio；
2. 完成 generator + speaker/content + source-corpus + license + **backbone-pretraining** lineage manifest；
3. 用 **MLAAD-tiny 或極小公開 subset** 驗 pipeline（plumbing）；
4. 過 gate 後才抓 **primary 所需 shards**（不預設全量 142.3GB）；
5. **大型 fallback 只在 primary 失敗時下載。**

## 8. 使用的指標
- **Primary endpoint**：`L_CR,m,g=P(accept∧ŷ=real|y=fake,g)`；`L_CR^macro=(1/|G|)Σ_g L_CR,g`。
- **Primary comparative**：`Δ_light`（§5，teacher-relative）。
- **Policy 聯合報告**：overall/fake/bona-fide coverage、FPR、selective risk、人工複核比例。
- **Ranking 診斷**：AURC、eAURC、error-AUROC、AUROC、EER、risk-coverage、accepted-set disagreement、Kendall τ / Spearman ρ。
- **Calibration control**：ECE、Brier、NLL、reliability diagram（TS/Platt 僅此，不作 repair）。
- **部署**：param count、model size、peak RAM、CPU latency、RTF、feature+selector overhead。
- **不確定性**：family bootstrap / hierarchical interval，**每次 bootstrap 重跑完整 policy fitting**（抽 dev→校準→selector→選 t→選 q→評 target）；~7 families → practical margin + bounded claim，不用 utterance-level p 值宣稱普遍性。

## 9. 資料切分（防洩漏）
A model-train ｜ B selector-train（**out-of-fold** correctness/cluster）｜ C policy-dev（校準 + `(q_m,t_m)` + 驗 source constraint）｜ D exploratory target（In-the-Wild/DFADD，僅 smoke test，不選方法/不調參/不改 endpoint）｜ E confirmatory target holdout（ASVspoof 5 subset，只做一次 final eval，不 target-label tuning）。

## 10. Phase-0 derisking 稽核（修正）
- **0.0** 環境 + 復現 **lineage-clean teacher**（非 XLS-R，見 §6），source eval 對上論文級 EER。
- **0.1（H1a 便宜首探）** 截短 probe（不訓練）+ `u0` 凍結 `(q_m,t_m)`；**In-the-Wild 僅 smoke test**（看 pipeline 與粗訊號，**不作正式 kill**）。
- **0.2（H1a confirmatory）** ASVspoof 5 C00 subset（family-macro `Δ_light`）；前置：§6 blocker 解 + lineage manifest 過 + 作者授權下載。
- **0.3（H1b）** (i) toy-logit invariance 確認；(ii) 測 §11 的 rank-changing repair shortlist（TS/Platt 僅 control）。
- **Phase 1** 僅 H1a 成立 + H1b 不足才做：由診斷導出 H2 → closest-work gate → 同 student/budget 對決。

## 11. Baselines（預先登記，所有調參只用 source）
frozen **lineage-clean teacher** ｜ truncated probe ｜ ordinary KD ｜ **H1b rank-changing repair shortlist**：normalized-margin / student-embedding Mahalanobis 或 ViM / confidence+OOD composite（SIRC 類；納入 TMLR 2024 generic SC 中適用 binary ADD 者）｜ cluster-conditional recalibration（**僅當 target inference 能無標籤決定 cluster/router 才合法**）｜ TS/Platt（probability-calibration control，已證 no-op）｜（gates 過後）H2。所有方法計 deployment cost。

## 12. Contribution contract（可守貢獻）
1. **replication**：忠實重現最近 lightweight/calibration-aware KD baselines；
2. **evaluation**：source-frozen、lineage-audited、generator-family-macro 的 external selective-policy transfer protocol；
3. **diagnostic**：區分 discrimination / score ordering / operating-point transfer / calibration 的失效來源；
4. **conditional incremental-method**：僅 H2 打贏強 source-only rank-changing repair 才成立；
5. **useful negative result**：H1a null 或便宜 repair 足夠時，留下對 edge ADD 評估規格的 bounded audit（但依作者設定不視為已達方法 bar）。

## 13. 一年範圍
做：一 source 設定、一 primary confirmatory holdout、一 teacher + 一~二 lightweight transformation、一 H2 機制、score/family-level 主分析、三態 + latency 可行的 reference model card。
不做：多 backbone 大矩陣、uncertainty 排行榜、手機 App/完整瀏覽器產品、human-subject study、多語全面泛化、partial deepfake、對抗攻擊、foundation model 預訓練、任何 target-label 調參。

## 14. Kill / Pivot
Kill：找不到 lineage-clean teacher/holdout；matched discrimination 後 `Δ_light` 無實質差異（Cattelan & Silva NeurIPS2023W：修正 confidence estimator 後 selective 退化可能由 accuracy 解釋 → **H1a 可能 null，早停 gate 必留**）；強 generic rank-changing repair 已足夠；H2 撞題；需 target labels/完整 teacher inference 才有增益；families/clusters 不足。
Pivot：方法空間消失 → 降為 replication/external audit，回候選方向（#4/#5）比較；不事後更名 loss 製造 novelty。

## 15. 算力（單張 RTX 4090, 24GB）
Phase-0 推論 + 截短 probe，幾十 GPU-h；全論文核心（H2 一 student + baselines）遠低於 500 GPU-h；frozen backbone + 特徵快取 + 分層抽樣。

## 16. 誠實風險聲明
1. 貢獻 bar 押在 H2 打贏**強 rank-changing repair**（非 no-op TS），未 derisk。
2. H1a 可能 null（matched accuracy 後 selective 退化可能消失）——早停 gate 必留。
3. 方法 novelty 窄且高拆解風險；H2 唯一活路＝由 H1a 診斷導出 + 過 closest-work + ADD-specific hook（confident-real false-negative）。
4. ~7 generator families 檢定力有限。
5. **XLS-R blocker 未解前，ASVspoof 5 confirmatory 不可用。**
6. 學校對 replication-plus-extension 型碩論的行政/口試門檻未知，須指導教授確認。
7. **參考文獻待查**：Kwok（venue/題名可能 ICASSP vs Interspeech 不一致）、Zhou & Wang 完整題名、Xu ICPR 2020（作者/DOI 待補）——交 Codex 核。

## 17. 現況與下一步
- **決策**：題目 GO（Selective-Policy Transfer）；實驗 CONDITIONAL GO。
- **Claude 下一步**：把 `u0/u1/q/t/α/β/δ/ε` 寫成 executable protocol + toy 驗證（base policy、TS/Platt invariance、rank-changing repair、joint policy fitting）；列 2–3 個 lineage-clean backbone 候選交 Codex 查。
- **Codex 進行中/待辦**：ASVspoof 5 generator+speaker/content+**backbone-pretraining** lineage manifest（延伸 `2026-07-18-1030`）；XMAD-Bench license+confound+overlap audit（使其成真實 fallback）；核 §16.7 三筆 citation。
- **待作者**：(a) 寫入 DECISIONS.md（§18）；(b) 指導教授確認貢獻 bar；(c) 授權 protocol-only 下載（依 §7.5，**不授權全量/pilot/訓練**）。
- **暫停中**：142.3GB 全量下載、full pilot、student/H2 訓練。

## 18. 建議作者寫入 DECISIONS.md 的條目（agent 不代寫）
> **2026-07-18 — Select selective-policy transfer for lightweight audio deepfake detection as the final working thesis direction.**
> The thesis will test whether a source-frozen accept/abstain/classification policy survives lightweight model transformation on documented lineage-disjoint unseen generators. The intended contribution is a rigorous replication and external-validity protocol plus, only if the H1a and H1b gates justify it, a diagnosis-driven incremental method that beats strong source-only rank-changing baselines under matched discrimination and deployment budgets. Critical-path datasets must be direct-download (no application/eligibility/hidden labels); ASVspoof 5 is primary confirmatory pending a lineage-clean backbone, with XMAD-Bench as an audited newer fallback. Human-subject evaluation, adaptive attacks, partial deepfakes, and foundation-model pretraining are excluded. Phase 0 remains gated on advisor approval, an executable policy specification, a lineage-clean teacher/holdout pair, and authorized data access.

## 19. 關鍵前作（★=待 Codex 核）
量測/可靠性：Salvi (ICASSP 2023)、Pascu (Interspeech 2024)、FADEL (ICASSP 2025)、★Zhou & Wang (arXiv 2606.21584)、Schäfer & Steinebach (ICWSM 2026)、★Kwok。
輕量/壓縮 ADD：DK-CAST (Discover Computing 2025)、FTDKD (TASLP 2024)、Edge/browser (arXiv 2606.30780)。
壓縮×可靠性：Zhong (ACL 2025)、DistilDoc (ICDAR 2024)、Mitra (CVPRW 2024)、KD(C) (ACCV 2024)、BN3 (CVPR 2021)、EnD² (NeurIPS 2021)、Kim (Interspeech 2021)、Niu (NeurIPS 2022)、★Xu (ICPR 2020)。
selective classification / shift：El-Yaniv (JMLR 2010)、SelectiveNet (ICML 2019)、Liang-Peng-Sun (TMLR 2024)、Cattelan & Silva (NeurIPS 2023 W)、Selective Classification under Distribution Shifts (arXiv 2405.05160)。
校準/單調：Guo (ICML 2017)、Ovadia (NeurIPS 2019)、Multi-domain TS (NeurIPS 2022)、TransCal (NeurIPS 2020)、Gong (ICCV 2021)。
資料集：ASVspoof 2019 LA、ASVspoof 5 (arXiv 2502.08857)、XMAD-Bench (arXiv 2506.00462)、DFADD (arXiv 2409.08731)、In-the-Wild、MLAAD-tiny。
