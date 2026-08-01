# Claude 確認：外部審核報告（thesis_selective_policy_review_for_codex_claude）

日期：2026-07-18
對象：`discussions/thesis_selective_policy_review_for_codex_claude.md`
性質：獨立確認（非背書）。作者將同時請 Codex 確認，然後定題。

## 總判斷
**這份審核正確、可採納，且實質改善計畫。** 有三個真正重要的修正我強力背書；有兩處我微調/反駁；參考文獻表有幾筆需 Codex 查證，不可當已驗證。採納後可升為 plan v3（最終）。

## 一、強力背書（採納，這是本審核最大價值）

1. **主 estimand 改為 teacher-relative double-difference `Δ_light`**（§3.4、§14）——**最重要的修正**。
   - 定義：`G_m = L_CR^target − L_CR^source`；`Δ_light = G_student − G_teacher`。
   - 為何關鍵：我原本的 H1a（`L_CR^student,target > L_CR^teacher,target`）**混淆了兩件事**——「輕量化造成的退化」與「teacher 本身在 target 就會失效」。double-difference 把 teacher 自己的 domain-shift failure 減掉，**隔離出輕量化『額外』造成的損失**。這直接回應論文的真正問題（不是「輕量 ADD 在未見 generator 會變差」——那是已知；是「輕量化本身多帶來多少 policy-transfer damage」）。**採納為 primary comparative estimand。**

2. **`L_CR` 可被『全部棄權』作弊 → 必須同時約束 coverage**（§四高嚴重度）——我漏了這個。只最小化 confident-real leakage 的退化解是「什麼都棄權」。**採納**：primary endpoint 必須與 overall/fake/bona-fide coverage 與人工複核比例聯合報告與約束。

3. **`α` 要進 policy 建構，不只當事後比較**（§3.2）——正確。若 `q` 只由 coverage 決定，`α` 就沒真的用到。**採納** UCB-constrained 定義：`(t_m,q_m)=argmax Coverage s.t. UCB(L_CR)≤α ∧ UCB(FPR)≤β`（用信賴上界非點估計），並含 no-feasible-policy fallback。

另外一致同意、直接採納的：資料五切分（model-train / **selector-train 用 out-of-fold** / policy-dev / exploratory / confirmatory）（§7.1）；bootstrap 要重跑完整 policy fitting（§10.2）；不宣稱 arbitrary unseen generator 的 risk guarantee、改用 observed/external violation 措辭（§3.3）；`lineage-disjoint` 弱化為 `documented lineage-disjoint under available metadata`（§十一）。

## 二、微調 / 反駁

1. **In-the-Wild 不該當正式 kill criterion（§四中高）——審核對，我的 plan v2 Stage 0.1 需改。** 我原寫「In-the-Wild 無退化→提早重估」。但 In-the-Wild 混雜 codec/speaker/language shift，null 可能有多種原因。**改**：In-the-Wild 僅 smoke test（確認 pipeline 會動、看有無粗訊號），**不作正式 kill**；正式 H1a 判定只在 confirmatory（ASVspoof5 C00）。

2. **H2 pinning——與我先前「不要 pin 死 H2」的立場需要調和。** 審核 §八 pin 了一個 method family（`L_CE+λ_KD·L_KD+λ_rank·L_correctness-rank+λ_cons·L_codec-consistency`）。我先前擔心 pin 死會變「已知成分組合」。**調和結論（雙方都對一半）**：pin **method family + 允許的 hyperparameter 範圍**（讓它可審查、可重現，避免「只有問題沒方案」的批評），但——(a) component **weighting/ablation 優先序由 H1a 失效診斷決定**；(b) **必過 method closest-work gate**；(c) ADD-specific 理由要明確（審核提供了一個好 hook：`L_correctness-rank` **特別處理 confident-real false negatives**——這是 ADD 不對稱危害特有的，不是通用 selective distillation）。這樣既可審查又不淪為換名。

