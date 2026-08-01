---
handoff_id: 2026-07-18-1015-dataset-recency-direct-access-delta
from: codex
to: claude
created_at: 2026-07-18T10:15:00+08:00
request_type: Decide
scope: 將作者新增的「資料集越新越好，但不接受申請與等待」轉成 plan v3 的 dataset access hard gate、候選排序與 fallback 規則
out_of_scope: 不下載資料、不改 DECISIONS.md、不直接覆寫 thesis plan v2、不解除 checkpoint-lineage blocker
in_reply_to: 2026-07-18-1009-final-topic-assessment
supersedes:
delta_of: 2026-07-18-1009-final-topic-assessment
source_artifacts: research/validations/2026-07-18-dataset-recency-direct-access-gate-delta.md; research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md; discussions/2026-07-18-thesis-plan-v2.md
expected_output: Claude 將 direct-access hard gate、dataset role map、ASVspoof5 primary、XMAD-Bench fallback 與 protocol-first download order 統整進 plan v3／共識文件
authority_boundary: 可提出 plan redline 與資料角色；不得代作者寫 DECISIONS.md、下載 corpus、啟動 pilot 或忽略 license/lineage/confounding gate
---

# Dataset recency / direct-access delta（給 Claude）

作者新增一項硬限制：**資料集盡量新，但 thesis critical path 不可依賴需要寄信、表單審核、資格判定、邀請、DUA countersignature、等待 challenge phase，或 final labels 尚未公開的資料。**

請把下列規則直接併入 plan v3：

> Critical-path datasets must be available by direct public download without manual application or unreleased labels. Among candidates that pass access, license, lineage, confounding, and feasibility gates, prefer the most recent release.

Codex 的查證結論：

1. **ASVspoof 5 現有資料是 direct public download，不需人工申請。** Zenodo 約 142.3 GB、ODC-By 1.0；官方要求寄信是針對請團隊建立 spoofed data，不是下載現有 dataset。因此仍建議作 primary confirmatory。
2. **ASVspoof 5 的 blocker 仍是 XLS-R/MLS upstream overlap，不是 access。** 請在 v3 換成 lineage-clean checkpoint，或更換 holdout；不可因資料可直接下載而略過。
3. **XMAD-Bench 是較新的 direct-access fallback／secondary**（約 61.3 GB），但要先 audit dataset license、cross-domain language/source/speaker/generator confounding 與 backbone-pretraining overlap，不能因較新就自動取代 ASVspoof 5。
4. **DFADD corrected/pinned release** 可 direct download，維持 exploratory replication；已知 source-shortcut 風險使其不能作唯一 confirmatory set。
5. **MLAAD-tiny** 只作約 4.2 GB 的 Stage-0 plumbing；full MLAAD 需要帳號且只有 synthetic audio，列 optional。**AUDETER** 雖新且 direct，但約 1.08 TB、缺 real audio，排除。
6. RADAR 2026 與任何 eligibility/hidden-label challenge dataset 一律排除 critical path，除非日後完整公開後重新 audit。
7. 下載順序必須是 protocol/metadata → lineage/license/confound manifest → tiny plumbing → 作者授權的必要 shards；不要先抓完整 142.3 GB。

完整表格、證據與 pass/kill 條件：

- `research/validations/2026-07-18-dataset-recency-direct-access-gate-delta.md`

本 delta 不改變原判定：**題目方向 GO；實驗規格 CONDITIONAL GO**。它新增的是資料存取與 fallback 約束。

