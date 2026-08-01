# 碩士論文計畫書（完整版）

> 整合 plan v3 共識 + Codex 三項查證（backbone lineage、ASVspoof5/XMAD manifest、citation audit，2026-07-18）。此為給作者的完整計畫書；正式定題由作者寫入 DECISIONS.md，下載/pilot/訓練仍暫停。

---

## 1. 論文題目

**中文**：未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留

**英文**：Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators

---

## 2. 論文概述

音訊深偽（audio deepfake）偵測器正被壓縮、蒸餾、放進瀏覽器與 edge 裝置，讓一般大眾、記者與事實查核者能**本機、低成本、離線**檢查可疑語音。但現行輕量化研究幾乎只用 EER、AUROC、延遲與模型大小證明「模型仍然能分辨真假」，忽略了真實部署的核心問題：**模型縮小後，那條在開發階段就固定下來的「接受／棄權／判定」決策規則（selective policy），遇到訓練時沒見過的新生成器，還守不守得住？**

本論文把此問題形式化為 **source-frozen selective-policy transfer**：分類門檻 `t` 與棄權門檻 `q` 僅由 source 開發資料決定並凍結，部署到 documented lineage-disjoint 的未見生成器時，其「把假語音高信心判成真人」的風險（confident-real leakage）是否仍守在事先承諾的上限內。研究採三段式 kill sequence：(H1a) 驗證輕量化是否造成**超出 teacher 自身失效之外**的額外策略退化；(H1b) 驗證便宜的 source-only rank-changing 修法是否救不回；(H2，條件性) 若前兩關成立，提出一個由失效診斷導出、且打贏強修法基線的保留方法。一個已用數值驗證的理論起點是：**純量後驗校準（temperature scaling / Platt）對 rank-based policy 是可證明的 no-op**，因此真正需要的是會改變樣本排序／決策幾何的機制。

貢獻定位為 **replication + external-validity protocol + 診斷**，只有 H2 打贏強基線時才主張方法貢獻；全程單張 RTX 4090、不做真人實測、不用 target labels 調參。

---

## 3. 研究背景

1. **deepfake audio 製造門檻極低、語音詐騙氾濫**，正侵蝕人們對電話、語音訊息與新聞的信任。
2. **兩條現有防線各有硬極限**：
   - *被動偵測（passive detection）*：面對未見／閉源生成器，泛化能力大幅下降（VoiceWukong 顯示 SOTA EER 從 <1% 升到 13.5%+，部分接近隨機）。
   - *密碼學溯源（C2PA）*：只能證明「內容未被竄改」，不能證明「非 AI 生成」，且對不附憑證的惡意 deepfake 零覆蓋。
3. **偵測器的部署形態正在改變**：從雲端大模型走向本機／edge／瀏覽器輕量模型（DK-CAST、FTDKD、2026 瀏覽器外掛），因為隱私、成本與可用性使雲端方案不適合一般大眾。
4. **真實部署使用的是「凍結的操作點」**：部署系統不能用 target 測試標籤重新選 EER 最佳門檻；它用的是開發階段就固定的分類與棄權門檻（Schäfer & Steinebach, ICWSM 2026 實證：預設門檻比 test-derived 門檻更符合現實，且效能可從 F1 91% 掉到 65%）。

---

## 4. 研究動機

**動機鏈（把個人動機與技術貢獻接在同一條因果鏈）**：

> 希望讓 ADD 更能被大眾／記者安全使用 → 必須本機、低成本 → 必須輕量化 → 輕量化不能只看 EER → 必須研究「凍結的選擇策略」是否被破壞、能否保留。

**部署情境（暫定）**：記者／事實查核者的本機初篩。三態輸出——`發現合成證據`（送人工複核）／`未發現合成證據`（**不等於**已驗證真人）／`證據不足，棄權`（強制升級人工或帶外查核，不靜默放行）。棄權後有明確承接動作，比向大眾直接承諾真假裁決更符合偵測器能力邊界。

