# 資料集 Delta：新近性偏好與免申請存取門檻

日期：2026-07-18  
模式：Validate + Compare + Decide  
delta_of：`research/validations/2026-07-18-final-topic-assessment-selective-policy-transfer.md`  
判定：**將「免人工申請／免等待」升格為 critical-path hard gate；在通過效度與存取 gate 的資料集中，優先採用最新者。**

## 1. Inquiry

作者新增的執行限制是：資料集應盡量新，但不接受需要寄信、審核資格、簽 DUA、等待核准、參賽後才取得，或最終標籤仍隱藏的資料集。本文查證目前候選的公開狀態，並決定其在 thesis plan 中的角色。

這項限制不等於「日期最新者自動勝出」。排序規則應為：

1. 先通過研究效度與 pretraining/data-lineage gate；
2. critical path 必須可立即取得，不等待人工核准；
3. 再比較發布時間、generator metadata、混淆、授權清晰度、容量與算力成本；
4. 只有前述條件相近時，才以較新者優先。

## 2. Access gate

| 等級 | 定義 | Thesis 角色 |
|---|---|---|
| **A — direct** | 匿名或公開連結可直接下載；無表單、人工審核或資格判定 | **critical path 必須使用 A** |
| **B — account-only** | 只需免費帳號／登入或接受標準條款；無人工審核與等待 | 只作 optional/secondary；不得成為唯一 confirmatory source |
| **C — approval/gated** | 需寄信、申請、資格審核、邀請、DUA countersignature，或 final labels/data 只給合格參賽者 | **排除於 critical path** |

補充：直接下載不表示可不管 license、資料來源或模型預訓練重疊；這三項仍是獨立 gate。

## 3. 查證結果

| Dataset | 新近性／狀態 | 存取與規模 | 效度／執行風險 | 決定 |
|---|---|---|---|---|
| **ASVspoof 5** | 2024 公開資料；2025/2026 有正式 challenge analyses | Zenodo 可直接下載，**A**；約 142.3 GB；ODC-By 1.0 | attack/protocol metadata 完整；但 confirmatory backbone 不得衍生自 MLS/LibriLight。現行 XLS-R 組合有 upstream-overlap blocker | **保留 primary confirmatory 首選**，先換 lineage-clean backbone；不需為既有資料申請。官方頁面所述寄信只適用於要求建立 spoofed data，不是下載既有 corpus |
| **XMAD-Bench** | 2025 preprint，EACL 2026 accepted | GitHub/Hugging Face/Drive 直接提供，**A**；約 61.3 GB | 很新、跨語言且 split 明確；但 cross-domain 同時改變 language、real-source、speaker、generator，因果歸因容易混淆。dataset/license metadata 仍需釐清；checkpoint corpus overlap 也需 audit | **newer direct-access fallback／secondary**；不能只因較新就取代 ASVspoof 5。通過 license、confounding、lineage audit 後才可升 primary |
| **DFADD** | IEEE SLT 2024；Hugging Face 2025 更新 | 直接下載，**A**；目前頁面約 42.7 GB，MIT metadata | 已知 LJSpeech/VCTK real-vs-fake source shortcut 風險；需固定 revision 並核對 corrected release | **exploratory replication**，不作唯一 confirmatory evidence |
| **MLAAD v9** | 持續更新；v9 宣稱 >1,000 h、>50 languages、>175 TTS models | Hugging Face；官方說明需帳號登入，**B**；CC BY-NC 4.0 | 只有 synthetic audio；real M-AILABS 要另取，組合與 provenance burden 高 | optional source-tracing／secondary，不放 critical path |
| **MLAAD-tiny** | MLAAD 的小型 teaching/debug subset | 可直接取得，**A**；約 4.2 GB；CC BY-NC 4.0 | 約 12.4k files、64 TTS；官方定位是 prototyping/debugging，代表性不足 | **Stage-0 plumbing only**；不可支撐最終 scientific claim |
| **AUDETER** | 2025，涵蓋近期 TTS/vocoder | Hugging Face 直接提供，**A**；約 1.08 TB；CC BY-NC-ND 4.0 | 只有 fake clips，real audio 須另取；容量對一人一年過大 | **排除**，新近性不足以抵消容量與配對成本 |
| **RADAR 2026／同類 challenge-gated final set** | 2026，最新 | evaluation data/labels 依 eligibility 或 challenge phase 提供，**C** | 時程與可得性由外部主辦方控制；不能保證 thesis critical path | **排除 critical path**；日後若完整公開才重新評估 |

### 關鍵查證

- **Verified：ASVspoof 5 現有資料免申請。** Zenodo record 有逐檔下載與公開授權；不需要人工核准。這符合作者的免等待要求，但完整資料仍大，不應在 metadata gate 前全量下載。
- **Verified：XMAD-Bench 免人工申請且更新。** 官方 repo 與 Hugging Face 提供下載，適合作備援；但「跨域」split 同時改變多個因素，不能直接把差異全歸因於 unseen generator。
- **Verified：DFADD 免人工申請。** 它適合重現與 exploratory check；已記錄的 source shortcut 使其不足以單獨承擔 confirmatory claim。
- **Verified：MLAAD 完整版無人工審核，但有帳號與資料拼接摩擦。** 因此列 B，不是作者所要的最乾淨 critical path。
- **Verified：最新 challenge data 不等於現在可用。** 需 eligibility、等 challenge release 或沒有公開 final labels 的 corpus，全部依作者規則排除。
- **Inference：ASVspoof 5 仍是目前最穩妥的 primary。** 它不是候選中日期最新，但在 direct access、正式 protocol、attack metadata、授權清晰度與既有 plan 相容性上整體較強；真正 blocker 是 checkpoint lineage，不是資料申請。

