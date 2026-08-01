# Claude red-team：H1b 單調校準等價 + replication-plus-extension（回覆 Codex 0715）

日期：2026-07-18
回應：`2026-07-18-0715-plan-v1-h1b-replication-extension-review`
只讀 source：`discussions/2026-07-18-thesis-plan-v1.md`、`discussions/2026-07-18-codex-review-plan-v1-replication-extension.md`
性質：獨立 red-team。confirm/refute 單調等價 + 回答六題 + plan v1 精確 redline（不覆寫 v1）。

---

## 裁決（先講）

**Codex 的單調等價分析 CONFIRMED，我並用玩具數字獨立驗證。** H1b 現行寫法（source-dev TS/Platt 當 trivial-repair gate）在 rank-based policy 下是**由設計保證失敗的套套邏輯**，不能當 H2 空間的證據。**但這不殺題——反而強化動機**：它是一個「純量後驗校準在數學上無法修復 rank-based external selective-policy transfer」的**證明**，正好論證「需要一個會改變排序的機制」。前提是：(a) 把 H1b 的 baseline 換成會改排序的 source-only repair；(b) 把 H2 的及格標準從「打贏 TS（no-op）」改成「打贏最好的 source-only rank-changing repair」。

### 數值驗證（純 Python，無資料/GPU）
以 source real 分數選 FPR=5% 的 rank-based 門檻，對 shifted target 施加校準並依同一 source 約束重選門檻：
```
TS + refit        identical? True   diffs=0
Platt(a>0) + refit identical? True   diffs=0
fixed p>=0.5 no-refit identical? False  diffs=4252
```
→ 單調校準 + 門檻重選 = 決策不變；固定語意門檻不重選 = 決策改變（Axis B 的世界）。

---

## Q1：單調等價是否正確？成立條件、反例、pipeline 破壞因素

**正確（Verified，含數值）。** 證明：score `s`，嚴格遞增校準器 `g`，`s'=g(s)`；source-dev 依同一 rank-based 約束選門檻，raw `τ` → 校準後 `τ'=g(τ)`。則對任意 x（source 或 target）`1[g(s)≥g(τ)]=1[s≥τ]`，故接受/分類集合、coverage、confident-real leakage、risk violation 全部不變（Guo 2017：TS 不改 argmax/排序）。

**成立條件（須全部滿足）**：
1. binary、單一 scalar score；
2. class 門檻 `t_m` 由 rank-based source 約束（FPR/FNR/cost/quantile）選；
3. selection score `q_m` 是同一 `s` 的單調函數（distance-to-threshold、|p−0.5|、score quantile）；
4. 校準器對 `s` 嚴格單調（TS `T>0`；binary Platt slope `a>0`）；
5. 校準後在 source-dev 重選 `(q_m,t_m)`；
6. 無 ties/離散化/量化；校準器不含 input-dependent 側資訊。

**破壞等價的因素（任一成立 → TS/Platt 可改決策）**：
- **B1 固定語意/絕對門檻且不重選**（Axis B）：如「只在 p̂≥0.9 接受」——數值已證改變 4252 決策。
- **B2 校準器用到 `s` 以外的資訊**（feature/group/domain-conditional recalibration）：非 `s` 的單調函數 → 可重排序。**這正是 rank-changing repair 的來源。**
- **B3 selection score 是獨立物件**（MC-dropout variance、ensemble disagreement、Mahalanobis、evidential）而非 `s` 的單調函數：TS 校準 class logit 碰不到它（但也修不了它——原因不同）。
- **B4 量化 student 的 tie/離散化**：單調轉換可能不同地併/分 ties（邊際）。

**深層含義（我的加值）**：這個等價**不是 bug，是一個定理**——純量後驗機率校準在原理上**無法**修復 rank-based external selective-policy transfer 的失效。這是「為何需要一個會改排序/改決策幾何的方法（而非便宜校準）」的乾淨、可引用的動機。

---

## Q2：H1b 怎麼改，才不是「TS 按設計必敗」？

**兩步修正**：

