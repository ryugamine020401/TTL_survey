# 五個方向：查證後定稿（Codex 驗證 A–E 套用版）

日期：2026-07-15
基礎：`discussions/2026-07-14-dataset-refine/03-updated-five-directions.md`（資料集更新版）
套用：`research/validations/2026-07-15-claims-to-verify-a-d.md`（Codex 對 A–E 的完整查證）
性質：**規劃文件更新，維持誠實。非正式定題**——依作者裁定，正式定題（寫 `DECISIONS.md`）前需先跑 pilot；此更新不需 pilot 即可進行。

> 一句話：Codex 的查證推翻了我多輪 agent 辯論裡好幾個「零前作」宣稱，並更正了具體事實。本文把這些更正**如實套進**五個方向——多數方向**仍成立**，但貢獻要從「首次做 X」改成「X 的 residual gap」，題目與資料集也依查證修正。**這些 residual gap 是 promising，不是已證實的 novelty**；pilot 的目的就是把 promising 變成可辯護。

---

## 一、查證改了什麼（總覽）

| 項目 | 我方 agent 原宣稱 | Codex 查證 | 套用動作 |
|---|---|---|---|
| **A1** selective ADD 棄權 | 「無前作」 | **Refuted**：Salvi(ICASSP 2023)、Pascu(Interspeech 2024) 已做 reliability threshold + 保留率曲線；FADEL(ICASSP 2025) evidential | 方向#1 保留，但貢獻改為「固定閾值跨世代 transfer 的 risk violation」；三者列 closest work |
| **A5** watermark×neural codec | 「前作未碰」 | **Refuted**：AudioMarkBench(NeurIPS 2024)、RAW-Bench/Özer(Interspeech 2025)、WMCodec 已碰 | 方向#5 收窄到「特定平台×codec×latency 的 BER–payload frontier」 |
| **A6** Article 50 審計 | 「零前作」 | **Refuted**：EU 官方已出 Article 50 audio marking 技術文件與 code of practice | 方向#5 的法規面收窄為 deployment-context，不當唯一技術貢獻 |
| **A8** 真實電信通道審計 | 「唯一無前作空白」 | **Refuted**：Delgado(2025 preprint)、RTCFake(ACL 2026, 600h) 已做 | 方向#4(原 D2) 降級；主張改為「真實 vs 模擬的 paired optimism gap」 |
| **A7** 繁中四軸 | 「撞題最少」 | **Unknown**，但鄰近撞題多（First Greeting、EmoFake、TeleAntiFraud-28k）；四軸嚴重 confounding | 方向#3(原 D4) 從四軸**收窄到兩軸**（duration × emotion） |
| **A2/A3/A4** | 「沒人問過 / 完全缺席 / 資訊理論錨」 | **Unknown / 跨領域已有**：reject-option adversarial 已有；reversibility「下界」缺形式化 | 保留為 RQ，但不得宣稱首次；A4 需 kill test 否則刪「information-theoretic bound」措辭 |
| **B4** Codecfake | 「IEEE TASLP 2024、source tracing」 | **更正**：Interspeech 2024、binary detection、1,058,216 筆 | 引用更正 |
| **B8** STOPA | 「= arXiv 2505.14188」 | **Refuted 混淆**：2505.14188 是 Negroni 的 Source Verification；STOPA 是 Firc et al. 另一篇 | 拆成兩篇分別引用 |
| **C2** EER 13.5–50% | 「閉源生成器所致」 | **因果過度**：VoiceWukong 混商用+開源+manipulation | 改中性寫法（見下） |
| **E1** DFADD | 「2024、diffusion/FM」 | **Verified 但**：SLT 2024、5 種 TTS（3 diffusion+2 FM）、MIT+upstream；**名字新 ≠ 嚴格 unseen** | 採用，但 split manifest 須逐一控制訓練語料/vocoder 重疊 |
| **E2** CodecFake+ | 「與 CodecFake 不同、別搞混」 | **更正**：它**就是** Interspeech 2024 CodecFake 的後繼（TASLP 2026）；CoRS≠CoSG | 採用，明確指定用 CoSG 做 laundering 對象 |
| **E4** MLAAD v10 | 「2025、v10、公開下載」 | **Refuted**：官方目前 **v9**、gated-contact-share、fake-only、CC BY-NC 4.0 | 改寫為 v9；不能用「v10 最新公開」當賣點 |
| **E5** SpeechFake | 「Apache-2.0」 | **Partially refuted**：中文 coverage ✅；但 real 為 CC BY-NC 4.0、部分 GPL-3.0 | 採用為 zh 對照，但正式用前建 license matrix |
| **E6** 2025 zh 情緒 TTS | 「2025 世代、台灣國語+哭腔/急迫」 | **Partially refuted**：CosyVoice2 是 2024-12、OpenVoice v2 是 2024-04；台灣國語+情緒**未驗證** | 方向#3 必須先 pilot；達不到門檻就縮成現成 zh-CN 比較 |
| **E3** RTCFake | 「HF 可下載、月0 驗證」 | **Unknown**：HTTP 401，非確認的 gated flow，redistribution 未知 | 方向#4/#5 **不得把 RTCFake 放關鍵路徑**；必須有純模擬退路 |
| **C1** VoiceWukong per-sample | 「Zenodo 申請可得人類標籤」 | **Unknown**：粒度未證實 | 不得放關鍵路徑（本已因放棄受騙率而非主線） |

