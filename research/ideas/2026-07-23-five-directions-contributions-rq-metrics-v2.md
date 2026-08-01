# 五個方向速覽：題目、貢獻、RQ、指標（查證後精簡版）

日期：2026-07-23。性質：proposal 設計草案，證據狀態已對齊 `research/validations/2026-07-23-five-directions-contributions-rq-metrics-audit.md`。
通則：所有 novelty 主張一律是「2026-07-23 記錄的搜尋範圍內未找到直接同題先作」，不是「第一個」。

---

## D1-B｜來電 sequential 版（查證：有希望、未驗證；須先過門一 kill test）

**題目**：《來電串流下輕量音訊深偽偵測器之凍結序列選擇策略轉移》
*Source-Frozen Sequential Selective-Policy Transfer of Lightweight Audio Deepfake Detectors for On-Device Call Screening under Unseen Generators*

**貢獻**：一個 call-level sequential policy（spoof 唯一吸收態、clean 監聽到掛斷、棄權綁升級），分開控制兩類整通風險，並稽核它在未見生成器上的轉移。部署想定錨在 OS 特權 on-device（Pixel 先例），為部署位置先例、非任務新穎性。

**RQ**：
1. 凍結 policy 的雙承諾（`R_fake^call ≤ α`、`R_bona^call ≤ β`）在未見生成器上守不守得住？輕量化額外退化多少？
2. 資料相依停止比最佳固定截斷 τ 好在哪（Pareto：latency/coverage）？τ*(α,β) 落在第幾秒？
3. （條件性）失效時 future-aware prefix 蒸餾能否修回？

**指標**：`R_fake^call`＝P(fake 整通未被抓且未升級)；`R_bona^call`＝P(bona 整通至少誤觸一次)——repeated looks 放大的是後者，inflation 掛 bona 側；`Δ_light^seq`＝(student 的 target−source 差)−(teacher 同差)。配平 AUROC/EER＋部署預算。

**怎麼贏**："Hi!"（ICASSP 2026）只測固定截斷準確率、無棄權無風險承諾——本文量「第幾秒有資格承諾」，不比準確率。LTT 保證只在 source 內成立，shift 下的轉移是被量測的結果，誠實分層。

**停損**：門一 kill test（state machine＋synthetic 驗證＋LTT 假設界線）不過 → 退 D1-A。

---

## D1-A｜完整語音版 proposal-final（查證：最穩）

**題目**：《未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留》
*Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators*

**貢獻**：source-frozen、lineage-audited、family-macro 的 selective-policy 外部轉移協定＋失效四源診斷（discrimination/ranking/operating point/calibration）＋條件性 policy-preserving 蒸餾。

**RQ**：
1. matched 辨識力與預算下，`Δ_light > ε`？（輕量化是否額外破壞凍結策略）
2. source-only 便宜 rank-changing 修法能否修回？（TS/Platt 在重選 threshold 條件下是 no-op，僅作 control）
3. （條件性）診斷導出的蒸餾機制能否勝過最強修法？

**指標**：`L_CR,g`＝P(自動判真|fake, family g) 的 family-macro；`Δ_light`＝(L_student^tgt−L_student^src)−(L_teacher^tgt−L_teacher^src)。同報 coverage、bona-fide 誤拒、threshold drift。

**怎麼贏**：頭號數字「ΔEER≈0 但 Δ_light>0」——輕量化前作（DK-CAST/FTDKD）未量 policy transfer；Zhou & Wang（2026 preprint）已做 threshold transfer 但無棄權、無壓縮 delta。

**停損**：退化可由 accuracy/ranking drop 完整解釋（Cattelan & Silva 路線）→ 撤機制主張，留負結果。

---

## D3｜攻擊成本前沿（查證：大修後版本）

**題目**：《被動語音深偽偵測之適應性洗刷攻擊成功成本前沿評估》
*An Attack-Success Cost-Frontier Assessment of Adaptive Laundering against Passive Audio Deepfake Detection*

**貢獻**：預先固定 action space 與攻擊者能力，輸出**多維成本**（金錢/計算/步數分開或按 persona 加權）的 attack-success Pareto frontier＋偵測器排序穩健性。已撤回：物理可逆性下界、neural codec 必殺論（laundering 先作已存在：IH&MMSec 2024、ReplayDF 2025）。