**明確不主張**：不驗證說話者身分、不涵蓋 adaptive attack／partial deepfake／多語全面泛化；無真人實測，故不宣稱降低受騙率／社會風險。

---

## 5. 當前痛點

1. **輕量化評估只看辨識力**：EER／AUROC／延遲說明「能分」，但**沒有回答「模型知不知道自己何時不該判斷」**。
2. **凍結門檻的隱性失效**：即使 teacher 與 student 的 AUROC 相近，壓縮／截層可能平移 score scale，使開發集凍結的門檻在新生成器上**過度自信地把 fake 判成 real**——這正是危害最大的「確定的錯誤」。
3. **teacher 自身也會在 shift 下失效**：直接比較 student 與 teacher 在 target 的 leakage，**混淆了「輕量化造成的退化」與「teacher 本來就會失效」**——痛點是缺乏能隔離兩者的量測。
4. **便宜校準修不了排序問題**：實務上第一直覺是「重新校準機率」（temperature scaling），但它在 rank-based policy 上是數學上的 no-op（本研究已數值驗證），無法修復排序型的策略失效。
5. **資料集與 lineage 陷阱**：多數評估未控制「偵測器的預訓練語料是否看過測試集的上游語者」，一旦重疊，「未見生成器」的宣稱失效。

---

## 6. 先前研究

**(a) ADD 可靠性、校準與部署**：Salvi (ICASSP 2023) 做 reliability estimation；Pascu (Interspeech 2024) 做跨資料集泛化與 calibration；FADEL (ICASSP 2025) 用 evidential uncertainty；Kwok (ICASSP 2025) 做 ensemble confidence calibration、Kwok (Interspeech 2025) 揭露 bona-fide cross-testing 弱點；**Zhou & Wang (arXiv 2606.21584)「When EER Hides Deployment Failure」直接稽核 threshold transfer 與 unlabeled score calibration**；Schäfer & Steinebach (ICWSM 2026) 證明預設門檻在社群資料上的落差。

**(b) 輕量／壓縮 ADD**：DK-CAST (Discover Computing 2025) codec-aware 蒸餾；FTDKD (TASLP 2024) 壓縮音訊的頻時域蒸餾；Detecting Audio Deepfakes on the Edge (arXiv 2606.30780) 截短 SSL + 瀏覽器外掛。

**(c) 壓縮×可靠性（跨領域）**：Zhong (ACL 2025) 量化 LLM 的 calibration gap；DistilDoc (ICDAR 2024) 顯示壓縮後 accuracy 與 AURC/ECE 脫鉤；Mitra (CVPRW 2024) 反證 pruning 不必然傷 calibration；KD(C) (ACCV 2024) calibrated-teacher→calibrated-student；BN3 (CVPR 2021)、EnD² (NeurIPS 2021)、Kim (Interspeech 2021, ASR uncertainty-matching KD) 為 uncertainty-preserving compression 先例。

**(d) selective classification / distribution shift**：El-Yaniv (JMLR 2010) risk-coverage 理論；SelectiveNet (ICML 2019) learned reject；Liang-Peng-Sun (TMLR 2024) generic rank-changing SC 分數（Energy/KNN/ViM/SIRC）；Cattelan & Silva (NeurIPS 2023 W) 顯示修正 confidence estimator 後 selective 退化可能由 accuracy 解釋；Xu, Pu & Zhao (ICPR 2020/2021) KD + abstention 組合。

**(e) 校準與 shift**：Guo (ICML 2017) temperature scaling；Ovadia (NeurIPS 2019) post-hoc 校準在 shift 下退化；Multi-domain TS (NeurIPS 2022)、TransCal (NeurIPS 2020)、Gong (ICCV 2021) shift-aware calibration。

---

## 7. 基於先前研究發現的問題與可改進的點

