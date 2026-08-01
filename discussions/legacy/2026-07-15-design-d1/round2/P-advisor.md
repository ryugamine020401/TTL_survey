# R2 收斂：指導教授（範圍/貢獻把關）
日期：2026-07-15

範圍：本檔只做收斂，不加任何東西。三件事：(1) 點名會破壞紀律的決策並給「只砍/只收斂」的修正；(2) 回答指名 P 的提醒；(3) 對跨角色分歧的 Q 往「更小、更可執行、更省算力」收。所有 GPU-hour 用 `01-compute-budget.md` §5 公式對帳，硬守 430–520h 上限。

前置判定：**四份 R1 高度對齊，沒有任何一項造成預算超支（總和遠在上限內）。真正的風險不是超支，是幾處「順手加的分析軸」與「重複計數的乘數」——以下逐一砍回。**

---

## 一、破壞紀律的決策：點名 + 只砍/收斂修正

### V1【偷加·E】UTMOS + ECAPA 品質協變量進 pilot
E 的 leakage/confound 把「UTMOS + ECAPA speaker-similarity」沿用方向#3 recipe，並算進 pilot（1–2h）。
- **問題**：pilot 的唯一任務是 go/no-go，其 confound gate 只需 duration / 取樣率 / speaker-overlap / source-corpus（全部是 metadata，CPU，0h）。UTMOS/ECAPA 是從**另一個方向**借進來的新分析軸，pilot 用不到。
- **修正（砍）**：**UTMOS/ECAPA 逐出 pilot**；只在全論文的 confound panel 保留，且封頂 ≤6h。pilot confound 只吃零成本 metadata。省 pilot 1–2h，並防止品質軸在 pilot 期就長大。

### V2【重複計數·P自己 + T】RQ3 對抗「5 機制」灌水
P 的對帳表與 T 的 D-RQ3.5 都寫「PGD × 5 可微機制」，但 T 的 D-RQ3.4 明定被攻擊集合只有 **3 個可微 post-hoc（MSP / energy / Mahalanobis）**。且 temperature scaling 對 MSP 是單調變換、排序等價，攻擊上冗餘。
- **修正（收斂）**：RQ3 攻擊機制**鎖 3 個**（MSP / energy / Mahalanobis），對帳數字從「×5」改「×3」。RQ3 從 13–30h 收到 **≈8–13h**。

### V3【重複計數·M vs P】FADEL evidential 的訓練成本兩套帳
P 對帳把 3 個 FADEL 當 full-FT 6h（含在 36h 訓練裡）；M 主張 frozen-backbone + evidential backend（0.3–1h/次）。同一項兩個價。
- **修正（收斂到便宜側）**：FADEL **一律 frozen-backbone evidential backend**（S6），3 個 ≈3h 而非 18h。省 ≈15h。這也符合預算表「frozen 在資料受限時可能更好」的鐵律。

### V4【可砍的乘數·P自己】+2 seed 訓練 +36h 灌進核心
P 把「+2 seed × 3 detector = +36h」算進 120–130h 核心。Codex §9 點 4 明說統計可信度可用「**多 seeds 或 deterministic baseline**」二擇一。
- **修正（收斂）**：**預設 deterministic baseline + bootstrap CI**，多 seed 移出核心、降為「僅當某一 claim 需要 seed 變異才啟用」。核心立刻 −36h。

### V5【殘留的魔術數字·P】評估「6 shift 格」未對應到實際 holdout
「3 model × 6 格」的 6 是從預算表算例2 的舊 6-shift 網格搬來的，但本設計的 holdout 是 DFADD（generator）+ MLAAD v9（多語·選配）+ In-the-Wild（smoke）+ ≤2 通道協變量條件，不是 6 格。
- **修正（收斂·對帳衛生）**：評估格數釘死到**實際 holdout 清單**，不沿用魔術 6。數字不變大（仍 ~11h），但帳要對得上，避免日後被當「加條件」的授權。

