# 碩士論文題目審核報告

## 審核對象

**原始題目**

> 未知生成器下輕量音訊深偽偵測器的選擇性策略轉移  
> Selective-Policy Transfer of Lightweight Audio Deepfake Detectors under Unseen Generators

**原始文件**：`貼上的 Markdown (1).md`

**用途**：供 Codex 與 Claude 進行第二輪 red-team 審查。

---

# 一、整體判斷

本題具備碩士論文價值，但目前建議評定為：

> **有條件通過，尚不宜直接視為正式定題。**

本研究不是單純再訓練一個 audio deepfake detector，而是研究：

- 輕量化後的偵測器；
- 在未知生成器上的外部泛化；
- 僅由 source 資料決定並凍結的分類／棄權策略；
- 高信心錯判真人的部署風險；
- source-only 策略修復或保留方法。

目前計畫同時綁定三個層次：

1. 未見生成器下的 operating-point transfer 評估。
2. 輕量化是否造成額外 transfer degradation。
3. 提出新的策略保留方法。

第 1 層已有接近的 threshold-transfer、calibration-transfer 與 selective classification 前作。因此，真正可能構成主要貢獻的部分應集中在：

> **輕量化是否造成超出 teacher 本身 domain-shift failure 的額外 selective-policy transfer degradation，以及如何在 source-only 條件下保留該策略。**

## 初步評分

| 面向 | 評價 | 說明 |
|---|---:|---|
| 問題重要性 | 8/10 | 部署問題明確，不只是模型準確率比較 |
| 可執行性 | 7/10 | 單張 RTX 4090 原則上可行，但資料與切分需先確認 |
| Novelty | 6/10 | threshold transfer 已有前作，必須縮窄主張 |
| 統計設計 | 5.5/10 | 約 7 個 generator families，無法支撐過廣的普遍性主張 |
| 方法完整度 | 5/10 | H2 尚未被定義成可直接審查、重現的方法 |
| 綜合結論 | 有條件通過 | 修正 estimand、policy 公式、baseline 與資料 lineage 後再正式定題 |

---

# 二、核心優點

## 2.1 問題具有真實部署意義

現有 ADD 研究常使用 EER、AUROC、accuracy、latency、parameter count 與 model size。然而實際部署系統不是只需要排序真假樣本，而是必須在固定 operating point 下做出：

- fake；
- real；
- abstain。

本研究把注意力放在：

> 模型輕量化後，source 階段決定的分類與棄權規則，在未知生成器上是否仍然有效。

這比單純比較 EER 更接近真實部署。

## 2.2 三態輸出比二元真假裁決合理

目前設定的三態輸出：

- 發現合成證據；
- 未發現合成證據；
- 證據不足，棄權。

此設計能避免把「沒有偵測到 deepfake」錯誤表述為「已證明是真人」，也較符合記者與事實查核者的人工升級流程。

## 2.3 已意識到純量單調校準的限制

若：

- calibration function `g` 對 score 嚴格單調；
- threshold 在校準後重新依 rank-based constraint 選擇；
- selection score 也是原 score 的單調函數；

則樣本排序及接受集合不會改變。

因此 Temperature Scaling 或 Platt Scaling可能改善 NLL、Brier、ECE 與機率語意，但不一定能修復 rank-based threshold transfer、selective decision geometry 或未知生成器下的錯誤排序。

將 TS／Platt 定位為 probability-calibration control，而非主要 repair，是正確方向。

## 2.4 計畫具有 kill gate

目前計畫已設計：

- H1a 不成立則停止；
- 便宜 rank-changing repair 已足夠則 kill H2；
- H2 打不贏 baseline 則降級為 external audit／negative result。

這能降低事後改寫假設的風險。

---

# 三、四個最關鍵問題

## 3.1 Novelty 已被直接前作逼近

最危險的主張是：

> 尚無研究檢查 source-frozen threshold 或 selective policy 在未知生成器上的轉移。

此主張需要大幅縮窄。已有研究涉及：

- speech deepfake detector 的 threshold transfer；
- EER 對 deployment operating-point failure 的遮蔽；
- calibration 在 dataset shift 下的限制；
- 預設 threshold 在 social-media data 上的適用性；
- browser／edge 上的 lightweight ADD；
- uncertainty-aware ADD；
- selective classification under distribution shift。

因此，不宜將 novelty 定位為「首次研究 threshold transfer」。

建議改成：