| 先前研究已做 | 發現的問題 / gap | 本研究改進 |
|---|---|---|
| Zhou & Wang 稽核 classification threshold transfer | 只處理**分類門檻**，未含**棄權門檻**與 selective policy；未在輕量化模型上做 | 加入 `q`（abstention）+ source-frozen selective **policy**，並比較 teacher vs 輕量 student |
| DK-CAST/FTDKD/edge 做輕量 ADD | 只報 EER/延遲，**未量壓縮後的 selective reliability / threshold transfer** | 建立 source-frozen、lineage-audited、family-macro 的 external policy transfer protocol |
| Pascu/FADEL 做 full-model 可靠性 | 在**完整模型**上，未觸及壓縮的交互 | 研究輕量化「額外」造成的策略退化 |
| KD(C)/Kim/EnD² 做 reliability-preserving 壓縮 | 均為**通用**方法，非 ADD-specific，未針對「未見生成器的 external selective-policy transfer」 | H2 由失效診斷導出、針對 confident-real 不對稱危害、過 closest-work gate |
| generic SC 已有 rank-changing 分數 | 未在 ADD × 輕量化 × 未見生成器組合下驗證是否足夠 | 把它們設為**強 H1b 修法基線**，H2 必須打贏 |
| 直接比較 student/teacher target leakage | **混淆**輕量化退化與 teacher 自身失效 | **teacher-relative double-difference `Δ_light`** 隔離兩者 |
| 便宜校準被當作修法 | temperature scaling 對 rank-based policy 是 **no-op（本研究數值證明）** | 降為 control，改用會改排序的 source-only 修法 |
| 常忽略 backbone 預訓練污染 | 偵測器預訓練可能看過測試集上游語者 | 只用 **LibriSpeech-960-only backbone**（符合 ASVspoof 5 規則），逐層 lineage manifest |

**可守的殘餘 gap（bounded wording）**：在已記錄搜尋範圍內，未見同時研究「lightweight ADD × documented lineage-disjoint unseen generators × source-frozen selective-policy transfer + teacher-relative 隔離 + 排序型修法基線」者。**不主張發明 KD/calibration/abstention。**

---

## 8. 改進方法（方法論）

### 8.1 核心設計
- raw score `s(x)∈ℝ`（fake 方向為正）；分類 `ŷ=1[s(x)≥t_m]`。
- **H1a base selector**：`u0(x)=|s(x)−t_m|`（decision-margin，非 rank-changing）；`accept ⇔ u0≥q_m`。
- **H1b repair selector**：`u1(x)=h(s(x), z_student(x))`（rank-changing，`z_student` 取自**部署中的 student**，不得需要完整 teacher inference；selector 的參數/latency/RAM 計入部署預算）。**須以 Kendall τ / accepted-set disagreement 實測確認 u1 真的改變 accepted set。**
- **α 進 policy（UCB 約束，不只事後比較）**：
  ```
  (q_m,t_m)=argmax Coverage_dev(q,t)
    s.t. UCB_{1-δ}[L_CR,dev(q,t)]≤α  且  FPR_real,dev(q,t)≤β
  ```
  無可行 policy → 輸出「無法承諾」（no-feasible-policy fallback）。**主 endpoint 與 coverage、人工複核比例聯合約束**（防「全棄權」作弊）。

### 8.2 主 comparative estimand（隔離輕量化額外損失）
```
G_m     = L_CR^target − L_CR^source        (每模型 transfer gap；source 分量用 held-out source)
Δ_light = G_student − G_teacher             (輕量化額外退化；per-family Δ_light,g 再 family-macro)
```
並列報 per-family `G_student, G_teacher` 分量以求透明。

### 8.3 單調等價的處置（已數值驗證）
TS/Platt(a>0) + 門檻依同一 source rank 約束重選 → target 決策**完全不變**（toy 驗證：diffs=0）；固定語意門檻不重選才會變（diffs=4252）。**含義**：純量校準原理上修不了 rank-based selective-policy transfer → TS/Platt 僅作 control，primary 修法必須 rank-changing。

