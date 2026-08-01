# D1-A 完整語音版｜碩士論文計畫書（proposal-final）

> 本文為候選方向 D1-A 的完整計畫書。母本為 `discussions/legacy/2026-07-18-thesis-proposal-final.md`，已依 `research/validations/2026-07-23-...-audit.md` 與 `2026-07-18-final-topic-assessment-...md` 之查證修正重排為 12 節結構。所有 novelty 主張採 bounded wording，僅指「在已記錄搜尋範圍（2026-07）內未找到直接同題先作」。計畫書階段：第 8.4「預期結果」與第 9「結果分析與討論」以預期／推估、結果表骨架與假設性推論呈現，不含實測數值。正式定題、資料下載與訓練仍待作者裁定。

---

## 1. 論文題目

**中文**：未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留

**英文**：Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators

---

## 2. 研究背景

音訊深偽（audio deepfake）的製造門檻極低，語音詐騙與假語音訊息正侵蝕大眾對電話、語音訊息與新聞的信任。現有兩條防線各有硬極限：被動偵測（passive detection）面對未見／閉源生成器時泛化能力大幅下降（VoiceWukong 顯示 SOTA EER 由 <1% 升至 13.5%+，部分接近隨機）；密碼學溯源（C2PA）只能證明內容未被竄改，不能證明非 AI 生成，且對不附憑證的惡意 deepfake 零覆蓋。

同時，偵測器的部署形態正從雲端大模型走向本機／edge／瀏覽器輕量模型（DK-CAST、FTDKD、2026 瀏覽器外掛），因為隱私、成本與可用性使雲端方案不適合一般大眾、記者與事實查核者的本機初篩。真實部署使用的是**開發階段就固定的操作點**：部署系統不能用 target 測試標籤重新選 EER 最佳門檻，只能用開發階段凍結的分類與棄權門檻。Schäfer & Steinebach（ICWSM 2026）實證：預設門檻比 test-derived 門檻更符合現實，且效能可從 F1 91% 掉到 65%。

---

## 3. 當前領域問題與痛點

1. **輕量化評估只看辨識力**：EER／AUROC／延遲能說明「模型能分真假」，但未回答「模型知不知道自己何時不該判斷」。
2. **凍結門檻的隱性失效**：即使 teacher 與 student 的 AUROC 相近，壓縮／截層可能平移 score scale，使開發集凍結的門檻在新生成器上過度自信地把 fake 判成 real——這正是危害最大的「確定的錯誤」（confident-real leakage）。
3. **teacher 自身也會在 shift 下失效**：直接比較 student 與 teacher 在 target 的 leakage，會混淆「輕量化造成的退化」與「teacher 本來就會失效」；痛點是缺乏能隔離兩者的量測。
4. **便宜校準修不了排序問題**：實務第一直覺是重新校準機率（temperature scaling），但在特定條件下它對 rank-based policy 是 no-op，無法修復排序型的策略失效。
5. **資料集與 lineage 陷阱**：多數評估未控制偵測器預訓練語料是否看過測試集上游語者，一旦重疊，「未見生成器」的宣稱即失效。

---

## 4. 研究動機

**動機鏈**（把個人動機與技術貢獻接在同一條因果鏈）：

> 希望讓 ADD 更能被大眾／記者安全使用 → 必須本機、低成本 → 必須輕量化 → 輕量化不能只看 EER → 必須研究「凍結的選擇策略」是否被破壞、能否保留。

**部署情境（暫定）**：記者／事實查核者的本機初篩，三態輸出——`發現合成證據`（送人工複核）／`未發現合成證據`（不等於已驗證真人）／`證據不足，棄權`（強制升級人工或帶外查核，不靜默放行）。棄權後有明確承接動作，比向大眾直接承諾真假裁決更符合偵測器能力邊界。

**明確不主張**：不驗證說話者身分、不涵蓋 adaptive attack／partial deepfake／多語全面泛化；無真人實測，故不宣稱降低受騙率或社會風險。

本問題形式化為 **source-frozen selective-policy transfer**：分類門檻 `t` 與棄權門檻 `q` 僅由 source 開發資料決定並凍結，部署到 documented lineage-disjoint 未見生成器時，其 confident-real leakage 是否仍守在事先承諾的上限內。貢獻定位為 **replication + external-validity protocol + 診斷**，只有 H2 打贏強基線時才主張方法貢獻。