> 研究「對同一 reference ADD 進行輕量化後，是否產生超出 reference teacher 本身 domain-shift failure 的額外 source-frozen selective-policy transfer degradation」，以及 ADD-specific source-only preservation mechanism。

較安全的英文 positioning：

> Within the documented search scope, prior studies separately examine threshold transfer in speech deepfake detection, uncertainty-aware detection, calibration under distribution shift, lightweight audio deepfake detection, and confidence-aware distillation. This study focuses on whether lightweight transformation introduces additional degradation in a source-frozen selective policy beyond the reference detector's own target-domain failure, and whether that degradation can be reduced without target labels.

### Novelty 分層

| 層次 | 前作狀態 | 本研究可否主張 |
|---|---|---|
| ADD 面對 unseen generators 會退化 | 已知 | 不可主張為新現象 |
| Lightweight／edge ADD | 已知 | 不可單獨主張 novelty |
| ADD calibration／uncertainty | 已知 | 不可泛稱首次 |
| ADD threshold transfer | 已有接近前作 | 必須承認並精確區隔 |
| Lightweight transformation 的額外 policy-transfer damage | 可能有空間 | 可作 H1 核心 |
| ADD-specific policy-preserving mechanism | 可能有空間 | 必須通過 closest-work gate |

## 3.2 `q`、`t` 與 `α` 尚未形成同一個可執行策略

目前計畫同時寫到：

- `t` 由固定 FPR 或 cost 決定；
- `q` 由 coverage constraint 決定；
- `α` 是預設 confident-real leakage 上限；
- target 上計算 `L_CR - α`。

問題是：

> 如果 `q` 只由 coverage 決定，policy 建構過程沒有真的使用 `α`。

此時 `α` 只是事後比較基準，不是 policy 本身的風險目標。

### 建議正式定義

令：

- `t_m`：模型 `m` 的 fake／real 分類門檻；
- `q_m`：接受／棄權門檻；
- `α`：source-dev 可接受的 confident-real leakage 上限；
- `β`：source-dev 可接受的 bona-fide false-positive 上限；
- `δ`：風險估計的信心水準。

定義：

\[
(t_m,q_m)
=
rg\max_{t,q}
\widehat{\mathrm{Coverage}}_{\mathrm{source-dev}}(t,q)
\]

subject to

\[
U_{1-\delta}
\left(
\widehat{L}_{CR,\mathrm{source-dev}}(t,q)
ight)
\leq lpha
\]

and

\[
U_{1-\delta}
\left(
\widehat{\mathrm{FPR}}_{\mathrm{source-dev}}(t,q)
ight)
\leq eta
\]

其中 `U` 是單尾信賴上界，而非 point estimate。

### 較容易實作的兩階段版本

1. 在 source-policy-dev 上依 `β` 選 `t_m`。
2. 固定 `t_m` 後，選 coverage 最大且 `L_CR` 信賴上界不超過 `α` 的 `q_m`。
3. 凍結 model、calibration、selector、`t_m`、`q_m`、feature normalization、cluster rule 與 hyperparameters。
4. 之後才允許接觸 target holdout。

## 3.3 不能宣稱對任意 unseen generator 提供 risk guarantee

只依賴 source data 建立的 policy，通常無法在沒有額外假設時保證：

\[
L_{CR,target}\leqlpha
\]

對任意未知生成器成立。

可能的 shift 包括：

- covariate shift；
- label shift；
- concept shift；
- generator architecture shift；
- codec／channel shift；
- speaker／language shift；
- score distribution shift；
- error-ranking shift。

### 不宜使用

- 保證未知生成器上的風險上限；
- certified risk；
- guaranteed target risk；
- assured safety；
- 維持 target-domain risk guarantee。

### 建議使用

- source-specified risk target；
- external policy violation；
- observed transfer violation；
- unseen-generator risk degradation；
- reduce external violation；
- empirical preservation under documented holdouts。

定義：

\[
V_{m,g}
=
L_{CR,m,g}^{target}-lpha
\]

但應解釋為：

> target generator family `g` 上，source-specified risk target 的觀察違規程度。

不是對 target 已提供的形式保證。

若要使用 guarantee，必須額外加入 covariate-shift assumptions、conformal risk control、unlabeled target calibration、density-ratio bound 或 distributionally robust optimization，會大幅擴張論文範圍。

## 3.4 Teacher 與 student 的 target 差異，不必然是輕量化造成

