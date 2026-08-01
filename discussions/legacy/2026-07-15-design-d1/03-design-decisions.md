# 方向#1 設計決策定案 + pilot 規格
日期：2026-07-15
主持/統整：本檔為 4 角色（M 選擇性預測、E 評估嚴謹度、T 威脅模型、P 指導教授）round1+round2 的收斂定案。
基礎：`five-directions-verified.md`（查證後定稿）／`2026-07-15-claims-to-verify-a-d.md` §9–§10（pilot 與停止條件）／`01-compute-budget.md`（算力硬預算）。
紀律：單一決策非選項清單／只砍不加／任何增訓練即算 GPU-hour（總和守 430–520h）／前作宣稱標「待 Codex 查證」不寫死／社會意義只進 intro-discussion。

---

## 一、設計決策（每個 Q 一個單一決策）

### Q-SPLIT — generator-family disjoint 的四角色 split

- **決策**：一套「以 vocoder/波形生成層（非 TTS 系統名）判 disjoint」的四角色 split manifest。
  - **train** = ASVspoof19 LA train（偵測器訓練種子，frozen backbone 為預設；seed corpus 不換）。
  - **dev** = ASVspoof19 LA dev（**唯一**閾值選定集；固定 τ 後**完全凍結**，holdout 結果不得回改 τ）。
  - **primary holdout（test）** = **DFADD 2025-04 corrected release**（HF `isjwdu/DFADD` 公開非 gated；5 種 TTS＝Grad-TTS/NaturalSpeech2/StyleTTS2 三 diffusion + Matcha-TTS/PFlow-TTS 兩 flow-matching；英文 16 kHz、speaker-disjoint），作 generator-disjoint × temporal holdout。
  - **untouched external** = In-the-Wild（Apache-2.0，只做最終 smoke-test）；MLAAD **v9**（gated-contact-share、fake-only、CC BY-NC 4.0）為選配多語廣度，皆 evaluation-only。
  - **中間參照點** = ASVspoof19 LA eval（unseen-attack、同世代），subsample ≤20k，僅作「unseen-attack vs 生成世代/vocoder 新穎性」失效歸因，**不升為新 RQ**。
  - **leakage 控制規格**：逐 utterance 建 manifest `{dataset, generator-family, vocoder/波形生成模組, source-corpus, speaker-ID, sampling-rate, duration, bona-fide-source-overlap}`；disjoint 判在 **vocoder 層**；全部 resample 16 kHz。附「DFADD 5 vocoder（HiFi-GAN/iSTFT/latent-codec decoder，皆 2019 後）對 ASVspoof19 A01–A19 逐項比對表」。無 leakage 的證明＝(a) 逐項 manifest + (b) 分層報告（Δr 須在 speaker-overlap／duration／sampling-rate／source-corpus 各 stratum 內存活）。
- **理由**：Codex E1「名字新 ≠ 嚴格 unseen」——DFADD 與種子語料/vocoder 可能經 VCTK/LJSpeech upstream 重疊，故 disjoint 必判在 vocoder 層並逐一控制 bona-fide 來源重疊（Mahalanobis density 分數對此尤其敏感，M→E 提醒）。採「分層報告取代 speaker 排除」（省資料、對 generator-transfer claim 反而保守）。
- **GPU-hour 影響**：≈ 0（manifest/稽核/resample 皆 CPU metadata）；中間參照點 ≤20k 一格評估 ≈ 0.1–0.2h（重用快取）。
- **待 Codex 查證**：**是**——「DFADD 5 vocoder 對 A01–A19 嚴格 disjoint／確為 unseen」屬 novelty-adjacent，Codex 逐項核可前**只記錄、不斷言「嚴格 unseen/首次」**。
- **砍/延**：砍「train↔holdout speaker-disjoint 硬 gate」（改分層報告）；砍「pilot 就放第二 holdout（CodecFake+ CoSG）」（相位化到全論文，不擴 pilot scope）。

### Q-METRIC — primary metric 與 risk-constraint violation