**RQ**：
1. 使 TPR@FPR≤1% 跌破門檻的最便宜配方之成本前沿？（greedy 給實證上界 c*≤c）
2. 哪些動作效果可被 channel-aware DA 實測追回、哪些不行？（實證標註，非定理）
3. 偵測器排序隨 persona/配方翻不翻轉？

**指標**：TPR@FPR≤1%（非 selective recall）、多維成本向量、DA 恢復率。

**怎麼贏**：前作量「劣化多大」，本文量「達成劣化最便宜付多少、付哪種幣」。

**停損**：成本排序對權重/seed 不穩 → 改報 robustness matrix＋敏感度分析。

---

## D4｜zh-TW 詐騙情境協定（查證：縮限後版本）

**題目**：《詐騙情境條件下語音深偽偵測的評估效度審計：一個繁體中文評測協定》
*An Evaluation-Validity Audit of Audio Deepfake Detection under Scam-Scenario Conditions: A Traditional Chinese Evaluation Protocol*

**貢獻**：zh-TW × 詐騙語意 × 時長 × 情緒 × 通道的 **crossed 因子設計＋交互項估計**（mixed-effects）。已撤回：「所有前作單軸」（"Hi!"、EmoFake、TeleAntiFraud、CFSDD 各佔軸）、因果品質解耦（UTMOS/ECAPA 只算 proxy 調整）。無法發布音訊就叫 protocol，不叫 corpus。

**RQ**：
1. 標準朗讀→詐騙情境，recall 落差總量？
2. 四軸主效應與預先選定交互項的效應量？
3. proxy 調整後殘餘關聯剩多少？

**指標**：TPR@FPR≤1% 落差、mixed-effects 效應量、proxy 調整後殘餘。

**怎麼贏**：前作各佔單軸但無受控交互分解；zh-TW＋話術語意的精確交集在記錄範圍內未找到先作。

**停損**：zh-TW lineage 不成立或因子無法 crossed → 降為小型 diagnostic study。

---

## D5｜watermark payload 前沿（查證：核心 novelty 被反證，大幅縮限）

**題目**：《通訊通道下音訊浮水印之可用承載量前沿估計》
*Operational Reliable-Payload Frontier Estimation for Audio Watermarks over Communication Channels*

**貢獻**：固定約束（品質、false-accept、block-error）下掃 payload×ECC 的**可用承載量前沿**＋detection/provenance/authentication 三任務分離。已撤回：可控植入首創（AudioMarkBench 已做）、「前作只報存活率」（RAW-Bench 已量 capacity）、Article 50 零先作與政策反證（EC 已出官方技術報告與 guidelines）。

**RQ**：
1. 各 watermark family 的約束下 payload frontier 與塌陷點？
2. ECC 能否把塌陷點外推（相對 RAW-Bench 固定 payload 多答了什麼）？
3. 三任務的可行性邊界各在哪？

**指標**：約束下可靠 bits、塌陷點位置、ECC 後 k。

**怎麼贏**：RAW-Bench 報「配定 payload 的 accuracy」，本文答「約束下最多能承載多少」——殘餘 novelty 全場最薄。

**停損**：相對 RAW-Bench 只是加 codecs → 不作主題，降 backup。

---

## 一頁對照

| | D1-B | D1-A | D3 | D4 | D5 |
|---|---|---|---|---|---|
| 查證判定 | 有希望未驗證 | **最穩** | 大修後可守 | 縮限後可守 | 殘餘最薄 |
| 主指標 | R_fake/R_bona^call、τ* | Δ_light、L_CR macro | 成本前沿、TPR@FPR | 落差＋交互效應量 | 約束下 bits |
| 最近先作 | "Hi!"、RTCFake | Zhou&Wang、DK-CAST | IH&MMSec24、ReplayDF | EmoFake、CFSDD 等 | AudioMarkBench、RAW-Bench |
| 勝負維度 | 何時有資格承諾 | 凍結策略沉默失效 | 最便宜付多少 | 受控交互分解 | 約束下前沿 |
| 停損 | kill test 不過→D1-A | accuracy 可解釋→負結果 | 排序不穩→matrix | lineage 不成立→diagnostic | 只加 codecs→backup |

**對決定書的修正**：D3「novelty 最耐久」評語隨物理下界撤回失效；D5 備援位置應重評；D1-A「最穩」強化；D1-B 維持「先過門一再談」。