---

## 5. 先前相關研究論文與統整

**(a) ADD 可靠性、校準與部署**：Salvi（ICASSP 2023）做 reliability estimation；Pascu（Interspeech 2024）做跨資料集泛化與 calibration；FADEL（ICASSP 2025）用 evidential uncertainty；Kwok（ICASSP 2025）做 ensemble confidence calibration、Kwok（Interspeech 2025）揭露 bona-fide cross-testing 弱點。**Zhou & Wang（arXiv 2606.21584, 2026 preprint）已直接以 LA source threshold 轉移到 ITW/DF21，報告 HTER/FRR/FAR 並比較多種無標籤 score 校正，直接碰撞 operating-point / threshold transfer 核心**——但無 lightweight student、無棄權維度、無壓縮 delta。Schäfer & Steinebach（ICWSM 2026）證明預設門檻在社群資料上的落差。

**(b) 輕量／壓縮 ADD**：DK-CAST（Discover Computing 2025）為 codec-aware 蒸餾，正式論文報 accuracy、F1、precision、recall、EER、min t-DCF、score distribution 與 mobile CPU latency、參數量、GFLOPs——**其殘餘缺口是未報 source-frozen selective-policy transfer（AURC／coverage-risk curve／lineage-disjoint operating-policy transfer），而非「只報 EER」**。FTDKD（TASLP 2024）為壓縮音訊的頻時域蒸餾，常用 EER/min t-DCF；適合當 lightweight KD baseline，但「重現 baseline」本身不足以作為論文貢獻。Detecting Audio Deepfakes on the Edge（arXiv 2606.30780）用截短 SSL + 瀏覽器外掛。

**(c) 壓縮×可靠性（跨領域）**：Zhong（ACL 2025）量化 LLM calibration gap；DistilDoc（ICDAR 2024）顯示壓縮後 accuracy 與 AURC/ECE 脫鉤；Mitra（CVPRW 2024）反證 pruning 不必然傷 calibration；Hebbalaguppe et al. KD(C)（ACCV 2024）calibrated-teacher→calibrated-student；BN3（CVPR 2021）、EnD²（NeurIPS 2021）、Kim（Interspeech 2021, ASR uncertainty-matching KD）為 uncertainty-preserving compression 先例。此類方法均為通用、非 ADD-specific。

**(d) selective classification / distribution shift**：El-Yaniv & Wiener（JMLR 2010）risk-coverage 理論；Geifman & El-Yaniv SelectiveNet（ICML 2019）learned reject；Liang, Peng & Sun（TMLR 2024）generic rank-changing SC 分數（Energy/KNN/ViM/SIRC）；**Cattelan & Silva（NeurIPS 2023 workshop，ImageNet classifier）發現修正 confidence estimator 後 selective 退化可大幅由 accuracy 及其 shift degradation 解釋——此為 H1 可被否證的重要反證，但屬 vision workshop 證據，不可當作 audio 已成立的定律**；Xu, Pu & Zhao（ICPR 2020/2021）KD + abstention 組合。

**(e) 校準與 shift**：Guo（ICML 2017）temperature scaling；Ovadia（NeurIPS 2019）post-hoc 校準在 shift 下退化；Multi-domain TS（NeurIPS 2022）、TransCal（NeurIPS 2020）、Gong（ICCV 2021）shift-aware calibration。

**可守的殘餘 gap（bounded wording）**：在已記錄搜尋範圍內，未見同時研究「lightweight ADD × documented lineage-disjoint unseen generators × source-frozen selective-policy transfer + teacher-relative 隔離 + 排序型修法基線」者。不主張發明 KD／calibration／abstention。

---

## 6. 研究問題（RQ）

採三段式 kill sequence，前一關成立才進下一關：

**H1a — 承諾轉移失敗 / `Δ_light > ε`**：在相同 source risk/coverage policy-fitting rule、matched discrimination tolerance 與部署預算下，ordinary lightweight student 使用預先定義的 base selector `u0`，其未見生成器 family-macro confident-real leakage 相對 teacher 增加至少具部署意義的實質差異 `ε`（即 `Δ_light > ε`，非只 `>0`、非 utterance p 值）。

