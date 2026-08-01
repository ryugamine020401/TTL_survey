# R1 設計立場：指導教授（範圍/貢獻把關）
日期：2026-07-15

範圍鎖定：本文只把我主責的三件事定成單一決策，並對其他角色的 Q 給一句風險提醒。任何想「順便多做」的一律當場砍。GPU-hour 全部用 `01-compute-budget.md` 第 5 節公式對帳，硬守 **430–520 GPU-h 總封套**。凡涉前作/novelty 一律標「待 Codex 查證」，不寫死。

---

## 主責 Q-CONTRIB：貢獻結構 + 可證偽的 primary claim

**單一決策（不是選項清單）**
貢獻結構鎖定為 **兩核心 + 一選配 + 一負結果**，且**不新增第五項**：
- **C1（核心·protocol）**：development-fixed、generator-disjoint、temporal-holdout 的可重現 selective-evaluation protocol（含 split manifest、version/hash、無 holdout tuning）。
- **C2（核心·failure map）**：在受控新生成器（DFADD）與多語廣度（MLAAD v9）holdout 上，量化 risk-constraint violation / coverage collapse / high-confidence error，按 generator family / 語言 / 來源做 failure map。
- **C3（選配·method）**：**僅限 post-hoc、development-only 的 score normalization / conformal risk control**；成功標準是「在 ≥2 個未動過的 holdout 上降低 risk violation 且不過度犧牲 coverage」，**不是 EER SOTA、不換 backbone**。若 pilot 後時間不夠，C3 直接砍成 future work，論文不受影響。
- **C4（負結果·成立）**：若所有分數的固定閾值都不可轉移，即為「低信心=部署安全閥」在新生成器下**不成立**的可用負結果。

**可證偽的 primary claim（一句話）**
> 在開發集固定的 risk/coverage 操作點、完全不以外部資料調參，轉移到 generator-disjoint、時間較新的 holdout 時，實際 selective risk 會**系統性超過預宣稱上限（violation > 0，統計顯著、且不由語言/取樣率/duration confound 解釋）**。

- **可證偽性**：若 holdout 觀測 risk ≤ target（bootstrap CI 內），claim 為假——論文轉為 C4 反向的「閾值可轉移」正面結論，**兩個方向都成篇**。
- **負結果長什麼樣、在什麼條件成立**：C4 只在「base detector 非隨機（過 AUROC gate）＋ confound 已控制」下才算數；若 detector 全體接近隨機，那不是負結果，是 pilot 失敗（見 Q-PILOT 轉向條件），不得寫成 finding。

**被我砍掉的選項與原因**
- 砍「把棄權**首次**引入 ADD」當貢獻——Codex A1 已 Refuted（Salvi 2023 / Pascu 2024 / FADEL 2025 為 closest work，必列）。
- 砍「新 backbone / 新偵測器架構」當 method 貢獻——超出查證後定稿，且吃訓練 GPU-hour（法則 4：換 backbone 即重訓）。
- 砍把 C3 升為核心——method 若失敗會拖垮整篇；降為選配，論文由 C1+C2 撐住。

**GPU-hour 影響**：**0**。C1/C2/C4 是量測與分析；C3 鎖定 post-hoc（吃同一次前向的快取 logits+embedding，S1），邊際 GPU 成本為零。**紅線**：任何要求「訓練一個校準頭 / 重訓 backbone」的 C3 變體當場砍。

**是否待 Codex 查證**：**是**。「無等同的 fixed-threshold 跨世代 risk-transfer protocol」在 Codex 為 **Unknown（promising，非 verified novelty）**——primary claim 的 novelty 措辭標「待 Codex 查證」，並把「closest-work 檢查」寫進 pilot 當轉向 gate（見下）。

---

## 主責：算力對帳（守 430–520 GPU-h 封套）

**單一決策**
方向#1 全論文帳本鎖定下列配置，總和落在封套內：
**2–3 detectors ／ post-hoc 分數共用單次前向（S1）／ 分層抽樣 20k 池（S2）／ frozen backbone + 快取 pooled 特徵（S3+S6）／ 共用 checkpoint（S4）／ neural codec 只在子集（S10）／ 對抗 recipe-level（S8）**。

