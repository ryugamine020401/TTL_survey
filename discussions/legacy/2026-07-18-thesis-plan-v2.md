# 碩士論文計畫書 v2（最終工作版）

## 未知生成器下輕量音訊深偽偵測器的選擇性策略轉移
### Selective-Policy Transfer of Lightweight Audio Deepfake Detectors under Unseen Generators

日期：2026-07-18　狀態：最終工作計畫（正式定題與 pilot 待作者/學長裁定；大檔下載與訓練暫停）
承接：plan v1（`2026-07-18-thesis-plan-v1.md`）+ H1b 單調等價 red-team（`2026-07-18-claude-redteam-h1b-monotonic-equivalence.md`，已採主軸 A + redline）
證據基礎：8 篇 survey、多輪多角色思辨、Codex 獨立查證（A–E claims / 七角色審查 / D1-P·D1-C literature gates / Q1–Q3 前作定位 / recalibration·holdout gates / H1b 單調等價），Claude red-team 與 toy 數值驗證。

---

## 0. 摘要

音訊深偽偵測器越來越準，也開始被縮小、放進瀏覽器與 edge 裝置，讓一般大眾、記者與查核者能**本機、低成本、離線**檢查可疑語音。但現行輕量化研究幾乎只用 EER、AUC、延遲、記憶體證明模型「仍然能分」，**沒有回答一個真正的部署問題：模型縮小後，遇到訓練沒見過的新生成器時，那條在開發階段就固定下來的「接受 / 棄權 / 標記」決策規則，還守不守得住？**

本論文把這個問題形式化為 **selective-policy transfer**：偵測器的分類門檻 `t` 與棄權門檻 `q` 只由 source 開發資料決定並凍結，部署到 **lineage-disjoint 未見生成器**時，是否仍能維持事先承諾的風險上限與覆蓋率。我們先驗證輕量化是否破壞這個策略（H1a）、便宜的 source-only 修法是否救得回（H1b），若確有破壞且便宜修法不足，再提出一個由失效診斷導出的機制保留它（H2）。

一個關鍵的理論起點（已用數值驗證）：**純量後驗機率校準（temperature scaling / Platt）在 rank-based policy 上是可證明的 no-op**——因此問題不是「調機率」，而是「能否用一個會改變樣本排序 / 決策幾何的 source-only 機制」保住外部策略。這把貢獻推向一片較少人碰的空間。

---

## 1. 研究背景

1. **deepfake audio 製造門檻極低，語音詐騙侵蝕社會對各種資訊的信任。**
2. **兩條現有防線各有硬極限**（survey 8 篇文獻）：
   - *被動偵測*：面對未見/閉源生成器，generalization 大幅下降（VoiceWukong：SOTA EER 從 <1% 升到 13.5%+，部分接近隨機）。
   - *密碼學 provenance（C2PA）*：只證「內容未被竄改」，不證「非 AI 生成」，且對不附憑證的惡意 deepfake 零覆蓋。
3. **一個被忽略的部署層缺口**：要讓偵測真正降低大眾受騙風險，偵測器必須能被本機、低成本、離線使用 → 必須輕量化。現行輕量/edge ADD（DK-CAST、FTDKD、2026 瀏覽器外掛 arXiv 2606.30780）**只用 EER/AUC/延遲/記憶體評估**，把偵測器當成「只會回真/假的二元黑盒」，沒有人檢查輕量化是否破壞了「該棄權時棄權」的能力。
4. **為何棄權能力才是部署關鍵**：真實使用中，一個把 fake 高信心判成 real 的「確定的錯誤」，比一次誠實的「我不確定，請人工複核」危害大得多。輕量化若保住了 AUROC（排序能力）卻讓開發集凍結的門檻在新生成器上失準，使用者收到的就是「看似確定、其實錯誤」的『真人』判斷。

---

## 2. 研究動機與要解決的問題

**動機鏈（把個人動機與技術貢獻接在同一條因果鏈）**：
> 希望讓 ADD 更能被大眾/記者安全使用 → 必須本機、低成本 → 必須輕量化 → 輕量化不能只看 EER → 必須研究「凍結的選擇性決策策略」在未見生成器上是否還守得住、能否保留。

