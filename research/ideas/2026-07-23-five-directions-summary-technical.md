# 五個候選方向摘要（專業版）

日期：2026-07-23。本文為定稿內容摘要；novelty 主張均指「已記錄搜尋範圍內未找到直接同題先作」。查證依據見 `research/validations/2026-07-23-five-directions-contributions-rq-metrics-audit.md`。

---

## D1-B｜來電串流版

**題目**：《來電串流下輕量音訊深偽偵測器之凍結序列選擇策略轉移》
*Source-Frozen Sequential Selective-Policy Transfer of Lightweight Audio Deepfake Detectors for On-Device Call Screening under Unseen Generators*

**貢獻**：建立 call-level sequential selective policy——spoof 為唯一吸收停止態、clean 非吸收監聽至掛斷、棄權綁定升級——分開控制 fake-call miss 與 bona-fide ever-false-alarm 兩類整通風險，並稽核凍結 policy 在 lineage-disjoint 未見生成器上的轉移。部署想定錨於 OS 特權 on-device 篩選（8kHz post-channel）。

**RQ**：
1. 凍結 policy 的雙承諾（`R_fake^call ≤ α`、`R_bona^call ≤ β`）在未見生成器上是否轉移？輕量化額外退化 `Δ_light^seq` 多大？
2. 資料相依停止相對最佳固定截斷 τ 是否 Pareto 改善 latency/coverage？τ*(α,β) 落在第幾秒？
3. （條件性）失效時，future-aware prefix 蒸餾能否在同預算下修回？

**指標**：`R_fake^call`＝P_fake(整通未觸發且未升級)；`R_bona^call`＝P_bona(任一前綴誤觸)；`inflation_bona`；`Δ_light^seq`（source/target × student/teacher 雙重差分）。配平：AUROC/EER tolerance＋部署預算。

**比較策略**：closest work 為固定截斷、無棄權、無風險承諾的超短音訊偵測（"Hi!" ICASSP 2026）——本文量「第幾秒有資格承諾」而非短音訊準確率。統計保證分層：LTT 式校準只在 source 內成立，shift 下轉移為被量測的 outcome。

**停損**：formalization kill test（state machine、synthetic 驗證、LTT 假設界線）不過 → 退 D1-A。

---

## D1-A｜完整語音版

**題目**：《未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留》
*Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators*

**貢獻**：source-frozen、lineage-audited、generator-family-macro 的 selective-policy 外部轉移協定；失效四源診斷（discrimination／ranking／operating point／calibration）；條件性 policy-preserving 蒸餾。

**RQ**：
1. matched 辨識力與部署預算下，`Δ_light > ε`？
2. source-only 的 rank-changing selector 能否修回 tolerance？（TS/Platt 在同 rank 約束重選 threshold 下為 no-op，僅作 control）
3. （條件性）診斷導出的蒸餾機制能否勝過 ordinary KD 與最強合法修法？

**指標**：`L_CR,g`＝P_fake(自動判真 | family g) 的 family-macro；`Δ_light`＝(L_student^tgt−L_student^src)−(L_teacher^tgt−L_teacher^src)。同報 coverage、bona-fide 誤拒、source-locked threshold drift。

**比較策略**：頭號可引用數字「ΔEER≈0 但 Δ_light>0」。輕量化前作（DK-CAST、FTDKD）未量 selective-policy transfer；threshold-transfer 前作（Zhou & Wang 2026 preprint）無棄權維度與壓縮 delta。

**停損**：若退化可由 accuracy/ranking drop 完整解釋 → 撤機制主張，保留為有用負結果。

---

## D3｜攻擊成本前沿

**題目**：《被動語音深偽偵測之適應性洗刷攻擊成功成本前沿評估》
*An Attack-Success Cost-Frontier Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

**貢獻**：預先固定 action space、攻擊者能力與多維成本向量（金錢／計算／步數分開或依 threat persona 加權），以 recipe-level greedy 搜尋輸出 attack-success Pareto frontier（實證上界 c*≤c），並檢驗偵測器排序的穩健性。