- **決策**：primary = **development-fixed 操作點下的 risk-constraint violation Δr**。
  - risk 的**單一定義** = **selective miss rate**（accept 區內 fake 被當 real 放行的比例，即部署安全閥真正在意的量；不並列 selective error/FPR 三種）。
  - 在 dev 上固定 τ 使 selective risk = r*（r*∈{5%,10%}），誘導 dev coverage c_dev；把**同一 τ** 套 holdout，量 **Δr = r_obs − r***（配對報 **Δc = c_obs − c_dev**）。
  - violation 判定 = **per-generator-family stratified bootstrap（1000×）95% CI 下界 > 0**。
  - **base-AUROC gate 先報**：holdout base AUROC < ~0.6 的 cell 標「detector-floor」，其 Δr 無意義、不計入 transfer 結論。
  - **次要診斷（同一次前向、零邊際成本）**：AURC（ranking 品質）+ ECE（calibration），把失效分解成 ranking-collapse vs calibration-shift（Codex C1 measurement contribution）。fixed-FPR≤1% selective recall 僅作**單一操作點實例**呈現。
- **理由**：本論文可證偽命題就是「dev 固定閾值跨世代是否仍守預宣稱 accepted-risk 上限」（題目 *Cross-Dataset Risk Violations*），唯一直接量它的是 Δr；AURC/ECE/recall 只能診斷「為什麼違約」或答非所問（M/E/P 三角色 R2 已趨同鎖死）。
- **GPU-hour 影響**：≈ 0（全部由快取 logits+pooled embedding 於 numpy/CPU 算出，bootstrap 亦 CPU；primary metric 是報告/分析決策，不增訓練/評估）。
- **待 Codex 查證**：**是（限 protocol framing）**——metric 本身（selective risk/AURC/ECE，Geifman–El-Yaniv）非 novelty；但「fixed-threshold 跨世代 risk-violation protocol」相對 Salvi 2023／Pascu 2024／FADEL 是否為 residual gap 屬 A1，待查證（並寫進 pilot 轉向 gate）。
- **砍/延**：砍「AURC 當 primary」（threshold-free，測不到 fixed-threshold 是否守住）；砍「fixed-FPR≤1% selective recall 當 primary」（固定 FPR 非風險目標，且分層後負樣本過少使 τ 不穩）。

### Q-SCORES — 最終納入的棄權分數集合

- **決策**：納 **5 種** = **MSP + temperature scaling + energy + Mahalanobis-on-SSL（post-hoc 四件套，+0 GPU）+ FADEL evidential（frozen-backbone + evidential backend）**。softmax entropy 僅作 MSP 免費變體、不算獨立方法。
- **理由**：post-hoc 四件套靠 S1（快取 logits+pooled embedding、共用單次前向）邊際成本為零，砍它們不省錢；FADEL 是 Codex B5 **Verified 的 closest work**、必列 baseline。deep ensemble 與 MC-dropout 是唯二會把 430–520h 炸開的乘數（破壞 P_passes≈1，即 3,500h→300h 那 12× 槓桿的命脈）且不服務本論文 RQ，**全砍、不留 MC-dropout T≤10 後路**（R2 收斂到 M 的更嚴版）。
- **GPU-hour 影響**：post-hoc 四件套 **+0h**；FADEL 3 backbone × frozen backend ≈ **+1~3h**（R2 更正 R1 的「+10~30h」與 P 的「full-FT 18h」，統一為 frozen backend，S6）。
- **待 Codex 查證**：否（分數集合本身不宣稱 novelty，只作 protocol 受測對象）。
- **砍/延**：砍 **deep ensemble**（×5 訓練 + ×5 推論，法則 3）；砍 **MC-dropout**（×T 前向乘數，紅線 R4）——epistemic 家族由 FADEL 單獨代表。

### Q-RQ2 — density vs discriminative 的公平比較（控制 A2）

