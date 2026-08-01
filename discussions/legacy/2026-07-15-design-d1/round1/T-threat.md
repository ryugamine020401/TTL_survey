# R1 設計立場：威脅模型設計者
日期：2026-07-15

範圍聲明：本文只設計 **RQ3 的評估用攻擊**（在 frozen 偵測器上、共用 RQ1/RQ2 快取的前向），不擴成一整套攻擊研究——攻擊成本地圖是方向#2 的事，這裡的攻擊只是「棄權安全閥在對抗壓力下是否還守得住」的壓力測試讀數。所有決策都是**只砍不加**：砍掉 black-box query、EOT-through-codec、per-sample 最佳化、MC-dropout/ensemble 對抗評估、全集攻擊。

---

## 主責：Q-RQ3 — confident-real / `max P(confident-real|fake)` 的操作化

Codex A3（`2026-07-15-claims-to-verify-a-d.md` §A3）：`max P(confident-real|fake)` 本質上是「targeted high-confidence misclassification while avoiding rejection」，reject-option adversarial 已有前作（CLAD、Stratified Adversarial Robustness with Rejection、Revisiting Adversarial Robustness with a Reject Option、Detecting Adversarial Examples Is Nearly As Hard）。因此**不能宣稱新攻擊概念**；增量只能來自「把標準攻擊當成 transfer protocol 內的壓力測試讀數」。以下五個子決策把它釘死成單一規格。

### D-RQ3.1【攻擊目標＝confident-real 區的操作定義】
**單一決策**：攻擊目標 = 把一個 fake 擾動到落入 **confident-real 接受區** = `{偵測器判 real}` ∩ `{棄權/信心分數 ≥ RQ1 在 dev 上固定的 accept 門檻 τ}`；即同時（a）越過 fake 決策邊界**且**（b）避開 abstain 區。報告量不是攻擊 SOTA，而是兩個讀數：(i) 固定擾動預算 ε 下到達 confident-real 的成功率（即 `max P(confident-real|fake)` 的經驗估計），(ii) **各棄權分數的對抗穩健度排序是否相對 RQ2 clean 排序翻轉**（呼應定稿 RQ3 的「排序在對抗欄下是否翻轉」）。
- **砍掉的選項**：把「confident-real」當成全新安全概念來賣（A3 已否證，是 targeted high-conf misclassification + reject option 的既有組合）。
- **一句理由**：目標區必須用 RQ1 的 dev-fixed τ 定義，才能讓 RQ3 是「同一協定的對抗欄」而非另開一篇攻擊論文（定稿 §三推薦#1 RQ3；A3）。
- **GPU-hour**：0（定義層，不新增計算）。
- **待 Codex 查證**：是——「dev-fixed 門檻 + unseen-generator transfer 下量 confident-real 到達率與排序翻轉」相對 CLAD / reject-option robustness 前作的增量，須查是否已有等同 measurement。

### D-RQ3.2【知識假設＝white-box，gradient PGD】
**單一決策**：採 **white-box、gradient-based PGD**（可微分 post-hoc 分數上直接做 targeted ascent 到 confident-real）。
- **砍掉的選項**：black-box query 攻擊（NES/SimBA）。
- **一句理由**：white-box 是 worst-case，給的是「攻擊者最低成本／能力上界」的可辯護框架；且算力上 white-box PGD-50 在 5k 樣本 × 3 模型 × 5 機制 = 6–13 GPU-h，而 black-box 10k-query × 5k 樣本 = 500–1,000 GPU-h（預算表 R8 紅線），black-box 直接降為 future work（`01-compute-budget.md` §4.4、§6-R8）。
- **GPU-hour**：見 D-RQ3.5 小計。
- **待 Codex 查證**：否（方法學選擇，非 novelty）。

### D-RQ3.3【品質/擾動預算＝單一 waveform-domain ε，2–3 點成本曲線，無 codec】
**單一決策**：waveform-domain L∞ PGD，單一感知錨定預算（以 SNR ≥ 一個預註冊值錨定 ε），在 **2–3 個 ε 點**畫「擾動預算–confident-real 到達率」曲線；擾動不穿過任何 codec。
- **砍掉的選項**：(a) EOT/BPDA 穿過 codec（×10 → 60–130 GPU-h，且 codec laundering 是方向#2 的 threat model，混入即違反範圍）；(b) feature-domain + waveform 多域攻擊；(c) per-sample 客製最佳化。
- **一句理由**：RQ3 只需在**乾淨通道**上探棄權閥，把 codec/laundering 留給方向#2，可避免 threat model 混淆並省 4–10×（A3 要求明確 quality budget；`01-compute-budget.md` §4.4 EOT-10 列 ×10、§4.5 laundering 屬 recipe-level 另案）。
- **GPU-hour**：ε 點數就是 D-RQ3.5 的乘數（×2–3）。
- **待 Codex 查證**：否。

