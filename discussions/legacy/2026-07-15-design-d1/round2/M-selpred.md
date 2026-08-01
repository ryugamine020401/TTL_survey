# R2 收斂：選擇性預測方法學家
日期：2026-07-15

範圍：只收斂、不加。以下逐一 (1) 點名破壞紀律的決策並給砍/收斂修正；(2) 回答指名我的提醒；(3) 對跨角色分歧的 Q 給收斂建議；末段做總 GPU-hour 對帳。

---

## 1. 破壞紀律的決策：點名 + 修正（修正方向只准砍或收斂）

### 1.1 偷加東西（增訓練成本卻非命題必需）

**V1 — FADEL 被寫成「每 backbone +1 次 full-FT 訓練」（我 R1 + P 對帳表都犯）**
- 症狀：我 R1 的 Q-SCORES 把 FADEL evidential 列為受測分數並估「+10~30 GPU-h」；P 的對帳表把「3 evidential(FADEL) full FT 6h」算進 36h 訓練欄。兩處都把 FADEL 當**新訓練的偵測器**在算，等於偷偷把一個訓練軸加進來。
- 判定：FADEL 是 B5 **Verified 的 closest work**，必列為 baseline——這一點不砍（砍了論文對「evidential SOTA 在我協定下怎麼表現」無法回答）。但「full-FT 一個 evidential 模型」是偷加的訓練成本。
- **修正（收斂到更省）**：FADEL 只做 **frozen-backbone + evidential backend**（0.3–1h/backbone，見預算表 S6），3 backbone 共 **≈1–3 GPU-h**，不是 10–30h。並且 **FADEL 不進 pilot**（pilot 只跑 post-hoc，見 P 的 Q-PILOT）。把我 R1 的「+10~30h」自我更正為 **+1~3h**。

**V2 — MC-dropout 被 P 留了條活路（「T≤10 + 抽樣子集才留」）**
- 症狀：P 的 Q-SCORES 提醒寫「MC-dropout 只在 T≤10 + 抽樣子集才留」；這是一個 P_passes×T 的乘數活口，即使 T=10，3 model × 6 格 × 10 萬池 仍 ≈+100 GPU-h（我 R1 引預算表算例 2 已算過）。留著就是留一個會被後續乘數放大的洞。
- **修正（收斂到砍）**：**MC-dropout 全砍，不留 T≤10 活口**。epistemic 家族已由 FADEL（+1 訓練、單次前向）代表，不必再付 ×T。維持 P_passes ≈ 1 是 3,500h→300h 那 12× 槓桿的核心，這個洞不能開。

**V3 — RQ3 的「~5 個可微機制」是虛列乘數（T R1 內部不一致）**
- 症狀：T 的 D-RQ3.4 寫「只攻 MSP/energy/Mahalanobis」（=3 個），但 D-RQ3.5 的成本估用「~5 可微機制」。temperature scaling 是 MSP 的單調變換（同排序、對 targeted 攻擊無獨立意義）、FADEL 是訓練分數不進對抗欄——真正可微且獨立的只有 **3 個**。用 5 個估等於虛列 1.67× 的對抗成本。
- **修正（收斂到砍）**：RQ3 對抗欄鎖 **3 個可微分數（MSP/energy/Mahalanobis）**，成本從 15–30h 下修到 **≈9–18h**。

### 1.2 算力對不上帳（同一項在不同角色被算成不同值）

**V4 — FADEL 訓練：P 算 full-FT 18h，我原算 10–30h，實需 1–3h。** 依 V1 統一為 frozen backend **1–3h**，訓練欄從 36h 降到 **≈21h**。

**V5 — P 對帳表「3 model × 6 shift 格」的 6 格來源不明。** 依 E 的 Q-SPLIT，holdout 實為 DFADD(primary) + In-the-Wild(smoke) + MLAAD v9(選配) + ASVspoof19 eval(中間參照) ≈ 4 個評估點；「6 格」疑似沿用預算表算例的佔位數。修正：**把評估 cell 數釘死為 manifest 列出的實際點數**，勿讓一個未定義的「6」當隱形乘數（此項不影響是否超支，但要消除帳面浮數）。

### 1.3 前作宣稱寫死？

**無違規。** 四角色都已把 novelty 標「待 Codex 查證」：M(A2、protocol)、E(DFADD 嚴格 unseen、protocol framing)、T(D-RQ3.1 vs CLAD/reject-option)、P(fixed-threshold transfer protocol)。E R1 line 20 對「DFADD vocoder 屬 2019 後、不在種子集」的敘述已由同檔「須記錄不得斷言／在此之前不寫嚴格 unseen」自我約束，可接受。此區無需砍。

---

## 2. 回答指名我的提醒