**要解決的問題（一句話）**：
> 當偵測能力（AUROC/EER）與部署預算（大小/延遲）相近時，**輕量化是否破壞只由 source 開發資料決定的 accept/abstain operating point 在未知 generator 上的轉移？若便宜的 source-only 修法不足，能否設計一個超過既有蒸餾的機制保留這種選擇性策略？**

**部署情境（暫定）**：**記者／事實查核者的本機初篩**。三態輸出——
- `發現合成證據`（送高優先人工複核）；
- `未發現合成證據`（**不等於**已驗證真人）；
- `證據不足，棄權`（強制升級為人工/帶外查核，不靜默放行）。

棄權後有明確承接動作，比向大眾直接承諾真假裁決更符合偵測器能力邊界。一般語音訊息使用者是後續受益者，非本論文已驗證的部署族群。**不主張**降低詐騙率/受騙率（無真人實測）、不驗證說話者身分。

---

## 3. 誠實的 novelty 定位（Codex 查證後）

把主張拆四層，各層前作狀態不同——這比籠統宣稱「創新」誠實也安全：

| 層 | 主張 | 前作狀態 | 誠實定位 |
|---|---|---|---|
| **現象**：壓縮在辨識力不變下傷可靠性 | 在 ADD 觀察 | **Partially（非定律）**：量化 LLM 有支持、pruning/BNN 有反證 | 不主張通用新現象；主張 ADD 特定情境的預註冊量測 |
| **設定**：輕量/edge ADD | 壓縮 ADD | **已知**（DK-CAST、FTDKD、edge/browser） | 不在此層 |
| **可靠性**：ADD 拒答可靠性 | 量可靠性 | **已知（full model）**（Pascu、FADEL） | 不在泛稱層 |
| **交集+方法**：輕量 ADD × 未見生成器 external selective-policy transfer × 保留方法 | 核心 | **Partially（窄交集 open）** | 只在窄交集可能成立；方法須由失效診斷導出，否則降為 application |

**可送審的一句 positioning**：
> Within our documented search scope, prior work separately (i) shows compression can alter calibration in some settings, (ii) develops calibration-/uncertainty-aware distillation, and (iii) evaluates distilled models with AURC. We found no work testing whether a **source-frozen selective policy** survives lightweight audio-deepfake transformation on **lineage-disjoint unseen generators**, nor an **ADD-specific mechanism** for that external selective-policy transfer.

**誠實結論**：這不是「完全創新」，而是「新組合 + 一個尚待驗證是否真有增量、且必須由 H1a 失效診斷導出的 ADD-specific 機制」。方法貢獻能否成立，是本計畫要 derisk 的核心賭注（見 §13）。

---

## 4. 核心研究問題與假設（kill sequence）

**核心 RQ**：見 §2 問題陳述。

- **H1a — 失效存在**：AUROC/EER 落在預設 matching tolerance 內時，ordinary lightweight student 各自用 source 開發資料凍結的 `(q_m,t_m)`，在未見 generator 上的 **generator-macro confident-real leakage / risk violation 顯著高於 teacher**。
- **H1b — 便宜修法 gate（已依單調等價修正）**：純量後驗校準（TS/Platt）在 rank-based policy 上是**已證 no-op**，僅作 probability-calibration **control**；真正的 gate 是——**最好的便宜 source-only rank-changing repair（feature-space selector / cluster-conditional recalibration）仍無法**把凍結策略的外部轉移修回 teacher 水準。能修回 → kill H2。
- **H2 — 方法 gate（不預先 pin 死）**：一個**由 H1a 失效診斷導出**、明確超過 confidence imitation、且會改變排序/決策幾何的機制，在 matched AUROC/eAURC、latency、參數量下，**同時打贏** ordinary KD、rank-changing repair baseline，並過 method closest-work gate。

**定序**：H1a 不成立 → 停。H1b 的 rank-changing repair 已足夠 → kill H2。H2 現行候選成分（correctness-ranking / selection-margin / clean↔codec consistency）各自已被前作涵蓋，**故不預先 pin**，待 H1a 診斷再定並過 closest-work gate。

---

## 5. 方法與公平比較設計