### 8.4 H2 機制（不預先 pin，由 H1a 診斷導出）
候選 family（過 closest-work gate 後才定案）：error-aware policy-preserving distillation
```
L = L_CE + λ_KD·L_KD + λ_rank·L_correctness-rank + λ_cons·L_codec-consistency
```
- `L_correctness-rank`：讓 selection score 把 student 的正確樣本排在錯誤之前，**特別處理 confident-real false negatives**（ADD 不對稱危害特有的 hook，非通用 confidence imitation）。
- `L_codec-consistency`：clean/codec/resampling 擾動下 selection ranking 穩定。
- component 權重/ablation 優先序由 H1a 失效診斷決定；不在 target 結果出來後臨時創造新 loss。

### 8.5 Teacher backbone（lineage-clean，已查證）
| 選項 | checkpoint | 預訓練 | ASVspoof5 合規 |
|---|---|---|---|
| **首選** | `facebook/wav2vec2-base` | LibriSpeech-960 only | PASS（plan 明文允許 LibriSpeech） |
| 替代1 | `facebook/hubert-base-ls960` | LibriSpeech-960 | PASS |
| 替代2 | `microsoft/wavlm-base` | LibriSpeech-960 | PASS |
| **禁用** | XLS-R / wavlm-base-plus / *-ll60k | 含 MLS / LibriLight | **FAIL**（與 eval 上游重疊） |
> 只解 base backbone；完整 teacher 仍須固定 `model id→revision→SHA-256→fine-tuning corpora→augmentation→holdout overlap`，且過 teacher quality gate。先只實作 wav2vec2-base，quality gate 失敗才切換。

---

## 9. 實驗設計

### 9.1 資料切分（防洩漏，五分）
A model-train｜B selector-train（**out-of-fold** correctness/cluster）｜C policy-dev（校準 + `(q_m,t_m)` + 驗 source 約束）｜D exploratory target（In-the-Wild/DFADD，**僅 smoke test**，不選方法/不調參/不改 endpoint）｜E confirmatory holdout（ASVspoof 5 C00 subset，只做一次 final eval）。

### 9.2 資料集（角色 + 免申請 hard gate）
| 角色 | 資料集 | 存取 | 關鍵事實 / 前置 |
|---|---|---|---|
| source anchor | ASVspoof 2019 LA | A 直接 | attack 偏舊；ODC-By |
| **primary confirmatory** | **ASVspoof 5 C00 selected subset** | A（Zenodo，protocol 已下載 20.7MB，MD5 PASS） | **7 architecture families**（A17, A21+A22 合併, A24, A25, A26, A28, A29）；**selected spoof 69,233 / bona fide 35,149**；**A17 speaker overlap <2% → 報含/不含 A17**；**A29(XTTS) 上游含 LibriLight → 標 caveat，不宣稱全 attack lineage-disjoint**；shortcut probes **PENDING** |
| newer fallback（條件式） | **XMAD-Bench** | A | **只作 compound-shift fallback**（cross-domain 同時改 source+speaker+generator，非 generator-isolated）；**license 不一致**（CC BY-NC-SA vs Apache）；**M-AILABS 與 LibriSpeech 同 LibriVox lineage → 英/德/俄/西 slice 未清；Arabic/Mandarin/Romanian 較安全但改語言** |
| exploratory replication | DFADD（pinned corrected release） | A | LJSpeech/VCTK shortcut；不作唯一 confirmatory |
| plumbing only | MLAAD-tiny | A | 僅驗 pipeline |
| 排除 | 完整 MLAAD（B 帳號）、AUDETER（1.08TB）、RADAR/challenge-gated（C） | — | — |

**Hard gate**：critical-path 資料集必須直接下載（免申請/資格/隱藏 labels）；先過 access/license/lineage/confounding/feasibility gate，才以新近性排序。**Primary→Fallback 切換**：ASVspoof5 找不到 lineage-clean teacher→切已 audit 的 XMAD compound-shift；XMAD 混淆/license 無法解→維持 secondary；任一變 C 級/連結失效→立即切、不等待。**Protocol-first 下載順序**：metadata→lineage manifest→MLAAD-tiny 驗 pipeline→過 gate 才抓 primary shards→fallback 只在 primary 失敗。