**對帳表（以 `01-compute-budget.md` 算例2 為錨，套用我的砍法）**

| 科目 | 配置 | GPU-h |
|---|---|---|
| 訓練 | 3 base + 3 evidential(FADEL)，full FT 6h（或 frozen 更省）；統計可信度用 deterministic + bootstrap，不加 seed 訓練 | 36 |
| 訓練·多 seed（僅 SSL detector，若採 3 seed 而非 deterministic） | +2 seed × 3 detector × 6h | +36 |
| 前處理 | neural codec transcode **僅** 抽樣 100k × 2 條件 + SSL pooled 特徵抽取 | 20–30 |
| 評估 | 3 model × 6 格 × 1.0（10萬池）× 0.6，post-hoc 5 機制共用單次前向 | 11 |
| 對抗（RQ3） | PGD-50 白盒，5,000 樣本 × 3 model × 5 機制，recipe-level | 13 |
| **核心小計** | | **≈ 120–130** |
| 除錯/重跑 + 15% 緩衝（封套內未動用的餘裕） | | 保留至 430–520 |

**結論：核心設計約 120–130 GPU-h，遠在 430–520 封套內；差額是除錯/重跑/多 seed 緩衝，不是加實驗的許可。**

**被我砍掉的選項與原因（法則 1–3）**
- 砍 **deep ensemble**（×5 訓練 +54h、×5 推論）——換不到與 primary claim 相稱的科學；C4 負結果不需要 ensemble。
- 砍 **MC-dropout 高 T**（×10–30 前向，全集上單項 1,000–2,600h，紅線 R4）——K=7 中它是少數真的要錢的；若 M 堅持保留，T≤10 且只在抽樣子集。
- 砍任何 **ASVspoof21 DF 全集 × 乘數**（法則 3，貴 30×）——一律分層抽 20k。
- 砍 **通道擴增訓練 × ensemble 併用**（算例3：690h，佔半個預算）——二選一，且本方向主軸是 generator shift 不是 channel，通道只作單一協變量。

**是否待 Codex 查證**：否（純算力事實）。

---

## 主責 Q-PILOT：pilot 收斂（把 Codex 第 9/10 節具體化為可執行規格）

**單一決策（每項一個值，不留選項）**
- **detector（1 個）**：XLS-R 300M **frozen** + AASIST/線性 backend，訓於 ASVspoof19 LA。理由：最便宜的可重現 SSL detector（S6），且 Scalable AASIST 顯示資料受限時 frozen 反而更好。**砍**：pilot 不用兩個 detector（那是全論文）、不用 XLS-R 1B（R2 死線、殺雞用牛刀）。
- **分數（2 種）**：MSP/entropy（discriminative）+ 一個 embedding/density score（同一 frozen 表徵上算，控制 A2 confound）。
- **dev 集**：ASVspoof19 LA **dev**，選定閾值後**完全凍結**。
- **兩個 risk target**：**5% 與 10%**（selective risk / fixed-FPR）。
- **holdout**：DFADD **2025-04 修正版**的 **10–20% 分層子集**，按 5 個 TTS（3 diffusion + 2 FM）generator family 分層；記錄 commit/日期；**split manifest 須逐一控制訓練語料/vocoder 重疊（E1：名字新 ≠ 嚴格 unseen）**。
- **success（全部要滿足）**：(a) 外部 base **AUROC ≥ 0.75**（「不接近隨機」gate）；(b) dev 固定閾值 → 外部 observed risk/coverage/violation，且至少一個 generator family 的 per-generator bootstrap CI **不跨 0**、可重複；(c) generator-family 層級**無洩漏**（manifest 證明）；(d) duration/取樣率配對後落差仍在（非 confound 解釋）。
- **stop/轉向（任一觸發即轉）**：所有外部 detector **AUROC < 0.6**（abstention 退化成「全拒絕」）；或找到相同 fixed-threshold + newer-holdout + risk-violation 前作且無 measurement delta；或 generator metadata 不足以支持 unseen 宣稱；或需用 holdout 調閾值才有正面結果。