### 5.1 半頁數學規格（消除單調等價的模糊）
- raw score：`s(x) ∈ ℝ`（單一 scalar，fake 方向為正）。
- 分類決策：`ŷ = 1[s(x) ≥ t_m]`，`t_m` 由 **source-dev 的 rank-based 約束**（固定 FPR 或 cost）決定。
- 選擇/棄權：primary selection score `u(x)` **刻意不限定為 `s` 的單調函數**——採 source-only、input-dependent 的 rank-changing 分數（如 frozen SSL embedding 上的 Mahalanobis/energy，與 logit 結合）；`accept ⇔ u(x) ≥ q_m`，`q_m` 由 source-dev 覆蓋率約束決定。棄權即 `u(x) < q_m`。
- 校準器 `g`（TS/Platt）：對 `s` 嚴格單調 → **對 rank-based `t_m` 是 no-op（已證，見下）**；因此只作機率語意 control，不作 policy repair。
- **擬合順序**：先在 source-train 訓練模型 → source-dev 擬合校準與 selector → 在同一 source 約束下決定 `(q_m,t_m)` → **全部凍結** → 才碰 holdout（不得用 holdout label 調任何東西）。

### 5.2 單調等價的處置（已數值驗證）
純量校準 + 門檻重選對 rank-based 決策不變（toy：TS/Platt+refit diffs=0；固定 p≥0.5 不重選 diffs=4252）。**含義**：純量校準原理上修不了 rank-based selective-policy transfer → 本設計刻意讓 primary selector `u(x)` 為 rank-changing，並把 TS/Platt 定位為 control。這是「為何需要方法而非便宜校準」的動機，不是 bug。`(q_m,t_m)` 公式定稿後會再跑一次本 pipeline 專屬 toy 確認。

### 5.3 模型與公平比較
- **teacher/reference**：frozen SSL ADD（XLS-R + AASIST 或 + linear head，訓於 source）。
- **lightweight students**：截短層 probe（最便宜、不需訓練）+ 至多一個 ordinary-KD student。
- **公平 estimand**：每個模型**各自**用相同 source train/dev 擬合校準與 `(q_m,t_m)`；**不得把 teacher 門檻硬套 student**（不同 score scale 會製造假失敗）。
- **matched discrimination**：配平只用 **deployment budget + AUROC/EER equivalence tolerance（預先定）**；**不用 eAURC 當配平變數**（會與主結果 circular）。

### 5.4 必要 baselines
frozen teacher ｜ truncated probe ｜ ordinary KD ｜ **source-only rank-changing repair（feature-space selector / cluster-conditional recalibration）= H1b 真 gate** ｜ TS/Platt（機率校準 control，已證 no-op）｜（gates 過後）H2 proposed 機制。

---

## 6. 資料集

| 角色 | 資料集 | 說明 | 狀態 |
|---|---|---|---|
| source（train/dev） | ASVspoof 2019 LA | 訓練 + 門檻擬合；ODC-By | 公開可下載 |
| exploratory 首探 | In-the-Wild | 小、可下載；lineage 不明 → 僅探路 | 公開（Apache 2.0） |
| exploratory replication | DFADD（2025-04 corrected） | 5 TTS family；固定 LJSpeech 文本/VCTK shortcut → 非 confirmatory | HF，MIT+upstream |
| **confirmatory holdout（主）** | ASVspoof 5 eval C00 非 adversarial/非 legacy 子集 | 8 IDs（A17/A21/A22/A24/A25/A26/A28/A29），A21/A22 合併 ≈ **7 architecture families**；shortcut 控制較好 | 142GB；**lineage manifest 待 Codex**、下載待授權；ODC-By |

7 families 是小叢集 → bounded evidence、family bootstrap、寬區間，不宣稱普遍優越。

---

## 7. 使用的指標

**主要 endpoint（部署風險）**：source-frozen policy 下，每 generator family 的 confident-real leakage
```
L_CR,g = P( accept ∧ ŷ=real | y=fake, g )
L_CR^macro = (1/|G|) Σ_g L_CR,g          ← 主要量
Δ_transfer = L_CR^macro(holdout) − α      ← 主要 transfer violation（α=預設風險上限）
```
**次要（同 policy）**：coverage（overall/real/fake）、selective risk / risk violation、逐 family 結果。
**排序診斷（配平 + 診斷用，不代替主 endpoint）**：eAURC、error-AUROC、AUROC、EER。
**校準診斷（輔助）**：Brier、NLL、ECE（衡量機率品質，不代替 ranking；TS 可改善 ECE 但不改排序，故列 control）。
**部署**：parameter count、CPU latency、peak RAM、model size。
**不確定性報告**：family bootstrap / hierarchical interval，誠實呈現 ~7 clusters 的寬區間，逐 family 列出；**不**用 utterance-level p-value 宣稱普遍優越。
**配平變數**：deployment budget + AUROC/EER equivalence tolerance（**不含 eAURC**）。