目前 H1a 類似比較：

\[
L_{CR}^{student,target}
>
L_{CR}^{teacher,target}
\]

這只能說 teacher 與 student 在 target 上不同，無法排除：

- teacher 本身已經失效；
- student head 訓練差異；
- KD objective 差異；
- truncation 改變 representation；
- checkpoint selection；
- optimization noise；
- source score-scale 差異；
- selector fitting variance。

### 建議主 estimand：difference-in-transfer-gap

先定義每個模型的 transfer gap：

\[
G_m
=
L_{CR,m}^{target}
-
L_{CR,m}^{source}
\]

再定義輕量化額外退化：

\[
\Delta_{\mathrm{light}}
=
G_{student}
-
G_{teacher}
\]

展開為：

\[
\Delta_{\mathrm{light}}
=
\left(
L_{CR}^{student,target}
-
L_{CR}^{teacher,target}
ight)
-
\left(
L_{CR}^{student,source}
-
L_{CR}^{teacher,source}
ight)
\]

它回答：

> 從 source 移到 target 後，student 相對 teacher 多惡化多少？

對每個 generator family 可定義：

\[
\Delta_{\mathrm{light},g}
=
G_{student,g}-G_{teacher,g}
\]

並計算 family macro：

\[
\Delta_{\mathrm{light}}^{macro}
=
rac{1}{|G|}
\sum_{g\in G}
\Delta_{\mathrm{light},g}
\]

---

# 四、其他重要潛在問題

| 嚴重度 | 潛在問題 | 原因 | 建議修正 |
|---|---|---|---|
| 高 | H2 尚未 pin 成方法 | 審查者可能認為只有問題、沒有技術方案 | 預先限定 method family、loss 與允許調整範圍 |
| 高 | H2 一處寫 matched AUROC/eAURC | eAURC 若作配平變數會與 outcome circular | 配平只用 budget、AUROC、EER；eAURC 作結果 |
| 高 | H1b rank-changing repair 不具體 | baseline 可隨結果改動 | 預註冊 baseline、特徵與 hyperparameter 範圍 |
| 高 | `t` 寫固定 FPR 或 cost | 兩者對 calibration 的性質不同 | 選單一 primary policy，另一個作 sensitivity analysis |
| 高 | 約 7 families 卻使用「顯著優於」 | cluster 數太少 | 以 effect size、practical margin、family interval 為主 |
| 高 | `L_CR` 可由大量 abstention 降低 | 全部棄權也能低 leakage | 同時約束 coverage、class coverage 與 review workload |
| 中高 | In-the-Wild null 被當早停 | 多種 shift 混雜 | 僅作 smoke test，不作正式 kill criterion |
| 中高 | selector 與 `q,t` 使用同一 dev | 容易 overfit dev error | selector-train 與 policy-dev 分離或 cross-fitting |
| 中高 | energy／distance 不一定 rank-changing | 名稱不同不代表排序改變 | 報告 Kendall τ、Spearman ρ、accepted-set disagreement |
| 中高 | Mahalanobis 可能只偵測 channel novelty | OOD 與分類錯誤不等價 | 加 cross-fitted correctness predictor baseline |
| 中 | 單一 teacher/student 難談一般輕量化 | 可能只是單一架構現象 | 至少包含 truncation 與 ordinary KD |
| 中 | lineage-disjoint 用詞過強 | 可能共享模型、語料或 vocoder | 改為 documented lineage-disjoint under available metadata |
| 中 | threshold uncertainty 未納入 | 區間會偏窄 | bootstrap 時重擬 selector、`q`、`t` |
| 中 | leakage 不等於使用者後驗風險 | 取決於 prevalence | 加 prevalence sensitivity analysis |
| 中 | AUROC/EER matching tolerance 未定 | 容易事後解釋 | 預先設定 practical equivalence margin |
| 中 | family macro 沒有樣本門檻 | 小 family 估計不穩 | 設 minimum sample size 與 sensitivity analysis |
| 中 | exploratory／confirmatory 角色混淆 | 可能產生隱性 target tuning | 事先限制每個 dataset 可做的決策 |

---

# 五、建議題目與研究問題

## 建議中文題目

> **未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留**

另一版：

> **輕量化對音訊深偽偵測器凍結選擇策略之外部轉移影響與保留方法**

## 建議英文題目

> **Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators**

另一版：

> **Assessing and Preserving Source-Frozen Selective Policies after Lightweight Transformation of Audio Deepfake Detectors**