**H1b — 強便宜修法閘**：只用 source train/dev 擬合、可在 student 端廉價推論、且預先登記的 rank-changing selector `u1`，仍不能把 student 的 external policy transfer 修回 teacher/reference tolerance。TS/Platt 僅作 probability-calibration control。

**H2 — 條件性、由診斷導出的蒸餾機制**：若 H1a 成立且 H1b 失敗，才根據 family／error／representation 診斷定義一個 training-time 或 lightweight selection-aware 機制；它必須在同一 student、同一 deployment budget 與 matched discrimination 下勝過 ordinary KD 及最強合法 H1b baseline，並通過 method closest-work gate。

---

## 7. 方法論

### 7.1 source-frozen selective policy（核心設計）

raw score `s(x)∈ℝ`（fake 方向為正）；分類 `ŷ=1[s(x)≥t_m]`。

- **H1a base selector**：`u0(x)=|s(x)−t_m|`（decision-margin，非 rank-changing）；`accept ⇔ u0≥q_m`。
- **H1b repair selector**：`u1(x)=h(s(x), z_student(x))`（rank-changing，`z_student` 取自部署中的 student，不得需要完整 teacher inference；selector 的參數／latency／RAM 計入部署預算）。須以 Kendall τ / accepted-set disagreement 實測確認 `u1` 真的改變 accepted set。

### 7.2 UCB policy fitting（α 進 policy 約束，非事後比較）

```
(q_m, t_m) = argmax Coverage_dev(q,t)
  s.t.  UCB_{1-δ}[L_CR,dev(q,t)] ≤ α   且   FPR_real,dev(q,t) ≤ β
```

無可行 policy → 輸出「無法承諾」（no-feasible-policy fallback）。主 endpoint 與 coverage、人工複核比例聯合約束，防「全棄權」作弊。

### 7.3 Δ_light（source/target × student/teacher 雙重差分）

主 comparative estimand，隔離「輕量化額外損失」與「teacher 自身失效」：

```
Δ_light = (L_student^target − L_student^source) − (L_teacher^target − L_teacher^source)
```

即先對每模型算 transfer gap `G_m = L_CR^target − L_CR^source`（source 分量用 held-out source 估），再取 `Δ_light = G_student − G_teacher`。此為 teacher-relative double difference，逐 family 計 `Δ_light,g` 後 family-macro；並列報 per-family `G_student, G_teacher` 分量以求透明。若只關心 target，應改稱 teacher-relative gap，不得混稱 double difference。

### 7.4 TS/Platt no-op control（含成立條件）

Temperature scaling／正斜率 Platt 對 rank-based selection 為 no-op，**僅在轉換嚴格單調、且在轉換後依同一 source rank 約束重新選 threshold 的條件下成立**；它會改變 calibration，也可能改變固定數值 threshold 的 operating point，故不可無條件宣稱 no-op。toy 驗證：TS/Platt(a>0) + 依同一 source rank 約束重選門檻 → target 決策完全不變（diffs=0）；固定語意門檻不重選才會變（diffs=4252）。含義：純量校準原理上修不了 rank-based selective-policy transfer → TS/Platt 僅作 control，primary 修法必須 rank-changing。

### 7.5 失效四源診斷

拆解 target policy 退化來源：**discrimination（辨識力）／ranking（排序品質）／operating point（凍結門檻漂移）／calibration（機率校準）**，用以判斷退化是否可由 discrimination drop 完整解釋（呼應 Cattelan & Silva 反證），並導出 H2 的機制 hook。

### 7.6 KD 輕量化與 H2 機制（不預先 pin，由 H1a 診斷導出）

候選 family（過 closest-work gate 後才定案）：error-aware policy-preserving distillation

```
L = L_CE + λ_KD·L_KD + λ_rank·L_correctness-rank + λ_cons·L_codec-consistency
```

- `L_correctness-rank`：讓 selection score 把 student 正確樣本排在錯誤之前，特別處理 confident-real false negatives（ADD 不對稱危害特有 hook，非通用 confidence imitation）。
- `L_codec-consistency`：clean/codec/resampling 擾動下 selection ranking 穩定。
- component 權重／ablation 優先序由 H1a 失效診斷決定；不在 target 結果出來後臨時創造新 loss。

### 7.7 lineage-clean backbone