**GPU-hour 影響**：**pilot ≈ 3–8 GPU-h**（1 frozen detector：~1h 訓練 + 特徵快取；MSP/entropy/embedding 全 post-hoc 單次前向；DFADD 10–20% 子集 ~20–40k 筆評估 ~0.3–0.5h；dev 評估 ~0.3h）。相對 430–520 封套可忽略，通過才進全論文。

**被我砍掉的選項與原因**
- 砍「pilot 就上多 detector / 多 shift 網格」——pilot 的唯一任務是判 go/no-go，不是縮小版全論文。
- 砍「pilot 就跑 DFADD 全集」——法則 3，10–20% 子集足以判結構。

**是否待 Codex 查證**：**是**。轉向條件裡的「找到相同 fixed-threshold transfer 前作且無 delta」＝ 把 A1 的 Unknown 當 pilot 內建 gate；closest-work 複查（Salvi/Pascu/FADEL 之外）標「待 Codex 查證」。

---

## 對非主責 Q 的風險提醒（各一句，給指名角色）

- **Q-SCORES → M**：deep ensemble = ×5 訓練 + ×5 推論、MC-dropout = ×10–30 前向，是 K=7 裡唯三真的燒錢的——**deep ensemble 直接砍，MC-dropout 只在 T≤10 + 抽樣子集才留**，否則 primary claim 換不回這筆算力。
- **Q-METRIC → M/E**：primary metric 只能有**一個**——選 **fixed-risk-target 的 risk-constraint violation**（正是可證偽 claim 所測），AURC/ECE 降為次要診斷，別三個並列稀釋 falsifiability。
- **Q-SPLIT → E**：這是 pilot 最高風險單點——manifest 必須同時證明 generator-family disjoint **且** 控制 DFADD 與 19LA 種子的訓練語料/vocoder 重疊（共用 VCTK/LJSpeech upstream 即洩漏），洩漏一次整個 primary claim 作廢。
- **Q-RQ2 → M**：density vs discriminative 必須在**同一個 frozen 共用表徵**上算兩種分數（A2）——一旦每類分數配不同 backbone，結論只是模型容量差，還多燒訓練 GPU-hour。
- **Q-RQ3 → T**：confident-real 非全新（reject-option adversarial 已有，CLAD 等，A3）——必給明確 threat model + query/quality budget + 相對一般 targeted attack 的增量價值，且**鎖 PGD-50 白盒（~13h），禁黑盒 ≥10k-query（R8，500–1,000h 紅線）**。

---

## 回傳：一行版決策 + GPU-hour 小計

- **Q-CONTRIB**：貢獻鎖 C1 protocol + C2 failure map（核心）／ C3 僅 post-hoc method（選配，可砍）／ C4 負結果；primary claim =「dev 固定閾值轉到 unseen-generator holdout，selective risk 系統性 violation > 0（顯著、非 confound）」，可雙向證偽；novelty 待 Codex 查證。**GPU：0**。
- **算力對帳**：鎖 2–3 detector + S1/S2/S3/S4/S6/S8/S10 全套省法，砍 deep ensemble 與 MC-dropout 高 T；核心 **≈ 120–130 GPU-h**，穩守 430–520 封套，差額是緩衝不是加實驗許可。
- **Q-PILOT**：1 frozen XLS-R300M+AASIST detector／2 分數／dev=19LA dev／risk target 5% & 10%／DFADD 2025-04 之 10–20% family-分層子集；success = AUROC≥0.75 gate + violation 可重複 + 無洩漏 + 非 confound；stop = 全體 AUROC<0.6 或撞相同前作。**GPU：≈ 3–8h**。

**GPU-hour 小計（主責範圍）：pilot ≈ 3–8h；全論文核心 ≈ 120–130h；總封套守 430–520h（餘裕全數保留為除錯/重跑緩衝，不動用於新實驗）。**
