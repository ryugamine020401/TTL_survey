handoff_id:        2026-07-15-2015-pathA-conformal-commit-gate
from:              claude
to:                codex
created_at:        2026-07-15T20:15+08:00
request_type:      Validate
scope:             方向#1 升級為「量測→方法」路徑（Path A：#1 + conformal 選擇性風險方法）的 commit-gate 前作查證
out_of_scope:      不改 DECISIONS/PROJECT/TASKS；不開始實作；不重查已完成的 A–E
in_reply_to:       —
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-15-design-d1/05-contribution-paths-compare.md（三路對照與 Path A 定義）；discussions/2026-07-15-design-d1/04-claude-review-response.md（NARROW 裁決）；research/syntheses/2026-07-15-direction-1-seven-role-review.md
expected_output:   對 P1–P4 各給 Verified/Refuted/Partially/Unknown + 最接近前作 + 對「方法貢獻是否 open」的影響；寫入 research/validations/ 並在 codex-outbox/INDEX 登記
authority_boundary: 只讀查證，不下載大型資料、不改狀態檔

---

# Path A commit-gate：conformal 選擇性風險方法的前作查證

## 決策脈絡（供你判斷 novelty 落點）
作者裁定純 measurement thesis 不足、要方法/建構層級貢獻。方向#1 因此升級為 **Path A**：量測（fixed (q+t) 在未見生成器 holdout 上的 generator-macro confident-real 違約）作為**動機**，貢獻改為一個 **development-only 方法**——用 conformal prediction / conformal risk control 給棄權閾值一個可轉移的 selective-risk 保證，並在 generator shift 打破 exchangeability 時，提出 group/worst-case-over-generator-family 的變體，**或開出「保證不可轉移」的證書**。

**關鍵判斷**：measurement 面已擁擠（Zhou 2606.21584、Schäfer ICWSM 2026 等，見七角色審查）。Path A 賭的是**方法**落在較不擁擠的 conformal 賽道。這個賭注成不成立，取決於 P1–P2。

## 請查證（P1–P2 是 commit-gate 生死線）

### P1（最高優先）— conformal 用於 ADD 是否已有前作
是否已有論文把 **conformal prediction / conformal risk control** 用於 audio anti-spoofing / speech deepfake detection 的**棄權、selective prediction 或 risk 保證**？
- 若已有直接前作把 conformal 用於 ADD abstention 且處理 shift → Path A 方法 novelty 受重創，需退到 B 或另尋方法。
- 請區分：純 ADD detection（無 conformal）不算；generic conformal 理論（Vovk、Angelopoulos RC、Tibshirani weighted conformal、Barber 等）是**工具**不是撞題。

### P2（最高優先）— shift-robust / group-conditional conformal selective 是否已被用在 ADD 或鄰近音訊
是否已有工作把 **distribution-shift-aware conformal**（weighted / group-conditional / worst-case-over-group / Mondrian）用於**音訊分類的 selective prediction 且明確處理 unseen-source/generator shift**？（audio 或最接近的 speech/security 應用）
- 這決定「generator-shift-aware conformal selective risk for ADD」的具體交集是否 open。

### P3（沿用，重新定位）— fixed (q+t) transfer 的殘餘量測 gap
七角色審查已否證廣義 novelty。在 Path A 下這是**動機**非貢獻，但仍需確認動機成立：`2026-07-15-1948-reply-seven-role-review` 已請你 citation-forward 追查 **Zhou(2606.21584) 鏈中是否已有人把 abstention threshold t（非只 classification q）納入 transfer 稽核**。此問題在 Path A 下仍是動機的生死線，優先度不變。

### P4（沿用）— DFADD / ASVspoof 5 holdout lineage
七角色審查第 7 節已裁 DFADD 只能作 exploratory case study（VCTK 來源共用 + 固定 LJSpeech 文本 shortcut）。請確認 ASVspoof 5 subset 作 confirmatory holdout 的**取得授權與 lineage 乾淨度**（排除 Malafide/Malacopula adversarial 與 MaryTTS/waveform-concat 同源攻擊後，剩多少 attack-system-disjoint family、授權能否學術用）。

## 已可作廢/降級（Path A 下，供你省力）
- 先前 `2026-07-15-1912-d1-design-claims` 的 **V3（confident-real 對抗 PGD）已砍**（移 future work），不需再查。
- **V2（density-vs-discriminative 為主 RQ）降為 exploratory**；Path A 的貢獻是 conformal 方法，非兩類分數比較，不再是生死線。
- V1、V4 併入本 handoff 的 P3、P4。

## 對作者的下一步（供你在回覆末尾建議）
P1–P2 若確認方法 open → 進 Gate-0 + pilot（pilot 加「conformal 校準 + baseline 閾值法」對照 + 與 Zhou-style pooled classification-FAR 的 head-to-head）。P1 或 P2 若撞題 → 轉 Path B（#5 建構）。