### 9.3 baselines（預先登記，調參只用 source）
frozen lineage-clean teacher｜truncated probe｜ordinary KD｜**H1b rank-changing 修法 shortlist**（normalized-margin / student-embedding Mahalanobis 或 ViM / SIRC 類 confidence+OOD composite）｜cluster-conditional recalibration（僅當 target inference 能無標籤決定 cluster 才合法）｜TS/Platt（control，已證 no-op）｜（gates 過後）H2。所有方法計 deployment cost。

### 9.4 Phase-0 derisking 稽核（越前面越便宜）
- **0.0** 環境 + 復現 wav2vec2-base teacher，source eval 對上論文級 EER。
- **0.1** 截短 probe（不訓練）+ u0 凍結 `(q_m,t_m)`；In-the-Wild **僅 smoke test**（不作正式 kill）。
- **0.2** ASVspoof 5 C00（family-macro `Δ_light`）；前置：teacher full-lineage manifest + 作者授權下載 + shortcut probes 通過。
- **0.3** (i) toy-logit invariance 確認；(ii) 測 rank-changing 修法 shortlist；TS/Platt 僅 control。
- **Phase 1** 僅 H1a 成立 + H1b 不足才做：由診斷導出 H2 → closest-work gate → 同 student/budget 對決。

---

## 10. 需要使用的參數：簡介與如何判別

| 參數 | 簡介 | 如何判別 / pass 準則 |
|---|---|---|
| `s(x)` | raw scalar score（fake 方向為正） | 由 teacher/student 輸出；用於分類與 selection |
| `t_m` | 模型 m 的 fake/real 分類門檻 | 由 source-dev 的 `FPR≤β` 決定並凍結；模型各自擬合，**不套 teacher 門檻** |
| `q_m` | 接受/棄權門檻 | 由 source-dev coverage 最大化 + `UCB(L_CR)≤α` 決定並凍結 |
| `α` | 可接受的 confident-real leakage 上限（風險承諾） | 進 policy 約束（非事後）；holdout 上 `L_CR^macro>α` 即 external violation |
| `β` | 可接受的 bona-fide FPR 上限 | source-dev 約束；防止用高誤報換低 leakage |
| `δ` | 風險估計的信心水準 | 用單尾信賴上界 `UCB_{1-δ}`，非點估計，避免樂觀偏誤 |
| `ε` | H1a 的具部署意義最小退化量 | `Δ_light>ε` 才算 H1a 成立（非只 `>0`、非 utterance p 值）；`ε` 預先定義 |
| `u0(x)=\|s−t_m\|` | H1a base selector（decision-margin） | H1a 用；不 rank-changing |
| `u1(x)=h(s,z_student)` | H1b rank-changing 修法 selector | 須以 Kendall τ / accepted-set disagreement **實測**確認真的改排序；student 端可廉價推論 |
| `L_CR,g` | family g 的 confident-real leakage `P(accept∧real\|fake,g)` | **主 endpoint**；越低越好，但須與 coverage 聯合看（防全棄權） |
| `G_m` | 模型 transfer gap `L_CR^target−L_CR^source` | 中介量；source 分量用 held-out source 估 |
| `Δ_light=G_student−G_teacher` | 輕量化**額外**退化 | **主 comparative estimand**；隔離 teacher 自身失效；per-family + family-macro |
| coverage（overall/fake/bona-fide） | 接受比例 | 聯合約束/報告；防「全棄權也低 leakage」 |
| AUROC / EER | 辨識力（排序） | **matching 變數**（配平 teacher/student 用預宣告 equivalence tolerance） |
| eAURC / error-AUROC | selective ranking 品質 | **secondary diagnostic，不作 matching 變數**（避免 circular） |
| ECE / Brier / NLL | 機率校準品質 | control（TS 改善這些但不改排序，故不作 repair） |
| 部署量（param/size/RAM/latency/RTF） | 部署預算 | matching 變數；selector overhead 計入 |

