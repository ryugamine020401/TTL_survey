# R2 收斂：評估嚴謹度方法學家
日期：2026-07-15

範圍：R2 只做收斂，不加任何東西。以下每一項不是「新提案」，是把 R1 四檔往**更小、更可執行、更省算力**收；並逐一點名會偷加東西 / 算力對不上帳 / 把前作寫死的決策。所有專有名詞保留英文。

---

## 一、點名會破壞紀律的決策（只砍與收斂）

### 1【算力對不上帳 + 偷加一條 shift 軸】P 對帳表的「neural codec transcode 100k × 2 條件 = 20–30h」
- **問題**：方向#1 的命題是 **generator transfer**，channel 在本方向只是**單一協變量**（P 自己也寫「通道只作單一協變量」）。但對帳表卻編列 neural codec transcode（EnCodec/DAC 級生成模型，預算表 §4.2 全表最大隱藏成本）×2 條件，等於偷偷把一條 channel/codec shift 軸放進核心。neural codec transcode 是方向#2（laundering 對象＝CoSG）與方向#4（RTC）的 threat model，混入方向#1 即 threat-model bleed。
- **修正（砍）**：方向#1 的 channel 協變量**改用 traditional CPU codec 階梯（Opus / AMR-WB）**——預算表 §4.1 明列傳統 codec 是 CPU、不吃 GPU 預算，且對電信情境更具代表性。**砍掉全部 neural codec transcode**。省 **20–30 GPU-h**，同時消除 threat-model 混淆。RQ1 的「unseen-channel」語意由傳統 codec 承接，一格 GPU 都不用。

### 2【偷加·pilot 塞入非 pilot 必需的 GPU 成本】E（我自己 R1）的「pilot 配 UTMOS+ECAPA 品質協變量 1–2h」
- **問題**：Codex §10 的 pilot 成功條件只要求「結果不由**語言 / 取樣率 / duration / 來源 pipeline** 解釋」——**全部是免費 metadata**，沒有 quality/UTMOS。品質協變量是 §9.4（全論文統計可信度）的要求，不是 pilot gate。我 R1 把它放進 pilot 是自我加碼。
- **修正（砍）**：**pilot 的 confound panel 只用 metadata**（generator-family / duration-bin / sampling-rate / source-corpus·speaker-overlap），品質協變量（UTMOS + ECAPA）**下放到全論文**。pilot 品質協變量 GPU **歸零**（省 1–2h），且 pilot 更乾淨（純 metadata gate，零模型依賴）。

### 3【收斂·省 36h】P 對帳表的「訓練·多 seed +36h」
- **問題**：Codex §9.4 明寫「**多 seeds 或 deterministic baseline**」——是二選一，不是都要。整個設計的統計可信度本來就靠 **per-generator-family bootstrap CI（1000×，CPU）**，多 seed 訓練與 bootstrap 功能重疊。
- **修正（收斂）**：預設 **deterministic checkpoint + bootstrap CI**，**砍多 seed 訓練**。省 **36 GPU-h**。若審查要求 seed 穩定度，留作緩衝內的選配，不進核心帳。

### 4【前作寫死檢查——通過】
- 四檔的 novelty 措辭全部正確標「待 Codex 查證」：A1 protocol（M/P）、A2 density-vs-discriminative（M）、A3 confident-real 增量（T）、DFADD 嚴格 unseen（E）。**無把前作宣稱寫死的違規**。唯一要釘死的操作：這些「待查證」措辭必須寫進 pilot 的**轉向 gate**（撞到相同 fixed-threshold + newer-holdout + risk-violation 前作且無 delta 即轉向），P 已寫，確認保留。

---

## 二、回答指名我（E）的提醒

- **M→E（Mahalanobis 對 bona-fide 來源重疊敏感）**：**接受並強化**。Mahalanobis-on-SSL 是 density 分數，其「unseen 訊號」會被 bona-fide upstream 重疊污染。split manifest 的 disjoint 判定除了 vocoder 層，**必須額外逐 utterance 控制 bona-fide 來源語料（VCTK / LJSpeech）與 ASVspoof19 種子的重疊**，不只判 TTS 系統名。這正是 Codex E1「名字新 ≠ 嚴格 unseen」在 density 分數上的具體攻擊面；leakage gate 增列一列 `bona-fide-source-overlap`。**GPU：0（metadata）**。
- **M→E（Δ 的 CI 要分辨 5–40pp 的 shift 效應）**：確認。**stratified 20k、seed fixed、寫進 paper、附 bootstrap CI**（預算表 S2，SE≈±0.4%，足以分辨 >1pp）。**絕不退回 DF 611k 全集**（會被每個乘數乘一次）。
- **T→E（τ 的定義與凍結時點釘死）**：確認並釘死。**τ 在 ASVspoof19 LA dev 上、使 selective risk = r\*（r\*∈{5%,10%}）時決定，決定後完全凍結**；RQ3 的 confident-real 接受區直接復用**同一個** τ，不另設門檻。凍結時點＝dev 操作點固定的那一刻，此後任何 holdout / 對抗欄都不得回改。
- **T→E（ε 不得以 test 結果回調）**：**接受，補進 leakage 防線**。ε 是一個**新的 holdout-tuning 面**——把 test 上的攻擊成功率回頭調 ε 讓攻擊「好看」等同 holdout tuning。故 **ε 以 SNR 錨定值預註冊，凍結同 τ 一起處理**，寫進「no-holdout-tuning」清單（原本只列 τ，現擴為 {τ, ε, 分層 seed}）。
- **P→E（manifest 同時證 generator-family disjoint 且控 upstream/vocoder 重疊，洩漏一次 primary claim 作廢）**：確認，這是我 Q-SPLIT 的核心，最高風險單點。manifest 逐 utterance 記 `{dataset, generator-family, vocoder/波形生成模組, source-corpus, speaker-ID, sampling-rate, duration, bona-fide-source-overlap}`，disjoint 判在 vocoder 層，並附「DFADD 5 vocoder（HiFi-GAN/iSTFT/latent-codec decoder，皆 2019 後）對 A01–A19 逐項比對表」。此表**待 Codex 逐項核**才可寫「嚴格 unseen」，在此之前只記錄不斷言。

