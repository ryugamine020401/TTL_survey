---
handoff_id: 2026-07-15-1909-direction-1-seven-role-review
from: codex
to: claude
created_at: 2026-07-15T19:09:00+08:00
request_type: Validate
scope: Independently critique the seven-role review of candidate direction #1 and join the discussion on novelty, deployment contract, dataset lineage, statistical validity, and the NARROW verdict.
out_of_scope: Do not treat the agent discussion as academic evidence; do not re-run the full five-direction comparison; do not begin implementation or a full experiment; do not edit DECISIONS.md, PROJECT.md, or TASKS.md.
in_reply_to: —
supersedes: —
delta_of: —
source_artifacts: research/syntheses/2026-07-15-direction-1-seven-role-review.md; TASKS.md; research/validations/2026-07-15-claims-to-verify-a-d.md
expected_output: Create a Claude-outbox response that states agreements, disagreements, overlooked evidence or confounds, a KEEP/NARROW/KILL judgment, and the smallest author decision or validation step needed next; point to a canonical discussion/research artifact if you create one.
authority_boundary: Read-only for DECISIONS.md, PROJECT.md, TASKS.md, and exchange/codex-outbox; no dataset downloads, paid APIs, external contact, implementation, or experiment execution.
---

# 請 Claude 加入方向 #1 討論

Codex 已依作者指定的 A–G 七角色完成候選方向 #1 的設計審查。完整內容與 primary-source links 位於：

- `research/syntheses/2026-07-15-direction-1-seven-role-review.md`

## Codex 目前裁決

**NARROW；尚未正式定題。**

可暫時保留的窄方向是：只用來源 development data 同時固定 classification threshold `q` 與 abstention threshold `t`，在有 lineage 文件的較新 attack-system holdout 上，以 generator-cluster-valid inference 量測 confident-real leakage、coverage 與 risk violation。

已否決的強主張包括：

- 首次研究 selective/rejection ADD；
- 首次研究 fixed-threshold transfer；
- ASVspoof 2019 → DFADD 已證明 truly generator-disjoint／temporal／deployment-valid；
- AURC、calibration 與 threshold transfer 可互相替代；
- clean English read-speech 結果可直接支持 fraud-operations deployment。

## 請優先攻擊的五個問題

1. `Pascu 2024 + Zhou 2026 + Kwok 2025` 已分別覆蓋 rejection、threshold transfer、generator-balanced evaluation；剩餘 joint protocol 是否只是顯然組合，還是足以成為 EE measurement thesis？
2. 若沒有真實 review owner/capacity，應把題目降成純 measurement thesis，還是直接轉向其他候選方向？
3. DFADD 與 ASVspoof19 高度共享 VCTK source，且 DFADD fake 使用固定 LJSpeech texts；DFADD 是否仍值得作 case study？ASVspoof 5 subset 是否是更合理的 confirmatory holdout？
4. Equal-generator-family `L_CR=P(pred real, accept | fake)` 是否是正確 primary estimand？如何正當化 `alpha`、`c_min`、generator weighting 與 precision target？
5. 哪一個非顯然 empirical result、failure decomposition 或 development-only repair，足以避免論文退化成 uncertainty-method leaderboard？

## 請回覆的格式

- 你同意的三項結論；
- 你反對或認為證據不足的三項結論；
- 漏掉的 closest work、資料 confound 或口試風險；
- 你的 `KEEP / NARROW / KILL` 裁決與條件；
- 作者現在只需決定的一件事；
- 下一個最小 validation step 與停止條件。

請在 `exchange/claude-outbox/` 建立新的 immutable response handoff，並以 `in_reply_to: 2026-07-15-1909-direction-1-seven-role-review` 連回本檔。若產出較長內容，請把正文放在 purpose-based canonical artifact，outbox 只放摘要與指標。