## 建議核心研究問題

> 在所有模型選擇、selector 與 decision thresholds 僅由 source data 建立並凍結的條件下，對同一 reference audio deepfake detector 進行輕量化，是否會造成超出 reference detector 本身 domain-shift failure 的額外 confident-real leakage？若存在此額外退化，source-only error-aware selection 或 policy-preserving distillation 能否在固定部署預算與辨識能力容忍範圍內降低該退化？

---

# 六、建議重新定義假設

## H1：Lightweight-induced transfer degradation

在 source AUROC／EER 與 deployment budget 符合預設 tolerance 時：

\[
\Delta_{\mathrm{light}}>\epsilon
\]

其中 `ε` 是具部署意義的最小退化量，不只是 `p < 0.05`。

## H2：Cheap source-only repair gate

預先指定的 source-only rank-changing repair baselines 無法將：

\[
\Delta_{\mathrm{light}}
\]

降低至預設 non-inferiority margin 內。

TS／Platt 僅作 probability calibration control。

## H3：Proposed mechanism

在以下條件相同時：

- student architecture；
- model-size budget；
- latency budget；
- source data；
- 不使用 target labels；
- AUROC／EER equivalence tolerance；

proposed mechanism 相較最佳 H2 baseline：

1. 降低 generator-macro `Δ_light`；
2. 不以 coverage collapse 換取；
3. 不增加不可接受的 bona-fide false-positive risk；
4. 可由 ablation 重現；
5. 不依賴 target-specific tuning。

---

# 七、建議最小可行實驗設計

## 7.1 資料切分

建議至少拆為：

### A. Model-train

用於 teacher／student training、KD 與 representation learning。

### B. Selector-train

用於 correctness predictor、error ranking、cluster assignment 與 distance selector。應使用 out-of-fold predictions，避免 selector 看到模型在自己訓練資料上的過度樂觀輸出。

### C. Policy-dev

只用於 calibration、決定 `t_m`、決定 `q_m` 與驗證 source risk constraints。

### D. Exploratory target

例如 In-the-Wild、DFADD，只可用於 pipeline smoke test，不可用於選方法、調 confirmatory hyperparameters 或更改 primary endpoint。

### E. Confirmatory target holdout

例如 ASVspoof 5 C00 指定子集，只做一次 final evaluation，不允許 target-label tuning。

## 7.2 模型設計

### Teacher

固定一個可重現的 reference detector，例如：

- frozen XLS-R + AASIST；
- frozen XLS-R + linear／MLP head；
- 公開 checkpoint 加固定 evaluation pipeline。

### Lightweight transformation A

- truncated SSL layers；
- frozen early-exit probe；
- layer dropping。

### Lightweight transformation B

- ordinary KD；
- smaller student backbone；
- parameter-efficient student。

至少需要兩種 transformation，避免把單一架構結果泛化為所有 lightweight methods。

## 7.3 H1b 必要 baselines

### Baseline 1：confidence／margin selector

\[
u(x)=|s(x)-t|
\]

### Baseline 2：class-conditional feature distance

例如 Mahalanobis、kNN 或 class prototype distance。需固定 embedding layer、normalization、covariance estimator 與 score combination。

### Baseline 3：cross-fitted error predictor

學習：

\[
P(\hat y_m=y\mid z_m(x),s_m(x))
\]

訓練標籤必須來自 out-of-fold correctness。

### Baseline 4：cluster-conditional recalibration

預先固定 cluster algorithm、cluster number、feature space、minimum cluster size、calibration method 與 fallback rule。

### Control：TS／Platt

只報告 ECE、NLL、Brier 與 decision-set invariance，不作主要 rank-changing repair。

---

# 八、建議 H2 方法骨架

可將 H2 限定為：

> **Error-aware policy-preserving distillation**

範例：

\[
\mathcal{L}
=
\mathcal{L}_{CE}
+
\lambda_{KD}\mathcal{L}_{KD}
+
\lambda_{rank}\mathcal{L}_{correctness-rank}
+
\lambda_{cons}\mathcal{L}_{codec-consistency}
\]

- `L_CE`：保留 fake／real discrimination。
- `L_KD`：保留 teacher soft prediction 或 representation。
- `L_correctness-rank`：讓 selection score 將 student 正確樣本排在錯誤樣本之前，特別處理 confident-real false negatives。
- `L_codec-consistency`：讓 clean／codec／resampling／bandwidth perturbation 下的 selection ranking 穩定。