**沒被推翻的**：C3（ASVspoof21 DF=611,829，Verified）、C4（C2PA 五目標未達成，Verified 為作者結論、需標 preprint）、B1/B2/B5/B6（D-CAPTCHA、StreamVC、FADEL、Authenticated Contradictions 皆 Verified）。GPU-hour 全部維持定稿、偵測器全程 frozen——查證**沒有**擴充任何實驗。

---

## 二、查證後的推薦排序

Codex 依查證重排（第 7 節）：**#1 → #2(原D3) → #3(原D4) → #4(原D2) → #5(原D5)**。與資料集精修版的差異：原 D2（真實通道）因 A8 被否證 + 前作碰撞，從 co-首選降到第 4；原 D5（watermark）因 A5 被否證收窄到第 5。方向#1 仍穩居第一。

---

## 三、五個方向（逐一，查證後）

### 推薦 #1 — 未知生成器下深偽偵測棄權門檻的可轉移性
- **中**：《未知語音生成器下深偽偵測棄權門檻的可轉移性：跨資料集風險違約與失效邊界》
- **英**：*Transferability of Abstention Thresholds for Audio Deepfake Detection under Unseen Generators: Cross-Dataset Risk Violations and Failure Boundaries*
- **一句話問題**：在開發集固定一個 risk/coverage 操作點、完全不以外部資料調參，轉移到時間較新且 generator-disjoint 的 holdout 時，實際風險上限超標多少、在哪裡崩？
- **三個 RQ（同一套方法：棄權分數 × shift 網格 × risk–coverage，一次前向快取三種切片）**
  - RQ1（轉移）：dev 固定閾值轉到 unseen-generator/unseen-channel holdout，selective risk 是否仍守住預宣稱上限？（fixed-FPR≤1% selective recall / AURC / ECE）
  - RQ2（分岔）：density-based 與 discriminative-derived 分數在同格是否分道揚鑣？（**須控制共同 backbone 與 representation quality，否則只是模型容量差異——Codex A2**）
  - RQ3（對抗）：把棄權推進 confident-real 區的最低成本？排序在對抗欄下是否翻轉？（**須給明確 threat model + query/quality budget，相對一般 targeted attack 的增量價值——Codex A3**）