| 選項 | checkpoint | 預訓練 | ASVspoof 5 合規 |
|---|---|---|---|
| **首選** | `facebook/wav2vec2-base` | LibriSpeech-960 only | PASS（評估計畫明文允許 LibriSpeech） |
| 替代1 | `facebook/hubert-base-ls960` | LibriSpeech-960 | PASS |
| 替代2 | `microsoft/wavlm-base` | LibriSpeech-960 | PASS |
| **禁用** | XLS-R / wavlm-base-plus / *-ll60k | 含 MLS / LibriLight | **FAIL**（與 eval 上游重疊） |

ASVspoof 5 官方評估計畫禁止 MLS、LibriLight 及其衍生 pretrained models（與 eval data overlap），明確允許 LibriSpeech；Meta XLS-R model card 列 MLS 為 pretraining corpus，故 XLS-R × ASVspoof 5 confirmatory 組合不可用。完整 teacher 須固定 `model id→revision→SHA-256→fine-tuning corpora→augmentation→backbone pretraining corpora→holdout upstream speaker/utterance overlap`，並過 teacher quality gate；先只實作 wav2vec2-base，quality gate 失敗才切換。

---

## 8. 實驗

### 8.1 設計（五分切分，防洩漏）

A model-train｜B selector-train（out-of-fold correctness/cluster）｜C policy-dev（校準 + `(q_m,t_m)` + 驗 source 約束）｜D exploratory target（In-the-Wild/DFADD，僅 smoke test，不選方法/不調參/不改 endpoint；In-the-Wild 無可信 generator lineage，不得通過 confirmatory claim）｜E confirmatory holdout（ASVspoof 5 C00 subset，只做一次 final eval）。

Phase-0 derisking：**0.0** 環境 + 復現 wav2vec2-base teacher，source eval 對上論文級 EER；**0.1** 截短 probe（不訓練）+ u0 凍結 `(q_m,t_m)`，In-the-Wild 僅 smoke test；**0.2** ASVspoof 5 C00（family-macro `Δ_light`），前置 teacher full-lineage manifest + shortcut probes 通過；**0.3** toy-logit invariance 確認 + 測 rank-changing 修法 shortlist，TS/Platt 僅 control；**Phase 1** 僅 H1a 成立 + H1b 不足才做 H2。

### 8.2 資料集

| 角色 | 資料集 | 存取 | 關鍵事實 / 前置 |
|---|---|---|---|
| source anchor | ASVspoof 2019 LA | 直接下載 | attack 偏舊；ODC-By |
| **primary confirmatory** | **ASVspoof 5 C00 selected subset** | Zenodo 直接下載（protocol 已下載 20.7MB, MD5 PASS） | 7 architecture families（A17, A21+A22 合併, A24, A25, A26, A28, A29）；selected spoof 69,233 / bona fide 35,149；A17 speaker overlap <2% → 報含/不含 A17；A29(XTTS) 上游含 LibriLight → 標 caveat，不宣稱全 attack lineage-disjoint；shortcut probes PENDING |
| newer fallback（條件式） | XMAD-Bench | 直接下載 | 只作 compound-shift fallback（同時改 source+speaker+generator，非 generator-isolated）；license 不一致（CC BY-NC-SA vs Apache）；M-AILABS 與 LibriSpeech 同 LibriVox lineage → 英/德/俄/西 slice 未清；Arabic/Mandarin/Romanian 較安全但改語言 |
| exploratory replication | DFADD（pinned corrected release） | 直接下載 | LJSpeech/VCTK shortcut；不作唯一 confirmatory |
| plumbing only | MLAAD-tiny | 直接下載 | 僅驗 pipeline |
| backbone lineage | wav2vec2-base ← LibriSpeech-960 | 直接下載 | lineage-clean，逐層 manifest |
| 排除 | 完整 MLAAD、AUDETER（1.08TB）、RADAR/challenge-gated | — | 需申請/資格/隱藏 labels，違反 critical-path 免申請直下載 hard gate |

**Hard gate**：critical-path 資料集必須免申請直接下載。Primary→Fallback 切換：ASVspoof 5 找不到 lineage-clean teacher→切已 audit 的 XMAD compound-shift；XMAD 混淆/license 無法解→維持 secondary；任一變 C 級/連結失效→立即切。Protocol-first 下載順序：metadata→lineage manifest→MLAAD-tiny 驗 pipeline→過 gate 才抓 primary shards。

### 8.3 參數與資源