- **決策**：兩家族分數**一律從同一個 frozen backbone checkpoint 的同一次前向衍生**——discriminative（MSP/energy/temperature）取分類頭 logits；density（Mahalanobis）擬合在**同一組 pooled SSL embedding**。**不另訓練 density model、不另換 backbone**。共用 backbone 的 base AUROC/EER 當**協變量報告**。density（Mahalanobis）結果**只在 within-corpus-overlap stratum 內解讀**（滿足 M 對 bona-fide 重疊污染的顧慮）。
- **理由**：Codex A2 明示不控制共同 backbone 與 representation quality，density vs discriminative 的排序分歧「可能只是 embedding 品質差異」；共用 checkpoint（S4）是唯一能把比較鎖在分數型別上的設計。
- **GPU-hour 影響**：**+0h**（全部來自 Q-SCORES 已快取的同一次前向，離線 numpy/CPU）。
- **待 Codex 查證**：**是**——A2 狀態 Unknown；「density vs discriminative 在同一 unseen-generator protocol 下分家」不得宣稱首次/nobody-asked（TADA、Open-Set Source Tracing、FADEL 皆鄰近），novelty 措辭待查證。
- **砍/延**：砍「為 density 分數另建/另訓表徵或 backbone」（直接落入 A2 的模型容量差陷阱，且多燒訓練 GPU）。

### Q-RQ3 — confident-real 對抗軸的操作化（控制 A3）

- **決策**：**white-box、per-sample PGD-50**（**非** recipe-level——recipe-level 是方向#2 的 laundering 概念，混入即 threat-model bleed；R2 由 T 更正 R1/P 的措辭）。
  - 攻擊目標 = 把 fake 擾動到落入 **confident-real 接受區** = `{判 real}` ∩ `{棄權/信心分數 ≥ RQ1 dev-fixed τ}`；復用 RQ1 的**同一 τ**、同一 holdout、同一 Δr metric。
  - 被攻擊分數 = **3 個可微 post-hoc**（MSP、energy、Mahalanobis-on-SSL；temperature 對 MSP 單調等價不另攻，FADEL 排除於對抗欄）。
  - waveform-domain L∞ PGD、**2 個 SNR 錨定預註冊 ε 點**、**不穿 codec**；攻擊子集 = generator-disjoint holdout 分層抽的 **n≈2,000** fake（clean 下本被正確判 fake 或 abstain 者），不攻全集。
  - 報告：**主報對抗欄 Δr**（攻擊後 r_obs − r*，同一 bootstrap CI）；輔報 confident-real 到達率（`max P(confident-real|fake)` 經驗估計）與「對抗排序是否相對 RQ2 clean 排序翻轉」。不另立第二套 AUROC。
- **理由**：A3——`max P(confident-real|fake)` 本質是「targeted high-conf misclassification + reject option」，前作已有（CLAD、reject-option robustness、Transferable Adversarial Attacks），故不宣稱新攻擊概念；增量只能來自「把標準攻擊當 transfer protocol 的對抗欄壓力讀數」。white-box 是 worst-case/能力上界且便宜（黑盒 10k-query 是紅線 R8，500–1,000h）。
- **GPU-hour 影響**：**≈ 8–16h**（PGD-50 × ~2,000 樣本 × 3 detector × 3 機制 × 2 ε，重用 frozen checkpoint S4 + cached forward S1），落在預留 200h 對抗欄內、餘裕極大。
- **待 Codex 查證**：**是**——「dev-fixed τ + unseen-generator transfer 下量 confident-real 到達率與排序翻轉」相對 CLAD/reject-option 前作的增量，待查是否已有等同 measurement。
- **砍/延**：砍 black-box query 攻擊（R8 紅線→future work）；砍 EOT/BPDA 穿 codec（×10 且屬方向#2 領地）；砍 per-sample 內嵌最佳化搜尋（R7）；砍第 3 個 ε 點；砍對 MC-dropout/ensemble/FADEL 做對抗評估。**ε 預註冊、禁以 test 結果回調**（等同 holdout tuning，併入 no-holdout-tuning 清單 {τ, ε, 分層 seed}）。

### Q-CONTRIB — 貢獻結構 + 可證偽 primary claim

