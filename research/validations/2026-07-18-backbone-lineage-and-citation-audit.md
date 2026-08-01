# Backbone lineage 與 citation audit

- 日期：2026-07-18
- 模式：Validate
- 問題：哪些英語 LibriSpeech-only SSL checkpoint 能避開 ASVspoof 5 禁止的 MLS／LibriLight upstream overlap？§16.7／§19 的三組引用應如何更正？
- 證據基礎：ASVspoof 5 Phase-2 Evaluation Plan、原始模型論文與官方 model card、IEEE／ISCA／arXiv／DBLP metadata；搜尋日 2026-07-18。

## 結論

**Verified — 可選的 3 個 lineage-clean base checkpoint：**

1. `facebook/wav2vec2-base`（首選）：wav2vec 2.0 BASE，LibriSpeech 960 h 自監督預訓練。
2. `facebook/hubert-base-ls960`（第一替代）：HuBERT BASE，LibriSpeech 960 h。
3. `microsoft/wavlm-base`（第二替代）：WavLM Base，LibriSpeech 960 h。

三者的已公開預訓練 lineage 都不含 MLS 或 LibriLight；ASVspoof 5 evaluation plan 又明文允許 LibriSpeech 及其預訓練模型，因 evaluation speakers 與 LibriSpeech 的重疊已被移除。因此，**在精確 checkpoint 層級**三者符合計畫要求。

但這只解除 base SSL backbone 的 blocker。完整 teacher 必須另外證明：ADD head／fine-tuning 只用允許資料、沒有隱藏的 MLS／LibriLight 衍生模型或資料增強，並固定 revision 與權重 hash。`lineage-clean` 也不等於 teacher 一定夠準；仍須通過既定 teacher reproduction／quality gate。

## 1. 規則基準

ASVspoof 5 Phase-2 Evaluation Plan 的 open-condition 規則要求：

- **Verified：**不得使用與 evaluation data 重疊的資料或系統；同一 speaker 的不同 utterance 也算重疊。
- **Verified：**LibriLight、MLS English、MUSAN speech 及由它們衍生的模型被禁止。
- **Verified：**Common Voice、較早的 VCTK-based ASVspoof datasets 被允許。
- **Verified：**LibriSpeech 與在 LibriSpeech 上預訓練的模型被明文允許，理由是 evaluation speakers 中與 LibriSpeech 重疊者已移除。

