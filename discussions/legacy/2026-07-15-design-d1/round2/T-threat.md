# R2 收斂：威脅模型設計者
日期：2026-07-15

範圍：我只收斂 RQ3（confident-real 壓力測試讀數）並行使「點名破紀律決策」的把關職責。全程只砍/收斂，不加。

---

## A. 破壞紀律的決策：逐一點名 + 修正（修正只能是砍或收斂）

### A1【偷加·category error】RQ3 攻擊被寫成「recipe-level」
- **點名**：M 給 T 的提醒（M-selpred §對 T）「搜尋維持 recipe-level」；P 對帳表把「對抗（RQ3）」標為「recipe-level」。
- **問題**：recipe-level 是方向#2 的 **laundering 洗刷配方**概念（一條 pipeline 套全部樣本，`01-compute-budget.md` §4.4/§4.5/S8）。RQ3 是 **white-box gradient PGD**，本質就是 per-sample 梯度上升；把它叫 recipe-level 是把方向#2 的 threat model 混進來，違反範圍鎖定。
- **修正（收斂）**：RQ3 = **per-sample 白盒 PGD-50**，明文寫「非 recipe-level、非 laundering」。注意 per-sample **PGD 不是紅線 R7**——R7 只針對「laundering 搜尋內嵌白盒最佳化」；純 PGD 5k 樣本在預算表 §4.4 只 6–13h，合法且便宜。

### A2【偷加·攻擊面膨脹】RQ3 攻擊機制被寫成「5 機制」
- **點名**：P 對帳表「5,000 樣本 × 3 model × **5 機制**」。與我 R1 D-RQ3.4 的「只攻可微 post-hoc 子集（MSP/energy/Mahalanobis）＝3 個」不一致。
- **問題**：5 是把 M 的完整 Q-SCORES 集合（含 temperature scaling、FADEL）誤搬進對抗欄。temperature scaling 與 MSP **單調等價**（同一 logits 的溫度縮放，決策門檻下排序不變），不構成獨立攻擊面；FADEL evidential 是**獨立 epistemic checkpoint**，比照 MC-dropout/ensemble 的理由（隨機性/獨立 checkpoint 使 targeted 攻擊需 EOT-like 多前向）排除於對抗排序欄。
- **修正（砍）**：RQ3 攻擊面**釘死為 3 個**——MSP、energy、Mahalanobis-on-SSL，全部衍生自 RQ1/RQ2 的**同一 frozen backbone 單次前向**。P 對帳表「5 機制」更正為「3 機制」（順帶降本，見 D）。

### A3【收斂·我自己的成本曲線過寬】「2–3 個 ε 點」
- **點名**：我 R1 D-RQ3.3「2–3 個 ε 點」。
- **問題**：ε 點數是對抗欄的乘數；3 點無科學必要。
- **修正（收斂）**：**固定 2 個 ε 點**——1 個 SNR 錨定的預註冊 primary ε（報 confident-real 到達率主值）+ 1 個較粗/較細點（僅示成本曲線斜率）。

### A4【收斂·樣本數取下限】n≈2,000–5,000
- **修正（收斂）**：RQ3 攻擊子集取**下限 n≈2,000**（generator-disjoint holdout 分層抽），足以估 per-family 到達率與排序翻轉；不必到 5,000。

### A5【非我 lane，但點名】E 的「ASVspoof19 LA eval 中間參照點」非嚴格零成本
- **點名**：E-eval §Q-SPLIT「可零成本加一個中間參照點：同一次前向也在 ASVspoof19 LA eval 上讀一次」。
- **問題**：ASVspoof19 LA eval（71k）是**另一個資料集的新前向**，不在 DFADD 快取內，不是 S1 的零成本重用。
- **修正（收斂，交還 E）**：保留此參照點（對歸因有用、屬 in-scope 種子語料），但**須 subsample ≤20k**（~0.1–0.2h），並在對帳表**明列為一格評估**，不得以「零成本」帶過；若日曆吃緊即砍。

