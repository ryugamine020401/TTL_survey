handoff_id:        2026-07-18-1030-asvspoof5-lineage-manifest
from:              claude
to:                codex
created_at:        2026-07-18T10:30+08:00
request_type:      Validate
scope:             ASVspoof 5 C00 confirmatory-holdout 的 Phase-0 lineage/shortcut manifest（解鎖 H1a Stage 0.2 的前置）
out_of_scope:      不下載 142GB audio；不改 DECISIONS/PROJECT/TASKS；不跑實驗
in_reply_to:       2026-07-17-2355-redteam-gates-and-proposal-v2
supersedes:        —
delta_of:          —
source_artifacts:  discussions/2026-07-15-design-d1/09-phase0-h1-audit-spec.md（Stage 0.2 前置）；research/validations/2026-07-17-recalibration-transfer-and-holdout-lineage-gates.md（Gate 2）
expected_output:   一份 ASVspoof 5 C00 selected-eval 的 lineage/shortcut manifest（下載小型 protocol/metadata 即可，需作者授權任何下載），供解鎖 Stage 0.2；寫入 research/validations/ 並登記
authority_boundary: 只讀查證 + 小型 metadata（作者授權後）；不下載 142GB audio、不改狀態檔

---

# 請 Codex 做：ASVspoof 5 C00 confirmatory holdout 的 lineage manifest

作者已裁定跑便宜的 H1a/H1b derisking 稽核（見 09 規格）。Stage 0.0–0.1 用 ASVspoof19 LA + In-the-Wild，不需要你；**Stage 0.2 confirmatory 需要 ASVspoof 5 C00 的 lineage manifest 先過**。這是你在 Gate 2 已標為「Phase 0 還要以 protocol manifest 實際核對才能解鎖 pilot」的那份。

## 請核對（小型 protocol/metadata，非 142GB audio；任何下載需作者授權）
就選定的 8 attack IDs（A17、A21、A22、A24、A25、A26、A28、A29；A21/A22 合併，~7 families）：
1. **每 family 實際可用 sample counts**（C00, bona fide + spoof）——供 simulation-based power/precision 判斷 7 clusters 夠不夠。
2. **speaker / content / source overlap**：A17 的 target-speaker overlap 程度；與 ASVspoof19 LA source（本題 teacher 訓練集）是否有 speaker/utterance 重疊——**這關係到「未見 generator」是否也意外「未見 speaker/source」而混淆**。
3. **checkpoint / 外部訓練 corpora lineage**（A17/A28/A29 的 pretrained 模型）——L0–L5，供判斷是否與 teacher 訓練資料共源。
4. **shortcut probes 可行性**：duration/silence/RMS/spectral/ASR-text-ID/speaker-ID 是否能高準確預測 label（若能 → holdout 污染）。
5. **license / attribution**：ODC-By 對 MLS/LibriVox component 的實際條款、可否學術使用、hash。
6. **C00 vs C01–C11**：確認 C00 為 uncompressed 16kHz，channel 效應與 generator 效應可分離（codec 留 secondary）。

## 產出
一份 go/no-go manifest：每 family 可用數 + overlap/shortcut 判斷 + license；標明「Stage 0.2 可解鎖 / 需先處理 X」。若 shortcut 或 overlap 嚴重到污染 confirmatory，回報並建議是否退回 In-the-Wild-only exploratory 或另尋 holdout。

## 平行進度
Claude 這邊同時進行 Stage 0.0–0.1（環境 + teacher 復現 + In-the-Wild 便宜首探），不等此 manifest。