| 參數 | 簡介 | 判別 / pass 準則 |
|---|---|---|
| `α` | confident-real leakage 上限（風險承諾） | 進 policy 約束；holdout 上 `L_CR^macro>α` 即 external violation |
| `β` | bona-fide FPR 上限 | source-dev 約束；防以高誤報換低 leakage |
| `δ` | 風險估計信心水準 | 用單尾信賴上界 `UCB_{1-δ}`，非點估計 |
| `ε` | H1a 具部署意義最小退化量 | `Δ_light>ε` 才算 H1a 成立；預先定義 |
| `t_m` / `q_m` | 分類 / 棄權門檻 | 各模型由 source-dev 擬合並凍結，不套 teacher 門檻 |
| `L_CR,g` | family g 的 confident-real leakage `P(accept∧real｜fake,g)` | 主 endpoint；須與 coverage 聯合看 |
| `Δ_light` | 輕量化額外退化（雙重差分） | 主 comparative estimand；per-family + family-macro |
| AUROC / EER | 辨識力 | matching 變數（預宣告 equivalence tolerance） |
| eAURC / error-AUROC | selective ranking 品質 | secondary diagnostic，不作 matching 變數（避免 circular） |
| ECE / Brier / NLL | 校準品質 | control（TS 改善但不改排序，故不作 repair） |
| param/size/RAM/latency/RTF | 部署預算 | matching 變數；selector overhead 計入 |
| GPU-h | 單張 RTX 4090 預算 | 全程單卡；teacher 復現 + student KD + H2 ablation 排入有限 GPU-h，Phase 越前越便宜優先 |

baselines（預先登記，調參只用 source）：frozen lineage-clean teacher｜truncated probe｜ordinary KD｜H1b rank-changing shortlist（normalized-margin / student-embedding Mahalanobis 或 ViM / SIRC 類 confidence+OOD composite）｜cluster-conditional recalibration（僅當 target inference 能無標籤決定 cluster 才合法）｜TS/Platt（control）｜（gates 過後）H2。所有方法計 deployment cost。

### 8.4 預期結果（結果表骨架＋預期／推估，無實測數值）

> 以下數值欄位於計畫書階段一律留白或標「預期／推估」，實際數值待 Phase 0/1 產生；此處僅呈現結果表結構與方向性假設。

**表 8.4-1｜H1a 主結果（family-macro，預期）**

| 模型 | AUROC (matched) | EER (matched) | L_CR^source | L_CR^target | G_m | Δ_light | 判定 |
|---|---|---|---|---|---|---|---|
| teacher (wav2vec2-base) | 〔預期基準〕 | 〔預期基準〕 | 〔待測〕 | 〔待測〕 | 〔待測〕 | — | — |
| lightweight student | 〔預期 ≈ teacher〕 | 〔預期 ≈ teacher〕 | 〔待測〕 | 〔待測〕 | 〔待測〕 | 〔預期 >ε〕 | 〔H1a？〕 |

*預期方向（推估）*：頭號可引用數字為 `ΔEER≈0 但 Δ_light>0`——即在配平辨識力下仍觀察到輕量化特有的凍結策略退化。**同時誠實承認可能 null**（見第 9 節）。

**表 8.4-2｜H1b 修法（預期）**

| 修法 | 類型 | 改排序? (Kendall τ) | Δ_light after repair | 是否修回 tolerance |
|---|---|---|---|---|
| TS / Platt | control (no-op*) | 預期否 | 預期 ≈ 未修 | 預期否（*成立條件見 7.4） |
| normalized-margin | rank-changing | 待測 | 〔待測〕 | 〔未知〕 |
| student-embedding Mahalanobis / ViM | rank-changing | 待測 | 〔待測〕 | 〔未知〕 |
| SIRC 類 confidence+OOD | rank-changing | 待測 | 〔待測〕 | 〔未知〕 |

**表 8.4-3｜H2 機制（條件性，預期）**

| 方法（同 student/budget） | Δ_light | vs 最強 H1b | ablation 增益來源 |
|---|---|---|---|
| ordinary KD | 〔待測〕 | — | — |
| 最強 H1b rank-changing repair | 〔待測〕 | 基準 | — |
| H2 policy-preserving distillation | 〔預期最低〕 | 〔預期勝出？〕 | 〔correctness-rank / codec-consistency 各項待 ablation〕 |