3. **「distance/energy 不必然 rank-changing」（§四中高）——審核對，補驗證。** 我之前假設 feature-distance selector 會改排序，但名稱不同不代表排序真的變。**採納**：H1b 的 rank-changing repair 必須用 **Kendall τ / Spearman ρ / accepted-set disagreement** 實際驗證它真的改了 accepted set；並加 **cross-fitted correctness predictor** baseline（Mahalanobis 可能只偵測 channel novelty 而非分類錯誤）。

## 三、需 Codex 查證，不可當已驗證（§12 參考表）

審核自己在 §12 標明「連結與 metadata 應再由 Codex/Claude 獨立查證」。我特別點出幾筆疑點：
- **Kwok**：此表寫「Robust ADD using Ensemble Confidence Calibration, **ICASSP 2025**」；但我們先前 Codex gate 的 Kwok 是 **Interspeech 2025 synthesizer pooling**——**venue/題名可能不一致，須查證是否同一篇或兩篇。**
- **Zhou & Wang (2606.21584)**：此表給了完整題名「When EER Hides Deployment Failure…」；先前只確認 arXiv id 與「threshold transfer」主題，**題名需核對**。
- **Xu, ICPR 2020**：審核自己標「待查」——需補完整作者/題名/DOI 或移除。
- FADEL、DK-CAST、Guo、Ovadia、KD(C)、Kim 等與先前 Codex 查證一致，風險低。

## 四、我可現在回答的數學問題（§15-B；不需文獻查證）

- **B1（`q,t,α,β` 最佳化可行？）**：可行——2D 門檻上的受約束最大化；UCB 約束使其保守但仍可解，**前提是可行域非空**（故 Gate 1 的 no-feasible-policy fallback 必要，例如放寬 β 或宣告該預算下無合格 policy）。
- **B2（TS/Platt no-op 充要條件？）**：充分＝{單一 scalar score}∧{g 對 s 嚴格單調}∧{門檻校準後依同一 rank-based 約束重選}∧{selection score 為 s 之單調函數}∧{無 ties}。任一破壞即非 no-op（已數值驗證：TS/Platt+refit diffs=0；固定 p≥0.5 不重選 diffs=4252）。
- **B3（`u(x)` 結合 distance+logit 必然 rank-changing？）**：**否，不必然**。若 distance 與 |s| 高度相關，accepted-set 可能幾乎不變。**必須實測**（Kendall τ / accepted-set disagreement）——正是 §二.3 的採納點。
- **B4（`Δ_light` 是最佳 comparative estimand？）**：是主 comparative estimand 的正確選擇（移除 teacher-failure 混淆）；但仍應**並列**報告 per-family `G_student`、`G_teacher` 分量以求透明，且註明其假設（同一 source baseline、同一 target shift）。
- **B5（source/target family 不對稱時 transfer gap？）**：只要 teacher 與 student 共用**同一 source baseline 與同一 target**，double-difference 仍隔離「兩模型對同一 shift 的差異反應」，asymmetry 不破壞其效度；報告時 source 分量以 held-out source（非 policy-dev）估計以免樂觀偏誤。

§15-A（novelty）、§15-D（dataset lineage）屬 Codex 查證職責（部分已在 `2026-07-18-1030` lineage manifest handoff）；§15-C（統計，~7 families 能做什麼推論）與 §15-E（method closest-work）我可在 H1a 診斷後接手。

## 五、結論與下一步
採納 §一 三項 + §二 三項調整 + §三 待查 + §四 數學確認後，計畫可從「輕量 ADD 外部可靠性量測」提升為「**輕量化造成的 external selective-policy degradation 分析 + 一個具可驗證增量的策略保留方法**」，且題目/estimand/policy/baseline 都收斂到可審查、可重現。

**建議最終題目**（採審核版，最精確）：
> **Transfer and Preservation of Source-Frozen Selective Policies in Lightweight Audio Deepfake Detectors under Unseen Generators**
> 未知生成器下輕量音訊深偽偵測器之凍結選擇策略轉移與保留

待 Codex 也確認後，我把以上全部整合成 **plan v3（最終定題版）**，不覆寫 v1/v2。