> 關鍵區分：AURC/risk–coverage 是 target score sweep（回答 ranking quality）；source-frozen `(q,t)` leakage 是 operating-point transfer（本題主 endpoint）——兩者分開報，不互相替代。

---

## 8. 執行計畫（Phase-0 derisking 稽核；越前面越便宜）

- **Stage 0.0**：建環境 + 復現公開 teacher，ASVspoof19 LA eval 對上論文 EER。（推論級，數小時）
- **Stage 0.1（H1a 便宜首探）**：加截短 probe（不訓練）；各模型 source-dev 凍結 `(q_m,t_m)`；在 **In-the-Wild** 看固定策略有無退化跡象。有 → 值得投 confirmatory；無 → 提早重估，省下大檔。（推論級，數小時）
- **Stage 0.2（H1a confirmatory）**：ASVspoof 5 C00（7 families，generator-macro）。前置：Codex lineage manifest 通過 + 作者授權下載。
- **Stage 0.3（H1b，已依 redline 改）**：(i) 先跑 toy-logit invariance 檢查，確認本 pipeline 的 `(q_m,t_m)` 落在等價條件；(ii) 真 gate 測 **source-only rank-changing repair** 能否修回；TS/Platt 僅作機率校準 control。
- **Phase 1（只有 H1a 成立 + H1b rank-changing repair 不足才做）**：由 H1a 診斷導出 H2 機制 → method closest-work gate → 在同 student/budget 下對決 baselines。

---

## 9. 預期結果（各假設與分支）

**我們預期會看到的（可否證，非既定）**：
- **H1a（預期成立、但誠實承認可能 null）**：輕量 student 在 matched discrimination 下，未見 generator 的 `L_CR^macro` 顯著高於 teacher，即凍結策略「悄悄」失準。頭號子結果：`ΔEER ≈ 0 但 Δ_transfer > 0`——一個數字說明「EER 看起來沒事、操作點卻漏 fake」。（Q1 文獻 mixed，故此為真賭注。）
- **H1b（預期：純量校準 no-op；rank-changing repair 未知）**：TS/Platt 依設計不改決策（control，確認 no-op）；便宜的 source-only rank-changing repair 能否修回是**開放**——Ovadia 2019 顯示 shift 下 post-hoc 常不足，對我們有利但不保證。
- **H2（若前兩關成立）**：由 H1a 診斷導出的機制，在 matched budget 下把 `L_CR^macro` 降到低於最好 rank-changing repair，且增益來自機制本身（消融證明，非模型變大/更多資料/target tuning）。

**結果分支（決策樹）**：
1. H1a null（matched discrimination 後無退化）→ **早停**，省下大檔；重估方向。
2. H1a 成立、H1b rank-changing repair 已修回 → **kill H2**；成果為「external-validity 評估 + 便宜修法有效」——但這偏量測，**低於作者貢獻 bar** → 回候選題比較。
3. H1a 成立、rank-changing repair 不足、H2 打贏 → **達 bar 的方法貢獻**：一個保留 external selective-policy 的機制 + 對 edge ADD 評估標準的修正 + 三態 model card。
4. H2 打不贏 baseline → 誠實降為 replication/external audit + negative result，回候選題比較（不事後改 loss 名製造 novelty）。

**有用的負結果**：即使 EER 保留，輕量化系統性破壞 fixed-policy transfer，且哪種 source-only 修法能/不能跨 generator 轉移——這對 edge ADD 的評估實務是具體、可引用的修正。（但作者已表明純量測/負結果低於期待，屆時走分支 2/4。）

---

## 10. 一年範圍

**做**：一個 source 訓練設定、一個 primary holdout（ASVspoof5 C00）、一個 teacher + 至多兩個輕量 transformation、一個由 H1a 導出的機制、score/family-level 主分析、一份三態輸出 + latency 可行的 reference deployment artifact。

