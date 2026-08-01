# R1 設計立場：評估嚴謹度方法學家
日期：2026-07-15

範圍：本檔只對主責的 **Q-SPLIT、Q-METRIC、leakage/confound** 給單一決策，並對非主責 Q 給一句風險提醒。遵守 00-agenda 紀律：單一決策非選項清單／只砍不加／算力對帳守 430–520h／前作宣稱標「待 Codex 查證」。

核心立場（貫穿三題）：**我主責的三個決策全部是「對同一次前向的快取分數做分析與報告」，本身幾乎不吃 GPU（S1/S4）。評估嚴謹度不是靠多花算力買來的，是靠 split manifest、metric 定義、confound 分層三件事把「benchmark report」升級成「論文」。**

---

## Q-SPLIT（主責）

### 單一決策
一套**四角色、以 vocoder/波形生成層為單位判 disjoint 的 split manifest**：

- **train**＝ASVspoof19 LA train（偵測器訓練種子，frozen backbone 為預設 S6；不換 seed corpus）。
- **dev**＝ASVspoof19 LA dev（**唯一**的閾值選定集；在此固定 risk/coverage 操作點後**完全凍結**，holdout 結果不得回頭改 τ）。
- **primary holdout（test）**＝DFADD 2025-04 corrected release，作 generator-disjoint × temporal holdout；pilot 取其 10–20% 子集，**跨 5 個 TTS family 分層抽樣**使 per-family bootstrap CI 可估。
- **untouched external**＝In-the-Wild（Apache-2.0，只做最終 smoke-test，永不碰閾值/方法選擇）；MLAAD v9 為選配多語廣度，同屬 evaluation-only。

leakage 控制的具體規格（回應 Codex E1「名字新 ≠ 嚴格 unseen」）：逐 utterance 建 manifest 記錄 `{dataset, generator-family, 波形生成模組/vocoder, source-corpus, speaker-ID, sampling-rate, duration}`，並在**vocoder/波形生成層**（非 TTS 名稱層）判 disjoint；全部 resample 至 16 kHz。無 leakage 的證明分兩層：(a) manifest 逐項列 ASVspoof19 A01–A19 的 vocoder 對 DFADD 的 HiFi-GAN/iSTFT/latent-codec decoder，確認後者屬 2019 後、確實不在種子攻擊集；(b) **分層報告**——risk-violation 必須在 speaker-overlap／duration／sampling-rate 各 stratum 內仍成立（confound gate）。可零成本加一個中間參照點：同一次前向也在 ASVspoof19 LA eval（unseen attack、同 corpus/世代）上讀一次，若閾值在此守住卻在 DFADD 崩，即把失效歸因於**生成世代/vocoder 新穎性**而非單純 unseen attack。

### 被砍的選項
- **砍「train↔holdout speaker-disjoint 當硬 gate」**：ASVspoof19 LA 與 DFADD bona-fide 都源自 VCTK，強制剔除重疊 speaker 會縮資料，且 bona-fide 側 speaker 重疊對「generator transfer」claim 反而**保守**（偵測器已看過這些真實語者，失效只能歸因於新生成器）——改用分層報告控制，不用排除控制。
- **砍「pilot 就放入第二 holdout（CodecFake+ CoSG）」**：那是方向#2 的資產與 Codex 7.1 對**全論文**的建議；pilot 維持 DFADD 單一 holdout 以守預算，全論文再加第二軸（相位化，不擴 scope）。

### 一句理由
Codex E1 明列 DFADD 與種子語料/vocoder 可能重疊、「名字新 ≠ 嚴格 unseen」，故 disjoint 必須判在 vocoder 層並用 manifest 逐一控制；HiFi-GAN/iSTFTNet/codec decoder 皆 2019 後，這條 gap 可滿足但**須記錄不得斷言**。

### GPU-hour 影響
**≈ 0 GPU-h**。manifest 建置、speaker/vocoder 稽核、16 kHz resample 皆 CPU/metadata；ASVspoof19 eval 中間參照重用同一批快取分數（S1）。

### 是否待 Codex 查證
**是（限一點）**：「DFADD 5 家 vocoder 對 ASVspoof19 LA 攻擊集嚴格 disjoint／確為 unseen」屬 novelty-adjacent，須待 Codex 逐項核 manifest 後才可寫；在此之前不寫「嚴格 unseen/首次」。split 的角色設計本身（train/dev/test）非前作宣稱，不待查證。

---

## Q-METRIC（主責）

### 單一決策
**primary metric ＝ development-fixed 操作點下的 risk-constraint violation Δr**：在 dev 上固定 τ 使 selective risk＝宣稱目標 r\*（Codex pilot 的 r\*∈{5%,10%}），誘導出 dev coverage c_dev；把**同一 τ** 套到 holdout，量 r_obs 與 c_obs，主指標為 **Δr = r_obs − r\*（配對報 Δc = c_obs − c_dev）**，並附 per-generator-family stratified bootstrap（1000×）95% CI。violation 判定＝Δr 的 CI 下界 > 0。

**次要指標（同一次前向、零邊際成本）**：AURC（threshold-free 的 ranking 品質）+ ECE（calibration）。這兩者把失效**分解**成 ranking-collapse vs calibration-shift，正是 Codex C1 的 measurement contribution。**base AUROC/EER gate 先報**：holdout 上 base 近隨機（AUROC<~0.6）的 cell 標「detector-floor」，其 Δr 無意義、不計入 transfer 結論（Codex 停止條件）。