- **貢獻（誠實版）**：不是「首次把棄權引入 ADD」。是 (a) development-fixed、generator-disjoint、temporal-holdout 的**可重現 selective-evaluation protocol**；(b) 量化 risk-constraint violation / coverage collapse / high-confidence error 的 failure map；(c)（選配）輕量 development-only 的 score normalization / conformal risk control；(d) 若所有分數閾值都不可轉移，則為可用的**負結果**。
- **Closest work（必列，非一筆帶過）**：Salvi et al.(ICASSP 2023)、Pascu et al.(Interspeech 2024)、FADEL(ICASSP 2025)。
- **資料集**：ASVspoof 2019 LA（訓練種子，**不換**，換即重訓）；**DFADD**（SLT 2024, arXiv 2409.08731, HF `isjwdu/DFADD` 公開非 gated, MIT+upstream attribution；記錄取得 commit/日期用 2025-04 修正版）作 unseen-generator 軸——**但 split manifest 須逐一控制訓練語料/vocoder 重疊，「名字新 ≠ 嚴格 unseen」**；**MLAAD v9**（非 v10；官方 gated-contact-share、fake-only、CC BY-NC 4.0）作多語廣度；In-the-Wild（Apache 2.0）作 smoke-test。
- **GPU**：430–520 h（不變）。**保底**：月 1–4 的 shift benchmark + calibration，不依賴任何申請。

### 推薦 #2（原 D3）— 被動偵測之 adaptive-laundering 攻擊成本上界
- **中**：《被動語音深偽偵測之適應性洗刷攻擊成本上界評估》
- **英**：*An Attacker-Cost Upper-Bound Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*
- **一句話問題**：對一個被動偵測器，攻擊者讓它失效最便宜要付多少（成本上界）？
- **三個 RQ（同一套方法：固定偵測器 + 離線 laundering 動作空間，一次 recipe-level greedy 搜尋，三種讀法）**
  - RQ1：讓 recall 跌破可用門檻的最便宜 laundering 配方（**輸出「成本上界」——接受 Codex B 的「列舉≠全稱」指正，不宣稱下界**）
  - RQ2：配方裡哪些可逆（DA 追得回）、哪些踩到 neural codec transcode 的不可逆
  - RQ3：攻擊成本–recall 曲線是懸崖還是緩坡
- **查證修正**：A4 的「物理可逆性資訊理論下界」**Unknown/未獲支持**——先做 2–3 個 transformation family 的 **kill test**（toy model 能否推出可檢驗 prediction）；不成立就**刪掉「information-theoretic lower bound」措辭**，改純經驗描述。RQ3 的 generic adversarial reject-option 已有前作（CLAD 等），須標增量價值。
- **資料集**：ASVspoof 2019 LA（種子不換）；**CodecFake+**（HF `CodecFake/CodecFake_Plus_Dataset` 公開非 gated, MIT repo-level, ~101GB；**它是 Interspeech 2024 CodecFake 的後繼/TASLP 2026，非另一資料集**；laundering 對象用 **CoSG** 部分，勿用 CoRS 混淆 threat model）；**DFADD** 作 unseen-generator 軸。抽 20k 確認/10k 搜尋。
- **GPU**：610 h（不變）。收斂度全場最高、貢獻不隨生成器過期。

### 推薦 #3（原 D4）— 詐騙情境條件下偵測的評估效度審計（繁中，收窄為兩軸）
- **中**：《詐騙情境條件下語音深偽偵測的評估效度審計：以繁體中文短語音與情緒為例》
- **英**：*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Short-Utterance and Emotion Study*
- **一句話問題**：現行 benchmark 用朗讀長句量的偵測率，對「詐騙現場的短、帶情緒語音」高估了多少？
- **查證修正（重要）**：原四軸（話術語意×短句×情緒×通道）Codex 判**嚴重 confounding、一年難估交互**，**收窄為兩個可控因素：duration × emotion**（通道作單一協變量而非交叉軸）；不把「繁中/詐騙語意本身」當已驗證 novelty。鄰近前作須引：First Greeting(2601.19573)、EmoFake、TeleAntiFraud-28k。
- **三個 RQ（同一套方法：一份 duration×emotion 分層語料，frozen 偵測器 fixed-FPR recall，讀三次）**：RQ1 總落差；RQ2 duration×emotion 主效應與交互；RQ3 品質協變量（UTMOS/ECAPA）配對後淨落差。
- **資料集**：自建 zh-TW（**但先做 E6 的 20–50 句 pilot**：選 2 個 license 清楚、機制不同的模型——如 OpenVoice v2 (MIT) + F5-TTS(code MIT/weights NC)——用**有同意的台灣說話者** reference，人工確認腔調/情緒/可懂度/identity leakage 達預註冊門檻；**達不到就縮成現成 zh-CN 比較**）；對照用 **CFAD**（Zenodo, 35.6GB, license 待確認）、**SpeechFake zh 部**（先建 license matrix）。
- **GPU**：~180 h（不變，最寬鬆）。失敗退路最可靠。

