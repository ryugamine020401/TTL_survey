# S-sequential 統計方法學家席（Round 1）

日期：2026-07-23。已讀 Gate 三席判決；接受 P/L 的 OS-privileged on-device 錨定（8kHz、單通道、逐秒前綴、離線模擬），在此場景下發言。

## 立場摘要

1. 「聽到第幾秒才 commit」可以形式化成乾淨的 sequential estimand，但**必須把整個停止策略（stopping policy）當作校準單位**，而非逐前綴各自校準——後者因資料相依停止（optional stopping）產生選擇偏誤，承諾會漏。
2. 「anytime」有兩個不同的統計意義，混用是審稿死穴：SAVI/e-process 的 anytime-valid 是跨樣本累積的，**不適用於單通話內相依音框**；通話內的 anytime 要靠有限 τ 網格上的 policy-level 校準（Learn-then-Test 路線）取得有限樣本保證。
3. defensible 與數值遊戲的分界＝三個預先登記的測試（可復現性、支配性、承諾轉移），缺一即退化為「把音訊切短再測」。
4. 與 proposal-final 的 UCB policy fitting 是**直接推廣**而非衝突：決策變數從 (q,t) 變成低維參數化的曲線 (q_τ, t_τ)，Δ_light 照搬。

## 主體分析

### 1. 形式化草案

- 前綴網格 τ ∈ T = {τ₁,…,τ_K}（建議 K≤8，如 1–8 秒逐秒），串流分數過程 s_τ(x) = s(x_{≤τ})，selector u_τ(x)。
- 凍結策略 π_θ，θ = {(t_τ, q_τ)}：在每個 τ，若 s_τ≥t_τ 且 u_τ≥q_τ → commit「發現合成證據」；若 real 方向同理 commit「未發現」；否則繼續聽；到 τ_K 強制三態（含棄權→升級查證）。commit 後決策終局。
- 停止時間 T(x) = 首次觸發 commit/升級的 τ，**是資料相依的隨機變數**。
- 主 estimand（policy-level anytime leakage）：`L_CR^seq(π) = P_fake(在 T 時 commit 為 accept-as-real)`，隨機性來自通話（utterance）分佈，不是通話內時間。風險承諾 = 對整個 π 承諾 `UCB_{1-δ}[L_CR^seq] ≤ α`，另加 halt-time 分桶的條件版（見 §2b）。
- 「第幾秒才有資格」的乾淨定義：`τ*(α) = min{τ : dev 上存在可行 (t_τ,q_τ) 使該桶條件洩漏承諾 ≤ α}`——這是研究輸出（一條可報告的量），不是輸入假設。

### 2. 統計機器是否撐得住「任意時刻停下都守住 α」

- **Verified**：anytime-valid 推論（e-process、confidence sequences）的成熟綜述為 Ramdas, Grünwald, Vovk & Shafer, "Game-Theoretic Statistics and Safe Anytime-Valid Inference," Statistical Science 38(4), 2023（https://projecteuclid.org/journals/statistical-science/volume-38/issue-4/Game-Theoretic-Statistics-and-Safe-Anytime-Valid-Inference/10.1214/23-STS894.full ；arXiv:2210.01948；查證 2026-07-23）。其有效性建立在跨樣本的 test martingale 上。**Inference**：單一通話內的逐秒音框高度相依、似然比不可得，score 過程 s_τ 不是 martingale，直接在通話內套 e-process/Ville 不成立。SAVI 真正可用之處是跨通話的部署監測（如 Conformal Selective Acting, arXiv:2605.20270，per-round e-process 做串流風險控制，查證 2026-07-23）——那是加分項，不是主保證。
- **Verified**：通話內資料相依停止的正確先例是 Ringel, Cohen, Freedman, Elad & Romano, "Early Time Classification with Accumulated Accuracy Gap Control"（arXiv:2402.00857，ICML 2024；查證 2026-07-23）：用 Learn-then-Test 校準停止規則，給有限樣本、distribution-free 的保證，且**條件在累積停止時間上**控制——正是防止「早停桶風險超標、靠晚停桶平均掩蓋」。我方主保證應走這條路線：有限 τ 網格 + policy-level（或 halt-time 分桶）約束 + δ 沿網格分配（union bound）。
- **Verified**：within-sequence 早判的深度學習先例 SPRT-TANDEM（arXiv:2006.05587，ICLR 2021 spotlight；查證 2026-07-23）放寬 SPRT 的 iid 假設，但其誤差控制是漸近/啟發式，非有限樣本 distribution-free——可作 policy 基線，不可作保證來源。
- **關鍵誠實聲明（Inference）**：LTT 式保證的有效性建立在 dev 與部署通話同分佈；未見生成器下它**會**破——但這不是缺陷，這正是論文問題本身：「凍結的 sequential policy 承諾在 shift 下守不守得住」，與 proposal-final 的 source-frozen transfer 完全同構。
- **兩種停止情境要分開承諾（Inference）**：(a) 系統決定停 → policy-level 單一 α；(b) 外生停止（對方掛斷；紅隊注意：**攻擊者控制通話長度**）→ 需 sup_τ 型保證，靠網格 union bound。(b) 才是「anytime」名副其實之處，也是對 D 席攻擊面的統計回應。