不應只模仿 teacher confidence，否則可能繼承 teacher 的錯誤高信心。

H1 可以決定失效模式、ablation 優先順序與 component weighting 的預註冊範圍，但不應在 target 結果出來後臨時創造新 loss。

---

# 九、建議評估指標

## Primary endpoint

\[
L_{CR,m,g}
=
P(
accept \land \hat y=real
\mid y=fake,g
)
\]

\[
L_{CR,m}^{macro}
=
rac{1}{|G|}
\sum_{g\in G}
L_{CR,m,g}
\]

## Primary comparative estimand

以 teacher-relative additional transfer degradation 為主，而非只比較 target leakage。

## Policy constraints

同時報告：

- overall coverage；
- fake coverage；
- bona-fide coverage；
- FPR；
- confident-real leakage；
- selective risk；
- 人工複核比例。

## Ranking diagnostics

- AURC；
- eAURC；
- error-AUROC；
- AUROC；
- EER；
- risk-coverage curve；
- accepted-set disagreement；
- Kendall τ；
- Spearman ρ。

## Probability calibration controls

- ECE；
- Brier score；
- NLL；
- reliability diagram。

## Deployment metrics

- parameter count；
- model size；
- peak RAM；
- CPU latency；
- real-time factor；
- feature extraction cost；
- selector overhead。

selector 的成本也必須計入。

---

# 十、統計分析建議

## 10.1 不應只用 utterance-level p-value

若 target 只有約 7 個 generator families，utterance 再多也不能等同於大量獨立 generator evidence。

建議使用：

- family-level effect；
- family bootstrap；
- hierarchical bootstrap；
- leave-one-family-out sensitivity；
- practical margin；
- bounded claim。

## 10.2 Bootstrap 應重跑完整 policy fitting

每次 bootstrap 應重新：

1. 抽 source-policy-dev；
2. fitting calibration；
3. fitting selector；
4. 選 `t`；
5. 選 `q`；
6. 評估 target。

否則會低估 policy-estimation uncertainty。

## 10.3 預先定義 equivalence tolerance

例如：

- AUROC 差異上限；
- EER 相對差異上限；
- latency 預算；
- parameter count 上限。

不能事後以「看起來差不多」宣稱 matched discrimination。

## 10.4 預先定義 practical effect

H1 建議測：

\[
\Delta_{\mathrm{light}}>\epsilon
\]

而非只測是否大於零。

---

# 十一、資料集風險

## ASVspoof 2019 LA

適合 source train／dev，但 attack technology 偏舊，需明確比較 source 與 target lineage。

## In-the-Wild

適合 smoke test，但 generator lineage、codec、speaker、language 與 recording pipeline shift 混雜。因此 In-the-Wild 上的 null 不應直接成為正式 kill criterion。

## DFADD

適合 diffusion／flow-matching exploratory test，但需控制文字、speaker corpus、vocoder 與 dataset shortcut。

## ASVspoof 5 C00

正式使用前必須完成：

| 欄位 | 必須確認 |
|---|---|
| Attack ID | 納入／排除哪些 ID |
| Generator type | TTS、VC、codec、adversarial 或其他 |
| Architecture | 具體 model family |
| Vocoder | 是否共享 |
| Training data | 是否與 source 有交集 |
| Base checkpoint | 是否共享 lineage |
| Speaker | 是否跨 source |
| Language | 是否跨 source |
| Channel／codec | 是否為主要 shift |
| Legacy attack | 是否排除 |
| Adversarial attack | 是否排除 |
| Samples per family | 是否足以估計低 leakage |
| Family merge rule | 合併依據是否預先定義 |

`lineage-disjoint` 建議改為：

> documented lineage-disjoint under available metadata。

---

# 十二、參考文獻對照表

> 以下連結與 metadata 應再由 Codex／Claude 獨立查證，尤其是 2025–2026 年文獻、正式會議版與 arXiv 版差異。

## 12.1 ADD 可靠性、校準、部署與輕量化