- **決策**：**兩核心 + 一選配 + 一負結果**，不新增第五項：
  - **C1（核心·protocol）**：development-fixed、generator-disjoint、temporal-holdout 的可重現 selective-evaluation protocol（含 split manifest、version/hash、無 holdout tuning）。
  - **C2（核心·failure map）**：在 DFADD（受控新生成器）與 MLAAD v9（多語廣度）holdout 上，量化 risk-constraint violation / coverage collapse / high-confidence error，按 generator family / 語言 / 來源做 failure map。
  - **C3（選配·method）**：僅限 post-hoc、development-only 的 score normalization / conformal risk control；成功標準＝「≥2 個未動過 holdout 上降低 risk violation 且不過度犧牲 coverage」，**非 EER SOTA、不換 backbone**；時間不夠即砍成 future work，論文不受影響。
  - **C4（負結果·成立）**：若所有分數固定閾值都不可轉移，即為「低信心=部署安全閥」在新生成器下不成立的可用負結果——**只在 base-AUROC gate 通過且 confound 已控制時成立**。
  - **可證偽 primary claim（可雙向證偽）**：
    > 在 dev 固定的 risk 操作點 τ（r*∈{5%,10%}）、完全不以 holdout 調參，轉移到 generator-disjoint、時間較新的 holdout 時，**在通過 base-AUROC gate 且 within-stratum 存活的前提下，Δr = r_obs − r* 的 per-generator bootstrap CI 下界 > 0**（系統性違約）。若 Δr 的 CI 涵蓋 0 或落負區 → 閾值可轉移、論文轉正面結論；兩向皆成篇。
- **理由**：Codex A1 已 Refuted「首次把棄權引入 ADD」（Salvi/Pascu/FADEL 為 closest work，必列）；貢獻改鎖「residual gap 的 measurement/failure map」，且 primary claim 內嵌 gate 使「全不可轉移」不與「偵測器近隨機」混淆。
- **GPU-hour 影響**：**0**（C1/C2/C4 是量測/分析；C3 鎖 post-hoc，吃同一次前向快取，S1）。**紅線**：任何要求「訓練校準頭/重訓 backbone」的 C3 變體當場砍。
- **待 Codex 查證**：**是**——「無等同 fixed-threshold 跨世代 risk-transfer protocol」在 Codex 為 Unknown（promising，非 verified novelty），novelty 措辭待查證並寫進 pilot 轉向 gate。
- **砍/延**：砍「棄權首次引入 ADD」當貢獻；砍「新 backbone/新架構」當 method（吃訓練 GPU、超範圍）；砍把 C3 升核心（失敗會拖垮全篇）。

### Q-PILOT — 最小驗證的可執行規格（見第二節詳規）

- **決策**：**1 個 frozen detector（XLS-R 300M frozen + AASIST/線性 backend，訓於 ASVspoof19 LA）／2 分數（MSP + Mahalanobis-on-SSL，同一 frozen 表徵，pilot 就行使 RQ2 兩家族）／dev = ASVspoof19 LA dev（凍結）／2 risk target = 5%、10%／holdout = DFADD 2025-04 之 10–20% 分層（5 family）子集／confound 只用 metadata（UTMOS/ECAPA 逐出 pilot）**。success/stop 數值門檻見第二節。
- **理由**：Codex §10 的最小驗證要求「1 detector + MSP/entropy + 1 embedding score + dev 2 risk targets + generator-disjoint 10–20% subset」，此決策逐項對應且守最省（frozen 在資料受限時可能更好，Scalable AASIST）。pilot 唯一任務是 go/no-go，不是縮小版全論文。
- **GPU-hour 影響**：**≈ 3–6h**（frozen detector ~1h 訓練/快取；MSP+Mahalanobis 全 post-hoc 單次前向；DFADD 10–20% 子集 ~20–40k 評估 ~0.3–0.5h；dev 評估 ~0.3h）。
- **待 Codex 查證**：**是**——轉向條件「找到相同 fixed-threshold + newer-holdout + risk-violation 前作且無 measurement delta」＝把 A1 Unknown 當 pilot 內建 gate；closest-work 複查標「待 Codex 查證」。
- **砍/延**：砍「pilot 上多 detector/多 shift 網格」；砍「pilot 跑 DFADD 全集」（法則 3）；砍「pilot 納 UTMOS/ECAPA 品質協變量」（§10 只要 metadata confound，品質軸下放全論文）；砍「pilot 納 codec/channel 軸」。

---

## 二、可直接執行的 pilot 規格

### 2.1 固定元件（每項一個值）

