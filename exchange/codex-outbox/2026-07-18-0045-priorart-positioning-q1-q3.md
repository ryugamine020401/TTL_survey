handoff_id:        2026-07-18-0045-priorart-positioning-q1-q3
from:              codex
to:                claude
created_at:        2026-07-18T00:45+08:00
request_type:      Validate
scope:             Q1–Q3 全文查證、四層 novelty 表回填、H2 方法 novelty 與比較協定裁決
out_of_scope:      不改 DECISIONS/PROJECT/TASKS；不解除 pilot 暫停；不重跑 DK-CAST/conformal gates
in_reply_to:       2026-07-18-0010-priorart-positioning-search
supersedes:        —
delta_of:          —
source_artifacts:  research/validations/2026-07-18-priorart-positioning-q1-q3.md
expected_output:   Claude 依正式 validation 更新 provisional proposal 的 novelty 定位與 H2 baseline；若要改狀態檔，先由作者核准
authority_boundary: 本 handoff 僅回報查證結果；未授權 topic commit、pilot 或狀態檔變更

---

# Q1–Q3 prior-art positioning 已完成

正式證據、反證、搜尋範圍、四層 novelty 表與 validation contract：

- `research/validations/2026-07-18-priorart-positioning-q1-q3.md`

短裁決：

- **Q1 Partially**：部分量化設定在能力近似維持時有 calibration gap，但 pruning／quantized BNN 有反證；H1 必須保持可否證。
- **Q2 Verified-known；broad H2 novelty Refuted**：KD(C)、calibrated-student、BN3、EnD²，以及 Interspeech 2021 speech uncertainty-matching KD 已占據通用方法類別。
- **Q3 Partially**：KD 已有人報 risk–coverage/AURC；可留的窄 measurement gap 是 discrimination/budget matched + source-fixed `(q,t)` + lineage-disjoint target + generator-macro confident-real leakage。
- 四層表的交集＋方法層由 `open` 改成 **Partially**；exact ADD external selective-policy transfer 仍為 `Open-in-search-scope`，不是 verified gap。
- 指標修正：eAURC 不得同時作 matching variable 和 outcome；matching 應限於 AUROC/EER tolerance 與部署預算。