**不做**：多 backbone 大矩陣、六種 uncertainty 排行榜、手機 App/完整瀏覽器產品、human-subject study、多語全面泛化、partial deepfake、對抗攻擊、新 foundation model 訓練、任何用 holdout label 調參。

---

## 11. Kill / pivot 條件

- **Kill**：matched discrimination 後無 H1a 退化；退化由 teacher 在 target 失效或 dataset shortcut 解釋；有效 family 數不足；需看 holdout 才能選 score/threshold。
- **Kill H2**：ordinary KD 或 rank-changing repair 已保住策略；proposed 機制無穩定增益；機制與 selective-classification/uncertainty-KD/DK-CAST 撞題且非由 H1a 導出。
- **Pivot**：方法空間消失 → 定位為嚴格 replication/external audit，回候選題（#4/#5）比較。

---

## 12. 算力預算（單張 RTX 4090, 24GB）

- Phase-0 稽核以推論 + 截短 probe 為主，幾十 GPU-hour 級。
- 全論文核心（含 H2 一個 student 訓練 + baselines）預估遠低於 500 GPU-hour；不 pretrain foundation model、不做組合爆炸矩陣、大資料集分層抽樣、frozen backbone + 特徵快取。

---

## 13. 誠實風險聲明（必讀）

1. **貢獻 bar 押在 H2**，且 H2 現在要打贏的是 **rank-changing repair（非 no-op 的 TS）**——bar 比先前更高；結果未 derisk，只能實測。
2. **方法 novelty 窄且高拆解風險**：三個候選成分各自已被前作涵蓋；H2 唯一活路是「由 H1a 失效診斷導出的機制」+ 過 closest-work gate，否則降 application。
3. **統計檢定力**：~7 generator families 是小叢集，方法普遍性主張受限。
4. **holdout 乾淨度**：ASVspoof5 lineage/shortcut 待 Codex manifest 核實；未過不解鎖 confirmatory。
5. **行政門檻未知**：學校/指導教授對 replication-plus-extension 型碩論的接受度，需學長裁定，非文獻能答。

---

## 14. 現況與下一步

- **決策**：採主軸 A（Selective-Policy Transfer）+ H1b/H2 redline；跑 Phase-0 H1a/H1b derisking 稽核。
- **Codex 進行中**：ASVspoof 5 C00 lineage/shortcut manifest（handoff `2026-07-18-1030`）。
- **Claude 下一步**：`(q_m,t_m)`、selection score `u(x)` 定成 §5.1 精確公式 + 本 pipeline 專屬 toy 確認。
- **待作者解鎖**（開跑 Stage 0.0）：計算環境（是否此 RTX 4090、Python/CUDA 可用）；授權下載 ASVspoof19 LA + In-the-Wild；公開 checkpoint 來源。ASVspoof5（142GB）延到 manifest 過 + 明確授權。
- **暫停中**：full pilot、142GB 下載、任何訓練。

---

## 15. 關鍵前作（Codex 已查證）

- 量測/可靠性：Salvi (ICASSP 2023)、Pascu (Interspeech 2024)、FADEL (ICASSP 2025)、Zhou & Wang (arXiv 2606.21584)、Schäfer & Steinebach (ICWSM 2026)、Kwok (Interspeech 2025)。
- 輕量/壓縮 ADD：DK-CAST (Discover Computing 2025)、FTDKD (TASLP 2024)、Detecting Audio Deepfakes on the Edge (arXiv 2606.30780)。
- 壓縮×可靠性（現象/方法/指標）：Zhong (ACL 2025)、DistilDoc (ICDAR 2024)、Mitra (CVPRW 2024)、KD(C) (ACCV 2024)、BN3 (CVPR 2021)、EnD² (NeurIPS 2021)、Kim (Interspeech 2021)、Niu (NeurIPS 2022)、Xu (ICPR 2020)。
- 校準/單調性：Guo (ICML 2017)、Ovadia (NeurIPS 2019)、Multi-domain TS (NeurIPS 2022)、TransCal (NeurIPS 2020)、Gong (ICCV 2021)。
- 資料集：ASVspoof 2019 LA、In-the-Wild、DFADD (arXiv 2409.08731)、ASVspoof 5 (arXiv 2502.08857)。

（各連結詳見 `research/validations/` 對應查證檔。）
