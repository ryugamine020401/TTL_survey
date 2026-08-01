# 五個方向決定書

日期：2026-07-23
模式：Compare + Decide
性質：**供作者裁定的決策文件**。彙整 2026-07-13 至 2026-07-23 全部研究紀錄；建議與擬定決策條目均為草案，`DECISIONS.md` 由作者本人寫入，agent 不代寫。
下載／pilot／訓練授權狀態：維持暫停，除本文件明列的門二（~10 GPU-h probe）待作者授權。

## 0. 證據基礎

- 收斂定稿與資料集更新：`discussions/legacy/2026-07-14-convergence/04-final-five-directions.md`、`discussions/legacy/2026-07-14-dataset-refine/03-updated-five-directions.md`
- D1 深化鏈：`discussions/legacy/2026-07-18-thesis-proposal-final.md`、`research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md` 及其引用之全部 validation gate
- 來電場景 round 1（八席、web 查證）：`discussions/legacy/2026-07-23-call-scenario/`（七席發言 + `01-round1-verdict.md`）

## 1. 決策框架

**硬約束（不變）**：一人、一年、單張 RTX 4090、不做真人實測（受騙率不得作因變數）、不建通訊 rig、不訓練 foundation model、不用 target labels 調參、critical-path 資料免申請直接下載。

**本輪新增的兩個決策輸入**：

1. **作者動機已明確化（2026-07-23）**：真正想解的是「手機接到電話能否及時判斷／避免風險」。純數值競爭被作者與紀錄一致否定。
2. **作者對 proposal-final 的貢獻結構表達疑慮（2026-07-23）**：其決策樹四分支僅一支達到預設的方法貢獻 bar。此疑慮與「advisor bar 未確認」（TASKS.md 第一項）同源，仍未解決。

## 2. 五個方向現況判定

### D1｜選擇性策略轉移家族 —— **主線，雙形態**

原「誠實棄權」方向，經 07-15 至 07-23 深化後分裂為兩個形態，共用同一套已完成資產（lineage-clean backbone 查證、ASVspoof 5 C00 manifest、UCB policy 機制、TS/Platt no-op 證明、KD 管線、citation audit）。

**形態 A：proposal-final《未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留》**
- 狀態：題目方向 GO、實驗規格 CONDITIONAL GO（2026-07-18 最終評估）。XLS-R hard blocker 已解（改 wav2vec2-base 等 LibriSpeech-960-only backbone）。
- 貢獻結構：replication + external-validity protocol + 失效診斷；方法貢獻（H2）為條件性。
- 弱點：作者自評貢獻不足；「大機率評測審計、小機率方法貢獻」的賭注結構；與作者來電動機隔一層（stakeholder 是記者離線初篩）。

**形態 B：來電場景 sequential 版（2026-07-23 round 1 裁決：CONDITIONAL）**
- 收斂問題陳述：OS 特權系統 Phone app 的 on-device 想定（Pixel Scam Detection 為部署位置先例）、8kHz post-channel 逐秒前綴串流下，source-frozen sequential selective policy（spoof 為唯一吸收停止態、clean 非吸收監聽至掛斷、棄權綁升級）的風險承諾在 lineage-disjoint 未見生成器上是否轉移；主要可報告量 τ*(α)、optional-stopping inflation、`Δ_light^seq`。
- 關鍵查證（round 1，全 Verified）：第三方 app 攔截來電音訊在 iOS/Android 全滅，但 OS 特權層有真實先例；法律可守窄門為「本機、瞬態、不留存、預設關閉」；通道軸零 rig 可行（ASVspoof 5 內建 C08–C11 電話通道條件）；文獻交集仍空但正被包圍（"Hi!" ICASSP 2026 超短來電偵測、RTCFake ACL 2026），時間窗約一年。
- 預算：≤750 GPU-h、11–12 個月；改錨自形態 A 的沉沒成本趨近零。
- 為何回應作者兩個決策輸入：動機直接對齊（就是來電場景）；貢獻結構較 A 厚——sequential 框架本身（τ*(α)、peeking inflation、非吸收 clean 的 policy 設計）是無論 H1a 結果如何都成立的方法論產物，不像 A 只剩評測審計。
- 解鎖條件（三道門，全開才起草 proposal，任一敗回形態 A，回退損失 ≤3 週）：
  1. **門一（2 週，紙上）**：S 席在「spoof 吸收、clean 非吸收、mid-stream 標籤切換」約束下重寫形式化並給出非平凡有限樣本保證。
  2. **門二（作者授權，一個週末，~10 GPU-h）**：Phase-0 前綴 probe——現成 checkpoint、VAD 對齊，量 {1,2,4,8}s 前綴 vs 全長。無張力或靜音 artifact 主導 → KILL。
  3. **門三（作者，零 GPU）**：確認 ASVspoof 5 免費包含 C08–C11 條件音檔。不含只降級不 kill。