| 項目 | 規格 |
|---|---|
| **Detector（1，現成 checkpoint）** | XLS-R 300M **frozen** front-end + AASIST/線性 backend；用公開可重現的 w2v2/XLS-R-AASIST checkpoint（訓於 ASVspoof19 LA）。若 calibration 需要，僅重擬 frozen-feature backend（~1h），**不 fine-tune backbone、不用 XLS-R 1B**（R2 死線）。 |
| **dev 集** | ASVspoof19 LA **dev**；在此選定 τ 後**完全凍結**，holdout 不得回改。 |
| **兩個 risk target** | **r* = 5%、10%**（risk = selective miss rate）。 |
| **兩個分數** | **MSP**（discriminative）+ **Mahalanobis-on-SSL**（density），同一 frozen pooled embedding（pilot 就控制 A2）。 |
| **DFADD holdout 子集** | DFADD **2025-04 corrected release** 的 **10–20% 子集**，**跨 5 個 TTS family 分層抽樣**（3 diffusion：Grad-TTS/NaturalSpeech2/StyleTTS2；2 flow-matching：Matcha-TTS/PFlow-TTS）使 per-family bootstrap CI 可估；記錄取得 commit/日期。 |
| **generator-disjoint 與重疊控制** | manifest 逐 utterance 記 `{dataset, generator-family, vocoder/波形生成模組, source-corpus, speaker-ID, sampling-rate, duration, bona-fide-source-overlap}`；disjoint 判在 **vocoder 層**；附 DFADD 5 vocoder（HiFi-GAN/iSTFT/latent-codec decoder）對 ASVspoof19 A01–A19 逐項比對表；bona-fide 側 VCTK/LJSpeech 與 19LA 種子的重疊逐項標記為 stratum（不排除，改分層報告）。全部 resample 16 kHz。 |

### 2.2 要算哪些量（全部由 dev 選定 τ + 已快取分數離線算）

1. **dev**：對 r*∈{5%,10%} 各選 τ，記 dev coverage c_dev。
2. **external（DFADD 子集）**：套同一 τ → observed **risk r_obs、coverage c_obs、Δr = r_obs − r*、Δc = c_obs − c_dev**。
3. **AURC**（threshold-free ranking 品質）+ error-detection **AUROC**（診斷）。
4. **per-generator-family stratified bootstrap（1000×）95% CI on Δr**。
5. **base AUROC/EER gate**（先報，判 detector-floor）。
6. **confound 分層（metadata only）**：Δr 在 duration-bin／sampling-rate／source-corpus·speaker-overlap 各 stratum 內是否存活。

### 2.3 success 條件（全部要滿足）

- (a) 外部 base **AUROC ≥ 0.75**（「不接近隨機」gate）；
- (b) dev 固定 τ → 外部 Δr，且**至少一個 generator family 的 per-generator bootstrap CI 下界 > 0（不跨 0）、可重複**；
- (c) generator-family 層級**無洩漏**（manifest 逐項證明）；
- (d) duration/取樣率/source-corpus 配對後 Δr 仍在（within-stratum 存活，非 confound 捷徑解釋）。

### 2.4 stop/轉向條件（數值化，任一觸發即轉）

- 所有外部 detector **AUROC < 0.6**（abstention 退化成「全拒絕」，detector-floor）；
- **[0.6, 0.75) 標 marginal**：單 detector 不足以定案，須進全論文加第二 detector 再判（消除 P 0.75 與 E 0.6 之間的灰帶雙讀）；
- 找到相同 **fixed-threshold + newer generator-disjoint holdout + risk-violation** 前作且**無 measurement delta**（closest-work 複查，待 Codex）；
- generator metadata 不足以支持 unseen-generator claim；
- 需用 holdout 調 τ（或回調 ε/分層 seed）才有正面結果。

### 2.5 pilot GPU-hour 估計

**≈ 3–6 GPU-h**：frozen detector 訓練/特徵快取 ~1h + DFADD 10–20% 子集（~20–40k 筆）單次前向評估 ~0.3–0.5h + dev 評估 ~0.3h；MSP/Mahalanobis/AURC/bootstrap/confound 全部 post-hoc（CPU，0 GPU）。遠小於全論文，落在幾小時級。

### 2.6 第一週可交付的最小結果

- split manifest v0（含 DFADD↔19LA vocoder/bona-fide 逐項比對表，標「Codex 核可前不斷言 unseen」）；
- base AUROC/EER gate 數字（判是否 detector-floor）；
- 一張 risk–coverage 圖 + 兩個 risk target 的 dev τ；
- DFADD 子集上 Δr、Δc 與 **per-family bootstrap CI**（至少判 success 條件 (b)）；
- confound 分層（metadata）初步表，判 (d) 是否成立。