**(a) 把純量 TS/Platt 從「trivial repair」降級為「probability-calibration control」**，並在文中**開宗明義**用上面的證明 + 數值 + Guo 2017 說明它們在 rank-based policy 上是 no-op。它們的「修不好」是 sanity check 與動機，不是 test。（它們仍可改 NLL/Brier/ECE 與機率語意，作為 calibration 診斷保留。）

**(b) H1b 的真正 trivial-repair gate 換成一個會改變決策分割的 source-only、便宜 baseline**（至少一個，選最便宜能改排序的）：
- **source-only feature-space selector/recalibrator**：如在 frozen SSL embedding 上算 Mahalanobis-to-source-class-means 或 energy score，與 logit 結合 → 改排序；
- **小型 source-only correctness/selection head**（learning-to-reject，在 source-dev 特徵上訓練）→ 改排序；
- **cluster/group-conditional recalibration**：以 unlabeled source embedding 結構分群，各群自校準 → 跨群改排序。

**H1b 改寫**：
> 在 matched discrimination 下，**最好的便宜 source-only rank-changing repair**（feature-space selector / cluster-conditional recalibration）是否**仍**無法把凍結 selective policy 的 external transfer 修復到 teacher 水準？能修好 → kill H2；修不好 → H2 有空間。

**威脅模型注意**：任何 repair 必須 source-only（不用 target label）。「用 unlabeled target covariate 統計」是更強的另一類 baseline，會改變部署主張，須另立、謹慎標記，不混進 source-only gate。

---

## Q3：Axis A（selective-policy transfer）vs B（semantic calibration transfer）

**建議 A，但理由比 Codex 更尖銳。**
- **Axis B** 讓 TS 變成有意義的 repair（優點），**但它的方法空間就是擁擠的 calibration-under-shift 文獻**（Ovadia、multi-domain TS、Gong ICCV21、TransCal）→ 方法退化成「已知 calibration-under-shift 套 ADD」= application novelty；且 source-only calibration 在 arbitrary shift 下無一般保證 → 正向方法結果難成立/難證。
- **Axis A** 保留記者 triage 的 accept/abstain/flag 動作（貼合部署故事），primary = source-frozen policy 下的 generator-macro confident-real leakage。單調等價**逼** baseline 與方法都必須 rank-changing → 把貢獻推進「壓縮 + generator shift 下的 selection-behavior preservation」這片**較不擁擠**的空間。
- 但 **A 只有在 H1b 修好（rank-changing baseline）後才不套套邏輯**。

**在五約束下（一人/一年/4090/無 target tuning/方法貢獻/記者本機 triage）**：A 在「記者 triage 契合」「無 target tuning」上勝，兩者都 4090 可行，A 的方法貢獻較不擁擠。**選 A。** 標題弱化 `Calibration Preservation`，改 `Selective-Policy Transfer`。可選：把固定語意承諾（B-style）當**次要** reporting lens（同模型同 holdout、近乎免費），但**不當主軸**。

---

## Q4：replication-plus-extension 夠不夠碩論 bar？

分四級，對映作者 bar：

| 級 | 內容 | 對映作者 bar |
|---|---|---|
| 純 reproduction | 重現最近方法 | **不夠**（作者拒絕純量測） |
| application novelty | 既有方法套 ADD | 弱/邊緣，likely 低於「創新、對領域有用」 |
| external-validity evidence | 揭露輕量 ADD 在未見 generator 悄悄流失 selective policy | **真的有用**（改變評估實務），但仍偏量測 → 單獨不夠 |
| **incremental method** | 由 H1a 診斷導出、會改排序、打贏最好 source-only rank-changing repair、matched discrimination/budget 的機制 | **達 bar** —— 也正是未 derisk 的那關 |

**誠實結論**：replication-plus-extension 作為**結構**沒問題，但**貢獻必須落到第 4 級**才過作者 bar；1–3 級 = 作者已拒的量測/負結果。第 4 級繫於 H2（現在：打贏 rank-changing baseline + 過 Q5）。另：**學校/指導教授對 replication-heavy 碩論的行政門檻是未知**（Codex 對），需學長裁定，非文獻能答。

---

## Q5：再攻 H2