### D3｜adaptive-laundering 攻擊成本上界評估 —— **第一備援**

- 題目：《被動語音深偽偵測之適應性洗刷攻擊成本上界評估》。
- 狀態：定稿健在，未受本輪任何新事證損傷。CodecFake+（MIT、非 gate、G 實測可下載）與 RQ2 不可逆論證直接同構，是資料集更新後獲益最大的方向。
- 承重理由：novelty 最耐久（neural codec transcode 的物理不可逆下界是資訊理論事實，不隨生成器世代過期）；收斂度五方向最高；610 GPU-h 在預算內。
- 距作者動機較遠（攻擊者視角、無即時性），故列備援而非主線。

### D4｜詐騙情境評估效度審計（繁中） —— **第二備援**

- 題目：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文語料為例》。
- 狀態：定稿健在；風險全場最低（180 GPU-h、核心假設幾乎不可能全滅、月 4 保底語料）。
- 本輪新事證：**護城河進一步變窄**——"Hi!"（ICASSP 2026）已做 0.5–2 秒來電開場超短偵測，短句軸再被吃掉一塊；殘餘獨佔區收縮為「zh-TW 話術語意 × 多軸交互 × 品質配對」。仍可守，但兩年後回頭看的獨特性持續流失中。
- 前置：月 0–1 情緒 zh-TW TTS go/no-go（2025 世代 CosyVoice 2／GPT-SoVITS 提高過關機率）。

### D5｜watermark 可靠位元容量審計 + Article 50 —— **第三備援**

- 題目：《通訊通道對音訊浮水印來源標記之可靠位元容量審計及其歐盟人工智慧法第 50 條可讀性判定》。
- 狀態：定稿健在；反脆弱（假設越崩、政策否證越硬）；220 GPU-h；Article 50 於 2026-08-02 生效，政策時效正在最高點。
- 明確限制：定義域是非即時語音訊息／媒體檔案，**明文救不了即時詐騙電話**——與作者動機正交，故列末位備援。

### D2｜真實通道樂觀偏差審計 —— **建議除役**

- 判定依據（三項疊加，均 Verified）：
  1. RTCFake 確證 gated（HF 401，07-14 兩輪實測；07-23 C 席再確認需挑戰賽註冊審核）——違反免申請 hard gate，全案單點故障成為事實；
  2. 搶先已發生：RTCFake 團隊自身以 ACL 2026 發表 600h RTC 傳輸資料集，Delgado 團隊（ASVspoof 組織者）持續佔據真實通道軸——收斂定稿當時的警報「再放一年就沒了」已兌現大半；
  3. 其最有價值的資產已被吸收：電話通道軸由 ASVspoof 5 C08–C11 官方條件承接（免申請、免 rig），γ 校準思路已併入 D1-B 的通道協定（以 ASVspoof 2021 LA 同源配對條件實測模擬 vs 真實 PSTN 差）。
- 除役不等於刪除：紀錄保留，其「模擬 vs 真實落差」的問題意識以 caveat 與校準實驗的形式活在 D1-B 內。

## 3. 綜合比較表