| 簡稱 | 正式名稱 | 場域／年份 | 與本研究的關係 | 連結 |
|---|---|---|---|---|
| Salvi | Reliability Estimation for Synthetic Speech Detection | ICASSP 2023 | ADD reliability estimation | https://ieeexplore.ieee.org/document/10095524/ |
| Pascu | Towards Generalisable and Calibrated Audio Deepfake Detection with Self-Supervised Representations | Interspeech 2024 | ADD generalization 與 calibration | https://www.isca-archive.org/interspeech_2024/pascu24_interspeech.html |
| FADEL | FADEL: Uncertainty-aware Fake Audio Detection with Evidential Deep Learning | ICASSP 2025／arXiv | evidential uncertainty | https://arxiv.org/abs/2504.15663 |
| Zhou & Wang | When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors | arXiv 2026 | 與 threshold-transfer 主軸最接近 | https://arxiv.org/abs/2606.21584 |
| Schäfer & Steinebach | Reality Check: Measuring Real-World Applicability of State-of-the-Art Audio Deepfake Detectors on Social Media Data | ICWSM 2026 | 固定 threshold 與現實資料 | https://ojs.aaai.org/index.php/ICWSM/article/view/42803 |
| Kwok et al. | Robust Audio Deepfake Detection using Ensemble Confidence Calibration | ICASSP 2025 | ensemble confidence calibration | https://ieeexplore.ieee.org/document/10889972/ |
| DK-CAST | Dynamic Knowledge Condensation with Audio-Selective Transformer for Audio Deepfake Detection | Discover Computing 2025 | 輕量 ADD、知識壓縮 | https://link.springer.com/article/10.1007/s10791-025-09746-4 |
| FTDKD | FTDKD: Frequency-Time Domain Knowledge Distillation for Low-Quality Compressed Audio Deepfake Detection | IEEE/ACM TASLP 2024 | ADD KD、壓縮音訊 | https://ieeexplore.ieee.org/document/10747292/ |
| Edge/browser | Detecting Audio Deepfakes on the Edge: Lightweight SSL-Based Detection in a Browser Plugin | arXiv 2026 | lightweight SSL、本機部署 | https://arxiv.org/abs/2606.30780 |

## 12.2 壓縮、蒸餾與可靠性

| 簡稱 | 正式名稱 | 場域／年份 | 關係 | 連結 |
|---|---|---|---|---|
| Zhong | Quantized Can Still Be Calibrated: A Unified Framework to Calibration in Quantized Large Language Models | ACL 2025 | 量化與 calibration 的跨領域證據 | https://aclanthology.org/2025.acl-long.1473/ |
| DistilDoc | DistilDoc: Knowledge Distillation for Visually-Rich Document Applications | ICDAR 2024 | KD／calibration 跨領域參考 | https://arxiv.org/abs/2406.08226 |
| Mitra | Investigating Calibration and Corruption Robustness of Post-hoc Pruned Perception CNNs: An Image Classification Benchmark Study | CVPRW 2024 | pruning、calibration、robustness | https://openaccess.thecvf.com/content/CVPR2024W/SAIAD/html/Mitra_Investigating_Calibration_and_Corruption_Robustness_of_Post-hoc_Pruned_Perception_CNNs_CVPRW_2024_paper.html |
| KD(C) | Calibration Transfer via Knowledge Distillation | ACCV 2024 | calibration-aware KD | https://openaccess.thecvf.com/content/ACCV2024/html/Hebbalaguppe_Calibration_Transfer_via_Knowledge_Distillation_ACCV_2024_paper.html |
| BN3 | Bayesian Nested Neural Networks for Uncertainty Calibration and Adaptive Compression | CVPR 2021 | compression 與 uncertainty | https://openaccess.thecvf.com/content/CVPR2021/html/Cui_Bayesian_Nested_Neural_Networks_for_Uncertainty_Calibration_and_Adaptive_Compression_CVPR_2021_paper.html |
| EnD² | Scaling Ensemble Distribution Distillation to Many Classes with Proxy Targets | NeurIPS 2021 | distribution／uncertainty distillation | https://proceedings.neurips.cc/paper/2021/hash/2f4ccb0f7a84f335affb418aee08a6df-Abstract.html |
| Kim | Multi-Domain Knowledge Distillation via Uncertainty-Matching for End-to-End ASR Models | Interspeech 2021 | speech uncertainty-matching KD | https://www.isca-archive.org/interspeech_2021/kim21g_interspeech.html |
| Niu | Respecting Transfer Gap in Knowledge Distillation | NeurIPS 2022 | teacher-student transfer gap | https://proceedings.neurips.cc/paper_files/paper/2022/hash/89b0e466b46292ce0bfe53618aadd3de-Abstract-Conference.html |
| Xu, ICPR 2020 | 無法由現有簡稱唯一辨認 | 待查 | 需補完整作者、題名、DOI | 待查 |