---

## 9. 結果分析與討論

> 本節為計畫書階段之假設性推論，明確標示「預期／推估」，並附成立與 null 兩種情境及其理由。

**H1a 預期成立、但誠實承認可能 null（推估）**：預期 lightweight student 在 matched discrimination 下，未見生成器 family-macro `Δ_light > ε`。*推估理由*：Zhong（ACL 2025）、DistilDoc（ICDAR 2024）顯示壓縮後 accuracy 與 calibration/排序脫鉤，`s` 的絕對尺度平移會使凍結門檻在新分佈上失準；且 confident-real 為不對稱危害，壓縮的邊界幾何改變最先傷到它。*可能 null 情境（必須保留早停 gate）*：Mitra（CVPRW 2024）反證 pruning 不必然傷 calibration；**Cattelan & Silva（NeurIPS 2023 workshop, vision）反證顯示修正 confidence estimator 後 selective 退化可大幅由 accuracy 解釋**——若失效四源診斷顯示退化可由 discrimination drop 完整解釋，則撤回「lightweight 特有 policy fragility」機制主張，保留為有用負結果或 deployment replication。此為本題最重要的可否證點；此反證屬 vision workshop 證據，不外推為 audio 定律。

**H1b 預期：純量校準 no-op（在 7.4 條件下確定）；rank-changing 修法能否救回未知（推估）**。*推估理由*：TS 對 rank-based policy 在轉換單調且重選門檻條件下為 no-op；Ovadia（NeurIPS 2019）、Multi-domain TS（NeurIPS 2022）顯示 source-only post-hoc 校準在 shift 下常不足 → 便宜修法傾向救不回（對本研究有利），但無保證，須實測。

**H2 預期（若前兩關成立，推估）**：由診斷導出的機制在 matched budget 下把 `Δ_light` 壓到低於最強 rank-changing 修法，且增益來自機制本身（ablation 證明，非模型變大／更多資料／target tuning）。*推估理由*：generic 修法只重排分數、不改變 student 對自身錯誤的表徵；針對 confident-real false-negative 的 correctness-rank + codec-consistency 蒸餾，理論上能把 teacher 的「錯誤自覺」與抗通道穩定性傳給 student。**但這是本計畫最未 derisk 的一關。**

**與 Zhou & Wang（2026 preprint）的區隔**：Zhou & Wang 已直接碰撞 threshold/operating-point transfer 並比較無標籤 score 校正，但無 lightweight student、無棄權（abstention）維度、無壓縮 delta（`Δ_light`）；本研究殘餘 gap 縮至 source-frozen selective **policy**（含 `q`）、compression double-difference 與 lineage-audited family-macro external audit。

**結果決策樹**：H1a null（matched 後無退化）→ 早停、省檔、重估；H1a 成立且 rank-changing 修法已救回 → kill H2，成果＝external-validity 評估（偏量測，低於作者方法 bar），回候選題；H1a 成立、修法不足、H2 打贏 → 達 bar 的方法貢獻 + edge ADD 評估標準修正 + 三態 model card；H2 打不贏 → 誠實降為 replication/external audit + negative result，不改 loss 名製造 novelty。

---

## 10. 總結

本計畫將 edge ADD 的核心部署風險形式化為 source-frozen selective-policy transfer，並以三段式 kill sequence（H1a 承諾轉移 / `Δ_light>ε`、H1b 便宜修法閘、H2 條件性蒸餾）嚴格分層檢驗。方法上以雙重差分 `Δ_light` 隔離輕量化額外退化與 teacher 自身失效，以 UCB 約束把風險上限 `α` 真正寫進 policy fitting，以失效四源診斷導出（而非預先 pin）H2 機制，並以 lineage-clean 的 LibriSpeech-960 backbone 確保「未見生成器」宣稱可守。貢獻定位為 replication + external-validity protocol + 診斷，方法貢獻僅在 H2 打贏強 rank-changing 基線時主張。全程單張 RTX 4090、不做真人實測、不用 target labels 調參、不訓練 foundation model、critical-path 資料免申請直下載。

---

## 11. 未來展望