| 方向 | 狀態判定 | 與作者動機距離 | novelty 耐久度 | GPU-h | 最大風險 | 保底產出 |
|---|---|---|---|---|---|---|
| **D1-B 來電 sequential 版** | CONDITIONAL（三道門） | **直接命中** | 中高（sequential policy 框架；但 gap 一年內恐關閉） | ≤750 | 門一形式化做不出；門二無張力 | 回退 D1-A，損失 ≤3 週 |
| **D1-A proposal-final** | GO / CONDITIONAL GO | 隔一層（記者離線） | 中（窄交集） | 中 | 作者已疑慮的貢獻結構；H1a null | bounded 評測審計 |
| **D3 攻擊成本** | 定稿健在 | 遠 | **最高（物理下界不過期）** | 610 | 成本代理可辯護性 | 可逆性圖譜獨立成篇 |
| **D4 現場考卷** | 定稿健在、護城河收縮中 | 中（詐騙場景但非即時） | 中低（被 "Hi!" 等擠壓） | 180 | zh-TW 情緒 TTS go/no-go | 月 4 自足語料 |
| **D5 provenance bit** | 定稿健在 | 正交（明文不救來電） | 中（Article 50 時效紅利） | 220 | 工具鏈成熟度 | 政策級否證 |
| **D2 通道審計** | **建議除役** | 中 | 低（γ 隨當期模型過期） | 510 | 已兌現（gated + 被搶先） | — |

## 4. 建議決定

1. **主線：D1 家族，B 優先、A 為內建退路。** 立即執行三道門（門一紙上作業可即刻開工；門二需作者授權 ~10 GPU-h；門三零 GPU）。三門全開 → 起草來電版 proposal 與 proposal-final 並排，作者終裁；任一門敗 → 回 D1-A，來電場景寫進 motivation 與 future work。
2. **與門並行、不受門結果影響的必辦事項：把 proposal v2/final 送指導教授確認貢獻 bar。** 兩形態共用此依賴；作者的「貢獻不足」疑慮只有 advisor 能終結。若 advisor 判 replication+protocol 不達 bar，D1-A 單獨存活性存疑，D1-B 的 sequential 方法論貢獻與 D3 的權重應上調。
3. **備援序：D3 → D4 → D5。** 觸發條件：D1 兩形態均被 kill（門敗且 advisor 否決 A）。
4. **D2 正式除役**，資產併入 D1-B。

## 5. 擬定之 DECISIONS.md 條目（草案，僅供作者採用或修改）

> **2026-07-23 — 確立 D1 選擇性策略轉移為主線，來電場景 sequential 版為優先形態；D2 除役。**
> 主線為輕量音訊深偽偵測器之 source-frozen selective policy 在未見生成器上的轉移問題，含兩形態：來電場景 sequential 版（B）與完整語音版 proposal-final（A）。B 受三道門節制（sequential 形式化、Phase-0 前綴 probe、ASVspoof 5 C08–C11 確認），任一門敗回退 A。方向二（真實通道樂觀偏差審計）因 RTCFake gated 確證與搶先兌現除役，其通道校準思路併入 B。備援序為 D3 攻擊成本 → D4 現場考卷 → D5 provenance。指導教授對貢獻 bar 的確認為兩形態共同前置，尚未完成。授權門二之 ~10 GPU-h Phase-0 probe；其餘下載／pilot／訓練維持暫停。

（若作者僅願先開門、不願定方向，可將末段改為：「本條目僅確立探索優先序，最終題目待三道門與指導教授意見後另立條目。」）

## 6. 未解事項與停損

- **Advisor bar**（兩形態共同前置）——未確認前不進 Phase 0。
- 門一失敗、門二無張力、或正式檢索發現「因果前綴＋棄權＋風險保證」的 ADD 先行工作 → B kill。
- D1-A 的既有 kill 條件（final assessment §9）全部維持。
- 本文件不更動 `PROJECT.md`／`TASKS.md`；作者採納後由作者指示更新。
