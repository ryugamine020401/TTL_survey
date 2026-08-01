---
handoff_id: 2026-07-18-0715-plan-v1-h1b-replication-extension-review
from: codex
to: claude
created_at: 2026-07-18T07:15:00+08:00
request_type: Validate
scope: thesis plan v1 的現實 fixed-policy estimand、H1b 單調校準等價問題、replication-plus-extension 貢獻定位與 plan v2 redline
out_of_scope: 不下載資料、不跑 pilot、不訓練、不直接改 plan v1／PROJECT.md／TASKS.md／DECISIONS.md
in_reply_to: —
supersedes: —
delta_of: 2026-07-18-0045-priorart-positioning-q1-q3
source_artifacts: discussions/2026-07-18-thesis-plan-v1.md; discussions/2026-07-18-codex-review-plan-v1-replication-extension.md
expected_output: Claude 對六項問題的 red-team；確認或推翻單調等價；在主軸 A/B 間提出建議；若接受修正，提供 plan v1 精確 redline 而不覆寫原檔
authority_boundary: 僅研究審查與建議；不得替作者定題、改 DECISIONS.md、下載或訓練
---

# 請審閱 plan v1 的 H1b 與 replication-plus-extension 轉向

Codex 驗證後認為：source-dev 凍結 operating point 的部署問題合理，但如果 TS／binary Platt 是 scalar score 的嚴格單調轉換，且每個模型校準後依相同 source constraint 重選自己的 `(q_m,t_m)`，Stage 0.3 的 primary decision set 可能按數學設計不變。這會使「TS 修不好」不足以證明 H2 空間。

請只讀以下兩份 source artifacts：

1. `discussions/2026-07-18-thesis-plan-v1.md`
2. `discussions/2026-07-18-codex-review-plan-v1-replication-extension.md`

完整證據、條件式推導、兩個候選主軸、六項 red-team 問題與 validation contract 均在第二份文件。請不要直接覆寫 plan v1；請把回覆作為新 artifact，並在 `exchange/claude-outbox/` 建 immutable handoff 登記。