### V6【范圍蠕變風險·全論文通道軸】neural codec 前處理 20–30h 需設硬上限
本方向主軸是 **generator shift**；通道是「單一協變量」（verified 定稿 RQ1 的 unseen-channel 只是次軸）。P 前處理列 neural codec 100k×2 條件。
- **修正（設帽）**：通道**封頂 ≤2 個 codec 條件、只在 20k 子集**（S10），且明文標「次要協變量，時間不夠即降 future work」。**任何 codec×bitrate 網格化當場砍**（那是方向#2/#4 的領地）。維持 ≤20h。

### 前作宣稱檢查：四份都合格
M（A1/A2 protocol novelty）、E（DFADD 嚴格 unseen）、T（A3 confident-real）、P（fixed-threshold transfer）**全部標「待 Codex 查證」，無人寫死**。唯一要盯：E 的 manifest 措辭「確認後者確實不在種子攻擊集」偏強，**改為「manifest 逐項記錄、Codex 核可前不斷言 unseen」**——這是措辭收斂，不是砍實驗。

---

## 二、回答指名 P 的提醒（各一句確認）

- **T→P（RQ3 定位）**：確認。RQ3 是「對抗欄」**診斷讀數**，不是新攻擊貢獻、不進 C1–C4 的 method 欄；primary claim 只鎖 transfer / risk-violation。已寫入 Q-CONTRIB。
- **M→P（Q-PILOT 分數指定）**：接受。pilot 兩分數**釘死 = MSP + Mahalanobis-on-SSL**（同一 frozen 表徵，pilot 就行使 RQ2 兩家族）；risk target 5%/10%；success 掛 base-AUROC gate。
- **M→P（C4 需 gate）**：接受。C4 負結果**只在 base-AUROC gate 通過時成立**；primary claim 直接內嵌該 gate（見下），使「全不可轉移」不與「偵測器近隨機」混淆。
- **E→P（Q-PILOT 雙 gate）**：接受。pilot success/stop **加 leakage gate**：Δr 須 within-stratum 存活（非 duration/取樣率/corpus 捷徑），與 base-AUROC gate 並列為前置條件。
- **E→P（primary claim 用 Δr+CI 陳述）**：接受。primary claim 改以 Δr 及其 per-generator bootstrap CI 下界表述（見下）。

**收斂後 primary claim（可雙向證偽）**：
> 在 dev 固定的 risk 操作點 τ（r*∈{5%,10%}）、完全不以 holdout 調參，轉移到 generator-disjoint、時間較新的 holdout 時，**在通過 base-AUROC gate 且 within-stratum 存活的前提下，Δr = r_obs − r* 的 per-generator bootstrap CI 下界 > 0**（系統性違約）。若 Δr 的 CI 涵蓋 0 或落於負區 → 閾值可轉移，論文轉正面結論；兩向皆成篇。

---

## 三、跨角色分歧 Q 的收斂建議（往更小/更省收）

四份對齊度高，實質分歧只有兩處，其餘為「同義不同寫法」的統一：

