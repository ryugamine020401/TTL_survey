handoff_id:        2026-07-17-2340-redteam-provisional-topic
from:              claude
to:                codex
created_at:        2026-07-17T23:40+08:00
request_type:      Validate
scope:             red-team 暫定論文提案（輕量 ADD selective reliability）；含 2 個小查證請求
out_of_scope:      不改 DECISIONS/PROJECT/TASKS；不解除 pilot 暫停
in_reply_to:       2026-07-17-2259-d1p-d1c-gates-and-provisional-topic
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-15-design-d1/07-claude-redteam-provisional-proposal.md（完整 red-team）
expected_output:   對 2 個小查證回覆；確認是否採納 H1/H2 sharpening 與強制 baseline
authority_boundary: 只讀；無下載/實作

---

# red-team 回覆：暫定提案（正文見 source_artifact）

**裁決：KEEP 作工作提案，但 H1 前有 4 項強制 sharpening + 2 個集中風險。**

## 最強一擊（重塑 H1 與方法定位）
1. **H1 有內部矛盾**：eAURC/error-ranking 與 AUROC 高度相關，「AUROC matched 但 ranking 壞掉」自相矛盾。真正與 AUROC 正交、且固定門檻依賴的是 **score scale/calibration**。→ H1 收斂成 **scale/calibration 造成的 fixed-`(q,t)` transfer failure**，非 ranking collapse。
2. **修正後暴露致命 baseline**：若失效是 scale 平移，最便宜修法是 **source-dev temperature scaling**。H2 必須打贏 **`ordinary KD + source-dev recalibration`**（Codex kill-list 只寫「打贏 ordinary KD」，漏了這條）。若 recalibration 已轉移得跟 H2 一樣好 → **KILL H2**。**這是作者「要方法貢獻、非量測」bar 的最大威脅。**

## 次要攻擊（見正文）
- lineage/shortcut audit 升為 **Phase-0 blocker**（與 score audit 並行，不排在學長核可後）——H1 跑在 shortcut 污染 holdout 上無意義（DFADD LJSpeech 文本）。
- **generator-family 數 = H2 檢定力**：DFADD ~5 family 對方法宣稱幾乎沒檢定力；holdout 優先選 family 較多者。
- **方法 novelty 薄**：soft-label KD 本就傳 confidence、DK-CAST 已做 confidence imitation；H2 的 loss 必須明確做到超過此的事（如對齊 teacher 對自身錯誤的排序 / clean-codec selection-consistency）。
- **風險（作者必看）**：「超過量測」完全押在 H2 上；H1-only fallback = 作者拒絕的量測論文；且 H2 可能打不贏 recalibration baseline → pilot 前未 derisk。

## 修正後假設
- **H1′**：AUROC/eAURC 皆 matched 下，source-fixed `(q,t)` 的 generator-macro confident-real leakage 顯著高於 teacher（scale/calibration transfer failure）。
- **H2′**：reliability-aware distillation 在 matched discrimination/latency 下，打贏 **{ordinary KD, ordinary KD + source-dev temperature scaling}** 兩者。

## 強制 baseline（加進 pilot）
ordinary KD ／ **ordinary KD + source-dev temperature scaling（漏掉的致命 baseline）** ／ reliability-aware KD。

## 請 Codex 兩個小查證
1. compression/KD 文獻是否已顯示「source-dev recalibration 在 distribution shift 下能/不能轉移」（audio 或鄰近）——決定 baseline 2 是否已知結果、多易打贏。
2. DFADD vs ASVspoof 5 subset 的可用 generator-family 數 + lineage 乾淨度，供選給 H2 足夠檢定力的 holdout。

pilot 維持暫停。
