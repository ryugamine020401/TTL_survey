# A-detection 偵測與選擇性預測專家席 — Round 1 發言

日期：2026-07-23。已讀 Gate 三席判決摘要，接受 P 席改錨後場景：OS-privileged 系統 Phone app 的 on-device 篩選，estimand 錨在 8kHz、單通道、逐秒前綴、on-device、無雲端，論文只做離線模擬。

## 立場摘要（≤5 行）

現有機器約六成可直接搬：selective policy 擬合程式碼、KD 管線、lineage-clean backbone、資料集選型全部保留；必須重做的是 estimand（`Δ_light` → `Δ_light(τ)` 或 commit-time 泛函）與統計機
制（交給 S 席）。不需要 chunk-based 串流架構重設計——離線「前綴重評分」是可辯護的模擬代理。最大隱藏地雷：**前綴評估會把 ASVspoof19 的 leading-silence 捷徑放大到極致**，前綴必須錨在語音起點而非檔案起點。資料面 ASVspoof 5 直接可用（平均 7–12 秒 + 內建 8kHz 窄帶條件）。最小骨架 3 模型 × 7 前綴格點 × 2 通道條件，總計 <250 GPU-h，單張 4090 可行。

## 主體分析

### 1. 哪些機器直接可用、哪些要重做

**直接可用**：(a) selective policy 的核心資產——`(t_m, q_m)` source-frozen 擬合、UCB 約束、`L_CR` endpoint、coverage 聯合約束（防全棄權）——概念與程式碼都能搬，只是決策單位從 utterance 換成 utterance 前綴〔Inference〕。(b) KD 輕量化管線與 teacher/student 對照結構原樣保留。(c) lineage-clean backbone（wav2vec2-base，LibriSpeech-960-only）不受場景切換影響，lineage 稽核成果全數繼承。(d) 資料集選型與免申請 hard gate 不變。

**必須重做**：(a) `Δ_light` 要從純量變成前綴長度 τ 的函數 `Δ_light(τ)`，或進一步壓成 commit-time 泛函（如「風險約束下的平均 commit 時間之 teacher-relative 差」）——後者才呼應 G 席「gap 必須錨在 commit-time 統計判定」的裁定，具體形式化交 S 席〔Inference〕。(b) 棄權語意分裂為「繼續聽」與「終局棄權/升級查證」，policy 從單點 `(t,q)` 變成序列規則；擬合程式可沿用骨架但決策幾何是新的。(c) family bootstrap 要處理同一 utterance 各前綴間的相依性，utterance 級獨立性假設不再免費成立——這是 S 席命脈。

### 2. 短前綴下 SSL 偵測器的已知劣化

**Verified**（查證日 2026-07-23）：短 utterance 劣化是已知且被專門研究的現象。AASIST2（Zhang & Lu, "Improving Short Utterance Anti-Spoofing with AASIST2"）專攻短語音；社群通行數字為 <2 秒段 EER 常 >10%，2–4 秒才降到 ~5% 量級（https://www.semanticscholar.org/paper/0dd73d31bfbe1f1aa574f939bf1516dad0f172ba ；https://arxiv.org/pdf/2508.09294 亦報 <3 秒 EER 9.44%）。「Hi!」（arXiv:2601.19573, 2026-01-27）直接做 0.5–2.0 秒超短輸入 + 通訊劣化（https://arxiv.org/abs/2601.19573）。**含義**：頭 1–3 秒正是偵測器最弱、棄權最必要的區間，所以「何時才有資格 commit」有真實張力，不是人造問題；但單畫長度-EER 曲線已被畫過（G 席同判），貢獻必須落在 frozen policy 的 commit-time 行為。

**Verified（關鍵地雷）**：Müller et al.「Speech is Silver, Silence is Golden」（arXiv:2106.12914, ASVspoof workshop 2021）證明 ASVspoof19 的 bona fide/spoof leading-silence 長度分佈不均，只用前導靜音長度就能達 EER 15.1%（https://arxiv.org/abs/2106.12914 ；後續 arXiv:2309.11827）。前綴評估把「檔案前幾秒」變成整個判定依據，等於**把這個捷徑放大到最大**：一個 1 秒前綴可能大半是靜音。若不處理，整個前綴 benchmark 量到的是靜音長度不是深偽證據。對策：前綴時間零點必須定義為 VAD 偵測的語音起點（能量式 VAD，不用 target labels，合規），並報告 trim/不 trim 雙版本；19LA 只能當 secondary。

### 3. 串流推論是否需要 chunk-based 重設計