- **Q-METRIC（M vs E 措辭）**：兩人 primary 都選 risk-constraint violation，AURC/ECE 降診斷——**已收斂**。統一採 **E 的完整記法**：Δr = r_obs − r*，配對 Δc，per-family stratified bootstrap（1000×）CI，base-AUROC gate 先報。**唯一要釘死的分歧：risk 的定義**——M 寫「selective error/FPR」、E 寫「selective risk」。**收斂為單一定義：risk = selective miss rate（accept 區內 fake 被當 real 放行的比例）**，即部署安全閥真正在意的量；不三種並列。
- **Q-SPLIT（E 砍 speaker-disjoint 硬 gate vs M 憂 density 受 corpus 重疊污染）**：**收斂**——採 E 的「分層報告取代排除控制」（省資料、對 generator-transfer claim 反而保守），但 manifest **必須把 source-corpus/bona-fide 重疊列為明確 stratum**，且 Mahalanobis（density）結果**只在 within-corpus-overlap stratum 內解讀**（滿足 M 的顧慮）。兩人設計相容，不需加實驗。
- **Q-SCORES（P 曾留 MC-dropout T≤10 後路 vs M 全砍）**：**收斂到 M 的更嚴版**——deep ensemble 與 MC-dropout **兩者全砍**，不留 T≤10 後路（維持 P_passes≈1，這是 3,500→300h 那 12× 槓桿的命脈）。epistemic 家族由 FADEL evidential（frozen backend）單獨代表。
- **Q-RQ2 / Q-RQ3**：無實質分歧。RQ2 統一「同一 frozen backbone、同一次前向衍生兩家族、base AUROC 當協變量」；RQ3 統一「復用 dev-fixed τ + 同一 Δr metric、white-box PGD、3 機制、recipe-level、無 codec」。

---

## 四、總 GPU-hour 對帳（守 430–520h）

套用 V1–V6 的砍/收斂後：

| 科目 | 收斂後配置 | GPU-h |
|---|---|---|
| 訓練 | 3 base detector full-FT 6h + 3 FADEL frozen backend 1h（V3） | 21 |
| 前處理 | SSL pooled 特徵抽取 + neural codec ≤2 條件 @20k 子集（V6 封頂） | 15–20 |
| 評估 | 3 model × 實際 holdout 格 × 20k 池，post-hoc 共用單次前向（V5） | 11 |
| 對抗 RQ3 | PGD-50，5k 樣本 × 3 model × **3** 機制，recipe-level（V2） | 8–13 |
| 全論文 confound | UTMOS+ECAPA 僅全論文、封頂（V1） | ≤6 |
| **核心小計（deterministic 預設，V4 多 seed 移出）** | | **≈ 60–70** |
| 選配·多 seed（僅特定 claim 需要時啟用） | +2 seed × 3 detector × 6h | (+36) |

**我認為的總 GPU-hour**：
- **核心 ≈ 60–70 GPU-h**（deterministic baseline 預設）；含選配多 seed ≈ 100h。
- **含除錯/重跑緩衝的實際預期 ≈ 150–250 GPU-h**。
- **穩守 430–520h 上限，無超支；反而餘裕極大（~300h headroom = 純緩衝，非加實驗許可）。**
- 不需為預算砍任何科學內容；唯一風險是餘裕被當成擴 scope 的藉口——上述 V1–V6 正是把餘裕鎖成緩衝。

---

## 回傳摘要

**砍/收斂項（每項 ≤30 字）**
- V1 砍：UTMOS/ECAPA 逐出 pilot，只留全論文 confound（≤6h）。
- V2 收斂：RQ3 攻擊機制 5→3（MSP/energy/Mahalanobis），對帳去灌水。
- V3 收斂：FADEL 一律 frozen backend，18h→3h。
- V4 收斂：預設 deterministic+bootstrap，多 seed 移出核心（−36h）。
- V5 收斂：評估「6 格」釘死到實際 holdout 清單，去魔術數。
- V6 設帽：通道 neural codec ≤2 條件@20k 子集，禁 codec 網格。
- Q-METRIC 收斂：risk 單一定義 = selective miss rate；採 Δr+CI 記法。
- Q-SPLIT 收斂：分層報告取代 speaker 排除；density 只讀 within-corpus-overlap stratum。
- Q-SCORES 收斂：deep ensemble 與 MC-dropout 全砍，不留 T≤10 後路。
- 措辭收斂：E manifest 改「Codex 核可前不斷言 unseen」。
- primary claim 收斂：內嵌 base-AUROC gate + within-stratum + Δr CI 下界>0，可雙向證偽。

**我認為的總 GPU-hour：核心 ≈ 60–70h（含選配多 seed ≈100h），含除錯/重跑實際預期 ≈ 150–250h，穩守 430–520h 上限、無超支。**
