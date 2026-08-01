# Phase-0 H1a/H1b 稽核規格（可執行、preregistration-ready）

日期：2026-07-18
目的：用最便宜的實驗，驗證 D1-P 方法貢獻的前兩關——H1a（壓縮是否破壞固定操作點轉移）、H1b（簡單重新校準能否修好）。任一關的結果都可能早殺這個方向，沉沒成本最小。
對齊：proposal v2（`research/ideas/2026-07-17-provisional-thesis-proposal-v2-calibration-transfer.md`）、recalibration/holdout gate、Claude red-team。
紀律：**凍結後才碰 holdout；不得用 holdout 選 layer/threshold/temperature/preprocessing/model。**

## 要驗證的假設
- **H1a**：在 AUROC/EER 落在預設 matching tolerance 內時，輕量 student 各自用 source-dev 決定並凍結的 `(q_m,t_m)`，在未見 generator 上的 **generator-macro confident-real leakage** 顯著高於 teacher。
- **H1b**：只用 source-dev 擬合的 temperature scaling（+ affine/Platt sensitivity）**修不好** ordinary KD/truncation 的 external fixed-threshold reliability 到 teacher 水準。

## 分階段（越前面越便宜，前兩階不需要 ASVspoof 5）

### Stage 0.0 — 環境 + teacher 復現（無 holdout）
- 建 Python/PyTorch/CUDA 環境；取一個**公開 frozen SSL ADD checkpoint**（XLS-R + AASIST 或 XLS-R + linear head，訓於 ASVspoof19 LA）。
- 在 ASVspoof19 LA eval 復現 base discrimination（AUROC/EER 對得上論文才採信）。
- **產出**：可跑的 scoring pipeline + teacher base gate 數字。**GPU：推論級，數小時。**

### Stage 0.1 — H1a 便宜首探（In-the-Wild，exploratory，仍不需 ASVspoof 5）
- 加**一個 truncated lightweight probe**（截短 XLS-R 層 + logistic head；**不需訓練**，最便宜）。
- 每個模型**各自**在 ASVspoof19 LA dev 擬合 calibration + 在固定 source operating constraint（如 source FPR + abstain coverage 目標）下決定自己的 `(q_m,t_m)`；**不得把 teacher 門檻套到 student**。凍結。
- 在 **In-the-Wild** 評估（小、可下載、當作第一個 out-of-domain 探針；generator lineage 不明 → 僅 exploratory，不作 confirmatory）。
- **問**：固定操作點在 matched discrimination 下有沒有退化的**跡象**？有 → 值得投 confirmatory；沒有 → 提早重估。**GPU：推論級，數小時。**

### Stage 0.2 — H1a confirmatory（ASVspoof 5 C00，需 lineage manifest + 授權下載）
- holdout = ASVspoof 5 eval 的 **C00 非 adversarial、非 legacy 子集**（~7 architecture families，見 Codex holdout gate）。
- **前置**：Codex 的 Phase-0 lineage/shortcut manifest 通過（sample counts、attack IDs、speaker/content overlap、checkpoint lineage、license、hash）；作者授權下載（142GB 或先取 eval 子集/metadata）。
- primary metric：每 family `P(accept 且判 real | 實為 fake, g)`，再 family-macro；報 coverage、risk violation、逐 family；**family bootstrap / hierarchical CI**（誠實呈現 ~7 clusters 的寬區間）。
- matching 只用 budget + AUROC/EER equivalence tolerance（**不用 eAURC 當配平變數**，避免 circular）。

### Stage 0.3 — H1b trivial-repair gate
- 對凍結的 student 加 **source-dev temperature scaling**，再加 **affine/Platt** 作 sensitivity；重評 external fixed-policy leakage。
- **問**：簡單重新校準能不能把 student 修回 teacher 的 external reliability？**能 → kill H2**（方法沒必要）；不能 → H2 有空間。

## 必要 baselines（此稽核階段）
frozen teacher／reference ｜ truncated lightweight probe ｜（Stage 1 再加 ordinary KD）｜ + source-dev TS ｜ + Platt sensitivity。

## 決策閘（此稽核輸出）
- Stage 0.1 無退化跡象 → 提早重估方向（省下大檔下載）。
- Stage 0.2 matched discrimination 後**確有** generator-macro 退化，且非 shortcut/teacher-fail 可解釋 → H1a 成立。
- Stage 0.3 簡單 recalibration 已修好 → **kill H2**（退回量測，低於作者 bar → 轉向）。
- H1a 成立 + H1b 顯示簡單修法不足 → **才**進 Phase 1 設計 H2（並先做 method closest-work gate）。

## 環境/資料前置（需作者解鎖）
1. 計算環境：確認在 RTX 4090 機器、Python/CUDA 可用（或授權我建環境）。
2. 公開 checkpoint 來源（XLS-R-AASIST 類）。
3. 下載授權：Stage 0.0–0.1 先授權 **ASVspoof19 LA + In-the-Wild**（數 GB，可直接下載）；**ASVspoof 5（142GB）延到 lineage manifest 過 + 明確授權**。