## 12.3 校準與 distribution shift

| 簡稱 | 正式名稱 | 場域／年份 | 關係 | 連結 |
|---|---|---|---|---|
| Guo | On Calibration of Modern Neural Networks | ICML 2017 | Temperature Scaling 標準引用 | https://proceedings.mlr.press/v70/guo17a.html |
| Ovadia | Can You Trust Your Model’s Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift | NeurIPS 2019 | uncertainty 在 shift 下退化 | https://proceedings.neurips.cc/paper/2019/hash/8558cb408c1d76621371888657d2eb1d-Abstract.html |
| Multi-domain TS | Robust Calibration with Multi-domain Temperature Scaling | NeurIPS 2022 | multi-domain calibration | https://proceedings.neurips.cc/paper_files/paper/2022/hash/b054fadf1ccd80b37d465f6082629934-Abstract-Conference.html |
| TransCal | Transferable Calibration with Lower Bias and Variance in Domain Adaptation | NeurIPS 2020 | calibration transfer | https://papers.nips.cc/paper/2020/hash/df12ecd077efc8c23881028604dbb8cc-Abstract.html |
| Gong | Confidence Calibration for Domain Generalization Under Covariate Shift | ICCV 2021 | domain-generalization calibration | https://openaccess.thecvf.com/content/ICCV2021/html/Gong_Confidence_Calibration_for_Domain_Generalization_Under_Covariate_Shift_ICCV_2021_paper.html |

## 12.4 Selective classification 基礎文獻

| 文獻 | 用途 | 連結 |
|---|---|---|
| On the Foundations of Noise-free Selective Classification | risk-coverage 理論基礎 | https://jmlr.org/papers/v11/el-yaniv10a.html |
| SelectiveNet: A Deep Neural Network with an Integrated Reject Option | learned reject option | https://arxiv.org/abs/1901.09192 |
| Revisiting the Evaluation of Uncertainty Estimation and Its Application to Explore Model Complexity-Uncertainty Trade-Off | AURC／risk-coverage | https://arxiv.org/abs/1903.02050 |
| How to Fix a Broken Confidence Estimator: Evaluating Post-hoc Methods for Selective Classification with Deep Neural Networks | post-hoc selector baseline | https://proceedings.mlr.press/v244/cattelan24a.html |
| Selective Classification Under Distribution Shifts | selective classification under shift | https://arxiv.org/abs/2405.05160 |

## 12.5 資料集

| 資料集 | 正式論文 | 用途與限制 | 連結 |
|---|---|---|---|
| ASVspoof 2019 | ASVspoof 2019: A Large-Scale Public Database of Synthesized, Converted and Replayed Speech | source train/dev；attack 較舊 | https://arxiv.org/abs/1911.01601 |
| In-the-Wild | Does Audio Deepfake Detection Generalize? | real-world exploratory；多種 shift 混雜 | https://arxiv.org/abs/2203.16263 |
| DFADD | DFADD: The Diffusion and Flow-Matching Based Audio Deepfake Dataset | diffusion／flow-matching；需控制 shortcut | https://arxiv.org/abs/2409.08731 |
| ASVspoof 5 | ASVspoof 5: Design, Collection and Validation of Resources for Spoofing, Deepfake, and Adversarial Attack Detection Using Crowdsourced Speech | confirmatory candidate；需做 lineage manifest | https://arxiv.org/abs/2502.08857 |

---

# 十三、正式定題前的四個 Gate

## Gate 1：Policy definition

完成唯一且可執行的：

- `s(x)`；
- `u(x)`；
- `t_m`；
- `q_m`；
- `α`；
- `β`；
- coverage constraint；
- fitting order；
- tie-breaking rule；
- no-feasible-policy fallback。

## Gate 2：Estimand

將主結果改為 teacher-relative additional transfer degradation，至少包含：

\[
G_m
\]

與：

\[
\Delta_{\mathrm{light}}
\]

## Gate 3：Method

預先固定：

- H1b baselines；
- proposed method family；
- allowed hyperparameter range；
- ablation；
- target information prohibition；
- success／failure margin。

## Gate 4：Dataset

完成 ASVspoof 5 C00：

- attack manifest；
- family definition；
- lineage evidence；
- shortcut analysis；
- exclusion rules；
- sample counts；
- statistical precision analysis。