### D-RQ3.4【被攻擊的分數集＝可微分 post-hoc 子集，frozen checkpoint】
**單一決策**：只攻擊**可微分的 post-hoc 分數**（MSP、energy、Mahalanobis-on-SSL），全部在 RQ1/RQ2 的**同一組 frozen checkpoint**上、重用 cached-forward 基建。
- **砍掉的選項**：對 MC-dropout / deep ensemble 做對抗評估。
- **一句理由**：MC-dropout/ensemble 的隨機性/多模型使 targeted 攻擊需 EOT-like 多次前向（成本爆炸），且對抗欄的重點是「排序翻轉」而非窮舉所有機制；砍掉不影響 RQ3 主張（`01-compute-budget.md` §4.4、法則 1；S4 共用 checkpoint）。
- **GPU-hour**：見小計。
- **待 Codex 查證**：否。

### D-RQ3.5【樣本範圍＝分層 fake 子集，非全集】
**單一決策**：攻擊對象 = 從 **generator-disjoint holdout** 分層抽出、且在 clean 條件下**本來被正確判 fake 或被正確 abstain** 的 fake 子集（n ≈ 2,000–5,000）；不在 611k 全集上攻擊。
- **砍掉的選項**：ASVspoof21 DF 全集 / 大子集攻擊。
- **一句理由**：對抗評估的每個乘數都會被資料量放大，分層抽樣是 CP 值最高一刀（`01-compute-budget.md` §5.2 法則 3、S2）。
- **GPU-hour**：**RQ3 小計 ≈ 15–30 GPU-h**——base（1 ε：PGD-50 × ~5k × 3 模型 × ~5 可微機制 = 6–13 h）× 2–3 個 ε 點；因重用 frozen checkpoint（S4）與 cached forward（S1），邊際成本只有攻擊迭代本身，落在預算表預留的 200 GPU-h 對抗欄內、餘裕極大（`01-compute-budget.md` §4.4、§8.1）。
- **待 Codex 查證**：否。

---

## 對其他 Q 的風險提醒（各一句，指名角色）

- **給 M（Q-SCORES）**：若最終保留 MC-dropout / deep ensemble，請明記它們**不進 RQ3 的對抗排序比較**（D-RQ3.4：不可微/隨機使 targeted 攻擊需 EOT，成本爆炸）——RQ3 的「排序翻轉」只在可微 post-hoc 子集（MSP/energy/Mahalanobis）上成立，須在 Q-SCORES 標清楚以免 RQ3 被要求覆蓋全機制。
- **給 M（Q-RQ2）**：RQ3 的「排序翻轉」讀數只有在 RQ2 已控制共同 backbone / representation quality 後才有意義（否則翻轉可能只是容量差，非對抗脆弱性差）——請確保 RQ2 的公平比較設定同時服務 RQ3。
- **給 E（Q-METRIC）**：confident-real 目標區直接吃 RQ1 的 dev-fixed accept 門檻 τ（D-RQ3.1），請在 Q-METRIC 把 τ 的定義與凍結時點釘死，RQ3 才有共用的目標邊界。
- **給 E（Q-SPLIT）**：RQ3 攻擊樣本必須取自 generator-disjoint holdout、且 **ε 預算須預註冊、不得以 test 結果回頭調 ε** 讓攻擊好看（等同 holdout tuning，違反定稿 §10 停止條件）——請把「對抗預算不調參」寫進 leakage 防線。
- **給 P（Q-CONTRIB）**：RQ3 **不得**寫成新攻擊貢獻（A3 已否證、且屬方向#2 領地）；primary claim 應鎖在門檻/棄權的 transfer 與 risk violation，RQ3 只是「對抗欄」的壓力測試讀數，請在貢獻結構把 RQ3 定位為診斷而非方法。

---

## 回傳摘要（單一決策一行版 + GPU-hour 小計）

- **D-RQ3.1**：confident-real = `{判 real}` ∩ `{分數 ≥ RQ1 dev-fixed τ}`；報 confident-real 到達率 + 對抗排序是否翻轉；不當新概念賣。（待 Codex 查證：增量 vs CLAD/reject-option 前作）
- **D-RQ3.2**：white-box gradient PGD；砍 black-box query（省 500–1,000h → 未做）。
- **D-RQ3.3**：waveform L∞ PGD、SNR 錨定單一 ε、2–3 點成本曲線、不穿 codec（EOT/codec 屬方向#2）。
- **D-RQ3.4**：只攻可微 post-hoc 子集（MSP/energy/Mahalanobis），frozen checkpoint 共用；MC-dropout/ensemble 不進對抗欄。
- **D-RQ3.5**：分層 fake 子集 n≈2,000–5,000，不攻全集。
- **GPU-hour 小計 ≈ 15–30 GPU-h**（重用 frozen checkpoint + cached forward，落在預留 200h 對抗欄內，餘裕大；不影響 430–520h 總預算）。