來源：[ASVspoof 5 Phase-2 Evaluation Plan](https://www.asvspoof.org/file/ASVspoof5___Evaluation_Plan_Phase2.pdf)、[ASVspoof 5 dataset paper](https://arxiv.org/html/2502.08857)。

## 2. 精確 checkpoint audit

| checkpoint | 已公開 pretraining corpus | MLS／LibriLight | ASV5 plan | 判定與用途 |
|---|---|---:|---:|---|
| `facebook/wav2vec2-base` | LibriSpeech 960 h；pretraining-only BASE | 無 | 允許 | **PASS／首選**；避免把 ASR fine-tuning 混入 teacher 定義 |
| `facebook/hubert-base-ls960` | LibriSpeech 960 h | 無 | 允許 | **PASS／第一替代**；必須保留完整 `-ls960` 名稱 |
| `microsoft/wavlm-base` | LibriSpeech 960 h | 無 | 允許 | **PASS／第二替代**；不可誤換成 Base+ |
| `facebook/data2vec-audio-base` | LibriSpeech 960 h | 無 | 允許 | **PASS／reserve**；為控制矩陣大小，暫不列前三 |
| `facebook/wav2vec2-base-960h` | LibriSpeech 960 h 預訓練，再作 960 h ASR fine-tuning | 無 | 允許 | lineage clean，但本題 feature teacher 優先用 pretraining-only `facebook/wav2vec2-base` |
| wav2vec 2.0 `lv60`／Libri-Light variants | Libri-Light 60k h | **有** | 禁止 | **REJECT** |
| HuBERT Large `ll60k` variants | Libri-Light 60k h | **有** | 禁止 | **REJECT** |
| `microsoft/wavlm-base-plus`／WavLM Large | 約 94k h mixture，含 Libri-Light 等 | **有** | 禁止 | **REJECT** |
| XLS-R family | 大型 multilingual mixture，含 MLS | **有** | 禁止 | **REJECT** |

原始證據：[wav2vec 2.0 paper](https://proceedings.neurips.cc/paper/2020/hash/92d1e1eb1cd6f9fba3227870bb6d7f07-Abstract.html)、[`facebook/wav2vec2-base`](https://huggingface.co/facebook/wav2vec2-base)、[HuBERT paper](https://arxiv.org/abs/2106.07447)、[`facebook/hubert-base-ls960`](https://huggingface.co/facebook/hubert-base-ls960)、[WavLM paper](https://arxiv.org/abs/2110.13900)、[`microsoft/wavlm-base`](https://huggingface.co/microsoft/wavlm-base)、[data2vec paper](https://proceedings.mlr.press/v162/baevski22a)、[`facebook/data2vec-audio-base`](https://huggingface.co/facebook/data2vec-audio-base)。

### 完整 teacher lineage contract

Phase 0 前，每個 teacher 都要有一列不可省略的 manifest：

`exact model id → revision/commit → model-file SHA-256 → SSL pretraining corpora → ADD fine-tuning corpora → augmentation/external model corpora → holdout overlap result`

**Stop condition：**任何環節 Unknown 且可能包含 MLS English、LibriLight、MUSAN speech、ASVspoof 5 evaluation speaker／utterance，該 teacher 不得進 confirmatory test。

建議先只實作 `facebook/wav2vec2-base`；若 teacher quality gate 失敗，再依序切換 HuBERT BASE、WavLM Base。不要同時把三者變成新的模型搜尋主題。

## 3. Citation 核對

### 3.1 Kwok：是兩篇不同論文，不是 venue／題名誤植

**Verified — ICASSP 2025（calibration／reliability 用）：**

> Kwok Chin Yuen, Duc-Tuan Truong, and Jia Qi Yip. “Robust Audio Deepfake Detection using Ensemble Confidence Calibration.” *ICASSP 2025 – 2025 IEEE International Conference on Acoustics, Speech and Signal Processing*, pp. 1–5. DOI: [10.1109/ICASSP49660.2025.10889972](https://doi.org/10.1109/ICASSP49660.2025.10889972).

**Verified — Interspeech 2025（cross-dataset evaluation 用）：**

> Chin Yuen Kwok, Jia Qi Yip, Zhen Qiu, Chi Hung Chi, and Kwok Yan Lam. “Bona fide Cross Testing Reveals Weak Spot in Audio Deepfake Detection Systems.” *Interspeech 2025*, pp. 2230–2234. DOI: [10.21437/Interspeech.2025-172](https://doi.org/10.21437/Interspeech.2025-172).

§19 若談 ensemble confidence calibration，應引用 ICASSP 論文；若談 bona-fide／cross-dataset heterogeneity，才引用 Interspeech 論文。若兩個主張都保留，就在 bibliography 分列兩筆。

### 3.2 Zhou & Wang：完整題名與狀態

**Verified：**

> Jingwen Zhou and Mingzhe Wang. “When EER Hides Deployment Failure: Auditing Threshold Transfer and Unlabeled Score Calibration for Speech Deepfake Detectors.” arXiv:2606.21584, version 1, submitted 19 June 2026. DOI: [10.48550/arXiv.2606.21584](https://doi.org/10.48550/arXiv.2606.21584).

截至搜尋日只查得 arXiv preprint，故不可寫成已 peer-reviewed／已正式發表。其內容直接涵蓋 threshold transfer 與 unlabeled score calibration，應繼續作為 closest-work／positioning 壓力測試，而非一般背景引用。

來源：[arXiv record](https://arxiv.org/abs/2606.21584)。

### 3.3 Xu ICPR：作者、題名、年份與 DOI

**Verified：**

> Yi Xu, Jian Pu, and Hui Zhao. “Knowledge Distillation with a Precise Teacher and Prediction with Abstention.” *2020 25th International Conference on Pattern Recognition (ICPR)*, pp. 9000–9006. DOI: [10.1109/ICPR48806.2021.9412696](https://doi.org/10.1109/ICPR48806.2021.9412696).

會議名稱保留 “2020”，但會議實際在 2021 年舉行／出版，DOI 也標 2021。bibliography 應依既定 style 統一；建議 publication year 寫 2021，booktitle 保留官方的 “2020 25th … (ICPR)”。此作把 knowledge distillation 與 abstention 結合，是視覺領域的方法層 collision，不是 ADD-specific 的直接先例。

## 4. 四層 novelty 影響

| 層級 | 此次新增證據後的狀態 | 理由 |
|---|---|---|
| 問題層 | **Partially supported** | deployment threshold／selective transfer 問題真實，但 Zhou & Wang 已直接處理 threshold transfer |
| 場景層 | **Promising, not verified gap** | lineage-disjoint unseen generator family + source-frozen policy 的精確設定仍可辨識，但需以 manifest 證明 |
| 方法層 | **Known components** | calibration、KD、abstention／selective prediction 均有先例；Xu 顯示 KD+abstention 的 generic 組合也已存在 |
| 證據／評估層 | **Potential contribution** | 可重現 lineage audit、family-level transfer、固定 policy 與部署失敗呈現仍可能構成扎實增量 |

這支持「replication-plus-improvement／更嚴格驗證」定位，不支持宣稱發明 KD、calibration 或 abstention。

## 5. Recommendation 與下一個最小步驟

- **Recommendation：**§6 固定首選 `facebook/wav2vec2-base`，預註冊 HuBERT BASE、WavLM Base 為按 gate 切換的 alternates。
- **下一個最小驗證：**在不下載模型前，為最終選定的 ADD teacher checkpoint 補齊 fine-tuning corpus、external components、revision、license；之後才下載並算 SHA-256。
- **Pivot condition：**三個 base checkpoint 若都無法產生通過 quality gate 的 teacher，改變 teacher architecture／task formulation，不可用含 MLS／LibriLight 的大型 checkpoint 偷渡過關。

## 未解不確定性與搜尋限制

- Model card 不能證明任意第三方 fine-tuned teacher 的完整 lineage；目前 PASS 只適用上述精確 base checkpoint。
- 此次未下載模型權重，尚無 revision pin 或權重 SHA-256。
- 來源搜尋以官方／原始出版資訊為主；Zhou & Wang 的 publication status 可能日後改變，定稿時需重查。

## Project-state 影響

本驗證不改作者專屬的 `DECISIONS.md`。它將「XLS-R hard blocker」改成「可由 LS960-only exact checkpoint 解決的設計約束」；題目仍是 GO、實驗仍是 CONDITIONAL GO。待作者／Claude 把 exact checkpoint 和 gate 正式納入共識計畫後，再同步 `PROJECT.md`／`TASKS.md`。