- **序列化延伸**：把 utterance-level policy 推廣為 call-level sequential selective policy（D1-B 方向），分開控制 fake-call miss 與 bona-fide ever-false-alarm，需先過 formalization kill test。
- **跨語言 / compound shift**：在解決 license 與 lineage 混淆後，以 XMAD-Bench 檢驗 source+speaker+generator 複合 shift 下的策略轉移。
- **adaptive attack 與 partial deepfake**：本計畫明確排除，未來可將凍結 policy 置於攻擊成本前沿（D3）框架下評估其穩健性。
- **三態 model card 標準化**：若 H2 成立，將 `發現/未發現/棄權` 三態輸出與 lineage manifest 推為 edge ADD 部署的可重現評估規格。

---

## 12. 參考文獻

**ADD 可靠性/校準/部署**
- C. Y. Kwok et al. "Robust Audio Deepfake Detection using Ensemble Confidence Calibration." ICASSP 2025. DOI:10.1109/ICASSP49660.2025.10889972.
- C. Y. Kwok et al. "Bona fide Cross Testing Reveals Weak Spot in Audio Deepfake Detection Systems." Interspeech 2025, pp.2230–2234. DOI:10.21437/Interspeech.2025-172.
- J. Zhou, M. Wang. "When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors." arXiv:2606.21584 v1 (2026-06-19, preprint). DOI:10.48550/arXiv.2606.21584.
- Schäfer & Steinebach. "Reality Check: Audio Deepfake Detectors on Social Media Data." ICWSM 2026.
- Salvi et al. "Reliability Estimation for Synthetic Speech Detection." ICASSP 2023.
- Pascu et al. "Towards Generalisable and Calibrated Audio Deepfake Detection with Self-Supervised Representations." Interspeech 2024.
- FADEL. "Uncertainty-aware Fake Audio Detection with Evidential Deep Learning." ICASSP 2025 / arXiv:2504.15663.

**輕量/壓縮 ADD**
- DK-CAST. "Dynamic Knowledge Condensation with Audio-Selective Transformer for Audio Deepfake Detection." Discover Computing 2025. DOI:10.1007/s10791-025-09746-4.
- FTDKD. "Frequency-Time Domain Knowledge Distillation for Low-Quality Compressed Audio Deepfake Detection." IEEE/ACM TASLP 2024.
- "Detecting Audio Deepfakes on the Edge: Lightweight SSL-Based Detection in a Browser Plugin." arXiv:2606.30780.

**壓縮×可靠性（跨領域）**
- Zhong et al. "Quantized Can Still Be Calibrated." ACL 2025.
- DistilDoc. ICDAR 2024. arXiv:2406.08226.
- Mitra et al. "Investigating Calibration and Corruption Robustness of Post-hoc Pruned Perception CNNs." CVPRW 2024.
- Hebbalaguppe et al. "Calibration Transfer via Knowledge Distillation." ACCV 2024.
- Cui et al. "Bayesian Nested Neural Networks." CVPR 2021.
- Ryabinin et al. "Scaling Ensemble Distribution Distillation." NeurIPS 2021.
- Kim et al. "Multi-Domain KD via Uncertainty-Matching for E2E ASR." Interspeech 2021.

**selective classification / shift / KD+abstention**
- El-Yaniv & Wiener. "On the Foundations of Noise-free Selective Classification." JMLR 2010.
- Geifman & El-Yaniv. "SelectiveNet." ICML 2019.
- Liang, Peng & Sun. "Selective Classification Under Distribution Shifts." TMLR 2024.
- Cattelan & Silva. (matched-accuracy selective performance). NeurIPS 2023 workshop.
- Y. Xu, J. Pu, H. Zhao. "Knowledge Distillation with a Precise Teacher and Prediction with Abstention." ICPR 2020 (pub. 2021), pp.9000–9006. DOI:10.1109/ICPR48806.2021.9412696.

**校準 / distribution shift**
- Guo et al. "On Calibration of Modern Neural Networks." ICML 2017.
- Ovadia et al. "Can You Trust Your Model's Uncertainty?" NeurIPS 2019.
- "Robust Calibration with Multi-domain Temperature Scaling." NeurIPS 2022.
- "TransCal: Transferable Calibration." NeurIPS 2020.
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

> 標註：Zhou & Wang 目前為 arXiv preprint（定稿時重查發表狀態）；Kwok 為兩篇不同論文（依主張分引）；Xu 為視覺領域 KD+abstention，非 ADD 直接先例；Cattelan & Silva 為 vision workshop 反證，不外推為 audio 定律。
