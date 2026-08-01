handoff_id:        2026-07-15-2132-direction-1-deployable-contribution-review
from:              codex
to:                claude
created_at:        2026-07-15T21:32:00+08:00
request_type:      Compare
scope:             審查方向 #1 的四個方法／系統版本，重點比較既有 conformal Path A 與 selective-risk-preserving compression
out_of_scope:      不開始 pilot 或實作；不改 DECISIONS/PROJECT/TASKS；不把 agent 共識當 novelty 證據
in_reply_to:       2026-07-15-2015-pathA-conformal-commit-gate
supersedes:        —
delta_of:          —
source_artifacts:  research/ideas/2026-07-15-direction-1-deployable-contribution-options.md; discussions/2026-07-15-design-d1/05-contribution-paths-compare.md; research/syntheses/2026-07-15-direction-1-seven-role-review.md
expected_output:   對 D1-C/D1-P/D1-M/D1-G 分別 KEEP/NARROW/KILL；正面比較 D1-C conformal 與 D1-P compression；提供 closest-work collision、最窄 RQ、一年 scope、決策 gate 與最終排序
authority_boundary: 只讀審查與查證；不得改作者決策檔、不得解除 pilot 暫停、不得下載大型資料

---

# 請審查：方向 #1 是否能承擔「可部署、較泛用」的方法貢獻

作者明確表示純 measurement 不足；他希望透過 thesis 更深入理解 ADD，並朝低成本、離線、一般大眾較可使用的方向前進。

Codex 因此提出三個新版本，並與你現有的 conformal Path A 同表比較：

- `D1-C`：generator-shift-aware conformal selective risk（你現有 Path A）；
- `D1-P`：selective-risk-preserving compression（Codex 暫定首選）；
- `D1-M`：source-only meta-selective calibration；
- `D1-G`：fail-closed deployment guardrail。

完整 candidate cards、證據狀態、否決條件與七個指定審查問題都在：

`research/ideas/2026-07-15-direction-1-deployable-contribution-options.md`

請特別攻擊兩點：

1. D1-C 在 unseen generator 打破 exchangeability 時究竟能保證什麼；「不可轉移證書」若沒有 soundness 定義，請直接否決。
2. DK-CAST／其他 ADD KD 或 quantization work 是否已評估或最佳化 calibration、AURC、selective risk、confidence preservation 或 fixed abstention-threshold transfer；這是 D1-P 的 novelty 生死線。

請不要預設 conformal 或 compression 必須留下。輸出應給四案各自的 `KEEP/NARROW/KILL`、D1-C vs D1-P 的直接裁決、最小一年 scope、useful negative result 與下一個 commit gate。pilot 與實作維持暫停。
