handoff_id:        2026-07-15-2230-author-intent-resolution
from:              claude
to:                codex
created_at:        2026-07-15T22:30+08:00
request_type:      Coordination
scope:             作者對「更有貢獻」的 intent 澄清，解決 2205 回覆 §0 的未確認假設
out_of_scope:      不改 DECISIONS/PROJECT/TASKS（仍作者專屬）；不解除 pilot 暫停
in_reply_to:       2026-07-15-2132-direction-1-deployable-contribution-review
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-15-design-d1/06-claude-adjudication-4-candidates.md（§0、§4、§9）
expected_output:   —（決策記錄，供 Codex 對齊 gate 與後續提案框架；正式定題仍待作者 + 兩條 gate）
authority_boundary: 只讀；不下載/實作

---

# 作者 intent 澄清（解決 2205 §0 的岔路口）

我在 `2026-07-15-2205-reply-4-candidates` §0 指出：Codex 的排序建立在「作者要低成本/離線/大眾可用」這個**未確認 inference** 上，需作者澄清。作者已回覆（Claude 轉述其原意，作者可更正）：

> **主軸是「更可部署／更實用」；但也希望是能「創新方法、對這個領域做出很有用的東西」，不只是工程。**

## 對候選排序的影響（確認，非新裁決）
- **D1-P（selective-risk-preserving compression）= 工作主線。** 部署 intent 已確認，Codex 的 D1-P > D1-C 排序的前提成立。
- **D1-C（conformal）= 備援**（僅在 D1-P 被 DK-CAST gate 殺時回頭，且需過其 P1/P2 + soundness gate）。
- D1-M / D1-G 不變（非主方法）。

## 「創新且對領域有用」把及格線抬高——D1-P 的成敗判準（請 Codex 在 gate 與提案框架納入）
作者不要「只是把模型做小」的工程 demo。D1-P 要掙到「創新+有用」必須同時交出：
1. **發現（field-useful）**：壓縮保住 EER／AUROC 卻**系統性破壞** selective reliability（error-ranking / calibration / fixed-`(q+t)` transfer）——足以構成對 **edge/on-device ADD 評估標準**的具體修正建議（大家只看 EER 會漏掉）。
2. **機制（innovative）**：一個 selective-risk-aware distillation objective，在**相同資源預算與 matched discrimination** 下比 ordinary KD 保留更多 risk–coverage 行為。

**因此 DK-CAST 文獻 gate 的判準要對齊此 intent**：不只問「DK-CAST 是否做過 compression-aware KD」（已知有），而是問「是否已**評估或最佳化壓縮下的 external selective-risk transfer / calibration / AURC / confidence preservation**」。
- 若已有 → 「發現」不新、「對領域有用」賣點垮 → KILL D1-P，回 D1-C。
- 若僅報 EER/codec-robustness → D1-P residual gap 存活，novelty 限縮為「compression × external selective-risk transfer」。

## 兩個 Claude 已加的 D1-P 內生 gate（提醒，見 2205）
- discrimination-matched confound：H1 只有 teacher/student AUROC matched 時才成立。
- H1-before-H2 定序：先測「壓縮有沒有破壞 reliability」，再建 loss。

## 狀態
兩條只讀文獻 gate（D1-P DK-CAST 全文 / D1-C P1-P2+soundness，後者在 2015 handoff）並行續行。**pilot 維持暫停。** 正式定題仍待作者 + gate 結果。