**判別邏輯總綱**：先用 budget + AUROC/EER 配平（排除「只是模型較好」）→ 看 `Δ_light` 是否 > `ε`（H1a）→ 看 rank-changing 修法能否把 `Δ_light` 壓回 non-inferiority margin（H1b）→ H2 是否在同預算下打贏最強修法（方法貢獻）。全程 family bootstrap（每次重跑完整 policy fitting），以 practical margin + family interval 表述，不用 utterance p 值宣稱普遍性。

---

## 11. 預計研究成果與推測原因

**預期主結果（可否證，非既定）**：

1. **H1a 預期成立、但誠實承認可能 null**——輕量 student 在 matched discrimination 下，未見生成器的 family-macro `Δ_light > ε`；頭號可引用數字：**`ΔEER≈0 但 Δ_light>0`**。
   - *推測原因*：Zhong (ACL 2025)、DistilDoc (ICDAR 2024) 顯示壓縮後 accuracy 與 calibration/排序脫鉤，`s` 的絕對尺度平移會使凍結門檻在新分佈上失準；且 confident-real 是不對稱危害，壓縮的邊界幾何改變最先傷到它。
   - *可能 null*：Mitra (CVPRW 2024) 反證 pruning 不必然傷 calibration；Cattelan & Silva (NeurIPS 2023 W) 顯示修正 confidence estimator 後 selective 退化可能由 accuracy 解釋——故保留早停 gate。

2. **H1b 預期：純量校準 no-op（確定）；rank-changing 修法能否救回未知**。
   - *推測原因*：temperature scaling 對 rank-based policy 是數學 no-op（本研究已證）；Ovadia (NeurIPS 2019)、Multi-domain TS (NeurIPS 2022) 顯示 source-only post-hoc 校準在 shift 下常不足 → 便宜修法**傾向**救不回（對我們有利），但無保證，須實測。

3. **H2 預期（若前兩關成立）**：由診斷導出的機制在 matched budget 下把 `Δ_light` 壓到低於最強 rank-changing 修法，且增益來自機制本身（ablation 證明，非模型變大/更多資料/target tuning）。
   - *推測原因*：generic 修法只重排分數、不改變 student 對「自身錯誤」的表徵；針對 confident-real false-negative 的 correctness-rank + codec-consistency 蒸餾，理論上能把 teacher 的「錯誤自覺」與抗通道穩定性傳給 student。**但這是本計畫最未 derisk 的一關。**

**結果決策樹**：
- H1a null（matched 後無退化）→ 早停，省下大檔；重估。
- H1a 成立、rank-changing 修法已救回 → kill H2；成果＝external-validity 評估（偏量測，低於作者方法 bar）→ 回候選題。
- H1a 成立、修法不足、H2 打贏 → **達 bar 的方法貢獻** + edge ADD 評估標準修正 + 三態 model card。
- H2 打不贏 → 誠實降為 replication/external audit + negative result，回候選題（不改 loss 名製造 novelty）。

**有用的負結果**：即使 EER 保留，輕量化系統性破壞 fixed-policy transfer、且哪種 source-only 修法能/不能跨 generator 轉移——對 edge ADD 評估實務是具體、可引用的修正。

---

## 12. 參考文獻

**ADD 可靠性/校準/部署**
- C. Y. Kwok, D.-T. Truong, J. Q. Yip. "Robust Audio Deepfake Detection using Ensemble Confidence Calibration." ICASSP 2025, pp.1–5. DOI:10.1109/ICASSP49660.2025.10889972.
- C. Y. Kwok, J. Q. Yip, Z. Qiu, C. H. Chi, K. Y. Lam. "Bona fide Cross Testing Reveals Weak Spot in Audio Deepfake Detection Systems." Interspeech 2025, pp.2230–2234. DOI:10.21437/Interspeech.2025-172.
- J. Zhou, M. Wang. "When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors." arXiv:2606.21584 v1 (2026-06-19, preprint). DOI:10.48550/arXiv.2606.21584.
- Schäfer & Steinebach. "Reality Check: … Audio Deepfake Detectors on Social Media Data." ICWSM 2026.
- Salvi et al. "Reliability Estimation for Synthetic Speech Detection." ICASSP 2023.
- Pascu et al. "Towards Generalisable and Calibrated Audio Deepfake Detection with Self-Supervised Representations." Interspeech 2024.
- FADEL. "Uncertainty-aware Fake Audio Detection with Evidential Deep Learning." ICASSP 2025 / arXiv:2504.15663.