## 4. 對 plan v2／最終認定的修正

### 4.1 Dataset role map

建議下一版固定：

- **source baseline / reproducibility anchor**：暫保留 ASVspoof 2019 LA；若作者非常重視 source 也要更新，另比較「ASVspoof 5 train/dev → eval」方案，但不可在未審查 split lineage 前直接替換。
- **primary confirmatory**：ASVspoof 5 eval 的預先登記 subset，前提是採用 ASVspoof-5-compatible、pretraining-lineage-clean backbone。
- **newer direct-access fallback／secondary**：XMAD-Bench；先解決 license、cross-domain confounding 與 backbone-pretraining overlap。
- **exploratory replication**：DFADD corrected/pinned release。
- **plumbing only**：MLAAD-tiny。
- **不列 critical path**：需要帳號拼接的完整 MLAAD、1.08 TB 的 AUDETER，以及申請／資格／hidden-label challenge sets。

### 4.2 新增 hard gate

Plan v3 應明文加入：

> All datasets required for the preregistered critical path must be available by direct public download without manual application, eligibility review, invitation, or unreleased labels. Among datasets that pass access, license, lineage, confounding, and feasibility gates, prefer the most recent release.

這個 gate 也要有 fallback：若 primary dataset 的公開連結失效或 license 改變，直接切換到已完成 audit 的 A 級候選，不等待申請。

### 4.3 下載順序

本次**沒有下載任何資料集**。若作者之後授權，最小且可逆的順序是：

1. 先下載 protocol／metadata，不下載 audio；
2. 完成 generator、speaker/content、source-corpus、license 與 checkpoint-pretraining lineage manifest；
3. 以 MLAAD-tiny 或極小公開 subset 驗證 pipeline；
4. 通過 gate 後才抓 primary 所需 shards，不預設下載完整 142.3 GB；
5. 大型 fallback 只在 primary 失敗時下載。

## 5. Validation contract

### 下一個最小步驟

1. Claude 將 access gate 與 dataset role map 整合進 plan v3／共識文件；
2. 對 ASVspoof 5 列出實際要用的 protocol rows、audio shards 與估計容量；
3. 列出 2–3 個 LibriSpeech-only 或其他可證明 lineage-clean 的 backbone 候選；
4. 對 XMAD-Bench 做一次 license、split-confound 與 pretraining-overlap audit，讓它成為真實可切換的 fallback；
5. 作者確認後，再更新 `PROJECT.md`／`TASKS.md` 並授權最小下載。

### Pass

- primary 與至少一個 fallback 都是 A 級；
- 無人工審核、等待名額或 hidden final labels；
- license 允許 thesis research 與結果重現；
- backbone 與 holdout upstream lineage 可辯護；
- confirmatory split 能把 generator-family claim 與 language/source/speaker confound 分開；
- 所需儲存、解壓暫存與訓練時間在單機範圍內。

### Kill / pivot

- ASVspoof 5 找不到 lineage-clean backbone：切到已 audit 的 XMAD-Bench 或其他 A 級 holdout；若保留 ASVspoof 5，只能降為 contaminated sensitivity。
- XMAD-Bench license 或 confounding 無法解決：維持 secondary，不升 primary。
- 候選變成 C 級或公開日期不確定：立即移出 critical path，不等待。
- 新資料集雖更新但需要 >1 TB、缺 real data 或沒有可重現 protocol：不因「新」而納入。

## 6. Project-state impact

- 本文是前一份最終認定的執行條件 delta，不改變「題目方向 GO；實驗規格 CONDITIONAL GO」。
- 現在不修改作者專屬的 `DECISIONS.md`，也不啟動資料下載。
- Claude 與作者接受 plan v3 後，`PROJECT.md` 應加入 direct-access hard gate；`TASKS.md` 應把 protocol-only audit、checkpoint lineage 與 fallback audit 排在任何大檔下載之前。

## 7. Evidence basis and limitations

查證日期：2026-07-18。來源以官方 dataset page、官方 challenge page、作者維護 repository、Hugging Face dataset card 與原始論文為主。容量是各官方頁面在查證日顯示值，可能隨 revision 改變；實驗應 pin dataset revision。未對 corpus audio 做抽樣，因此音檔品質、metadata 一致性與實際解壓容量仍是 Unknown。

- ASVspoof 5 Zenodo：https://zenodo.org/records/14498691
- ASVspoof 5 Phase-2 Evaluation Plan：https://www.asvspoof.org/file/ASVspoof5___Evaluation_Plan_Phase2.pdf
- XMAD-Bench paper：https://arxiv.org/abs/2506.00462
- XMAD-Bench official repository：https://github.com/ristea/xmad-bench
- XMAD-Bench dataset：https://huggingface.co/datasets/unibuc-cs/XMAD-Bench
- DFADD paper：https://arxiv.org/abs/2409.08731
- DFADD dataset：https://huggingface.co/datasets/isjwdu/DFADD
- MLAAD official page：https://deepfake-demo.aisec.fraunhofer.de/mlaad
- MLAAD dataset：https://huggingface.co/datasets/mueller91/MLAAD
- MLAAD-tiny：https://huggingface.co/datasets/mueller91/MLAAD-tiny
- AUDETER：https://huggingface.co/datasets/wqz995/AUDETER
- RADAR 2026：https://sites.google.com/view/radar2026