- **E → M（Q-SCORES：ensemble/MC-dropout 不得進 pilot split）**：接受，且更強——不只不進 pilot，**全論文都砍 MC-dropout、砍 deep ensemble**（見 V2）。pilot 只需單一 frozen checkpoint 的 post-hoc 分數建 threshold-transfer 與 base-AUROC gate。
- **E → M（Q-RQ2：固定同一 frozen backbone + 同一 pooled 特徵 + 報 representation-quality 控制）**：完全一致，即我 R1 Q-RQ2 決策。鎖死：density(Mahalanobis) 與 discriminative(MSP/energy/temp) 皆從**同一次前向**衍生，base AUROC/EER 當協變量報告。
- **T → M（Q-SCORES：若留 MC-dropout/ensemble 須明記不進 RQ3）**：已 moot——兩者全砍，RQ3 對抗欄本就只在 3 個可微 post-hoc 上（見 V3）。
- **T → M（Q-RQ2：RQ3 排序翻轉須先控制 backbone）**：一致。RQ2 的共用 frozen 表徵設定同時服務 RQ3；未控制前不解讀「翻轉」。
- **P → M（Q-SCORES：ensemble 砍、MC-dropout T≤10 保留）**：**部分不接受**——deep ensemble 砍(同意)，但 MC-dropout **不留 T≤10 活口，全砍**（V2，往更小收）。
- **P → M（Q-METRIC：primary 只能一個 = risk-constraint violation）**：完全一致，即我 R1 決策。

---

## 3. 跨角色分歧 Q 的收斂建議（一律往更小/更省收）

**Q-SCORES（M vs P 分歧在 MC-dropout）** → 收斂：最終分數集 = **MSP + temperature scaling + energy + Mahalanobis-on-SSL（post-hoc 四件套，+0h）+ FADEL（frozen backend，+1~3h）**；**MC-dropout、deep ensemble 全砍**。理由：維持 P_passes≈1，唯一訓練增量是 FADEL frozen backend。

**Q-METRIC（M、E、P 已趨同）** → 鎖死：primary = **development-fixed 操作點的 risk-constraint violation，統一記號 Δr（配對報 Δc）**；violation 判定 = per-generator-family stratified bootstrap(1000×) 95% CI 下界 > 0；AURC + ECE 降為**分解失效用的次要診斷**；fixed-FPR≤1% selective recall 僅作單一操作點實例。base-AUROC gate 先報。三角色文字統一為此，不再並列三個 primary。

**Q-PILOT 的分數與 gate（M、E、P 各給了一片）** → 收斂：
- 分數鎖 **MSP + Mahalanobis-on-SSL 兩種**（讓 RQ2 兩家族在 pilot 就同時被行使）；FADEL、第二 detector 皆**不進 pilot**（那是全論文）。
- **AUROC gate 消除模糊帶**：P 的 success 用 ≥0.75、stop 用 <0.6，中間 [0.6, 0.75) 無定義。收斂為：**success 需 ≥0.75；hard-stop <0.6；[0.6, 0.75) 標 marginal（單 detector 不足以定案，須進全論文加第二 detector 再判）**，避免灰帶被兩讀。
- 兩個 risk target = 5% / 10%（三角色一致）。

**Q-RQ3 樣本/機制** → 收斂：可微分數 **3 個**（V3），fake 子集 n≈2,000–5,000（不攻全集），white-box PGD、2–3 個 SNR 錨定 ε、不穿 codec、reuse dev-fixed τ 為 confident-real 目標邊界。成本 ≈9–18h。

**channel/codec 軸** → 收斂：direction #1 主軸是 generator shift，channel 僅單一協變量；**neural codec transcode 鎖抽樣子集、至多 1–2 條件（S10），不進 pilot**（E 已砍 pilot 的 codec，全論文保留為協變量）。

---

## 4. 總 GPU-hour 對帳（守 430–520h 封套？）

以收斂後單價重算全論文核心：

| 科目 | 收斂後配置 | GPU-h |
|---|---|---|
| 訓練 | 3 base × 6h(full FT) + 3 FADEL frozen backend × ~1h（V1/V4） | ≈21 |
| 前處理 | SSL pooled 特徵抽取 + neural codec transcode 子集 1–2 條件（V-channel, S10） | 20–30 |
| 評估 | 3 model × 實際 cell 數(~4–6) × 子集 × 0.6，post-hoc 共用單次前向 | ≈11 |
| 對抗(RQ3) | 3 可微分數 × ~5k × 3 model × 2–3 ε，recipe-level（V3） | 9–18 |
| confound | UTMOS + ECAPA 品質協變量（E 主責） | 3–6 |
| **核心小計** | | **≈64–86** |
| 選配·多 seed | 若採 3 seed 訓練（非預設，deterministic+bootstrap 為預設） | +36 |
| **含多 seed** | | **≈100–122** |

**結論：不超。** 核心 ≈64–86h（含選配多 seed ≈100–122h），**遠在 430–520h 封套內**，差額全數為除錯/重跑/15% 緩衝，非新增實驗許可。相較 P R1 的 120–130h，我的收斂再省下 FADEL full-FT(~15h) 與 RQ3 虛列機制(~7–12h) 兩筆。**沒有任何一項需要砍來救預算**（因為根本沒超）；上述砍項全是為守「P_passes≈1」與「消除帳面浮數/虛列乘數」的紀律，不是為省封套。

---

## 回傳摘要（見任務要求的純文字，另附於對話回覆）