**Verified**：wav2vec2 是非因果架構——feature encoder 的 group norm 與 kernel~128 卷積、雙向 attention 都不適合因果串流，強制因果化會嚴重劣化；串流化需 chunk-mask 重訓或 lookahead 設計（https://arxiv.org/pdf/2109.07327 ；https://arxiv.org/pdf/2110.05241）。**但**：P 席已錨定論文只做離線模擬，因此正確做法是**前綴重評分**（每個前綴獨立跑一次完整 forward）——這在統計上完全等價於「一個非因果模型每秒對到目前為止的音訊重新推論」，部署上也真實存在（重評分的 RTF 成本誠實報告即可，Pixel 級硬體跑 base 模型逐秒重評分並非天方夜譚，何況 student 更小）〔Inference〕。**明確反對**把 chunk-based 因果重訓收進範圍：那是第二篇論文的量級，且會汙染與 proposal-final 的 teacher/student 對照。額外機會〔Hypothesis〕：KD 可自然升級為「full-context teacher → prefix student」的 future-aware 蒸餾，串流語音翻譯已有先例（arXiv:2303.07914），這給 H2 一個場景原生的機制候選，而非硬湊。

### 4. 資料面：現有資料集能否支撐前綴評估

**Verified**：ASVspoof 5 訓練集平均 11.92s（SD 2.99）、dev 平均 7.08s（https://arxiv.org/pdf/2502.08857 ；https://www.sciencedirect.com/science/article/pii/S0885230825000506），支撐到 ~8s 的前綴格點綽綽有餘；且內建 C08(Opus)/C09(AMR)/C10(Speex) 8kHz 窄帶與 C11 真實 PSTN 條件（G 席同判），電話通道軸免自建。19LA 平均僅 2–4 秒 + 靜音捷徑，只能當 secondary/煙霧測試。**逐步截短完整 utterance 即可支撐錨定後的 estimand**——per-utterance 前綴判定不需要真對話資料；真實來電對話動態（真人開場再切 VC）屬 D 席攻擊面，不進主 estimand〔Inference〕。RTCFake（ACL 2026）可列 robustness 候選。

### 5. 最小實驗骨架與算力

- **模型 3 個**：teacher（wav2vec2-base + 輕 head）、student ×2（截層 KD 4-6 層版、更小版），維持 H1a 對照結構。
- **前綴格點 7 點**：τ ∈ {0.5, 1, 2, 3, 4, 6, 8}s，自 VAD 語音起點起算。
- **條件 2 組**：16kHz clean、8kHz 窄帶（ASVspoof5 內建條件或 C 席離線模擬）。
- **粗估**〔Inference〕：訓練/蒸餾 3 模型 ≈ 50–70 GPU-h；前綴評分（ASVspoof5 selected subset ~104k utt × 7 前綴，總音訊量 ~680h，RTF~0.02）≈ 15 GPU-h/模型/條件 → ~90 GPU-h；含 bootstrap 重擬合與重跑緩衝，全輪 <250 GPU-h，單張 4090 約 3–4 週日曆。Phase-0 前綴 probe（不訓練，現成 checkpoint + 截短）一個週末可出「有沒有張力」的生死訊號。

## 對候選研究問題的具體修改或否決

不否決，三項修改：(1) estimand 明寫「前綴自 VAD 語音起點對齊，報告靜音處理敏感度」，否則 benchmark 無效；(2) 明寫「離線前綴重評分為串流模擬代理，不做因果架構重設計」，把 RTF 報告列為部署可行性證據而非工程交付；(3) 主 comparative estimand 定為 commit-time 泛函的 teacher-relative 差（`Δ_light` 的序列版），保住與 proposal-final 的連續性與 G 席要求。

## Kill conditions

1. Phase-0 前綴 probe 顯示 1 秒前綴效能已 ≈ 完整 utterance（無「多聽有益」張力）→ sequential 問題是空的，kill。
2. S 席無法在相依前綴上給出非平凡 anytime 風險保證 → 退化為長度-EER 曲線，kill（與 G 席同判）。
3. VAD 對齊後仍發現前綴分數被靜音/起點 artifact 主導且無法控制 → benchmark 不可信，kill。
4. 評估成本失控（格點 × bootstrap × 模型 >500 GPU-h）→ 砍格點；砍到 3 點仍不夠則場景不可行。

## 給下一波的一句話

給 S：policy 擬合程式碼與 UCB 骨架可直接給你，但相依前綴上的風險保證與「繼續聽 vs 終局棄權」的語意切分是你的，做不出非平凡結果就啟動我的 kill 條件 2；給 C：我只需要你把 ASVspoof5 窄帶條件與離線 codec 模擬對齊到同一前綴格點。

## 附：搜尋詞紀錄

- "short utterance audio deepfake detection performance degradation duration EER wav2vec2"
- ""Hi!" ICASSP 2026 short audio deepfake detection incoming call 0.5s 2s lightweight arXiv 2601.19573"
- "Müller "silence is golden" ASVspoof 2019 leading silence duration shortcut deepfake detection"
- "ASVspoof 2019 LA average utterance duration seconds trim truncate 4 seconds training"
- "wav2vec2 streaming inference non-causal bidirectional transformer chunk causal masking incremental prefix re-computation"
- "AASIST short utterance duration analysis anti-spoofing 1 second 2 second EER increase length robustness"
- "ASVspoof 5 utterance duration seconds average crowdsourced MLS codec conditions C08 C09 C10 C11 8kHz bandwidth"