### 被砍的選項
- **砍「fixed-FPR≤1% selective recall 當 primary」**：(a) 它表達的是某操作點的 recall，不是本論文命題的「風險違約」；(b) FPR≤1% 在分層後 ~20k holdout 上因負樣本過少使 τ 極不穩、CI 過寬。降為次要報告值。
- **砍「AURC 當 primary」**：AURC 是 threshold-free 的 ranking 摘要，回答「排序是否還好」（近 RQ2）而非「固定閾值是否守住」（RQ1＝命題）；AURC 可漂亮而 fixed-threshold 已崩。保留為分解失效用的次要診斷。

### 一句理由
本論文命題是「development-fixed 固定閾值跨世代是否仍守 accepted-risk 上限」，唯一直接量它的是 Δr；AURC/fixed-FPR-recall 各自只回答 ranking 或單點 recall，錯位為 primary 會使結論答非所問（Codex A1 修正後可研究問題原文）。

### GPU-hour 影響
**≈ 0 GPU-h**。全部 metric 由快取的 logits+pooled embedding 於 numpy/CPU 算出（S1）；bootstrap 為 CPU。primary metric 的選擇是**報告/分析決策，增訓練/評估次數為零**。

### 是否待 Codex 查證
**否**（就 metric 本身）：selective risk / AURC / ECE 均為選擇性預測標準定義（Geifman–El-Yaniv 等），非 novelty。**但**「fixed-threshold 跨世代 risk-violation protocol」相對 Salvi 2023／Pascu 2024／FADEL 是否為 residual gap，屬 A1 已標之 novelty 宣稱，**待 Codex 查證**；novelty 在 protocol framing，不在 metric。

---

## leakage / confound（主責）

### 單一決策
一組**固定的 confound-control panel，套用到每一個 holdout 結果、全部由快取前向零邊際成本算出**：把 risk-violation 在 `{generator-family, duration-bin, sampling-rate, source-corpus/speaker-overlap}` 各 stratum 內分層報告，並配一個品質協變量（UTMOS + ECAPA speaker-similarity，沿用方向#3 recipe 但此處只作 control、不長成新軸）。**判準：holdout 的 Δr 只有在 within-stratum 仍成立（即非由 duration/取樣率/corpus 捷徑解釋）才算真正的 transfer failure**——這正是 pilot 成功條件「結果非由語言/取樣率/duration 解釋」的可操作化。

### 被砍的選項
- **砍「pilot 納入 channel/codec confound 軸」**：方向#1 pilot 用 DFADD（乾淨 16 kHz），channel 屬全論文 shift grid；pilot 加 codec transcode 每條件 4–8 GPU-h（預算表 4.2）且對 pilot 命題無用。砍出 pilot，保留為全論文軸。
- **砍「用 MC-dropout/deep-ensemble 做 leakage 分析」**：建立 leakage/confound 不需要它們，單一 frozen checkpoint 的 post-hoc 分數即足（S1、法則1）；是否納 ensemble 屬 Q-SCORES，見對 M 的提醒。

### 一句理由
Codex 第 9 節第 4 點與 pilot 成功條件均要求「診斷 channel/duration/quality confound、結果不得由取樣率/duration/來源 pipeline 解釋」，故 confound 分層是通過條件而非額外實驗。

### GPU-hour 影響
**pilot ≈ 1–2 GPU-h、全論文 ≈ 3–6 GPU-h**：唯一花費是 UTMOS+ECAPA 品質協變量抽取（預算算例5：10 萬筆 3–6 GPU-h，~20k pilot 子集約 1–2 GPU-h）；分層本身 = 0（CPU）。

### 是否待 Codex 查證
**否**：confound control 屬方法學，非前作/novelty 宣稱。

---

## 對非主責 Q 的風險提醒（指名）

- **給 M（Q-SCORES）**：deep ensemble/MC-dropout **不得進 pilot 的 split**——pilot 只需單一 frozen checkpoint + post-hoc 分數（MSP/entropy/energy/Mahalanobis）即可建立 threshold-transfer 與 base-AUROC gate（法則1）；ensemble 一旦進 pilot 會把 gate 成本 ×E 且無助於命題。
- **給 M（Q-RQ2）**：density vs discriminative 比較**必須固定同一 frozen backbone 與同一組 pooled 特徵並報 representation-quality 控制**（Codex A2），否則結論退化成模型容量差、不可解釋。
- **給 T（Q-RQ3）**：confident-real 對抗軸的結果**必須跑在同一 holdout split、用同一 Δr risk-violation metric 報告**，勿為 RQ3 另立評估協定，否則「對抗欄下排序翻轉」不可比；query/quality budget 須預先固定（A3）。
- **給 P（Q-PILOT）**：pilot 的 success/stop 數值門檻**必須含 (i) base-AUROC gate（如 holdout AUROC≥0.6）先於任何 Δr 解讀、(ii) leakage gate（Δr 須 within-stratum 存活）**，否則「風險違約」會與 detector-floor 或 corpus 捷徑混淆。
- **給 P（Q-CONTRIB）**：可證偽的 primary claim 建議直接以 **Δr 及其 CI** 陳述（例：「dev 固定 τ 在 ≥k 個 generator-family 上 Δr 的 CI 下界 > 0」），使負結果（全部可轉移／全部不可轉移）可量測。

---

## GPU-hour 小計（本檔三個主責決策）
- Q-SPLIT：≈ 0 GPU-h（metadata + 重用快取）
- Q-METRIC：≈ 0 GPU-h（post-hoc from cached forward）
- leakage/confound：pilot ≈ 1–2 GPU-h / 全論文 ≈ 3–6 GPU-h（唯一花費：UTMOS+ECAPA）
- **合計：pilot ≈ 1–2 GPU-h；全論文 ≈ 3–6 GPU-h**（全部為分析/報告在已編列之單次前向上的重用，對 430–520h 總預算近乎中性）