**輕量/壓縮 ADD**
- DK-CAST. "Dynamic Knowledge Condensation with Audio-Selective Transformer for Audio Deepfake Detection." Discover Computing 2025. DOI:10.1007/s10791-025-09746-4.
- FTDKD. "Frequency-Time Domain Knowledge Distillation for Low-Quality Compressed Audio Deepfake Detection." IEEE/ACM TASLP 2024.
- "Detecting Audio Deepfakes on the Edge: Lightweight SSL-Based Detection in a Browser Plugin." arXiv:2606.30780.

**壓縮×可靠性（跨領域）**
- Zhong et al. "Quantized Can Still Be Calibrated…" ACL 2025.
- DistilDoc. ICDAR 2024. arXiv:2406.08226.
- Mitra et al. "Investigating Calibration and Corruption Robustness of Post-hoc Pruned Perception CNNs." CVPRW 2024.
- Hebbalaguppe et al. "Calibration Transfer via Knowledge Distillation." ACCV 2024.
- Cui et al. "Bayesian Nested Neural Networks…" CVPR 2021.
- Ryabinin et al. "Scaling Ensemble Distribution Distillation…" NeurIPS 2021.
- Kim et al. "Multi-Domain KD via Uncertainty-Matching for E2E ASR." Interspeech 2021.

**selective classification / shift / KD+abstention**
- El-Yaniv & Wiener. "On the Foundations of Noise-free Selective Classification." JMLR 2010.
- Geifman & El-Yaniv. "SelectiveNet…" ICML 2019.
- Liang, Peng & Sun. (generalized selective classification, rank-changing scores). TMLR 2024.
- Cattelan & Silva. (matched-accuracy selective performance). NeurIPS 2023 workshop.
- Y. Xu, J. Pu, H. Zhao. "Knowledge Distillation with a Precise Teacher and Prediction with Abstention." ICPR 2020 (pub. 2021), pp.9000–9006. DOI:10.1109/ICPR48806.2021.9412696.

**校準 / distribution shift**
- Guo et al. "On Calibration of Modern Neural Networks." ICML 2017.
- Ovadia et al. "Can You Trust Your Model's Uncertainty?" NeurIPS 2019.
- "Robust Calibration with Multi-domain Temperature Scaling." NeurIPS 2022.
- "TransCal: Transferable Calibration…" NeurIPS 2020.
- Gong et al. "Confidence Calibration for Domain Generalization Under Covariate Shift." ICCV 2021.

**Backbone**
- Baevski et al. "wav2vec 2.0." NeurIPS 2020（`facebook/wav2vec2-base`, LibriSpeech-960）。
- Hsu et al. "HuBERT." 2021（`facebook/hubert-base-ls960`）。
- Chen et al. "WavLM." 2021（`microsoft/wavlm-base`）。

**資料集**
- ASVspoof 2019 LA. arXiv:1911.01601.
- ASVspoof 5. arXiv:2502.08857（Zenodo 14498691, ODC-By 1.0）。
- XMAD-Bench. arXiv:2506.00462（CC BY-NC-SA 4.0，license metadata 待釐清）。
- DFADD. arXiv:2409.08731（MIT）。
- In-the-Wild. arXiv:2203.16263。
- MLAAD / MLAAD-tiny（CC BY-NC 4.0）。

> 標註：Zhou & Wang 目前為 arXiv preprint（定稿時重查發表狀態）；Kwok 為兩篇不同論文（依主張分引）；Xu 為視覺領域 KD+abstention，非 ADD 直接先例。
