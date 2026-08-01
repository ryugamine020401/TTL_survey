---
handoff_id: 2026-07-18-1009-final-topic-assessment
from: codex
to: claude
created_at: 2026-07-18T10:09:00+08:00
request_type: Decide
scope: 對 thesis plan v2 作最終 GO/CONDITIONAL-GO 認定，整合 novelty、H1a/H1b/H2、policy estimand、strong baselines、checkpoint/holdout lineage 與定題條件
out_of_scope: 不覆寫 plan v2、不替作者改 DECISIONS.md、不下載資料、不跑 pilot、不訓練
in_reply_to: —
supersedes: —
delta_of: 2026-07-18-0715-plan-v1-h1b-replication-extension-review
source_artifacts: discussions/2026-07-18-thesis-plan-v2.md; research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md
expected_output: Claude 獨立確認或反駁本判定；統整成 plan v3／consensus delta，明確處理 XLS-R×ASVspoof5 overlap、H1a/H1b selector 分層、alpha policy fitting、matching 與 preregistered rank-changing baselines
authority_boundary: 僅可提出統整與 redline；題目由作者裁定，DECISIONS.md 由作者專屬；未授權下載、pilot 或訓練
---

# 最終題目認定送交 Claude 統整

Codex 對 plan v2 的最終判定是：

> **題目方向 GO；實驗規格 CONDITIONAL GO。**

題目與核心 RQ 可固定為 `Selective-Policy Transfer of Lightweight Audio Deepfake Detectors under Unseen Generators`，但 confirmatory design 尚有一個 hard blocker：ASVspoof 5 官方 evaluation plan 禁止 MLS/LibriLight-derived pretrained models，官方 XLS-R checkpoint 含 MLS，故 plan v2 的 `XLS-R teacher × ASVspoof 5 eval holdout` 存在 upstream overlap，不能直接作 lineage-clean confirmatory evidence。

另有四項定題前必修：

1. H1a base selector `u0` 與 H1b rank-changing repair `u1` 必須分層；
2. `alpha` 必須由 source joint policy fitting 真正約束；
3. H2 移除 matched eAURC，eAURC 僅作 outcome/diagnostic；
4. rank-changing baseline shortlist、source-only selection rule 與 inference cost 必須預先登記。

請讀完整 artifact：

- `research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md`

並與：

- `discussions/2026-07-18-thesis-plan-v2.md`

統整。請保留支持與反證，尤其是 TMLR 2024 generalized selective classification 的強 generic baselines，以及 Cattelan & Silva 2023「matched accuracy 後 selective shift degradation 可能消失」的 null evidence。不要覆寫 plan v2；以新的 plan v3／consensus artifact 與 Claude-outbox handoff 回覆。

