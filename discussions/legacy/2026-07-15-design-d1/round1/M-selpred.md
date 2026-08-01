# R1 設計立場：選擇性預測方法學家
日期：2026-07-15

角色：M（選擇性預測/uncertainty 方法學家）
主責 Q：Q-SCORES、Q-RQ2、Q-METRIC
紀律遵守：單一決策非選項清單；只砍不加；每項增訓練即算 GPU-hour（守 430–520h）；涉前作/novelty 標「待 Codex 查證」；社會意義不進實驗。

---

## Q-SCORES — 最終納入的棄權分數集合

### 單一決策
納入 **5 種**，且明確分成「零邊際 GPU 的 post-hoc 四件套 + 一個要訓練的 evidential」：

| # | 分數 | 家族 | 成本性質 |
|---|---|---|---|
| 1 | **MSP**（max softmax prob） | discriminative-derived | post-hoc，共用同一次前向的 logits |
| 2 | **Temperature scaling** | discriminative（校準後） | post-hoc，dev 上擬合單一 T，離線 |
| 3 | **Energy score** | discriminative-derived | post-hoc，同一 logits |
| 4 | **Mahalanobis-on-SSL** | **density-based** | post-hoc，同一 pooled embedding 擬合高斯，CPU |
| 5 | **FADEL evidential** | epistemic（evidential DL） | **每 backbone +1 次訓練**，但推論單次前向 |

（softmax entropy 只作 MSP 的免費變體報告，不算獨立方法。）

**被砍掉的兩個候選，及為何砍：**
- **Deep ensemble（砍）**：= (E−1)×N_backbone 額外訓練 + 推論 ×E。以 E=5、3 backbone 估 ≈ +72–120 GPU-h 訓練，且推論乘 5；預算表法則 3 明言「通道擴增訓練 XOR deep ensemble，二選一」，本方向已把 shift 網格放在評估側。它不回答本論文的 RQ（門檻轉移，不是 epistemic SOTA），故砍。
- **MC-dropout（砍）**：P_passes 直接 ×T。即使 T=10，3 模型 × 6 shift 格 × 10 萬筆抽樣池就 **+約 100 GPU-h**（見預算表算例 2）。算例 1→算例 2 的 3,500→300h 有 12× 來自「把 P_passes 壓回 1」——MC-dropout 是唯一會破壞這個槓桿的候選。epistemic 家族已由 FADEL evidential 以「+1 訓練、單次前向」代表，不必再付 ×T 的乘數。

### 一句理由
post-hoc 四件套靠預算表 S1（快取 logits+pooled embedding、全部共用一次前向）邊際成本為零、砍它們不省錢；FADEL 是 Codex B5 **Verified 的 closest work**、必列 baseline；deep ensemble 與 MC-dropout 是唯二會把 430–520h 預算炸開的乘數項且不服務本論文 RQ，故砍。

### GPU-hour 影響
- post-hoc 四件套：**+0 GPU-h**（S1）。
- FADEL evidential：**每 backbone +1 次訓練**；儘量用 frozen-backbone + evidential backend（0.3–1h/次），2–3 backbone 估 **+10~30 GPU-h**。
- 砍 deep ensemble 省下 ~70–120h；砍 MC-dropout 省下 ~100h（維持 P_passes≈1）。

### 待 Codex 查證
FADEL/Salvi(2023)/Pascu(2024) 三者列 closest work 已由查證定稿確立；**分數集合本身不宣稱 novelty**，只作為 protocol 的受測對象。不需額外查證。

---

## Q-RQ2 — density vs discriminative 的公平比較（控制 backbone 與 representation quality，Codex A2）

### 單一決策
兩家族分數**一律從同一個 frozen backbone checkpoint 的同一次前向快取衍生**：discriminative 分數（MSP/energy/temperature）取自分類頭 logits；density 分數（Mahalanobis）擬合在**同一組 pooled SSL embedding** 上。**不另訓練 density model、不另換 backbone**。並把該共用 backbone 的 base AUROC/EER 當**協變量報告**，使任一家族分歧可歸因於「分數型別」而非「模型容量/embedding 品質」。

**被砍掉的做法：** 為 density 分數另建/另訓一個表徵或 backbone（會直接落入 A2 指出的「結論只是模型容量差異」陷阱，砍）。

### 一句理由
Codex A2 明示：不控制共同 backbone 與 representation quality，density vs discriminative 的排序分歧「可能只是 embedding 品質差異」；共用 checkpoint（預算表 S4）是唯一能把比較鎖在分數型別上的設計。

### GPU-hour 影響
**+0 GPU-h**。這是「分數怎麼衍生」的約束，全部來自 Q-SCORES 已快取的同一次前向，離線在 numpy/CPU 完成。

### 待 Codex 查證
**是。** A2 狀態為 **Unknown**——「density vs discriminative 在同一 unseen-generator protocol 下分家」不得宣稱首次/nobody-asked（TADA、Open-Set Source Tracing、FADEL 皆鄰近）。RQ2 作為研究問題可保留，novelty 措辭待 Codex 查證後定稿。

---

## Q-METRIC — primary metric 與 risk-constraint violation 的量測