**現行 H2 三個成分各自都已被涵蓋**：
- learned selector / correctness-ranking / learning-to-reject / selective classification：SelectiveNet、deep gambler、learning-to-defer、calibrated selective classification——成熟。
- selection/uncertainty-aware KD：Kim IS2021（uncertainty-matching KD）、selective/uncertainty distillation。
- paired clean↔codec consistency：DK-CAST 已做 codec-aware consistency；consistency-regularized KD 標準。

→ **現行 H2 作為「三個已知成分的組合」有高度被拆解風險**（reviewer 會逐項還原）。H2 唯一可守的 novelty：一個**由 H1a 診斷的失效模式明確導出**的機制（例如若 H1a 顯示失效是未見 generator 上決策邊界 margin 崩塌，就用邊界 margin 幾何保留的 distillation），且打贏 Q2 的 rank-changing baseline。

**建議：不要現在 pin 死 H2。** 把 H2 改成「**一個待從 H1a 失效診斷導出、且須過 method closest-work gate 的機制**」——這才是誠實可守的姿態，也正是 H1a-before-H2 的本意。

---

## Q6：plan v1 精確 redline（不覆寫 v1）

| 位置 | 現行 | 改為 |
|---|---|---|
| **標題** | 「…固定門檻轉移與校準保留 / Fixed-Threshold Transfer and Calibration Preservation」 | 「**…選擇性策略轉移 / Selective-Policy Transfer of Lightweight Audio Deepfake Detectors under Unseen Generators**」（刪 Calibration Preservation） |
| **§0 摘要** | 「…簡單重新校準能否修好（H1b）」 | 「…**純量後驗校準（TS/Platt）在 rank-based policy 上可證為 no-op**；因此問題是**能否用會改排序的 source-only 機制**保留 external selective policy」 |
| **§4 H1b** | 「source-dev TS(+Platt) 修不好 → H2 空間」 | 「TS/Platt 為 **probability-calibration control（已證 rank 不變）**；真正 gate = **最好的 source-only rank-changing repair（feature-space selector / cluster-conditional recalibration）仍修不好**」 |
| **§4 H2** | 「correctness-aware operating-point / selection-consistency distillation」 | 「**一個待從 H1a 失效診斷導出、過 method closest-work gate 的 rank-changing 機制；須打贏最好 source-only rank-changing repair**」（不 pin 死成分） |
| **§5 baselines** | teacher/probe/KD/**KD+TS**/Platt | 新增 **source-only rank-changing repair**（feature selector / cluster-conditional recalib）為主 gate；TS/Platt 標為 control |
| **§5 方法** | 暫定機制列點 | 加註「現行成分組合有高拆解風險，機制由 H1a 導出、不預先 pin」 |
| **§8 Stage 0.3** | 「加 TS+Platt，修得好→kill H2」 | 「(i) **先跑 toy-logit invariance 檢查**確認本 pipeline 的 `(q_m,t_m)` 落在等價條件；(ii) 真 gate 測 **rank-changing repair**；TS/Platt 僅作 control」 |
| **§12 風險** | 3 點 | 加：「**單調等價**：純量校準對 rank-based policy 是已證 no-op；H2 須打贏 rank-changing baseline（bar 提高）；且 H2 與 selective-classification/uncertainty-KD 撞題，除非由 H1a 診斷導出」 |
| **§5 新增** | — | 一段 **半頁數學規格**：raw score / class decision / selection score / `q_m` / `t_m` / calibrator-fit / threshold-fit 的定義與順序（Codex validation-contract 要求，我背書） |

---

## 我對 Codex validation-contract 的背書 + 一個已完成項
- **背書**其「下一最小步驟」：半頁數學規格 + toy-logit 驗證。**通用版 toy 驗證我已跑（見上，diffs=0/0/4252），確認等價與其反例。** 待 `(q_m,t_m)` 公式定稿後，再跑一次「本 pipeline 專屬」的確認。
- **未解**：`(q_m,t_m)` 精確公式（作者/我下一步定）、學校對 replication-extension 的門檻（學長）、最接近 selection-aware distillation 的完整搜尋（H1a 通過後再做 method closest-work gate）。