### 推薦 #4（原 D2）— 真實 vs 模擬通道的樂觀偏差（降級 + 去單點故障）
- **中**：《真實通道上音訊深偽反制訊號存活的樂觀偏差及其畸變層歸因》
- **英**：*Optimism Bias in the Survival of Audio Deepfake Countermeasure Signals over Communication Channels: A Distortion-Layer Attribution*
- **查證修正**：A8 被否證（Delgado 2025、RTCFake ACL 2026 已做真實通道）→ 唯一可守的是「**同 utterance 的 real-platform vs 可重現 simulation 的 paired optimism gap**」或不同 threat model。**RTCFake 不得放關鍵路徑**（E3: HTTP 401、redistribution 未知）——必須以「純模擬 codec 階梯（Opus+AMR-WB×bitrate×PLR）+ AudioSeal watermark 存活」為**主線**，RTCFake 若人工審核後可用才作加分臂。
- **三 RQ**：RQ1 偵測器 recall 存活差分 γ；RQ2 AudioSeal watermark bit 存活；RQ3 畸變層歸因（codec/丟包/DSP 哪層造成 γ、DA 能否救回）。
- **GPU**：~510 h。**停止條件**：若拿不到任何真實通道資料且模擬已足夠代表（γ≈1），論文轉為「模擬保真度的正面驗證」——仍成篇。
- **資料集**：3 家 **2025 世代乾淨開源 TTS**（換 XTTS/VITS/YourTTS）；real 用公開語料；watermark 用 AudioSeal。

### 推薦 #5（原 D5）— 通訊條件下 watermark 的可靠位元容量前緣（收窄）
- **中**：《通訊通道對音訊浮水印來源標記之可靠位元容量審計》
- **英**：*A Reliable-Bit Capacity Audit of Audio Watermark Provenance over Communication Channels*
- **查證修正**：A5 被否證（AudioMarkBench、RAW-Bench/Özer 2505.19663、WMCodec 已碰 neural codec）→ **必須全部納入 baseline**，主張收窄為「**固定真實 RTC 平台 × 特定 neural codec × latency/payload 的可達 BER–payload Pareto frontier**」，且**先查舊有 telephony watermarking 文獻**再談增量。A6 的 Article 50 收窄為 deployment-context 觀察，**不當唯一技術貢獻**（EU 官方已有 audio marking 技術文件）。
- **三 RQ**：RQ1 各 watermark 家族在通道上的可靠 bit 容量與塌陷點；RQ2「索引不 payload」構造能否單機端到端存活；RQ3 對照 Article 50 兩階操作門檻判可讀/不可讀。
- **GPU**：~220 h（最省）。載體語音年份不影響物理量測，維持不換。**停止條件**：若只是重做 AudioMarkBench/RAW-Bench 就停。

---

## 四、下一步（依作者裁定：先更新方向、再依結果決定 pilot）

Codex 指定的**下一個最小驗證**（方向#1 的 pilot，決定是否正式定題）：
1. 一個可重現 detector + MSP/entropy + 一個 embedding score；
2. 在一個 dev dataset 設兩個 risk target（如 5%、10%）、**完全凍結**；
3. 跑一個 generator-disjoint、時間較新的 10–20% pilot subset（DFADD 適用）；
4. 只看：dev 選定閾值 → external observed risk/coverage/violation、AURC、per-generator bootstrap CI、base AUROC gate。

**成功**：至少一 detector 不接近隨機、ranking/threshold transfer 呈可重複差異、split 在 generator-family 層級無洩漏、結果非由語言/取樣率/duration 解釋。
**轉向**：找到相同 fixed-threshold+newer-holdout+risk-violation 前作且無 measurement delta；或全部 detector 接近隨機使 abstention 退化成「全拒絕」。

**pilot 前不寫 `DECISIONS.md`。** pilot 通過才由**作者**寫入正式定題。