**RQ**：
1. 使 TPR@FPR≤1% 跌破可用門檻的最便宜配方，其多維成本前沿為何？
2. 哪些 laundering 動作的效果可被 channel-aware DA 實測恢復、哪些不可？
3. 偵測器排序是否隨 persona 成本權重與配方翻轉？

**指標**：TPR@FPR≤1%、多維成本向量、DA 恢復率、前沿幾何（懸崖／緩坡）。

**比較策略**：robustness 前作（IH&MMSec 2024 laundering database、ReplayDF 2025）量「劣化多大」；本文量「達成劣化最便宜付多少、付哪種幣」。

**停損**：成本排序對權重／seed／shortlist 不穩 → 改報 recipe-level robustness matrix＋敏感度分析。

---

## D4｜zh-TW 詐騙情境評測協定

**題目**：《詐騙情境條件下語音深偽偵測的評估效度審計：一個繁體中文評測協定》
*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Evaluation Protocol*

**貢獻**：zh-TW × 詐騙話術語意 × 時長 × 情緒 × 通道的 crossed 因子設計，以 mixed-effects 估計主效應與預先選定的交互項；UTMOS＋ECAPA proxy 調整後的殘餘關聯；授權與 lineage 明確的可重現評測協定。

**RQ**：
1. 標準朗讀 → 詐騙情境條件，fixed-FPR recall 落差總量？
2. 四軸主效應與交互項效應量？
3. proxy 調整後殘餘關聯剩多少？

**指標**：TPR@FPR≤1% 落差矩陣、mixed-effects 效應量（含 generator/speaker random effects）、proxy 調整後殘餘。

**比較策略**：相鄰前作各佔單軸（時長×通道、情緒 VC、電詐語意、中文電詐集），但無受控 crossed 交互分解；zh-TW×話術語意交集未找到先作。

**停損**：合法可重建的 zh-TW lineage 不成立或因子無法 crossed → 降為小型 controlled diagnostic study。

---

## D5｜浮水印可用承載量前沿

**題目**：《通訊通道下音訊浮水印之可用承載量前沿估計》
*Operational Reliable-Payload Frontier Estimation for Audio Watermarks over Communication Channels*

**貢獻**：固定品質、false-accept 與 block-error 約束下，掃描 payload×ECC 得到各 watermark family 的 operational payload frontier 與塌陷點；並把 detection（可否判定 AI 生成）、payload/provenance（可否解出訊息）、authentication（可否驗證來源）三任務的可行性邊界分開報告。EU AI Act Article 50 僅作 use-case motivation。

**RQ**：
1. 各 family 在 channel×約束矩陣上的 payload frontier 與塌陷點？
2. ECC 能否外推塌陷點？
3. 三任務可行性邊界各在哪？

**指標**：約束下可靠承載 bits、塌陷點位置、ECC 修正後索引位元 k。

**比較策略**：建於 RAW-Bench（Interspeech 2025）之上——它報配定 payload 下的 accuracy，本文答「約束下最多能可靠承載多少」＋任務分離。

**停損**：相對 RAW-Bench 僅增加 codecs 而無新估計問題 → 不作主題，降為 benchmark extension。

---

## 一頁對照

| | D1-B | D1-A | D3 | D4 | D5 |
|---|---|---|---|---|---|
| 核心問題 | 第幾秒有資格承諾 | 凍結策略是否沉默失效 | 攻擊最便宜付多少 | 成績單對詐騙現場灌水多少 | 通道後還能載多少 bit |
| 主指標 | R_fake/R_bona^call、τ*(α,β) | Δ_light、family-macro L_CR | 成本前沿、TPR@FPR | 落差＋交互效應量 | 約束下可靠 bits |
| 勝負維度 | 整通承諾 vs 固定截斷 | policy transfer（前作未量） | 最壞成本 vs 平均劣化 | 受控交互 vs 單軸 | 前沿估計 vs 配定 payload |
| 主要風險 | 形式化 kill test | H1a 可能 null | 成本定義可辯護性 | zh-TW lineage | 殘餘 novelty 薄 |