---

# 十四、建議修訂後的論文故事

1. ADD 輕量化使本機部署可行。
2. 現有研究主要證明辨識能力與運算成本。
3. 真實系統使用的是 source 階段凍結的 operating policy，而不是 target 上重新最佳化的 EER threshold。
4. Reference detector 在 domain shift 下本來就可能失效。
5. 本研究真正關注 lightweight transformation 是否造成額外 policy-transfer damage。
6. 使用 teacher-relative transfer-gap estimand，把一般 domain shift 與 lightweight-induced degradation 分開。
7. 先測量並診斷失效。
8. 再測便宜的 source-only rank-changing repair。
9. 若仍不足，提出 error-aware policy-preserving distillation。
10. 在未見 generator family 上，以 confident-real leakage、coverage、FPR、eAURC 與 deployment cost 共同評估。

## 一句話版本

> 本研究不是單純證明輕量 ADD 在未知生成器上會變差，而是隔離並量化「輕量化本身」對 source-frozen accept／abstain policy 所造成的額外外部轉移損失，並研究能否在不使用 target labels 的條件下保留該策略。

---

# 十五、給 Codex／Claude 的第二輪審查問題

請獨立查證，不要只延續本文件的結論。

## A. Novelty

1. 是否已有研究直接比較 teacher 與 compressed／distilled student 的 selective-policy transfer？
2. 是否已有 ADD-specific abstention／selective classification method？
3. Zhou & Wang 2026 是否涵蓋 source-frozen accept／abstain policy，還是只處理分類 threshold？
4. Browser-edge ADD 是否已評估 uncertainty、abstention 或 fixed threshold？
5. 是否已有 policy-preserving distillation、risk-coverage distillation 或 error-ranking KD？

## B. Mathematics

1. `q,t,α,β` 的最佳化定義是否可行？
2. TS／Platt no-op 的必要與充分條件是什麼？
3. 當 `u(x)` 結合 distance 與 logit 時，是否必然 rank-changing？
4. `Δ_light` 是否是最適合的 comparative estimand？
5. source 與 target family 不對稱時，transfer gap 應如何定義？

## C. Statistics

1. 約 7 個 generator families 可以做哪些合理推論？
2. family bootstrap 是否適合？
3. 是否應使用 hierarchical Bayesian model？
4. threshold fitting uncertainty 如何納入？
5. practical equivalence margin 如何設定？
6. leakage 很低時，樣本數是否足夠？

## D. Dataset

1. ASVspoof 5 C00 attack IDs 是否真的可視為約 7 architecture families？
2. 各 family 是否 lineage-disjoint？
3. 是否共享 vocoder、training corpus、speaker、codec 或 base checkpoint？
4. C00 是否包含 legacy、adversarial、codec 或 partial spoof？
5. 各 family fake sample 數是否足以估計低 leakage？
6. ASVspoof 2019 與 ASVspoof 5 是否存在 lineage overlap？

## E. Method

1. Cross-fitted correctness predictor 是否已足以解決 H1？
2. proposed loss 是否只是 existing selective distillation 的重新命名？
3. correctness-ranking、selection-margin、codec consistency 各自的 closest work 是什麼？
4. 哪種機制真正具有 ADD-specific 理由？
5. 如何避免 proposed method 只靠更多參數、augmentation 或 supervision 取勝？

---

# 十六、最終結論

此題目前不應被否決。它具備：

- 清楚的部署情境；
- 可否證的核心問題；
- 可控的算力需求；
- 明確的 baseline gate；
- 有價值的 negative result；
- 潛在的方法貢獻。

但仍有三個決定性風險：

1. Novelty 可能被 threshold-transfer 與 selective-classification 前作壓縮。
2. Policy、risk target 與 primary estimand 尚未完全對齊。
3. H2 尚未被定義成可直接審查與重現的方法。

最優先修訂順序：

1. 固定 `q,t,α,β` 的 policy definition。
2. 將主 estimand 改為 teacher-relative `Δ_light`。
3. 固定 H1b baselines。
4. 限定 H2 method family。
5. 完成 ASVspoof 5 lineage／shortcut manifest。
6. 再執行小型 pilot。

完成後，本研究有機會從：

> 對 lightweight ADD 的外部可靠性量測

提升為：

> 輕量化造成的 external selective-policy degradation 分析，以及一個具有可驗證增量的策略保留方法。
