# 來電場景版研究問題 — 討論設定（Round 1）

日期：2026-07-23
發起人：作者（經與 Claude 討論後定案編制）
狀態：問題琢磨階段。本討論**不取代** `discussions/2026-07-18-thesis-proposal-final.md`（現行計畫書），而是並行探索作者真實動機的可守版本；產出將與 proposal-final 並排比較後由作者裁定。

---

## 1. 作者的真實動機（本輪的固定出發點）

> 手機接到電話時，有沒有辦法**及時**判斷對方聲音是不是深偽？或者說，有沒有方法可以更準確地判斷、或避免受騙風險？

作者已知的顧慮：這個方向可能淪為數值競爭（刷準確率），而且新生成器不斷出現、偵測器準確率持續劣化。本輪的任務不是刷數字，而是把這個動機**琢磨成一個可以在硬約束下辯護的研究問題**，或誠實宣判它不可行並提出改錨方案。

## 2. 候選研究問題（Hypothesis 等級，本輪的琢磨對象）

> 來電場景下，輕量音訊深偽偵測器**聽到第幾秒**才有資格給出守得住風險承諾的判定？在此之前必須棄權（繼續聽或升級查證）。

即：把 proposal-final 的 source-frozen selective policy 從「完整語音 → 三態輸出」推廣為「串流前綴 → anytime 三態輸出」，判定單位從 utterance 變成 utterance 前綴，音訊沿時間逐步到達。

這只是候選形式化，各角色可以修改、推翻或提出替代——但最終必須收斂回**一個**問題。

## 3. 已識別的三個死穴（角色任務由此而來）

1. **音訊逐秒到達**：判定變成 sequential decision，需要新的方法論（anytime/early-decision、sequential risk control）。
2. **音訊走過電話通道**：8kHz、AMR/Opus/EVS、丟包。原方向二紀錄已判：離線 codec 模擬可行，自建電信 rig「日曆無界」禁止。
3. **「手機接到電話」本身**：iOS/Android 對第三方 app 存取通話音訊的限制、通話錄音的合法性。若無任何可部署行為者能合法取得通話音訊流，場景即為空中樓閣。**這是第一優先 kill question。**

## 4. 繼承的硬約束（不因換場景而鬆動）

- 一位碩士生、一年、單張 RTX 4090（24GB）。
- 不做真人實測；受騙率不得作因變數（`2026-07-14-convergence/00-constraints.md` 裁定）。
- 不自建蜂巢電信/通訊軟體 rig；真實通道只能用現成可下載資料或離線模擬。
- 不用 target labels 調參；不訓練 foundation model。
- critical-path 資料集必須免申請直接下載。
- 討論是腦力激盪產物，不是同儕審查；重要主張標注 **Verified / Inference / Hypothesis / Unknown**，Verified 必須附當前來源。

## 5. 編制與任務

### Gate 席（第一波，持 kill 權）

- **P-platform 行動平台工程師**：宣判「誰能拿到通話音訊」。iOS/Android 通話音訊 API 現況、Google Call Screen 等先例、carrier/OS/app 三種部署點、擴音側錄等 workaround。若全滅，提出場景改錨選項（語音訊息、視訊會議、擴音側錄、carrier 端）。
- **L-legal 法律與隱私專家**：通話錄音/監聽合法性（台灣通保法脈絡、GDPR、美國 two-party consent 等代表性法域）、本機處理 vs 上雲的隱私差異、平台政策。輸出為背景論證，非專業法律意見。
- **G-historian 文獻史官**：closest-work 查證。partial/segment-level spoof detection（如 PartialSpoof）、streaming/real-time ADD、early-exit 推論、電話通道 ADD（含 Delgado 團隊 arXiv 2509.26471 後續動向）、sequential decision 在 ADD 的應用。宣判「streaming × selective policy × 輕量化 × 未見生成器」交集是否仍空著，列出最近的三篇工作。

### Formalize 席（第二波，收到 Gate 判決後發言）

- **S-sequential 統計方法學家**：把「聽到第幾秒才 commit」形式化。sequential testing、anytime-valid 風險控制、前綴長度作為 coverage 新維度；estimand 要乾淨，防止「即時」淪為把音訊切短的數值遊戲。
- **A-detection 偵測與選擇性預測專家**：現有機器（selective policy、`Δ_light`、KD 輕量化、UCB policy fitting）哪些可以直接搬進串流前綴、哪些必須重做;短音訊下 SSL 偵測器的已知劣化。
- **C-signal 電信通道訊號專家**：哪些通道效應可離線模擬（codec、PLR，CPU 可做）、哪些做不到;串流場景下通道模擬與前綴評估如何組合;繼承原方向二的教訓。
- **D-redteam 紅隊**：來電場景新攻擊面——攻擊者是活人在線上，可即時適應（真人開場再切 VC、誘發棄權疲勞、壓低音量/製造噪音）;streaming VC 現況;沿用「不給攻擊者背書」判準。

### Converge 席（第三波）

- **H-professor 教授兼收斂法官**：合併原 H 與算力鷹派/收斂法官職能。執行「這還是一個問題嗎」測試、一年日曆與 GPU 粗算、與 proposal-final 的並排比較（改錨成本 vs 保留現題把來電寫進 motivation）。持有 kill switch：若 P/L 判定無合法可部署點，裁定轉向場景改錨。**不寫入 DECISIONS/PROJECT/TASKS**，只產出建議。

### 刻意不設席

B-crypto/provenance（即時通話明文在 provenance 定義域外）、E-visionary（歷史上的範圍爆炸源）、F-public（受騙率已不得作因變數，使用者視角由 H 在部署價值層代管）。

## 6. 議程與 kill 順序

1. P/L/G 各自獨立發言（不互看），各給 verdict 與 kill 判定。
2. S/A/C/D 收到 Gate 三席判決摘要後發言;若 Gate 已觸發改錨，則對改錨後的場景發言。
3. H 讀全部七份發言，產出 round-1 裁決：問題陳述收斂版（或改錨版）、與 proposal-final 的比較、下一輪需要什麼、kill/pivot 條件。

## 7. 輸出格式要求（每一席）

- 檔案：`discussions/2026-07-23-call-scenario/round1/<席位代號>.md`，繁體中文。
- 必含段落：**立場摘要**（≤5 行）、**主體分析**（重要主張標 Verified/Inference/Hypothesis/Unknown，Verified 附來源 URL 與查證日期）、**對候選研究問題的具體修改或否決**、**kill conditions**（什麼證據出現就該放棄我支持的路線）、**給下一波的一句話**。
- 需要當前事實（API 現況、法規、文獻、SOTA）一律先 web 查證再主張，記錄搜尋詞。
- 長度 800–2000 字;超出者刪次要內容。