### 3. Peeking penalty：本題最可量測的新量

逐 τ 邊際校準（每個 τ 各自守 α）+ 資料相依停止 ≠ 整體守 α：commit 事件系統性選中「分數路徑早穿越門檻」的通話。定義 **optional-stopping inflation = policy-level 實際洩漏 − 逐 τ 名目承諾**。這個量：(i) 可在 dev/target 上直接量測；(ii) 是「sequential 框架有無內容」的實證判準；(iii) 據 G 席檢索，未在 ADD 出現過（弱否定下的 Hypothesis）。

### 4. defensible vs 數值遊戲的分界（三測試，須預先登記）

1. **可復現性測試**：若全部結果可由「獨立評測各固定長度裁切」重生成，即為 Shi et al.「Hi!」的地盤，無新意。必要條件＝存在資料相依 T 且報告 peeking inflation。
2. **支配性測試**：在同一 α 下，自適應停止必須在 (coverage, E[T]) 上 Pareto-支配最佳固定 τ 策略；不支配則 sequential 無附加值。
3. **承諾轉移測試**：主 endpoint 是凍結 sequential policy 在未見生成器族上的 family-macro 實際洩漏是否 ≤ α，及 Δ_light 的 sequential 版——這才接回論文命脈。

### 5. 前綴長度是新增軸，不是取代

coverage 由純量變成隨 τ 的函數，操作面成為 (α, coverage, E[T]) 三維面。為防組合爆炸：主 endpoint 固定為純量（policy-level family-macro L_CR^seq @ 凍結 α），coverage 與 E[T] 作聯合約束（防「全棄權」與「全拖到 τ_K」兩種作弊），曲面只作 secondary 圖表。

### 6. 與 UCB policy fitting 的銜接

同一個約束最佳化程式，`argmax Coverage s.t. UCB[L_CR^seq]≤α, FPR≤β`，決策變數從 2 個變 2K 個 → dev 過擬合風險上升。處方：單調/低維參數化（如 t_τ 單調遞減的兩參數族）、family bootstrap 每次重擬整條曲線（proposal-final §10 原則直接沿用）。成本衝突：評測推論量 ×K，且 wav2vec2 非串流架構須逐前綴重算——這是 A/C 席的地盤，我只標記為可行性前提。

## 對候選研究問題的具體修改

保留「串流前綴 → anytime 三態」，但改寫為：**「來電場景（OS-privileged on-device、8kHz 前綴串流）下，source-frozen 的 sequential selective policy——含資料相依停止時間——其風險承諾在未見生成器上是否轉移；τ*(α) 與 optional-stopping inflation 為新增可報告量。」**保證框架明寫 Learn-then-Test 式有限樣本校準（引 Ringel et al.），不得宣稱 e-process/SAVI 於通話內成立；SAVI 僅限跨通話監測作 optional extension。

## Kill conditions

1. dev 實測顯示 τ < τ_K 時無任何可行 commit 點（短前綴分數太不穩）→ 退化回 proposal-final 全長版。
2. peeking inflation ≈ 0 且自適應停止不支配最佳固定 τ → sequential 框架空心，kill。
3. τ 網格 ×K 的推論成本破 4090/一年日曆預算。
4. G 席補檢索發現 ADD 已有 LTT/conformal 式資料相依停止 + 風險控制的工作 → gap 已被佔。

搜尋詞記錄：`anytime-valid inference e-process confidence sequences Ramdas survey 2023`；`anytime-valid risk control conformal "risk control" sequential streaming`；`SPRT-TANDEM sequential density ratio estimation early classification ICLR`；`early classification of time series reliability guarantee data-dependent stopping conformal`。

## 給下一波的一句話

給 A/C：一切保證都以「K≤8 個前綴點上能以可承受成本重算分數、且短前綴分數不完全崩壞」為前提——請先量 1–4 秒 8kHz 前綴上 SSL 偵測器的分數穩定性與逐前綴推論成本，這決定我的形式化是活是死。