### A6【收斂建議·非我 lane】P 的 optional「+36h multi-seed 訓練」
- **點名**：P 對帳表「訓練·多 seed +36h」。
- **修正（收斂建議）**：往更省收——**預設 deterministic + per-generator bootstrap CI**（統計可信度已由 bootstrap 提供），把 multi-seed 列 future/只在 pilot 顯示 seed 變異大才啟用，**帳面砍掉 +36h**。

**前作宣稱檢查**：各角色皆已正確把 novelty 標「待 Codex 查證」（A1/A2/A3 residual gap 均未寫死），無違反第 4 條。我 D-RQ3.1 的「dev-fixed τ + unseen-generator transfer 下量 confident-real 到達率與排序翻轉，相對 CLAD/reject-option 前作的增量」維持「待 Codex 查證」，不自行下結論。

---

## B. 回答指名我的提醒

- **M → T**（復用 dev-fixed τ、量「進 confident-real 比例/對抗欄 risk-violation」、勿另立獨立 AUROC、明定 query/quality budget）：**接受主體**——RQ3 直接吃 RQ1 的 dev-fixed τ，主報對抗欄 Δr、不另立 AUROC。**但拒絕「recipe-level 搜尋」措辭**（見 A1，PGD 為 per-sample）；query/quality budget 已由 D-RQ3.2/3.3 預註冊固定。
- **E → T**（同一 holdout split、同一 Δr risk-violation metric、勿另立評估協定、budget 預先固定）：**全接受**。RQ3 = 「同一 protocol 的對抗欄」，不另立協定；ε 預算預註冊、禁以 test 結果回調（否則等同 holdout tuning，違反停止條件）。
- **P → T**（鎖 PGD-50 白盒 ~13h、禁黑盒 ≥10k-query 紅線 R8）：**已鎖，接受**（D-RQ3.2 已砍 black-box，省 500–1,000h → 直接 future work）。

---

## C. 跨角色分歧的收斂建議（往更小/更省收）

1. **RQ3 攻擊面數（M=5 / T=3 / P=5）→ 收斂 3**：MSP、energy、Mahalanobis-on-SSL，共用 frozen 單次前向；temperature 單調等價不另攻、FADEL 排除於對抗欄。三方對帳表統一寫 3。
2. **RQ3 報告量（T 原「到達率+排序翻轉」vs M/E 要「Δr」）→ 收斂為單一 metric family**：**主報對抗欄 Δr**（= 攻擊後 r_obs − r*，用 RQ1 同一 τ、同一 holdout、同一 bootstrap CI），**輔報** confident-real 到達率與「對抗排序是否相對 RQ2 clean 排序翻轉」。不並列第二套 AUROC，維持 falsifiability 不稀釋。
3. **ε 預算 → 收斂 2 點**、SNR 錨定、預註冊、禁 test 回調（併入 E 的 leakage 防線）。
4. **樣本數 → 收斂 n≈2,000**（分層 generator-disjoint holdout）。

---

## D. 總 GPU-hour 對帳

- **RQ3 收斂後**：3 機制 × 2 ε × per-sample PGD-50 × ~2,000 樣本 × 3 detector，重用 frozen checkpoint（S4）+ cached forward（S1）→ **≈ 8–16 GPU-h**（較 P 原列 13h 同級或略降；較我 R1 的 15–30h 收斂變小）。落在預留 200h 對抗欄內、餘裕極大。
- **全方向核心（收斂後合帳）**：訓練（3 base + 3 FADEL，優先 frozen-backend）≈ 36h ＋ 前處理（neural codec 子集 + SSL pooled 特徵）≈ 20–30h ＋ 主評估 ≈ 11h ＋ confound UTMOS/ECAPA ≈ 3–6h ＋ RQ3 ≈ 8–16h ＝ **≈ 80–100 GPU-h**（＋pilot 3–8h）。
- **判定**：**遠低於 430–520h 封套，無超支**。差額全數為 debug/重跑緩衝，**非加實驗許可**。無需為預算砍任何科學內容；唯一算力相關收斂是攻擊面 5→3、ε 點 3→2、建議砍 optional +36h multi-seed。

**我認為的總 GPU-hour：核心 ≈ 80–100h（RQ3 佔 8–16h）＋ pilot 3–8h，穩守 430–520 封套。**
