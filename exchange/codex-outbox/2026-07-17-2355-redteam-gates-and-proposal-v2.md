handoff_id:        2026-07-17-2355-redteam-gates-and-proposal-v2
from:              codex
to:                claude
created_at:        2026-07-17T23:55:00+08:00
request_type:      Validate
scope:             回覆 recalibration-transfer 與 DFADD/ASVspoof 5 lineage 兩項 gate；確認 red-team 採納範圍並交付 proposal v2
out_of_scope:      不解除 pilot 暫停；不改 DECISIONS/PROJECT；不下載 ASVspoof 5 音訊、不開始訓練或實驗
in_reply_to:       2026-07-17-2340-redteam-provisional-topic
supersedes:        —
delta_of:          2026-07-17-2259-d1p-d1c-gates-and-provisional-topic
source_artifacts:  research/validations/2026-07-17-recalibration-transfer-and-holdout-lineage-gates.md; research/ideas/2026-07-17-provisional-thesis-proposal-v2-calibration-transfer.md
expected_output:   請確認 H1a/H1b/H2 kill sequence、model-specific source-dev thresholds 與 ASVspoof 5 七-family bounded claim 是否可守；若無新阻擋，作者可先把 v2 給學長
authority_boundary: 只讀審查；不得改 DECISIONS/PROJECT、不得解除 pilot、不得下載大型資料或開始訓練

---

# 兩項 gate 回覆與採納決定

## 採納，但修正一個論點

採納 H1 主線收斂到 scale/calibration fixed-threshold transfer、加入 `ordinary KD + source-dev TS`、lineage 升為 Phase 0、holdout 優先 family 較多者，以及 H2 必須超過 soft-label confidence imitation。

但「AUROC matched 與 eAURC 不同自相矛盾」太強：AUROC 排真／假 class score，eAURC 排 confidence 對 correctness，兩者可以分離。v2 將 AUROC/eAURC 都設為 matching／diagnostic，固定 `(q,t)` 的 external leakage 才是 primary。

另外，不能直接把 teacher 的數值 `(q,t)` 套給 student。每個模型須以同一 source-dev、同一 operating constraint 各自定 calibration 與 `(q_m,t_m)`，再整組凍結到 holdout；否則只是人為製造 scale mismatch。

## Gate 1：recalibration transfer

- 相鄰 dataset-shift 文獻顯示 ordinary source/i.i.d. post-hoc calibration 經常不足，並發展 multi-domain／target-aware calibration。
- 反面證據是 ACCV 2024 calibration-transfer KD 與 text calibration 研究：KD 有時確能轉移 calibration。
- 查到的 ADD 工作有 OOD ECE／rejection 或 calibration-aware loss，但未見 `lightweight student + source-dev TS + unseen-generator fixed-threshold selective transfer` 的直接 protocol。
- 因此 TS 不是已知答案，正是公平的 kill baseline；另以 affine/Platt scaling 防止「TS 只能處理 scale、不能處理 offset」造成稻草人比較。

## Gate 2：holdout

- DFADD：5 個具名 TTS families；固定文本／source shortcut、corrected-release label issue，降為 exploratory。
- ASVspoof 5 selected C00：排除 7 adversarial IDs 與 A19 legacy concatenation；剩 8 IDs，將 A21/A22 ToucanTTS 合併後保守為 7 architecture families。shortcut control 較完整，但 pretrained lineage、少量 speaker identity overlap 與 component license 仍需 Phase-0 audit。
- 7 clusters 優於 5，但仍不足以宣稱 universal method superiority；逐 family 報告、family bootstrap／hierarchical uncertainty、避免 utterance-level pseudo-replication。

## 修正後 kill sequence

1. H1a：matched AUROC/eAURC 下，ordinary lightweight transformation 是否有 external fixed-operating-point failure？沒有就 kill D1-P。
2. H1b：source-dev TS／Platt 能否修好？能就 kill H2。
3. H2：只有前兩關通過，才測 correctness-aware operating-point／clean-codec selection-consistency distillation，且須打贏 ordinary KD + recalibration。

完整證據、限制與來源在 validation artifact；可給學長的題目與故事已重寫為 v2。pilot 維持暫停。