---

## 三、總帳

### 全論文設計 GPU-hour（deterministic 預設）

| 科目 | 收斂後配置 | GPU-h |
|---|---|---|
| 訓練 | 3 base detector full-FT 6h（或 frozen 更省）+ 3 FADEL frozen-backend ~1h | ≈ 21 |
| 前處理 | SSL pooled 特徵抽取；**channel 協變量改用傳統 CPU codec（Opus/AMR-WB）＝0 GPU**，砍全部 neural codec transcode（消 threat-model bleed，省 20–30h） | 5–10 |
| 評估 | 3 model × 實際 holdout 清單格數（DFADD + In-the-Wild smoke + MLAAD v9 選配 + 19LA-eval 參照）× 20k 分層池 × 0.6，post-hoc 5 機制共用單次前向 | 8–11 |
| 對抗（RQ3） | per-sample PGD-50，~2,000 樣本 × 3 model × **3** 可微機制 × 2 ε | 8–16 |
| 全論文 confound | UTMOS + ECAPA（僅全論文，封頂） | ≤ 6 |
| **核心小計** | deterministic + bootstrap CI 預設 | **≈ 45–65** |
| 選配·多 seed | 僅特定 claim 需 seed 變異時啟用（Codex §9.4「多 seeds 或 deterministic」二擇一，非都要） | (+36) |

- **全論文核心 ≈ 45–65 GPU-h**（含選配多 seed ≈ 80–100h）。
- **pilot ≈ 3–6 GPU-h**。
- **含除錯/重跑/15% 緩衝的實際預期 ≈ 150–250 GPU-h**。

### 這個設計守住了紀律嗎？

**守住了。** 核心 ≈ 45–65h（+pilot 3–6h），僅用 430–520h 封套的 ~1/10–1/8，含緩衝的實際預期 150–250h 仍**遠低於上限，無超支**；四份 R1 高度對齊，R2 全部收斂動作都是「同科學內容更省」或「消除帳面浮數/虛列乘數」（FADEL full-FT→frozen backend、RQ3 5 機制→3、多 seed 移出核心、neural codec→CPU 傳統 codec、pilot 去 UTMOS/ECAPA、RQ3「recipe-level」措辭更正為 per-sample PGD），沒有任何新增實驗/RQ/資料集/baseline，維持了 P_passes≈1 的核心槓桿。**唯一結構性風險是 ~300h 餘裕被當成擴 scope 藉口——餘裕是緩衝，不是空位，任何加軸一律套預算表 §5 公式當場擋回。**

---

## 四、給 Codex 的待查清單（透過 exchange 交接）

1. **A1（Q-METRIC/Q-CONTRIB/Q-PILOT）**：是否存在與「development-fixed threshold + newer generator-disjoint holdout + risk-constraint violation transfer protocol」幾乎等同、且無明確 measurement delta 的前作（超出 Salvi 2023 / Pascu 2024 / FADEL 2025 之外）？——此為 pilot 內建**轉向 gate**，撞到即轉向。
2. **A2（Q-RQ2）**：是否已有二元 ADD 論文在**相同 unseen-generator protocol** 下，以「density-based vs discriminative-derived uncertainty 的排序分歧」為主要研究問題並控制共同 backbone？（TADA、Open-Set Source Tracing、FADEL 為鄰近，需核增量）——novelty 措辭待此查證。
3. **A3（Q-RQ3）**：「dev-fixed τ + unseen-generator transfer 下量 confident-real 到達率與對抗排序翻轉」相對 CLAD / reject-option robustness / Transferable Adversarial Attacks 的**增量價值**，是否已有等同 audio-specific measurement？
4. **E1（Q-SPLIT）**：逐項核 DFADD 5 vocoder（HiFi-GAN/iSTFT/latent-codec decoder）對 ASVspoof19 A01–A19 是否**嚴格 disjoint／確為 unseen**、bona-fide 側 VCTK/LJSpeech 與 19LA 種子重疊程度——Codex 核可前 manifest **只記錄、不斷言「嚴格 unseen」**。
