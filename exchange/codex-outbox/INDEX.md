# codex-outbox — INDEX（僅由 Codex 寫入）

Codex 送給 Claude 的 handoff／回覆清單。Claude 只讀本檔與本 outbox 的檔案。

## 最新狀態

已完成 plan v3 的 backbone、ASVspoof 5 lineage、XMAD fallback 與 citation 查證：**題目方向 GO；ASVspoof 5 實驗規格仍為 CONDITIONAL GO**。`facebook/wav2vec2-base`、`facebook/hubert-base-ls960`、`microsoft/wavlm-base` 均為 LibriSpeech-960-only 且符合官方 plan，可解掉 XLS-R/MLS blocker；但完整 ADD teacher lineage/hash 與 audio shortcut probes 仍是 hard gates。官方 protocol 重算 C00 selected spoof 69,233、bona fide 35,149；A17 需 include/exclude sensitivity，A29 的 XTTS 上游含 LibriLight。XMAD-Bench 因 license metadata 不一致、cross-domain 多重 confounding 與 M-AILABS/LibriSpeech overlap Unknown，只能作 conditional compound-shift fallback。citation corrections 已送 Claude 統整。

## Handoff 登記

| handoff_id | 日期 | request_type | 狀態 | 指向的正式 artifact | 說明 |
|---|---|---|---|---|---|
| `2026-07-18-2140-backbone-lineage-manifest-citations` | 2026-07-18 | Validate | 待 Claude 統整 | `research/validations/2026-07-18-backbone-lineage-and-citation-audit.md`; `research/validations/2026-07-18-asvspoof5-xmad-lineage-manifest.md` | 選定三個 LibriSpeech-960-only exact backbones；以官方 protocol 固定 ASV5 C00 counts／A17-A29 lineage；XMAD 降為 conditional compound-shift fallback；更正 Kwok 兩篇、Zhou & Wang 題名／preprint 狀態及 Xu ICPR DOI／年份。 |
| `2026-07-18-1015-dataset-recency-direct-access-delta` | 2026-07-18 | Decide | 待 Claude 統整 | `research/validations/2026-07-18-dataset-recency-direct-access-gate-delta.md` | 將「越新越好，但免申請／免等待」轉成 critical-path hard gate；查證 ASVspoof 5 是 direct download 且保留 primary，XMAD-Bench 作較新 fallback，DFADD exploratory，排除 approval/hidden-label challenge sets 與 AUDETER 等不合一人一年資源者。 |
| `2026-07-18-1009-final-topic-assessment` | 2026-07-18 | Decide | 待 Claude 統整 | `research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md` | 最終判定為題目 GO／實驗 CONDITIONAL GO；新增 XLS-R×ASVspoof5 upstream overlap blocker與四項必修規格，提供修正後 H1a/H1b/H2、validation contract 及 author-owned decision entry。 |
| `2026-07-18-0715-plan-v1-h1b-replication-extension-review` | 2026-07-18 | Validate | 待 Claude 審閱 | `discussions/2026-07-18-codex-review-plan-v1-replication-extension.md` | 驗證 fixed-policy 現實性；指出 H1b 的 TS/Platt 單調等價風險；提出 selective-policy 與 semantic-calibration 兩主軸，請 Claude 檢查公式、closest work、replication-plus-extension 貢獻 bar 並提供 plan redline。 |
| `2026-07-18-0045-priorart-positioning-q1-q3` | 2026-07-18 | Validate | 待 Claude 審閱 | `research/validations/2026-07-18-priorart-positioning-q1-q3.md` | Q1 Partially；Q2 generic method known、broad H2 novelty Refuted；Q3 AURC/risk–coverage known。四層表回填，交集＋方法層改為 Partially；留下 exact external selective-policy transfer 的窄 gap。 |
| `2026-07-17-2355-redteam-gates-and-proposal-v2` | 2026-07-17 | Validate | 待 Claude 確認 | `research/validations/2026-07-17-recalibration-transfer-and-holdout-lineage-gates.md`; `research/ideas/2026-07-17-provisional-thesis-proposal-v2-calibration-transfer.md` | 回覆兩項 gate；採納 calibration-transfer 主線與致命 recalibration baseline，修正 AUROC/eAURC 論點與 model-specific threshold 公平性；ASVspoof 5 C00 暫勝。 |
| `2026-07-17-2259-d1p-d1c-gates-and-provisional-topic` | 2026-07-17 | Validate | 已由 Claude 2340 回覆 | `research/validations/2026-07-17-d1p-d1c-literature-gates.md`; `research/ideas/2026-07-17-provisional-thesis-proposal-selective-reliability-lightweight-add.md` | D1-P gate 存活但縮窄；D1-C P1 no direct hit、P2 generic collision，降為 baseline／備援；請 Claude red-team 暫定題目、H1/H2 與動機故事。 |
| `2026-07-15-2132-direction-1-deployable-contribution-review` | 2026-07-15 | Compare | 已由 Claude 2205/2230 回覆 | `research/ideas/2026-07-15-direction-1-deployable-contribution-options.md` | 四案 D1-C/D1-P/D1-M/D1-G 審查；Claude 排序 D1-P > D1-C > D1-M > D1-G，作者 intent 後續確認 D1-P 為工作主線。 |
| `2026-07-15-1909-direction-1-seven-role-review` | 2026-07-15 | Validate | 已回覆 | `research/syntheses/2026-07-15-direction-1-seven-role-review.md`; `discussions/2026-07-15-design-d1/04-claude-review-response.md` | Claude 已回覆 NARROW；後續方法貢獻爭點由 2132 handoff 接續。 |
| `2026-07-15-1801-codex-config-alignment` | 2026-07-15 | Coordination | 已完成 | `AGENTS.md`; `.agents/skills/develop-thesis-ideas/SKILL.md`; `PROJECT.md` | Codex 端已對齊 B+、嚴格 `DECISIONS.md` 權限及 legacy synthesis 路徑。詳見同名 handoff。 |

## Pre-exchange 回覆

A–E 查證的正式 artifact 位於 `research/validations/2026-07-15-claims-to-verify-a-d.md`；此為 pre-exchange 交付，歷史 request 登記在 `claude-outbox/INDEX.md`。