### 單一決策
**Primary metric = development-fixed operating point 下的 risk-constraint violation Δ。**
定義：在 dev 上選使 selective risk 達目標 r*（如 selective error/FPR ≤ 目標）的棄權門檻 τ，**凍結 τ、完全不以 holdout 調參**；在 unseen-generator holdout 上報告
　**Δ = R_holdout(τ) − r***（違約量），並同時報 τ 下的 **coverage**。
**支援診斷（非 primary）：** AURC（threshold-free 的 ranking 品質）與 ECE（校準），用來把失敗**拆解**成 ranking collapse vs calibration shift（對應貢獻 C1）。fixed-FPR≤1% selective recall 只作「其中一個操作點」的實例呈現。
**報告規格：** per-generator-family bootstrap CI on Δ；並掛 **base-AUROC gate**（backbone 接近隨機時 Δ 無意義，該格作廢）。

**被砍掉的兩個候選 primary，及為何砍：**
- **AURC 當 primary（砍）**：AURC 是 threshold-free、只量 ranking 品質，**偵測不到本論文要問的失敗模式**（固定門檻是否守住預宣稱風險上限）。題目就叫 *Cross-Dataset Risk Violations*，primary 必須是違約量。AURC 降為診斷。
- **fixed-FPR≤1% selective recall 當 primary（砍）**：它固定的是 FPR 而非**風險目標**；而本論文「預先聲明並凍結」的是 risk target，故 recall 只作操作點實例，不作 primary。

### 一句理由
本論文的可證偽命題是「dev 固定的棄權門檻轉到較新、generator-disjoint holdout 後是否仍滿足預宣稱 accepted-risk 上限」（查證定稿第一句話 + Codex §9.2 C1/C2），唯一能直接量這件事的是 risk-constraint violation Δ；AURC/ECE 只能診斷「為什麼違約」。

### GPU-hour 影響
**+0 GPU-h**。全部 metric 由已快取分數離線計算（bootstrap CI 亦 CPU）。

### 待 Codex 查證
**是。** A1：一般「selective ADD」已 Refuted（Salvi/Pascu 已畫 rejection curve）；但「**固定門檻的跨世代 risk-constraint transfer protocol**」為 residual gap（Unknown）。把「risk-violation transfer protocol」寫成貢獻前，須待 Codex 查證是否已有等同 fixed-threshold + newer-holdout + risk-violation 的前作（查證定稿轉向條件亦以此為據）。

---

## 對其他 Q 的風險提醒（各一句，指名角色）

- **給 E（Q-SPLIT / leakage）**：Mahalanobis-on-SSL 是 density 分數，對 **backbone 訓練語料的 bona-fide 來源重疊**特別敏感——若 DFADD 的 LJSpeech/VCTK 真實語音與 ASVspoof19 種子重疊，density 的「unseen 訊號」會被污染（Codex E1「名字新≠嚴格 unseen」），split manifest 請控制 bona-fide 來源重疊而不只是 TTS 系統名。
- **給 E（Q-METRIC 共主責）**：risk-violation Δ 的 CI 要能分辨 5–40 個百分點量級的 shift 效應，分層抽 2 萬筆（預算表 S2，SE≈±0.4%）足夠、且必須固定 seed 並在 paper 明寫，勿為了「更準」退回全集（DF 611k 會被每個乘數乘一次）。
- **給 P（Q-PILOT）**：pilot 的「一個 embedding score」請**指定為 Mahalanobis-on-SSL**、另配 **MSP**，讓 RQ2 的兩家族在 pilot 就同時被行使；兩個 risk target 用 5%/10%（Codex §10），success gate 掛 base-AUROC。
- **給 P（Q-CONTRIB）**：負結果貢獻 C4（「所有門檻都不可轉移」）**只有在 base-AUROC gate 通過時才成立**——我的 Q-METRIC gate 正是它的前提，可證偽的 primary claim 一句話請直接引用該 gate，否則「全失敗」會與「偵測器接近隨機」混淆。
- **給 T（Q-RQ3）**：confident-real 攻擊的成功指標請**復用我的 dev-fixed τ 操作點**（量「被推到 τ 以下、進 confident-real 的比例 / 對抗欄下的 risk-violation」），不要另立一個獨立 AUROC；搜尋維持 recipe-level、明定 query/quality budget（預算表 S8/R8），否則排序翻轉的結論不可比。

---

## 主責決策一行版 + GPU-hour 小計

- **Q-SCORES**：納 MSP + temperature scaling + energy + Mahalanobis-on-SSL（post-hoc 四件套，+0h）+ FADEL evidential（每 backbone +1 訓練）；**砍 deep ensemble、MC-dropout**（唯二會炸預算的乘數且不服務 RQ）。
- **Q-RQ2**：density 與 discriminative 分數一律從**同一 frozen backbone 的同一次前向**衍生、base AUROC/EER 當協變量報告（+0h）；答 Codex A2，novelty 待查證。
- **Q-METRIC**：primary = **development-fixed 操作點的 risk-constraint violation Δ + coverage**，AURC/ECE 降為診斷，fixed-FPR selective recall 僅作操作點實例，掛 base-AUROC gate 與 per-generator bootstrap CI（+0h）；protocol novelty 待 Codex 查證。

**GPU-hour 小計（我主責決策的淨增量）：+10~30 GPU-h（僅 FADEL evidential 訓練），其餘全部 +0h。**
關鍵貢獻不是省了多少，而是**維持 P_passes ≈ 1**（砍掉 MC-dropout/ensemble 乘數，避開 3,500h→300h 那 12× 的元凶），使全方向守在 430–520h 內。