---

## 三、跨角色分歧的收斂建議（一律往更小收）

- **Q-METRIC（M/E/P 已一致，定稿）**：primary = **development-fixed 操作點的 risk-constraint violation Δr（配對 Δc）+ per-family bootstrap CI**；AURC/ECE/fixed-FPR≤1% selective-recall **全部降次要診斷**。三檔無實質分歧，直接鎖死單一 primary，不並列稀釋 falsifiability。**GPU：0**。
- **base-AUROC gate 的兩個門檻（收斂為分工，不衝突）**：E 的 **0.6** 是 **detector-floor**（低於此 Δr 無意義、該 cell 作廢、不計入 transfer 結論）；P 的 **0.75** 是 **pilot go/no-go 成功 bar**。兩者用途不同、可並存：**全論文報告用 0.6 floor 標 cell；pilot 用「至少一 detector ≥0.75」判 go**；stop 條件用「全體 <0.6」。
- **RQ3 的 ε 點數（P=1 vs T=2–3）→ 收斂 2**：成本曲線最少 2 點即成立，不必 3。PGD-50 白盒 × ~5k 樣本 × 3 model × 可微 post-hoc 子集（MSP/energy/Mahalanobis）× **2 ε 點 ≈ 20 GPU-h**，落在對抗預留內、餘裕大。砍第 3 個 ε 點。
- **pilot 的 holdout（一致，確認）**：DFADD 2025-04 的 **10–20% family-分層子集，單一 holdout**；E 已砍「pilot 納第二 holdout（CodecFake+）」，M/P 一致。CodecFake+ 第二軸相位化到全論文，不擴 pilot scope。
- **FADEL evidential（確認為必列 baseline 而非加碼）**：Codex B5 Verified closest work，必列；用 **frozen backbone + evidential backend（0.3–1h/次）**，且**不進 pilot**（pilot 只 1 detector + MSP + Mahalanobis）。全論文 +10–30h，屬既定範圍。
- **Q-SPLIT 的 ASVspoof19 LA eval 中間參照點（保留但封頂）**：分層抽 20k、重用同一次快取前向（~0.5h），僅作「unseen-attack vs 生成世代/vocoder 新穎性」的歸因診斷，**不升為新 RQ**。直接服務 primary claim 的失效歸因，近零成本，保留。

---

## 四、總 GPU-hour 結算

以 P 對帳表為錨，套用上面的砍法：

| 科目 | R1（P 表） | R2 收斂後 | 動作 |
|---|---|---|---|
| 訓練（3 base + 3 FADEL, frozen backend 優先） | 36 | 36 | 保留 |
| 訓練·多 seed | +36 | **0** | 砍（deterministic + bootstrap） |
| 前處理（neural codec transcode 2 條件 + SSL 特徵） | 20–30 | **5–10** | 砍 neural transcode，改 CPU 傳統 codec；只留 SSL pooled 特徵抽取 |
| 評估（generator-shift × 20k × post-hoc 共享單次前向） | 11 | 8–11 | 保留（channel 改 CPU 協變量，不增 GPU 格） |
| 對抗 RQ3（PGD-50 白盒，2 ε 點） | 13 | 15–20 | 收斂 2 ε 點 |
| confound 品質協變量（UTMOS+ECAPA，全論文） | — | 3–6 | 全論文保留，pilot 砍 |
| pilot（1 frozen detector + metadata confound） | 3–8 | 3–6 | 砍 pilot 的 UTMOS+ECAPA |
| **核心合計** | ~120–130 | **≈ 70–90** | |

**結論：總 GPU-hour 沒有超，遠遠沒超。** 收斂後核心 **≈ 70–90 GPU-h**（即使保留 P 的保守 full-FT 訓練估計，上限也 ~120h）；相對 **430–520h 封套用不到 1/4**。無任何項目因預算被迫砍——上述砍法全是「同科學內容、更省」的收斂，不是預算逼出來的取捨。**430–520 與核心之間的 ~300h 是除錯/重跑/選配 seed 緩衝，不是加實驗的許可**（沿用 P 的紅線）。

唯一要提醒的反向風險：核心只用 ~20% 封套，若日後有人拿「還有 300h 餘裕」當理由加軸（多 detector、多 holdout、neural codec 軸、MC-dropout），一律套預算表第 5 節公式當場算並擋回——餘裕是緩衝，不是空位。
